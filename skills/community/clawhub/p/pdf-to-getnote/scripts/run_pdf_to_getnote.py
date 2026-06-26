#!/usr/bin/env python3
"""
PDF 转 GetNotes 笔记 - 一键脚本
凭证自动从 ~/.openclaw/openclaw.json → skills.entries.getnote 读取
用法: python3 run_pdf_to_getnote.py <pdf_path> [topic_id] [title]
"""
import sys, os, json, time, urllib.request, fitz

API_BASE = "https://openapi.biji.com"

def load_getnote_credentials():
    """从 ~/.openclaw/openclaw.json 读取 GetNotes 凭证"""
    cfg_path = os.path.expanduser("~/.openclaw/openclaw.json")
    with open(cfg_path) as f:
        cfg = json.load(f)
    getnote = cfg.get("skills", {}).get("entries", {}).get("getnote", {})
    api_key = getnote.get("apiKey")
    client_id = getnote.get("env", {}).get("GETNOTE_CLIENT_ID")
    if not api_key or not client_id:
        raise ValueError("GetNotes 凭证未配置：请在 ~/.openclaw/openclaw.json 的 skills.entries.getnote 中配置 apiKey 和 GETNOTE_CLIENT_ID")
    return api_key, client_id

def pdf_to_images(pdf_path, output_dir, zoom=2.0):
    os.makedirs(output_dir, exist_ok=True)
    doc = fitz.open(pdf_path)
    mat = fitz.Matrix(zoom, zoom)
    paths = []
    for i in range(len(doc)):
        page = doc[i]
        pix = page.get_pixmap(matrix=mat)
        out = f"{output_dir}/page_{i+1:02d}.png"
        pix.save(out)
        paths.append(out)
        print(f"  [{i+1}/{len(doc)}] {os.path.getsize(out)//1024}KB")
    doc.close()
    print(f"PDF转图完成: {len(paths)}页 -> {output_dir}")
    return paths

def get_upload_token(api_key, client_id):
    req = urllib.request.Request(
        f"{API_BASE}/open/api/v1/resource/image/upload_token?mime_type=png&count=1",
        headers={"Authorization": f"Bearer {api_key}", "X-Client-ID": client_id}
    )
    with urllib.request.urlopen(req) as r:
        return json.loads(r.read())

def upload_to_oss(page_path, token_data):
    import subprocess
    d = token_data["data"]
    cmd = [
        "curl", "-s", "-X", "POST", d["host"],
        "-F", f"key={d['object_key']}",
        "-F", f"OSSAccessKeyId={d['accessid']}",
        "-F", f"policy={d['policy']}",
        "-F", f"signature={d['signature']}",
        "-F", f"callback={d['callback']}",
        "-F", f"Content-Type=image/png",
        "-F", f"file=@{page_path}"
    ]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        raise Exception(f"OSS upload failed: {r.stderr[:200]}")
    return d["access_url"]

def create_plain_text_note(api_key, client_id, title, content, tags):
    payload = json.dumps({
        "note_type": "plain_text",
        "title": title,
        "content": content,
        "tags": tags
    }).encode()
    req = urllib.request.Request(
        f"{API_BASE}/open/api/v1/resource/note/save",
        data=payload,
        headers={
            "Authorization": f"Bearer {api_key}",
            "X-Client-ID": client_id,
            "Content-Type": "application/json"
        },
        method="POST"
    )
    with urllib.request.urlopen(req) as r:
        result = json.loads(r.read())
    if not result.get("success"):
        raise Exception(f"创建笔记失败: {result['error']}")
    return result["data"]["id"]

def add_to_knowledge(api_key, client_id, topic_id, note_id):
    payload = json.dumps({"topic_id": topic_id, "note_ids": [note_id]}).encode()
    req = urllib.request.Request(
        f"{API_BASE}/open/api/v1/resource/knowledge/note/batch-add",
        data=payload,
        headers={
            "Authorization": f"Bearer {api_key}",
            "X-Client-ID": client_id,
            "Content-Type": "application/json"
        },
        method="POST"
    )
    with urllib.request.urlopen(req) as r:
        return json.loads(r.read())

def main():
    if len(sys.argv) < 2:
        print("用法: python3 run_pdf_to_getnote.py <pdf_path> [topic_id] [title]")
        print("  topic_id: 可选，知识库 ID（如 EJlejByn）")
        print("  title: 可选，自定义笔记标题")
        sys.exit(1)

    pdf_path = sys.argv[1]
    topic_id = sys.argv[2] if len(sys.argv) > 2 else None
    custom_title = sys.argv[3] if len(sys.argv) > 3 else None

    # 凭证从配置文件读取
    api_key, client_id = load_getnote_credentials()
    print(f"✅ 凭证加载成功")

    pdf_name = os.path.splitext(os.path.basename(pdf_path))[0]
    title = custom_title or f"{pdf_name} - 完整摘要版"
    output_dir = f"/tmp/pdf_pages/{pdf_name}"

    print(f"📄 处理文件: {pdf_path}")

    # Step 1: PDF -> PNG
    print("\n[1/5] PDF -> PNG 转换...")
    page_paths = pdf_to_images(pdf_path, output_dir)

    # Step 2: 上传所有页
    print("\n[2/5] 上传图片到 OSS...")
    page_urls = []
    for i, page_path in enumerate(page_paths):
        for attempt in range(3):
            try:
                token_data = get_upload_token(api_key, client_id)
                if not token_data.get("success"):
                    raise Exception(token_data["error"]["message"])
                access_url = upload_to_oss(page_path, token_data)
                page_urls.append({"page": i+1, "access_url": access_url})
                print(f"  [{i+1}/{len(page_paths)}] ✅")
                break
            except Exception as e:
                if attempt < 2:
                    time.sleep(2)
                else:
                    raise
        time.sleep(0.3)

    with open(f"/tmp/{pdf_name}_urls.json", "w") as f:
        json.dump(page_urls, f)

    # Step 3: 构建内容（AI 摘要由调用方在外部生成，此处用模板占位）
    print("\n[3/5] 构建笔记内容...")
    ai_summary = f"""## 📄 文档信息
- **文件名：** {pdf_name}
- **总页数：** {len(page_urls)}页

## 📝 内容摘要
[请替换为AI生成的摘要内容]

## 💡 关键洞察
[请替换为AI生成的关键洞察]

---
*注：PDF原件图片见下方*
"""

    content = ai_summary + "\n\n## 📑 PDF 原件\n\n"
    for item in page_urls:
        content += f"### 第{item['page']}页\n![]({item['access_url']})\n\n"

    # Step 4: 创建笔记
    print("\n[4/5] 创建 GetNotes 笔记...")
    note_id = create_plain_text_note(api_key, client_id, title, content, ["PDF导入", "蓝莓自动"])
    print(f"  ✅ 笔记创建成功: {note_id}")

    # Step 5: 加入知识库
    if topic_id:
        print(f"\n[5/5] 加入知识库 {topic_id}...")
        result = add_to_knowledge(api_key, client_id, topic_id, note_id)
        if result.get("success"):
            print(f"  ✅ 已加入知识库")
        else:
            print(f"  ⚠️ 加入知识库失败: {result['error']}")
    else:
        print("\n[5/5] 未指定知识库，跳过")

    print(f"\n✅ 全部完成！笔记ID: {note_id}")

if __name__ == "__main__":
    main()
