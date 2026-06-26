#!/usr/bin/env python3
"""
Kimi 用量查询脚本 - 安全版
查询 API 用量、额度、订阅信息
支持加密保存 Cookie
"""

import argparse
import json
import sys
import os
import base64
from datetime import datetime
from pathlib import Path

try:
    import requests
except ImportError:
    print("请先安装 requests: pip install requests")
    sys.exit(1)

# 尝试导入加密库
try:
    from cryptography.fernet import Fernet
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
    CRYPTO_AVAILABLE = True
except ImportError:
    CRYPTO_AVAILABLE = False
    print("警告: 未安装 cryptography，Cookie 将以明文存储")
    print("建议安装: pip install cryptography")

# Cookie 保存路径
CONFIG_DIR = Path.home() / ".config" / "kimi-quota"
COOKIE_FILE = CONFIG_DIR / "cookie.enc"
SALT_FILE = CONFIG_DIR / "salt"


def get_or_create_salt():
    """获取或创建 salt"""
    if SALT_FILE.exists():
        with open(SALT_FILE, "rb") as f:
            return f.read()
    else:
        salt = os.urandom(16)
        with open(SALT_FILE, "wb") as f:
            f.write(salt)
        os.chmod(SALT_FILE, 0o600)
        return salt


def get_key_from_env():
    """从环境变量获取加密密钥，或使用机器标识派生"""
    # 优先使用环境变量
    env_key = os.environ.get("KIMI_QUOTA_KEY")
    if env_key:
        return env_key.encode()
    
    # 否则使用机器标识派生密钥（不够安全但无需用户配置）
    import platform
    import getpass
    
    # 组合机器信息作为密码
    machine_id = f"{platform.node()}-{getpass.getuser()}-{platform.system()}"
    
    salt = get_or_create_salt()
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
    )
    return base64.urlsafe_b64encode(kdf.derive(machine_id.encode()))


def get_cipher():
    """获取加密器"""
    if not CRYPTO_AVAILABLE:
        return None
    key = get_key_from_env()
    return Fernet(key)


def save_cookie(cookie: str):
    """保存 Cookie 到文件（加密）"""
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    
    cipher = get_cipher()
    if cipher:
        # 加密存储
        encrypted = cipher.encrypt(cookie.encode())
        with open(COOKIE_FILE, "wb") as f:
            f.write(encrypted)
    else:
        # 明文存储（警告用户）
        with open(COOKIE_FILE, "w") as f:
            f.write(cookie)
    
    os.chmod(COOKIE_FILE, 0o600)  # 只有用户可读


def load_cookie():
    """从文件加载 Cookie（解密）"""
    if not COOKIE_FILE.exists():
        return None
    
    cipher = get_cipher()
    try:
        if cipher:
            with open(COOKIE_FILE, "rb") as f:
                encrypted = f.read()
            return cipher.decrypt(encrypted).decode()
        else:
            with open(COOKIE_FILE, "r") as f:
                return f.read().strip()
    except Exception:
        print("❌ 无法解密 Cookie，可能是在不同机器上保存的")
        print("提示: 设置环境变量 KIMI_QUOTA_KEY 使用相同密钥")
        return None


def clear_cookie():
    """清除保存的 Cookie"""
    if COOKIE_FILE.exists():
        COOKIE_FILE.unlink()
    if SALT_FILE.exists():
        SALT_FILE.unlink()


def extract_auth_token(cookie: str):
    """从 Cookie 中提取 authorization token"""
    for part in cookie.split(";"):
        if "kimi-auth=" in part:
            return part.split("kimi-auth=")[1].strip()
    return None


def get_subscription_data(cookie: str = None, token: str = None):
    """获取订阅信息"""
    url = "https://www.kimi.com/apiv2/kimi.gateway.order.v1.SubscriptionService/GetSubscription"
    
    headers = {
        "accept": "*/*",
        "accept-language": "zh-CN,zh;q=0.9",
        "content-type": "application/json",
        "origin": "https://www.kimi.com",
        "referer": "https://www.kimi.com/membership/subscription",
        "x-msh-platform": "web",
        "x-msh-version": "1.0.0",
        "x-language": "zh-CN",
        "r-timezone": "Asia/Shanghai",
    }
    
    auth_token = None
    if cookie:
        headers["cookie"] = cookie
        auth_token = extract_auth_token(cookie)
    elif token:
        auth_token = token
    
    if auth_token:
        headers["authorization"] = f"Bearer {auth_token}"
    else:
        return None
    
    try:
        response = requests.post(url, headers=headers, json={}, timeout=10)
        if response.status_code == 200:
            return response.json()
    except Exception:
        pass
    return None


