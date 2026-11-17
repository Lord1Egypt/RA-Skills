# -*- coding: utf-8 -*-
"""授权管理模块 - 付费体系框架

功能：
1. 机器码生成 - 唯一标识用户设备
2. 使用次数计数 - 本地JSON存储，每日重置
3. 会员等级判断 - free / normal（premium 为"敬请期待"）
4. 60天免费期机制 - 首次使用算起60天内除移植评估外全部免费
5. 强制联网验证 - 每次使用Skill都验证授权状态
6. 使用数据上报 - 每3.5天自动上报一次
7. 请求签名机制 - 防止伪造请求和篡改数据
8. 配置完整性校验 - 检测关键配置是否被篡改

付费体系（V1）：
- 免费用户：全自动20次/日，半自动8次/日（免费期结束后自动应用）
- 普通会员：8.88元/月 | 23.88元/季 | 88.88元/年（连续包月）
- 高级会员：敬请期待（不开放）
- 单次按需：9.9/49.9/89.9/39.9元

免费期规则：
- 从首次使用当天算起60天
- 期间除"模组移植可行性评估报告"外所有功能免费
- "模组移植可行性评估报告"：首次免费，之后每天1次
- 60天后自动开启付费机制（免费用户20次/天，普通会员100次/天）
"""

import hashlib
import hmac
import json
import logging
import os
import platform
import secrets
import socket
import time
import uuid
from datetime import datetime, timedelta, date
from pathlib import Path
from typing import Any, Dict, Optional
from urllib.request import Request, urlopen
from urllib.error import URLError

from core.i18n import t

logger = logging.getLogger(__name__)

# === 付费全局开关 ===
# False = 付费机制未正式开启（仍限制次数，但显示友好提示）
# True  = 付费机制已正式开启（显示升级选项，允许购买会员）
# 注意：此开关只控制是否显示付费提示，不控制次数限制
# 次数限制在免费期结束后自动应用
ENABLE_PAYMENT = True

# === 🔒 配置完整性校验 (防篡改) ===
# 关键配置项的哈希签名。如果用户修改了服务器地址或开关，哈希不匹配会被检测到。
# 
# 部署流程:
#   1. 先修改下面的 AUTH_SERVER_URL 和 ENABLE_PAYMENT
#   2. 运行一次: python -c "from core.auth_manager import _compute_config_fingerprint; print(_compute_config_fingerprint())"
#   3. 将输出的指纹填入 CONFIG_FINGERPRINT
#   4. 这样用户如果篡改了关键配置就会被检测到
def _compute_config_fingerprint() -> str:
    """计算关键配置的指纹哈希（用于防篡改检测）"""
    fingerprint_src = f"{ENABLE_PAYMENT}|{AUTH_SERVER_URL}|v1-salt-mc"
    return hashlib.sha256(fingerprint_src.encode("utf-8")).hexdigest()[:16]

# ⚠️ 部署前请运行上面的函数，把真实指纹填到这里
# 当前 V1.0.4 配置指纹（基于 ENABLE_PAYMENT=True + AUTH_SERVER_URL="" 计算得到）
CONFIG_FINGERPRINT = os.environ.get(
    "MC_SKILL_CONFIG_FINGERPRINT",
    "f3fac2f31ff49470"  # "AUTO" = 自动计算首次运行（开发模式）。发布前必须改为固定值！
)

# === 🔐 客户端签名密钥 (与服务器 auth_server.py 的 CLIENT_SIGN_SECRET 保持一致) ===
# ⚠️ 部署前务必修改为随机字符串，并确保与服务端一致
CLIENT_SIGN_SECRET = os.environ.get(
    "MC_SKILL_SIGN_SECRET",
    "mc-skill-sign-key-2026-v3"  # ← 部署前修改为与服务端相同的随机字符串
)

# === 在线验证服务器 ===
# 管理员服务器地址（已内置，用户无需配置）
# 当前 V1.0.4 版本保持本地运行，云服务器部署计划推迟至下一个大版本更新
# 下一大版本部署时再修改为真实服务器地址："http://your-domain.com:8000" 或 "https://api.mc-skill.com"
#
# 如需临时覆盖（调试用），可设置环境变量 MC_SKILL_SERVER_URL
AUTH_SERVER_URL = os.environ.get(
    "MC_SKILL_SERVER_URL",
    ""  # ← V1.0.4 留空 = 不启用强制联网验证（与项目规划一致，下一大版本再填真实地址）
)
AUTH_SERVER_TIMEOUT = 10  # 超时秒数

# === 数据上报配置 ===
REPORT_INTERVAL_DAYS = 3.5  # 上报间隔：每3.5天上报一次（一周两次）
MAX_PENDING_RECORDS = 50   # 本地最多缓存的待上报记录数

# === 免费期天数 ===
FREE_PERIOD_DAYS = 60  # 首次使用后60天免费期

# === 会员等级 ===
TIER_FREE = "free"        # 免费用户
TIER_NORMAL = "normal"    # 普通会员 8.88元/月
TIER_PREMIUM = "premium"  # 高级会员（敬请期待，暂不开放）

# === 会员等级显示名称（通过 t() 动态获取翻译）===
_TIER_NAME_KEYS = {
    TIER_FREE: "auth.tier.free",
    TIER_NORMAL: "auth.tier.member",
    TIER_PREMIUM: "auth.tier.coming_soon",
}

def _get_tier_name(tier: str) -> str:
    """根据等级获取本地化名称"""
    return t(_TIER_NAME_KEYS.get(tier, "common.unknown"))

# === 功能类型 ===
FUNC_AUTO = "auto"        # 全自动功能（F2/F4/F7/F8等）
FUNC_SEMI = "semi"        # 半自动功能（F3/F6等）

# === 特殊功能：模组移植可行性评估报告 ===
# 免费期内：首次免费，之后每天1次
# 付费期后：免费用户每天1次，普通会员每天5次
SPECIAL_FEATURE_MIGRATION_ASSESS = "migration_assess"

