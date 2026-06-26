#!/usr/bin/env python3
"""
OneDrive Photo Batch Skill Runtime

功能：
- 云端照片筛选（名称/日期/大小/格式/相册）
- 批量 OCR + 索引 + 可选 embedding 语义检索
- full 全量索引（识别后立即删除本地临时文件）
- 哈希去重增量
- 云端 move/upload/delete
- 本地回收站（tmp_photo）与 15 天自动清理

说明：
- 默认不长期保留云端照片本地副本。
- 仅删除动作（非 hard）会保存本地回收副本。
"""

from __future__ import annotations

import argparse
import base64
import csv
import datetime as dt
import hashlib
import json
import logging
import os
import sqlite3
import sys
import tempfile
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple

try:
    import msal
except Exception:  # pragma: no cover
    msal = None

import requests

PHOTO_EXTS = {"jpg", "jpeg", "png", "webp", "heic", "bmp", "tiff", "gif"}


def utc_now_iso() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat()


def parse_iso(ts: Optional[str]) -> Optional[dt.datetime]:
    if not ts:
        return None
    try:
        return dt.datetime.fromisoformat(ts.replace("Z", "+00:00"))
    except Exception:
        return None


def ensure_parent(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def load_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def merge_dict(base: Dict[str, Any], override: Dict[str, Any]) -> Dict[str, Any]:
    out = dict(base)
    for k, v in override.items():
        if isinstance(v, dict) and isinstance(out.get(k), dict):
            out[k] = merge_dict(out[k], v)
        else:
            out[k] = v
    return out


def default_config() -> Dict[str, Any]:
    root = Path("/root/.openclaw/workspace")
    return {
        "auth": {
            "client_id": "",
            "authority": "https://login.microsoftonline.com/common",
            "scopes": ["Files.Read"],
        },
        "paths": {
            "token_cache": str(root / "tmp/onedrive_photo_batch/token_cache.json"),
            "db": str(root / "tmp/onedrive_photo_batch/index.db"),
            "tmp_dir": str(root / "tmp/onedrive_photo_batch/work"),
            "recycle_dir": str(root / "tmp_photo"),
            "log_file": str(root / "tmp/onedrive_photo_batch/skill.log"),
        },
        "ocr": {
            "endpoint": "https://api.siliconflow.cn/v1",
            "api_key": "",
            "default_model": "Qwen/Qwen3-VL-8B-Instruct",
            "prompt": "请进行OCR，逐行输出可见文字，再给三条关键内容摘要。",
            "default_interval_sec": 1.0,
            "model_intervals_sec": {},
            "album_overrides": {},
            "batch_overrides": {},
            "timeout_sec": 180,
            "max_tokens": 900,
        },
        "embedding": {
            "enabled": False,
            "endpoint": "https://api.siliconflow.cn/v1",
            "api_key": "",
            "model": "BAAI/bge-m3",
            "timeout_sec": 60,
        },
        "performance": {
            "parallel": 2,
            "max_download_kbps": 0,
            "retry": 2,
            "api_retry": 2,
            "backoff_sec": 1.0,
            "download_timeout_sec": 300,
        },
        "mode": {
            "read_only": True
        }
    }


class SkillContext:
    def __init__(self, cfg: Dict[str, Any]):
        self.cfg = cfg
        self.logger = self._build_logger(Path(cfg["paths"]["log_file"]))
        self.db = IndexDB(Path(cfg["paths"]["db"]), self.logger)
        self.drive = OneDriveClient(cfg["auth"], Path(cfg["paths"]["token_cache"]), self.logger)
        self.model = OCRClient(cfg["ocr"], self.logger)
        self.embed = EmbeddingClient(cfg["embedding"], self.logger)
        self.policy = ModelPolicy(cfg["ocr"])
        self.rate = ModelRateLimiter(cfg["ocr"])

    @staticmethod
    def _build_logger(log_file: Path) -> logging.Logger:
        ensure_parent(log_file)
        logger = logging.getLogger("onedrive-photo-batch")
        logger.setLevel(logging.INFO)
        logger.handlers.clear()
        fmt = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
        fh = logging.FileHandler(log_file, encoding="utf-8")
        fh.setFormatter(fmt)
        logger.addHandler(fh)
        sh = logging.StreamHandler(sys.stdout)
        sh.setFormatter(fmt)
        logger.addHandler(sh)
        return logger


class OneDriveClient:
    GRAPH_BASE = "https://graph.microsoft.com/v1.0"

    def __init__(self, auth_cfg: Dict[str, Any], cache_path: Path, logger: logging.Logger):
        self.client_id = auth_cfg.get("client_id", "")
        self.authority = auth_cfg.get("authority", "https://login.microsoftonline.com/common")
        self.scopes = auth_cfg.get("scopes", ["Files.ReadWrite"])
        self.cache_path = cache_path
        self.legacy_cache_path = Path("/root/.openclaw/workspace/token_cache.json")
        self.logger = logger
        self._token_lock = threading.Lock()
        self._token: Optional[str] = None

    def _acquire_token(self) -> str:
        if msal is None:
            raise RuntimeError("缺少依赖 msal，请先安装：pip install msal")
        if not self.client_id:
            raise RuntimeError("缺少 auth.client_id")

        cache = msal.SerializableTokenCache()
        # 优先读取技能缓存；缺失时兼容旧缓存迁移
        if self.cache_path.exists():
            cache.deserialize(self.cache_path.read_text(encoding="utf-8"))
        elif self.legacy_cache_path.exists():
            cache.deserialize(self.legacy_cache_path.read_text(encoding="utf-8"))

        app = msal.PublicClientApplication(
            client_id=self.client_id,
            authority=self.authority,
            token_cache=cache,
        )

        result = None
        accounts = app.get_accounts()
        if accounts:
            result = app.acquire_token_silent(self.scopes, account=accounts[0])

        if not result:
            flow = app.initiate_device_flow(scopes=self.scopes)
            if "user_code" not in flow:
                raise RuntimeError(f"创建设备码失败: {flow}")
            print(flow["message"])
            result = app.acquire_token_by_device_flow(flow)

        # 始终落盘，避免会话切换后重复授权
        ensure_parent(self.cache_path)
        self.cache_path.write_text(cache.serialize(), encoding="utf-8")

        token = result.get("access_token") if isinstance(result, dict) else None
        if not token:
            raise RuntimeError(f"获取 token 失败: {result}")
        return token

    def _bearer(self) -> str:
        with self._token_lock:
            if self._token:
                return self._token
            self._token = self._acquire_token()
            return self._token

    def request(
        self,
        method: str,
        url_or_path: str,
        *,
        params: Optional[Dict[str, Any]] = None,
        json_data: Optional[Dict[str, Any]] = None,
        data: Optional[bytes] = None,
        stream: bool = False,
        absolute: bool = False,
        timeout: int = 120,
    ) -> requests.Response:
        token = self._bearer()
        url = url_or_path if absolute else f"{self.GRAPH_BASE}{url_or_path}"
        headers = {"Authorization": f"Bearer {token}"}
        if json_data is not None:
            headers["Content-Type"] = "application/json"

        resp = requests.request(
            method,
            url,
            headers=headers,
            params=params,
            json=json_data,
            data=data,
            stream=stream,
            timeout=timeout,
        )
        if resp.status_code == 401:
            with self._token_lock:
                self._token = None
            token = self._bearer()
            headers["Authorization"] = f"Bearer {token}"
            resp = requests.request(
                method,
                url,
                headers=headers,
                params=params,
                json=json_data,
                data=data,
                stream=stream,
                timeout=timeout,
            )
        if resp.status_code >= 400:
            raise RuntimeError(f"Graph {method} {url} 失败: {resp.status_code} {resp.text[:500]}")
        return resp

    def iter_children(self, item_id: str = "root") -> Iterable[Dict[str, Any]]:
        if item_id == "root":
            path = "/me/drive/root/children"
        else:
            path = f"/me/drive/items/{item_id}/children"
        url = f"{self.GRAPH_BASE}{path}?$top=200"
        while url:
            resp = self.request("GET", url, absolute=True)
            data = resp.json()
            for it in data.get("value", []):
                yield it
            url = data.get("@odata.nextLink")

    def iter_all_photos(self) -> Iterable[Dict[str, Any]]:
        stack: List[str] = ["root"]
        while stack:
            folder = stack.pop()
            for it in self.iter_children(folder):
                if it.get("folder") is not None:
                    stack.append(it["id"])
                    continue
                name = it.get("name", "")
                ext = name.rsplit(".", 1)[-1].lower() if "." in name else ""
                if ext in PHOTO_EXTS:
                    yield it

    def download_item(self, item_id: str, out_path: Path, max_kbps: int = 0, timeout_sec: int = 300) -> str:
        ensure_parent(out_path)
        h = hashlib.sha256()
        start = time.monotonic()
        written = 0

        with self.request("GET", f"/me/drive/items/{item_id}/content", stream=True, timeout=max(30, int(timeout_sec))) as resp:
            with out_path.open("wb") as f:
                for chunk in resp.iter_content(chunk_size=256 * 1024):
                    if not chunk:
                        continue
                    f.write(chunk)
                    h.update(chunk)
                    written += len(chunk)
                    if max_kbps > 0:
                        expected = written / (max_kbps * 1024)
                        elapsed = max(1e-6, time.monotonic() - start)
                        if expected > elapsed:
                            time.sleep(expected - elapsed)

        return h.hexdigest()

    def move_item(self, item_id: str, target_parent_id: str) -> Dict[str, Any]:
        resp = self.request(
            "PATCH",
            f"/me/drive/items/{item_id}",
            json_data={"parentReference": {"id": target_parent_id}},
        )
        return resp.json()

    def delete_item(self, item_id: str) -> None:
        self.request("DELETE", f"/me/drive/items/{item_id}")

    def put_file(self, drive_path: str, local_file: Path) -> Dict[str, Any]:
        safe = drive_path.strip("/")
        with local_file.open("rb") as f:
            data = f.read()
        resp = self.request(
            "PUT",
            f"/me/drive/root:/{safe}:/content",
            data=data,
            timeout=300,
        )
        return resp.json()


class OCRClient:
    def __init__(self, cfg: Dict[str, Any], logger: logging.Logger):
        self.endpoint = cfg.get("endpoint", "").rstrip("/")
        self.api_key = cfg.get("api_key", "")
        self.prompt = cfg.get("prompt", "请OCR识别图片文字")
        self.timeout = int(cfg.get("timeout_sec", 180))
        self.max_tokens = int(cfg.get("max_tokens", 900))
        self.logger = logger

    def ocr_image(self, image_path: Path, model: str, prompt: Optional[str] = None) -> str:
        if not self.endpoint or not self.api_key:
            raise RuntimeError("OCR endpoint/api_key 未配置")

        raw = image_path.read_bytes()
        b64 = base64.b64encode(raw).decode("utf-8")
        url = f"{self.endpoint}/chat/completions"
        payload = {
            "model": model,
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt or self.prompt},
                        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{b64}"}},
                    ],
                }
            ],
            "max_tokens": self.max_tokens,
            "temperature": 0.1,
        }
        resp = requests.post(
            url,
            headers={"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"},
            json=payload,
            timeout=self.timeout,
        )
        if resp.status_code >= 400:
            raise RuntimeError(f"OCR失败 {resp.status_code}: {resp.text[:500]}")
        data = resp.json()
        content = data.get("choices", [{}])[0].get("message", {}).get("content", "")
        if isinstance(content, list):
            return "\n".join(str(x) for x in content)
        return str(content)


