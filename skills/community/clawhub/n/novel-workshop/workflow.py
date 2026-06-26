#!/usr/bin/env python3
"""
🎲 命题小说多模型创作工坊 v4
用法: python3 workflow.py "写作prompt" ["文档标题"]

流程: MiMo写初稿 → Gemini+Claude三路并行审阅 → Gemini改稿 → 本地存档 + 飞书文档完整写入
全程自动，飞书群聊实时进度推送。

配置: 自动从 ~/.openclaw/openclaw.json 读取 API Key 和飞书配置。
      可用环境变量覆盖: OPENROUTER_API_KEY, FEISHU_CHAT_ID, FEISHU_FOLDER_TOKEN, FEISHU_OWNER_OPEN_ID
"""

import sys, json, os, time, requests, concurrent.futures, re

# ============ 配置 ============
OPENROUTER_API_KEY = None
OPENROUTER_BASE = "https://openrouter.ai/api/v1"

MODELS = {
    "write": "xiaomi/mimo-v2-flash",
    "review_logic": "google/gemini-2.5-pro",
    "review_literary": "google/gemini-2.5-pro",
    "review_sharp": "anthropic/claude-opus-4.6",
    "revise": "google/gemini-2.5-pro",
}

FALLBACK_MODELS = {
    "xiaomi/mimo-v2-flash": "google/gemini-2.5-pro",
    "google/gemini-2.5-pro": "anthropic/claude-opus-4.6",
    "anthropic/claude-opus-4.6": "google/gemini-2.5-pro",
}

# 飞书配置
FEISHU_APP_ID = None
FEISHU_APP_SECRET = None
FEISHU_CHAT_ID = os.environ.get("FEISHU_CHAT_ID", "oc_4680833fd5ab374f3e26c90739ef6946")
FEISHU_FOLDER_TOKEN = os.environ.get("FEISHU_FOLDER_TOKEN", "U01TfC1RdlwEBzdHJCIcXwCQnVg")
FEISHU_OWNER_OPEN_ID = os.environ.get("FEISHU_OWNER_OPEN_ID", "ou_5b28826e6f7c9e54fcb49ba0b7e0b944")
FEISHU_TOKEN = None

# ============ 初始化 ============

def load_config():
    global OPENROUTER_API_KEY, FEISHU_APP_ID, FEISHU_APP_SECRET
    try:
        cfg = json.load(open(os.path.expanduser("~/.openclaw/openclaw.json")))
        providers = cfg.get("models", {}).get("providers", {})
        OPENROUTER_API_KEY = providers.get("openrouter", {}).get("apiKey", "")
        feishu = cfg.get("channels", {}).get("feishu", {})
        FEISHU_APP_ID = feishu.get("appId", "")
        FEISHU_APP_SECRET = feishu.get("appSecret", "")
    except Exception as e:
        print(f"⚠️ 读取配置失败: {e}")
    if not OPENROUTER_API_KEY:
        OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY", "")
    if not OPENROUTER_API_KEY:
        print("❌ 找不到 OpenRouter API Key")
        sys.exit(1)

def get_feishu_token():
    global FEISHU_TOKEN
    if not FEISHU_APP_ID or not FEISHU_APP_SECRET:
        return None
    try:
        resp = requests.post("https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal",
            json={"app_id": FEISHU_APP_ID, "app_secret": FEISHU_APP_SECRET}, timeout=10).json()
        FEISHU_TOKEN = resp.get("tenant_access_token", "")
        return FEISHU_TOKEN
    except:
        return None

# ============ 飞书消息推送 ============

def feishu_send(msg):
    """发送消息到飞书群聊"""
    if not FEISHU_TOKEN:
        print(f"  [飞书] (无token，跳过) {msg}")
        return
    try:
        resp = requests.post(
            f"https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=chat_id",
            headers={"Authorization": f"Bearer {FEISHU_TOKEN}", "Content-Type": "application/json"},
            json={
                "receive_id": FEISHU_CHAT_ID,
                "msg_type": "text",
                "content": json.dumps({"text": msg})
            },
            timeout=10
        ).json()
        if resp.get("code") == 0:
            print(f"  [飞书] ✅ 已发送: {msg[:50]}...")
        else:
            print(f"  [飞书] ⚠️ 发送失败: {resp.get('msg', 'unknown')}")
    except Exception as e:
        print(f"  [飞书] ⚠️ 发送异常: {e}")

# ============ OpenRouter API ============

def chat(model, messages, timeout=180):
    resp = requests.post(
        f"{OPENROUTER_BASE}/chat/completions",
        headers={
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://openclaw.ai"
        },
        json={"model": model, "messages": messages, "max_tokens": 16384},
        timeout=timeout
    )
    data = resp.json()
    if "error" in data:
        raise Exception(f"API error: {data['error']}")
    return data["choices"][0]["message"]["content"]