# === 各等级次数限制（免费期结束后自动生效）===
DAILY_LIMITS = {
    TIER_FREE: {
        FUNC_AUTO: 20,       # 全自动每日20次
        FUNC_SEMI: 8,        # 半自动每日8次
        SPECIAL_FEATURE_MIGRATION_ASSESS: 1,  # 移植评估每天1次
    },
    TIER_NORMAL: {
        FUNC_AUTO: 100,      # 普通会员每日100次
        FUNC_SEMI: 50,       # 普通会员每日50次
        SPECIAL_FEATURE_MIGRATION_ASSESS: 5,  # 移植评估每天5次
    },
    # 高级会员敬请期待，不开放
}

# === 普通会员定价 ===
PRICING = {
    "monthly": {
        "name": t("auth.pricing_monthly"),
        "price": 8.88,
        "unit": "元/月",
        "desc": t("auth.pricing_desc_monthly"),
    },
    "monthly_auto": {
        "name": t("auth.pricing_monthly_auto"),
        "price": 8.88,
        "unit": "元/月",
        "desc": t("auth.pricing_desc_monthly_auto"),
    },
    "quarterly": {
        "name": t("auth.pricing_quarterly"),
        "price": 23.88,
        "unit": "元/季",
        "desc": t("auth.pricing_desc_quarterly"),
    },
    "yearly": {
        "name": t("auth.pricing_yearly"),
        "price": 88.88,
        "unit": "元/年",
        "desc": t("auth.pricing_desc_yearly"),
    },
}

# === 单次按需定价 ===
PAY_PER_USE = {
    "migration_assess": {"name": t("auth.per_use_migration_assess"), "price": 9.9},
    "shallow_adapt": {"name": t("auth.per_use_shallow_adapt"), "price": 49.9},
    "deep_diagnosis": {"name": t("auth.per_use_deep_diagnosis"), "price": 89.9},
    "crash_fix": {"name": t("auth.per_use_crash_fix"), "price": 39.9},
}

# === 作者测试设备列表 (仅这些设备会显示完整付费信息) ===
# 普通用户看不到单次按需付费（V1阶段还未实现），使整体更划算
_AUTHOR_MACHINE_IDS = [
    "5184c91c54610b2852a9369f68332286",  # 作者主设备
]


def _is_author_device() -> bool:
    """判断当前设备是否为作者测试设备"""
    # 方式1: 机器码匹配
    if _get_machine_id() in _AUTHOR_MACHINE_IDS:
        return True
    # 方式2: 环境变量 (AUTHOR_MODE=1)
    if os.environ.get("MC_SKILL_AUTHOR_MODE", "0") == "1":
        return True
    return False

# === 本地数据存储 ===
_DATA_DIR = Path(__file__).resolve().parent.parent / "data"
_AUTH_FILE = _DATA_DIR / "auth_state.json"


def _get_machine_id() -> str:
    """生成机器唯一标识码"""
    raw = ""
    try:
        raw += str(uuid.getnode())
    except Exception:
        pass
    try:
        raw += socket.gethostname()
    except Exception:
        pass
    try:
        raw += platform.system() + platform.machine()
    except Exception:
        pass
    return hashlib.md5(raw.encode("utf-8")).hexdigest()[:32]


def _default_auth_state() -> Dict[str, Any]:
    """默认授权状态"""
    return {
        "machine_id": _get_machine_id(),
        "tier": TIER_FREE,
        "license_key": "",
        "license_expires": "",
        "subscription_type": "",  # monthly / monthly_auto / quarterly / yearly
        "first_use_date": "",    # 首次使用日期（YYYY-MM-DD）
        "free_period_end": "",   # 免费期结束日期
        "daily_usage": {},
        "last_reset_date": datetime.now().strftime("%Y-%m-%d"),
        "total_usage": {},
        "migration_assess_first_used": False,  # 移植评估是否已使用过首次免费
        # === 强制联网验证相关 ===
        "server_token": "",          # 服务器返回的临时Token（有效期1小时）
        "server_token_expires": "",  # Token过期时间
        "last_online_check": "",     # 上次在线验证时间
        "online_verify_enabled": bool(AUTH_SERVER_URL),  # 是否启用强制联网验证
        # === 数据上报相关 ===
        "last_report_time": "",      # 上次成功上报时间
        "pending_reports": [],       # 待上报的数据记录列表
    }


def _check_and_downgrade_expired_license(state: Dict[str, Any]) -> bool:
    """检查授权是否过期，如果过期则自动降级为免费用户
    
    规则：
    - tier=normal 且 license_expires < 今天 → 降级为 TIER_FREE，清空授权相关字段
    - premium 过期同理
    - 返回值：True = 发生过降级（需要保存 state）
    """
    tier = state.get("tier", TIER_FREE)
    if tier == TIER_FREE:
        return False  # 本来就是免费，无需检查

    expires_str = state.get("license_expires", "")
    if not expires_str:
        # 有 tier 但没写过期时间（异常数据）→ 为保险起见不直接改，记录日志
        logger.warning(f"[授权降级] tier={tier} 但 license_expires 为空，跳过自动降级")
        return False

    try:
        expires_date = datetime.strptime(expires_str, "%Y-%m-%d").date()
    except Exception:
        logger.warning(f"[授权降级] license_expires='{expires_str}' 格式异常，跳过自动降级")
        return False

    today = date.today()
    if today > expires_date:
        # 授权已过期 → 自动降级回免费用户
        old_tier = tier
        state["tier"] = TIER_FREE
        state["license_key"] = ""
        state["license_expires"] = ""
        state["subscription_type"] = ""
        logger.info(f"[授权自动降级] tier={old_tier} → free，原因：license_expires={expires_str} < today={today}")
        return True

    return False  # 仍在有效期内


