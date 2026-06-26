"""
权限检查核心模块
提供用户识别、权限检查和统一鉴权功能
"""

import json
import os
from datetime import datetime
from typing import Optional, Dict, Any, Tuple

# 数据文件路径
DATA_DIR = "/workspace/data"
USERS_FILE = os.path.join(DATA_DIR, "users.json")
ACCOUNTS_FILE = os.path.join(DATA_DIR, "accounts.json")
PERMISSIONS_FILE = os.path.join(DATA_DIR, "permissions.json")

# 权限配置
ROLE_PERMISSIONS = {
    "owner": {
        "read": True,
        "write": True,
        "admin": True,
        "execute": True
    },
    "friend": {
        "read": True,
        "write": False,
        "admin": False,
        "execute": True
    },
    "stranger": {
        "read": False,
        "write": False,
        "admin": False,
        "execute": False
    }
}


def _load_json(file_path: str) -> Dict[str, Any]:
    """加载 JSON 文件"""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def identify_user(open_id: str, platform: str) -> Optional[Dict[str, Any]]:
    """
    根据平台账号 ID 查找对应的用户信息
    
    Args:
        open_id: 平台账号 ID（如飞书的 open_id）
        platform: 平台名称（如 "feishu"）
    
    Returns:
        用户对象（含 user_id, name, role）或 None（未找到）
    """
    # 加载账号绑定关系
    accounts_data = _load_json(ACCOUNTS_FILE)
    accounts = accounts_data.get("accounts", [])
    
    # 查找账号绑定
    account = None
    for acc in accounts:
        if acc.get("open_id") == open_id and acc.get("platform") == platform:
            account = acc
            break
    
    if not account:
        return None
    
    user_id = account.get("user_id")
    if not user_id:
        return None
    
    # 加载用户信息
    users_data = _load_json(USERS_FILE)
    users = users_data.get("users", [])
    
    # 查找用户
    for user in users:
        if user.get("user_id") == user_id:
            return user
    
    return None


def check_permission(user: Dict[str, Any], permission: str) -> bool:
    """
    检查用户是否拥有指定权限
    
    Args:
        user: 用户对象（需包含 role 字段）
        permission: 权限名称（read/write/admin/execute）
    
    Returns:
        True 允许，False 拒绝
    """
    if not user or not isinstance(user, dict):
        return False
    
    role = user.get("role", "stranger")
    
    # 获取角色权限配置
    role_perms = ROLE_PERMISSIONS.get(role, ROLE_PERMISSIONS.get("stranger", {}))
    
    # 返回权限结果
    return role_perms.get(permission, False)


def authenticate(request: Dict[str, Any]) -> Dict[str, Any]:
    """
    统一鉴权入口
    
    Args:
        request: 请求对象，需包含以下字段：
            - open_id: 平台账号 ID
            - platform: 平台名称
            - permission: 请求的权限名称（可选，不提供则只验证身份）
    
    Returns:
        {
            "allowed": True/False,
            "user": user对象,
            "reason": "说明"
        }
    """
    open_id = request.get("open_id")
    platform = request.get("platform")
    permission = request.get("permission")
    
    # 参数校验
    if not open_id or not platform:
        return {
            "allowed": False,
            "user": None,
            "reason": "缺少必要参数 open_id 或 platform"
        }
    
    # 识别用户
    user = identify_user(open_id, platform)
    
    if not user:
        return {
            "allowed": False,
            "user": None,
            "reason": "未找到绑定的用户"
        }
    
    # 如果没有指定权限检查，只验证身份（视为通过）
    if not permission:
        return {
            "allowed": True,
            "user": user,
            "reason": "身份验证通过"
        }
    
    # 检查权限
    allowed = check_permission(user, permission)
    
    if allowed:
        return {
            "allowed": True,
            "user": user,
            "reason": f"权限检查通过 ({permission})"
        }
    else:
        role = user.get("role", "unknown")
        return {
            "allowed": False,
            "user": user,
            "reason": f"权限不足: {role} 角色无权执行 {permission}"
        }


