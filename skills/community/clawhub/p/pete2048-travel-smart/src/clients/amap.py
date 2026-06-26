# -*- coding: utf-8 -*-
"""
高德地图 API 客户端
"""
import math
from typing import Optional
import requests
from loguru import logger
from ..config.settings import AMAP_KEY, AMAP_BASE_URL


class AmapClient:
    """高德地图 API 封装"""

    def __init__(self, key: str = None):
        self.key = key or AMAP_KEY
        if not self.key:
            raise ValueError("AMAP_KEY 未配置，请配置高德地图 Web API Key")
        self.base_url = AMAP_BASE_URL

    def _get(self, endpoint: str, params: dict) -> dict:
        """通用 GET 请求"""
        params["key"] = self.key
        url = f"{self.base_url}/{endpoint}"
        try:
            resp = requests.get(url, params=params, timeout=10)
            data = resp.json()
            if data.get("status") != "1":
                logger.error(f"高德 API 错误: {data}")
                return {}
            return data
        except Exception as e:
            logger.error(f"高德请求异常: {e}")
            return {}

    def geocode(self, address: str, city: str = "") -> Optional[dict]:
        """
        地理编码：地址 → 坐标

        Returns: {"lng": 116.463, "lat": 39.923, "province": "...", "city": "...", "district": "..."}
        """
        params = {"address": address, "city": city}
        data = self._get("geocode/geo", params)
        if data.get("geocodes"):
            g = data["geocodes"][0]
            return {
                "lng": float(g["location"].split(",")[0]),
                "lat": float(g["location"].split(",")[1]),
                "province": g.get("province", ""),
                "city": g.get("city", ""),
                "district": g.get("district", ""),
            }
        return None

    def regeo(self, lng: float, lat: float) -> Optional[dict]:
        """
        逆地理编码：坐标 → 地址
        """
        params = {"location": f"{lng},{lat}", "extensions": "base"}
        data = self._get("geocode/regeo", params)
        if data.get("regeocode"):
            r = data["regeocode"]
            return {
                "address": r.get("formatted_address", ""),
                "province": r.get("addressComponent", {}).get("province", ""),
                "city": r.get("addressComponent", {}).get("city", ""),
                "district": r.get("addressComponent", {}).get("district", ""),
            }
        return None

    def around_search(
        self,
        lng: float,
        lat: float,
        keywords: str = "",
        types: str = "",
        radius: int = 5000,
        count: int = 20,
    ) -> list:
        """
        周边搜索

        Args:
            lng, lat: 中心坐标
            keywords: 关键字（多个用|分隔）
            types: POI 类型（餐饮、酒店、景点等）
            radius: 搜索半径（米），最大 50000
            count: 返回数量，最大 50

        Returns: [{"name": "...", "location": "lng,lat", "address": "...", "distance": 123}, ...]
        """
        params = {
            "location": f"{lng},{lat}",
            "keywords": keywords,
            "types": types,
            "radius": min(radius, 50000),
            "offset": count,
            "page": 1,
            "extensions": "base",
        }
        data = self._get("place/around", params)
        pois = []
        if data.get("pois"):
            for p in data["pois"]:
                pois.append(
                    {
                        "name": p.get("name", ""),
                        "location": p.get("location", ""),
                        "address": p.get("address", ""),
                        "distance": float(p.get("distance", 0)),
                        "type": p.get("type", ""),
                    }
                )
        return pois

    def place_keyword(
        self, keywords: str, city: str = "", citylimit: bool = False, count: int = 20
    ) -> list:
        """
        关键字搜索

        Returns: [{"name": "...", "location": "lng,lat", "address": "...", "tel": "..."}, ...]
        """
        params = {
            "keywords": keywords,
            "city": city,
            "citylimit": "true" if citylimit else "false",
            "offset": count,
            "page": 1,
            "extensions": "base",
        }
        data = self._get("place/text", params)
        pois = []
        if data.get("pois"):
            for p in data["pois"]:
                pois.append(
                    {
                        "name": p.get("name", ""),
                        "location": p.get("location", ""),
                        "address": p.get("address", ""),
                        "tel": p.get("tel", ""),
                    }
                )
        return pois

    def driving_route(
        self, origin: str, destination: str, waypoints: str = ""
    ) -> Optional[dict]:
        """
        驾车路径规划

        Args:
            origin: 起点坐标 "lng,lat"
            destination: 终点坐标 "lng,lat"
            waypoints: 途经点坐标（多个用;分隔）

        Returns: {"distance": 12345, "time": 600, "steps": [...]}
        """
        params = {
            "origin": origin,
            "destination": destination,
            "extensions": "base",
        }
        if waypoints:
            params["waypoints"] = waypoints
        data = self._get("direction/driving", params)
        if data.get("route"):
            r = data["route"]
            return {
                "distance": int(r.get("distance", 0)),  # 米
                "time": int(r.get("time", 0)),  # 秒
                "paths": [
                    {
                        "distance": int(p.get("distance", 0)),
                        "time": int(p.get("time", 0)),
                    }
                    for p in r.get("paths", [])
                ],
            }
        return None

    def distance(
        self, origins: str, destination: str
    ) -> Optional[dict]:
        """
        距离测量

        Args:
            origins: 起点坐标，多个用;分隔
            destination: 终点坐标

        Returns: {"distance": 1234, "time": 120}
        """
        params = {"origins": origins, "destination": destination, "type": "1"}
        data = self._get("distance", params)
        if data.get("results"):
            r = data["results"][0]
            return {
                "distance": int(r.get("distance", 0)),
                "time": int(r.get("duration", 0)),
            }
        return None

    @staticmethod
    def parse_location(loc_str: str) -> tuple:
        """解析 "lng,lat" 字符串为 (lng, lat)"""
        if not loc_str or "," not in loc_str:
            return None, None
        parts = loc_str.split(",")
        return float(parts[0]), float(parts[1])

    @staticmethod
    def haversine_meters(lng1: float, lat1: float, lng2: float, lat2: float) -> float:
        """计算两点间球面距离（米）"""
        R = 6371000
        phi1, phi2 = math.radians(lat1), math.radians(lat2)
        dphi = math.radians(lat2 - lat1)
        dlambda = math.radians(lng2 - lng1)
        a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
        return 2 * R * math.atan2(math.sqrt(a), math.sqrt(1 - a))
