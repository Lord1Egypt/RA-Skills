#!/usr/bin/env python3
"""低频采集乙方宝当天搜索结果及未读详情。"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import random
import re
import shutil
import sqlite3
import stat
import subprocess
import sys
import time
from dataclasses import dataclass
from datetime import datetime
from html.parser import HTMLParser
from pathlib import Path
from typing import Any, Iterable
from urllib.parse import urlparse
from zoneinfo import ZoneInfo

from curl_cffi import requests
from dotenv import load_dotenv


BASE_URL = "https://qiye.qianlima.com"
APP_URL = f"{BASE_URL}/new_qd_yfbsite/"
API_URL = f"{APP_URL}api"
SEARCH_URL = f"{API_URL}/search"
DETAIL_URL = f"{API_URL}/subZhaobiao/zbDetail"
AREA_IDS = {"广西": "6"}
SHANGHAI = ZoneInfo("Asia/Shanghai")


def _load_env() -> None:
    """Load .env from explicit path, workdir, CWD, or next to this script."""
    candidates: list[Path] = []
    env_file = os.environ.get("QIANLIMA_ENV", "").strip()
    if env_file:
        candidates.append(Path(env_file).expanduser())
    workdir = os.environ.get("QIANLIMA_WORKDIR", "").strip()
    if workdir:
        candidates.append(Path(workdir).expanduser() / ".env")
    candidates.append(Path.cwd() / ".env")
    candidates.append(Path(__file__).resolve().with_name(".env"))
    for path in candidates:
        if path.is_file():
            load_dotenv(path)
            return
    load_dotenv()


def _default_workdir() -> Path:
    raw = os.environ.get("QIANLIMA_WORKDIR", "").strip()
    if raw:
        return Path(raw).expanduser()
    return Path.cwd()


_load_env()


class QianlimaError(RuntimeError):
    pass


class QianlimaAuthError(QianlimaError):
    pass


class QianlimaRestrictedError(QianlimaError):
    pass


@dataclass(frozen=True)
class Config:
    keyword: str
    area_id: str
    date: str
    db_path: Path
    output_dir: Path
    min_sleep: float
    max_sleep: float
    max_pages: int
    list_limit: int | None
    max_details: int | None
    analyze_details: int
    analysis_model: str
    analysis_base_url: str
    analysis_token: str
    refresh_details: bool
    token: str
    openid: str
    cookie: str


class Store:
    def __init__(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        self.connection = sqlite3.connect(path)
        self.connection.row_factory = sqlite3.Row
        self.connection.execute("PRAGMA journal_mode=WAL")
        self.connection.executescript(
            """
            CREATE TABLE IF NOT EXISTS items (
                content_id TEXT PRIMARY KEY,
                area_id TEXT NOT NULL,
                page_from TEXT NOT NULL,
                title TEXT NOT NULL,
                update_date TEXT NOT NULL,
                first_seen_at TEXT NOT NULL,
                last_seen_at TEXT NOT NULL,
                detail_status TEXT NOT NULL DEFAULT 'pending',
                detail_read_at TEXT,
                detail_error TEXT,
                list_json TEXT NOT NULL,
                detail_json TEXT
            );
            CREATE INDEX IF NOT EXISTS idx_items_detail_status
                ON items(detail_status);
            """
        )

    def upsert_list_item(self, item: dict[str, Any], fallback_area: str) -> str:
        content_id = str(item.get("contentId") or item.get("searchId") or "")
        if not content_id:
            raise QianlimaError("列表记录缺少 contentId，无法建立去重键")
        now = datetime.now(SHANGHAI).isoformat(timespec="seconds")
        values = (
            content_id,
            str(item.get("areaId") or fallback_area),
            str(item.get("pageFrom") or "zhaobiao"),
            _plain_text(item.get("title")),
            str(item.get("updateDate") or ""),
            now,
            now,
            json.dumps(item, ensure_ascii=False, separators=(",", ":")),
        )
        self.connection.execute(
            """
            INSERT INTO items (
                content_id, area_id, page_from, title, update_date,
                first_seen_at, last_seen_at, list_json
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(content_id) DO UPDATE SET
                area_id=excluded.area_id,
                page_from=excluded.page_from,
                title=excluded.title,
                update_date=excluded.update_date,
                last_seen_at=excluded.last_seen_at,
                list_json=excluded.list_json
            """,
            values,
        )
        self.connection.commit()
        return content_id

    def needs_detail(self, content_id: str, refresh: bool) -> bool:
        if refresh:
            return True
        row = self.connection.execute(
            "SELECT detail_status FROM items WHERE content_id = ?", (content_id,)
        ).fetchone()
        return row is None or row["detail_status"] not in {"success", "restricted"}

    def mark_fetching(self, content_id: str) -> None:
        self.connection.execute(
            """
            UPDATE items
            SET detail_status='fetching', detail_error=NULL
            WHERE content_id=?
            """,
            (content_id,),
        )
        self.connection.commit()

    def save_detail(self, content_id: str, detail: dict[str, Any]) -> None:
        now = datetime.now(SHANGHAI).isoformat(timespec="seconds")
        self.connection.execute(
            """
            UPDATE items
            SET detail_status='success', detail_read_at=?, detail_error=NULL,
                detail_json=?
            WHERE content_id=?
            """,
            (
                now,
                json.dumps(detail, ensure_ascii=False, separators=(",", ":")),
                content_id,
            ),
        )
        self.connection.commit()

    def save_error(self, content_id: str, error: str) -> None:
        self.connection.execute(
            """
            UPDATE items
            SET detail_status='failed', detail_error=?
            WHERE content_id=?
            """,
            (error[:1000], content_id),
        )
        self.connection.commit()

    def save_restricted(self, content_id: str, error: str) -> None:
        self.connection.execute(
            """
            UPDATE items
            SET detail_status='restricted', detail_error=?, detail_json=NULL
            WHERE content_id=?
            """,
            (error[:1000], content_id),
        )
        self.connection.commit()

    def export_rows(self, content_ids: Iterable[str]) -> list[dict[str, Any]]:
        rows = []
        for content_id in content_ids:
            row = self.connection.execute(
                "SELECT * FROM items WHERE content_id=?", (content_id,)
            ).fetchone()
            if not row:
                continue
            rows.append(
                {
                    "content_id": row["content_id"],
                    "area_id": row["area_id"],
                    "page_from": row["page_from"],
                    "title": row["title"],
                    "update_date": row["update_date"],
                    "first_seen_at": row["first_seen_at"],
                    "last_seen_at": row["last_seen_at"],
                    "detail_status": row["detail_status"],
                    "detail_read_at": row["detail_read_at"],
                    "detail_error": row["detail_error"],
                    "list": json.loads(row["list_json"]),
                    "detail": (
                        json.loads(row["detail_json"]) if row["detail_json"] else None
                    ),
                }
            )
        return rows

    def close(self) -> None:
        self.connection.close()


class QianlimaClient:
    def __init__(self, config: Config) -> None:
        self.config = config
        self.session = requests.Session()
        self.request_count = 0
        self.api_headers = {
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            "Referer": APP_URL,
            "Authorization": f"Bearer {config.token}",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
        }
        if config.cookie:
            self.api_headers["Cookie"] = config.cookie

    def close(self) -> None:
        self.session.close()

    def warm_up(self) -> None:
        response = self.session.get(
            APP_URL,
            impersonate="chrome",
            timeout=30,
        )
        self.request_count += 1
        response.raise_for_status()

    def _sleep_between_requests(self) -> None:
        if self.request_count:
            delay = random.uniform(
                self.config.min_sleep, self.config.max_sleep
            )
            print(f"[限速] 等待 {delay:.2f} 秒")
            time.sleep(delay)

    def _get_json(self, url: str, params: dict[str, Any]) -> dict[str, Any]:
        if self.config.openid:
            params = {**params, "openid": self.config.openid}

        last_error: Exception | None = None
        for attempt in range(1, 4):
            self._sleep_between_requests()
            self.request_count += 1
            try:
                response = self.session.get(
                    url,
                    params=params,
                    headers=self.api_headers,
                    impersonate="chrome",
                    timeout=30,
                )
                response.raise_for_status()
                payload = response.json()
                code = payload.get("code", 200)
                if code == 401:
                    raise QianlimaAuthError(
                        "登录授权已失效，请更新 QIANLIMA_TOKEN"
                    )
                if code != 200:
                    raise QianlimaError(
                        f"接口返回 code={code}: {payload.get('msg', '')}"
                    )
                return payload
            except QianlimaError:
                raise
            except Exception as error:
                last_error = error
                if attempt == 3:
                    break
                retry_delay = attempt * 2 + random.uniform(0.5, 1.5)
                print(
                    f"[重试] 第 {attempt} 次请求失败，"
                    f"{retry_delay:.2f} 秒后重试"
                )
                time.sleep(retry_delay)
        raise QianlimaError(f"请求失败: {last_error}")

    def search_page(self, page_number: int) -> tuple[list[dict[str, Any]], int]:
        api_date = self.config.date.replace("-", "/")
        params: dict[str, Any] = {
            "pageSize": 30,
            "pageNum": page_number,
            "pageFrom": "zhaobiao",
            "keyword": self.config.keyword,
            "queryType": "",
            "offSet": "",
            "viewMonitor": "false",
            "areaIds": self.config.area_id,
            "keywords": "",
            "times": f"{api_date},{api_date}",
            "searchType": "",
            "filterCondition": 1,
            "nature": "",
            "defTimeFlag": "0",
        }
        payload = self._get_json(SEARCH_URL, params)
        data = payload.get("data") or {}
        items = (
            data.get("resultList")
            or data.get("realTimeList")
            or data.get("resultSet")
            or []
        )
        total = int(
            data.get("count")
            or data.get("totalNum")
            or data.get("totalElements")
            or len(items)
        )
        return items, total

    def get_detail(self, item: dict[str, Any]) -> dict[str, Any]:
        params = {
            "contentId": item["contentId"],
            "pageFrom": item.get("pageFrom") or "zhaobiao",
            "areaId": item.get("areaId") or self.config.area_id,
            "searchKeyWord": self.config.keyword,
        }
        payload = self._get_json(DETAIL_URL, params)
        detail = payload.get("data") or {}
        if detail.get("errType") is not None:
            raise QianlimaRestrictedError(
                "详情受访问权限限制: "
                f"errType={detail.get('errType')}, "
                f"payLevels={detail.get('payLevels') or ''}"
            )
        if not detail.get("title") and not detail.get("content"):
            raise QianlimaError("详情接口未返回标题或正文")
        return detail

    def download_attachment(self, url: str) -> tuple[bytes, str]:
        parsed = urlparse(url)
        if (
            parsed.scheme != "https"
            or not parsed.hostname
            or not (
                parsed.hostname == "qianlima.com"
                or parsed.hostname.endswith(".qianlima.com")
            )
        ):
            raise QianlimaError("附件下载地址不属于 qianlima.com，已拒绝")

        last_error: Exception | None = None
        for attempt in range(1, 4):
            self._sleep_between_requests()
            self.request_count += 1
            try:
                with requests.Session() as public_session:
                    response = public_session.get(
                        url,
                        headers={"Accept": "application/octet-stream,*/*"},
                        impersonate="chrome",
                        timeout=60,
                    )
                auth_mode = "public_no_credentials"
                if response.status_code in {401, 403}:
                    self._sleep_between_requests()
                    self.request_count += 1
                    response = self.session.get(
                        url,
                        headers={
                            "Accept": "application/octet-stream,*/*",
                            "Authorization": f"Bearer {self.config.token}",
                            "Referer": APP_URL,
                        },
                        impersonate="chrome",
                        timeout=60,
                    )
                    auth_mode = "qianlima_bearer_fallback"
                response.raise_for_status()
                body = response.content
                if not body:
                    raise QianlimaError("附件响应为空")
                if "application/json" in response.headers.get("content-type", ""):
                    payload = response.json()
                    raise QianlimaError(
                        f"附件接口返回 JSON: code={payload.get('code')} "
                        f"msg={payload.get('msg', '')}"
                    )
                return body, auth_mode
            except QianlimaError:
                raise
            except Exception as error:
                last_error = error
                if attempt == 3:
                    break
                retry_delay = attempt * 2 + random.uniform(0.5, 1.5)
                print(
                    f"[附件重试] 第 {attempt} 次下载失败，"
                    f"{retry_delay:.2f} 秒后重试"
                )
                time.sleep(retry_delay)
        raise QianlimaError(f"附件下载失败: {last_error}")


def _plain_text(value: Any) -> str:
    return re.sub(r"<[^>]+>", "", str(value or "")).strip()


class _HTMLCleaner(HTMLParser):
    BLOCK_TAGS = {
        "br", "div", "p", "li", "tr", "table", "section", "article",
        "h1", "h2", "h3", "h4", "h5", "h6",
    }

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.parts: list[str] = []
        self.ignored_depth = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag in {"script", "style"}:
            self.ignored_depth += 1
        elif not self.ignored_depth and tag in self.BLOCK_TAGS:
            self.parts.append("\n")
        elif not self.ignored_depth and tag in {"td", "th"}:
            self.parts.append("\t")

    def handle_endtag(self, tag: str) -> None:
        if tag in {"script", "style"} and self.ignored_depth:
            self.ignored_depth -= 1
        elif not self.ignored_depth and tag in self.BLOCK_TAGS:
            self.parts.append("\n")

    def handle_data(self, data: str) -> None:
        if not self.ignored_depth:
            self.parts.append(data)

    def text(self) -> str:
        text = "".join(self.parts).replace("\xa0", " ")
        text = re.sub(r"[ \t]+", " ", text)
        return re.sub(r"\n\s*\n+", "\n", text).strip()


def clean_html(value: Any) -> str:
    cleaner = _HTMLCleaner()
    cleaner.feed(str(value or ""))
    cleaner.close()
    return cleaner.text()


def _attachment_mentions(content_text: str) -> list[dict[str, str]]:
    mentions: list[dict[str, str]] = []
    for line in content_text.splitlines():
        match = re.match(
            r"^\s*\d+[、.．]\s*(.+?\.(?:docx?|xlsx?|pdf|zip|rar))\s*$",
            line,
            flags=re.IGNORECASE,
        )
        if match:
            mentions.append({"name": match.group(1), "source": "content_text"})
    return mentions


def _clean_metadata(value: Any) -> Any:
    if isinstance(value, dict):
        return {key: _clean_metadata(item) for key, item in value.items()}
    if isinstance(value, list):
        return [_clean_metadata(item) for item in value]
    if isinstance(value, str) and re.search(r"<[^>]+>", value):
        return clean_html(value)
    return value


def _safe_filename(value: Any, fallback: str) -> str:
    name = Path(str(value or "")).name.strip()
    name = re.sub(r"[\x00-\x1f/:*?\"<>|]", "_", name)
    return name[:180] or fallback


def _extract_document_text(path: Path) -> tuple[str, str | None]:
    if path.suffix.lower() not in {".doc", ".docx", ".rtf", ".odt"}:
        return "", f"暂不支持解析 {path.suffix or '无扩展名'} 文件"
    textutil = Path("/usr/bin/textutil")
    if textutil.is_file():
        command = [str(textutil), "-convert", "txt", "-stdout", str(path)]
    elif path.suffix.lower() == ".doc" and shutil.which("antiword"):
        command = [str(shutil.which("antiword")), str(path)]
    else:
        return "", "当前系统缺少可用的 Word 文本提取器"
    try:
        completed = subprocess.run(
            command,
            check=True,
            capture_output=True,
            timeout=60,
        )
        text = completed.stdout.decode("utf-8", errors="replace")
        text = text.replace("\x00", "")
        text = re.sub(r"[ \t]+", " ", text)
        text = re.sub(r"\n\s*\n+", "\n", text).strip()
        if not text:
            return "", "文档转换成功但没有提取到文本"
        return text, None
    except Exception as error:
        return "", f"文档解析失败: {error}"


def download_and_extract_attachments(
    client: QianlimaClient,
    detail: dict[str, Any],
    artifact_dir: Path,
    content_id: str,
) -> list[dict[str, Any]]:
    attachment_dir = artifact_dir / "attachments" / content_id
    documents: list[dict[str, Any]] = []
    manifest: list[dict[str, Any]] = []
    manifest_path = attachment_dir / "manifest.json"
    previous_manifest: dict[str, dict[str, Any]] = {}
    if manifest_path.is_file():
        try:
            previous_manifest = {
                item["name"]: item
                for item in json.loads(manifest_path.read_text(encoding="utf-8"))
                if item.get("name")
            }
        except (json.JSONDecodeError, OSError):
            previous_manifest = {}
    for index, attachment in enumerate(detail.get("downlinkList") or [], 1):
        url = str(attachment.get("url") or "").strip()
        if not url:
            continue
        filename = _safe_filename(
            attachment.get("title"), f"attachment_{index}"
        )
        attachment_dir.mkdir(parents=True, exist_ok=True)
        file_path = attachment_dir / filename
        downloaded = False
        auth_mode = previous_manifest.get(filename, {}).get(
            "download_auth_mode", "cached_auth_mode_unknown"
        )
        if not file_path.is_file() or file_path.stat().st_size == 0:
            body, auth_mode = client.download_attachment(url)
            temporary_path = file_path.with_name(file_path.name + ".part")
            temporary_path.write_bytes(body)
            temporary_path.replace(file_path)
            downloaded = True
            print(f"[附件] 已保存 {filename} ({len(body)} bytes)")
        else:
            print(f"[附件] 跳过已下载 {filename}")

        extracted_text, extraction_error = _extract_document_text(file_path)
        text_path: Path | None = None
        if extracted_text:
            text_path = file_path.with_name(file_path.name + ".txt")
            text_path.write_text(extracted_text + "\n", encoding="utf-8")
        file_hash = hashlib.sha256(file_path.read_bytes()).hexdigest()
        record = {
            "name": filename,
            "source_url": url,
            "local_path": str(file_path.resolve()),
            "size_bytes": file_path.stat().st_size,
            "sha256": file_hash,
            "downloaded_this_run": downloaded,
            "download_auth_mode": auth_mode,
            "extracted_text_path": (
                str(text_path.resolve()) if text_path is not None else None
            ),
            "extracted_chars": len(extracted_text),
            "extraction_error": extraction_error,
        }
        manifest.append(record)
        documents.append(
            {
                "name": filename,
                "local_path": record["local_path"],
                "extracted_text": extracted_text,
                "extraction_error": extraction_error,
            }
        )

    if manifest:
        attachment_dir.mkdir(parents=True, exist_ok=True)
        manifest_path.write_text(
            json.dumps(manifest, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
    return documents


def clean_detail(detail: dict[str, Any], content_id: str) -> dict[str, Any]:
    summary = detail.get("summary") or {}
    contacts = summary.get("yfbZbContactInfoResponse") or {}
    content_text = clean_html(detail.get("content"))
    attachments = detail.get("downlinkList") or []
    if not attachments:
        attachments = _attachment_mentions(content_text)
    return {
        "content_id": content_id,
        "title": _plain_text(detail.get("title")),
        "type": detail.get("type"),
        "area_name": detail.get("areaName"),
        "update_date": detail.get("updateDate"),
        "summary": summary,
        "contacts": contacts,
        "attachments": attachments,
        "stages": detail.get("stages") or [],
        "content_text": content_text,
        "source_metadata": _clean_metadata(
            {key: value for key, value in detail.items() if key != "content"}
        ),
    }


def analyze_detail(config: Config, cleaned: dict[str, Any]) -> str:
    if not config.analysis_token:
        raise QianlimaError("缺少环境变量 ANTHROPIC_AUTH_TOKEN")
    prompt = """你是医疗招投标信息分析助手。只能依据输入数据，不要猜测。
请用中文 Markdown 输出：
1. 招标项目一句话结论
2. 招标需要什么：产品、服务、供应商资质、报名/投标要求、关键日期
3. 重点与难点：逐条说明，并给出依据
4. 单位信息：招标单位、代理单位及其他单位
5. 产品清单：逐项列出；若原文没有完整清单，明确说明缺失
6. 联系人信息：姓名、角色、电话、邮箱；对脱敏或缺失字段明确标注
7. 信息完整性审计：单位、产品、联系人、金额、截止时间、附件是否齐全
8. 建议下一步动作

输入数据：
""" + json.dumps(cleaned, ensure_ascii=False)
    url = config.analysis_base_url.rstrip("/") + "/v1/messages"
    response = requests.post(
        url,
        headers={
            "Authorization": f"Bearer {config.analysis_token}",
            "Content-Type": "application/json",
        },
        json={
            "model": config.analysis_model,
            "max_tokens": 128000,
            "messages": [{"role": "user", "content": prompt}],
        },
        timeout=180,
    )
    response.raise_for_status()
    payload = response.json()
    texts = [
        block.get("text", "")
        for block in payload.get("content", [])
        if block.get("type") == "text"
    ]
    result = "\n".join(texts).strip()
    if not result:
        raise QianlimaError("MiniMax 返回中没有 text 内容块")
    return result


def _parse_args() -> Config:
    parser = argparse.ArgumentParser(
        description="低频采集乙方宝当天搜索列表和未读详情"
    )
    parser.add_argument("--keyword", required=True, help="搜索关键词")
    parser.add_argument("--area", default="广西", help="内置地区名称，默认广西")
    parser.add_argument("--area-id", help="直接指定乙方宝地区 ID")
    parser.add_argument(
        "--date",
        default=datetime.now(SHANGHAI).date().isoformat(),
        help="采集日期 YYYY-MM-DD，默认上海时区当天",
    )
    workdir = _default_workdir()
    parser.add_argument(
        "--db",
        default=str(workdir / "data" / "qianlima.sqlite3"),
        help="SQLite 状态库路径（默认 $QIANLIMA_WORKDIR/data/qianlima.sqlite3）",
    )
    parser.add_argument(
        "--output-dir",
        default=str(workdir / "output"),
        help="输出目录（默认 $QIANLIMA_WORKDIR/output）",
    )
    parser.add_argument("--min-sleep", type=float, default=2.5)
    parser.add_argument("--max-sleep", type=float, default=5.5)
    parser.add_argument("--max-pages", type=int, default=20)
    parser.add_argument("--list-limit", type=int, help="最多保留多少条列表记录")
    parser.add_argument(
        "--max-details",
        type=int,
        help="仅检查列表前 N 条的详情；其中已成功读取的会跳过",
    )
    parser.add_argument("--analyze-details", type=int, default=0)
    parser.add_argument("--analysis-model", default="MiniMax-M2.7")
    parser.add_argument("--qianlima-token-file", default=".qianlima_token")
    parser.add_argument("--refresh-details", action="store_true")
    args = parser.parse_args()

    try:
        datetime.strptime(args.date, "%Y-%m-%d")
    except ValueError as error:
        parser.error(f"--date 格式错误: {error}")
    if args.min_sleep < 1 or args.max_sleep < args.min_sleep:
        parser.error("--min-sleep 必须至少为 1 秒，且不能大于 --max-sleep")
    area_id = args.area_id or AREA_IDS.get(args.area)
    if not area_id:
        parser.error("未知地区；请使用 --area-id 指定乙方宝地区 ID")
    token = os.environ.get("QIANLIMA_TOKEN", "").strip()
    token_file = Path(args.qianlima_token_file)
    if not token and token_file.is_file():
        token = token_file.read_text(encoding="utf-8").strip()
        if token_file.stat().st_mode & (stat.S_IRWXG | stat.S_IRWXO):
            print(
                f"[警告] {token_file} 权限过宽，建议执行 chmod 600",
                file=sys.stderr,
            )
    if token.lower().startswith("bearer "):
        token = token[7:].strip()
    if not token:
        parser.error("缺少 QIANLIMA_TOKEN 或 --qianlima-token-file")
    if args.list_limit is not None and args.list_limit < 1:
        parser.error("--list-limit 必须至少为 1")
    if args.max_details is not None and args.max_details < 1:
        parser.error("--max-details 必须至少为 1")
    if args.analyze_details < 0:
        parser.error("--analyze-details 不能为负数")

    return Config(
        keyword=args.keyword,
        area_id=str(area_id),
        date=args.date,
        db_path=Path(args.db),
        output_dir=Path(args.output_dir),
        min_sleep=args.min_sleep,
        max_sleep=args.max_sleep,
        max_pages=args.max_pages,
        list_limit=args.list_limit,
        max_details=args.max_details,
        analyze_details=args.analyze_details,
        analysis_model=args.analysis_model,
        analysis_base_url=os.environ.get(
            "ANTHROPIC_BASE_URL", "https://api.minimaxi.com/anthropic"
        ),
        analysis_token=os.environ.get("ANTHROPIC_AUTH_TOKEN", "").strip(),
        refresh_details=args.refresh_details,
        token=token,
        openid=os.environ.get("QIANLIMA_OPENID", "").strip(),
        cookie=os.environ.get("QIANLIMA_COOKIE", "").strip(),
    )


def _output_path(config: Config) -> Path:
    keyword = re.sub(r"[^\w\u4e00-\u9fff-]+", "_", config.keyword).strip("_")
    config.output_dir.mkdir(parents=True, exist_ok=True)
    return config.output_dir / (
        f"qianlima_{config.date}_{keyword}_{config.area_id}.jsonl"
    )


def _artifact_dir(config: Config) -> Path:
    keyword = re.sub(r"[^\w\u4e00-\u9fff-]+", "_", config.keyword).strip("_")
    path = config.output_dir / f"qianlima_{config.date}_{keyword}_{config.area_id}"
    path.mkdir(parents=True, exist_ok=True)
    return path


def run(config: Config) -> Path:
    store = Store(config.db_path)
    client = QianlimaClient(config)
    ordered_ids: list[str] = []
    items_by_id: dict[str, dict[str, Any]] = {}
    try:
        print("[准备] 建立正常 Chrome 会话")
        client.warm_up()

        total = 0
        for page_number in range(1, config.max_pages + 1):
            items, total = client.search_page(page_number)
            print(
                f"[列表] 第 {page_number} 页 {len(items)} 条，"
                f"接口总数 {total}"
            )
            if not items:
                break
            new_on_page = 0
            for item in items:
                if (
                    config.list_limit is not None
                    and len(ordered_ids) >= config.list_limit
                ):
                    break
                content_id = store.upsert_list_item(item, config.area_id)
                if content_id not in items_by_id:
                    ordered_ids.append(content_id)
                    items_by_id[content_id] = item
                    new_on_page += 1
            if (
                not new_on_page
                or (config.list_limit is not None and len(ordered_ids) >= config.list_limit)
                or len(ordered_ids) >= total
                or len(items) < 30
            ):
                break
        else:
            raise QianlimaError(
                f"达到 {config.max_pages} 页安全上限，未继续请求"
            )

        detail_count = 0
        detail_ids = (
            ordered_ids[: config.max_details]
            if config.max_details is not None
            else ordered_ids
        )
        for content_id in detail_ids:
            if not store.needs_detail(content_id, config.refresh_details):
                print(f"[详情] 跳过已读 {content_id}")
                continue
            item = items_by_id[content_id]
            store.mark_fetching(content_id)
            try:
                detail = client.get_detail(item)
                store.save_detail(content_id, detail)
                detail_count += 1
                print(f"[详情] 已保存 {content_id} {_plain_text(item.get('title'))}")
            except QianlimaRestrictedError as error:
                store.save_restricted(content_id, str(error))
                print(f"[详情] 权限受限 {content_id}: {error}", file=sys.stderr)
            except Exception as error:
                store.save_error(content_id, str(error))
                print(f"[详情] 失败 {content_id}: {error}", file=sys.stderr)

        rows = store.export_rows(ordered_ids)
        output_path = _output_path(config)
        with output_path.open("w", encoding="utf-8") as file:
            for row in rows:
                file.write(json.dumps(row, ensure_ascii=False) + "\n")

        artifact_dir = _artifact_dir(config)
        detail_id_set = set(detail_ids)
        for stale_path in artifact_dir.glob("detail_*"):
            matching_row = next(
                (
                    row
                    for row in rows
                    if stale_path.name.startswith(f"detail_{row['content_id']}_")
                ),
                None,
            )
            if matching_row is None or not matching_row["detail"] or not any(
                stale_path.name.startswith(f"detail_{content_id}_")
                for content_id in detail_id_set
            ):
                stale_path.unlink()
        (artifact_dir / "list.json").write_text(
            json.dumps([row["list"] for row in rows], ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        analyzed = 0
        for row in rows:
            if row["content_id"] not in detail_id_set or not row["detail"]:
                continue
            content_id = row["content_id"]
            cleaned = clean_detail(row["detail"], content_id)
            cleaned["attachment_documents"] = download_and_extract_attachments(
                client, row["detail"], artifact_dir, content_id
            )
            (artifact_dir / f"detail_{content_id}_raw.json").write_text(
                json.dumps(row["detail"], ensure_ascii=False, indent=2),
                encoding="utf-8",
            )
            (artifact_dir / f"detail_{content_id}_clean.json").write_text(
                json.dumps(cleaned, ensure_ascii=False, indent=2),
                encoding="utf-8",
            )
            if analyzed < config.analyze_details:
                analysis = analyze_detail(config, cleaned)
                (artifact_dir / f"detail_{content_id}_analysis.md").write_text(
                    analysis + "\n", encoding="utf-8"
                )
                analyzed += 1
        print(
            f"[完成] 列表 {len(ordered_ids)} 条，本次详情 {detail_count} 条，"
            f"模型分析 {analyzed} 条，输出 {artifact_dir}"
        )
        return output_path
    finally:
        client.close()
        store.close()


def main() -> int:
    try:
        run(_parse_args())
        return 0
    except QianlimaAuthError as error:
        print(f"[错误] {error}", file=sys.stderr)
        return 2
    except (QianlimaError, OSError) as error:
        print(f"[错误] {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
