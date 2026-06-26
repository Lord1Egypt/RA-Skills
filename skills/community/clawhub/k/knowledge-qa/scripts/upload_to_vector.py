# -*- coding: utf-8 -*-
import sys as _sys
_sys.stdout.reconfigure(encoding='utf-8')
_sys.stderr.reconfigure(encoding='utf-8')

"""
知识库向量上传脚本
功能：
1. 扫描 raw_docs 目录下的所有文件（PDF/MD/DOCX）
2. 识别新文件（对比 indexed_files.json）
3. 提取文本内容并分块
4. 调用百炼 API 生成向量
5. 调用 DashVector API 上传
6. 更新 indexed_files.json
"""

import json
import os
import hashlib
import re
import time
from datetime import datetime

import pdfplumber
import requests
import argparse


def load_config(kb_path=None):
    """
    加载知识库配置。
    kb_path: 知识库根目录路径。
             不传 -> 自动发现（当前目录或父目录）
             传入 -> 直接在 kb_path 下找 config.json
    """
    if kb_path is None:
        kb_path = _find_knowledge_base()
        if kb_path is None:
            raise FileNotFoundError(
                "未找到知识库目录。请确保当前目录或其子目录包含 raw_docs/ 和 config.json，"
                "或使用 --kb-path 参数指定知识库路径。"
            )
    config_path = os.path.join(kb_path, "config.json")
    with open(config_path, "r", encoding="utf-8") as f:
        return json.load(f)


def _find_knowledge_base(start_path=None):
    """
    自动发现知识库目录。
    查找逻辑：当前目录 -> 当前目录子目录 -> 父目录子目录
    """
    if start_path is None:
        start_path = os.getcwd()

    if os.path.isdir(start_path):
        raw = os.path.join(start_path, "raw_docs")
        cfg = os.path.join(start_path, "config.json")
        if os.path.isdir(raw) and os.path.isfile(cfg):
            return start_path

    candidates = []
    if os.path.isdir(start_path):
        for item in os.listdir(start_path):
            sub = os.path.join(start_path, item)
            if os.path.isdir(sub):
                raw = os.path.join(sub, "raw_docs")
                cfg = os.path.join(sub, "config.json")
                if os.path.isdir(raw) and os.path.isfile(cfg):
                    candidates.append(sub)

    if candidates:
        return candidates[0]

    parent = os.path.dirname(start_path)
    if parent and parent != start_path and os.path.isdir(parent):
        for item in os.listdir(parent):
            sub = os.path.join(parent, item)
            if os.path.isdir(sub):
                raw = os.path.join(sub, "raw_docs")
                cfg = os.path.join(sub, "config.json")
                if os.path.isdir(raw) and os.path.isfile(cfg):
                    return sub

    return None


def load_indexed_files(config):
    path = config["knowledge_base"]["indexed_files_path"]
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"last_updated": None, "files": []}


def save_indexed_files(config, data):
    path = config["knowledge_base"]["indexed_files_path"]
    data["last_updated"] = datetime.now().isoformat()
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def safe_doc_id(filename, chunk_index):
    """生成 DashVector 合法的文档 ID（只允许 [a-zA-Z0-9_-!@#$%+=.]）"""
    import urllib.parse
    name = os.path.splitext(filename)[0]
    safe_name = urllib.parse.quote(name, safe='')
    if len(safe_name) > 40:
        safe_name = safe_name[:40]
    return f"{safe_name}_{chunk_index}"


def scan_raw_docs(root_path):
    """
    递归扫描 raw_docs 目录下的所有文件。
    返回的每个文件记录包含 partition 字段：
    - 直接在 raw_docs 根目录 -> partition = "default"
    - 在 raw_docs/FOLDER/ 子目录 -> partition = folder_name（小写，字母数字下划线）
    """
    files = []
    for root, dirs, filenames in os.walk(root_path):
        rel_root = os.path.relpath(root, root_path)

        if rel_root == ".":
            partition = "default"
        else:
            parts = rel_root.split(os.sep)
            folder_name = parts[0]
            partition = re.sub(r"[^a-z0-9_]", "_", folder_name.lower())

        for filename in filenames:
            if filename.lower() == "readme.md":
                continue
            filepath = os.path.join(root, filename)
            rel_path = os.path.relpath(filepath, root_path)
            files.append({
                "path": filepath,
                "relative_path": rel_path,
                "name": filename,
                "size": os.path.getsize(filepath),
                "partition": partition
            })
    return files


