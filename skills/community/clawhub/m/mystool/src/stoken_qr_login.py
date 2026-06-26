"""
stoken 扫码补全模块
用于 Cookie 登录或短信登录后 stoken 缺失时，通过扫码补全 stoken。
流程与 qr_login.py 相同，但只更新现有账号的 stoken 字段，不重新绑定。
"""

from qr_login import (
    fetch_qrcode,
    game_token_to_cookies,
    qrcode_to_image_url,
    query_qrcode,
)

__all__ = [
    "fetch_qrcode",
    "game_token_to_cookies",
    "qrcode_to_image_url",
    "query_qrcode",
]
