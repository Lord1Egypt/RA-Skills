#!/usr/bin/env python3
"""
京东 ClawTip 支付验证模块 (v3.0 - 标准 ClawTip 架构版)

采用 ClawTip 本地订单流架构：
- Phase 1: 脚本创建订单 JSON 到标准路径 (~/.openclaw/skills/orders/{indicator}/)
- Phase 2: ClawTip Agent 读取订单，完成支付，回写 payCredential
- Phase 3: 脚本读取 payCredential 并 SM4 验证

订单路径: ~/.openclaw/skills/orders/{indicator}/{order_no}.json
  indicator = md5(slug).hexdigest()
"""

import os
import sys
import json
import time
import uuid
import hashlib
import base64
import shutil
from datetime import datetime

# ======================== 核心配置 ========================
_SKILL_SLUG = "libu-premarket"
_SKILL_DISPLAY_NAME = "礼部侍郎-A股盘前作战地图"

# SM4 密钥 (Base64, 16字节) - 由京东邮件提供
# 🚨 安全修复: 移除硬编码默认值，延迟到实际使用时检查
_SM4_KEY_BASE64 = os.environ.get("CLAWTIP_SM4_KEY")

# ClawTip 收款服务ID (payTo) - base64编码，防肉眼直接提取
# 注意: 实际值通过 base64 解码 _PAY_TO_B64 获得，不在注释中明文存储
_PAY_TO_B64 = "ODVhZTg5NWMxYTA4YTdlMmVmZTVmMThiNzM5ZTMzMzcyMDI2MDQxODE0MjIyODAwMjAwMDY5ODhERnRtclNBdkdoRWFacDNsemtrcGJuS29mWFRnQnNmc1I2aWF6ek9iQnY0anF5akNzcjk4ZlZDZjRsUldEUmp0eXFaTVFpQVk="
_PAY_TO = base64.b64decode(_PAY_TO_B64).decode("utf-8")


def _require_sm4_key():
    """延迟校验 SM4 密钥，避免 import 时直接崩溃"""
    key = os.environ.get("CLAWTIP_SM4_KEY") or _SM4_KEY_BASE64
    if not key:
        print("[支付] 🚨 CLAWTIP_SM4_KEY 未设置")
        print("[支付] 💡 export CLAWTIP_SM4_KEY='你的SM4密钥'")
        sys.exit(1)
    return key

# 标准订单路径: ~/.openclaw/skills/orders/{indicator}/
_OPENCLAW_BASE = os.path.expanduser("~/.openclaw")
_INDICATOR = hashlib.md5(_SKILL_SLUG.encode("utf-8")).hexdigest()
_ORDER_DIR = os.path.join(_OPENCLAW_BASE, "skills", "orders", _INDICATOR)

# 降级: 兼容旧路径 (slug-based)
_ORDER_DIR_LEGACY = os.path.expanduser(os.path.join("~/.openclaw/skills/orders", _SKILL_SLUG))

# SKU 定价
_SKU_CONFIG = {
    "sku_once":    {"name": "单次体验", "price": 0.8,  "cents": 80},
    "sku_monthly": {"name": "月度订阅", "price": 9.9,  "cents": 990},
}


# ======================== 工具函数 ========================

def _sm4_encrypt(plain_dict: dict) -> str:
    """
    使用 SM4-ECB 加密订单数据，生成 encrypted_data
    对应官方 Java: SM4EncryptionUtils.encrypt(plainText, Base64.decode(sm4Key))
    Hutool 的 sm4.encryptBase64() 等价于 SM4-ECB + PKCS7 Padding + Base64
    """
    from gmssl.sm4 import CryptSM4, SM4_ENCRYPT
    key_bytes = base64.b64decode(_require_sm4_key())
    plain_bytes = json.dumps(plain_dict, ensure_ascii=False).encode("utf-8")
    # PKCS7 Padding
    pad_len = 16 - (len(plain_bytes) % 16)
    padded = plain_bytes + bytes([pad_len] * pad_len)
    crypt = CryptSM4()
    crypt.set_key(key_bytes, SM4_ENCRYPT)
    encrypted = crypt.crypt_ecb(padded)
    return base64.b64encode(encrypted).decode("utf-8")


