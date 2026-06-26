#!/usr/bin/env python3
"""
媒体大数据平台Token管理器
提供文件级持久化和多进程安全的Token管理
"""

import os
import json
import time
import fcntl
import threading
import logging
from pathlib import Path
from typing import Optional, Dict, Any
from datetime import datetime, timedelta
import requests
import urllib.parse
import urllib3
import warnings

# 禁用 urllib3 的不安全请求警告
warnings.filterwarnings("ignore", category=urllib3.exceptions.InsecureRequestWarning)

# 配置日志
logger = logging.getLogger(__name__)

class TokenManager:
    """
    媒体大数据平台Token管理器
    支持文件级持久化和多进程安全访问
    """

    def __init__(self, token_file_path: Optional[str] = None):
        """
        初始化Token管理器

        Args:
            token_file_path: Token存储文件路径，默认为当前skill目录下的.mbd_token_cache.json
        """
        if token_file_path is None:
            # 获取当前文件所在目录（scripts目录）的父目录（项目根目录）
            current_dir = Path(__file__).parent.parent
            self.token_file = current_dir / ".mbd_token_cache.json"
        else:
            self.token_file = Path(token_file_path)

        # 确保token文件目录存在
        self.token_file.parent.mkdir(parents=True, exist_ok=True)

        # 进程内缓存，避免频繁文件读取
        self._cached_token = None
        self._cache_timestamp = 0
        self._cache_lock = threading.Lock()

        # 文件锁超时时间（秒）
        self.file_lock_timeout = 30

    def _acquire_file_lock(self, file_handle):
        """
        获取文件锁，支持超时机制

        Args:
            file_handle: 文件句柄

        Raises:
            TimeoutError: 获取锁超时
        """
        start_time = time.time()
        while True:
            try:
                fcntl.flock(file_handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
                return
            except (IOError, OSError):
                if time.time() - start_time > self.file_lock_timeout:
                    raise TimeoutError(f"无法在{self.file_lock_timeout}秒内获取文件锁")
                time.sleep(0.1)

    def _release_file_lock(self, file_handle):
        """释放文件锁"""
        try:
            fcntl.flock(file_handle.fileno(), fcntl.LOCK_UN)
        except (IOError, OSError):
            pass

    def _read_token_from_file(self) -> Optional[Dict[str, Any]]:
        """
        从文件读取Token信息

        Returns:
            Token信息字典，如果文件不存在或读取失败则返回None
        """
        if not self.token_file.exists():
            logger.info(f"Token文件不存在: {self.token_file}")
            return None

        logger.info(f"开始读取Token文件: {self.token_file}")

        try:
            with open(self.token_file, 'r', encoding='utf-8') as f:
                self._acquire_file_lock(f)
                try:
                    content = f.read().strip()
                    if not content:
                        logger.warning("Token文件为空")
                        return None
                    token_data = json.loads(content)
                    logger.info("Token文件读取成功")
                    return token_data
                finally:
                    self._release_file_lock(f)
        except (json.JSONDecodeError, IOError, TimeoutError) as e:
            error_msg = f"读取Token文件失败: {e}"
            logger.error(error_msg)
            print(error_msg)
            return None

    def _write_token_to_file(self, token_data: Dict[str, Any]) -> bool:
        """
        将Token信息写入文件

        Args:
            token_data: Token信息字典

        Returns:
            写入成功返回True，否则返回False
        """
        logger.info(f"开始写入Token到文件: {self.token_file}")

        try:
            with open(self.token_file, 'w', encoding='utf-8') as f:
                self._acquire_file_lock(f)
                try:
                    json.dump(token_data, f, ensure_ascii=False, indent=2)
                    f.flush()
                    os.fsync(f.fileno())
                    logger.info("Token文件写入成功")
                    return True
                finally:
                    self._release_file_lock(f)
        except (IOError, TimeoutError) as e:
            error_msg = f"写入Token文件失败: {e}"
            logger.error(error_msg)
            print(error_msg)
            return False

    def _is_token_expired(self, token_data: Dict[str, Any]) -> bool:
        """
        检查Token是否过期（提前5分钟刷新）

        Args:
            token_data: Token信息字典

        Returns:
            如果Token过期返回True，否则返回False
        """
        if not token_data or 'created_at' not in token_data or 'expires_in' not in token_data:
            logger.warning("Token数据不完整，视为已过期")
            return True

        created_at = token_data['created_at']
        expires_in = token_data['expires_in']
        current_time = time.time()
        age = current_time - created_at

        # 提前5分钟刷新（300秒）
        is_expired = age >= (expires_in - 300)

        if is_expired:
            remaining = expires_in - age
            logger.info(f"Token已过期，剩余时间: {remaining:.1f}秒 (提前5分钟刷新)")
        else:
            remaining = (expires_in - 300) - age
            logger.info(f"Token有效，剩余刷新时间: {remaining:.1f}秒")

        return is_expired

    def _fetch_new_token(self, appid: str, secret: str) -> Optional[Dict[str, Any]]:
        """
        从API获取新的Token

        Args:
            appid: 应用ID
            secret: 应用密钥

        Returns:
            Token信息字典，如果获取失败则返回None
        """
        token_url = "https://mbdapi.fzdzyun.com/api/token"
        logger.info(f"调用Token API: {token_url}")

        data = {
            "grant_type": "secret",
            "appid": appid,
            "secret": secret,
        }

        headers = {
            "Accept": "application/json",
            "Content-Type": "application/x-www-form-urlencoded",
            "format": "founder",
        }

        logger.info(f"Token API请求参数: grant_type=secret, appid={appid[:8]}...")

        try:
            response = requests.post(
                url=token_url,
                data=urllib.parse.urlencode(data),
                headers=headers,
                timeout=30,
                verify=False,
            )
            response.raise_for_status()
            result = response.json()

            logger.info(f"Token API响应状态码: {response.status_code}")

            if result.get("status") != 0:
                error_msg = f"Token请求失败: {result.get('message', 'Unknown error')}"
                logger.error(error_msg)
                print(error_msg)
                return None

            token_data = result.get("data", {})
            if not token_data.get("access_token"):
                error_msg = "Token响应中缺少access_token"
                logger.error(error_msg)
                print(error_msg)
                return None

            logger.info("Token API响应解析成功")

            # 构建完整的Token信息
            token_info = {
                "access_token": token_data.get("access_token", ""),
                "expires_in": token_data.get("expires_in", 7200),
                "proj_id": token_data.get("projId"),
                "area_id": token_data.get("areaId"),
                "app_id": token_data.get("appId"),
                "media_id": token_data.get("mediaId"),
                "user_id": token_data.get("userId"),
                "created_at": time.time(),
                "appid": appid  # 保存appid用于刷新
            }

            logger.info(f"新Token构建完成，有效期: {token_info['expires_in']}秒")
            return token_info

        except requests.RequestException as e:
            error_msg = f"获取Token请求失败: {e}"
            logger.error(error_msg)
            print(error_msg)
            return None
        except json.JSONDecodeError as e:
            error_msg = f"解析Token响应失败: {e}"
            logger.error(error_msg)
            print(error_msg)
            return None

    def get_token(self, appid: Optional[str] = None, secret: Optional[str] = None,
                  force_refresh: bool = False) -> Optional[str]:
        """
        获取有效的访问Token

        Args:
            appid: 应用ID，如果为None则从环境变量读取
            secret: 应用密钥，如果为None则从环境变量读取
            force_refresh: 是否强制刷新Token

        Returns:
            访问Token字符串，如果获取失败则返回None
        """
        logger.info(f"开始获取Token，force_refresh={force_refresh}")

        # 优先使用进程内缓存
        with self._cache_lock:
            current_time = time.time()
            if (not force_refresh and self._cached_token and
                self._cache_timestamp > current_time - 300 and  # 5分钟内不重新检查文件
                not self._is_token_expired(self._cached_token)):
                logger.info("使用进程内缓存的Token")
                return self._cached_token.get("access_token")

        logger.info("进程内缓存不可用，检查文件缓存")

        # 从环境变量获取凭据
        if appid is None:
            appid = os.getenv("NEWS_BIGDATA_API_KEY")
        if secret is None:
            secret = os.getenv("NEWS_BIGDATA_API_SECRET")

        if not appid or not secret:
            error_msg = "错误: 缺少API凭据。请设置环境变量 NEWS_BIGDATA_API_KEY 和 NEWS_BIGDATA_API_SECRET"
            logger.error(error_msg)
            print(error_msg)
            return None

        logger.info(f"API凭据检查通过，appid: {appid[:8]}...")

        # 尝试从文件读取Token
        token_data = None
        if not force_refresh:
            logger.info(f"尝试从文件读取Token: {self.token_file}")
            token_data = self._read_token_from_file()

        # 检查Token是否有效
        if token_data:
            logger.info("从文件成功读取Token")
            if self._is_token_expired(token_data):
                logger.warning("文件中的Token已过期，需要刷新")
                # 检查过期时间
                created_at = token_data.get('created_at', 0)
                expires_in = token_data.get('expires_in', 0)
                expired_time = time.time() - created_at - expires_in
                logger.info(f"Token已过期 {expired_time/60:.1f} 分钟")
            else:
                # 验证Token中的appid是否匹配
                if token_data.get("appid") == appid:
                    logger.info("文件Token有效且appid匹配，使用文件Token")
                    with self._cache_lock:
                        self._cached_token = token_data
                        self._cache_timestamp = current_time
                    return token_data.get("access_token")
                else:
                    logger.warning("文件Token的appid不匹配，需要重新获取")
        else:
            logger.info("文件中未找到Token或读取失败")

        # 获取新Token
        logger.info("开始调用API获取新Token")
        new_token_data = self._fetch_new_token(appid, secret)
        if new_token_data:
            logger.info("API获取Token成功")
            # 保存到文件
            if self._write_token_to_file(new_token_data):
                logger.info(f"新Token已保存到文件: {self.token_file}")
                with self._cache_lock:
                    self._cached_token = new_token_data
                    self._cache_timestamp = current_time
                logger.info(f"新Token有效期: {new_token_data.get('expires_in')}秒")
                return new_token_data.get("access_token")
            else:
                warning_msg = "警告: Token获取成功但保存到文件失败"
                logger.warning(warning_msg)
                print(warning_msg)
                # 即使文件保存失败，也返回Token
                return new_token_data.get("access_token")

        logger.error("获取Token失败")
        return None

    def clear_token_cache(self):
        """清除所有Token缓存"""
        with self._cache_lock:
            self._cached_token = None
            self._cache_timestamp = 0

        # 删除token文件
        try:
            if self.token_file.exists():
                self.token_file.unlink()
        except OSError as e:
            print(f"删除Token文件失败: {e}")

    def get_token_info(self) -> Optional[Dict[str, Any]]:
        """
        获取完整的Token信息

        Returns:
            Token信息字典，如果获取失败则返回None
        """
        # 优先使用进程内缓存
        with self._cache_lock:
            if self._cached_token:
                return self._cached_token.copy()

        # 从文件读取
        token_data = self._read_token_from_file()
        if token_data:
            with self._cache_lock:
                self._cached_token = token_data
                self._cache_timestamp = time.time()
            return token_data.copy()

        return None

    def is_token_valid(self) -> bool:
        """
        检查当前是否有有效的Token

        Returns:
            如果有有效Token返回True，否则返回False
        """
        token_data = self.get_token_info()
        return token_data is not None and not self._is_token_expired(token_data)


def main():
    """测试Token管理器"""
    manager = TokenManager()

    # 测试获取Token
    token = manager.get_token()
    if token:
        print(f"成功获取Token: {token[:20]}...")
        print(f"Token有效: {manager.is_token_valid()}")

        # 显示Token信息
        token_info = manager.get_token_info()
        if token_info:
            created_time = datetime.fromtimestamp(token_info.get('created_at', 0))
            expires_in = token_info.get('expires_in', 0)
            print(f"创建时间: {created_time}")
            print(f"有效期: {expires_in}秒")
    else:
        print("获取Token失败")

    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())