def chat_with_fallback(model, messages, role_name, timeout=180):
    try:
        print(f"  📡 {role_name}: 使用 {model}...")
        result = chat(model, messages, timeout)
        print(f"  ✅ {role_name}: 完成 ({len(result)} chars)")
        return result
    except Exception as e:
        print(f"  ⚠️ {role_name}: {model} 失败 ({e}), 尝试备选...")
        fallback = FALLBACK_MODELS.get(model)
        if fallback:
            try:
                result = chat(fallback, messages, timeout)
                print(f"  ✅ {role_name}: 备选 {fallback} 完成")
                return result
            except Exception as e2:
                print(f"  ❌ {role_name}: 备选也失败 ({e2})")
                return f"[审阅失败: {e2}]"
        return f"[审阅失败: {e}]"

def extract_score(text):
    matches = re.findall(r'(\d+(?:\.\d+)?)\s*/\s*10', text)
    return matches[0] if matches else "?"

# ============ 主流程 ============

def main():
    if len(sys.argv) < 2:
        print("用法: python3 workflow.py \"写作prompt\" [\"文档标题\"]")
        sys.exit(1)

    write_prompt = sys.argv[1]
    doc_title = sys.argv[2] if len(sys.argv) > 2 else "命题创作"

    load_config()
    get_feishu_token()

    start_time = time.time()

    # Step 0: 通知
    feishu_send(f"[░░░░░] 0/5 收到命题！工作流启动中 🎲")

    # ---- Step 1: 写初稿 ----
    print(f"\n{'='*50}\n  [█░░░░] 1/5 写初稿\n{'='*50}")

    draft = chat_with_fallback(
        MODELS["write"],
        [{"role": "user", "content": f"{write_prompt}\n\n直接输出正文（含标题），不需要任何解释或前言。"}],
        "初稿写作",
        timeout=240
    )

    # 提取标题（第一行去掉#号）
    first_line = draft.strip().split('\n')[0].strip().lstrip('#').strip()
    story_title = first_line if first_line else doc_title

    feishu_send(f"[█░░░░] 1/5 初稿完成 ✅《{story_title}》({len(draft)}字) 三路审阅启动中…")

    # ---- Step 2: 三路并行审阅 ----
    print(f"\n{'='*50}\n  [██░░░] 2/5 三路并行审阅\n{'='*50}")

    review_tasks = {
        "logic": {
            "model": MODELS["review_logic"],
            "name": "逻辑检阅",
            "prompt": f"你是严谨的文学逻辑审阅专家。审阅以下小说，从以下维度分析：\n1. 情节自洽性\n2. 时间线\n3. 因果关系\n4. 世界观矛盾\n\n评分1-10，详细说明。用中文。\n\n---以下是小说全文---\n\n{draft}"
        },
        "literary": {
            "model": MODELS["review_literary"],
            "name": "文学性分析",
            "prompt": f"你是资深文学评论家。审阅以下小说，从以下维度分析：\n1. 语言风格\n2. 意象构建\n3. 叙事手法\n4. 主题深度\n\n评分1-10，详细说明。用中文。\n\n---以下是小说全文---\n\n{draft}"
        },
        "sharp": {
            "model": MODELS["review_sharp"],
            "name": "锐评",
            "prompt": f"你是毒舌但有料的文学批评家，风格尖锐、一针见血。对以下小说进行锐评：\n1. 用最犀利的语言指出最大的问题\n2. 不要客气，不要留面子\n3. 给出3个核心改动建议（具体、可操作）\n\n用中文。\n\n---以下是小说全文---\n\n{draft}"
        }
    }

    reviews = {}
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        futures = {}
        for key, task in review_tasks.items():
            future = executor.submit(
                chat_with_fallback, task["model"],
                [{"role": "user", "content": task["prompt"]}],
                task["name"], 180
            )
            futures[future] = key

        for future in concurrent.futures.as_completed(futures):
            key = futures[future]
            reviews[key] = future.result()

    logic_score = extract_score(reviews.get("logic", ""))
    literary_score = extract_score(reviews.get("literary", ""))

    feishu_send(f"[██░░░] 2/5 审阅完成 ✅ 逻辑 {logic_score}/10 | 文学 {literary_score}/10 | 改稿启动中…")

    # ---- Step 3: 改稿 ----
    print(f"\n{'='*50}\n  [███░░] 3/5 改稿\n{'='*50}")

    revision_prompt = f"""你是一位优秀的作家。以下是一篇小说初稿和三份审阅意见。请根据审阅意见全面修改小说，输出完整新版本。

修改要求：
1. 认真采纳锐评的建议，大胆改动
2. 保留原作优秀的部分
3. 让角色更真实立体
4. 结尾不要鸡汤金句，留白更好

直接输出修改后的完整小说（含标题），不需要解释修改了什么。

## 初稿
{draft}

## 审阅A：逻辑检阅
{reviews.get('logic', '[未完成]')}

## 审阅B：文学性分析
{reviews.get('literary', '[未完成]')}

## 审阅C：锐评
{reviews.get('sharp', '[未完成]')}"""

    revision = chat_with_fallback(
        MODELS["revise"],
        [{"role": "user", "content": revision_prompt}],
        "改稿",
        timeout=300
    )

    feishu_send(f"[███░░] 3/5 改稿完成 ✅ 保存中…")

    # ---- Step 4: 本地存档 ----
    print(f"\n{'='*50}\n  [████░] 4/5 存档\n{'='*50}")

    local_path = os.path.expanduser(f"~/.openclaw/workspace/novels/{doc_title}.md")
    os.makedirs(os.path.dirname(local_path), exist_ok=True)
    with open(local_path, "w") as f:
        f.write(f"# 🎲 命题创作《{doc_title}》— 多模型创作工坊\n\n")
        f.write(f"**日期**：{time.strftime('%Y-%m-%d')}\n")
        f.write(f"**评分**：逻辑 {logic_score}/10 | 文学 {literary_score}/10\n\n---\n\n")
        f.write(f"## Part 1：初稿\n\n{draft}\n\n---\n\n")
        f.write(f"## Part 2：三路审阅\n\n")
        f.write(f"### 逻辑检阅\n\n{reviews.get('logic', '[未完成]')}\n\n")
        f.write(f"### 文学性分析\n\n{reviews.get('literary', '[未完成]')}\n\n")
        f.write(f"### 锐评\n\n{reviews.get('sharp', '[未完成]')}\n\n---\n\n")
        f.write(f"## Part 3：终稿\n\n{revision}\n")
    print(f"  💾 本地保存: {local_path}")

    # 飞书文档创建 + 写入完整内容
    doc_id = ""
    doc_url = ""
    if FEISHU_TOKEN:
        doc_id = create_feishu_doc(f"🎲 命题创作《{doc_title}》— 多模型创作工坊", FEISHU_TOKEN)
        if doc_id:
            doc_url = f"https://feishu.cn/docx/{doc_id}"
            print(f"  📄 飞书文档已创建: {doc_url}")
            feishu_send(f"[████░] 4/5 存档完成 ✅ 正在写入飞书文档…")
            # 读取本地完整 md 文件，写入飞书文档（不省略任何内容！）
            write_feishu_doc_content(doc_id, local_path, FEISHU_TOKEN)
        else:
            feishu_send(f"[████░] 4/5 存档完成 ✅ 飞书文档创建失败，仅本地保存")
    else:
        feishu_send(f"[████░] 4/5 存档完成 ✅ 仅本地保存")

    # ---- Step 5: 完成通知 ----
    elapsed = time.time() - start_time

    if doc_url:
        final_msg = f"[█████] 5/5 全部完成！🎲\n\n⏱️ 总耗时: {elapsed:.0f} 秒\n📊 评分: 逻辑 {logic_score}/10 | 文学 {literary_score}/10\n📄 飞书文档: {doc_url}"
    else:
        final_msg = f"[█████] 5/5 写作完成！🎲\n\n⏱️ 总耗时: {elapsed:.0f} 秒\n📊 评分: 逻辑 {logic_score}/10 | 文学 {literary_score}/10\n💾 已保存到本地"
    feishu_send(final_msg)

    print(f"\n{'='*50}")
    print(f"  🎲 完成！总耗时: {elapsed:.0f} 秒")
    print(f"{'='*50}")

    # JSON 摘要
    summary = {
        "story_title": story_title,
        "doc_title": doc_title,
        "doc_url": doc_url,
        "doc_id": doc_id,
        "local_path": local_path,
        "scores": {"logic": logic_score, "literary": literary_score},
        "elapsed_seconds": round(elapsed),
        "status": "success"
    }
    print(f"\n__SUMMARY__:{json.dumps(summary, ensure_ascii=False)}")