def get_usage_data(cookie: str = None, token: str = None):
    """获取用量统计（通过 Billing API）"""
    url = "https://www.kimi.com/apiv2/kimi.gateway.billing.v1.BillingService/GetUsages"
    
    headers = {
        "accept": "*/*",
        "accept-language": "zh-CN,zh;q=0.9",
        "content-type": "application/json",
        "origin": "https://www.kimi.com",
        "referer": "https://www.kimi.com/code/console",
        "x-msh-platform": "web",
        "x-msh-version": "1.0.0",
        "x-language": "zh-CN",
        "r-timezone": "Asia/Shanghai",
    }
    
    auth_token = None
    if cookie:
        headers["cookie"] = cookie
        auth_token = extract_auth_token(cookie)
    elif token:
        auth_token = token
    
    if auth_token:
        headers["authorization"] = f"Bearer {auth_token}"
    else:
        return None
    
    try:
        response = requests.post(url, headers=headers, json={"scope": ["FEATURE_CODING"]}, timeout=10)
        if response.status_code == 200:
            return response.json()
    except Exception:
        pass
    return None


def format_report(sub_data: dict, usage_data: dict):
    """格式化报告"""
    result = []
    
    # 标题
    result.append("=" * 60)
    result.append("🌙 Kimi 用量报告")
    result.append("=" * 60)
    result.append(f"查询时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    result.append("")
    
    # API 用量
    result.append("-" * 60)
    result.append("📊 API 用量 (Kimi Code)")
    result.append("-" * 60)
    
    if usage_data and "usages" in usage_data:
        for usage in usage_data["usages"]:
            detail = usage.get("detail", {})
            limits = usage.get("limits", [])
            
            limit = detail.get("limit", "N/A")
            used = detail.get("used", "N/A")
            remaining = detail.get("remaining", "N/A")
            reset_time = detail.get("resetTime", "")
            
            # 计算百分比
            if limit != "N/A" and used != "N/A":
                percent = int(used) / int(limit) * 100
                result.append(f"本周用量: {percent:.0f}%")
            else:
                result.append(f"本周用量: {used}/{limit}")
            
            result.append(f"  └─ 已用: {used} 次, 剩余: {remaining} 次")
            
            if reset_time:
                reset_dt = datetime.fromisoformat(reset_time.replace('Z', '+00:00'))
                now = datetime.now(reset_dt.tzinfo)
                hours_left = (reset_dt - now).total_seconds() / 3600
                result.append(f"  └─ 重置: {hours_left:.0f} 小时后 ({reset_time[:10]})")
            
            # 频限明细
            if limits:
                for lim in limits:
                    window = lim.get("window", {})
                    lim_detail = lim.get("detail", {})
                    
                    duration = window.get("duration", 0)
                    time_unit = window.get("timeUnit", "")
                    
                    if duration and time_unit:
                        if time_unit == "TIME_UNIT_MINUTE":
                            window_str = f"{duration} 分钟"
                        elif time_unit == "TIME_UNIT_HOUR":
                            window_str = f"{duration} 小时"
                        else:
                            window_str = f"{duration} {time_unit}"
                        
                        lim_limit = lim_detail.get("limit", "N/A")
                        lim_remaining = lim_detail.get("remaining", "N/A")
                        lim_reset = lim_detail.get("resetTime", "")
                        
                        result.append(f"\n频限窗口: {window_str}")
                        result.append(f"  └─ 限额: {lim_limit}, 剩余: {lim_remaining}")
                        if lim_reset:
                            lim_reset_dt = datetime.fromisoformat(lim_reset.replace('Z', '+00:00'))
                            hours_left = (lim_reset_dt - now).total_seconds() / 3600
                            result.append(f"  └─ 重置: {hours_left:.0f} 小时后")
    else:
        result.append("⚠️  无法获取用量数据（需要登录 Cookie）")
    
    # 订阅信息
    if sub_data:
        subscription = sub_data.get("subscription", {})
        goods = subscription.get("goods", {})
        
        result.append("")
        result.append("-" * 60)
        result.append("📦 订阅套餐")
        result.append("-" * 60)
        result.append(f"套餐: {goods.get('title', 'N/A')}")
        result.append(f"等级: {sub_data.get('currentMembershipLevel', 'N/A')}")
        
        amounts = goods.get("amounts", [{}])[0]
        price_cents = amounts.get("priceInCents", 0)
        result.append(f"价格: ¥{int(price_cents)/100:.0f}/月")
        
        start_time = subscription.get("currentStartTime", "")
        end_time = subscription.get("currentEndTime", "")
        next_billing = subscription.get("nextBillingTime", "")
        
        if start_time:
            result.append(f"周期: {start_time[:10]} ~ {end_time[:10] if end_time else 'N/A'}")
        if next_billing:
            result.append(f"续费: {next_billing[:10]}")
        
        status = subscription.get("status", "")
        result.append(f"状态: {'✅ 活跃' if status == 'SUBSCRIPTION_STATUS_ACTIVE' else '❌ 非活跃'}")
        
        # 功能额度
        result.append("")
        result.append("-" * 60)
        result.append("🎯 功能额度")
        result.append("-" * 60)
        
        memberships = sub_data.get("memberships", [])
        features = {}
        
        for m in memberships:
            feature = m.get("feature", "")
            level = m.get("level", "")
            left = m.get("leftCount")
            total = m.get("totalCount")
            end = m.get("endTime", "")[:10] if m.get("endTime") else ""
            
            if feature not in features:
                features[feature] = []
            features[feature].append({
                "level": level,
                "left": left,
                "total": total,
                "end": end
            })
        
        feature_names = {
            "FEATURE_DEEP_RESEARCH": "🔍 深度研究",
            "FEATURE_OK_COMPUTER": "🤖 Agent",
            "FEATURE_NORMAL_SLIDES": "📊 PPT",
            "FEATURE_CODING": "💻 Code"
        }
        
        for feature_code, name in feature_names.items():
            if feature_code in features:
                for item in features[feature_code]:
                    level = "付费" if "INTERMEDIATE" in item["level"] else "免费"
                    if item["left"] is not None and item["total"] is not None:
                        result.append(f"{name}: {item['left']}/{item['total']} 次 ({level})")
                    else:
                        result.append(f"{name}: 无限 ({level})")
    else:
        result.append("")
        result.append("-" * 60)
        result.append("📦 订阅套餐")
        result.append("-" * 60)
        result.append("⚠️  无法获取订阅数据")
    
    result.append("")
    result.append("=" * 60)
    
    return "\n".join(result)


def main():
    parser = argparse.ArgumentParser(description="查询 Kimi 用量和额度")
    parser.add_argument("--cookie", help="Kimi 登录 Cookie (包含 kimi-auth)")
    parser.add_argument("--token", help="Kimi API Token")
    parser.add_argument("--save", action="store_true", help="保存 Cookie 供以后使用")
    parser.add_argument("--json", action="store_true", help="输出 JSON 格式")
    parser.add_argument("--clear", action="store_true", help="清除保存的 Cookie")
    
    args = parser.parse_args()
    
    # 清除 Cookie
    if args.clear:
        clear_cookie()
        print("✅ 已清除保存的 Cookie")
        return
    
    # 保存 Cookie
    if args.save and args.cookie:
        save_cookie(args.cookie)
        print("✅ Cookie 已保存到:", COOKIE_FILE)
        return
    
    # 确定使用哪个 Cookie/Token
    cookie = args.cookie
    token = args.token
    
    if not cookie and not token:
        # 尝试加载保存的 Cookie
        saved_cookie = load_cookie()
        if saved_cookie:
            cookie = saved_cookie
        else:
            print("❌ 错误: 没有提供 Cookie/Token，也没有保存的 Cookie")
            print("\n首次使用:")
            print("1. 登录 https://www.kimi.com")
            print("2. F12 打开开发者工具 → Application → Cookies → kimi-auth")
            print("3. 复制 Cookie 值")
            print(f"4. 运行: python3 {sys.argv[0]} --cookie \"kimi-auth=xxx\" --save")
            print("\n之后就可以直接运行:")
            print(f"   python3 {sys.argv[0]}")
            sys.exit(1)
    
    # 获取数据
    sub_data = get_subscription_data(cookie=cookie, token=token)
    usage_data = get_usage_data(cookie=cookie, token=token)
    
    if args.json:
        output = {
            "subscription": sub_data,
            "usage": usage_data,
            "timestamp": datetime.now().isoformat()
        }
        print(json.dumps(output, indent=2, ensure_ascii=False))
    else:
        print(format_report(sub_data, usage_data))


if __name__ == "__main__":
    main()
