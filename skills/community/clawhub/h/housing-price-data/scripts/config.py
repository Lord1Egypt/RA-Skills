# -*- coding: utf-8 -*-
"""
配置文件 - 住宅价格指数数据获取
"""

# 国家统计局 RSS 地址
RSS_URL = "https://www.stats.gov.cn/sj/zxfb/rss.xml"

# 公告标题关键字
TITLE_KEY = "70个大中城市商品住宅销售价格变动情况"

# 指标名称
INDICATORS = {
    "new": "新建商品住宅销售价格指数",
    "used": "二手住宅销售价格指数",
    "new_cat": "新建商品住宅销售价格分类指数",
    "used_cat": "二手住宅销售价格分类指数",
}

# 70 个大中城市
SUPPORTED_CITIES = [
    "北京", "天津", "石家庄", "太原", "呼和浩特", "沈阳", "大连", "长春", "哈尔滨", "上海",
    "南京", "杭州", "宁波", "合肥", "福州", "厦门", "南昌", "济南", "青岛", "郑州",
    "武汉", "长沙", "广州", "深圳", "南宁", "海口", "重庆", "成都", "贵阳", "昆明",
    "西安", "兰州", "西宁", "银川", "乌鲁木齐", "唐山", "秦皇岛", "包头", "丹东", "锦州",
    "吉林", "牡丹江", "无锡", "徐州", "扬州", "温州", "金华", "蚌埠", "安庆", "泉州",
    "九江", "赣州", "烟台", "济宁", "洛阳", "平顶山", "宜昌", "襄阳", "岳阳", "常德",
    "韶关", "湛江", "惠州", "桂林", "北海", "三亚", "泸州", "南充", "遵义", "大理",
]

# 城市常见别名
CITY_ALIASES = {
    "北京市": "北京",
    "天津市": "天津",
    "上海市": "上海",
    "重庆市": "重庆",
}

# 指标别名（用于命令行参数）
METRIC_ALIASES = {
    "环比": ["环比", "环比指数", "月环比", "mom", "MoM"],
    "同比": ["同比", "同比指数", "年同比", "yoy", "YoY"],
    "定基": ["定基", "定基指数", "fixed-base"],
}

# 有效指标列表（用于验证）
VALID_METRICS = list(METRIC_ALIASES.keys())

# 请求配置
REQUEST_CONFIG = {
    "timeout": 20,
    "max_attempts": 3,
    "retry_delays": [0.4, 0.8, 1.5],
    "headers": {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        "Referer": "https://www.stats.gov.cn/",
    },
}

# 缓存配置
CACHE_CONFIG = {
    "enabled": True,
    "ttl_seconds": 3600,  # 1小时缓存
    "max_size": 100,
}

# 默认参数
DEFAULTS = {
    "city": "武汉",
    "metrics": "环比,同比",
    "limit": 100,
}
