# -*- coding: utf-8 -*-
"""
自定义异常类
"""


class HousingDataError(Exception):
    """基础异常类"""


class NetworkError(HousingDataError):
    """网络请求错误"""

    def __init__(self, message: str, url: str = None, status_code: int = None):
        self.url = url
        self.status_code = status_code
        super().__init__(message)


class ParseError(HousingDataError):
    """数据解析错误"""

    def __init__(self, message: str, period: str = None):
        self.period = period
        super().__init__(message)


class CityNotFoundError(HousingDataError):
    """城市未找到错误"""

    def __init__(self, city: str, available_cities: list = None):
        self.city = city
        self.available_cities = available_cities or []
        message = f"城市「{city}」未在70个大中城市列表中"
        super().__init__(message)


class RSSFeedError(HousingDataError):
    """RSS 获取错误"""

    def __init__(self, message: str, feed_url: str = None):
        self.feed_url = feed_url
        super().__init__(message)


class DataUnavailableError(HousingDataError):
    """数据不可用错误"""

    def __init__(self, message: str, period: str = None, city: str = None):
        self.period = period
        self.city = city
        super().__init__(message)
