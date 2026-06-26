import requests
import json
import os


def login(email: str, password: str) -> str:
    """
    使用账号密码登录 LetPub，返回 cookies 字符串

    Args:
        email: 登录邮箱
        password: 登录密码

    Returns:
        登录后的 cookies 字符串（包含 PHPSESSID 等）
    """
    session = requests.Session()

    # 第1步：先访问登录页，获取初始 cookies（PHPSESSID 等）
    login_page_url = "https://www.letpub.com.cn/index.php?page=login"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36 Edg/149.0.0.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    }
    session.get(login_page_url, headers=headers)

    # 第2步：发送登录请求
    login_url = "https://www.letpub.com.cn/content/index.php?action=loginajax"
    login_headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36 Edg/149.0.0.0",
        "Accept": "*/*",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Origin": "https://www.letpub.com.cn",
        "Referer": "https://www.letpub.com.cn/index.php?page=login",
        "X-Requested-With": "XMLHttpRequest",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
    }
    data = {
        "email": email,
        "password": password,
    }

    response = session.post(login_url, data=data, headers=login_headers)
    response.raise_for_status()

    # 第3步：从 session 中提取所有 cookies 并拼接为字符串
    cookies_dict = session.cookies.get_dict()
    cookies_str = "; ".join(f"{k}={v}" for k, v in cookies_dict.items())

    return cookies_str, response


def save_cookies(cookies_str: str):
    """
    将 cookies 字符串保存到 assets/cookies.json

    Args:
        cookies_str: cookies 字符串
    """
    cookies_file = os.path.join(os.path.dirname(__file__), '..', 'assets', 'cookies.json')
    with open(cookies_file, 'w', encoding='utf-8') as f:
        json.dump({"cookies": cookies_str}, f, ensure_ascii=False, indent=2)


def auto_login(email: str, password: str) -> str:
    """
    一键登录并保存 cookies

    Args:
        email: 登录邮箱
        password: 登录密码

    Returns:
        登录后的 cookies 字符串
    """
    cookies_str, response = login(email, password)

    # 检查登录结果
    print(f"登录响应: {response.text}")
    print(f"获取到的 cookies: {cookies_str}")

    # 保存到文件
    save_cookies(cookies_str)
    print("Cookies 已保存到 assets/cookies.json")

    return cookies_str


def load_credentials() -> tuple:
    """
    从 assets/credentials.json 加载账号密码

    Returns:
        (email, password) 元组
    """
    credentials_file = os.path.join(os.path.dirname(__file__), '..', 'assets', 'credentials.json')
    if not os.path.exists(credentials_file):
        raise FileNotFoundError(f"找不到账号配置文件: {credentials_file}，请先创建并填入 email 和 password")
    with open(credentials_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    email = data.get('email', '').strip()
    password = data.get('password', '').strip()
    if not email or not password:
        raise ValueError("assets/credentials.json 中 email 或 password 为空，请填写")
    return email, password


def _load_cookies_from_file() -> str:
    """
    从 assets/cookies.json 读取 cookies 字符串（内部使用）

    Returns:
        cookies 字符串，文件不存在或为空时返回空字符串
    """
    cookies_file = os.path.join(os.path.dirname(__file__), '..', 'assets', 'cookies.json')
    if os.path.exists(cookies_file):
        with open(cookies_file, 'r', encoding='utf-8') as f:
            try:
                data = json.load(f)
                return data.get('cookies', '').strip()
            except json.JSONDecodeError:
                return ''
    return ''


def ensure_logged_in(force: bool = False) -> str:
    """
    确保已登录：检查本地 cookies 是否有效，若无效则自动登录续期

    Args:
        force: True 时忽略现有 cookies，强制重新登录

    判断逻辑（force=False 时）：
    - cookies.json 不存在或为空 → 重新登录
    - cookies 中不含 PHPSESSID → 重新登录
    - 否则直接返回现有 cookies

    Returns:
        有效的 cookies 字符串
    """
    if not force:
        existing = _load_cookies_from_file()
        if existing and 'PHPSESSID=' in existing:
            return existing

    # cookies 无效或强制续期，使用 credentials.json 重新登录
    email, password = load_credentials()
    cookies_str, response = login(email, password)
    response_text = response.text.strip()

    if not response_text.startswith('SUCCESS'):
        raise RuntimeError(f"自动登录失败，响应: {response_text}，请检查 assets/credentials.json 中的账号密码")

    save_cookies(cookies_str)
    return cookies_str


if __name__ == "__main__":
    # 从 credentials.json 读取账号密码，自动登录并保存 cookies
    email, password = load_credentials()
    print(f"使用账号: {email}")
    cookies = auto_login(email, password)