# 便捷函数：检查是否为 owner
def is_owner(user: Dict[str, Any]) -> bool:
    """检查用户是否为 owner"""
    return user.get("role") == "owner"


# 便捷函数：检查是否为 friend
def is_friend(user: Dict[str, Any]) -> bool:
    """检查用户是否为 friend"""
    return user.get("role") == "friend"


# 便捷函数：检查是否为 stranger
def is_stranger(user: Dict[str, Any]) -> bool:
    """检查用户是否为 stranger"""
    return user.get("role") == "stranger"


# ============ 认证 2.0 新增函数 ============

def _save_json(file_path: str, data: Dict[str, Any]) -> None:
    """保存 JSON 文件"""
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def _generate_id(existing_ids: list, prefix: str) -> str:
    """生成新的 ID"""
    if not existing_ids:
        return f"{prefix}001"
    
    # 提取数字部分
    numbers = []
    for id_str in existing_ids:
        try:
            # 处理 u001 和 u_001 两种格式
            num = int(id_str.replace(prefix, ""))
            numbers.append(num)
        except:
            continue
    
    if not numbers:
        return f"{prefix}001"
    
    new_num = max(numbers) + 1
    return f"{prefix}{new_num:03d}"


def identify_account(open_id: str, platform: str) -> Tuple[Optional[Dict], bool]:
    """
    识别账号状态
    
    Args:
        open_id: 平台账号 ID
        platform: 平台名称
    
    Returns:
        (account, is_new_account)
        - account: 账号信息，不存在则返回 None
        - is_new_account: 是否是新账号
    """
    accounts_data = _load_json(ACCOUNTS_FILE)
    accounts = accounts_data.get("accounts", [])
    
    # 查找账号
    for acc in accounts:
        if acc.get("open_id") == open_id and acc.get("platform") == platform:
            return acc, False
    
    # 账号不存在
    return None, True


def create_account(open_id: str, platform: str) -> Dict[str, Any]:
    """
    创建新账号记录
    
    Args:
        open_id: 平台账号 ID
        platform: 平台名称
    
    Returns:
        新创建的账号信息
    """
    accounts_data = _load_json(ACCOUNTS_FILE)
    accounts = accounts_data.get("accounts", [])
    
    # 生成新 ID
    existing_ids = [acc.get("account_id", "") for acc in accounts]
    new_id = _generate_id(existing_ids, "acc")
    
    # 创建账号记录（未绑定用户）
    new_account = {
        "account_id": new_id,
        "platform": platform,
        "open_id": open_id,
        "user_id": None,  # 未绑定
        "bound_at": None,
        "created_at": datetime.now().isoformat() + "Z"
    }
    
    accounts.append(new_account)
    accounts_data["accounts"] = accounts
    _save_json(ACCOUNTS_FILE, accounts_data)
    
    return new_account


def bind_account_to_user(open_id: str, platform: str, user_id: str) -> bool:
    """
    绑定账号到用户
    
    Args:
        open_id: 平台账号 ID
        platform: 平台名称
        user_id: 用户 ID
    
    Returns:
        是否绑定成功
    """
    accounts_data = _load_json(ACCOUNTS_FILE)
    accounts = accounts_data.get("accounts", [])
    
    for acc in accounts:
        if acc.get("open_id") == open_id and acc.get("platform") == platform:
            acc["user_id"] = user_id
            acc["bound_at"] = datetime.now().isoformat() + "Z"
            accounts_data["accounts"] = accounts
            _save_json(ACCOUNTS_FILE, accounts_data)
            return True
    
    return False


def find_user_by_name(name: str) -> Optional[Dict]:
    """
    根据名字查找用户
    
    Args:
        name: 用户名字
    
    Returns:
        用户信息，不存在则返回 None
    """
    users_data = _load_json(USERS_FILE)
    users = users_data.get("users", [])
    
    for user in users:
        if user.get("name") == name:
            return user
    
    return None


