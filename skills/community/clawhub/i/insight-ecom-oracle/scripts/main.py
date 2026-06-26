import requests
import json
import uuid

LAF_URL = "https://q3me0awfv7.sealosgzg.site/insight-ecom-gateway"
PAYMENT_URL = "https://afdian.com/order/create?plan_id=c27d1baa33c911f1a45652540025c377&product_type=0&remark=&affiliate_code="

# 多维度召回关键词组合
QUERY_VARIATIONS = [
    "",           # 原始词
    "材质",        # +材质
    "场景",        # +场景
    "风格",        # +风格
    "主图",        # +主图
    "详情页",      # +详情页
    "短视频",      # +短视频
    "商业摄影",    # +商业摄影
]

def search_once(query, user_id):
    """单次搜索调用"""
    payload = {"action": "search", "query": query, "user_id": user_id}
    try:
        response = requests.post(LAF_URL, json=payload, timeout=10)
        return response.json()
    except Exception:
        return None

def extract_prompts(data):
    """
    从 data 中提取单个或多个提示词。
    data 可以是字符串（API直接返回内容）或列表（API返回多条记录）。
    """
    prompts = []

    # data 是列表（多条记录）
    if isinstance(data, list):
        for item in data:
            if isinstance(item, dict) and 'content' in item:
                content = item['content'] or ''
                if len(content) > 200 and ('Role' in content or '# Role' in content):
                    prompts.append(content)
            elif isinstance(item, str):
                if len(item) > 200 and 'Role' in item:
                    prompts.append(item)
        return prompts

    # data 是字符串
    if not data or not isinstance(data, str):
        return []

    # 尝试按横向分隔线分割
    splits = data.split('---')
    if len(splits) > 1:
        prompts = [p.strip() for p in splits if p.strip() and len(p.strip()) > 200]
    else:
        # 单块内容，按 Role: 分割
        role_splits = data.split('Role:')
        if len(role_splits) > 2:
            for part in role_splits[1:]:
                full = ('Role:' + part).strip()
                if len(full) > 200:
                    prompts.append(full)
        else:
            prompts = [data.strip()] if len(data.strip()) > 200 else []

    # 过滤：必须包含 Role 关键字，长度 > 200
    prompts = [p for p in prompts if ('Role' in p or '# Role' in p) and len(p) > 200]

    return prompts

def deduplicate(prompts, max_count=5):
    """基于 Role 行和前100字符做去重，返回最多 max_count 条"""
    seen = set()
    unique = []
    for p in prompts:
        # 用 Role 行 + 前80字符作为去重 key
        lines = p.split('\n')
        role_line = next((l for l in lines if l.startswith('Role:')), lines[0][:80])
        key = role_line[:80].strip()
        if key not in seen:
            seen.add(key)
            unique.append(p)
        if len(unique) >= max_count:
            break
    return unique

def multi_recall(query, user_id, max_results=5):
    """
    多维度召回：
    1. 原始词
    2. 原始词+材质/场景/风格/主图/详情页/短视频/商业摄影 等变体
    3. 对每条结果做分割、去重
    4. 最多返回 max_results 条
    5. 每条返回 {title, content, category} 完整对象
    """
    all_items = []

    # 构建召回变体
    variations = [query]
    for suffix in QUERY_VARIATIONS:
        if suffix:
            variations.append(f"{query}{suffix}")
            variations.append(f"{query} {suffix}")

    # 去重保持顺序
    variations = list(dict.fromkeys(variations))

    seen_ids = set()
    for q in variations:
        if len(all_items) >= max_results:
            break
        res = search_once(q, user_id)
        if not res:
            continue
        status = res.get("status") or res.get("ec")
        if status != "success":
            continue
        raw_data = res.get("data", "")

        # data 是列表（API返回多条记录）
        if isinstance(raw_data, list):
            for item in raw_data:
                if not isinstance(item, dict):
                    continue
                title = item.get('title', '')
                content = item.get('content', '')
                category = item.get('category', '')
                if not content or len(content) < 100:
                    continue
                pid = title[:80].strip()
                if pid and pid not in seen_ids:
                    seen_ids.add(pid)
                    all_items.append({'title': title, 'content': content, 'category': category})
                if len(all_items) >= max_results:
                    break
            continue

        # data 是字符串（单条内容）
        if isinstance(raw_data, str):
            if "未找到" in raw_data or "尚未收录" in raw_data:
                continue
            prompts = extract_prompts(raw_data)
            for p in prompts:
                role_line = next((l for l in p.split('\n') if l.startswith('Role:')), "")
                pid = role_line[:100].strip()
                if pid and pid not in seen_ids:
                    seen_ids.add(pid)
                    all_items.append({'title': pid, 'content': p, 'category': ''})
                if len(all_items) >= max_results:
                    break

    return all_items