class EmbeddingClient:
    def __init__(self, cfg: Dict[str, Any], logger: logging.Logger):
        self.enabled = bool(cfg.get("enabled", False))
        self.endpoint = cfg.get("endpoint", "").rstrip("/")
        self.api_key = cfg.get("api_key", "")
        self.model = cfg.get("model", "")
        self.timeout = int(cfg.get("timeout_sec", 60))
        self.logger = logger

    def embed(self, text: str) -> Optional[List[float]]:
        if not self.enabled:
            return None
        if not self.endpoint or not self.api_key or not self.model:
            raise RuntimeError("embedding 配置不完整")
        payload = {"model": self.model, "input": text}
        resp = requests.post(
            f"{self.endpoint}/embeddings",
            headers={"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"},
            json=payload,
            timeout=self.timeout,
        )
        if resp.status_code >= 400:
            raise RuntimeError(f"Embedding失败 {resp.status_code}: {resp.text[:500]}")
        data = resp.json()
        emb = data.get("data", [{}])[0].get("embedding")
        return emb


class ModelPolicy:
    def __init__(self, ocr_cfg: Dict[str, Any]):
        self.default_model = ocr_cfg.get("default_model", "")
        self.album_overrides = ocr_cfg.get("album_overrides", {}) or {}
        self.batch_overrides = ocr_cfg.get("batch_overrides", {}) or {}

    def resolve(self, *, album_path: str, cmd_model: Optional[str], batch: Optional[str]) -> str:
        if cmd_model:
            return cmd_model
        if batch and batch in self.batch_overrides:
            return self.batch_overrides[batch]
        lp = (album_path or "").lower()
        for key, model in self.album_overrides.items():
            if key.lower() in lp:
                return model
        return self.default_model