def create_user(name: str, role: str = "stranger") -> Dict[str, Any]:
    """
    创建新用户
    
    Args:
        name: 用户名字
        role: 角色（默认 stranger）
    
    Returns:
        新创建的用户信息
    """
    users_data = _load_json(USERS_FILE)
    users = users_data.get("users", [])
    
    # 生成新 ID
    existing_ids = [u.get("user_id", "") for u in users]
    new_id = _generate_id(existing_ids, "u")
    
    # 创建用户记录
    now = datetime.now().isoformat() + "Z"
    new_user = {
        "user_id": new_id,
        "name": name,
        "role": role,
        "identity": role,
        "created_at": now,
        "first_seen": now
    }
    
    users.append(new_user)
    users_data["users"] = users
    _save_json(USERS_FILE, users_data)
    
    return new_user


def handle_unknown_user(open_id: str, platform: str) -> Dict[str, Any]:
    """
    处理未知用户的主函数
    
    实现认证 2.0 流程：
    1. 检查账号是否存在
    2. 如果不存在，创建账号
    3. 检查是否绑定用户
    4. 返回状态和响应信息
    
    Args:
        open_id: 平台账号 ID
        platform: 平台名称
    
    Returns:
        {
            "status": "new_account" | "unbound" | "bound",
            "account": 账号信息,
            "user": 用户信息（如果已绑定）,
            "response": "需要返回给用户的消息",
            "action": "greet" | "ask_name" | "normal"
        }
    """
    # Step 1: 检查账号是否存在
    account, is_new = identify_account(open_id, platform)
    
    if is_new or not account:
        # 新账号，需要创建
        account = create_account(open_id, platform)
        return {
            "status": "new_account",
            "account": account,
            "user": None,
            "response": "你好呀～ 我们好像第一次见面，先认识一下吧？😊",
            "action": "greet"
        }
    
    # Step 2: 检查是否绑定用户
    user_id = account.get("user_id")
    
    if not user_id:
        # 账号存在但未绑定用户
        return {
            "status": "unbound",
            "account": account,
            "user": None,
            "response": "我们之前聊过，但我不确定你是谁～ 如果你愿意，可以告诉我名字，我记下来～",
            "action": "ask_name"
        }
    
    # Step 3: 已绑定用户，获取用户信息
    user = identify_user(open_id, platform)
    
    return {
        "status": "bound",
        "account": account,
        "user": user,
        "response": None,
        "action": "normal"
    }


def process_name_response(open_id: str, platform: str, name: str) -> Dict[str, Any]:
    """
    处理用户回复名字的逻辑
    
    Args:
        open_id: 平台账号 ID
        platform: 平台名称
        name: 用户告诉的名字
    
    Returns:
        {
            "status": "new_user" | "existing_user",
            "user": 用户信息,
            "response": "需要返回给用户的消息"
        }
    """
    # 检查名字是否已存在
    existing_user = find_user_by_name(name)
    
    if existing_user:
        # 名字已存在，可能是老用户或重名
        # 这里先简化为创建新用户（后续可以加验证机制）
        user = create_user(name)
        bind_account_to_user(open_id, platform, user["user_id"])
        return {
            "status": "new_user",
            "user": user,
            "response": f"{name}你好！很高兴认识你～ 有什么我可以帮你的吗？✨"
        }
    else:
        # 名字不存在，创建新用户
        user = create_user(name)
        bind_account_to_user(open_id, platform, user["user_id"])
        return {
            "status": "new_user",
            "user": user,
            "response": f"{name}你好！很高兴认识你～ 有什么我可以帮你的吗？✨"
        }


if __name__ == "__main__":
    # 测试代码
    print("=== 权限检查模块测试 ===")
    
    # 测试 identify_user
    print("\n1. 测试 identify_user:")
    user = identify_user("ou_xxx", "feishu")
    print(f"   结果: {user}")
    
    # 测试 check_permission
    if user:
        print("\n2. 测试 check_permission:")
        for perm in ["read", "write", "admin", "execute"]:
            result = check_permission(user, perm)
            print(f"   {perm}: {result}")
    
    # 测试 authenticate
    print("\n3. 测试 authenticate:")
    result = authenticate({
        "open_id": "ou_xxx",
        "platform": "feishu",
        "permission": "read"
    })
    print(f"   结果: {result}")