def _load_auth_state() -> Dict[str, Any]:
    """加载本地授权状态"""
    if not _AUTH_FILE.exists():
        return _default_auth_state()
    try:
        with open(_AUTH_FILE, "r", encoding="utf-8") as f:
            state = json.load(f)
        
        dirty = False  # 标记是否需要持久化
        
        # === 自动同步：根据当前配置更新强制验证开关 ===
        should_enable = bool(AUTH_SERVER_URL)
        if state.get("online_verify_enabled", False) != should_enable:
            state["online_verify_enabled"] = should_enable
            if should_enable:
                logger.info(f"[联网验证] 已自动启用，服务器地址: {AUTH_SERVER_URL}")
            dirty = True
        
        # === 授权过期 → 自动降级（防止用户授权过期后依旧享受 normal 次数）===
        if _check_and_downgrade_expired_license(state):
            dirty = True
        
        # === 检查是否需要重置每日计数 ===
        today = datetime.now().strftime("%Y-%m-%d")
        if state.get("last_reset_date") != today:
            state["daily_usage"] = {}
            state["last_reset_date"] = today
            dirty = True

        if dirty:
            _save_auth_state(state)
        return state
    except Exception as e:
        logger.warning(f"加载授权状态失败: {e}")
        return _default_auth_state()


def _save_auth_state(state: Dict[str, Any]) -> None:
    """保存授权状态到本地"""
    try:
        _DATA_DIR.mkdir(parents=True, exist_ok=True)
        with open(_AUTH_FILE, "w", encoding="utf-8") as f:
            json.dump(state, f, ensure_ascii=False, indent=2)
    except Exception as e:
        logger.warning(f"保存授权状态失败: {e}")


def _get_today_key() -> str:
    return datetime.now().strftime("%Y-%m-%d")


def _ensure_first_use_recorded(state: Dict[str, Any]) -> Dict[str, Any]:
    """确保首次使用日期已记录

    如果是首次使用，记录当天日期并设置60天后的免费期结束日期。
    同时显示机器码提示，让用户复制给AI Agent。
    """
    if not state.get("first_use_date"):
        today = date.today()
        state["first_use_date"] = today.strftime("%Y-%m-%d")
        free_end = today + timedelta(days=FREE_PERIOD_DAYS)
        state["free_period_end"] = free_end.strftime("%Y-%m-%d")
        _save_auth_state(state)
        logger.info(f"记录首次使用日期: {state['first_use_date']}, 免费期至: {state['free_period_end']}")
        
        # 显示首次使用欢迎提示和机器码
        machine_id = state.get("machine_id", "未知")
        print("\n" + "=" * 60)
        print("  🎉 欢迎使用 MC Skill！")
        print("=" * 60)
        print(f"\n  📍 您的机器码:")
        print(f"  {'─' * 50}")
        print(f"  {machine_id}")
        print(f"  {'─' * 50}")
        print(f"\n  ⚠️  重要提示:")
        print(f"  1. 请复制上面的机器码发给您的 AI Agent")
        print(f"  2. AI Agent 需要此机器码来管理您的授权")
        print(f"  3. 后续订阅套餐时也需要此机器码")
        print(f"  4. 请妥善保管，不要泄露给他人\n")
        print("=" * 60 + "\n")
        
        # 尝试自动复制到剪贴板（Windows）
        try:
            import subprocess
            import sys
            if sys.platform == "win32":
                subprocess.run("clip", input=machine_id, capture_output=True, text=True)
                print("  ✅ 机器码已自动复制到剪贴板\n")
        except Exception:
            print("  💡 请手动复制上面的机器码\n")
    
    return state


def is_in_free_period() -> bool:
    """判断当前是否在免费期内

    Returns:
        True = 在免费期内（前60天）
        False = 免费期已过，需要付费
    """
    state = _load_auth_state()
    state = _ensure_first_use_recorded(state)

    free_end_str = state.get("free_period_end", "")
    if not free_end_str:
        return True  # 没有记录结束日期，视为免费期

    try:
        free_end = datetime.strptime(free_end_str, "%Y-%m-%d").date()
        return date.today() <= free_end
    except Exception:
        return True


def get_free_period_info() -> Dict[str, Any]:
    """获取免费期信息"""
    state = _load_auth_state()
    state = _ensure_first_use_recorded(state)

    first_use = state.get("first_use_date", "")
    free_end_str = state.get("free_period_end", "")

    if not free_end_str:
        return {
            "in_free_period": True,
            "first_use_date": first_use,
            "free_period_end": "",
            "days_remaining": FREE_PERIOD_DAYS,
        }

    try:
        free_end = datetime.strptime(free_end_str, "%Y-%m-%d").date()
        today = date.today()
        # 使用 ceil 逻辑：最后一天显示剩余1天而不是0天
        days_remaining = (free_end - today).days
        if days_remaining <= 0 and today <= free_end:
            days_remaining = 1
        else:
            days_remaining = max(0, days_remaining)
        return {
            "in_free_period": today <= free_end,
            "first_use_date": first_use,
            "free_period_end": free_end_str,
            "days_remaining": days_remaining,
        }
    except Exception:
        return {
            "in_free_period": True,
            "first_use_date": first_use,
            "free_period_end": free_end_str,
            "days_remaining": FREE_PERIOD_DAYS,
        }


def get_current_tier() -> str:
    """获取当前会员等级"""
    state = _load_auth_state()
    return state.get("tier", TIER_FREE)


def get_machine_id() -> str:
    """获取当前机器码"""
    return _get_machine_id()


def get_usage_stats() -> Dict[str, Any]:
    """获取使用统计"""
    state = _load_auth_state()
    state = _ensure_first_use_recorded(state)
    tier = state.get("tier", TIER_FREE)
    daily = state.get("daily_usage", {})
    total = state.get("total_usage", {})
    limits = DAILY_LIMITS.get(tier, DAILY_LIMITS[TIER_FREE])
    free_info = get_free_period_info()

    return {
        "machine_id": state.get("machine_id", ""),
        "tier": tier,
        "tier_name": _get_tier_name(tier),
        "daily_usage": daily,
        "total_usage": total,
        "daily_limits": limits,
        "payment_enabled": ENABLE_PAYMENT,
        "license_key": state.get("license_key", ""),
        "license_expires": state.get("license_expires", ""),
        "subscription_type": state.get("subscription_type", ""),
        "first_use_date": state.get("first_use_date", ""),
        "free_period_end": state.get("free_period_end", ""),
        "in_free_period": free_info["in_free_period"],
        "days_remaining": free_info["days_remaining"],
        "pricing": PRICING,
        "premium_status": t("auth.tier.coming_soon"),
    }


