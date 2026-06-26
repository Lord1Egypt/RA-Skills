"""
Cloudflare 邮箱保护解密器

解码被 Cloudflare Email Protection 保护的邮箱地址。

背景:
    许多使用 Cloudflare CDN 的网站会启用邮箱保护功能。
    邮箱地址会被替换为加密字符串，如:
    <a href="/cdn-cgi/l/email-protection#f493919e85c6c5b499959d9887da80879d9a939c8195da919081da979a">

原理:
    Cloudflare 使用简单的 XOR 加密:
    - 第一个字节（2个字符）是密钥
    - 后续每个字节与密钥 XOR 得到原始字符

使用示例:
    from cloudflare_email_decoder import decode_cloudflare_email, extract_cloudflare_email

    # 直接解码
    email = decode_cloudflare_email("f493919e85c6c5...")

    # 从链接中提取
    href = "/cdn-cgi/l/email-protection#f493919e85c6c5..."
    email = extract_cloudflare_email(href)
"""


def decode_cloudflare_email(encoded: str) -> str:
    """
    解码 Cloudflare 邮箱保护

    Args:
        encoded: 加密后的十六进制字符串
                 (如 "f493919e85c6c5b499959d9887da80879d9a939c8195da919081da979a")

    Returns:
        解密后的邮箱地址
        如果解密失败，返回空字符串

    Example:
        >>> decode_cloudflare_email("f493919e85c6c5b499959d9887da80879d9a939c8195da919081da979a")
        'gejq21@mails.tsinghua.edu.cn'
    """
    try:
        encoded = encoded.strip()

        # 检查格式
        if not encoded or len(encoded) < 4:
            return ''

        # 第一个字节是密钥
        key = int(encoded[:2], 16)

        # XOR 解密
        decoded = ''
        for i in range(2, len(encoded), 2):
            char_code = int(encoded[i:i+2], 16) ^ key
            decoded += chr(char_code)

        # 验证结果是否像邮箱
        if '@' in decoded and '.' in decoded:
            return decoded
        return ''

    except (ValueError, IndexError):
        return ''


def extract_cloudflare_email(href: str) -> str:
    """
    从 Cloudflare 保护的链接中提取邮箱

    Args:
        href: 形如 "/cdn-cgi/l/email-protection#abc123def" 的链接

    Returns:
        解密后的邮箱地址

    Example:
        >>> href = "/cdn-cgi/l/email-protection#f493919e85c6c5..."
        >>> extract_cloudflare_email(href)
        'gejq21@mails.tsinghua.edu.cn'
    """
    prefix = '/cdn-cgi/l/email-protection#'

    if prefix not in href:
        return ''

    encoded = href.split('#')[-1]
    return decode_cloudflare_email(encoded)


def is_cloudflare_protected(href: str) -> bool:
    """
    检查链接是否是 Cloudflare 保护的邮箱

    Args:
        href: 链接字符串

    Returns:
        是否是 Cloudflare 保护的邮箱链接
    """
    return '/cdn-cgi/l/email-protection' in href


def extract_all_cloudflare_emails(html: str) -> list:
    """
    从 HTML 中提取所有 Cloudflare 保护的邮箱

    Args:
        html: HTML 内容

    Returns:
        邮箱地址列表
    """
    import re

    # 匹配 Cloudflare 邮箱保护链接
    pattern = r'/cdn-cgi/l/email-protection#([a-fA-F0-9]+)'

    emails = []
    for match in re.finditer(pattern, html):
        encoded = match.group(1)
        email = decode_cloudflare_email(encoded)
        if email:
            emails.append(email)

    return emails


# 解密过程可视化
def explain_decryption(encoded: str) -> None:
    """
    可视化解密过程，用于调试和学习

    Args:
        encoded: 加密后的十六进制字符串

    Example:
        >>> explain_decryption("f493919e85c6c5b499959d9887da80879d9a939c8195da919081da979a")
    """
    print(f"加密字符串: {encoded}")
    print(f"长度: {len(encoded)} 字符 = {len(encoded)//2} 字节")
    print()

    key = int(encoded[:2], 16)
    print(f"密钥: 0x{encoded[:2]} ({key})")
    print()

    print("解密过程:")
    print("-" * 50)

    decoded = ''
    for i in range(2, len(encoded), 2):
        byte_hex = encoded[i:i+2]
        byte_val = int(byte_hex, 16)
        char_val = byte_val ^ key
        char = chr(char_val)

        decoded += char
        print(f"  0x{byte_hex} ^ 0x{encoded[:2]} = 0x{char_val:02x} = '{char}'")

    print("-" * 50)
    print(f"结果: {decoded}")


# 测试用例
TEST_CASES = [
    {
        "encoded": "f493919e85c6c5b499959d9887da80879d9a939c8195da919081da979a",
        "expected": "gejq21@mails.tsinghua.edu.cn"
    },
    {
        "encoded": "d2bbb7a1b3a0b6b5fcb0bbb9a0b6bb92b3bca1",
        "expected": "test@example.com"
    }
]


def run_tests():
    """运行测试用例"""
    print("Running tests...\n")

    for i, case in enumerate(TEST_CASES, 1):
        encoded = case["encoded"]
        expected = case["expected"]
        result = decode_cloudflare_email(encoded)

        status = "✓" if result == expected else "✗"
        print(f"Test {i}: {status}")
        print(f"  Input: {encoded[:30]}...")
        print(f"  Expected: {expected}")
        print(f"  Got: {result}")
        print()


# 使用示例
if __name__ == "__main__":
    # 示例 1: 基本使用
    print("=== 基本使用 ===")
    href = "/cdn-cgi/l/email-protection#f493919e85c6c5b499959d9887da80879d9a939c8195da919081da979a"
    email = extract_cloudflare_email(href)
    print(f"从链接提取邮箱: {email}")

    # 示例 2: 直接解码
    print("\n=== 直接解码 ===")
    encoded = "f493919e85c6c5b499959d9887da80879d9a939c8195da919081da979a"
    email = decode_cloudflare_email(encoded)
    print(f"解码结果: {email}")

    # 示例 3: 解密过程可视化
    print("\n=== 解密过程可视化 ===")
    explain_decryption("f493919e85c6c5")

    # 示例 4: 运行测试
    print("\n=== 运行测试 ===")
    run_tests()