def write_feishu_doc_content(doc_id, local_path, token):
    """读取本地 md 文件完整内容，通过飞书 API 分段写入文档。
    使用 openclaw CLI 的 feishu_doc write 工具，确保不省略任何内容。"""
    import subprocess
    try:
        with open(local_path, "r") as f:
            full_content = f.read()

        if not full_content.strip():
            print("  ⚠️ 本地文件为空，跳过写入")
            return

        # 使用 openclaw tool 调用 feishu_doc write
        # 先尝试直接用飞书 API 写入纯文本 block
        # 飞书文档 API: 创建文本块
        headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

        # 将内容按段落拆分为 block
        lines = full_content.split('\n')
        blocks = []
        current_text = []

        for line in lines:
            stripped = line.strip()
            if stripped.startswith('# '):
                # 跳过一级标题（已经是文档标题）
                continue
            elif stripped.startswith('## '):
                if current_text:
                    blocks.append({"type": "text", "content": '\n'.join(current_text)})
                    current_text = []
                blocks.append({"type": "heading2", "content": stripped[3:]})
            elif stripped.startswith('### '):
                if current_text:
                    blocks.append({"type": "text", "content": '\n'.join(current_text)})
                    current_text = []
                blocks.append({"type": "heading3", "content": stripped[4:]})
            elif stripped == '---':
                if current_text:
                    blocks.append({"type": "text", "content": '\n'.join(current_text)})
                    current_text = []
                blocks.append({"type": "divider", "content": ""})
            else:
                current_text.append(line)

        if current_text:
            blocks.append({"type": "text", "content": '\n'.join(current_text)})

        # 使用飞书 Descendant API 批量创建 block
        doc_block_id = doc_id  # 根 block = 文档 ID

        created = 0
        for block in blocks:
            try:
                if block["type"] == "divider":
                    block_data = {
                        "block_type": 22,  # divider
                        "divider": {}
                    }
                elif block["type"] == "heading2":
                    block_data = {
                        "block_type": 4,  # heading2
                        "heading2": {
                            "elements": [{"text_run": {"content": block["content"]}}],
                            "style": {}
                        }
                    }
                elif block["type"] == "heading3":
                    block_data = {
                        "block_type": 5,  # heading3
                        "heading3": {
                            "elements": [{"text_run": {"content": block["content"]}}],
                            "style": {}
                        }
                    }
                else:
                    # 文本块，每段不超过 500 字符，超过则拆分
                    text = block["content"].strip()
                    if not text:
                        continue
                    # 按段落拆分
                    paragraphs = text.split('\n\n')
                    for para in paragraphs:
                        para = para.strip()
                        if not para:
                            continue
                        # 飞书单个文本块有字符限制，按行再拆
                        sub_lines = para.split('\n')
                        for sub_line in sub_lines:
                            sub_line_stripped = sub_line.strip()
                            if not sub_line_stripped:
                                continue
                            para_data = {
                                "block_type": 2,  # text
                                "text": {
                                    "elements": [{"text_run": {"content": sub_line_stripped}}],
                                    "style": {}
                                }
                            }
                            resp = requests.post(
                                f"https://open.feishu.cn/open-apis/docx/v1/documents/{doc_id}/blocks/{doc_block_id}/children",
                                headers=headers,
                                json={"children": [para_data], "index": -1},
                                timeout=15
                            ).json()
                            if resp.get("code") == 0:
                                created += 1
                            else:
                                print(f"  ⚠️ 写入失败: {resp.get('msg', '')[:80]}")
                    continue

                resp = requests.post(
                    f"https://open.feishu.cn/open-apis/docx/v1/documents/{doc_id}/blocks/{doc_block_id}/children",
                    headers=headers,
                    json={"children": [block_data], "index": -1},
                    timeout=15
                ).json()
                if resp.get("code") == 0:
                    created += 1
                else:
                    print(f"  ⚠️ 写入失败: {resp.get('msg', '')[:80]}")
            except Exception as e:
                print(f"  ⚠️ 写入异常: {e}")

        print(f"  📝 飞书文档写入完成: {created} 个文本块")

    except Exception as e:
        print(f"  ❌ 飞书文档写入失败: {e}")


def create_feishu_doc(title, token):
    try:
        resp = requests.post(
            "https://open.feishu.cn/open-apis/docx/v1/documents",
            headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
            json={"title": title, "folder_token": FEISHU_FOLDER_TOKEN},
            timeout=15
        ).json()
        doc_id = resp.get("data", {}).get("document", {}).get("document_id", "")
        if doc_id:
            try:
                requests.post(
                    f"https://open.feishu.cn/open-apis/drive/v1/permissions/{doc_id}/members?type=docx&need_notification=false",
                    headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
                    json={"member_type": "openid", "member_id": FEISHU_OWNER_OPEN_ID, "perm": "full_access"},
                    timeout=10
                )
            except:
                pass
        return doc_id
    except:
        return ""


if __name__ == "__main__":
    main()
