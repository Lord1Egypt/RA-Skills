"""OK.com 数据类型定义"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Locale:
    """当前区域设置"""
    country: str          # e.g. "singapore"
    country_code: str     # e.g. "SG"
    subdomain: str        # e.g. "sg"
    city: str             # e.g. "singapore"
    lang: str             # e.g. "en"
    bus_id: int           # e.g. 100005

    def base_url(self) -> str:
        return f"https://{self.subdomain}.ok.com/{self.lang}/city-{self.city}/"


@dataclass
class City:
    """城市信息（从 allCities API 返回）"""
    local_id: str         # e.g. "14"
    name: str             # e.g. "Toronto"
    code: str             # e.g. "toronto"


@dataclass
class Category:
    """分类信息（从 getLevelCates API 返回）"""
    category_id: str
    name: str
    code: str
    children: list[Category] = field(default_factory=list)


@dataclass
class Listing:
    """帖子列表项"""
    title: str
    price: str | None = None
    location: str | None = None
    url: str | None = None
    image_url: str | None = None
    listing_id: str | None = None


@dataclass
class ListingDetail:
    """帖子完整详情"""
    title: str
    price: str | None = None
    description: str | None = None
    location: str | None = None
    seller_name: str | None = None
    images: list[str] = field(default_factory=list)
    url: str | None = None
    listing_id: str | None = None
    category: str | None = None
    posted_time: str | None = None
    features: dict[str, str] = field(default_factory=dict)


@dataclass
class SearchResult:
    """搜索结果"""
    keyword: str
    total_count: int | None = None
    listings: list[Listing] = field(default_factory=list)
    locale: Locale | None = None