class ModelRateLimiter:
    def __init__(self, ocr_cfg: Dict[str, Any]):
        self.default_interval = float(ocr_cfg.get("default_interval_sec", 1.0))
        self.model_intervals = {str(k): float(v) for k, v in (ocr_cfg.get("model_intervals_sec", {}) or {}).items()}
        self.lock = threading.Lock()
        self.next_allowed: Dict[str, float] = {}

    def wait(self, model: str):
        interval = self.model_intervals.get(model, self.default_interval)
        with self.lock:
            now = time.monotonic()
            na = self.next_allowed.get(model, now)
            if now < na:
                time.sleep(na - now)
            self.next_allowed[model] = time.monotonic() + interval


class IndexDB:
    def __init__(self, path: Path, logger: logging.Logger):
        self.path = path
        self.logger = logger
        ensure_parent(path)
        self.conn = sqlite3.connect(str(path), check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self.lock = threading.Lock()
        self._init()

    def _init(self):
        with self.conn:
            self.conn.execute(
                """
                CREATE TABLE IF NOT EXISTS photos (
                    id TEXT PRIMARY KEY,
                    name TEXT,
                    ext TEXT,
                    size INTEGER,
                    created_at TEXT,
                    modified_at TEXT,
                    album_path TEXT,
                    parent_id TEXT,
                    web_url TEXT,
                    remote_hash TEXT,
                    etag TEXT,
                    content_sha256 TEXT,
                    ocr_text TEXT,
                    summary TEXT,
                    model TEXT,
                    indexed_at TEXT,
                    embedding_json TEXT,
                    logical_deleted INTEGER DEFAULT 0,
                    deleted_at TEXT,
                    trash_path TEXT,
                    hard_deleted INTEGER DEFAULT 0,
                    last_seen_at TEXT
                )
                """
            )
            self.conn.execute(
                """
                CREATE TABLE IF NOT EXISTS ops_log (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    ts TEXT,
                    action TEXT,
                    item_id TEXT,
                    detail TEXT
                )
                """
            )

    def log_op(self, action: str, item_id: str, detail: Dict[str, Any]):
        with self.lock, self.conn:
            self.conn.execute(
                "INSERT INTO ops_log(ts,action,item_id,detail) VALUES(?,?,?,?)",
                (utc_now_iso(), action, item_id, json.dumps(detail, ensure_ascii=False)),
            )

    def upsert_metadata(self, rec: Dict[str, Any]):
        with self.lock, self.conn:
            self.conn.execute(
                """
                INSERT INTO photos(id,name,ext,size,created_at,modified_at,album_path,parent_id,web_url,remote_hash,etag,last_seen_at)
                VALUES(:id,:name,:ext,:size,:created_at,:modified_at,:album_path,:parent_id,:web_url,:remote_hash,:etag,:last_seen_at)
                ON CONFLICT(id) DO UPDATE SET
                    name=excluded.name,
                    ext=excluded.ext,
                    size=excluded.size,
                    created_at=excluded.created_at,
                    modified_at=excluded.modified_at,
                    album_path=excluded.album_path,
                    parent_id=excluded.parent_id,
                    web_url=excluded.web_url,
                    remote_hash=excluded.remote_hash,
                    etag=excluded.etag,
                    last_seen_at=excluded.last_seen_at
                """,
                rec,
            )

    def update_index(
        self,
        item_id: str,
        *,
        content_sha256: str,
        ocr_text: str,
        summary: str,
        model: str,
        embedding: Optional[List[float]],
    ):
        with self.lock, self.conn:
            self.conn.execute(
                """
                UPDATE photos SET
                    content_sha256=?,
                    ocr_text=?,
                    summary=?,
                    model=?,
                    indexed_at=?,
                    embedding_json=?,
                    logical_deleted=0,
                    deleted_at=NULL,
                    hard_deleted=0
                WHERE id=?
                """,
                (
                    content_sha256,
                    ocr_text,
                    summary,
                    model,
                    utc_now_iso(),
                    json.dumps(embedding) if embedding is not None else None,
                    item_id,
                ),
            )

    def get(self, item_id: str) -> Optional[sqlite3.Row]:
        with self.lock:
            cur = self.conn.execute("SELECT * FROM photos WHERE id=?", (item_id,))
            return cur.fetchone()

    def mark_deleted(self, item_id: str, trash_path: Optional[str], hard: bool):
        with self.lock, self.conn:
            self.conn.execute(
                """
                UPDATE photos SET logical_deleted=1, deleted_at=?, trash_path=?, hard_deleted=? WHERE id=?
                """,
                (utc_now_iso(), trash_path, 1 if hard else 0, item_id),
            )

    def restore(self, item_id: str):
        with self.lock, self.conn:
            self.conn.execute(
                "UPDATE photos SET logical_deleted=0, deleted_at=NULL, trash_path=NULL, hard_deleted=0 WHERE id=?",
                (item_id,),
            )

    def set_trash_path_null(self, item_id: str):
        with self.lock, self.conn:
            self.conn.execute("UPDATE photos SET trash_path=NULL WHERE id=?", (item_id,))

    def query(self, where: str = "1=1", params: Tuple[Any, ...] = (), limit: int = 100) -> List[sqlite3.Row]:
        with self.lock:
            cur = self.conn.execute(f"SELECT * FROM photos WHERE {where} LIMIT ?", (*params, limit))
            return cur.fetchall()

    def query_deleted_with_trash(self) -> List[sqlite3.Row]:
        with self.lock:
            cur = self.conn.execute(
                "SELECT * FROM photos WHERE logical_deleted=1 AND trash_path IS NOT NULL"
            )
            return cur.fetchall()


def item_to_meta(item: Dict[str, Any]) -> Dict[str, Any]:
    name = item.get("name", "")
    ext = name.rsplit(".", 1)[-1].lower() if "." in name else ""
    parent_path = (item.get("parentReference") or {}).get("path", "")
    album_path = ""
    if "/drive/root:" in parent_path:
        album_path = parent_path.split("/drive/root:", 1)[1] or "/"
    elif parent_path:
        album_path = parent_path
    hashes = (item.get("file") or {}).get("hashes") or {}
    remote_hash = hashes.get("quickXorHash") or hashes.get("sha1Hash") or ""

    return {
        "id": item.get("id"),
        "name": name,
        "ext": ext,
        "size": int(item.get("size", 0)),
        "created_at": item.get("createdDateTime"),
        "modified_at": item.get("lastModifiedDateTime"),
        "album_path": album_path,
        "parent_id": (item.get("parentReference") or {}).get("id"),
        "web_url": item.get("webUrl"),
        "remote_hash": remote_hash,
        "etag": item.get("eTag", ""),
        "last_seen_at": utc_now_iso(),
    }


def match_fuzzy(text: str, pattern: str) -> bool:
    return pattern.lower() in (text or "").lower()


def apply_filters(items: Iterable[Dict[str, Any]], args: argparse.Namespace) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    fmts = set()
    if args.formats:
        fmts = {x.strip().lower().lstrip(".") for x in args.formats.split(",") if x.strip()}

    date_from = parse_iso(args.date_from) if args.date_from else None
    date_to = parse_iso(args.date_to) if args.date_to else None

    for item in items:
        m = item_to_meta(item)
        name = m["name"]
        album = m["album_path"] or ""

        if args.name:
            if args.name_mode == "exact" and name != args.name:
                continue
            if args.name_mode == "fuzzy" and not match_fuzzy(name, args.name):
                continue

        if args.album:
            if args.album_mode == "exact" and album != args.album:
                continue
            if args.album_mode == "fuzzy" and not match_fuzzy(album, args.album):
                continue

        if fmts and m["ext"] not in fmts:
            continue

        if args.min_size is not None and m["size"] < args.min_size:
            continue
        if args.max_size is not None and m["size"] > args.max_size:
            continue

        mt = parse_iso(m["modified_at"]) or parse_iso(m["created_at"])
        if date_from and (not mt or mt < date_from):
            continue
        if date_to and (not mt or mt > date_to):
            continue

        out.append(item)
        if args.limit and len(out) >= args.limit:
            break

    return out


def cosine(a: List[float], b: List[float]) -> float:
    if not a or not b or len(a) != len(b):
        return -1.0
    dot = sum(x * y for x, y in zip(a, b))
    na = sum(x * x for x in a) ** 0.5
    nb = sum(y * y for y in b) ** 0.5
    if na == 0 or nb == 0:
        return -1.0
    return dot / (na * nb)


def summarize_text(txt: str) -> str:
    lines = [x.strip() for x in txt.splitlines() if x.strip()]
    return " | ".join(lines[:3])[:500]


def ensure_tmp_file(tmp_dir: Path, item_name: str) -> Path:
    tmp_dir.mkdir(parents=True, exist_ok=True)
    suffix = ""
    if "." in item_name:
        suffix = "." + item_name.rsplit(".", 1)[-1]
    fd, path = tempfile.mkstemp(prefix="photo_", suffix=suffix, dir=str(tmp_dir))
    os.close(fd)
    return Path(path)


def auto_clean_recycle(ctx: SkillContext, retention_days: int = 15) -> int:
    now = dt.datetime.now(dt.timezone.utc)
    removed = 0
    for row in ctx.db.query_deleted_with_trash():
        deleted_at = parse_iso(row["deleted_at"])
        trash_path = row["trash_path"]
        if not deleted_at or not trash_path:
            continue
        age = (now - deleted_at).days
        if age >= retention_days:
            p = Path(trash_path)
            if p.exists():
                try:
                    p.unlink()
                    removed += 1
                except Exception as e:
                    ctx.logger.error(f"清理回收站文件失败: {p} err={e}")
            ctx.db.set_trash_path_null(row["id"])
    if removed:
        ctx.logger.info(f"回收站自动清理: removed={removed}")
    return removed


def sync_and_filter_cloud(ctx: SkillContext, args: argparse.Namespace) -> List[Dict[str, Any]]:
    all_items = list(ctx.drive.iter_all_photos())
    selected = apply_filters(all_items, args)
    for item in selected:
        ctx.db.upsert_metadata(item_to_meta(item))
    return selected


def cmd_search(ctx: SkillContext, args: argparse.Namespace):
    auto_clean_recycle(ctx)

    if args.semantic_query and args.keyword:
        raise RuntimeError("--semantic-query 与 --keyword 不能同时使用，请二选一")

    if args.semantic_query:
        if not ctx.embed.enabled:
            raise RuntimeError("embedding 未启用，无法语义检索")
        qemb = ctx.embed.embed(args.semantic_query)
        rows = ctx.db.query("logical_deleted=0 AND embedding_json IS NOT NULL", limit=args.limit or 50)
        scored = []
        for r in rows:
            try:
                emb = json.loads(r["embedding_json"])
                s = cosine(qemb or [], emb)
                scored.append((s, r))
            except Exception:
                continue
        scored.sort(key=lambda x: x[0], reverse=True)
        for s, r in scored[: args.limit or 20]:
            print(json.dumps({"score": round(s, 4), "id": r["id"], "name": r["name"], "album": r["album_path"]}, ensure_ascii=False))
        return

    selected = sync_and_filter_cloud(ctx, args)

    if args.keyword:
        keyword = (args.keyword or "").strip()
        if not keyword:
            return

        clauses = ["logical_deleted=0"]
        params: List[Any] = []

        if args.name:
            if args.name_mode == "exact":
                clauses.append("name = ?")
                params.append(args.name)
            else:
                clauses.append("lower(name) LIKE ?")
                params.append(f"%{args.name.lower()}%")

        if args.album:
            if args.album_mode == "exact":
                clauses.append("ifnull(album_path,'') = ?")
                params.append(args.album)
            else:
                clauses.append("lower(ifnull(album_path,'')) LIKE ?")
                params.append(f"%{args.album.lower()}%")

        if args.formats:
            fmts = [x.strip().lower().lstrip('.') for x in args.formats.split(',') if x.strip()]
            if fmts:
                clauses.append(f"ext IN ({','.join(['?'] * len(fmts))})")
                params.extend(fmts)

        if args.min_size is not None:
            clauses.append("size >= ?")
            params.append(int(args.min_size))
        if args.max_size is not None:
            clauses.append("size <= ?")
            params.append(int(args.max_size))
        if args.date_from:
            clauses.append("ifnull(modified_at, created_at) >= ?")
            params.append(args.date_from)
        if args.date_to:
            clauses.append("ifnull(modified_at, created_at) <= ?")
            params.append(args.date_to)

        field_expr = "ifnull(ocr_text,'') || '\n' || ifnull(summary,'')"
        if args.keyword_field == "ocr":
            field_expr = "ifnull(ocr_text,'')"
        elif args.keyword_field == "summary":
            field_expr = "ifnull(summary,'')"

        if args.keyword_mode == "exact":
            clauses.append(f"instr({field_expr}, ?) > 0")
            params.append(keyword)
        else:
            clauses.append(f"lower({field_expr}) LIKE ?")
            params.append(f"%{keyword.lower()}%")

        where = " AND ".join(clauses)
        rows = ctx.db.query(where=where, params=tuple(params), limit=args.limit or 100)

        for r in rows:
            print(json.dumps({
                "id": r["id"],
                "name": r["name"],
                "album": r["album_path"],
                "keyword": keyword,
                "keyword_mode": args.keyword_mode,
                "keyword_field": args.keyword_field,
                "web_url": r["web_url"],
            }, ensure_ascii=False))
        return

    for item in selected:
        m = item_to_meta(item)
        print(json.dumps(m, ensure_ascii=False))


def should_skip_by_hash(ctx: SkillContext, meta: Dict[str, Any]) -> bool:
    prev = ctx.db.get(meta["id"])
    if not prev:
        return False
    if int(prev["logical_deleted"] or 0) == 1:
        return False
    if not prev["ocr_text"]:
        return False
    old_hash = (prev["remote_hash"] or "")
    new_hash = (meta.get("remote_hash") or "")
    if old_hash and new_hash and old_hash == new_hash:
        return True
    if (prev["etag"] or "") and (meta.get("etag") or "") and prev["etag"] == meta["etag"]:
        return True
    return False


def process_one_item(
    ctx: SkillContext,
    item: Dict[str, Any],
    args: argparse.Namespace,
) -> Dict[str, Any]:
    meta = item_to_meta(item)
    ctx.db.upsert_metadata(meta)

    if should_skip_by_hash(ctx, meta):
        return {"id": meta["id"], "name": meta["name"], "status": "skipped_hash"}

    tmp_dir = Path(ctx.cfg["paths"]["tmp_dir"])
    tmp_file = ensure_tmp_file(tmp_dir, meta["name"])

    retry = int(ctx.cfg["performance"].get("retry", 2))
    api_retry = int(ctx.cfg["performance"].get("api_retry", retry))
    backoff_sec = float(ctx.cfg["performance"].get("backoff_sec", 1.0))
    dl_timeout = int(ctx.cfg["performance"].get("download_timeout_sec", 300))
    max_kbps = int(args.max_download_kbps if args.max_download_kbps is not None else ctx.cfg["performance"].get("max_download_kbps", 0))
    model = ctx.policy.resolve(album_path=meta.get("album_path") or "", cmd_model=args.model, batch=args.batch)

    try:
        last_dl_err: Optional[Exception] = None
        sha = ""
        for i in range(api_retry + 1):
            try:
                sha = ctx.drive.download_item(meta["id"], tmp_file, max_kbps=max_kbps, timeout_sec=dl_timeout)
                last_dl_err = None
                break
            except Exception as e:
                last_dl_err = e
                time.sleep(backoff_sec * (i + 1))
        if last_dl_err is not None:
            raise last_dl_err

        last_err: Optional[Exception] = None
        text = ""
        for i in range(retry + 1):
            try:
                ctx.rate.wait(model)
                text = ctx.model.ocr_image(tmp_file, model, prompt=args.prompt)
                last_err = None
                break
            except Exception as e:
                last_err = e
                time.sleep(backoff_sec * (i + 1))

        if last_err is not None:
            raise last_err

        emb = None
        if ctx.embed.enabled:
            try:
                emb = ctx.embed.embed(text)
            except Exception as e:
                ctx.logger.error(f"embedding失败 id={meta['id']}: {e}")

        ctx.db.update_index(
            meta["id"],
            content_sha256=sha,
            ocr_text=text,
            summary=summarize_text(text),
            model=model,
            embedding=emb,
        )
        ctx.db.log_op("index", meta["id"], {"model": model, "sha": sha})
        return {"id": meta["id"], "name": meta["name"], "status": "indexed", "model": model}

    finally:
        # 铁律：识别后立即删除本地临时副本
        try:
            if tmp_file.exists():
                tmp_file.unlink()
        except Exception as e:
            ctx.logger.error(f"删除临时文件失败: {tmp_file} err={e}")


def cmd_full(ctx: SkillContext, args: argparse.Namespace):
    auto_clean_recycle(ctx)
    ctx.logger.info("full start")

    items = apply_filters(ctx.drive.iter_all_photos(), args)
    total = len(items)
    ctx.logger.info(f"full scan candidates={total}")

    workers = int(args.parallel if args.parallel is not None else ctx.cfg["performance"].get("parallel", 2))
    stats = {"indexed": 0, "skipped_hash": 0, "failed": 0}

    with ThreadPoolExecutor(max_workers=max(1, workers)) as ex:
        futs = [ex.submit(process_one_item, ctx, it, args) for it in items]
        for fut in as_completed(futs):
            try:
                r = fut.result()
                st = r.get("status", "failed")
                stats[st] = stats.get(st, 0) + 1
                ctx.logger.info(f"full item id={r.get('id')} status={st}")
            except Exception as e:
                stats["failed"] += 1
                ctx.logger.error(f"full item failed: {e}")

    ctx.logger.info(f"full done stats={stats}")
    print(json.dumps({"total": total, "stats": stats}, ensure_ascii=False))


def build_trash_name(item_id: str, name: str) -> str:
    ts = dt.datetime.now().strftime("%Y%m%d%H%M%S")
    return f"{item_id}_{ts}_{name}"


def cmd_delete(ctx: SkillContext, args: argparse.Namespace):
    auto_clean_recycle(ctx)
    items = sync_and_filter_cloud(ctx, args)
    recycle_dir = Path(ctx.cfg["paths"]["recycle_dir"])
    recycle_dir.mkdir(parents=True, exist_ok=True)

    for item in items:
        meta = item_to_meta(item)
        trash_path = None
        if not args.hard:
            tname = build_trash_name(meta["id"], meta["name"])
            tp = recycle_dir / tname
            ctx.drive.download_item(meta["id"], tp, max_kbps=int(ctx.cfg["performance"].get("max_download_kbps", 0)))
            trash_path = str(tp)

        ctx.drive.delete_item(meta["id"])
        ctx.db.mark_deleted(meta["id"], trash_path=trash_path, hard=bool(args.hard))
        ctx.db.log_op("delete_hard" if args.hard else "delete_soft", meta["id"], {"trash_path": trash_path})
        print(json.dumps({"id": meta["id"], "name": meta["name"], "deleted": True, "hard": bool(args.hard)}, ensure_ascii=False))


def cmd_restore(ctx: SkillContext, args: argparse.Namespace):
    auto_clean_recycle(ctx)
    rows = ctx.db.query("logical_deleted=1 AND trash_path IS NOT NULL", limit=args.limit or 1000)
    count = 0
    for r in rows:
        if args.item_id and r["id"] != args.item_id:
            continue
        deleted_at = parse_iso(r["deleted_at"])
        if deleted_at and (dt.datetime.now(dt.timezone.utc) - deleted_at).days >= 15 and not args.force:
            continue

        trash_path = Path(r["trash_path"])
        if not trash_path.exists():
            ctx.db.set_trash_path_null(r["id"])
            continue

        album = (r["album_path"] or "/").strip("/")
        drive_path = f"{album}/{r['name']}" if album else r["name"]
        ctx.drive.put_file(drive_path, trash_path)
        ctx.db.restore(r["id"])
        ctx.db.log_op("restore", r["id"], {"from": str(trash_path), "to": drive_path})
        print(json.dumps({"id": r["id"], "restored": True, "to": drive_path}, ensure_ascii=False))
        count += 1

    print(json.dumps({"restored": count}, ensure_ascii=False))


def cmd_trash_empty(ctx: SkillContext, args: argparse.Namespace):
    recycle_dir = Path(ctx.cfg["paths"]["recycle_dir"])
    recycle_dir.mkdir(parents=True, exist_ok=True)
    removed = 0
    for p in recycle_dir.glob("*"):
        if p.is_file():
            p.unlink(missing_ok=True)
            removed += 1
    rows = ctx.db.query("logical_deleted=1", limit=100000)
    for r in rows:
        ctx.db.set_trash_path_null(r["id"])
    print(json.dumps({"trash_cleared": removed}, ensure_ascii=False))


def cmd_move(ctx: SkillContext, args: argparse.Namespace):
    auto_clean_recycle(ctx)
    if not args.target_album_path:
        raise RuntimeError("move 需要 --target-album-path")

    # 先选中文件
    items = sync_and_filter_cloud(ctx, args)
    target_folder = args.target_album_path.strip("/")

    # 用简单 PUT-copy 思路：下载再上传到目标，再删除原文件（更稳且不依赖 folder id 查找）
    for item in items:
        meta = item_to_meta(item)
        tmp_file = ensure_tmp_file(Path(ctx.cfg["paths"]["tmp_dir"]), meta["name"])
        try:
            ctx.drive.download_item(meta["id"], tmp_file)
            new_path = f"{target_folder}/{meta['name']}" if target_folder else meta["name"]
            ctx.drive.put_file(new_path, tmp_file)
            ctx.drive.delete_item(meta["id"])
            ctx.db.log_op("move", meta["id"], {"to": new_path})
            print(json.dumps({"id": meta["id"], "moved_to": new_path}, ensure_ascii=False))
        finally:
            tmp_file.unlink(missing_ok=True)


def cmd_upload(ctx: SkillContext, args: argparse.Namespace):
    auto_clean_recycle(ctx)
    target_album = (args.target_album_path or "").strip("/")
    paths = [Path(p) for p in (args.files or [])]
    for p in paths:
        if not p.exists() or not p.is_file():
            print(json.dumps({"file": str(p), "uploaded": False, "reason": "not_found"}, ensure_ascii=False))
            continue
        drive_path = f"{target_album}/{p.name}" if target_album else p.name
        item = ctx.drive.put_file(drive_path, p)
        meta = item_to_meta(item)
        ctx.db.upsert_metadata(meta)
        ctx.db.log_op("upload", meta["id"], {"path": drive_path})
        print(json.dumps({"file": str(p), "uploaded": True, "id": meta["id"], "path": drive_path}, ensure_ascii=False))


def cmd_export(ctx: SkillContext, args: argparse.Namespace):
    where = "1=1"
    params: List[Any] = []
    if not args.include_deleted:
        where += " AND logical_deleted=0"

    rows = ctx.db.query(where, tuple(params), limit=args.limit or 100000)
    out = Path(args.out)
    ensure_parent(out)

    if args.format == "json":
        payload = [dict(r) for r in rows]
        out.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    else:
        fields = [
            "id",
            "name",
            "ext",
            "size",
            "album_path",
            "model",
            "indexed_at",
            "logical_deleted",
            "deleted_at",
            "trash_path",
            "summary",
        ]
        with out.open("w", encoding="utf-8", newline="") as f:
            w = csv.DictWriter(f, fieldnames=fields)
            w.writeheader()
            for r in rows:
                row = {k: r[k] for k in fields}
                w.writerow(row)
    print(json.dumps({"exported": len(rows), "out": str(out)}, ensure_ascii=False))


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="OneDrive Photo Batch Skill")
    p.add_argument("--config", required=True, help="配置文件路径（JSON）")

    sub = p.add_subparsers(dest="command", required=True)

    def add_common_filters(sp: argparse.ArgumentParser):
        sp.add_argument("--name", help="按文件名筛选")
        sp.add_argument("--name-mode", choices=["exact", "fuzzy"], default="fuzzy")
        sp.add_argument("--album", help="按相册/路径筛选")
        sp.add_argument("--album-mode", choices=["exact", "fuzzy"], default="fuzzy")
        sp.add_argument("--date-from", help="开始时间 ISO8601")
        sp.add_argument("--date-to", help="结束时间 ISO8601")
        sp.add_argument("--min-size", type=int)
        sp.add_argument("--max-size", type=int)
        sp.add_argument("--formats", help="格式列表，如 jpg,png")
        sp.add_argument("--limit", type=int, default=100)

    sp_search = sub.add_parser("search", help="云端检索 / 语义检索 / 关键词精确检索")
    add_common_filters(sp_search)
    sp_search.add_argument("--semantic-query", help="语义查询（需 embedding 已启用）")
    sp_search.add_argument("--keyword", help="关键词检索（在 OCR/summary 文本中匹配）")
    sp_search.add_argument("--keyword-mode", choices=["exact", "fuzzy"], default="exact", help="关键词匹配模式")
    sp_search.add_argument("--keyword-field", choices=["all", "ocr", "summary"], default="all", help="关键词匹配字段")

    sp_full = sub.add_parser("full", help="全量识别并建索引")
    add_common_filters(sp_full)
    sp_full.add_argument("--model", help="本批次强制模型")
    sp_full.add_argument("--batch", help="批次名（用于 batch_overrides）")
    sp_full.add_argument("--prompt", help="覆盖默认OCR提示词")
    sp_full.add_argument("--parallel", type=int, help="并行处理数")
    sp_full.add_argument("--max-download-kbps", type=int, help="下载限速")

    sp_del = sub.add_parser("delete", help="删除云端照片（默认软删除+回收站）")
    add_common_filters(sp_del)
    sp_del.add_argument("--hard", action="store_true", help="彻底清除（不入回收站）")

    sp_restore = sub.add_parser("restore", help="从本地回收站恢复（15天内）")
    sp_restore.add_argument("--item-id", help="指定恢复项ID")
    sp_restore.add_argument("--limit", type=int, default=100)
    sp_restore.add_argument("--force", action="store_true", help="忽略15天窗口")

    sub.add_parser("trash-empty", help="清空本地回收站")

    sp_move = sub.add_parser("move", help="移动照片到相册（下载-上传-删除原图）")
    add_common_filters(sp_move)
    sp_move.add_argument("--target-album-path", required=True, help="目标相册路径，如 /Pictures/Archive")

    sp_upload = sub.add_parser("upload", help="上传本地照片到云端相册")
    sp_upload.add_argument("--target-album-path", default="", help="目标相册路径")
    sp_upload.add_argument("files", nargs="+", help="本地文件路径")

    sp_export = sub.add_parser("export", help="导出索引结果")
    sp_export.add_argument("--format", choices=["json", "csv"], default="json")
    sp_export.add_argument("--out", required=True)
    sp_export.add_argument("--include-deleted", action="store_true")
    sp_export.add_argument("--limit", type=int, default=100000)

    return p