def main(params):
    query = params.get("query", "")
    user_id = params.get("user_id", "")

    # ==================== 步骤1：生成/验证 user_id ====================
    if not user_id or user_id == "guest":
        new_id = "user_" + str(uuid.uuid4())[:8]
        return {
            "status": "need_register",
            "is_registered": False,
            "is_paid": False,
            "is_expired": False,
            "user_id": new_id,
            "payment_url": PAYMENT_URL,
            "payment_status": "未支付",
            "message": f"""📋 请先注册【灵犀神谕】账号

━━━━━━━━━━━━━━━
您的账号信息
━━━━━━━━━━━━━━━
👤 用户ID：{new_id}
📊 状态：未注册
💰 支付状态：未支付
━━━━━━━━━━━━━━━

请按以下步骤完成注册：

1️⃣ 点击下方链接支付（199元/年）
   → {PAYMENT_URL}

2️⃣ 支付时【留言/备注】栏填写：
   {new_id}

3️⃣ 支付成功后，回复：
   激活 {new_id}

—— 灵犀出品，必属精品"""
        }

    # ==================== 步骤2：多维度召回 ====================
    try:
        prompts = multi_recall(query, user_id, max_results=5)
    except Exception as e:
        prompts = []

    # ==================== 步骤3：检查支付状态 ====================
    check_payload = {"action": "search", "query": query, "user_id": user_id}
    try:
        check_response = requests.post(LAF_URL, json=check_payload, timeout=10)
        check_data = check_response.json()
        check_status = check_data.get("status") or check_data.get("ec")
    except Exception:
        check_status = None

    # ==================== 步骤4：分发结果 ====================
    if check_status == "success":
        account_msg = f"""━━━━━━━━━━━━━━━
您的账号信息
━━━━━━━━━━━━━━━
👤 用户ID：{user_id}
📊 状态：已注册 ✅
💰 支付状态：已支付 ✅
━━━━━━━━━━━━━━━"""

        if prompts:
            header = f"✅ 权限验证通过，共匹配到 {len(prompts)} 条提示词：\n\n{account_msg}\n\n"
            body_lines = []
            for i, item in enumerate(prompts, 1):
                # item = {title, content, category}
                title = item.get('title', '') if isinstance(item, dict) else ''
                content = item.get('content', item) if isinstance(item, dict) else item
                category = item.get('category', '') if isinstance(item, dict) else ''
                cat_label = f"📂 {category} |" if category else ""
                body_lines.append(f"**【{i}】** {cat_label} **{title}**\n")
                # Full master_prompt in markdown code block, fully visible
                body_lines.append(f"```\n{content}\n```\n")
                body_lines.append("")
            body = "\n".join(body_lines)
            footer = "\n—— 灵犀出品，必属精品"
            full_message = header + body + footer

            # Split message into chunks of ≤3800 chars to respect Telegram limit
            # Strategy: accumulate prompts one by one until adding the next would exceed limit
            TELEGRAM_LIMIT = 3800
            header_only = header  # account header part
            footer_only = footer  # "—— 灵犀出品，必属精品"

            chunks = []
            current_block = ""

            for i, item in enumerate(prompts):
                title = item.get('title', '') if isinstance(item, dict) else ''
                content = item.get('content', item) if isinstance(item, dict) else item
                category = item.get('category', '') if isinstance(item, dict) else ''
                cat_label = f"📂 {category} |" if category else ""
                prompt_block = f"**【{i+1}】** {cat_label} **{title}**\n\n```\n{content}\n```\n\n"

                if not current_block:
                    # First block: always include header
                    test = header_only + prompt_block
                else:
                    test = current_block + prompt_block

                if len(test) > TELEGRAM_LIMIT:
                    # Finalize current chunk with footer
                    if current_block:
                        chunks.append(current_block + footer_only)
                    # Start new chunk with header + this prompt
                    current_block = header_only + prompt_block
                else:
                    current_block = test

            # Don't forget the last block
            if current_block:
                chunks.append(current_block + footer_only)

            return {
                "status": "success",
                "is_registered": True,
                "is_paid": True,
                "is_expired": False,
                "user_id": user_id,
                "payment_url": PAYMENT_URL,
                "payment_status": "已支付",
                "data": prompts,
                "message": chunks[0] if chunks else full_message,
                "chunks": chunks
            }
        else:
            # 支付用户但无结果
            raw = check_data.get("data", "")
            if "未找到" in raw or "尚未收录" in raw:
                msg = f"✅ 权限验证通过\n\n{account_msg}\n\n🔍 目前神谕库尚未收录「{query}」相关的商业模型，建议尝试更通用的关键词或联系魔童进行定制。\n\n—— 灵犀出品，必属精品"
            else:
                # API成功但无可用结果，转为单条raw返回
                prompts_raw = extract_prompts(raw)
                if prompts_raw:
                    return {
                        "status": "success",
                        "is_registered": True,
                        "is_paid": True,
                        "is_expired": False,
                        "user_id": user_id,
                        "payment_url": PAYMENT_URL,
                        "payment_status": "已支付",
                        "data": prompts_raw,
                        "message": f"✅ 权限验证通过，以下是您的搜索结果：\n\n{account_msg}\n\n{prompts_raw[0]}\n\n—— 灵犀出品，必属精品"
                    }
                msg = f"✅ 权限验证通过\n\n{account_msg}\n\n🔍 未找到匹配的提示词，请尝试其他关键词。\n\n—— 灵犀出品，必属精品"

            return {
                "status": "success",
                "is_registered": True,
                "is_paid": True,
                "is_expired": False,
                "user_id": user_id,
                "payment_url": PAYMENT_URL,
                "payment_status": "已支付",
                "data": [],
                "message": msg
            }

    elif check_status == "expired":
        return {
            "status": "expired",
            "is_registered": True,
            "is_paid": True,
            "is_expired": True,
            "user_id": user_id,
            "payment_url": PAYMENT_URL,
            "payment_status": "已过期",
            "message": f"""🔄 您的权限已过期

━━━━━━━━━━━━━━━
您的账号信息
━━━━━━━━━━━━━━━
👤 用户ID：{user_id}
📊 状态：已注册（权限过期）
💰 支付状态：已过期
━━━━━━━━━━━━━━━

请按以下步骤续费：

1️⃣ 点击续费链接（199元/年）
   → {PAYMENT_URL}

2️⃣ 支付时【留言】填写：
   {user_id}

3️⃣ 支付成功后回复：
   激活 {user_id}

—— 灵犀出品，必属精品"""
        }

    elif check_status in ("need_pay", "need_pay未支付"):
        return {
            "status": "need_pay",
            "is_registered": True,
            "is_paid": False,
            "is_expired": False,
            "user_id": user_id,
            "payment_url": PAYMENT_URL,
            "payment_status": "未支付",
            "message": f"""💳 请完成支付以激活权限

━━━━━━━━━━━━━━━
您的账号信息
━━━━━━━━━━━━━━━
👤 用户ID：{user_id}
📊 状态：已注册（待激活）
💰 支付状态：未支付
━━━━━━━━━━━━━━━

请复制上方用户ID，粘贴到爱发电支付留言框：

1️⃣ 点击支付链接（199元/年）
   → {PAYMENT_URL}

2️⃣ 留言内容：
   {user_id}

3️⃣ 支付后回复本消息，24小时内开通

—— 灵犀出品，必属精品"""
        }

    else:
        return {
            "status": "error",
            "is_registered": False,
            "is_paid": False,
            "is_expired": False,
            "user_id": user_id,
            "payment_url": PAYMENT_URL,
            "payment_status": "未知",
            "message": check_data.get("message") if check_data else "⏱️ 连接超时，请检查网络后重试"
        }
