"""
本地测试工具：伪造一个 clawtip SUCCESS credential
仅用于本地联调 /api/clawtip/get-service-result，不要用于生产。

用法：
  python3 mock_credential.py <orderNo>

依赖：
  pip install gmssl
"""
import sys
import json
import base64
from datetime import datetime

try:
    from gmssl import sm4
except ImportError:
    print("请先安装 gmssl：pip install gmssl")
    sys.exit(1)

# 与 application.yml 的 clawtip.sm4-key 保持一致
SM4_KEY_BASE64 = "xK9MtxnmTqfxBhuQXpAmcw=="
PAY_TO = "b7b74e49a338aedb54f06ad30ddee3c2202604151358380010007062GGnHrKwgwTk6ZKzKxhYyt7l45VU0iYD5cJAnvmJJssMMp8YwPwhD6SjsuUIDeK4tdYjJmgDs"
AMOUNT_FEN = "10"


def pkcs7_pad(data: bytes, block_size: int = 16) -> bytes:
    pad_len = block_size - len(data) % block_size
    return data + bytes([pad_len] * pad_len)


def sm4_encrypt_base64(plain: str, key_bytes: bytes) -> str:
    """Hutool SM4 默认：ECB 模式 + PKCS5Padding，输出 Base64"""
    cipher = sm4.CryptSM4()
    cipher.set_key(key_bytes, sm4.SM4_ENCRYPT)
    padded = pkcs7_pad(plain.encode("utf-8"))
    encrypted = cipher.crypt_ecb(padded)
    return base64.b64encode(encrypted).decode("ascii")


def make_credential(order_no: str) -> str:
    payload = {
        "orderNo": order_no,
        "amount": AMOUNT_FEN,
        "payTo": PAY_TO,
        "payStatus": "SUCCESS",
        "finishTime": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
    plain = json.dumps(payload, ensure_ascii=False)
    key_bytes = base64.b64decode(SM4_KEY_BASE64)
    return sm4_encrypt_base64(plain, key_bytes)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 mock_credential.py <orderNo>")
        sys.exit(1)
    credential = make_credential(sys.argv[1])
    print(credential)