def _migrate_legacy_orders():
    """迁移旧路径订单到标准 indicator 路径 (仅迁移格式兼容的)"""
    if os.path.exists(_ORDER_DIR_LEGACY):
        os.makedirs(_ORDER_DIR, exist_ok=True)
        migrated = 0
        for f in os.listdir(_ORDER_DIR_LEGACY):
            if not f.endswith('.json'):
                continue
            src = os.path.join(_ORDER_DIR_LEGACY, f)
            try:
                with open(src) as fh:
                    data = json.load(fh)
                # Skip old format orders that lack standard fields
                if 'order_no' not in data and 'skill-id' not in data:
                    # 删除不兼容的旧订单
                    os.remove(src)
                    print(f"[支付] 🗑️ 已清理不兼容的旧订单: {f}")
                    continue
                dst = os.path.join(_ORDER_DIR, f)
                if not os.path.exists(dst):
                    shutil.copy2(src, dst)
                    migrated += 1
            except:
                pass
        if migrated > 0:
            print(f"[支付] 📦 已迁移 {migrated} 个兼容订单到标准路径")


def _ensure_order_dir():
    """确保订单目录存在 (标准路径 + 兼容旧路径)"""
    os.makedirs(_ORDER_DIR, exist_ok=True)
    _migrate_legacy_orders()


def _find_latest_order():
    """查找最新的订单文件
    
    修复: 改为按文件名(订单号)排序，而非文件修改时间。
    订单号格式: YYYYMMDDHHMMSS + 微秒 + UUID，天然按时间排序。
    按 mtime 排序可能误读被 ClawTip 回写更新的旧订单。
    """
    _ensure_order_dir()
    files = [f for f in os.listdir(_ORDER_DIR) if f.endswith('.json')]
    if not files:
        return None
    # 按文件名排序 (订单号包含时间戳，字典序=时间序)
    files.sort(reverse=True)
    path = os.path.join(_ORDER_DIR, files[0])
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f), path
    except Exception:
        return None


def create_order(sku_id: str = "sku_monthly"):
    """
    Phase 1: 创建订单 (标准 ClawTip 格式)
    
    写入 JSON 到 ~/.openclaw/skills/orders/{indicator}/{order_no}.json
    ClawTip Agent 会读取此文件，完成支付后回写 payCredential
    """
    _ensure_order_dir()
    
    sku = _SKU_CONFIG.get(sku_id, _SKU_CONFIG["sku_monthly"])
    order_no = datetime.now().strftime("%Y%m%d%H%M%S") + f"{datetime.now().microsecond:06d}" + uuid.uuid4().hex[:6]
    
    # 生成 encrypted_data: SM4 加密 {orderNo, amount, payTo}
    # 对应官方 Java 后端的 SM4EncryptionUtils.encrypt()
    encrypted_data = _sm4_encrypt({
        "orderNo": order_no,
        "amount": str(sku["cents"]),
        "payTo": _PAY_TO
    })
    
    # 标准 ClawTip 订单格式
    order = {
        "skill-id": _SKILL_SLUG,
        "order_no": order_no,
        "amount": sku["cents"],              # 金额(分)
        "question": f"运行 {_SKILL_DISPLAY_NAME}",
        "encrypted_data": encrypted_data,    # SM4 加密的订单数据
        "pay_to": _PAY_TO,                   # 收款服务ID
        "description": f"{_SKILL_DISPLAY_NAME} - {sku['name']}",
        "slug": _SKILL_SLUG,
        "resource_url": "local",              # 本地脚本模式，无远程服务地址
        # 额外字段 (兼容性 + 本地使用)
        "sku_id": sku_id,
        "price": sku["price"],
        "status": "unpaid",
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "payCredential": None,
    }
    
    path = os.path.join(_ORDER_DIR, f"{order_no}.json")
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(order, f, indent=2, ensure_ascii=False)
    
    print(f"[支付] 🛒 订单已创建: {order_no}")
    print(f"[支付]    SKU: {sku['name']} ({sku_id})")
    print(f"[支付]    金额: ¥{sku['price']}")
    print(f"[支付]    路径: {path}")
    print(f"[支付]    indicator: {_INDICATOR}")
    print(f"[支付] 💡 请让 Agent 调用: clawtip order_no={order_no} indicator={_INDICATOR}")
    
    return order, path


