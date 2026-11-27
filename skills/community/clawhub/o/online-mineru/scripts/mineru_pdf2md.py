#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Online_MinerU — 用 MinerU 精准解析 API 把 PDF 转成 Markdown。

流程：
  1) 拆分 PDF：先按 <=200 页切块，再对 >200MB 的块继续二分，直到「<=200页 且 <=200MB」
  2) 批量申请上传链接（单次 <=50 个）-> PUT 上传（不要设 Content-Type）
  3) 轮询批量任务状态
  4) 下载结果 zip（含 full.md + images/）
  5) 清理页眉页脚 + 重写图片路径 + 按页顺序合并成一个 md（md + images 目录）

Token 读取优先级：--token > 环境变量 MINERU_API_TOKEN > ~/.openclaw/.env > `openclaw secrets store get`(env 类型) > 技能目录 .secrets/mineru_token
"""
from __future__ import annotations

import argparse
import json
import math
import os
import re
import shutil
import subprocess
import sys
import time
import zipfile
from collections import Counter
from pathlib import Path

import requests
from pypdf import PdfReader, PdfWriter

API_BASE = "https://mineru.net"
MAX_PAGES = 200
MAX_BYTES = 200 * 1024 * 1024
UPLOAD_GROUP = 50  # 单次申请上传链接上限


def log(msg: str) -> None:
    print(f"[{time.strftime('%H:%M:%S')}] {msg}", flush=True)


# --------------------------------------------------------------------------- #
# Token
# --------------------------------------------------------------------------- #
def _parse_env_file(path: Path) -> dict:
    out = {}
    try:
        for line in path.read_text(encoding="utf-8", errors="ignore").splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            out[k.strip()] = v.strip().strip('"').strip("'")
    except FileNotFoundError:
        pass
    return out


def resolve_token(explicit: str | None = None) -> str | None:
    if explicit and explicit.strip():
        return explicit.strip()
    v = os.environ.get("MINERU_API_TOKEN", "").strip()
    if v and "__OPENCLAW" not in v and "redacted" not in v.lower():
        return v
    for p in [Path.home() / ".openclaw" / ".env", Path.cwd() / ".env"]:
        d = _parse_env_file(p)
        for k in ("MINERU_API_TOKEN", "MINERU_TOKEN", "MINERU_KEY"):
            if d.get(k):
                return d[k]
    try:
        r = subprocess.run(
            ["openclaw", "secrets", "store", "get", "MINERU_API_TOKEN"],
            capture_output=True, text=True, timeout=20,
        )
        if r.returncode == 0 and r.stdout.strip():
            return r.stdout.strip()
    except Exception:
        pass
    p = Path(__file__).resolve().parent.parent / ".secrets" / "mineru_token"
    if p.exists():
        t = p.read_text(encoding="utf-8").strip()
        if t:
            return t
    return None


# --------------------------------------------------------------------------- #
# PDF helpers
# --------------------------------------------------------------------------- #
def page_count(path: Path) -> int:
    with open(path, "rb") as f:
        return len(PdfReader(f).pages)


def detect_scanned(path: Path, sample: int = 5, threshold: int = 20) -> bool:
    """粗略判断是否为扫描件（几乎没有文字层 -> 需要 OCR）。"""
    with open(path, "rb") as f:
        r = PdfReader(f)
        n = len(r.pages)
        if n == 0:
            return False
        step = max(1, n // sample)
        idxs = list(range(0, n, step))[:sample]
        total = 0
        for i in idxs:
            try:
                total += len((r.pages[i].extract_text() or "").strip())
            except Exception:
                pass
    return (total / max(1, len(idxs))) < threshold


def sanitize(name: str) -> str:
    s = re.sub(r"[^A-Za-z0-9_.-]", "_", name).strip("_")
    return (s or "document")[:60]


def plan_chunks(src: Path, workdir: Path, job: str) -> list[dict]:
    """按 <=200页 且 <=200MB 切块，返回有序 chunk 列表。"""
    workdir.mkdir(parents=True, exist_ok=True)
    leaves: list[tuple[int, int, Path]] = []

    with open(src, "rb") as f:
        reader = PdfReader(f)
        total = len(reader.pages)
        if total == 0:
            raise SystemExit("PDF 没有页面")

        def build(gs: int, ge: int) -> tuple[Path, int]:
            w = PdfWriter()
            for i in range(gs - 1, ge):
                w.add_page(reader.pages[i])
            tmp = workdir / f"part_{gs:05d}_{ge:05d}.pdf"
            with open(tmp, "wb") as o:
                w.write(o)
            return tmp, os.path.getsize(tmp)

        def plan(gs: int, ge: int) -> None:
            pages = ge - gs + 1
            if pages > MAX_PAGES:
                mid = gs + MAX_PAGES - 1
                plan(gs, mid)
                plan(mid + 1, ge)
                return
            tmp, size = build(gs, ge)
            if size > MAX_BYTES and pages > 1:
                tmp.unlink(missing_ok=True)
                mid = (gs + ge) // 2
                plan(gs, mid)
                plan(mid + 1, ge)
                return
            if size > MAX_BYTES and pages == 1:
                raise SystemExit(f"第 {gs} 页单页就超过 200MB，无法按页拆分，请人工处理：{tmp}")
            leaves.append((gs, ge, tmp))

        plan(1, total)

    chunks = []
    for i, (gs, ge, tmp) in enumerate(leaves, 1):
        name = f"{job}__{i:04d}.pdf"
        final = workdir / name
        tmp.replace(final)
        chunks.append({
            "idx": i, "start": gs, "end": ge, "pages": ge - gs + 1,
            "path": str(final), "name": name,
            "data_id": f"{job}__{i:04d}", "size": os.path.getsize(final),
        })
    return chunks


# --------------------------------------------------------------------------- #
# MinerU API
# --------------------------------------------------------------------------- #
def _session(token: str) -> requests.Session:
    s = requests.Session()
    s.headers.update({"Authorization": f"Bearer {token}"})
    return s


def _raise_if_auth(r, body=None) -> None:
    """鉴权失败时给出明确提示（MinerU Key 最多约 90 天有效，过期需更换）。"""
    if r is not None and r.status_code in (401, 403):
        raise SystemExit(
            "MinerU 鉴权失败（HTTP %s）：Token 可能已过期或无效。"
            "Key 最长约 90 天有效，请到 https://mineru.net/apiManage 更换，并更新 MINERU_API_TOKEN。" % r.status_code
        )
    if isinstance(body, dict):
        msg = (str(body.get("msg", "")) + str(body.get("message", ""))).lower()
        code = body.get("code")
        if code not in (0, None) and any(k in msg for k in ("token", "auth", "unauthor", "过期", "invalid", "expire")):
            raise SystemExit(
                f"MinerU 鉴权失败 / Token 可能过期：{body}。"
                "请到 https://mineru.net/apiManage 更换 Key，并更新 MINERU_API_TOKEN。"
            )


def _post_json(s: requests.Session, url: str, payload: dict) -> dict:
    last = None
    for attempt in range(1, 6):
        try:
            r = s.post(url, json=payload, timeout=60)
            if r.status_code < 500:
                j = r.json()
                _raise_if_auth(r, j)
                return j
        except requests.RequestException as e:
            last = e
        time.sleep(min(30, 2 ** attempt))
    raise RuntimeError(f"请求失败: {url}: {last}")


def apply_upload_urls(s, files, model, language, enable_formula, enable_table, is_ocr):
    payload = {
        "model_version": model,
        "language": language,
        "enable_formula": enable_formula,
        "enable_table": enable_table,
        "files": [{"name": f["name"], "data_id": f["data_id"], "is_ocr": is_ocr} for f in files],
    }
    j = _post_json(s, f"{API_BASE}/api/v4/file-urls/batch", payload)
    if j.get("code") != 0:
        raise RuntimeError(f"申请上传链接失败: {j}")
    data = j["data"]
    return data["batch_id"], data["file_urls"]


def upload_file(url: str, path: str) -> None:
    last = None
    for attempt in range(1, 6):
        try:
            with open(path, "rb") as fh:
                r = requests.put(url, data=fh, timeout=600)
            if r.status_code in (200, 201, 204):
                return
            last = f"HTTP {r.status_code}: {r.text[:200]}"
            if r.status_code < 500:
                raise RuntimeError(f"上传失败 {last}")
        except requests.RequestException as e:
            last = str(e)
        time.sleep(min(30, 2 ** attempt))
    raise RuntimeError(f"上传失败: {last}")


def poll_batch(s: requests.Session, batch_id: str, timeout: int, interval: int) -> list:
    start = time.time()
    last_line = ""
    while True:
        r = s.get(f"{API_BASE}/api/v4/extract-results/batch/{batch_id}", timeout=60)
        j = r.json()
        _raise_if_auth(r, j)
        if j.get("code") != 0:
            raise RuntimeError(f"查询批量任务失败: {j}")
        results = j["data"]["extract_result"]
        states = [x.get("state") for x in results]
        summary = " ".join(f"{x.get('file_name','?')}={x.get('state')}" for x in results)
        if summary != last_line:
            log(f"  batch {batch_id}: {summary}")
            last_line = summary
        if all(st in ("done", "failed") for st in states):
            return results
        if time.time() - start > timeout:
            raise TimeoutError(f"批量任务 {batch_id} 等待超时({timeout}s)")
        time.sleep(interval)


def download_zip(url: str, dest: Path) -> None:
    dest.mkdir(parents=True, exist_ok=True)
    zpath = dest / "_result.zip"
    with requests.get(url, stream=True, timeout=600) as r:
        r.raise_for_status()
        with open(zpath, "wb") as f:
            for chunk in r.iter_content(1 << 16):
                f.write(chunk)
    with zipfile.ZipFile(zpath) as z:
        z.extractall(dest)
    zpath.unlink(missing_ok=True)


# --------------------------------------------------------------------------- #
# Markdown 合并
# --------------------------------------------------------------------------- #
PAGE_NUM_RES = [
    re.compile(r"^\s*[-—–]?\s*\d{1,4}\s*[-—–]?\s*$"),
    re.compile(r"^\s*(第\s*\d+\s*页.*|页\s*\d+.*|page\s+\d+.*|\d+\s*/\s*\d+)\s*$", re.I),
]
NOCONTENT_PREFIX = ("#", "|", "!", "<", "*", "-", "•", ">")


def load_hf_texts(chunk_dir: Path) -> set:
    """从 content_list.json 精确提取被标为 header/footer/page_number 的文本。
    MinerU 会给每个版面块标注 type；这些块才是真正的页眉/页脚/页码。"""
    fs = sorted(chunk_dir.glob("*_content_list.json"))
    if not fs:
        return set()
    try:
        data = json.loads(fs[0].read_text(encoding="utf-8"))
    except Exception:
        return set()
    hf = set()
    for d in data:
        if d.get("type") in ("header", "footer", "page_number", "page_header", "page_footer"):
            t = (d.get("text") or "").strip()
            if t:
                hf.add(re.sub(r"\s+", " ", t))
    return hf


def clean_markdown(text: str, page_count: int, hf_set=None, strip_page_numbers: bool = True) -> str:
    """清理页眉/页脚/页码。
    只删：① content_list 中标注为 header/footer/page_number 的整行文本；② 整行是纯页码。
    不做“重复短行”猜测，避免误删正文。注：MinerU 生成 full.md 时通常已自行剔除这些块。
    """
    hf_set = hf_set or set()
    out = []
    blanks = 0
    for l in text.splitlines():
        s = re.sub(r"\s+", " ", l).strip()
        if strip_page_numbers and any(r.match(l) for r in PAGE_NUM_RES):
            continue
        if s and s in hf_set:
            continue
        if s == "":
            blanks += 1
            if blanks > 2:
                continue
        else:
            blanks = 0
        out.append(l)
    return "\n".join(out).strip("\n")


def rewrite_imgs(text: str, chunk_tag: str) -> str:
    for pat in ("](images/", 'src="images/', "src='images/"):
        pre = pat[: -len("images/")]
        text = text.replace(pat, f"{pre}images/{chunk_tag}/")
    return text


def find_md(d: Path) -> Path | None:
    cands = sorted(d.rglob("full.md"))
    if not cands:
        cands = sorted(d.rglob("*.md"), key=lambda p: p.stat().st_size, reverse=True)
    return cands[0] if cands else None


def merge_chunks(recs: dict, workdir: Path, outdir: Path, stem: str, clean_hf: bool) -> tuple[Path, Path]:
    final_dir = outdir / stem
    if final_dir.exists():
        shutil.rmtree(final_dir)
    (final_dir / "images").mkdir(parents=True, exist_ok=True)

    parts = []
    for idx in sorted(recs):
        rec = recs[idx]
        chunk_dir = workdir / f"chunk_{idx:04d}"
        md = find_md(chunk_dir)
        if not md:
            raise RuntimeError(f"第 {idx} 块未找到 markdown")
        text = md.read_text(encoding="utf-8", errors="ignore")
        if clean_hf:
            text = clean_markdown(text, rec["pages"], hf_set=load_hf_texts(chunk_dir))
        tag = f"chunk_{idx:04d}"
        # 复制图片到 images/<tag>/
        for idir in [p for p in chunk_dir.rglob("images") if p.is_dir()]:
            dest = final_dir / "images" / tag
            for p in idir.rglob("*"):
                if p.is_file():
                    dest.mkdir(parents=True, exist_ok=True)
                    target = dest / p.name
                    if not target.exists():
                        shutil.copy2(p, target)
        text = rewrite_imgs(text, tag)
        if text.strip():
            parts.append(text.strip("\n"))

    merged = "\n\n".join(parts) + "\n"
    mdfile = final_dir / f"{stem}.md"
    mdfile.write_text(merged, encoding="utf-8")
    (final_dir / "manifest.json").write_text(
        json.dumps({"chunks": {str(k): v for k, v in recs.items()}}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    return mdfile, final_dir


# --------------------------------------------------------------------------- #
# State / main
# --------------------------------------------------------------------------- #
def load_state(p: Path):
    if p.exists():
        try:
            return json.loads(p.read_text(encoding="utf-8"))
        except Exception:
            return None
    return None


def save_state(p: Path, st: dict) -> None:
    p.write_text(json.dumps(st, ensure_ascii=False, indent=2), encoding="utf-8")


def run(args) -> Path:
    src = Path(args.pdf).expanduser().resolve()
    if not src.exists():
        raise SystemExit(f"找不到 PDF: {src}")
    stem = args.name or src.stem
    job = sanitize(stem)
    workdir = Path(args.workdir).expanduser() if args.workdir else src.parent / ".mineru_work" / job
    outdir = Path(args.outdir).expanduser() if args.outdir else src.parent
    workdir.mkdir(parents=True, exist_ok=True)
    statep = workdir / "state.json"

    st = load_state(statep) if args.resume else None
    if not st:
        st = {"input": str(src), "stem": stem, "chunks": [], "groups": [], "results": {}}

    if not st["chunks"] or not all(Path(c["path"]).exists() for c in st["chunks"]):
        n = page_count(src)
        log(f"PDF 共 {n} 页，开始规划拆分（<= {MAX_PAGES} 页 / {MAX_BYTES // 1024 // 1024}MB）...")
        st["chunks"] = plan_chunks(src, workdir, job)
        save_state(statep, st)

    chunks = st["chunks"]
    log(f"分块数：{len(chunks)}  ->  " + ", ".join(
        f"#{c['idx']}(p{c['start']}-{c['end']},{c['size'] // 1024 // 1024}MB)" for c in chunks))

    if args.dry_run:
        log("--dry-run：仅拆分，不调用 API。")
        return workdir / "_dry_run"

    token = resolve_token(args.token)
    if not token:
        raise SystemExit(
            "未找到 MINERU_API_TOKEN。请先设置环境变量 / ~/.openclaw/.env / OpenClaw secrets store / 技能 .secrets/mineru_token"
        )

    if args.ocr == "auto":
        is_ocr = detect_scanned(src)
    elif args.ocr == "on":
        is_ocr = True
    else:
        is_ocr = False
    log(f"OCR：{'开启' if is_ocr else '关闭'}（--ocr {args.ocr}）")

    s = _session(token)
    done_idx = {int(k) for k, v in st["results"].items() if v.get("state") == "done"}
    covered = set()
    for g in st["groups"]:
        covered.update(g["idx"])
    pending = [c["idx"] for c in chunks if c["idx"] not in done_idx and c["idx"] not in covered]

    for i in range(0, len(pending), UPLOAD_GROUP):
        grp = pending[i:i + UPLOAD_GROUP]
        files = [next(c for c in chunks if c["idx"] == j) for j in grp]
        bid, urls = apply_upload_urls(
            s, files, args.model, args.language,
            not args.no_formula, not args.no_table, is_ocr,
        )
        log(f"申请到上传链接 batch={bid}（{len(urls)} 个）")
        if len(urls) != len(files):
            raise RuntimeError(f"上传链接数量不匹配：{len(urls)} != {len(files)}")
        for f, u in zip(files, urls):
            upload_file(u, f["path"])
            log(f"已上传 #{f['idx']} {f['name']}")
        st["groups"].append({"batch_id": bid, "idx": grp, "uploaded": True})
        save_state(statep, st)

    for g in st["groups"]:
        need = [j for j in g["idx"] if st["results"].get(str(j), {}).get("state") != "done"]
        if not need:
            continue
        log(f"轮询 batch={g['batch_id']} ...")
        results = poll_batch(s, g["batch_id"], args.timeout, args.poll_interval)
        byid = {}
        for r in results:
            if r.get("data_id"):
                byid[str(r["data_id"])] = r
            if r.get("file_name"):
                byid[str(r["file_name"])] = r
        for j in g["idx"]:
            c = next(x for x in chunks if x["idx"] == j)
            r = byid.get(c["data_id"]) or byid.get(c["name"]) or {}
            st["results"][str(j)] = {
                "state": r.get("state"),
                "zip_url": r.get("full_zip_url"),
                "err": r.get("err_msg", ""),
            }
        save_state(statep, st)

    all_idx = [c["idx"] for c in chunks]
    failed = [j for j in all_idx if st["results"].get(str(j), {}).get("state") != "done"]
    if failed:
        for j in failed:
            log(f"失败/未完成 #{j}: {st['results'].get(str(j))}")
        if not args.allow_partial:
            raise SystemExit(f"{len(failed)} 块未成功，已中止合并（可加 --resume 重试，或 --allow-partial 只合并成功块）")

    for c in chunks:
        j = c["idx"]
        rec = st["results"][str(j)]
        if rec.get("state") != "done":
            continue
        cdir = workdir / f"chunk_{j:04d}"
        if not (cdir.exists() and find_md(cdir)):
            log(f"下载结果 #{j} ...")
            download_zip(rec["zip_url"], cdir)
            rec["extracted"] = True
            save_state(statep, st)

    rmap = {
        c["idx"]: {"pages": c["pages"]}
        for c in chunks
        if st["results"].get(str(c["idx"]), {}).get("state") == "done"
    }
    mdfile, finaldir = merge_chunks(rmap, workdir, outdir, stem, clean_hf=not args.no_clean_hf)
    log(f"完成 ✅  输出：{mdfile}")
    log(f"图片目录：{finaldir / 'images'}")
    if not args.keep_temp:
        log(f"中间文件保留在：{workdir}（加 --keep-temp 可保留；需要可手动删除）")
    return mdfile


def _submit_url_batch(s, items, model, language, enable_formula, enable_table):
    payload = {
        "model_version": model,
        "language": language,
        "enable_formula": enable_formula,
        "enable_table": enable_table,
        "files": items,
    }
    j = _post_json(s, f"{API_BASE}/api/v4/extract/task/batch", payload)
    if j.get("code") != 0:
        raise RuntimeError(f"提交 URL 批量任务失败: {j}")
    return j["data"]["batch_id"]


def run_url(args) -> Path:
    """URL 模式：文件不落地本机，交给 MinerU 服务器侧拉取解析。
    无需下载大文件——只要 URL 是 MinerU 能访问的（国内地址最佳）。
    >200 页时用 --total-pages 传递总页数，脚本按 page_ranges 自动分片。
    """
    if not args.pdf_url:
        raise SystemExit("--pdf-url 为空")
    stem = args.name or Path(args.pdf_url.split("?")[0]).stem or "document"
    job = sanitize(stem)
    workdir = Path(args.workdir).expanduser() if args.workdir else Path.cwd() / ".mineru_work" / job
    outdir = Path(args.outdir).expanduser() if args.outdir else Path.cwd()
    workdir.mkdir(parents=True, exist_ok=True)
    token = resolve_token(args.token)
    if not token:
        raise SystemExit("未找到 MINERU_API_TOKEN")
    s = _session(token)

    tp = args.total_pages or 0
    if tp > MAX_PAGES:
        ranges = [(a, min(tp, a + MAX_PAGES - 1)) for a in range(1, tp + 1, MAX_PAGES)]
    else:
        ranges = [(None, None)]

    is_ocr = args.ocr == "on"
    items = []
    for i, (a, b) in enumerate(ranges, 1):
        it = {"url": args.pdf_url, "data_id": f"{job}__{i:04d}", "is_ocr": is_ocr}
        if a:
            it["page_ranges"] = f"{a}-{b}"
        items.append(it)
    log(f"URL 模式：{len(items)} 个任务  URL={args.pdf_url}")

    if args.dry_run:
        for it in items:
            log("DRY " + json.dumps(it, ensure_ascii=False))
        return workdir / "_dry"

    bid = _submit_url_batch(s, items, args.model, args.language, not args.no_formula, not args.no_table)
    log(f"批量任务 batch={bid}，开始轮询 ...")
    results = poll_batch(s, bid, args.timeout, args.poll_interval)
    byid = {}
    for r in results:
        if r.get("data_id"):
            byid[str(r["data_id"])] = r
        if r.get("file_name"):
            byid[str(r["file_name"])] = r

    recs = {}
    for i, (a, b) in enumerate(ranges, 1):
        key = f"{job}__{i:04d}"
        r = byid.get(key) or {}
        if r.get("state") != "done":
            log(f"#{i} 未完成: {r.get('state')} {r.get('err_msg', '')}")
            if not args.allow_partial:
                raise SystemExit("存在未完成/失败的块")
            continue
        cdir = workdir / f"chunk_{i:04d}"
        if not (cdir.exists() and find_md(cdir)):
            download_zip(r["full_zip_url"], cdir)
        recs[i] = {"pages": (b - a + 1) if a else 1}

    mdfile, finaldir = merge_chunks(recs, workdir, outdir, stem, clean_hf=not args.no_clean_hf)
    log(f"完成 ✅  输出：{mdfile}")
    return mdfile


def main(argv=None):
    ap = argparse.ArgumentParser(description="MinerU 精准解析 API：PDF -> Markdown（自动拆分/合并）")
    ap.add_argument("pdf", nargs="?", help="输入 PDF 文件路径（本地文件模式）")
    ap.add_argument("--pdf-url", help="URL 模式：直接交给 MinerU 服务器侧拉取（无需本地文件）")
    ap.add_argument("--total-pages", type=int, default=0, help="URL 模式下文件总页数（>200 页时用于自动分片）")
    ap.add_argument("--outdir", help="输出目录（默认与 PDF 同级）")
    ap.add_argument("--workdir", help="中间文件目录（默认 <pdf目录>/.mineru_work/<job>）")
    ap.add_argument("--name", help="输出名/文件名前缀（默认用 PDF 文件名）")
    ap.add_argument("--token", help="MinerU Token（默认读环境变量/配置文件）")
    ap.add_argument("--model", default="vlm", choices=["vlm", "pipeline"], help="模型版本，默认 vlm")
    ap.add_argument("--language", default="ch", help="文档语言，默认 ch")
    ap.add_argument("--ocr", default="auto", choices=["auto", "on", "off"], help="是否 OCR：auto 自动判断是否扫描件")
    ap.add_argument("--no-formula", action="store_true", help="关闭公式识别")
    ap.add_argument("--no-table", action="store_true", help="关闭表格识别")
    ap.add_argument("--no-clean-hf", action="store_true", help="关闭页眉页脚清理")
    ap.add_argument("--resume", action="store_true", help="复用 state.json 断点续传")
    ap.add_argument("--allow-partial", action="store_true", help="允许只合并成功的块")
    ap.add_argument("--keep-temp", action="store_true", help="保留中间文件")
    ap.add_argument("--dry-run", action="store_true", help="只拆分并打印分块，不调用 API")
    ap.add_argument("--timeout", type=int, default=3600, help="单批任务等待上限秒数，默认 3600")
    ap.add_argument("--poll-interval", type=int, default=10, help="轮询间隔秒数，默认 10")
    args = ap.parse_args(argv)
    if args.pdf_url:
        run_url(args)
        return
    if not args.pdf:
        ap.error("需要提供 PDF 路径，或使用 --pdf-url")
    run(args)


if __name__ == "__main__":
    main()
