# GxpCode Skill — ③ 获取详情页文本 + 下载附件 PDF（按域名并发）

import json
import os
import re
import shutil
import time
import base64
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.parse import urlparse
from playwright.sync_api import sync_playwright

import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

BATCH = 5
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/125.0.0.0 Safari/537.36"


def _domain(url: str) -> str:
    return urlparse(url).netloc


def _domain_root(url: str) -> str:
    parsed = urlparse(url)
    return f"{parsed.scheme}://{parsed.netloc}"


def _safe_filename(source: str, title: str) -> str:
    safe = re.sub(r"[\\/:*?\"<>|]", "_", title)[:60]
    return f"{source}_{safe}.pdf"


def _download_pdf(page, pdf_url: str, output_dir: str, filename: str) -> str:
    path = os.path.join(output_dir, filename)
    try:
        data = page.evaluate(f"""async () => {{
            const r = await fetch('{pdf_url}');
            const b = await r.blob();
            return new Promise((ok) => {{
                const fr = new FileReader();
                fr.onload = () => ok(fr.result);
                fr.readAsDataURL(b);
            }});
        }}""")
        if data and "," in str(data):
            b64 = str(data).split(",", 1)[1]
            with open(path, "wb") as f:
                f.write(base64.b64decode(b64))
        return path if os.path.exists(path) else ""
    except Exception:
        return ""


def _process_domain(domain: str, items: list, pdf_dir: str) -> list:
    """一个线程处理一个域名的所有条目"""
    results = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=["--no-sandbox", "--disable-blink-features=AutomationControlled"])
        for batch_start in range(0, len(items), BATCH):
            batch = items[batch_start:batch_start + BATCH]
            context = browser.new_context(user_agent=UA, viewport={"width": 1920, "height": 1080}, locale="zh-CN")
            for item in batch:
                url = item["url"]
                print(f"[{domain}] {item['title'][:50]}...")
                page = context.new_page()
                try:
                    try:
                        page.goto(url, timeout=30000, wait_until="domcontentloaded")
                    except Exception as ge:
                        if "Download is starting" in str(ge):
                            # PIC/S: 详情页是 PDF，先跳到首页再 fetch
                            page.goto(_domain_root(url), timeout=15000, wait_until="domcontentloaded")
                            data = page.evaluate(f"""async () => {{
                                const r = await fetch('{url}');
                                const b = await r.blob();
                                return new Promise((ok) => {{
                                    const fr = new FileReader();
                                    fr.onload = () => ok(fr.result);
                                    fr.readAsDataURL(b);
                                }});
                            }}""")
                            fname = _safe_filename(item["source"].replace("/", "_"), item["title"])
                            path = os.path.join(pdf_dir, fname)
                            if data and "," in str(data):
                                b64 = str(data).split(",", 1)[1]
                                with open(path, "wb") as f:
                                    f.write(base64.b64decode(b64))
                            item["detail_text"] = "[PDF document]"
                            item["attachment"] = path if os.path.exists(path) else ""
                            results.append(item)
                            page.close()
                            continue
                        else:
                            raise
                    time.sleep(2)
                    body = page.evaluate("() => document.body.innerText")
                    attachment = ""
                    for sel in ['a[href*="/main/att/download/"]', 'a[href$=".pdf"]']:
                        for a in page.query_selector_all(sel):
                            href = a.get_attribute("href") or ""
                            if href:
                                fname = _safe_filename(item["source"].replace("/", "_"), item["title"])
                                attachment = _download_pdf(page, href, pdf_dir, fname)
                                if attachment:
                                    break
                        if attachment:
                            break
                    item["detail_text"] = body[:5000]
                    item["attachment"] = attachment
                    results.append(item)
                except Exception as e:
                    print(f"  [{domain}] FAIL: {e}")
                finally:
                    page.close()
            context.close()
        browser.close()
    return results