def verify_credential_sm4(credential: str, order: dict = None) -> dict:
    """
    Phase 3: 验证支付凭证 (SM4 解密 + 交叉验证)
    
    安全加固 v3.1:
    - 交叉验证: 凭证中的 orderNo/amount/payTo 必须与订单文件一致
    - 防止凭证复用 (用 A 订单的凭证解锁 B 订单)
    - 防止伪造 (需同时满足 SM4 解密 + 字段匹配)
    
    返回: {"valid": bool, "sku_id": str, "payload": dict}
    """
    if not credential or len(credential) < 10:
        return {"valid": False, "reason": "credential_empty"}

    try:
        from gmssl.sm4 import CryptSM4, SM4_DECRYPT
    except ImportError:
        print("[支付] ⚠️ 未安装 gmssl 库: pip install gmssl")
        return {"valid": False, "reason": "missing_gmssl"}

    try:
        key_bytes = base64.b64decode(_require_sm4_key())
        if len(key_bytes) != 16:
            return {"valid": False, "reason": f"invalid_key_length: {len(key_bytes)}"}

        crypt = CryptSM4()
        crypt.set_key(key_bytes, SM4_DECRYPT)
        
        encrypted_data = base64.b64decode(credential)
        decrypted_bytes = crypt.crypt_ecb(encrypted_data)
        
        # 去 PKCS7 Padding
        pad_len = decrypted_bytes[-1]
        if 0 < pad_len <= 16:
            decrypted_bytes = decrypted_bytes[:-pad_len]
        
        payload = json.loads(decrypted_bytes.decode('utf-8'))
        
        # 验证 payStatus — 生产环境接受 SUCCESS + 沙箱接受 TEST_SUCCESS
        pay_status = payload.get('payStatus', payload.get('pay_status', ''))
        if pay_status.upper() not in ('SUCCESS', 'PAID', '1', 'TRUE', 'TEST_SUCCESS'):
            return {"valid": False, "reason": f"not_paid: {pay_status}"}
        
        # 🔒 交叉验证: 凭证字段必须与订单文件一致
        if order:
            # 1. orderNo 必须匹配
            cred_order_no = payload.get('orderNo', payload.get('orderId', ''))
            file_order_no = order.get('order_no', order.get('order_id', ''))
            if cred_order_no and file_order_no and cred_order_no != file_order_no:
                return {"valid": False, "reason": f"orderNo不匹配: {cred_order_no[:12]}... vs {file_order_no[:12]}..."}
            
            # 2. payTo 必须匹配
            cred_payto = payload.get('payTo', payload.get('pay_to', ''))
            if cred_payto and cred_payto != _PAY_TO:
                return {"valid": False, "reason": "payTo不匹配"}
            
            # 3. amount 必须匹配
            cred_amount = str(payload.get('amount', ''))
            file_amount = str(order.get('amount', ''))
            if cred_amount and file_amount and cred_amount != file_amount:
                return {"valid": False, "reason": f"amount不匹配: {cred_amount} vs {file_amount}"}
        
        # 验证过期时间
        now = int(time.time())
        expires_at = payload.get('expire_at', payload.get('expires_at', 0))
        if expires_at and expires_at < now:
            return {"valid": False, "reason": "expired"}
            
        sku_id = payload.get('sku_id', 'sku_once')
        return {
            "valid": True,
            "sku_id": sku_id,
            "expires_at": expires_at,
            "payload": payload,
        }
        
    except Exception as e:
        print(f"[支付] ❌ 凭证解密失败: {str(e)}")
        return {"valid": False, "reason": f"decryption_error: {str(e)}"}


