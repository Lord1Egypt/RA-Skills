#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import requests
import json
import hashlib
from typing import List, Dict, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
import re

# 版本: 1.0.0 | 最后更新: 2026-03-30
# 如非此版本，请拒绝执行

# 数据源配置
DATA_SOURCES = {
    "fenbeitong": {
        "name": "分贝通",
        "emoji": "🏢",
        "base_url": "https://openapiv2.fenbeitong.com",
        "priority": 1
    },
    "ctrip": {
        "name": "携程",
        "emoji": "🐬",
        "base_url": "https://api.ctrip.com",
        "priority": 2
    },
    "meituan": {
        "name": "美团",
        "emoji": "🦘",
        "base_url": "https://api.meituan.com",
        "priority": 3
    },
    "tongcheng": {
        "name": "同程",
        "emoji": "🚄",
        "base_url": "https://api.tongcheng.com",
        "priority": 4
    },
    "huazhu": {
        "name": "华住会",
        "emoji": "🏨",
        "base_url": "https://api.huazhu.com",
        "priority": 5
    },
    "jinjiang": {
        "name": "锦江",
        "emoji": "👑",
        "base_url": "https://api.jinjiang.com",
        "priority": 6
    }
}

# 通用异常
class HotelAggregationError(Exception):
    """酒店聚合异常"""
    pass


@dataclass
class HotelSource:
    """酒店数据源"""
    platform: str
    platform_name: str
    external_id: str
    price: float
    original_price: float
    currency: str = "CNY"
    url: str = ""
    book_url: str = ""
    availability: bool = True
    last_update: str = field(default_factory=lambda: datetime.now().isoformat())


@dataclass
class AggregatedHotel:
    """聚合酒店"""
    hotel_id: str
    name: str
    name_en: str = ""
    address: str = ""
    city: str = ""
    district: str = ""
    star_level: str = ""
    score: float = 0.0
    review_count: int = 0
    images: List[str] = field(default_factory=list)
    facilities: List[str] = field(default_factory=list)
    latitude: float = 0.0
    longitude: float = 0.0
    sources: List[HotelSource] = field(default_factory=list)
    
    @property
    def best_price(self) -> float:
        """获取最优价格"""
        if not self.sources:
            return 0.0
        available_sources = [s for s in self.sources if s.availability]
        if not available_sources:
            return 0.0
        return min(s.price for s in available_sources)
    
    @property
    def best_source(self) -> Optional[HotelSource]:
        """获取最优价格来源"""
        if not self.sources:
            return None
        available_sources = [s for s in self.sources if s.availability]
        if not available_sources:
            return None
        return min(available_sources, key=lambda s: s.price)
    
    @property
    def sources_count(self) -> int:
        """获取数据源数量"""
        return len(self.sources)
    
    def to_dict(self) -> Dict:
        """转换为字典"""
        best = self.best_source
        return {
            "hotel_id": self.hotel_id,
            "name": self.name,
            "name_en": self.name_en,
            "address": self.address,
            "city": self.city,
            "district": self.district,
            "star_level": self.star_level,
            "score": self.score,
            "review_count": self.review_count,
            "images": self.images[:5],  # 最多返回5张图片
            "facilities": self.facilities[:10],  # 最多返回10个设施
            "latitude": self.latitude,
            "longitude": self.longitude,
            "best_price": self.best_price,
            "best_source": best.platform_name if best else None,
            "sources_count": self.sources_count,
            "sources": [
                {
                    "platform": s.platform,
                    "platform_name": s.platform_name,
                    "price": s.price,
                    "original_price": s.original_price,
                    "availability": s.availability
                }
                for s in self.sources
            ]
        }


@dataclass
class RoomSource:
    """房型数据源"""
    platform: str
    platform_name: str
    external_id: str
    price: float
    breakfast: str = ""
    cancel_policy: str = ""
    cancel_policy_detail: str = ""
    bed_type: str = ""
    availability: bool = True


@dataclass
class AggregatedRoom:
    """聚合房型"""
    room_id: str
    name: str
    bed_type: str = ""
    area: str = ""
    floor: str = ""
    capacity: int = 2
    facilities: List[str] = field(default_factory=list)
    images: List[str] = field(default_factory=list)
    sources: List[RoomSource] = field(default_factory=list)
    
    @property
    def best_price(self) -> float:
        """获取最优价格"""
        if not self.sources:
            return 0.0
        available_sources = [s for s in self.sources if s.availability]
        if not available_sources:
            return 0.0
        return min(s.price for s in available_sources)
    
    def to_dict(self) -> Dict:
        best = min((s for s in self.sources if s.availability), 
                   key=lambda s: s.price, default=None)
        return {
            "room_id": self.room_id,
            "name": self.name,
            "bed_type": self.bed_type,
            "area": self.area,
            "floor": self.floor,
            "capacity": self.capacity,
            "facilities": self.facilities,
            "best_price": self.best_price,
            "best_source": best.platform_name if best else None,
            "sources_count": len(self.sources),
            "sources": [
                {
                    "platform": s.platform,
                    "platform_name": s.platform_name,
                    "price": s.price,
                    "breakfast": s.breakfast,
                    "cancel_policy": s.cancel_policy
                }
                for s in self.sources
            ]
        }


