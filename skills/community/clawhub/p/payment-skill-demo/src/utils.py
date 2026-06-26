"""
工具函数模块

提供支付 Skill 所需的各种工具函数。
"""

import uuid
import re
from datetime import datetime
from typing import Optional, Tuple
from decimal import Decimal, InvalidOperation


def generate_transaction_id(prefix: str = "txn") -> str:
    """
    生成唯一的交易 ID。
    
    Args:
        prefix: 交易 ID 前缀，默认为 "txn"
    
    Returns:
        格式为 "{prefix}_{timestamp}_{uuid}" 的交易 ID
    
    Example:
        >>> txn_id = generate_transaction_id()
        >>> print(txn_id)
        txn_20260315_550e8400e29b41d4a716446655440000
    """
    timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
    unique_id = str(uuid.uuid4()).replace("-", "")[:16]
    return f"{prefix}_{timestamp}_{unique_id}"


def generate_verification_id(prefix: str = "ver") -> str:
    """
    生成跨设备验证 ID。
    
    Args:
        prefix: 验证 ID 前缀，默认为 "ver"
    
    Returns:
        格式为 "{prefix}_{uuid}" 的验证 ID
    """
    unique_id = str(uuid.uuid4()).replace("-", "")[:16]
    return f"{prefix}_{unique_id}"


def format_currency(amount: float, currency: str = "CNY") -> str:
    """
    格式化货币显示。
    
    Args:
        amount: 金额
        currency: 货币代码
    
    Returns:
        格式化后的货币字符串
    
    Example:
        >>> format_currency(299.00, "CNY")
        '¥299.00'
        >>> format_currency(99.99, "USD")
        '$99.99'
    """
    currency_symbols = {
        "CNY": "¥",
        "USD": "$",
        "EUR": "€",
        "GBP": "£",
        "JPY": "¥",
    }
    symbol = currency_symbols.get(currency, currency)
    return f"{symbol}{amount:.2f}"


def validate_amount(amount: float) -> Tuple[bool, Optional[str]]:
    """
    验证支付金额。
    
    Args:
        amount: 支付金额
    
    Returns:
        (是否有效, 错误信息)
    
    Example:
        >>> validate_amount(299.00)
        (True, None)
        >>> validate_amount(-100)
        (False, '金额必须大于0')
        >>> validate_amount(299.999)
        (False, '金额最多2位小数')
    """
    try:
        # 转换为 Decimal 以精确处理浮点数
        decimal_amount = Decimal(str(amount))
        
        # 检查金额范围
        if decimal_amount <= 0:
            return False, "金额必须大于0"
        
        if decimal_amount > 1000000:
            return False, "金额不能超过1,000,000"
        
        # 检查小数位数
        if decimal_amount.as_tuple().exponent < -2:
            return False, "金额最多2位小数"
        
        return True, None
    except (InvalidOperation, ValueError):
        return False, "金额格式无效"


def validate_currency(currency: str) -> Tuple[bool, Optional[str]]:
    """
    验证货币代码。
    
    Args:
        currency: ISO 4217 货币代码
    
    Returns:
        (是否有效, 错误信息)
    
    Example:
        >>> validate_currency("CNY")
        (True, None)
        >>> validate_currency("INVALID")
        (False, '无效的货币代码')
    """
    valid_currencies = {
        "CNY", "USD", "EUR", "GBP", "JPY", "AUD", "CAD", "CHF",
        "HKD", "SGD", "INR", "KRW", "MXN", "NZD", "ZAR"
    }
    
    if not isinstance(currency, str):
        return False, "货币代码必须是字符串"
    
    currency_upper = currency.upper()
    
    if currency_upper not in valid_currencies:
        return False, f"无效的货币代码: {currency}"
    
    return True, None


