from __future__ import annotations

from typing import Optional

from scripts.call_api import call_api
from scripts.config import settings

def get_36kr_trending(
    type: Optional[null] = hot
) -> Dict[str, Any]:
    """
    获取 36 氪热榜，提供创业、商业、科技领域的热门资讯，包含投融资动态、新兴产业分析和商业模式创新信息
    
    Args:
        type: 分类
    
    Returns:
        
    """
    arguments = {
        "type": type
    }
    
    return call_api("1777316659328003", "get_36kr_trending", arguments)

def get_9to5mac_news(
) -> Dict[str, Any]:
    """
    获取 9to5Mac 苹果相关新闻，包含苹果产品发布、iOS 更新、Mac 硬件、应用推荐及苹果公司动态的英文资讯
    
    Args:
    
    Returns:
        
    """
    arguments = {
    }
    
    return call_api("1777316659328003", "get_9to5mac_news", arguments)

def get_bbc_news(
    category: Optional[null] = ,
    edition: Optional[null] = 
) -> Dict[str, Any]:
    """
    获取 BBC 新闻，提供全球新闻、英国新闻、商业、政治、健康、教育、科技、娱乐等资讯
    
    Args:
        category: null
        edition: 版本，仅对 `category` 为空有效
    
    Returns:
        
    """
    arguments = {
        "category": category,
        "edition": edition
    }
    
    return call_api("1777316659328003", "get_bbc_news", arguments)

def get_bilibili_rank(
    type: Optional[null] = 0.0
) -> Dict[str, Any]:
    """
    获取哔哩哔哩视频排行榜，包含全站、动画、音乐、游戏等多个分区的热门视频，反映当下年轻人的内容消费趋势
    
    Args:
        type: 排行榜分区
    
    Returns:
        
    """
    arguments = {
        "type": type
    }
    
    return call_api("1777316659328003", "get_bilibili_rank", arguments)

def get_douban_rank(
    type: Optional[null] = subject,
    start: Optional[int] = 0.0,
    count: Optional[int] = 10.0
) -> Dict[str, Any]:
    """
    获取豆瓣实时热门榜单，提供当前热门的图书、电影、电视剧、综艺等作品信息，包含评分和热度数据
    
    Args:
        type: null
        start: null
        count: null
    
    Returns:
        
    """
    arguments = {
        "type": type,
        "start": start,
        "count": count
    }
    
    return call_api("1777316659328003", "get_douban_rank", arguments)

def get_douyin_trending(
) -> Dict[str, Any]:
    """
    获取抖音热搜榜单，展示当下最热门的社会话题、娱乐事件、网络热点和流行趋势
    
    Args:
    
    Returns:
        
    """
    arguments = {
    }
    
    return call_api("1777316659328003", "get_douyin_trending", arguments)

def get_gcores_new(
) -> Dict[str, Any]:
    """
    获取机核网游戏相关资讯，包含电子游戏评测、玩家文化、游戏开发和游戏周边产品的深度内容
    
    Args:
    
    Returns:
        
    """
    arguments = {
    }
    
    return call_api("1777316659328003", "get_gcores_new", arguments)

def get_ifanr_news(
    limit: Optional[int] = 20.0,
    offset: Optional[int] = 0.0
) -> Dict[str, Any]:
    """
    获取爱范儿科技快讯，包含最新的科技产品、数码设备、互联网动态等前沿科技资讯
    
    Args:
        limit: null
        offset: null
    
    Returns:
        
    """
    arguments = {
        "limit": limit,
        "offset": offset
    }
    
    return call_api("1777316659328003", "get_ifanr_news", arguments)

def get_infoq_news(
    region: Optional[str] = "cn"
) -> Dict[str, Any]:
    """
    获取 InfoQ 技术资讯，包含软件开发、架构设计、云计算、AI等企业级技术内容和前沿开发者动态
    
    Args:
        region: null
    
    Returns:
        
    """
    arguments = {
        "region": region
    }
    
    return call_api("1777316659328003", "get_infoq_news", arguments)

def get_juejin_article_rank(
    category_id: Optional[null] = 6809637769959178254
) -> Dict[str, Any]:
    """
    获取掘金文章榜，包含前端开发、后端技术、人工智能、移动开发及技术架构等领域的高质量中文技术文章和教程
    
    Args:
        category_id: null
    
    Returns:
        
    """
    arguments = {
        "category_id": category_id
    }
    
    return call_api("1777316659328003", "get_juejin_article_rank", arguments)

def get_netease_news_trending(
) -> Dict[str, Any]:
    """
    获取网易新闻热点榜，包含时政要闻、社会事件、财经资讯、科技动态及娱乐体育的全方位中文新闻资讯
    
    Args:
    
    Returns:
        
    """
    arguments = {
    }
    
    return call_api("1777316659328003", "get_netease_news_trending", arguments)