def extract_text_pdf(filepath):
    """使用 pdfplumber 提取 PDF 文本"""
    texts = []
    try:
        with pdfplumber.open(filepath) as pdf:
            for i, page in enumerate(pdf.pages):
                text = page.extract_text()
                if text and text.strip():
                    texts.append(f"[Page {i+1}]\n{text}")
        return "\n\n".join(texts)
    except Exception as e:
        print(f"  PDF read failed: {e}")
        return ""


def extract_text_md(filepath):
    """读取 Markdown 文本"""
    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()


def extract_text_docx(filepath):
    """读取 Word 文档文本"""
    try:
        from docx import Document
        doc = Document(filepath)
        return "\n".join([p.text for p in doc.paragraphs if p.text.strip()])
    except ImportError:
        print("  Note: python-docx not installed, cannot read .docx files")
        return ""


def extract_content(filepath):
    """根据文件类型提取文本内容"""
    ext = os.path.splitext(filepath)[1].lower()
    if ext == ".pdf":
        return extract_text_pdf(filepath)
    elif ext == ".md":
        return extract_text_md(filepath)
    elif ext in [".docx", ".doc"]:
        return extract_text_docx(filepath)
    else:
        return ""


def chunk_text(text, chunk_size=600, overlap=50):
    """将长文本分块，便于向量检索"""
    paragraphs = re.split(r'\n\s*\n', text)
    chunks = []
    current_chunk = ""

    for para in paragraphs:
        if len(current_chunk) + len(para) < chunk_size:
            current_chunk += para + "\n\n"
        else:
            if current_chunk.strip():
                chunks.append(current_chunk.strip())
            overlap_text = current_chunk[-overlap:] if len(current_chunk) > overlap else current_chunk
            current_chunk = overlap_text + para + "\n\n"

    if current_chunk.strip():
        chunks.append(current_chunk.strip())

    return [c[:2000] for c in chunks]


def generate_embeddings_bailian(config, texts):
    """调用百炼 API 生成向量"""
    api_key = config["bailian"]["api_key"]
    model = config["bailian"].get("model", "text-embedding-v3")
    dimension = config["dashvector"]["dimension"]

    url = "https://dashscope.aliyuncs.com/compatible-mode/v1/embeddings"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    all_embeddings = []
    for i, text in enumerate(texts):
        payload = {
            "model": model,
            "input": text,
            "dimensions": dimension,
            "encoding_format": "float"
        }
        try:
            response = requests.post(url, headers=headers, json=payload, timeout=30)
            if response.status_code == 200:
                result = response.json()
                embedding = result["data"][0]["embedding"]
                all_embeddings.append(embedding)
            else:
                print(f"  Vector generation failed: {response.status_code} - {response.text[:200]}")
                return None
        except Exception as e:
            print(f"  Vector generation error: {e}")
            return None

    return all_embeddings


def create_partition_if_not_exists(config, partition_name):
    """
    如果 DashVector 分区不存在，则创建它。
    partition_name: 合法的分区名（小写字母、数字、下划线）
    """
    api_key = config["dashvector"]["api_key"]
    endpoint = config["dashvector"]["endpoint"]
    collection = config["dashvector"]["collection_name"]
    url = f"{endpoint}/v1/collections/{collection}/partitions"
    headers = {
        "dashvector-auth-token": api_key,
        "Content-Type": "application/json"
    }

    payload = {"name": partition_name}
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        resp_data = response.json()
        if response.status_code == 200 and resp_data.get("code") == 0:
            return True, f"Partition '{partition_name}' created"
        elif resp_data.get("code") == 60010:
            return True, f"Partition '{partition_name}' already exists"
        else:
            return False, f"Failed to create partition: code={resp_data.get('code')} msg={resp_data.get('message')}"
    except Exception as e:
        return False, f"Partition creation error: {e}"


