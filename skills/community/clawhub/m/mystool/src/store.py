"""
账号数据管理 — 读写 accounts.json
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Optional, Tuple

DATA_DIR = Path(__file__).parent.parent / "data"
ACCOUNTS_FILE = DATA_DIR / "accounts.json"


def _ensure_dir():
    DATA_DIR.mkdir(parents=True, exist_ok=True)


def load_accounts() -> Dict[str, dict]:
    """
    加载所有账号数据。
    结构: { user_id: { "accounts": [ { "uid", "nickname", "cookies", "games": [...] } ] } }
    """
    _ensure_dir()
    if not ACCOUNTS_FILE.exists():
        return {}
    try:
        with open(ACCOUNTS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def save_accounts(data: Dict[str, dict]):
    """保存账号数据"""
    _ensure_dir()
    with open(ACCOUNTS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def get_user_accounts(user_id: str) -> List[dict]:
    """获取某用户绑定的所有米游社账号"""
    data = load_accounts()
    return data.get(user_id, {}).get("accounts", [])


def add_account(user_id: str, uid: str, nickname: str, cookies: Dict[str, str], games: List[dict]) -> bool:
    """
    添加或更新账号绑定
    :return: True=新增, False=更新
    """
    data = load_accounts()
    user_data = data.setdefault(user_id, {"accounts": []})
    accounts = user_data["accounts"]

    # 检查是否已存在
    for acc in accounts:
        if acc["uid"] == uid:
            acc["nickname"] = nickname
            acc["cookies"] = cookies
            acc["games"] = games
            save_accounts(data)
            return False

    accounts.append({
        "uid": uid,
        "nickname": nickname,
        "cookies": cookies,
        "games": games,
    })
    save_accounts(data)
    return True


def remove_account(user_id: str, uid: str) -> bool:
    """删除账号绑定"""
    data = load_accounts()
    user_data = data.get(user_id)
    if not user_data:
        return False
    before = len(user_data["accounts"])
    user_data["accounts"] = [a for a in user_data["accounts"] if a["uid"] != uid]
    if len(user_data["accounts"]) < before:
        save_accounts(data)
        return True
    return False


def get_all_user_ids() -> List[str]:
    """获取所有有绑定账号的用户 ID"""
    return list(load_accounts().keys())


# 标准米游社 Cookie 字段（过滤非标准 key）
STANDARD_COOKIE_KEYS = {
    "account_id", "account_id_v2", "account_mid_v2",
    "ltoken", "ltoken_v2", "ltmid_v2", "ltuid", "ltuid_v2",
    "cookie_token", "cookie_token_v2",
    "mid", "stoken", "stoken_v2", "stuid", "stuid_v2",
    "login_uid", "MHYUUID", "DEVICEFP", "DEVICEFP_SEED_ID", 
    "DEVICEFP_SEED_TIME", "MIHOYO_LOGIN_PLATFORM_LIFECYCLE_ID",
}


def parse_cookie_string(cookie_str: str) -> Dict[str, str]:
    """
    将 Cookie 字符串解析为字典
    支持格式: "key1=val1; key2=val2" 或 "key1=val1\nkey2=val2"
    自动过滤非标准字段（如中文 key）
    """
    cookies = {}
    # 统一分隔符
    parts = cookie_str.replace("\n", ";").split(";")
    for part in parts:
        part = part.strip()
        if "=" in part:
            k, _, v = part.partition("=")
            key = k.strip()
            # 过滤非 ASCII 字符的 key
            if key and all(ord(c) < 128 for c in key):
                cookies[key] = v.strip()
    return cookies


def extract_uid_from_cookies(cookies: Dict[str, str]) -> Optional[str]:
    """从 Cookie 中提取用户 UID"""
    for key in ["account_id", "ltuid", "stuid", "login_uid"]:
        if cookies.get(key):
            return cookies[key]
    return None


def validate_cookies(cookies: Dict[str, str]) -> Tuple[bool, str]:
    """
    验证 Cookie 是否包含必要字段
    返回 (是否有效, 提示信息)
    """
    has_basic = bool(cookies.get("cookie_token") and cookies.get("account_id"))
    has_stoken = bool(cookies.get("stoken") and (cookies.get("stuid") or cookies.get("account_id")))

    if not has_basic and not has_stoken:
        return False, (
            "Cookie 缺少必要字段。\n"
            "需要包含以下之一：\n"
            "• `cookie_token` + `account_id`\n"
            "• `stoken` + `stuid`"
        )
    return True, "OK"


# ── 登录会话状态持久化 ─────────────────────────────────────────────────────────
# 用文件存储跨消息的扫码会话，key = user_id

LOGIN_SESSIONS_FILE = DATA_DIR / "login_sessions.json"


def save_login_session(user_id: str, ticket: str, qr_url: str, device: str = None):
    """保存扫码登录会话（ticket + device + 时间戳）"""
    _ensure_dir()
    sessions = _load_login_sessions()
    sessions[user_id] = {
        "ticket": ticket,
        "qr_url": qr_url,
        "device": device,
        "created_at": time.time(),
    }
    with open(LOGIN_SESSIONS_FILE, "w", encoding="utf-8") as f:
        json.dump(sessions, f, ensure_ascii=False, indent=2)


def get_login_session(user_id: str) -> Optional[Dict]:
    """获取用户的扫码登录会话，超过3分钟自动失效"""
    sessions = _load_login_sessions()
    s = sessions.get(user_id)
    if not s:
        return None
    if time.time() - s.get("created_at", 0) > 180:
        clear_login_session(user_id)
        return None
    return s


def clear_login_session(user_id: str):
    """清除登录会话"""
    sessions = _load_login_sessions()
    sessions.pop(user_id, None)
    _ensure_dir()
    with open(LOGIN_SESSIONS_FILE, "w", encoding="utf-8") as f:
        json.dump(sessions, f, ensure_ascii=False, indent=2)


def _load_login_sessions() -> Dict:
    if not LOGIN_SESSIONS_FILE.exists():
        return {}
    try:
        with open(LOGIN_SESSIONS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


# ── 短信登录会话状态持久化 ───────────────────────────────────────────────────────

SMS_SESSIONS_FILE = DATA_DIR / "sms_sessions.json"


def save_sms_session(user_id: str, session: dict):
    """保存短信登录会话"""
    _ensure_dir()
    sessions = _load_sms_sessions()
    session["created_at"] = session.get("created_at", time.time())
    sessions[user_id] = session
    with open(SMS_SESSIONS_FILE, "w", encoding="utf-8") as f:
        json.dump(sessions, f, ensure_ascii=False, indent=2)


def get_sms_session(user_id: str) -> Optional[Dict]:
    """获取用户的短信登录会话，超过 5 分钟自动失效"""
    sessions = _load_sms_sessions()
    s = sessions.get(user_id)
    if not s:
        return None
    if time.time() - s.get("created_at", 0) > 300:
        clear_sms_session(user_id)
        return None
    return s


def clear_sms_session(user_id: str):
    """清除短信登录会话"""
    sessions = _load_sms_sessions()
    sessions.pop(user_id, None)
    _ensure_dir()
    with open(SMS_SESSIONS_FILE, "w", encoding="utf-8") as f:
        json.dump(sessions, f, ensure_ascii=False, indent=2)


def _load_sms_sessions() -> Dict:
    if not SMS_SESSIONS_FILE.exists():
        return {}
    try:
        with open(SMS_SESSIONS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


import time  # noqa: E402 (放末尾避免循环)


# ── 跨平台用户识别码 ─────────────────────────────────────────────────────────

LINK_CODES_FILE = DATA_DIR / "link_codes.json"


def generate_link_code(user_id: str) -> str:
    """
    生成用户识别码（6位字母数字）
    用于跨平台账号绑定
    """
    import random
    import string
    
    _ensure_dir()
    
    # 加载现有识别码
    codes = _load_link_codes()
    
    # 生成新识别码
    code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    
    # 存储识别码映射
    codes[code] = {
        "user_id": user_id,
        "created_at": time.time(),
    }
    
    with open(LINK_CODES_FILE, "w", encoding="utf-8") as f:
        json.dump(codes, f, ensure_ascii=False, indent=2)
    
    return code


def verify_link_code(code: str) -> Optional[str]:
    """
    验证识别码，返回原用户ID
    识别码有效期10分钟
    """
    codes = _load_link_codes()
    
    code_data = codes.get(code.upper())
    if not code_data:
        return None
    
    # 检查是否过期（10分钟）
    if time.time() - code_data.get("created_at", 0) > 600:
        # 删除过期识别码
        codes.pop(code.upper(), None)
        _save_link_codes(codes)
        return None
    
    return code_data.get("user_id")


def _load_link_codes() -> Dict:
    if not LINK_CODES_FILE.exists():
        return {}
    try:
        with open(LINK_CODES_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def _save_link_codes(codes: Dict):
    _ensure_dir()
    with open(LINK_CODES_FILE, "w", encoding="utf-8") as f:
        json.dump(codes, f, ensure_ascii=False, indent=2)


def merge_user_accounts(source_user_id: str, target_user_id: str) -> bool:
    """
    合并两个平台用户的账号数据
    source_user_id: 原用户（有米游社账号）
    target_user_id: 目标用户（要共享账号）
    """
    data = load_accounts()
    
    source_accounts = data.get(source_user_id, {}).get("accounts", [])
    target_accounts = data.get(target_user_id, {}).get("accounts", [])
    
    if not source_accounts:
        return False
    
    # 合并账号数据（目标用户复制源用户的账号）
    # 如果目标用户已有相同 UID 的账号，更新 cookies 和 games
    merged_accounts = []
    
    for src_acc in source_accounts:
        src_uid = src_acc["uid"]
        merged = False
        
        for tgt_acc in target_accounts:
            if tgt_acc["uid"] == src_uid:
                # 合并 cookies（取字段更多的版本）
                merged_cookies = {**tgt_acc.get("cookies", {}), **src_acc.get("cookies", {})}
                # 合并 games（取非空的版本）
                merged_games = src_acc.get("games", []) or tgt_acc.get("games", [])
                
                tgt_acc["cookies"] = merged_cookies
                tgt_acc["games"] = merged_games
                tgt_acc["nickname"] = src_acc.get("nickname", tgt_acc.get("nickname"))
                merged = True
                break
        
        if not merged:
            # 目标用户没有此账号，添加
            target_accounts.append({
                "uid": src_acc["uid"],
                "nickname": src_acc.get("nickname", ""),
                "cookies": src_acc.get("cookies", {}),
                "games": src_acc.get("games", []),
            })
    
    data.setdefault(target_user_id, {"accounts": target_accounts})
    data[target_user_id]["accounts"] = target_accounts
    
    save_accounts(data)
    return True




# ── 跨平台用户识别码 ─────────────────────────────────────────────────────────

LINK_CODES_FILE = DATA_DIR / "link_codes.json"


def generate_link_code(user_id: str) -> str:
    """
    生成用户识别码（6位字母数字）
    用于跨平台账号绑定
    """
    import random
    import string
    
    _ensure_dir()
    
    # 加载现有识别码
    codes = _load_link_codes()
    
    # 生成新识别码
    code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    
    # 存储识别码映射
    codes[code] = {
        "user_id": user_id,
        "created_at": time.time(),
    }
    
    with open(LINK_CODES_FILE, "w", encoding="utf-8") as f:
        json.dump(codes, f, ensure_ascii=False, indent=2)
    
    return code


def verify_link_code(code: str) -> Optional[str]:
    """
    验证识别码，返回原用户ID
    识别码有效期10分钟
    """
    codes = _load_link_codes()
    
    code_data = codes.get(code.upper())
    if not code_data:
        return None
    
    # 检查是否过期（10分钟）
    if time.time() - code_data.get("created_at", 0) > 600:
        # 删除过期识别码
        codes.pop(code.upper(), None)
        _save_link_codes(codes)
        return None
    
    return code_data.get("user_id")


def _load_link_codes() -> Dict:
    if not LINK_CODES_FILE.exists():
        return {}
    try:
        with open(LINK_CODES_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def _save_link_codes(codes: Dict):
    _ensure_dir()
    with open(LINK_CODES_FILE, "w", encoding="utf-8") as f:
        json.dump(codes, f, ensure_ascii=False, indent=2)


def merge_user_accounts(source_user_id: str, target_user_id: str) -> bool:
    """
    合并两个平台用户的账号数据
    source_user_id: 原用户（有米游社账号）
    target_user_id: 目标用户（要共享账号）
    """
    data = load_accounts()
    
    source_accounts = data.get(source_user_id, {}).get("accounts", [])
    target_accounts = data.get(target_user_id, {}).get("accounts", [])
    
    if not source_accounts:
        return False
    
    # 合并账号数据（目标用户复制源用户的账号）
    # 如果目标用户已有相同 UID 的账号，更新 cookies 和 games
    for src_acc in source_accounts:
        src_uid = src_acc["uid"]
        merged = False
        
        for tgt_acc in target_accounts:
            if tgt_acc["uid"] == src_uid:
                # 合并 cookies（取字段更多的版本）
                merged_cookies = {**tgt_acc.get("cookies", {}), **src_acc.get("cookies", {})}
                # 合并 games（取非空的版本）
                merged_games = src_acc.get("games", []) or tgt_acc.get("games", [])
                
                tgt_acc["cookies"] = merged_cookies
                tgt_acc["games"] = merged_games
                tgt_acc["nickname"] = src_acc.get("nickname", tgt_acc.get("nickname"))
                merged = True
                break
        
        if not merged:
            # 目标用户没有此账号，添加
            target_accounts.append({
                "uid": src_acc["uid"],
                "nickname": src_acc.get("nickname", ""),
                "cookies": src_acc.get("cookies", {}),
                "games": src_acc.get("games", []),
            })
    
    data.setdefault(target_user_id, {"accounts": target_accounts})
    data[target_user_id]["accounts"] = target_accounts
    
    save_accounts(data)
    return True