def run(gxpcode: str):
    s2_dir = os.path.join(gxpcode, "s2")
    if not os.path.exists(s2_dir):
        print("s2/ not found, skip S3")
        return

    # 收集所有 s2 文件
    all_items = []
    for fname in os.listdir(s2_dir):
        if fname.endswith(".json"):
            with open(os.path.join(s2_dir, fname), "r", encoding="utf-8") as f:
                items = json.load(f)
            if items:
                all_items.extend(items)

    if not all_items:
        print("s2/ is empty, skip S3")
        return

    # PDF 下载到工作空间（第二参数），未指定则落在 gxpcode_data 外的工作目录
    if len(sys.argv) > 2:
        output_root = sys.argv[2]
    else:
        output_root = os.getcwd()
    pdf_dir = os.path.join(output_root, "gxpcode_pdfs")
    os.makedirs(pdf_dir, exist_ok=True)

    # 按域名分组并发
    groups = defaultdict(list)
    for item in all_items:
        groups[_domain(item["url"])].append(item)

    print(f"Groups: { {k: len(v) for k, v in groups.items()} }")

    all_results = []
    with ThreadPoolExecutor(max_workers=len(groups)) as executor:
        futures = {
            executor.submit(_process_domain, domain, grp, pdf_dir): domain
            for domain, grp in groups.items()
        }
        for future in as_completed(futures):
            domain = futures[future]
            try:
                r = future.result()
                all_results.extend(r)
                print(f"[{domain}] done: {len(r)} items")
            except Exception as e:
                print(f"[{domain}] CRASH: {e}")

    # 空 body 重试（上限 2 轮）
    for retry_round in range(1, 3):
        empty = [d for d in all_results if not d["detail_text"]]
        if not empty:
            break
        print(f"Retry round {retry_round}: {len(empty)} empty items")
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True, args=["--no-sandbox", "--disable-blink-features=AutomationControlled"])
            context = browser.new_context(user_agent=UA, viewport={"width": 1920, "height": 1080}, locale="zh-CN")
            for item in empty:
                url = item["url"]
                page = context.new_page()
                try:
                    page.goto(url, timeout=30000, wait_until="domcontentloaded")
                    time.sleep(2)
                    body = page.evaluate("() => document.body.innerText")
                    if body:
                        item["detail_text"] = body[:5000]
                except Exception:
                    pass
                finally:
                    page.close()
                    time.sleep(2)
            context.close()
            browser.close()

    # 按 source 分文件输出（先写临时目录，完成后原子 rename）
    s3_dir = os.path.join(gxpcode, "s3")
    s3_tmp = os.path.join(gxpcode, "s3_tmp")
    if os.path.exists(s3_tmp):
        shutil.rmtree(s3_tmp)
    os.makedirs(s3_tmp, exist_ok=True)
    src_groups = defaultdict(list)
    for d in all_results:
        src_groups[d["source"]].append(d)
    for src, grp in src_groups.items():
        path = os.path.join(s3_tmp, f"s3_{src.replace('/', '_')}.json")
        with open(path, "w", encoding="utf-8") as f:
            json.dump(grp, f, ensure_ascii=False, indent=2)
    # 标记完成（先写 tmp 再整体替换）
    with open(os.path.join(s3_tmp, ".done"), "w") as f:
        f.write("")
    if os.path.exists(s3_dir):
        shutil.rmtree(s3_dir)
    os.rename(s3_tmp, s3_dir)
    ok = sum(1 for d in all_results if d['detail_text'])
    empty = sum(1 for d in all_results if not d['detail_text'])
    pdfs = sum(1 for d in all_results if d.get('attachment'))
    print(f"s3/: {len(all_results)} items in {len(src_groups)} files (OK={ok}, EMPTY={empty}, PDF={pdfs})")


if __name__ == "__main__":
    import sys
    run(sys.argv[1] if len(sys.argv) > 1 else "gxpcode_data")