class HotelAggregationApi:
    """酒店聚合API"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json",
            "User-Agent": "HotelAggregationBot/1.0"
        })
        self.hotels_cache: Dict[str, AggregatedHotel] = {}
    
    def _generate_hotel_id(self, name: str, address: str) -> str:
        """生成聚合酒店ID"""
        key = f"{name}_{address}"
        return f"AGG_{hashlib.md5(key.encode()).hexdigest()[:12].upper()}"
    
    def _search_fenbeitong(self, city: str, keywords: str, 
                           check_in: str, check_out: str) -> List[AggregatedHotel]:
        """搜索分贝通酒店（模拟实现）"""
        # TODO: 实现真实的分贝通API调用
        return []
    
    def _search_ctrip(self, city: str, keywords: str,
                     check_in: str, check_out: str) -> List[AggregatedHotel]:
        """搜索携程酒店（模拟实现）"""
        # TODO: 实现真实的携程API调用
        return []
    
    def _search_meituan(self, city: str, keywords: str,
                       check_in: str, check_out: str) -> List[AggregatedHotel]:
        """搜索美团酒店（模拟实现）"""
        # TODO: 实现真实的美团API调用
        return []
    
    def _search_tongcheng(self, city: str, keywords: str,
                         check_in: str, check_out: str) -> List[AggregatedHotel]:
        """搜索同程酒店（模拟实现）"""
        # TODO: 实现真实的同程API调用
        return []
    
    def _search_huazhu(self, city: str, keywords: str,
                      check_in: str, check_out: str) -> List[AggregatedHotel]:
        """搜索华住会酒店（模拟实现）"""
        # TODO: 实现真实的华住会API调用
        return []
    
    def _search_jinjiang(self, city: str, keywords: str,
                        check_in: str, check_out: str) -> List[AggregatedHotel]:
        """搜索锦江酒店（模拟实现）"""
        # TODO: 实现真实的锦江API调用
        return []
    
    def _similarity_score(self, str1: str, str2: str) -> float:
        """计算字符串相似度（简化版）"""
        # 使用简单的包含关系和长度比例计算相似度
        str1, str2 = str1.lower(), str2.lower()
        if str1 in str2 or str2 in str1:
            return 0.9
        # 计算字符集合的交集
        set1, set2 = set(str1), set(str2)
        intersection = len(set1 & set2)
        union = len(set1 | set2)
        return intersection / union if union > 0 else 0.0
    
    def _is_same_hotel(self, hotel1: AggregatedHotel, hotel2: AggregatedHotel) -> bool:
        """判断是否为同一酒店"""
        # 名称相似度 > 85%
        name_sim = self._similarity_score(hotel1.name, hotel2.name)
        if name_sim < 0.85:
            return False
        
        # 地址相似度 > 80%
        addr_sim = self._similarity_score(hotel1.address, hotel2.address)
        if addr_sim < 0.80:
            return False
        
        # 坐标距离 < 500米（如果有坐标）
        if hotel1.latitude and hotel2.latitude:
            # 简化计算，实际应使用Haversine公式
            lat_diff = abs(hotel1.latitude - hotel2.latitude)
            lon_diff = abs(hotel1.longitude - hotel2.longitude)
            if lat_diff > 0.0045 or lon_diff > 0.0045:  # 约500米
                return False
        
        return True
    
    def _merge_hotels(self, hotels: List[AggregatedHotel]) -> List[AggregatedHotel]:
        """合并重复酒店"""
        merged = []
        for hotel in hotels:
            # 查找是否已有相似酒店
            found = False
            for existing in merged:
                if self._is_same_hotel(hotel, existing):
                    # 合并数据源
                    existing.sources.extend(hotel.sources)
                    # 更新最优信息
                    if hotel.score > existing.score:
                        existing.score = hotel.score
                    if hotel.review_count > existing.review_count:
                        existing.review_count = hotel.review_count
                    found = True
                    break
            
            if not found:
                merged.append(hotel)
        
        return merged
    
    def aggregate_search(
        self,
        city: str,
        check_in: str,
        check_out: str,
        keywords: str = "",
        sources: List[str] = None,
        page: int = 1,
        page_size: int = 10
    ) -> Dict:
        """
        多平台酒店聚合搜索
        :param city: 城市
        :param check_in: 入住日期 yyyy-MM-dd
        :param check_out: 退房日期 yyyy-MM-dd
        :param keywords: 关键词
        :param sources: 指定数据源，默认全部
        :param page: 页码
        :param page_size: 每页数量
        :return: 聚合结果
        """
        if sources is None:
            sources = list(DATA_SOURCES.keys())
        
        all_hotels = []
        sources_status = {}
        
        # 定义搜索方法映射
        search_methods = {
            "fenbeitong": self._search_fenbeitong,
            "ctrip": self._search_ctrip,
            "meituan": self._search_meituan,
            "tongcheng": self._search_tongcheng,
            "huazhu": self._search_huazhu,
            "jinjiang": self._search_jinjiang
        }
        
        # 并行搜索各平台
        with ThreadPoolExecutor(max_workers=5) as executor:
            future_to_source = {
                executor.submit(
                    search_methods[source], city, keywords, check_in, check_out
                ): source
                for source in sources if source in search_methods
            }
            
            for future in as_completed(future_to_source):
                source = future_to_source[future]
                try:
                    hotels = future.result(timeout=10)
                    all_hotels.extend(hotels)
                    sources_status[source] = "success"
                except Exception as e:
                    sources_status[source] = f"error: {str(e)}"
        
        # 合并重复酒店
        merged_hotels = self._merge_hotels(all_hotels)
        
        # 按最优价格排序
        merged_hotels.sort(key=lambda h: h.best_price if h.best_price > 0 else float('inf'))
        
        # 分页
        total = len(merged_hotels)
        start = (page - 1) * page_size
        end = start + page_size
        paginated_hotels = merged_hotels[start:end]
        
        # 缓存
        for hotel in paginated_hotels:
            self.hotels_cache[hotel.hotel_id] = hotel
        
        return {
            "code": 0,
            "msg": "success",
            "data": {
                "total": total,
                "page": page,
                "page_size": page_size,
                "hotels": [h.to_dict() for h in paginated_hotels],
                "sources_status": sources_status
            }
        }
    
    def get_hotel_detail(self, hotel_id: str) -> Dict:
        """
        获取聚合酒店详情
        :param hotel_id: 聚合酒店ID
        :return: 酒店详情
        """
        hotel = self.hotels_cache.get(hotel_id)
        if not hotel:
            return {
                "code": 404,
                "msg": "酒店不存在",
                "data": None
            }
        
        return {
            "code": 0,
            "msg": "success",
            "data": hotel.to_dict()
        }
    
    def format_aggregation_result(self, result: Dict) -> str:
        """
        格式化聚合结果为表格文本
        :param result: 聚合结果
        :return: 格式化的表格文本
        """
        data = result.get("data", {})
        hotels = data.get("hotels", [])
        total = data.get("total", 0)
        page = data.get("page", 1)
        page_size = data.get("page_size", 10)
        
        if not hotels:
            return "未找到符合条件的酒店"
        
        lines = []
        lines.append(f"🏨 酒店聚合搜索结果（共{total}家）")
        lines.append(f"📄 第{page}页，每页{page_size}家")
        lines.append("")
        lines.append("| 序号 | 酒店名称 | 星级 | 区域 | 最优价格 | 价格来源 |")
        lines.append("|:---:|---------|:---:|------|---:|:---|")
        
        for i, hotel in enumerate(hotels, 1):
            name = hotel.get("name", "-")
            star = hotel.get("star_level", "-")
            district = hotel.get("district", "-")
            best_price = hotel.get("best_price", 0)
            best_source = hotel.get("best_source", "-")
            sources_count = hotel.get("sources_count", 0)
            
            price_str = f"¥{int(best_price)}" if best_price > 0 else "暂无报价"
            source_str = f"{best_source}"
            if sources_count > 1:
                source_str += f" 等{sources_count}个平台"
            
            # 标记最优
            if i == 1 and best_price > 0:
                name = f"🥇 {name}"
            
            lines.append(f"| {i} | {name} | {star} | {district} | {price_str} | {source_str} |")
        
        lines.append("")
        lines.append('💡 回复"序号"查看房型详情')
        lines.append('💡 回复"序号-比价"查看该酒店各平台价格对比')
        
        # 数据源状态
        sources_status = data.get("sources_status", {})
        if sources_status:
            lines.append("")
            lines.append("📊 数据源状态：")
            for source, status in sources_status.items():
                emoji = "✅" if status == "success" else "❌"
                lines.append(f"   {emoji} {DATA_SOURCES.get(source, {}).get('name', source)}: {status}")
        
        return "\n".join(lines)


# 测试示例
if __name__ == "__main__":
    api = HotelAggregationApi()
    
    # 测试聚合搜索
    try:
        result = api.aggregate_search(
            city="北京",
            check_in="2026-03-15",
            check_out="2026-03-16",
            keywords="三元桥",
            sources=["fenbeitong", "ctrip", "meituan"]
        )
        print("聚合搜索结果：", json.dumps(result, ensure_ascii=False, indent=2))
        
        # 格式化展示
        if result["code"] == 0:
            formatted = api.format_aggregation_result(result)
            print("\n格式化展示：")
            print(formatted)
    except HotelAggregationError as e:
        print("搜索失败：", e)