def check_permission(feature: str, func_type: str = FUNC_AUTO) -> Dict[str, Any]:
    """检查功能使用权限

    权限判断逻辑：
    0. 配置完整性校验（防篡改）
    0.5. 强制联网验证（每次调用）
    1. 如果在免费期内（前60天）：
       - 移植评估功能：首次免费，之后每天1次
       - 其他功能：不限次数
    2. 如果免费期已过：
       - 自动应用基础限制（免费用户20次/天，普通会员100次/天）
       - ENABLE_PAYMENT 只控制是否显示付费提示和允许升级
    """
    # === 配置完整性校验（防篡改）===
    integrity = _verify_config_integrity()
    if not integrity["ok"]:
        # 检测到配置被篡改，直接拒绝（但免费期内仍保留降级）
        state = _load_auth_state()
        free_info = get_free_period_info()
        if not free_info["in_free_period"] and state.get("tier", TIER_FREE) == TIER_FREE:
            return {
                "allowed": False,
                "tier": TIER_FREE,
                "remaining": 0,
                "limit": 0,
                "reason": "⚠️ 检测到客户端配置被修改，请重新下载安装包！",
                "online": False,
                "_tampered": True,
            }
        logger.warning(integrity["message"])
    
    # === 强制联网验证 ===
    verify_result = _force_online_verify()
    if not verify_result.get("success"):
        # 联网验证失败，拒绝使用
        return {
            "allowed": False,
            "tier": TIER_FREE,
            "remaining": 0,
            "limit": 0,
            "reason": f"授权验证失败: {verify_result.get('reason', '未知错误')}",
            "online": verify_result.get("online", False),
        }
    
    state = _load_auth_state()
    state = _ensure_first_use_recorded(state)

    # === 特殊功能：模组移植可行性评估 ===
    if feature == SPECIAL_FEATURE_MIGRATION_ASSESS:
        return _check_migration_assess_permission(state)

    # === 免费期内：其他功能不限 ===
    free_info = get_free_period_info()
    if free_info["in_free_period"]:
        return {
            "allowed": True,
            "tier": state.get("tier", TIER_FREE),
            "remaining": -1,
            "limit": -1,
            "reason": t("auth.free_period_remaining", days=free_info['days_remaining']),
        }

    # === 免费期过后：自动应用基础限制 ===
    tier = state.get("tier", TIER_FREE)
    limits = DAILY_LIMITS.get(tier, DAILY_LIMITS[TIER_FREE])
    limit = limits.get(func_type, 20)

    daily = state.get("daily_usage", {})
    used = daily.get(feature, 0)

    if used >= limit:
        # 构建提示信息 + 触发支付页面
        if ENABLE_PAYMENT:
            upgrade_hint = t("auth.upgrade_hint_enable", max=100)
            payment_triggered = False
            try:
                from core.payment_page import show_payment_page
                page_reason = f"{t('auth.limit_reached', used=limit, limit=limit)}, {t('auth.upgrade_hint_enable', max=100)}"
                show_payment_page(reason=page_reason, mode="limit")
                payment_triggered = True
            except Exception:
                pass
            # reason 末段明确标注「已生成支付页面」，防止 AI Agent 忽略链接
            page_hint = t("auth.payment_page_generated") if payment_triggered else ""
            upgrade_hint = upgrade_hint + (f"，{page_hint}" if page_hint else "")
        else:
            upgrade_hint = t("auth.upgrade_hint_disable")
        return {
            "allowed": False,
            "tier": tier,
            "remaining": 0,
            "limit": limit,
            "reason": f"{t('auth.limit_reached', used=limit, limit=limit)}, {upgrade_hint}",
        }

    return {
        "allowed": True,
        "tier": tier,
        "remaining": limit - used,
        "limit": limit,
        "reason": "",
    }


def _check_migration_assess_permission(state: Dict[str, Any]) -> Dict[str, Any]:
    """检查模组移植可行性评估功能的权限

    规则：
    - 免费期内：首次免费，之后每天1次
    - 付费期后：免费用户每天1次，普通会员每天5次
    """
    free_info = get_free_period_info()
    tier = state.get("tier", TIER_FREE)

    # 首次使用免费
    first_used = state.get("migration_assess_first_used", False)
    today = _get_today_key()
    daily = state.get("daily_usage", {})
    today_used = daily.get(SPECIAL_FEATURE_MIGRATION_ASSESS, 0)

    if free_info["in_free_period"]:
        # 免费期内
        if not first_used:
            # 首次使用，免费
            return {
                "allowed": True,
                "tier": tier,
                "remaining": 1,
                "limit": 1,
                "reason": t("auth.migration_assess_first_free"),
                "is_first_use": True,
            }
        else:
            if today_used >= 1:
                return {
                    "allowed": False,
                    "tier": tier,
                    "remaining": 0,
                    "limit": 1,
                    "reason": t("auth.migration_assess_limit_reached", count=1),
                    "is_first_use": False,
                }
            return {
                "allowed": True,
                "tier": tier,
                "remaining": 1 - today_used,
                "limit": 1,
                "reason": t("auth.migration_assess_daily_free", count=1),
                "is_first_use": False,
            }
    else:
        # 付费期（免费期结束后自动应用限制）
        limits = DAILY_LIMITS.get(tier, DAILY_LIMITS[TIER_FREE])
        limit = limits.get(SPECIAL_FEATURE_MIGRATION_ASSESS, 1)

        if today_used >= limit:
            if ENABLE_PAYMENT:
                upgrade_hint = t("auth.upgrade_hint_enable", max=5)
                payment_triggered = False
                try:
                    from core.payment_page import show_payment_page
                    page_reason = f"{t('auth.limit_reached', used=limit, limit=limit)}, {t('auth.upgrade_hint_enable', max=5)}"
                    show_payment_page(reason=page_reason, mode="limit")
                    payment_triggered = True
                except Exception:
                    pass
                page_hint = t("auth.payment_page_generated") if payment_triggered else ""
                upgrade_hint = upgrade_hint + (f"，{page_hint}" if page_hint else "")
            else:
                upgrade_hint = t("auth.upgrade_hint_disable")
            return {
                "allowed": False,
                "tier": tier,
                "remaining": 0,
                "limit": limit,
                "reason": f"{t('auth.limit_reached', used=limit, limit=limit)}, {upgrade_hint}",
                "is_first_use": not first_used,
            }

        return {
            "allowed": True,
            "tier": tier,
            "remaining": limit - today_used,
            "limit": limit,
            "reason": "",
            "is_first_use": not first_used,
        }