def _check_subscription_valid(order: dict, verify_result: dict) -> bool:
    """
    订阅有效期检查 (v3.1 新增)
    
    月度订阅 (sku_monthly) 有效期 30 天:
    - 优先使用 JD 凭证中的 expires_at
    - 若无 expires_at (sandbox/旧凭证)，使用订单创建时间 + 30 天
    - 沙箱模式 (TEST_SUCCESS) 跳过过期检查
    """
    payload = verify_result.get("payload", {})
    pay_status = payload.get("payStatus", payload.get("pay_status", ""))
    
    # 沙箱模式 (TEST_SUCCESS) 跳过过期检查
    if pay_status.upper() == "TEST_SUCCESS":
        return True
    
    now = int(time.time())
    expires_at = payload.get("expire_at", payload.get("expires_at", 0))
    
    if not expires_at:
        # 优先使用凭证中的 finishTime (支付完成时间) + 30 天
        # 这比订单创建时间更准确，因为用户可能创建订单后几天才支付
        finish_time = payload.get("finishTime", payload.get("finish_time", ""))
        if finish_time:
            try:
                # finishTime 通常为时间戳(秒) 或 ISO 日期字符串
                if isinstance(finish_time, (int, float)):
                    expires_at = int(finish_time) + 30 * 86400
                else:
                    dt = datetime.strptime(str(finish_time), "%Y-%m-%d %H:%M:%S")
                    expires_at = int(dt.timestamp()) + 30 * 86400
            except:
                pass
        
        # 兜底: 使用订单创建时间 + 30 天
        if not expires_at:
            created_at = order.get("created_at", "")
            if created_at:
                try:
                    dt = datetime.strptime(created_at, "%Y-%m-%d %H:%M:%S")
                    expires_at = int(dt.timestamp()) + 30 * 86400
                except:
                    return True  # 解析失败，放行
    
        # 最终兜底: 无任何时间信息，放行 (避免误杀老用户)
        if not expires_at:
            return True
    
    if expires_at < now:
        print(f"[支付] ⏰ 订阅已过期 ({datetime.fromtimestamp(expires_at).strftime('%Y-%m-%d')})")
        print(f"[支付] 💡 请重新支付以继续使用月度订阅")
        return False
    
    days_left = (expires_at - now) // 86400
    if days_left <= 3:
        print(f"[支付] ⚠️ 订阅将在 {days_left} 天后过期")
    
    return True


def check_and_verify() -> bool:
    """
    主入口: 检查支付状态
    返回: True 如果已支付且验证通过
    """
    # 安全检查: 禁止任何环境变量绕过
    if os.environ.get("LIBU_SKIP_PAYMENT") == "true":
        print("[支付] 🚨 安全告警: LIBU_SKIP_PAYMENT 被拒绝")
        return False
    if os.environ.get("LIBU_MOCK_PAYMENT") == "true":
        print("[支付] 🚨 安全告警: 生产环境禁止 Mock 模式")
        return False

    # 3. 查找订单 (自动迁移旧路径)
    result = _find_latest_order()
    if result is None:
        print("[支付] ⏳ 未找到订单，正在创建...")
        create_order()
        return False  # 首次运行，等用户支付
    
    order, path = result
    
    # 4. 检查支付凭证
    # 🔒 安全加固 v3.1: 必须有 payCredential，不再接受 status="paid" 无凭证
    cred = order.get("payCredential")
    has_credential = cred and len(cred) > 20
    
    if not has_credential:
        # 无凭证 → 未支付 (即使 status="paid" 也不放行)
        sku_id = order.get("sku_id", "sku_monthly")
        price = order.get("price", 9.9)
        order_no = order.get("order_no", order.get("order_id", "unknown"))
        print(f"[支付] ⏳ 待支付: {order_no} ({sku_id} | ¥{price})")
        print(f"[支付] 💡 请让 Agent 调用: clawtip order_no={order_no} indicator={_INDICATOR}")
        return False
    
    # 5. 验证凭证 (传入 order 进行交叉验证)
    verify_result = verify_credential_sm4(cred, order)
    if not verify_result.get("valid"):
        print(f"[支付] ❌ 凭证验证失败: {verify_result.get('reason')}")
        return False
    
    # 6. 订阅有效期检查 (v3.1 新增)
    sku_id = verify_result.get("sku_id", order.get("sku_id", "sku_once"))
    if sku_id == "sku_monthly":
        if not _check_subscription_valid(order, verify_result):
            return False
    
    print(f"[支付] ✅ 支付验证通过 | SKU: {sku_id}")
    return True


if __name__ == "__main__":
    result = check_and_verify()
    sys.exit(0 if result else 1)
