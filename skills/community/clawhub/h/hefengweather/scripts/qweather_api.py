"""
和风天气 API 客户端
提供统一的 API 调用接口
"""

import httpx
import logging
import os
import time
from datetime import datetime, timedelta, timezone
from typing import Optional, Dict, Any

import jwt
from dotenv import load_dotenv

# 配置日志
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("qweather_api")

# 加载环境变量
load_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env"))
load_dotenv(os.path.expanduser("~/.config/qweather/.env"))


class QWeatherAPI:
    """和风天气 API 客户端"""

    def __init__(self):
        self._api_host: Optional[str] = None
        self._auth_header: Optional[Dict[str, str]] = None

    def _init_config(self) -> None:
        """初始化API配置"""
        if self._auth_header is not None:
            return

        self._api_host = os.environ.get("HEFENG_API_HOST")
        api_key = os.environ.get("HEFENG_API_KEY")
        project_id = os.environ.get("HEFENG_PROJECT_ID")
        key_id = os.environ.get("HEFENG_KEY_ID")
        private_key_path = os.environ.get("HEFENG_PRIVATE_KEY_PATH")
        private_key_str = os.environ.get("HEFENG_PRIVATE_KEY")

        if not self._api_host:
            raise ValueError("HEFENG_API_HOST 环境变量未设置,请先运行 configure.py")

        if api_key:
            self._auth_header = {"X-QW-Api-Key": api_key, "Content-Type": "application/json"}
            logger.info("使用API KEY认证模式")
        else:
            # JWT认证
            if not project_id or not key_id or (not private_key_path and not private_key_str):
                raise ValueError(
                    "必须设置 HEFENG_API_KEY,或者设置完整的JWT认证配置"
                )

            if private_key_path:
                with open(private_key_path, "rb") as f:
                    private_key = f.read()
            else:
                private_key = private_key_str.replace("\\r\\n", "\n").replace("\\n", "\n").encode()

            payload = {
                "iat": int(time.time()),
                "exp": int(time.time()) + 900,
                "sub": project_id,
            }
            headers = {"kid": key_id}

            encoded_jwt = jwt.encode(payload, private_key, algorithm="EdDSA", headers=headers)
            self._auth_header = {"Authorization": f"Bearer {encoded_jwt}"}
            logger.info("使用JWT认证模式")

    def get_city_location(self, city: str, return_coords: bool = False) -> Optional[str]:
        """
        根据城市名称获取LocationID或经纬度

        Args:
            city: 城市名称
            return_coords: 是否返回经纬度坐标

        Returns:
            LocationID 或 "纬度,经度" 格式的坐标
        """
        self._init_config()

        url = f"https://{self._api_host}/geo/v2/city/lookup"

        try:
            response = httpx.get(url, headers=self._auth_header, params={"location": city})

            if response.status_code != 200:
                logger.error(f"查询城市位置失败 - 状态码: {response.status_code}")
                return None

            data = response.json()
            if data and data.get("location") and len(data["location"]) > 0:
                if return_coords:
                    lat = float(data["location"][0]["lat"])
                    lon = float(data["location"][0]["lon"])
                    return f"{lat:.2f},{lon:.2f}"
                return data["location"][0]["id"]
            else:
                logger.warning(f"未找到城市 '{city}' 的位置信息")
                return None

        except Exception as e:
            logger.error(f"查询城市位置时发生错误: {e}")
            return None

    def request(self, endpoint: str, params: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        发起 API 请求

        Args:
            endpoint: API 端点路径
            params: 请求参数

        Returns:
            API 响应的 JSON 数据
        """
        self._init_config()

        url = f"https://{self._api_host}/{endpoint}"

        try:
            response = httpx.get(url, headers=self._auth_header, params=params)
            if response.status_code == 200:
                return response.json()
            logger.error(f"API 请求失败 - 状态码: {response.status_code}, 响应: {response.text}")
            return None
        except Exception as e:
            logger.error(f"API 请求时发生错误: {e}")
            return None


# 全局实例
api = QWeatherAPI()