WRITE_COMMANDS = {"delete", "restore", "trash-empty", "move", "upload"}
ONEDRIVE_COMMANDS = {"search", "full", "delete", "restore", "move", "upload"}


def fail(code: str, message: str) -> Dict[str, Any]:
    return {"ok": False, "error": {"code": code, "message": message}}


def ensure_runtime_requirements(args: argparse.Namespace):
    if args.command in ONEDRIVE_COMMANDS and msal is None:
        raise RuntimeError(
            "缺少依赖 msal（当前解释器不可用）。请在虚拟环境运行，例如："
            " /root/.openclaw/workspace/tmp/onedrive-demo-venv/bin/python"
            " /root/.openclaw/workspace/skills/onedrive-photo-batch/scripts/onedrive_photo_batch.py ..."
        )


def run_preflight(cfg: Dict[str, Any], args: argparse.Namespace):
    auth = cfg.get("auth") or {}
    paths = cfg.get("paths") or {}
    ocr = cfg.get("ocr") or {}
    emb = cfg.get("embedding") or {}

    if args.command in ONEDRIVE_COMMANDS and not auth.get("client_id"):
        raise RuntimeError("CONFIG_ERROR: 缺少 auth.client_id")

    required_paths = ["token_cache", "db", "tmp_dir", "log_file"]
    for key in required_paths:
        if not (paths.get(key) and str(paths.get(key)).strip()):
            raise RuntimeError(f"CONFIG_ERROR: 缺少 paths.{key}")

    if args.command == "full":
        if not ocr.get("endpoint") or not ocr.get("api_key"):
            raise RuntimeError("CONFIG_ERROR: full 需要配置 ocr.endpoint 与 ocr.api_key")

    if args.command == "search" and getattr(args, "semantic_query", None):
        if not emb.get("enabled"):
            raise RuntimeError("CONFIG_ERROR: semantic-query 需要 embedding.enabled=true")
        if not emb.get("endpoint") or not emb.get("api_key") or not emb.get("model"):
            raise RuntimeError("CONFIG_ERROR: semantic-query 需要完整 embedding 配置")


