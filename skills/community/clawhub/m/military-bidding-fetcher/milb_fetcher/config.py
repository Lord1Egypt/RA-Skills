#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
配置加载模块 (milb-fetcher)

按优先级读取 .env 配置，缺失时使用默认值：
  1. ~/.config/milb-fetcher/.env  （用户全局配置）
  2. ./.env                        （当前运行目录，最高优先级）
"""

from pathlib import Path
from typing import Dict, List, Optional


# 默认配置值 (FETCHER_* 前缀)
DEFAULTS = {
    'FETCHER_KEYWORDS': '体系,模型,仿真,数据,决策,规划,分析,智能,AI,软件,系统,信息,算法,效能',
    'FETCHER_EXCLUDE_KEYWORDS': '体能,训练鞋,鞋类,服装,被装,医疗,药品,器械,膝关节,光纤,电梯,物业,绿化,装修,工程,建材,食材,食品,副食',
    'FETCHER_HIGH_VALUE_KEYWORDS': '模型,仿真,数据,决策,分析,智能,AI,软件,意向',
    'FETCHER_REGIONS': '北京,天津,河北,湖北,湖南',
}


def _parse_env_file(path: Path) -> Dict:
    """解析单个 .env 文件，返回配置字典"""
    config = {}
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                config[key.strip()] = value.strip()
    return config


def load_config() -> Dict:
    """
    按优先级加载 .env 配置，后加载的优先级更高：
    1. ~/.config/milb-fetcher/.env  （用户全局配置）
    2. ./.env                        （当前运行目录，最高优先级）

    Returns:
        Dict: 合并后的配置字典
    """
    candidates = [
        Path.home() / '.config' / 'milb-fetcher' / '.env',
        Path.cwd() / '.env',
    ]
    config = {}
    for path in candidates:
        if path.exists():
            config.update(_parse_env_file(path))
    return config


def get_config(key: str, default: Optional[str] = None) -> Optional[str]:
    """
    获取单个配置项

    Args:
        key: 配置键名
        default: 默认值，如果 .env 中未定义则使用此值

    Returns:
        配置值字符串
    """
    config = load_config()
    return config.get(key, default or DEFAULTS.get(key))


def get_keywords() -> List[str]:
    """获取核心关键词列表"""
    value = get_config('FETCHER_KEYWORDS')
    return [k.strip() for k in value.split(',') if k.strip()] if value else []


def get_exclude_keywords() -> List[str]:
    """获取排除关键词列表"""
    value = get_config('FETCHER_EXCLUDE_KEYWORDS')
    return [k.strip() for k in value.split(',') if k.strip()] if value else []


def get_high_value_keywords() -> List[str]:
    """获取高价值关键词列表"""
    value = get_config('FETCHER_HIGH_VALUE_KEYWORDS')
    return [k.strip() for k in value.split(',') if k.strip()] if value else []


def get_proxies() -> Optional[dict]:
    """返回 requests 用的 proxies 字典，FETCHER_USE_PROXY=true 时生效，否则返回 None"""
    use_proxy = get_config('FETCHER_USE_PROXY', 'false').lower() == 'true'
    if not use_proxy:
        return None
    proxy_url = get_config('FETCHER_PROXY')
    if not proxy_url:
        return None
    return {'http': proxy_url, 'https': proxy_url}


def get_output_dir() -> str:
    """获取输出目录"""
    return get_config('FETCHER_OUTPUT_DIR', '~/.openclaw/workspace/military-bidding')


def get_regions() -> Dict[str, str]:
    """获取地区字典"""
    value = get_config('FETCHER_REGIONS')
    region_codes = {
        '北京': '110000', '天津': '120000', '河北': '130000',
        '山西': '140000', '内蒙古': '150000', '辽宁': '210000',
        '吉林': '220000', '黑龙江': '230000', '上海': '310000',
        '江苏': '320000', '浙江': '330000', '安徽': '340000',
        '福建': '350000', '江西': '360000', '山东': '370000',
        '河南': '410000', '湖北': '420000', '湖南': '430000',
        '广东': '440000', '广西': '450000', '海南': '460000',
        '重庆': '500000', '四川': '510000', '贵州': '520000',
        '云南': '530000', '西藏': '540000', '陕西': '610000',
        '甘肃': '620000', '青海': '630000', '宁夏': '640000',
        '新疆': '650000'
    }
    if not value:
        return {}
    region_names = [r.strip() for r in value.split(',') if r.strip()]
    return {name: region_codes.get(name, '') for name in region_names if name in region_codes}


if __name__ == '__main__':
    # 测试输出
    print("=== milb-fetcher 配置加载测试 ===")
    print(f"核心关键词: {get_keywords()}")
    print(f"排除关键词: {get_exclude_keywords()}")
    print(f"高价值关键词: {get_high_value_keywords()}")
    print(f"地区: {get_regions()}")