def upload_with_retry(url, headers, payload, max_retries=4, base_delay=1.0):
    """
    带指数退避的 HTTP POST 请求。
    遇到 405 / 429 / 503 时自动重试。
    返回 (response, attempts, last_error_hint)，attempts 为尝试次数，
    last_error_hint 为连续 405 时的第一条错误信息（方便诊断）。
    """
    last_resp = None
    last_error_hint = None
    consecutive_405 = 0

    for attempt in range(max_retries):
        try:
            resp = requests.post(url, headers=headers, json=payload, timeout=60)
            last_resp = resp

            if resp.status_code == 200:
                if attempt > 0:
                    print(f"    [+] Attempt {attempt + 1}: HTTP 200 OK (recovered after {attempt} retries)")
                return resp, attempt + 1, None

            if resp.status_code in (405, 429, 503):
                consecutive_405 += 1
                # 记录第一条 405 的响应体用于诊断（通常包含了拒绝原因）
                if consecutive_405 == 1:
                    last_error_hint = f"HTTP {resp.status_code}: {resp.text[:300]}"
                # 连续 3 次 405 说明服务端明确拒绝，不必继续重试
                if consecutive_405 >= 3:
                    print(f"    [x] HTTP {resp.status_code} repeated {consecutive_405}x — request rejected by server, stopping retries")
                    break
                delay = base_delay * (2 ** attempt)
                print(f"    [!] HTTP {resp.status_code} (attempt {attempt + 1}/{max_retries}), "
                      f"waiting {delay:.1f}s... [reason: {resp.text[:100]}]")
                time.sleep(delay)
                continue

            # 其他 HTTP 错误（400/401/500 等）不重试
            print(f"    [x] HTTP {resp.status_code}: {resp.text[:200]}")
            return resp, attempt + 1, None

        except requests.exceptions.Timeout:
            print(f"    [!] Timeout (attempt {attempt + 1}/{max_retries}), retrying...")
            consecutive_405 = 0
            time.sleep(base_delay * (2 ** attempt))
        except Exception as e:
            print(f"    [!] Request error: {e} (attempt {attempt + 1}/{max_retries})")
            consecutive_405 = 0
            time.sleep(base_delay * (2 ** attempt))

    # 所有重试均失败
    return last_resp, max_retries, last_error_hint


def upload_to_dashvector(config, docs, partition, batch_size=1, max_retries=4):
    """
    调用 DashVector API 上传文档（含向量），小批量多次上传。
    partition: 物理分区名（放在请求体顶层，作用于整批文档）
    遇到 405/429/503 时自动指数退避重试（最多 4 次）。
    """
    api_key = config["dashvector"]["api_key"]
    endpoint = config["dashvector"]["endpoint"]
    collection = config["dashvector"]["collection_name"]
    url = f"{endpoint}/v1/collections/{collection}/docs"
    headers = {
        "dashvector-auth-token": api_key,
        "Content-Type": "application/json"
    }

    all_success = True
    all_results = []
    total = len(docs)

    for i in range(0, total, batch_size):
        batch = docs[i:i+batch_size]
        batch_num = i // batch_size + 1
        batch_start = i + 1
        batch_end = min(i + batch_size, total)
        print(f"    Uploading {batch_start}-{batch_end}/{total}...")

        payload = {"partition": partition, "docs": batch}
        payload_size = len(json.dumps(payload, ensure_ascii=False).encode("utf-8"))
        print(f"    Payload size: {payload_size} bytes ({len(batch)} doc(s))")

        try:
            response, attempts, error_hint = upload_with_retry(url, headers, payload,
                                                               max_retries=max_retries, base_delay=1.0)

            if response is None or response.status_code != 200:
                # 所有重试全部失败
                all_success = False
                http_code = response.status_code if response is not None else "timeout"
                err_msg = f"HTTP {http_code} after {attempts} attempts"
                if error_hint:
                    err_msg += f" | first 405: {error_hint}"
                all_results.append({
                    "batch": batch_num,
                    "range": f"{batch_start}-{batch_end}",
                    "error": err_msg
                })
                print(f"    [x] Upload failed after {attempts} attempts")
                if error_hint:
                    print(f"    [i] First 405 hint: {error_hint}")
                continue

            # HTTP 200，检查业务层 code
            resp_data = response.json()

            if resp_data.get("code") != 0:
                all_success = False
                all_results.append({
                    "batch": batch_num,
                    "range": f"{batch_start}-{batch_end}",
                    "error": f"API code={resp_data.get('code')}: {resp_data.get('message')}"
                })
                print(f"    [x] API error: code={resp_data.get('code')}")
                continue

            outputs = resp_data.get("output", [])
            # -2027 = Duplicate Key，幂等跳过不算失败
            failed = [d for d in outputs if d.get("code") != 0 and d.get("code") != -2027]
            if failed:
                all_success = False
                all_results.append({"batch": batch_num, "range": f"{batch_start}-{batch_end}", "failed": failed})
                print(f"    [!] {len(failed)} chunk(s) failed")
            else:
                skipped = [d for d in outputs if d.get("code") == -2027]
                ok_count = len(outputs) - len(skipped)
                if skipped:
                    print(f"    [+] {ok_count} uploaded, {len(skipped)} duplicates skipped")
                else:
                    print(f"    [+] {ok_count} uploaded successfully")

        except Exception as e:
            all_success = False
            all_results.append({
                "batch": batch_num,
                "range": f"{batch_start}-{batch_end}",
                "exception": str(e)
            })
            print(f"    [x] Exception: {e}")

        # 批次间稍微间隔，降低触发限流概率
        if i + batch_size < total:
            time.sleep(0.3)

    return all_success, all_results


