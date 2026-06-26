"""OK.com Cookie 持久化与管理"""

from __future__ import annotations

import json
import logging
from pathlib import Path

logger = logging.getLogger("ok-cookies")

COOKIE_DIR = Path(__file__).parent.parent.parent / ".cookies"


def save_cookies(cookies: list[dict], country: str = "default") -> Path:
    """保存 cookies 到本地文件

    Args:
        cookies: Chrome cookie 列表
        country: 国家标识（用于文件命名）

    Returns:
        保存的文件路径
    """
    COOKIE_DIR.mkdir(parents=True, exist_ok=True)
    path = COOKIE_DIR / f"{country}_cookies.json"
    path.write_text(json.dumps(cookies, ensure_ascii=False, indent=2), encoding="utf-8")
    logger.info("Cookies 已保存: %s (%d 条)", path, len(cookies))
    return path


def load_cookies(country: str = "default") -> list[dict] | None:
    """加载本地保存的 cookies

    Args:
        country: 国家标识

    Returns:
        Cookie 列表，文件不存在返回 None
    """
    path = COOKIE_DIR / f"{country}_cookies.json"
    if not path.exists():
        return None
    try:
        cookies = json.loads(path.read_text(encoding="utf-8"))
        logger.info("Cookies 已加载: %s (%d 条)", path, len(cookies))
        return cookies
    except (json.JSONDecodeError, OSError) as e:
        logger.warning("Cookies 加载失败: %s", e)
        return None


def delete_cookies(country: str = "default") -> bool:
    """删除本地保存的 cookies

    Args:
        country: 国家标识

    Returns:
        是否成功删除
    """
    path = COOKIE_DIR / f"{country}_cookies.json"
    if path.exists():
        path.unlink()
        logger.info("Cookies 已删除: %s", path)
        return True
    return False