def validate_merchant_id(merchant_id: str) -> Tuple[bool, Optional[str]]:
    """
    验证商户 ID。
    
    Args:
        merchant_id: 商户 ID
    
    Returns:
        (是否有效, 错误信息)
    """
    if not isinstance(merchant_id, str):
        return False, "商户 ID 必须是字符串"
    
    if len(merchant_id) == 0:
        return False, "商户 ID 不能为空"
    
    if len(merchant_id) > 255:
        return False, "商户 ID 长度不能超过255"
    
    # 只允许字母、数字、下划线和连字符
    if not re.match(r"^[a-zA-Z0-9_-]+$", merchant_id):
        return False, "商户 ID 只能包含字母、数字、下划线和连字符"
    
    return True, None


def validate_description(description: str) -> Tuple[bool, Optional[str]]:
    """
    验证支付描述。
    
    Args:
        description: 支付描述
    
    Returns:
        (是否有效, 错误信息)
    """
    if not isinstance(description, str):
        return False, "描述必须是字符串"
    
    if len(description) == 0:
        return False, "描述不能为空"
    
    if len(description) > 500:
        return False, "描述长度不能超过500"
    
    return True, None


def validate_reference_id(reference_id: str) -> Tuple[bool, Optional[str]]:
    """
    验证幂等性标识。
    
    Args:
        reference_id: 幂等性标识
    
    Returns:
        (是否有效, 错误信息)
    """
    if not isinstance(reference_id, str):
        return False, "幂等性标识必须是字符串"
    
    if len(reference_id) == 0:
        return False, "幂等性标识不能为空"
    
    if len(reference_id) > 255:
        return False, "幂等性标识长度不能超过255"
    
    # UUID 或订单号格式
    if not re.match(r"^[a-zA-Z0-9_-]+$", reference_id):
        return False, "幂等性标识只能包含字母、数字、下划线和连字符"
    
    return True, None


def parse_timestamp(timestamp: int) -> str:
    """
    将时间戳转换为可读的日期时间字符串。
    
    Args:
        timestamp: Unix 时间戳（秒）
    
    Returns:
        格式为 "YYYY-MM-DD HH:MM:SS" 的日期时间字符串
    
    Example:
        >>> parse_timestamp(1710489600)
        '2026-03-15 12:00:00'
    """
    try:
        dt = datetime.utcfromtimestamp(timestamp)
        return dt.strftime("%Y-%m-%d %H:%M:%S")
    except (ValueError, OSError):
        return "Invalid timestamp"


def get_current_timestamp() -> int:
    """
    获取当前 Unix 时间戳。
    
    Returns:
        当前时间戳（秒）
    """
    return int(datetime.utcnow().timestamp())


def calculate_expiry_time(ttl_seconds: int) -> int:
    """
    计算过期时间戳。
    
    Args:
        ttl_seconds: 生存时间（秒）
    
    Returns:
        过期时间戳
    
    Example:
        >>> current = get_current_timestamp()
        >>> expiry = calculate_expiry_time(300)
        >>> expiry - current
        300
    """
    return get_current_timestamp() + ttl_seconds


def is_expired(expiry_time: int) -> bool:
    """
    检查是否已过期。
    
    Args:
        expiry_time: 过期时间戳
    
    Returns:
        是否已过期
    """
    return get_current_timestamp() > expiry_time


def truncate_string(text: str, max_length: int = 100) -> str:
    """
    截断字符串以防止日志过长。
    
    Args:
        text: 原始字符串
        max_length: 最大长度
    
    Returns:
        截断后的字符串
    """
    if len(text) <= max_length:
        return text
    return text[:max_length - 3] + "..."


def mask_sensitive_data(data: str, show_chars: int = 4) -> str:
    """
    掩盖敏感数据（如 API 密钥）。
    
    Args:
        data: 原始数据
        show_chars: 显示的字符数
    
    Returns:
        掩盖后的数据
    
    Example:
        >>> mask_sensitive_data("sk_live_abc123def456", 4)
        'sk_l...456'
    """
    if len(data) <= show_chars * 2:
        return "*" * len(data)
    
    start = data[:show_chars]
    end = data[-show_chars:]
    middle = "*" * (len(data) - show_chars * 2)
    return f"{start}{middle}{end}"