def main():
    parser = argparse.ArgumentParser(description="Knowledge base vector upload script")
    parser.add_argument("--kb-path", dest="kb_path", default=None,
                        help="Knowledge base path, auto-detect if not provided")
    args = parser.parse_args()

    print("=" * 50)
    print("Knowledge Base Vector Upload")
    print("=" * 50)

    kb_path = args.kb_path
    if kb_path:
        print(f"\nSpecified knowledge base: {kb_path}")
    else:
        print(f"\nAuto-detecting knowledge base...")

    config = load_config(kb_path)
    print(f"\nConfig loaded")
    print(f"  DashVector Collection: {config['dashvector']['collection_name']}")
    print(f"  Bailian Model: {config['bailian']['model']}")
    print(f"  Vector Dimension: {config['dashvector']['dimension']}")

    root_path = config["knowledge_base"]["root_path"]
    all_files = scan_raw_docs(root_path)
    print(f"\nScan complete, found {len(all_files)} files")

    from collections import Counter
    partition_counts = Counter(f["partition"] for f in all_files)
    print(f"  Partition distribution: {dict(partition_counts)}")

    indexed = load_indexed_files(config)
    indexed_names = {f["name"] for f in indexed["files"]}
    print(f"Already indexed: {len(indexed_names)} files")

    new_files = [f for f in all_files if f["name"] not in indexed_names]
    if not new_files:
        print("\nNo new files found, upload complete")
        return

    print(f"\nFound {len(new_files)} new files:")
    for f in new_files:
        print(f"  - [{f['partition']}] {f['relative_path']}")

    needed_partitions = set(f["partition"] for f in new_files)
    print(f"\nEnsuring partitions exist: {needed_partitions}")
    for pname in sorted(needed_partitions):
        if pname == "default":
            continue
        ok, msg = create_partition_if_not_exists(config, pname)
        print(f"  {msg}")

    total_uploaded = 0
    for file_info in new_files:
        partition = file_info["partition"]
        print(f"\nProcessing: [{partition}] {file_info['relative_path']}")

        content = extract_content(file_info["path"])
        if not content:
            print(f"  Skipped: unable to extract content")
            continue

        print(f"  Text length: {len(content)} chars")
        chunks = chunk_text(content)
        print(f"  Chunks: {len(chunks)}")

        print(f"  Generating vectors...")
        embeddings = generate_embeddings_bailian(config, chunks)
        if not embeddings:
            print(f"  Vector generation failed, skipping")
            continue

        print(f"  Vectors generated ({len(embeddings)} embeddings)")

        docs = []
        for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
            docs.append({
                "id": safe_doc_id(f"{partition}_{file_info['name']}", i),
                "vector": embedding,
                "fields": {
                    "content": chunk,
                    "source": file_info["name"],
                    "partition": partition,
                    "chunk_index": i
                }
            })

        print(f"  Uploading to DashVector ({len(docs)} chunks, partition={partition})...")
        success, result = upload_to_dashvector(config, docs, partition=partition, max_retries=4)
        if success:
            indexed["files"].append({
                "name": file_info["name"],
                "relative_path": file_info["relative_path"],
                "size": file_info["size"],
                "indexed_at": datetime.now().isoformat(),
                "chunks": len(chunks),
                "partition": partition
            })
            total_uploaded += 1
            print(f"  Upload successful! ({len(chunks)} chunks)")
        else:
            print(f"  Upload failed: {result}")

    save_indexed_files(config, indexed)
    print(f"\nIndex record updated: {len(indexed['files'])} files total")

    print(f"\n{'=' * 50}")
    print(f"Upload complete! {total_uploaded} files uploaded")
    print(f"{'=' * 50}")


if __name__ == "__main__":
    main()