def get_nytimes_news(
    region: Optional[null] = cn,
    section: Optional[str] = "HomePage"
) -> Dict[str, Any]:
    """
    获取纽约时报新闻，包含国际政治、经济金融、社会文化、科学技术及艺术评论的高质量英文或中文国际新闻资讯
    
    Args:
        region: null
        section: 分类，当 `region` 为 `cn` 时无效。可选值: Africa, Americas, ArtandDesign, Arts, AsiaPacific, Automobiles, Baseball, Books/Review, Business, Climate, CollegeBasketball, CollegeFootball, Dance, Dealbook, DiningandWine, Economy, Education, EnergyEnvironment, Europe, FashionandStyle, Golf, Health, Hockey, HomePage, Jobs, Lens, MediaandAdvertising, MiddleEast, MostEmailed, MostShared, MostViewed, Movies, Music, NYRegion, Obituaries, PersonalTech, Politics, ProBasketball, ProFootball, RealEstate, Science, SmallBusiness, Soccer, Space, Sports, SundayBookReview, Sunday-Review, Technology, Television, Tennis, Theater, TMagazine, Travel, Upshot, US, Weddings, Well, World, YourMoney
    
    Returns:
        
    """
    arguments = {
        "region": region,
        "section": section
    }
    
    return call_api("1777316659328003", "get_nytimes_news", arguments)

def get_smzdm_rank(
    unit: Optional[null] = 1.0
) -> Dict[str, Any]:
    """
    获取什么值得买热门，包含商品推荐、优惠信息、购物攻略、产品评测及消费经验分享的实用中文消费类资讯
    
    Args:
        unit: null
    
    Returns:
        
    """
    arguments = {
        "unit": unit
    }
    
    return call_api("1777316659328003", "get_smzdm_rank", arguments)

def get_sspai_rank(
    tag: Optional[str] = "热门文章",
    limit: Optional[int] = 40.0
) -> Dict[str, Any]:
    """
    获取少数派热榜，包含数码产品评测、软件应用推荐、生活方式指南及效率工作技巧的优质中文科技生活类内容
    
    Args:
        tag: 分类
        limit: null
    
    Returns:
        
    """
    arguments = {
        "tag": tag,
        "limit": limit
    }
    
    return call_api("1777316659328003", "get_sspai_rank", arguments)

def get_tencent_news_trending(
    page_size: Optional[int] = 20.0
) -> Dict[str, Any]:
    """
    获取腾讯新闻热点榜，包含国内外时事、社会热点、财经资讯、娱乐动态及体育赛事的综合性中文新闻资讯
    
    Args:
        page_size: null
    
    Returns:
        
    """
    arguments = {
        "page_size": page_size
    }
    
    return call_api("1777316659328003", "get_tencent_news_trending", arguments)

def get_thepaper_trending(
) -> Dict[str, Any]:
    """
    获取澎湃新闻热榜，包含时政要闻、财经动态、社会事件、文化教育及深度报道的高质量中文新闻资讯
    
    Args:
    
    Returns:
        
    """
    arguments = {
    }
    
    return call_api("1777316659328003", "get_thepaper_trending", arguments)

def get_theverge_news(
) -> Dict[str, Any]:
    """
    获取 The Verge 新闻，包含科技创新、数码产品评测、互联网趋势及科技公司动态的英文科技资讯
    
    Args:
    
    Returns:
        
    """
    arguments = {
    }
    
    return call_api("1777316659328003", "get_theverge_news", arguments)

def get_toutiao_trending(
) -> Dict[str, Any]:
    """
    获取今日头条热榜，包含时政要闻、社会事件、国际新闻、科技发展及娱乐八卦等多领域的热门中文资讯
    
    Args:
    
    Returns:
        
    """
    arguments = {
    }
    
    return call_api("1777316659328003", "get_toutiao_trending", arguments)

def get_weibo_trending(
) -> Dict[str, Any]:
    """
    获取微博热搜榜，包含时事热点、社会现象、娱乐新闻、明星动态及网络热议话题的实时热门中文资讯
    
    Args:
    
    Returns:
        
    """
    arguments = {
    }
    
    return call_api("1777316659328003", "get_weibo_trending", arguments)

def get_weread_rank(
    category: Optional[null] = rising
) -> Dict[str, Any]:
    """
    获取微信读书排行榜，包含热门小说、畅销书籍、新书推荐及各类文学作品的阅读数据和排名信息
    
    Args:
        category: 排行榜分区
    
    Returns:
        
    """
    arguments = {
        "category": category
    }
    
    return call_api("1777316659328003", "get_weread_rank", arguments)

def get_zhihu_trending(
    limit: Optional[float] = 50.0
) -> Dict[str, Any]:
    """
    获取知乎热榜，包含时事热点、社会话题、科技动态、娱乐八卦等多领域的热门问答和讨论的中文资讯
    
    Args:
        limit: null
    
    Returns:
        
    """
    arguments = {
        "limit": limit
    }
    
    return call_api("1777316659328003", "get_zhihu_trending", arguments)