def record_usage(feature: str) -> None:
    """记录一次功能使用（含数据上报）"""
    state = _load_auth_state()
    state = _ensure_first_use_recorded(state)
    daily = state.get("daily_usage", {})
    total = state.get("total_usage", {})

    daily[feature] = daily.get(feature, 0) + 1
    total[feature] = total.get(feature, 0) + 1

    # 移植评估特殊：标记首次使用
    if feature == SPECIAL_FEATURE_MIGRATION_ASSESS:
        state["migration_assess_first_used"] = True

    state["daily_usage"] = daily
    state["total_usage"] = total
    _save_auth_state(state)

    logger.debug(f"记录使用: {feature}, 今日={daily[feature]}, 总计={total[feature]}")
    
    # === 数据上报（本地缓存，每3.5天统一上报一次）===
    _report_usage_data(feature, 1)


def activate_license(license_key: str, tier: str = TIER_NORMAL,
                     expires: str = "", subscription_type: str = "monthly") -> Dict[str, Any]:
    """激活授权码（支持续费叠加兜底，防止管理员误发短日期授权码导致用户损失）

    规则：
    1. 如果用户当前已是付费会员且旧授权仍有效 → 取「旧 expires 与 新 expires」的较大者
       （例如用户年卡还剩 100 天，续费月卡 30 天 → 最终为 年卡原过期日，不会 30 天后过期）
    2. 如果旧授权已过期 / 本来就是免费用户 → 直接采用新 expires
    3. 真正的「精确续费天数叠加」逻辑在管理员服务端生成授权码时计算，
       客户端这里只是做兜底，不反向延长服务端下发的日期。

    Args:
        license_key: 授权码
        tier: 会员等级（目前仅支持 normal，premium 为敬请期待）
        expires: 过期时间（YYYY-MM-DD），由管理员服务端计算后下发
        subscription_type: 订阅类型 monthly/monthly_auto/quarterly/yearly
    """
    if tier == TIER_PREMIUM:
        return {
            "success": False,
            "tier": tier,
            "message": t("auth.premium_coming_soon"),
        }

    state = _load_auth_state()

    # === 续费兜底：旧 expires（若仍有效）和 新 expires 取较大者 ===
    final_expires = expires
    old_expires_str = state.get("license_expires", "")
    old_tier = state.get("tier", TIER_FREE)
    today_date = date.today()
    try:
        if old_expires_str and old_tier != TIER_FREE:
            old_expires_date = datetime.strptime(old_expires_str, "%Y-%m-%d").date()
            # 旧授权仍然有效（还没过期）
            if old_expires_date >= today_date:
                new_expires_date = datetime.strptime(expires, "%Y-%m-%d").date()
                if old_expires_date > new_expires_date:
                    # 旧的有效期比新的更长 → 采用旧的（保护用户权益，比如误发了更短的码）
                    final_expires = old_expires_str
                    logger.info(
                        f"[授权激活] 续费兜底：旧 expires({old_expires_str}) > 新 expires({expires})，"
                        f"保留较晚的日期 {final_expires}"
                    )
    except Exception as e:
        logger.warning(f"[授权激活] 续费兜底计算异常，直接采用新 expires={expires}: {e}")

    state["tier"] = tier
    state["license_key"] = license_key
    state["license_expires"] = final_expires
    state["subscription_type"] = subscription_type

    _save_auth_state(state)
    logger.info(f"授权激活成功: tier={tier}, expires={final_expires}, sub={subscription_type}")

    sub_name = PRICING.get(subscription_type, {}).get("name", subscription_type)
    return {
        "success": True,
        "tier": tier,
        "license_key": license_key,
        "expires": final_expires,
        "subscription_type": subscription_type,
        "message": t("auth.activate_success", tier=_get_tier_name(tier), subscription=sub_name, expires=final_expires),
    }


def verify_license_online(license_key: str) -> Dict[str, Any]:
    """在线验证授权码（预留接口）"""
    if not AUTH_SERVER_URL:
        logger.info("未配置在线验证服务器，使用本地验证")
        return {
            "success": False,
            "online": False,
            "reason": "在线验证服务暂未开放，请使用本地激活",
        }

    try:
        from urllib.request import Request, urlopen
        req_data = json.dumps({
            "license_key": license_key,
            "machine_id": _get_machine_id(),
        }).encode("utf-8")

        req = Request(
            f"{AUTH_SERVER_URL}/verify",
            data=req_data,
            headers={
                "Content-Type": "application/json",
                "User-Agent": "MC-Skill-V1/1.0",
            },
            method="POST",
        )

        with urlopen(req, timeout=AUTH_SERVER_TIMEOUT) as resp:
            result = json.loads(resp.read().decode("utf-8"))
            return result

    except Exception as e:
        logger.error(f"在线验证失败: {e}")
        return {
            "success": False,
            "online": True,
            "reason": f"验证服务连接失败: {str(e)}",
        }


# ==================== 🔐 签名 HTTP 请求 ====================

def _compute_sign(data_str: str, timestamp: str, nonce: str) -> str:
    """
    计算请求签名 (与服务器 auth_server.py 中的 compute_sign 保持一致)
    
    签名算法: HMAC-SHA256(CLIENT_SIGN_SECRET, timestamp + nonce + data_str)
    """
    message = f"{timestamp}{nonce}{data_str}"
    return hmac.new(
        CLIENT_SIGN_SECRET.encode("utf-8"),
        message.encode("utf-8"),
        hashlib.sha256
    ).hexdigest()


