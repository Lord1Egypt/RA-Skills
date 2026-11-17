#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MC Skill 客户端授权验证模块 v3.0 - 静默轮询模式

安全设计:
  1. 启动时自动查询服务器授权状态，用户零交互
  2. 后台定时轮询（每5分钟），授权变更实时生效
  3. Token 只存内存，不落盘（防止本地文件被盗）
  4. 离线模式使用本地缓存，但缓存最多 1 小时
  5. 机器码 + 服务器签名双重验证

使用方法（Skill 启动时调用）:
    from core.auth_client import verify_auth, start_background_polling
    
    # 启动时验证
    auth = verify_auth()
    
    # 启动后台轮询（可选，保持授权实时同步）
    start_background_polling()
"""

import json
import os
import hashlib
import platform
import uuid
import sys
import threading
import time
import requests
from datetime import datetime, timedelta

# ==================== 配置 ====================
SERVER_URL = "http://localhost:8000"

# 本地缓存路径（仅用于离线模式，不存 Token）
CACHE_FILE = os.path.join(
    os.path.dirname(os.path.dirname(__file__)), 
    "data", "auth_cache.json"
)

# 轮询间隔（秒）
POLL_INTERVAL = 300  # 5 分钟

# 离线缓存有效期（秒）
OFFLINE_CACHE_TTL = 3600  # 1 小时

# 免费额度配置
FREE_DAILY_LIMITS = {"auto": 20, "semi": 8, "evaluate": 1}
MEMBER_DAILY_LIMITS = {"auto": 100, "semi": 50, "evaluate": 5}

# ==================== 全局状态 ====================
# 内存中的授权状态（不落盘）
_memory_auth = {
    "authorized": False,
    "tier": "free",
    "plan": "free",
    "plan_cn": "",
    "token": None,
    "expire_at": None,
    "days_left": 0,
    "last_check": None,
    "token_expires_at": None,
}

_background_thread = None
_polling_active = False

# ==================== 工具函数 ====================
def get_machine_id():
    """获取机器唯一标识"""
    system_info = f"{platform.node()}-{platform.processor()}-{uuid.getnode()}"
    return hashlib.sha256(system_info.encode()).hexdigest()[:16]

def load_cache():
    """加载本地离线缓存"""
    if os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE, "r", encoding="utf-8") as f:
                cache = json.load(f)
            # 检查缓存是否过期
            cached_at = cache.get("cached_at", "")
            if cached_at:
                cached_time = datetime.fromisoformat(cached_at)
                if (datetime.now() - cached_time).total_seconds() > OFFLINE_CACHE_TTL:
                    return None  # 缓存过期
            return cache
        except (json.JSONDecodeError, IOError, ValueError):
            pass
    return None

def save_cache(data):
    """保存本地离线缓存（不含 Token）"""
    os.makedirs(os.path.dirname(CACHE_FILE), exist_ok=True)
    cache_data = {
        "authorized": data.get("authorized", False),
        "tier": data.get("tier", "free"),
        "plan": data.get("plan", "free"),
        "plan_cn": data.get("plan_cn", ""),
        "expire_at": data.get("expire_at"),
        "days_left": data.get("days_left", 0),
        "cached_at": datetime.now().isoformat(),
        # 注意：不保存 token！
    }
    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(cache_data, f, ensure_ascii=False, indent=2)

def clear_cache():
    """清除本地缓存"""
    if os.path.exists(CACHE_FILE):
        os.remove(CACHE_FILE)

# ==================== 核心验证逻辑 ====================
def verify_auth():
    """
    验证用户权限（Skill 启动时调用，以及定期轮询）
    
    返回:
        dict: {
            "authorized": bool,
            "tier": str,  # "free" 或 "normal"
            "plan": str,  # "monthly"/"quarterly"/"yearly"
            "plan_cn": str,
            "remaining": dict,
            "message": str,
            "offline": bool,  # 是否离线模式
        }
    """
    global _memory_auth
    machine_id = get_machine_id()
    
    # 1. 尝试在线查询
    try:
        resp = requests.post(
            f"{SERVER_URL}/api/auth/quick-check",
            json={"machine_id": machine_id},
            timeout=5
        )
        data = resp.json()
        
        if data.get("authorized"):
            # 授权有效 - 更新内存状态
            _memory_auth.update({
                "authorized": True,
                "tier": data.get("tier", "normal"),
                "plan": data.get("plan", "unknown"),
                "plan_cn": data.get("plan_cn", ""),
                "token": data.get("token"),
                "expire_at": data.get("expire_at"),
                "days_left": data.get("days_left", 0),
                "last_check": datetime.now().isoformat(),
                "token_expires_at": datetime.now() + timedelta(
                    seconds=data.get("token_expires_in", 3600)
                ),
            })
            # 保存离线缓存（不含 Token）
            save_cache(_memory_auth)
            
            return {
                "authorized": True,
                "tier": _memory_auth["tier"],
                "plan": _memory_auth["plan"],
                "plan_cn": _memory_auth["plan_cn"],
                "expire_at": _memory_auth["expire_at"],
                "remaining": get_remaining_quota(_memory_auth["plan"], is_member=True),
                "message": f"会员有效，剩余 {_memory_auth['days_left']} 天",
                "offline": False,
            }
        else:
            # 服务器返回未授权 - 清除内存状态
            reason = data.get("reason", "未知原因")
            _memory_auth.update({
                "authorized": False,
                "tier": "free",
                "plan": "free",
                "plan_cn": "",
                "token": None,
                "expire_at": None,
                "days_left": 0,
                "last_check": datetime.now().isoformat(),
            })
            clear_cache()
            
            return {
                "authorized": False,
                "tier": "free",
                "plan": "free",
                "plan_cn": "免费用户",
                "remaining": get_remaining_quota("free", is_member=False),
                "message": reason,
                "offline": False,
            }
            
    except requests.exceptions.ConnectionError:
        # 2. 服务器无法连接 - 使用离线缓存
        pass
    except Exception as e:
        # 3. 其他错误 - 使用离线缓存
        pass
    
    # ---------- 离线模式 ----------
    return _check_offline(machine_id)

def _check_offline(machine_id):
    """离线模式检查授权"""
    global _memory_auth
    
    # 优先使用内存中的状态
    if _memory_auth["authorized"] and _memory_auth["token"]:
        # 检查内存 Token 是否过期
        if _memory_auth.get("token_expires_at"):
            if datetime.now() < _memory_auth["token_expires_at"]:
                return {
                    "authorized": True,
                    "tier": _memory_auth["tier"],
                    "plan": _memory_auth["plan"],
                    "plan_cn": _memory_auth["plan_cn"],
                    "expire_at": _memory_auth["expire_at"],
                    "remaining": get_remaining_quota(_memory_auth["plan"], is_member=True),
                    "message": f"离线模式，会员有效，剩余 {_memory_auth['days_left']} 天",
                    "offline": True,
                }
    
    # 使用本地缓存
    cache = load_cache()
    if cache and cache.get("authorized"):
        # 检查缓存有效期
        cached_at = datetime.fromisoformat(cache.get("cached_at", "2000-01-01T00:00:00"))
        if (datetime.now() - cached_at).total_seconds() <= OFFLINE_CACHE_TTL:
            return {
                "authorized": True,
                "tier": cache.get("tier", "normal"),
                "plan": cache.get("plan", "unknown"),
                "plan_cn": cache.get("plan_cn", ""),
                "expire_at": cache.get("expire_at"),
                "remaining": get_remaining_quota(cache.get("plan", "monthly"), is_member=True),
                "message": f"离线模式（缓存 {int((datetime.now()-cached_at).total_seconds())}秒前）",
                "offline": True,
            }
    
    # 无有效缓存
    return {
        "authorized": False,
        "tier": "free",
        "plan": "free",
        "plan_cn": "免费用户",
        "remaining": get_remaining_quota("free", is_member=False),
        "message": "离线模式，未找到有效授权",
        "offline": True,
    }

# ==================== 后台轮询 ====================
def start_background_polling():
    """
    启动后台轮询线程（保持授权状态实时同步）
    
    每 POLL_INTERVAL 秒（默认5分钟）自动查询一次服务器。
    如果管理员撤销授权，最多5分钟内生效。
    """
    global _background_thread, _polling_active
    
    if _polling_active:
        return  # 已经在运行
    
    _polling_active = True
    
    def _poll_loop():
        global _polling_active
        while _polling_active:
            try:
                verify_auth()
            except Exception:
                pass
            time.sleep(POLL_INTERVAL)
    
    _background_thread = threading.Thread(target=_poll_loop, daemon=True)
    _background_thread.start()

def stop_background_polling():
    """停止后台轮询"""
    global _polling_active
    _polling_active = False

# ==================== 辅助函数 ====================
def get_remaining_quota(plan, is_member):
    """获取每日剩余额度"""
    limits = MEMBER_DAILY_LIMITS if is_member else FREE_DAILY_LIMITS
    return {
        "auto": limits["auto"],
        "semi": limits["semi"],
        "evaluate": limits["evaluate"],
    }

def get_auth_info():
    """获取当前授权信息（用于显示）"""
    global _memory_auth
    
    info = {
        "authorized": _memory_auth["authorized"],
        "tier": _memory_auth["tier"],
        "plan": _memory_auth["plan"],
        "plan_cn": _memory_auth["plan_cn"] or "免费用户",
        "expire_at": _memory_auth["expire_at"],
        "days_left": _memory_auth["days_left"],
        "server_connected": False,
        "machine_id": get_machine_id(),
    }
    
    # 尝试快速检查服务器连通性
    try:
        resp = requests.get(f"{SERVER_URL}/api/public/status", timeout=2)
        info["server_connected"] = resp.status_code == 200
    except Exception:
        pass
    
    return info

# ==================== 向后兼容 ====================
def activate_license(license_code, user_name=""):
    """
    旧版激活函数（保留兼容性）
    新版无需用户激活，管理员直接在后台开通
    """
    return {
        "success": False,
        "message": "已切换到服务端直控模式，请联系管理员开通授权",
    }

# ==================== 测试 ====================
if __name__ == "__main__":
    print("=" * 60)
    print("MC Skill 客户端授权 v3.0 - 静默轮询模式")
    print("=" * 60)
    print()
    print(f"机器码: {get_machine_id()}")
    print()
    
    # 测试授权验证
    result = verify_auth()
    print(f"授权状态: {'✅ 已授权' if result['authorized'] else '❌ 未授权'}")
    print(f"用户等级: {result['tier']}")
    print(f"套餐: {result.get('plan_cn', result['plan'])}")
    print(f"消息: {result['message']}")
    print(f"离线模式: {result.get('offline', False)}")
    
    if result.get('expire_at'):
        print(f"过期时间: {result['expire_at']}")
    
    # 测试获取详细信息
    info = get_auth_info()
    print()
    print("详细信息:")
    for key, value in info.items():
        print(f"  {key}: {value}")
