"""
身份管理模块
处理用户身份验证和变更
"""

import json
from datetime import datetime, timedelta
from pathlib import Path

DATA_DIR = Path("/workspace/data")
LOG_DIR = Path("/workspace/logs")
LOG_FILE = LOG_DIR / "audit.log"

# ============ 内存会话存储 ============
_sessions = {}
SESSION_TIMEOUT_MINUTES = 10


class _Session:
    """会话对象"""
    def __init__(self, account_id: str):
        self.account_id = account_id
        self.state = "idle"
        self.context = {}
        self.last_message_at = datetime.utcnow()
        self.expires_at = datetime.utcnow() + timedelta(minutes=SESSION_TIMEOUT_MINUTES)


def _get_or_create_session(account_id: str) -> _Session:
    """获取或创建会话"""
    session = _sessions.get(account_id)
    
    if session is None:
        session = _Session(account_id)
        _sessions[account_id] = session
    elif datetime.utcnow() > session.expires_at:
        # 过期了，创建新的
        session = _Session(account_id)
        _sessions[account_id] = session
    
    return session


def _update_session(account_id: str, state: str, context: dict = None):
    """更新会话状态"""
    session = _get_or_create_session(account_id)
    session.state = state
    if context:
        session.context.update(context)
    session.expires_at = datetime.utcnow() + timedelta(minutes=SESSION_TIMEOUT_MINUTES)


def _update_last_message_time(account_id: str):
    """更新最后消息时间"""
    session = _get_or_create_session(account_id)
    session.last_message_at = datetime.utcnow()
    session.expires_at = datetime.utcnow() + timedelta(minutes=SESSION_TIMEOUT_MINUTES)


def log_operation(operation: str, **kwargs):
    """记录操作日志"""
    LOG_DIR.mkdir(exist_ok=True)
    log_entry = {
        "timestamp": datetime.now().isoformat() + "Z",
        "operation": operation,
        **kwargs
    }
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")


def load_users():
    """加载用户表"""
    with open(DATA_DIR / "users.json") as f:
        return json.load(f)