def _signed_post(path: str, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """
    发送带签名的 POST 请求到服务器
    
    自动附加签名头:
      - x-timestamp: 当前时间戳（秒）
      - x-nonce:     随机字符串（防止重放）
      - x-sign:      HMAC-SHA256 签名
    
    Args:
        path: 接口路径，如 "/api/auth/quick-check"
        data: 请求体字典
    
    Returns:
        服务器响应的 JSON 字典，失败返回 None
    """
    if not AUTH_SERVER_URL:
        return None
    
    now_ts = str(int(time.time()))
    nonce = secrets.token_hex(8)
    data_str = json.dumps(data, ensure_ascii=False)
    
    # 计算签名
    sign = _compute_sign(data_str, now_ts, nonce)
    
    req_data = data_str.encode("utf-8")
    req = Request(
        f"{AUTH_SERVER_URL}{path}",
        data=req_data,
        headers={
            "Content-Type": "application/json",
            "User-Agent": "MC-Skill-V1/1.0",
            "x-timestamp": now_ts,
            "x-nonce": nonce,
            "x-sign": sign,
        },
        method="POST",
    )
    
    with urlopen(req, timeout=AUTH_SERVER_TIMEOUT) as resp:
        return json.loads(resp.read().decode("utf-8"))


# ==================== 🔒 配置防篡改检测 ====================

def _verify_config_integrity() -> Dict[str, Any]:
    """
    校验关键配置是否被篡改
    
    检测内容:
      1. ENABLE_PAYMENT 开关是否被修改
      2. AUTH_SERVER_URL 是否被替换
      3. CONFIG_FINGERPRINT 是否匹配
    
    Returns:
        {"ok": bool, "tampered_fields": list, "message": str}
    """
    result = {
        "ok": True,
        "tampered_fields": [],
        "message": "配置完整性校验通过",
    }
    
    # AUTO 模式（开发环境），跳过校验
    if CONFIG_FINGERPRINT == "AUTO":
        return result
    
    # 计算当前指纹并与预设比较
    current_fp = _compute_config_fingerprint()
    if current_fp != CONFIG_FINGERPRINT:
        result["ok"] = False
        result["tampered_fields"].append("global_config")
        result["message"] = (
            f"⚠️  检测到关键配置被篡改！"
            f"预期指纹: {CONFIG_FINGERPRINT[:8]}... "
            f"实际指纹: {current_fp[:8]}..."
        )
        logger.warning(result["message"])
    
    return result


# ==================== 强制联网验证与数据上报 ====================

def _force_online_verify() -> Dict[str, Any]:
    """强制联网验证（每次使用Skill时调用）
    
    流程：
    1. 检查本地Token是否有效（有效期1小时）
    2. Token无效则请求服务器获取新Token
    3. 返回验证结果（成功/失败/离线降级）
    
    Returns:
        {
            "success": bool,      # 验证是否通过
            "online": bool,       # 是否在线模式
            "tier": str,          # 服务器确认的会员等级
            "reason": str,        # 失败原因（如有）
        }
    """
    state = _load_auth_state()
    machine_id = state.get("machine_id", "")
    
    # 检查是否启用了强制联网验证
    if not state.get("online_verify_enabled", False) or not AUTH_SERVER_URL:
        return {
            "success": True,
            "online": False,
            "tier": state.get("tier", TIER_FREE),
            "reason": "离线模式（未启用强制验证）",
        }
    
    # 检查本地Token是否有效
    token_expires = state.get("server_token_expires", "")
    now = datetime.now()
    
    if token_expires:
        try:
            expires_time = datetime.fromisoformat(token_expires)
            if now < expires_time:
                # Token仍有效，直接使用
                logger.debug(f"使用有效Token: 过期时间 {token_expires}")
                return {
                    "success": True,
                    "online": True,
                    "tier": state.get("tier", TIER_FREE),
                    "reason": "",
                }
        except ValueError:
            pass
    
    # Token无效，请求服务器获取新Token（使用签名请求）
    try:
        # 使用带签名的请求
        result = _signed_post("/api/auth/quick-check", {
            "machine_id": machine_id,
            "timestamp": now.isoformat(),
        })
        
        if result is None:
            raise URLError("签名请求失败")
            
        # 服务器响应成功（无论是否授权）
        server_success = result.get("success") or result.get("authorized") is not None
        
        if server_success:
            # 更新本地Token（如果有）
            if result.get("token"):
                state["server_token"] = result.get("token", "")
                state["server_token_expires"] = result.get("expires", "")
            
            state["last_online_check"] = now.isoformat()
            
            # 检查是否授权
            if result.get("authorized"):
                # 同步服务器端的会员等级
                server_tier = result.get("tier", "")
                if server_tier and server_tier != state.get("tier"):
                    state["tier"] = server_tier
                    logger.info(f"服务器同步会员等级: {server_tier}")
                
                _save_auth_state(state)
                
                return {
                    "success": True,
                    "online": True,
                    "tier": state.get("tier", TIER_FREE),
                    "reason": "",
                }
            else:
                # 服务器连接成功，但用户未授权
                _save_auth_state(state)
                return {
                    "success": False,
                    "online": True,
                    "tier": TIER_FREE,
                    "reason": result.get("reason", "服务器验证失败"),
                }
        else:
            # 服务器返回失败
            return {
                "success": False,
                "online": True,
                "tier": TIER_FREE,
                "reason": result.get("message") or result.get("reason", "服务器验证失败"),
            }
                
    except (URLError, OSError) as e:
        # 网络连接失败，降级处理
        logger.warning(f"联网验证失败，降级为离线模式: {e}")
        state["last_online_check"] = now.isoformat()
        _save_auth_state(state)
        
        # 检查是否允许离线使用（免费期内或有本地授权）
        local_tier = state.get("tier", TIER_FREE)
        free_info = get_free_period_info()
        
        if free_info.get("in_free_period") or local_tier != TIER_FREE:
            # 免费期内或已有本地授权，允许离线使用
            return {
                "success": True,
                "online": False,
                "tier": local_tier,
                "reason": f"网络不可用，降级离线模式（{str(e)[:50]}）",
            }
        else:
            # 免费期已过且无本地授权，拒绝使用
            return {
                "success": False,
                "online": False,
                "tier": TIER_FREE,
                "reason": f"网络不可用，无法验证授权（{str(e)[:50]}）",
            }
    except Exception as e:
        logger.error(f"联网验证异常: {e}")
        return {
            "success": False,
            "online": False,
            "tier": TIER_FREE,
            "reason": f"验证异常: {str(e)[:50]}",
        }


def _should_report() -> bool:
    """检查是否应该上报数据（每3.5天一次，即一周两次）"""
    state = _load_auth_state()
    last_report = state.get("last_report_time", "")
    
    if not last_report:
        # 从未上报过，应该立即上报
        return True
    
    try:
        last_time = datetime.fromisoformat(last_report)
        now = datetime.now()
        interval = timedelta(days=REPORT_INTERVAL_DAYS)
        return (now - last_time) >= interval
    except (ValueError, TypeError):
        return True


def _report_usage_data(feature: str, usage_count: int) -> None:
    """上报使用数据到管理员服务器
    
    机制：
    1. 每次使用Skill时调用
    2. 本地缓存使用数据
    3. 每3.5天统一上报一次（一周两次）
    4. 上报成功后清除缓存
    
    Args:
        feature: 使用的功能名称
        usage_count: 本次使用次数（通常为1）
    """
    state = _load_auth_state()
    now = datetime.now()
    
    # 添加新的使用记录到本地缓存
    pending = state.get("pending_reports", [])
    pending.append({
        "feature": feature,
        "count": usage_count,
        "timestamp": now.isoformat(),
    })
    
    # 如果缓存超过最大限制，保留最近的记录
    if len(pending) > MAX_PENDING_RECORDS:
        pending = pending[-MAX_PENDING_RECORDS:]
    
    state["pending_reports"] = pending
    
    # 检查是否应该立即上报
    if _should_report() and AUTH_SERVER_URL:
        _do_report(state)
    else:
        # 只是保存缓存
        _save_auth_state(state)


def _do_report(state: Dict[str, Any]) -> None:
    """执行数据上报（使用签名请求）"""
    pending = state.get("pending_reports", [])
    
    if not pending:
        return
    
    try:
        machine_id = state.get("machine_id", "")
        now = datetime.now()
        
        # 准备上报数据
        report_data = {
            "machine_id": machine_id,
            "report_time": now.isoformat(),
            "usage_records": pending,
            "stats": {
                "tier": state.get("tier", TIER_FREE),
                "total_usage": state.get("total_usage", {}),
                "first_use_date": state.get("first_use_date", ""),
            }
        }
        
        # 使用带签名的请求发送到服务器
        result = _signed_post("/api/auth/report-usage", report_data)
        
        if result is None:
            raise URLError("签名请求失败")
        
        if result.get("success"):
            # 上报成功，清除缓存
            state["pending_reports"] = []
            state["last_report_time"] = now.isoformat()
            _save_auth_state(state)
            logger.info(f"使用数据上报成功: {len(pending)} 条记录")
        else:
            logger.warning(f"数据上报失败: {result.get('message', '未知错误')}")
            _save_auth_state(state)  # 保存缓存，下次再试
            
    except Exception as e:
        logger.warning(f"数据上报异常: {e}")
        # 上报失败，保留缓存等待下次
    
    # 保存当前状态
    _save_auth_state(state)


def get_report_status() -> Dict[str, Any]:
    """获取数据上报状态（供管理员查看）"""
    state = _load_auth_state()
    return {
        "last_report_time": state.get("last_report_time", ""),
        "pending_count": len(state.get("pending_reports", [])),
        "should_report": _should_report(),
        "server_url": AUTH_SERVER_URL or "未配置",
        "online_verify_enabled": state.get("online_verify_enabled", False),
    }


def reset_usage() -> None:
    """重置使用计数（调试用）"""
    state = _load_auth_state()
    state["daily_usage"] = {}
    state["total_usage"] = {}
    state["last_reset_date"] = _get_today_key()
    _save_auth_state(state)
    logger.info("使用计数已重置")


def set_tier(tier: str) -> None:
    """设置会员等级（调试/管理用）"""
    state = _load_auth_state()
    state["tier"] = tier
    _save_auth_state(state)
    logger.info(f"会员等级已设置为: {tier}")


def reset_free_period() -> None:
    """重置免费期（调试用，清除首次使用日期）"""
    state = _load_auth_state()
    state["first_use_date"] = ""
    state["free_period_end"] = ""
    state["migration_assess_first_used"] = False
    _save_auth_state(state)
    logger.info("免费期已重置")


def enable_payment() -> None:
    """启用付费限制（全局）"""
    global ENABLE_PAYMENT
    ENABLE_PAYMENT = True
    logger.info("付费限制已启用")


def disable_payment() -> None:
    """禁用付费限制（全局）"""
    global ENABLE_PAYMENT
    ENABLE_PAYMENT = False
    logger.info("付费限制已禁用")


def print_auth_status() -> None:
    """打印当前授权状态"""
    stats = get_usage_stats()
    print("=" * 55, flush=True)
    print(f"  {t('banner.title')} - {t('auth.title')}", flush=True)
    print("=" * 55, flush=True)
    print(f"  {t('auth.machine_id')}: {stats['machine_id']}", flush=True)
    print(f"  {t('auth.member_tier')}: {stats['tier_name']}", flush=True)
    print(f"  {t('auth.payment_methods')}: {'✅' if stats['payment_enabled'] else '⏳'}", flush=True)
    print(f"  {t('auth.auth_code')}: {stats['license_key'] or t('auth.not_activated')}", flush=True)
    print(f"  {t('auth.expiry_date')}: {stats['license_expires'] or '—'}", flush=True)

    # 免费期信息
    if stats["in_free_period"]:
        print(f"\n  ┌─────────────────────────────────", flush=True)
        print(f"  │  {t('auth.free_period')} ({t('auth.remaining')} {stats['days_remaining']} days)", flush=True)
        print(f"  │  {t('auth.first_use_date')}: {stats['first_use_date'] or '—'}", flush=True)
        print(f"  │  {t('auth.free_until')}: {stats['free_period_end'] or '—'}", flush=True)
        print(f"  └─────────────────────────────────", flush=True)
    else:
        print(f"\n  ┌─────────────────────────────────", flush=True)
        print(f"  │  {t('auth.free_period')}: {t('auth.expired')} ({stats['free_period_end']})", flush=True)
        print(f"  │  {t('auth.tier.free')}: {stats['daily_limits'].get('auto', 20)}/day", flush=True)
        print(f"  └─────────────────────────────────", flush=True)

    # 使用统计
    print(f"\n  {t('auth.today_usage')}:", flush=True)
    for feat, count in stats["daily_usage"].items():
        feat_name = {"migration_assess": t("feature.f9.name")}.get(feat, feat)
        limit = stats["daily_limits"].get(feat, stats["daily_limits"].get("auto", 20))
        if limit > 0:
            print(f"    {feat_name}: {count}/{limit}", flush=True)
        else:
            print(f"    {feat_name}: {count} ({t('auth.unlimited')})", flush=True)
    if not stats["daily_usage"]:
        print(f"    ({t('common.no_data')})", flush=True)

    print(f"\n  {t('auth.total_usage')}:", flush=True)
    for feat, count in stats["total_usage"].items():
        feat_name = {"migration_assess": t("feature.f9.name")}.get(feat, feat)
        print(f"    {feat_name}: {count}", flush=True)
    if not stats["total_usage"]:
        print(f"    ({t('common.no_data')})", flush=True)

    # 定价信息
    print(f"\n  {t('auth.member_subscription')}:", flush=True)
    for key, info in stats["pricing"].items():
        print(f"    {info['name']}: {info['price']}{info['unit']} ({info['desc']})", flush=True)

    # 单次按需付费：仅作者设备可见（V1阶段功能未实现，对普通用户隐藏）
    if _is_author_device():
        print(f"\n  {t('auth.per_use_payment')} {t('auth.author_test_only')}:", flush=True)
        for key, info in PAY_PER_USE.items():
            print(f"    {info['name']}: {info['price']} CNY/use", flush=True)

    print(f"\n  {t('auth.premium_coming_soon')}", flush=True)
    print("=" * 55, flush=True)


def get_auth_status_json() -> Dict[str, Any]:
    """获取授权状态（JSON格式，供API调用）

    Returns:
        包含完整授权信息的字典，结构与 get_usage_stats() 一致
    """
    stats = get_usage_stats()
    # 添加额外的可用信息
    stats["payment_enabled"] = ENABLE_PAYMENT
    stats["auth_server_url"] = AUTH_SERVER_URL
    stats["free_period_days"] = FREE_PERIOD_DAYS
    return stats


def get_available_plans() -> Dict[str, Any]:
    """获取可用套餐列表（供API调用和命令行显示）

    Returns:
        {
            "plans": {...},          # 普通会员订阅套餐
            "per_use": {...} | None, # 单次按需付费（仅作者设备可见）
            "premium_coming_soon": bool,  # 高级会员是否敬请期待
            "tier_info": {...},      # 各等级说明
            "daily_limits": {...},   # 各等级每日限制
        }
    """
    is_author = _is_author_device()

    tier_info = {
        TIER_FREE: {
            "name": _get_tier_name(TIER_FREE),
            "desc": "免费用户",
            "daily_limits": DAILY_LIMITS.get(TIER_FREE, {}),
        },
        TIER_NORMAL: {
            "name": _get_tier_name(TIER_NORMAL),
            "desc": "普通会员",
            "daily_limits": DAILY_LIMITS.get(TIER_NORMAL, {}),
        },
        TIER_PREMIUM: {
            "name": _get_tier_name(TIER_PREMIUM),
            "desc": "敬请期待",
            "coming_soon": True,
        },
    }

    result = {
        "plans": PRICING,
        "per_use": PAY_PER_USE if is_author else None,
        "premium_coming_soon": True,
        "tier_info": tier_info,
        "daily_limits": DAILY_LIMITS,
        "free_period_days": FREE_PERIOD_DAYS,
        "payment_enabled": ENABLE_PAYMENT,
    }
    return result


def print_available_plans() -> None:
    """打印可用套餐列表（命令行格式）"""
    plans = get_available_plans()
    is_author = plans["per_use"] is not None

    print("=" * 60, flush=True)
    print(f"  {t('banner.title')} - 套餐列表", flush=True)
    print("=" * 60, flush=True)

    # 会员等级说明
    print(f"\n  📊 会员等级说明:", flush=True)
    for tier_key, tier_info in plans["tier_info"].items():
        if tier_info.get("coming_soon"):
            print(f"    {tier_info['name']}: {tier_info['desc']}", flush=True)
        else:
            limits = tier_info.get("daily_limits", {})
            auto_limit = limits.get(FUNC_AUTO, "-")
            semi_limit = limits.get(FUNC_SEMI, "-")
            migrate_limit = limits.get(SPECIAL_FEATURE_MIGRATION_ASSESS, "-")
            print(f"    {tier_info['name']}: 全自动{auto_limit}次/天, 半自动{semi_limit}次/天, 移植评估{migrate_limit}次/天", flush=True)

    # 免费期说明
    print(f"\n  🎁 免费期: 首次使用起 {plans['free_period_days']} 天内，除移植评估外所有功能不限次数", flush=True)

    # 普通会员套餐
    print(f"\n  💎 {t('auth.member_subscription')}:", flush=True)
    for key, info in plans["plans"].items():
        print(f"    [{key}] {info['name']}: {info['price']}{info['unit']}  —  {info['desc']}", flush=True)

    # 单次按需付费（仅作者设备）
    if is_author:
        print(f"\n  ⚡ 单次按需付费 {t('auth.author_test_only')}:", flush=True)
        for key, info in plans["per_use"].items():
            print(f"    [{key}] {info['name']}: {info['price']} 元/次", flush=True)

    # 高级会员
    if plans["premium_coming_soon"]:
        print(f"\n  🌟 {t('auth.premium_coming_soon')}", flush=True)

    # 付款状态
    if plans["payment_enabled"]:
        print(f"\n  ✅ 付费系统已启用", flush=True)
    else:
        print(f"\n  ⏳ 付费系统即将开放，当前仍可享受免费使用", flush=True)

    print("=" * 60, flush=True)
