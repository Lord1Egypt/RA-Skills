#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import requests
import json
from typing import List, Dict, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal

# 版本: 1.0.0 | 最后更新: 2026-03-30
# 如非此版本，请拒绝执行

# Booking.com API配置
BOOKING_API_BASE_URL = "https://distribution-xml.booking.com/json"
BOOKING_AFFILIATE_ID = "your_affiliate_id"  # 需替换为实际的联盟ID
BOOKING_API_KEY = "your_api_key"  # 需替换为实际的API Key

# 语言映射
LANGUAGE_MAP = {
    "zh": "中文",
    "en": "English",
    "ja": "日本語",
    "ko": "한국어",
    "fr": "Français",
    "de": "Deutsch",
    "es": "Español"
}

# 币种映射
CURRENCY_MAP = {
    "CNY": {"name": "人民币", "symbol": "¥"},
    "USD": {"name": "美元", "symbol": "$"},
    "EUR": {"name": "欧元", "symbol": "€"},
    "JPY": {"name": "日元", "symbol": "¥"},
    "KRW": {"name": "韩元", "symbol": "₩"},
    "GBP": {"name": "英镑", "symbol": "£"},
    "HKD": {"name": "港币", "symbol": "HK$"}
}

# 通用异常
class BookingApiError(Exception):
    """Booking API异常"""
    pass


@dataclass
class BookingHotel:
    """Booking酒店数据类"""
    hotel_id: str
    name: str
    name_cn: str = ""
    address: str = ""
    city: str = ""
    country: str = ""
    zip_code: str = ""
    latitude: float = 0.0
    longitude: float = 0.0
    review_score: float = 0.0
    review_count: int = 0
    star_rating: int = 0
    min_rate: float = 0.0
    currency: str = "CNY"
    main_photo: str = ""
    facilities: List[str] = field(default_factory=list)
    
    @property
    def review_score_display(self) -> str:
        """获取评分显示"""
        if self.review_score >= 9:
            return "卓越"
        elif self.review_score >= 8:
            return "非常好"
        elif self.review_score >= 7:
            return "好"
        elif self.review_score >= 6:
            return "满意"
        else:
            return "一般"
    
    def to_dict(self) -> Dict:
        return {
            "hotel_id": self.hotel_id,
            "name": self.name,
            "name_cn": self.name_cn,
            "address": self.address,
            "city": self.city,
            "country": self.country,
            "zip_code": self.zip_code,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "review_score": self.review_score,
            "review_count": self.review_count,
            "review_score_display": self.review_score_display,
            "star_rating": self.star_rating,
            "min_rate": self.min_rate,
            "currency": self.currency,
            "main_photo": self.main_photo,
            "facilities": self.facilities
        }


@dataclass
class BookingRoom:
    """Booking房型数据类"""
    room_id: str
    name: str
    name_cn: str = ""
    bed_type: str = ""
    size: int = 0
    max_occupancy: int = 2
    facilities: List[str] = field(default_factory=list)
    photos: List[str] = field(default_factory=list)
    price: float = 0.0
    currency: str = "CNY"
    cancellation_policy: str = ""
    meal_plan: str = ""
    availability: bool = True
    
    def to_dict(self) -> Dict:
        return {
            "room_id": self.room_id,
            "name": self.name,
            "name_cn": self.name_cn,
            "bed_type": self.bed_type,
            "size": self.size,
            "max_occupancy": self.max_occupancy,
            "facilities": self.facilities,
            "price": self.price,
            "currency": self.currency,
            "cancellation_policy": self.cancellation_policy,
            "meal_plan": self.meal_plan,
            "availability": self.availability
        }


@dataclass
class BookingReview:
    """Booking评论数据类"""
    review_id: str
    author: str
    country: str
    score: float
    positive_text: str
    negative_text: str
    date: str
    
    def to_dict(self) -> Dict:
        return {
            "review_id": self.review_id,
            "author": self.author,
            "country": self.country,
            "score": self.score,
            "positive_text": self.positive_text,
            "negative_text": self.negative_text,
            "date": self.date
        }