def run(args: argparse.Namespace):
    cfg_path = Path(args.config).expanduser().resolve()
    cfg = merge_dict(default_config(), load_json(cfg_path, {}))
    ensure_runtime_requirements(args)
    run_preflight(cfg, args)
    ctx = SkillContext(cfg)

    try:
        read_only = bool((cfg.get("mode") or {}).get("read_only", True))
        if read_only and args.command in WRITE_COMMANDS:
            raise RuntimeError(f"当前为只读验收模式，已屏蔽写操作: {args.command}")

        if args.command == "search":
            cmd_search(ctx, args)
        elif args.command == "full":
            cmd_full(ctx, args)
        elif args.command == "delete":
            cmd_delete(ctx, args)
        elif args.command == "restore":
            cmd_restore(ctx, args)
        elif args.command == "trash-empty":
            auto_clean_recycle(ctx)
            cmd_trash_empty(ctx, args)
        elif args.command == "move":
            cmd_move(ctx, args)
        elif args.command == "upload":
            cmd_upload(ctx, args)
        elif args.command == "export":
            cmd_export(ctx, args)
        else:
            raise RuntimeError(f"未知命令: {args.command}")
    except Exception as e:
        ctx.logger.exception(f"command failed: {args.command}: {e}")
        raise


if __name__ == "__main__":
    parser = build_parser()
    ns = parser.parse_args()
    try:
        run(ns)
    except Exception as e:
        msg = str(e)
        code = "RUNTIME_ERROR"
        if "CONFIG_ERROR:" in msg:
            code = "CONFIG_ERROR"
            msg = msg.split("CONFIG_ERROR:", 1)[1].strip()
        elif "Graph" in msg:
            code = "API_ERROR"
        elif "timed out" in msg.lower() or "timeout" in msg.lower():
            code = "TIMEOUT"
        print(json.dumps(fail(code, msg), ensure_ascii=False))
        sys.exit(1)