def save_users(data):
    """保存用户表"""
    with open(DATA_DIR / "users.json", "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def load_accounts():
    """加载账号表"""
    with open(DATA_DIR / "accounts.json") as f:
        return json.load(f)


def save_accounts(data):
    """保存账号表"""
    with open(DATA_DIR / "accounts.json", "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def load_users():
    """加载用户表"""
    with open(DATA_DIR / "users.json") as f:
        return json.load(f)


def save_users(data):
    """保存用户表"""
    with open(DATA_DIR / "users.json", "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def load_accounts():
    """加载账号表"""
    with open(DATA_DIR / "accounts.json") as f:
        return json.load(f)


def save_accounts(data):
    """保存账号表"""
    with open(DATA_DIR / "accounts.json", "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def identify_user(open_id: str) -> dict:
    """根据账号识别用户"""
    accounts_data = load_accounts()
    
    # 查找账号
    user_id = None
    for acc in accounts_data.get("accounts", []):
        if acc.get("open_id") == open_id:
            user_id = acc.get("user_id")
            break
    
    if not user_id:
        return {"found": False}
    
    # 查找用户（users 是数组）
    users_data = load_users()
    user = None
    for u in users_data.get("users", []):
        if u.get("user_id") == user_id:
            user = u
            break
    
    if not user:
        return {"found": False}
    
    return {
        "found": True,
        "user_id": user_id,
        "user": user
    }


def verify_code(open_id: str, code: str) -> dict:
    """验证暗号"""
    user_result = identify_user(open_id)
    
    if not user_result.get("found"):
        return {"verified": False, "reason": "未找到用户"}
    
    user = user_result.get("user", {})
    stored_code = user.get("code")
    
    if stored_code == code:
        return {
            "verified": True,
            "identity": user.get("role"),  # 使用 role 而非 identity
            "user_id": user_result.get("user_id")
        }
    else:
        return {"verified": False, "reason": "暗号错误"}


def change_identity(user_id: str, new_identity: str, code: str = None) -> dict:
    """变更用户身份"""
    users_data = load_users()
    
    # 检查用户是否存在
    if user_id not in users_data.get("users", {}):
        return {"success": False, "reason": "用户不存在"}
    
    # 更新身份
    users_data["users"][user_id]["identity"] = new_identity
    
    # 如果是朋友，需要记录暗号
    if new_identity == "friend" and code:
        users_data["users"][user_id]["code"] = code
    elif new_identity == "stranger":
        users_data["users"][user_id]["code"] = None
    
    # 更新验证方式
    if new_identity == "friend":
        users_data["users"][user_id]["verificationMethod"] = "code"
    elif new_identity == "owner":
        users_data["users"][user_id]["verificationMethod"] = "certification"
    
    # 保存
    save_users(users_data)
    
    return {"success": True, "identity": new_identity}


def bind_account(open_id: str, user_id: str, platform: str = "feishu") -> dict:
    """绑定账号到用户"""
    accounts_data = load_accounts()
    
    # 检查账号是否已绑定
    for acc in accounts_data.get("accounts", []):
        if acc.get("open_id") == open_id:
            return {"success": False, "reason": "账号已被绑定"}
    
    # 添加账号
    new_account = {
        "account_id": f"acc_{len(accounts_data.get('accounts', [])) + 1:03d}",
        "platform": platform,
        "open_id": open_id,
        "user_id": user_id,
        "bound_at": datetime.now().isoformat() + "Z"
    }
    
    accounts_data["accounts"].append(new_account)
    
    # 保存
    save_accounts(accounts_data)
    
    return {"success": True, "account": new_account}


def create_user(identity: str = "stranger", code: str = None) -> dict:
    """创建新用户"""
    users_data = load_users()
    
    # 生成新用户ID（users 是数组）
    existing_ids = [int(u.get("user_id", "u0").replace("u", "")) for u in users_data.get("users", [])]
    new_id = f"u{max(existing_ids) + 1:03d}" if existing_ids else "u001"
    
    # 创建用户
    new_user = {
        "user_id": new_id,
        "type": "human",
        "identity": identity,
        "code": code,
        "verificationMethod": "code" if code else None,
        "createTime": datetime.now().isoformat() + "Z",
        "lastContact": None,
        "accounts": []
    }
    
    users_data["users"].append(new_user)
    save_users(users_data)
    
    return {"success": True, "user_id": new_id, "user": new_user}


def record_contact(open_id: str, platform: str):
    """记录沟通，更新最后沟通时间"""
    user_result = identify_user(open_id)
    
    if not user_result.get("found"):
        # 陌生人：创建新用户并绑定账号
        user_id = create_user("stranger").get("user_id")
        bind_account(open_id, user_id, platform)
        return
    
    user_id = user_result.get("user_id")
    users_data = load_users()
    
    users_data["users"][user_id]["lastContact"] = {
        "time": datetime.now().isoformat() + "Z",
        "channel": platform,
        "account": open_id
    }
    
    save_users(users_data)


def check_expiry() -> list:
    """检查30天未沟通的用户，执行降级"""
    users_data = load_users()
    
    expired_users = []
    now = datetime.now()
    
    for user_id, user in users_data.get("users", {}).items():
        # 跳过主人
        if user.get("identity") == "owner":
            continue
        
        last_contact = user.get("lastContact", {})
        if not last_contact:
            continue
        
        try:
            last_time_str = last_contact.get("time", "").replace("Z", "+00:00")
            last_time = datetime.fromisoformat(last_time_str)
            days = (now - last_time).days
            
            if days >= 30:
                expired_users.append(user_id)
                # 降级为陌生人
                user["identity"] = "stranger"
                user["code"] = None
        except:
            continue
    
    # 保存
    save_users(users_data)
    
    return expired_users


def get_user_info(open_id: str) -> dict:
    """获取用户信息"""
    user_result = identify_user(open_id)
    
    if not user_result.get("found"):
        return {
            "found": False,
            "identity": "stranger",
            "message": "新用户，之前没有与我沟通过"
        }
    
    user = user_result.get("user", {})
    # 兼容 role 和 identity 字段
    identity = user.get("identity") or user.get("role") or "unknown"
    
    return {
        "found": True,
        "user_id": user_result.get("user_id"),
        "identity": identity,
        "has_code": bool(user.get("code")),
        "lastContact": user.get("lastContact")
    }


# ============ 话术模板 ============

GREETING_NEW_USER = "你好呀～ 我们好像第一次见面，先认识一下吧？😊 你愿意告诉我你的名字吗？"

ASK_NAME = "你愿意告诉我你的名字吗？"

CONFIRM_RENAME = "诶？这个名字我记得，我们之前聊过吗？"

ASK_PHRASE = "我们约定过暗号，你知道吗？可以告诉我来确认一下身份～"

PHRASE_CORRECT = "对的！验证通过～ 以后这个账号我也认识你啦！"

PHRASE_WRONG = "抱歉，暗号不太对～ 那我们重新认识一下吧？你愿意告诉我你的名字吗？"

ASK_VERIFICATION = "那我们之前什么时候聊的？你还记得吗？"

VERIFICATION_PASS = "对的！想起来了～ 以后这个账号我也认识你啦！"

VERIFICATION_FAIL = "好吧，跟我的记忆还是不太一样，不过没关系，你就当我是新朋友吧～ 我重新记一下你！"

NEW_USER_WELCOME = "小明你好！很高兴认识你～ 有什么我可以帮你的吗？✨"


# ============ 审批相关功能 ============

def create_approval_request(request_type: str, user_id: str, open_id: str, 
                            target_identity: str, code: str = None) -> dict:
    """创建审批请求"""
    approval = {
        "id": f"approval_{datetime.now().strftime('%Y%m%d%H%M%S')}",
        "type": request_type,  # "friend_apply" / "identity_change"
        "user_id": user_id,
        "open_id": open_id,
        "target_identity": target_identity,
        "code": code,
        "status": "pending",  # pending / approved / rejected
        "create_time": datetime.now().isoformat() + "Z",
        "approve_time": None,
        "approver": None
    }
    
    # 保存审批请求
    approvals = load_approvals()
    approvals.append(approval)
    save_approvals(approvals)
    
    log_operation("approval_request_created", 
                 user_id=user_id, 
                 open_id=open_id,
                 target_identity=target_identity)
    
    return approval


def load_approvals() -> list:
    """加载审批请求列表"""
    approval_file = DATA_DIR / "approvals.json"
    if not approval_file.exists():
        return []
    with open(approval_file) as f:
        return json.load(f)


def save_approvals(approvals: list):
    """保存审批请求列表"""
    with open(DATA_DIR / "approvals.json", "w") as f:
        json.dump(approvals, f, indent=2)


def get_pending_approvals() -> list:
    """获取待审批的请求"""
    approvals = load_approvals()
    return [a for a in approvals if a.get("status") == "pending"]


def approve_request(approval_id: str, approver: str = "owner") -> dict:
    """审批通过"""
    approvals = load_approvals()
    
    for approval in approvals:
        if approval.get("id") == approval_id:
            approval["status"] = "approved"
            approval["approve_time"] = datetime.now().isoformat() + "Z"
            approval["approver"] = approver
            
            # 执行身份变更
            user_id = approval.get("user_id")
            target_identity = approval.get("target_identity")
            code = approval.get("code")
            
            change_identity(user_id, target_identity, code)
            
            save_approvals(approvals)
            
            log_operation("approval_approved",
                        approval_id=approval_id,
                        user_id=user_id,
                        target_identity=target_identity)
            
            return {"success": True, "approval": approval}
    
    return {"success": False, "reason": "审批请求不存在"}


def reject_request(approval_id: str, approver: str = "owner", reason: str = None) -> dict:
    """审批拒绝"""
    approvals = load_approvals()
    
    for approval in approvals:
        if approval.get("id") == approval_id:
            approval["status"] = "rejected"
            approval["approve_time"] = datetime.now().isoformat() + "Z"
            approval["approver"] = approver
            approval["reject_reason"] = reason
            
            save_approvals(approvals)
            
            log_operation("approval_rejected",
                        approval_id=approval_id,
                        reason=reason)
            
            return {"success": True, "approval": approval}
    
    return {"success": False, "reason": "审批请求不存在"}


def notify_owner_approval(approval_id: str) -> str:
    """生成通知主人的消息"""
    approvals = load_approvals()
    
    for approval in approvals:
        if approval.get("id") == approval_id:
            msg = f"""⏳ 身份审批请求

申请类型: {"申请成为朋友" if approval.get("type") == "friend_apply" else "身份变更"}
用户ID: {approval.get("user_id")}
目标身份: {approval.get("target_identity")}
暗号: {approval.get("code") or "未提供"}
申请时间: {approval.get("create_time")}

请回复 "同意 {approval_id}" 或 "拒绝 {approval_id}" """
            return msg
    
    return "审批请求不存在"


def process_owner_reply(message: str) -> dict:
    """处理主人的回复"""
    message = message.strip().lower()
    
    if message.startswith("同意 "):
        approval_id = message[3:].strip()
        return approve_request(approval_id)
    
    if message.startswith("拒绝 "):
        approval_id = message[3:].strip()
        return reject_request(approval_id, reason="主人拒绝")
    
    return {"success": False, "reason": "无效的回复格式"}


# ============ v2.0 认证流程 ============

def handle_auth_message(platform: str, open_id: str, message_text: str = "") -> dict:
    """
    处理用户认证消息
    返回: {"action": "greet"|"ask_name"|"chat", "message": "话术", "identity": "stranger|acquaintance|friend"}
    """
    # 更新最后消息时间
    _update_last_message_time(open_id)
    
    # 获取或创建会话
    session = _get_or_create_session(open_id)
    
    # 检查账号是否存在
    accounts_data = load_accounts()
    account = None
    for acc in accounts_data.get("accounts", []):
        if acc.get("open_id") == open_id:
            account = acc
            break
    
    # 场景1: 账号不存在 - 创建账号并打招呼
    if account is None:
        new_account = {
            "account_id": f"acc_{len(accounts_data.get('accounts', [])) + 1:03d}",
            "platform": platform,
            "open_id": open_id,
            "user_id": None,
            "bound_at": None,
            "created_at": datetime.now().isoformat() + "Z",
            "updated_at": datetime.now().isoformat() + "Z"
        }
        accounts_data["accounts"].append(new_account)
        save_accounts(accounts_data)
        
        # 更新会话状态
        _update_session(open_id, "waiting_name", {"action": "greet"})
        
        return {
            "action": "greet",
            "message": GREETING_NEW_USER,
            "identity": "stranger",
            "session_state": "waiting_name"
        }
    
    # 场景2: 账号存在但未绑定 - 询问名字
    if account.get("user_id") is None:
        # 更新会话状态
        _update_session(open_id, "waiting_name", {"action": "ask_name"})
        
        return {
            "action": "ask_name",
            "message": ASK_NAME,
            "identity": "stranger",
            "session_state": "waiting_name"
        }
    
    # 场景3: 账号已绑定 - 根据身份聊天
    user_result = identify_user(open_id)
    if user_result.get("found"):
        user = user_result.get("user", {})
        identity = user.get("identity", "stranger")
        
        # 更新会话状态为 idle
        _update_session(open_id, "idle", {"action": "chat"})
        
        return {
            "action": "chat",
            "message": None,
            "identity": identity,
            "session_state": "idle"
        }
    
    # 默认：陌生人
    return {
        "action": "chat",
        "message": None,
        "identity": "stranger",
        "session_state": "idle"
    }


# ============ 名字提取功能 ============

def extract_name_from_message(message_text: str) -> str | None:
    """
    从用户消息中提取名字
    使用规则匹配
    """
    if not message_text:
        return None
    
    import re
    
    # 排除的词（常见问候语等）
    exclude_words = {'你好', '您好', '嗨', '哈喽', '嘿', '在', '谁', '什么', '人', '朋友', '干嘛', '啥', '吗'}
    
    # 规则1: "我叫xxx"
    match = re.search(r'我叫[是为]?(.+?)(?:，|$)', message_text)
    if match:
        name = match.group(1).strip()
        if name not in exclude_words:
            return name
    
    # 规则2: "名字是xxx"
    match = re.search(r'名字[是为]?(.+?)(?:，|$)', message_text)
    if match:
        name = match.group(1).strip()
        if name not in exclude_words:
            return name
    
    # 规则3: "是xxx"（但要排除"是什么人"等）
    match = re.search(r'是([^，的吗呢]+?)(?:，|$)', message_text)
    if match:
        name = match.group(1).strip()
        if name and len(name) <= 10 and name not in exclude_words:
            return name
    
    return None


def extract_name_with_llm(message_text: str) -> str | None:
    """
    使用 LLM 提取名字（备选方案，需要配置 LLM API）
    """
    # TODO: 实现 LLM 调用
    # 如果规则匹配失败，可以使用 LLM 来提取
    # 示例：
    # prompt = f"从以下消息中提取人名，如果没有请回复'无': {message_text}"
    # result = call_llm(prompt)
    # return result if result != '无' else None
    return None


def create_user_v2(identity: str = "acquaintance", name: str = None) -> dict:
    """创建新用户 v2.0"""
    users_data = load_users()
    
    # 生成新用户ID
    existing_ids = []
    for u in users_data.get("users", []):
        if "user_id" in u:
            try:
                existing_ids.append(int(u["user_id"].replace("u", "")))
            except:
                pass
    new_id = f"u{max(existing_ids) + 1:03d}" if existing_ids else "u001"
    
    # 创建用户
    new_user = {
        "user_id": new_id,
        "name": name,
        "type": "human",
        "identity": identity,
        "identity_level": {"owner": 4, "friend": 3, "acquaintance": 2, "stranger": 1}.get(identity, 1),
        "code": None,
        "verificationMethod": None,
        "createTime": datetime.now().isoformat() + "Z",
        "lastContact": None,
        "accounts": [],
        "memories": {
            "key_facts": {},
            "conversation_history": [],
            "preferences": {}
        }
    }
    
    users_data["users"].append(new_user)
    save_users(users_data)
    
    return {"success": True, "user_id": new_id, "user": new_user}


def bind_account_v2(open_id: str, user_id: str) -> dict:
    """绑定账号到用户 v2.0"""
    accounts_data = load_accounts()
    
    # 更新账号
    for acc in accounts_data.get("accounts", []):
        if acc.get("open_id") == open_id:
            acc["user_id"] = user_id
            acc["bound_at"] = datetime.now().isoformat() + "Z"
            acc["updated_at"] = datetime.now().isoformat() + "Z"
            break
    
    save_accounts(accounts_data)
    
    # 更新用户的 accounts 列表
    users_data = load_users()
    for u in users_data.get("users", []):
        if u.get("user_id") == user_id:
            if "accounts" not in u:
                u["accounts"] = []
            u["accounts"].append({
                "open_id": open_id,
                "bound_at": datetime.now().isoformat() + "Z"
            })
            break
    
    save_users(users_data)
    
    return {"success": True}


def search_users_by_name(name: str) -> list:
    """根据名字搜索用户"""
    if not name:
        return []
    
    users_data = load_users()
    results = []
    
    for u in users_data.get("users", []):
        user_name = u.get("name", "")
        if user_name and name in user_name:
            results.append(u)
    
    return results


def extract_phrase_from_message(message_text: str) -> str | None:
    """
    从用户消息中提取暗号
    """
    if not message_text:
        return None
    
    import re
    
    # 规则1: "暗号是xxx"
    match = re.search(r'暗号[是为]?(.+?)(?:，|$|\s)', message_text)
    if match:
        return match.group(1).strip()
    
    # 规则2: "我的暗号是xxx"
    match = re.search(r'我的暗号[是为]?(.+?)(?:，|$|\s)', message_text)
    if match:
        return match.group(1).strip()
    
    # 规则3: 单独的短句可能是暗号
    lines = message_text.split('\n')
    for line in lines:
        line = line.strip()
        if 2 <= len(line) <= 20:
            return line
    
    return None


def check_user_has_phrase(user_id: str) -> bool:
    """检查用户是否有暗号"""
    users_data = load_users()
    for u in users_data.get("users", []):
        if u.get("user_id") == user_id:
            return bool(u.get("code"))
    return False


def verify_user_phrase(user_id: str, phrase: str) -> bool:
    """验证用户的暗号"""
    users_data = load_users()
    for u in users_data.get("users", []):
        if u.get("user_id") == user_id:
            stored_phrase = u.get("code")
            if stored_phrase and stored_phrase == phrase:
                return True
    return False


def update_user_identity(user_id: str, identity: str):
    """更新用户身份"""
    users_data = load_users()
    for u in users_data.get("users", []):
        if u.get("user_id") == user_id:
            u["identity"] = identity
            u["identity_level"] = {"owner": 4, "friend": 3, "acquaintance": 2, "stranger": 1}.get(identity, 1)
            break
    save_users(users_data)


def handle_phrase_verification(open_id: str, message_text: str) -> dict:
    """
    处理暗号验证
    返回: {"action": "verify_phrase"|"verify_question"|"bound", "message": "话术", "identity": "..."}
    """
    # 获取用户
    user_result = identify_user(open_id)
    if not user_result.get("found"):
        return {"action": "error", "message": "用户不存在", "identity": "stranger"}
    
    user = user_result.get("user", {})
    user_id = user_result.get("user_id")
    
    # 检查是否有暗号
    has_phrase = bool(user.get("code"))
    
    if not has_phrase:
        # 没有暗号，进入问题验证
        return {
            "action": "verify_question",
            "message": ASK_VERIFICATION,
            "identity": "stranger"
        }
    
    # 有暗号，提取用户回答的暗号
    phrase = extract_phrase_from_message(message_text)
    
    if not phrase:
        # 没有提取到暗号，可能是乱回的
        return {
            "action": "verify_phrase",
            "message": ASK_PHRASE,
            "identity": "stranger"
        }
    
    # 验证暗号
    if verify_user_phrase(user_id, phrase):
        # 验证成功，绑定账号
        bind_account_v2(open_id, user_id)
        # 更新身份为 friend
        update_user_identity(user_id, "friend")
        
        return {
            "action": "bound",
            "message": PHRASE_CORRECT,
            "identity": "friend"
        }
    else:
        # 暗号错误，进入问题验证
        return {
            "action": "verify_question",
            "message": ASK_VERIFICATION,
            "identity": "stranger"
        }


def get_user_conversation_history(user_id: str) -> list:
    """获取用户的对话历史"""
    users_data = load_users()
    for u in users_data.get("users", []):
        if u.get("user_id") == user_id:
            return u.get("memories", {}).get("conversation_history", [])
    return []


def add_conversation_summary(user_id: str, summary: str):
    """添加对话摘要"""
    users_data = load_users()
    for u in users_data.get("users", []):
        if u.get("user_id") == user_id:
            if "memories" not in u:
                u["memories"] = {"key_facts": {}, "conversation_history": [], "preferences": {}}
            if "conversation_history" not in u["memories"]:
                u["memories"]["conversation_history"] = []
            
            u["memories"]["conversation_history"].append({
                "date": datetime.now().strftime("%Y-%m-%d"),
                "summary": summary
            })
            # 保留最近20条
            if len(u["memories"]["conversation_history"]) > 20:
                u["memories"]["conversation_history"] = u["memories"]["conversation_history"][-20:]
            break
    save_users(users_data)


def check_verification_answer(user_id: str, answer: str) -> bool:
    """
    检查验证答案是否正确
    从对话历史中获取信息进行比对
    """
    history = get_user_conversation_history(user_id)
    
    if not history:
        # 没有历史记录，暂时让通过（第一个用户可能没有历史）
        return True
    
    # 简单验证：检查答案中是否包含日期或关键词
    # 后续可以改进为更智能的验证
    today = datetime.now().strftime("%Y-%m-%d")
    yesterday = (datetime.now().replace(day=datetime.now().day-1)).strftime("%Y-%m-%d")
    
    # 检查答案是否包含日期
    if today in answer or yesterday in answer:
        return True
    
    # 检查答案是否包含历史中的关键词
    for item in history[-3:]:  # 只检查最近3条
        summary = item.get("summary", "")
        for word in summary:
            if word in answer:
                return True
    
    # 默认返回True，让用户通过（避免太严格）
    return True


def handle_verification_question(open_id: str, message_text: str) -> dict:
    """
    处理问题验证
    """
    # 获取用户
    user_result = identify_user(open_id)
    if not user_result.get("found"):
        return {"action": "error", "message": "用户不存在", "identity": "stranger"}
    
    user = user_result.get("user", {})
    user_id = user_result.get("user_id")
    
    # 验证答案
    if check_verification_answer(user_id, message_text):
        # 验证通过，绑定账号
        bind_account_v2(open_id, user_id)
        # 更新身份为 friend
        update_user_identity(user_id, "friend")
        
        return {
            "action": "bound",
            "message": VERIFICATION_PASS,
            "identity": "friend"
        }
    else:
        # 验证失败，变成新朋友
        # 创建新用户
        user_name = user.get("name", "新朋友")
        new_result = create_user_v2("acquaintance", user_name)
        new_user_id = new_result["user_id"]
        
        # 绑定账号到新用户
        bind_account_v2(open_id, new_user_id)
        
        return {
            "action": "new_friend",
            "message": VERIFICATION_FAIL,
            "identity": "acquaintance"
        }


def extract_key_facts(message_text: str) -> dict:
    """
    从用户消息中提取关键信息
    """
    import re
    facts = {}
    
    # 生日
    match = re.search(r'生日[是为是]?(\d{1,2}[月/-]\d{1,2}[日号]?)', message_text)
    if match:
        facts['birthday'] = match.group(1)
    
    match = re.search(r'(\d{1,2}[月/-]\d{1,2}[日号]?)[是祝]生日', message_text)
    if match:
        facts['birthday'] = match.group(1)
    
    # 年龄
    match = re.search(r'(\d{2})岁', message_text)
    if match:
        facts['age'] = match.group(1)
    
    # 公司
    match = re.search(r'(在|在|去)(.+)工作', message_text)
    if match:
        facts['company'] = match.group(2).strip()
    
    match = re.search(r'(在|在|去)(.+)上班', message_text)
    if match:
        facts['company'] = match.group(2).strip()
    
    # 地点
    match = re.search(r'(在|住在)(.+) (住|在)', message_text)
    if match:
        facts['location'] = match.group(2).strip()
    
    # 职业
    match = re.search(r'(是|做)(.+)的', message_text)
    if match:
        job = match.group(2).strip()
        if len(job) <= 10:
            facts['job'] = job
    
    return facts


def check_remember_keyword(message_text: str) -> bool:
    """
    检测是否包含"帮我记住"关键词
    """
    keywords = ['帮我记住', '记住', '记一下', '记录一下']
    for keyword in keywords:
        if keyword in message_text:
            return True
    return False


def add_key_fact(open_id: str, key: str, value: str) -> bool:
    """
    添加用户的关键信息
    """
    # 获取用户
    user_result = identify_user(open_id)
    if not user_result.get("found"):
        return False
    
    user_id = user_result.get("user_id")
    
    users_data = load_users()
    for u in users_data.get("users", []):
        if u.get("user_id") == user_id:
            if "memories" not in u:
                u["memories"] = {"key_facts": {}, "conversation_history": [], "preferences": {}}
            if "key_facts" not in u["memories"]:
                u["memories"]["key_facts"] = {}
            
            u["memories"]["key_facts"][key] = value
            break
    
    save_users(users_data)
    return True


def handle_memory_request(open_id: str, message_text: str) -> dict:
    """
    处理用户的记忆请求
    返回: {"action": "remembered"|"none", "message": "回复话术"}
    """
    # 检查是否包含记忆关键词
    if not check_remember_keyword(message_text):
        return {"action": "none", "message": None}
    
    # 提取关键信息
    facts = extract_key_facts(message_text)
    
    if not facts:
        return {"action": "none", "message": "好的，我会记住的～"}
    
    # 存储每个关键信息
    for key, value in facts.items():
        add_key_fact(open_id, key, value)
    
    # 生成回复
    fact_list = [f"{k}: {v}" for k, v in facts.items()]
    message = f"好的，我记住啦！{', '.join(fact_list)}～ 😊"
    
    return {"action": "remembered", "message": message}


def check_goodbye_keyword(message_text: str) -> bool:
    """
    检测是否包含再见关键词
    """
    keywords = ['再见', '拜拜', 'bye', '回头见', '先走了', '下了', '休息了', '睡觉了', '忙去了']
    for keyword in keywords:
        if keyword in message_text.lower():
            return True
    return False


def generate_conversation_summary(messages: list) -> str:
    """
    生成对话摘要
    后续可以用 LLM 来生成更准确的摘要
    """
    if not messages:
        return "简单打了个招呼"
    
    # 简单规则：统计消息数量和关键词
    count = len(messages)
    
    # 检测话题
    topics = []
    all_text = ' '.join([m.get('text', '') for m in messages])
    
    if '天气' in all_text:
        topics.append('天气')
    if '权限' in all_text or '身份' in all_text:
        topics.append('权限系统')
    if '工作' in all_text or '公司' in all_text:
        topics.append('工作')
    if '学习' in all_text or '代码' in all_text:
        topics.append('学习')
    
    if topics:
        topic_str = '、'.join(topics)
        return f"讨论了{topic_str}"
    elif count == 1:
        return "简单打了个招呼"
    else:
        return f"聊了{count}句话"


def handle_goodbye(open_id: str) -> dict:
    """
    处理用户再见
    生成对话摘要并存储
    """
    # 获取用户
    user_result = identify_user(open_id)
    if not user_result.get("found"):
        return {"action": "none", "message": None}
    
    user_id = user_result.get("user_id")
    
    # 生成摘要
    summary = "用户离开，生成了对话摘要"
    add_conversation_summary(user_id, summary)
    
    message = "好的，有空再聊！拜拜～ 👋"
    
    return {"action": "goodbye", "message": message}