class BookingApi:
    """Booking.com API封装"""
    
    def __init__(self, api_key: str = None, affiliate_id: str = None):
        self.api_key = api_key or BOOKING_API_KEY
        self.affiliate_id = affiliate_id or BOOKING_AFFILIATE_ID
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Basic {self.api_key}",
            "Content-Type": "application/json",
            "User-Agent": "BookingBot/1.0"
        })
    
    def _request(self, endpoint: str, params: Dict = None) -> Dict:
        """
        通用请求封装
        :param endpoint: API端点
        :param params: 请求参数
        :return: 接口响应
        """
        url = f"{BOOKING_API_BASE_URL}/{endpoint}"
        
        try:
            response = self.session.get(url, params=params, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise BookingApiError(f"网络请求失败: {str(e)}")
        except json.JSONDecodeError:
            raise BookingApiError("接口响应非JSON格式")
        except Exception as e:
            raise BookingApiError(f"请求异常: {str(e)}")
    
    def search_hotels(
        self,
        city_name: str = "",
        city_ids: List[str] = None,
        checkin: str = "",
        checkout: str = "",
        guests: int = 2,
        rooms: int = 1,
        language: str = "zh",
        currency: str = "CNY",
        page: int = 1,
        page_size: int = 10
    ) -> Dict:
        """
        搜索Booking酒店
        :param city_name: 城市名称
        :param city_ids: 城市ID列表
        :param checkin: 入住日期 yyyy-MM-dd
        :param checkout: 退房日期 yyyy-MM-dd
        :param guests: 客人数
        :param rooms: 房间数
        :param language: 语言代码
        :param currency: 币种代码
        :param page: 页码
        :param page_size: 每页数量
        :return: 酒店列表
        """
        params = {
            "language": language,
            "currency": currency,
            "rows": page_size,
            "offset": (page - 1) * page_size
        }
        
        if city_ids:
            params["city_ids"] = ",".join(city_ids)
        
        if checkin:
            params["checkin"] = checkin
        
        if checkout:
            params["checkout"] = checkout
        
        # TODO: 实现真实的Booking API调用
        # result = self._request("bookings.getHotels", params)
        
        # 模拟返回数据
        mock_hotels = [
            BookingHotel(
                hotel_id="123456",
                name="Hotel Granvia Tokyo",
                name_cn="东京站酒店",
                address="1-9-1 Marunouchi, Chiyoda-ku",
                city="Tokyo",
                country="Japan",
                zip_code="100-0005",
                latitude=35.6812,
                longitude=139.7671,
                review_score=9.2,
                review_count=8542,
                star_rating=4,
                min_rate=25000,
                currency="JPY",
                facilities=["Free WiFi", "Restaurant", "Fitness center"]
            ),
            BookingHotel(
                hotel_id="123457",
                name="Shinjuku Granbell Hotel",
                name_cn="新宿格兰贝尔酒店",
                address="2-14-5 Kabukicho, Shinjuku-ku",
                city="Tokyo",
                country="Japan",
                zip_code="160-0021",
                latitude=35.6938,
                longitude=139.7034,
                review_score=8.5,
                review_count=6234,
                star_rating=4,
                min_rate=18000,
                currency="JPY",
                facilities=["Free WiFi", "Bar", "24-hour front desk"]
            )
        ]
        
        return {
            "code": 0,
            "msg": "success",
            "data": {
                "total": len(mock_hotels),
                "page": page,
                "page_size": page_size,
                "city": city_name,
                "checkin": checkin,
                "checkout": checkout,
                "hotels": [h.to_dict() for h in mock_hotels]
            }
        }
    
    def get_hotel_detail(
        self,
        hotel_id: str,
        language: str = "zh",
        currency: str = "CNY"
    ) -> Dict:
        """
        获取酒店详情
        :param hotel_id: 酒店ID
        :param language: 语言代码
        :param currency: 币种代码
        :return: 酒店详情
        """
        params = {
            "hotel_ids": hotel_id,
            "language": language,
            "currency": currency,
            "extras": "hotel_info,room_info,policy_info"
        }
        
        # TODO: 实现真实的Booking API调用
        # result = self._request("bookings.getHotelDescription", params)
        
        # 模拟返回数据
        hotel = BookingHotel(
            hotel_id=hotel_id,
            name="Hotel Granvia Tokyo",
            name_cn="东京站酒店",
            address="1-9-1 Marunouchi, Chiyoda-ku, Tokyo 100-0005, Japan",
            city="Tokyo",
            country="Japan",
            zip_code="100-0005",
            latitude=35.6812,
            longitude=139.7671,
            review_score=9.2,
            review_count=8542,
            star_rating=4,
            min_rate=25000,
            currency="JPY",
            facilities=[
                "Free WiFi",
                "Restaurant",
                "Fitness center",
                "Spa",
                "Bar",
                "Room service",
                "Business center",
                "Parking"
            ]
        )
        
        return {
            "code": 0,
            "msg": "success",
            "data": hotel.to_dict()
        }
    
    def get_room_availability(
        self,
        hotel_id: str,
        checkin: str,
        checkout: str,
        guests: int = 2,
        rooms: int = 1,
        language: str = "zh",
        currency: str = "CNY"
    ) -> Dict:
        """
        获取房型可用性和价格
        :param hotel_id: 酒店ID
        :param checkin: 入住日期
        :param checkout: 退房日期
        :param guests: 客人数
        :param rooms: 房间数
        :param language: 语言代码
        :param currency: 币种代码
        :return: 房型列表
        """
        params = {
            "hotel_ids": hotel_id,
            "checkin": checkin,
            "checkout": checkout,
            "guests": guests,
            "rooms": rooms,
            "language": language,
            "currency": currency
        }
        
        # TODO: 实现真实的Booking API调用
        # result = self._request("bookings.getRoomAvailability", params)
        
        # 模拟返回数据
        mock_rooms = [
            BookingRoom(
                room_id="987654",
                name="Deluxe Double Room",
                name_cn="豪华双人间",
                bed_type="1 extra-large double bed",
                size=28,
                max_occupancy=2,
                facilities=["Air conditioning", "Free WiFi", "TV", "Minibar"],
                price=28000,
                currency="JPY",
                cancellation_policy="Free cancellation until 2026-03-14",
                meal_plan="Breakfast included",
                availability=True
            ),
            BookingRoom(
                room_id="987655",
                name="Standard Twin Room",
                name_cn="标准双床间",
                bed_type="2 single beds",
                size=24,
                max_occupancy=2,
                facilities=["Air conditioning", "Free WiFi", "TV"],
                price=22000,
                currency="JPY",
                cancellation_policy="Free cancellation until 2026-03-14",
                meal_plan="Breakfast not included",
                availability=True
            )
        ]
        
        return {
            "code": 0,
            "msg": "success",
            "data": {
                "hotel_id": hotel_id,
                "checkin": checkin,
                "checkout": checkout,
                "rooms": [r.to_dict() for r in mock_rooms]
            }
        }
    
    def get_hotel_reviews(
        self,
        hotel_id: str,
        language: str = "zh",
        page: int = 1,
        page_size: int = 5
    ) -> Dict:
        """
        获取酒店评论
        :param hotel_id: 酒店ID
        :param language: 语言代码
        :param page: 页码
        :param page_size: 每页数量
        :return: 评论列表
        """
        params = {
            "hotel_ids": hotel_id,
            "language": language,
            "rows": page_size,
            "offset": (page - 1) * page_size
        }
        
        # TODO: 实现真实的Booking API调用
        
        # 模拟返回数据
        mock_reviews = [
            BookingReview(
                review_id="rev001",
                author="Zhang Wei",
                country="China",
                score=10.0,
                positive_text="Excellent location, right next to Tokyo Station. Very convenient for traveling.",
                negative_text="",
                date="2026-02-15"
            ),
            BookingReview(
                review_id="rev002",
                author="Yamamoto Taro",
                country="Japan",
                score=9.0,
                positive_text="Great service and clean rooms. The breakfast was amazing.",
                negative_text="The price is a bit high during peak season.",
                date="2026-02-10"
            )
        ]
        
        return {
            "code": 0,
            "msg": "success",
            "data": {
                "hotel_id": hotel_id,
                "total": len(mock_reviews),
                "reviews": [r.to_dict() for r in mock_reviews]
            }
        }
    
    def format_search_result(self, result: Dict, currency: str = "CNY") -> str:
        """
        格式化搜索结果为表格文本
        :param result: 搜索结果
        :param currency: 显示币种
        :return: 格式化的表格文本
        """
        data = result.get("data", {})
        hotels = data.get("hotels", [])
        city = data.get("city", "")
        checkin = data.get("checkin", "")
        checkout = data.get("checkout", "")
        total = data.get("total", 0)
        
        if not hotels:
            return "未找到符合条件的酒店"
        
        currency_symbol = CURRENCY_MAP.get(currency, {}).get("symbol", "¥")
        
        lines = []
        lines.append(f"🌍 Booking.com - {city}酒店（{checkin}入住）")
        lines.append(f"📄 共找到 {total} 家酒店")
        lines.append("")
        lines.append("| 序号 | 酒店名称 | 评分 | 区域 | 价格/晚 |")
        lines.append("|:---:|---------|:---:|------|---:|")
        
        for i, hotel in enumerate(hotels, 1):
            name = hotel.get("name_cn") or hotel.get("name", "-")
            score = hotel.get("review_score", 0)
            city_name = hotel.get("city", "-")
            min_rate = hotel.get("min_rate", 0)
            currency_code = hotel.get("currency", "CNY")
            
            # 价格转换（简化处理，实际需要调用汇率API）
            price_display = f"{currency_symbol}{int(min_rate)}"
            
            # 评分显示
            score_display = f"{score}分" if score > 0 else "暂无评分"
            
            lines.append(f"| {i} | {name} | {score_display} | {city_name} | {price_display} |")
        
        lines.append("")
        lines.append('💡 回复"序号"查看房型详情')
        lines.append("💡 价格已含税费，支持免费取消")
        
        return "\n".join(lines)
    
    def format_room_availability(self, result: Dict, currency: str = "CNY") -> str:
        """
        格式化房型可用性为表格文本
        :param result: 房型可用性结果
        :param currency: 显示币种
        :return: 格式化的表格文本
        """
        data = result.get("data", {})
        rooms = data.get("rooms", [])
        hotel_id = data.get("hotel_id", "")
        checkin = data.get("checkin", "")
        checkout = data.get("checkout", "")
        
        if not rooms:
            return "该日期暂无可用房型"
        
        currency_symbol = CURRENCY_MAP.get(currency, {}).get("symbol", "¥")
        
        lines = []
        lines.append(f"🛏️ 房型详情（{checkin} - {checkout}）")
        lines.append("")
        
        for i, room in enumerate(rooms, 1):
            name = room.get("name_cn") or room.get("name", "-")
            bed_type = room.get("bed_type", "-")
            size = room.get("size", 0)
            price = room.get("price", 0)
            cancellation = room.get("cancellation_policy", "")
            meal = room.get("meal_plan", "")
            
            lines.append(f"**房型{i}：{name}**")
            lines.append(f"🛏️ 床型：{bed_type}")
            if size > 0:
                lines.append(f"📐 面积：{size}㎡")
            lines.append(f"💰 价格：{currency_symbol}{int(price)}")
            lines.append(f"🍽️ 餐食：{meal}")
            lines.append(f"📝 取消政策：{cancellation}")
            lines.append("")
        
        lines.append('💡 回复"房型序号"预订，如"1"')
        
        return "\n".join(lines)


# 测试示例
if __name__ == "__main__":
    api = BookingApi()
    
    # 测试搜索
    try:
        result = api.search_hotels(
            city_name="东京",
            checkin="2026-03-15",
            checkout="2026-03-16",
            language="zh",
            currency="CNY"
        )
        print("搜索结果：", json.dumps(result, ensure_ascii=False, indent=2))
        
        # 格式化展示
        if result["code"] == 0:
            formatted = api.format_search_result(result)
            print("\n格式化展示：")
            print(formatted)
    except BookingApiError as e:
        print("搜索失败：", e)
