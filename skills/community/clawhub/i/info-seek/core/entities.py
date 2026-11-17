#!/usr/bin/env python3
"""
core/entities.py — Infoseek 跨语言实体词典（v2.0.0 新增，v2.1.0 元数据扩展）

146 个实体条目（v2.0.1 = 95；v2.1.0 不扩展），覆盖 5 个类别：
- ORG: 组织/公司
- PRODUCT: 产品/品牌
- TECH: 技术/框架
- PERSON: 人物
- METRIC: 度量/单位

每条目含 aliases（跨语言变体）+ v2.1.0 元数据：
- created_at / last_verified_at / last_seen_at
- hit_count_30d
- source (manual / llm / wikidata)
- confidence (0-1)

v2.1.0 变更：所有实体已自动迁移含默认元数据（core/entity_meta.migrate_entities）。

- ORG: 组织/公司
- PRODUCT: 产品/品牌
- TECH: 技术/框架
- PERSON: 人物
- METRIC: 度量/单位

每条目含 aliases（跨语言变体），用于词典匹配 NER。
"""

import json
import os
import re
from datetime import date
from pathlib import Path
from typing import List, Dict, Optional

# G8-apply: 公共入口类型契约守卫（纯 stdlib，scripts/entry_guard.py）
import sys as _eg_sys
from pathlib import Path as _eg_p
_eg_dir = str(_eg_p(__file__).resolve().parent.parent / 'scripts')
if _eg_dir not in _eg_sys.path:
    _eg_sys.path.insert(0, _eg_dir)
from entry_guard import (require_text, require_mapping, require_sequence, coerce_mapping_list)

# ═══════════════════════════════════════════════════════════════
# ORG: 公司/组织（50+）
# ═══════════════════════════════════════════════════════════════

ORG_ENTITIES = [
    # AI 科技公司
{'name': 'OpenAI', 'aliases': ['openai', 'OpenAI Inc.', 'OPENAI', 'open ai'], 'category': 'AI', 'created_at': '2026-08-08', 'last_verified_at': '2026-08-08', 'last_seen_at': '2026-08-08', 'hit_count_30d': 0, 'source': 'manual', 'confidence': 1.0},
{'name': 'Anthropic', 'aliases': ['anthropic', 'Anthropic PBC', 'Claude AI'], 'category': 'AI', 'created_at': '2026-08-08', 'last_verified_at': '2026-08-08', 'last_seen_at': '2026-08-08', 'hit_count_30d': 0, 'source': 'manual', 'confidence': 1.0},
{'name': 'Google', 'aliases': ['google', 'Google Inc.', 'GOOG', 'Alphabet'], 'category': 'TECH', 'created_at': '2026-08-08', 'last_verified_at': '2026-08-08', 'last_seen_at': '2026-08-08', 'hit_count_30d': 0, 'source': 'manual', 'confidence': 1.0},
{'name': 'Microsoft', 'aliases': ['microsoft', 'MSFT', 'Microsoft Corp.', '微软'], 'category': 'TECH', 'created_at': '2026-08-08', 'last_verified_at': '2026-08-08', 'last_seen_at': '2026-08-08', 'hit_count_30d': 0, 'source': 'manual', 'confidence': 1.0},
{'name': 'Meta', 'aliases': ['meta', 'Facebook', 'META', 'Instagram'], 'category': 'TECH', 'created_at': '2026-08-08', 'last_verified_at': '2026-08-08', 'last_seen_at': '2026-08-08', 'hit_count_30d': 0, 'source': 'manual', 'confidence': 1.0},
{'name': 'Apple', 'aliases': ['apple', 'AAPL', 'Apple Inc.', '苹果'], 'category': 'TECH', 'created_at': '2026-08-08', 'last_verified_at': '2026-08-08', 'last_seen_at': '2026-08-08', 'hit_count_30d': 0, 'source': 'manual', 'confidence': 1.0},
{'name': 'Amazon', 'aliases': ['amazon', 'AWS', 'AMZN'], 'category': 'TECH', 'created_at': '2026-08-08', 'last_verified_at': '2026-08-08', 'last_seen_at': '2026-08-08', 'hit_count_30d': 0, 'source': 'manual', 'confidence': 1.0},
{'name': 'NVIDIA', 'aliases': ['nvidia', 'NVDA', 'GPU'], 'category': 'HARDWARE', 'created_at': '2026-08-08', 'last_verified_at': '2026-08-08', 'last_seen_at': '2026-08-08', 'hit_count_30d': 0, 'source': 'manual', 'confidence': 1.0},
{'name': 'Mistral AI', 'aliases': ['mistral', 'Mistral AI', 'mistral ai'], 'category': 'AI', 'created_at': '2026-08-08', 'last_verified_at': '2026-08-08', 'last_seen_at': '2026-08-08', 'hit_count_30d': 0, 'source': 'manual', 'confidence': 1.0},
{'name': 'DeepMind', 'aliases': ['deepmind', 'DeepMind', 'deep mind'], 'category': 'AI', 'created_at': '2026-08-08', 'last_verified_at': '2026-08-08', 'last_seen_at': '2026-08-08', 'hit_count_30d': 0, 'source': 'manual', 'confidence': 1.0},
{'name': 'xAI', 'aliases': ['xai', 'X.AI', 'Grok'], 'category': 'AI', 'created_at': '2026-08-08', 'last_verified_at': '2026-08-08', 'last_seen_at': '2026-08-08', 'hit_count_30d': 0, 'source': 'manual', 'confidence': 1.0},
{'name': 'Perplexity', 'aliases': ['perplexity', 'Perplexity AI'], 'category': 'AI', 'created_at': '2026-08-08', 'last_verified_at': '2026-08-08', 'last_seen_at': '2026-08-08', 'hit_count_30d': 0, 'source': 'manual', 'confidence': 1.0},
{'name': '智谱AI', 'aliases': ['智谱', 'Zhipu', 'GLM'], 'category': 'AI', 'created_at': '2026-08-08', 'last_verified_at': '2026-08-08', 'last_seen_at': '2026-08-08', 'hit_count_30d': 0, 'source': 'manual', 'confidence': 1.0},
{'name': '月之暗面', 'aliases': ['月之暗面', 'Moonshot', 'Kimi'], 'category': 'AI', 'created_at': '2026-08-08', 'last_verified_at': '2026-08-08', 'last_seen_at': '2026-08-08', 'hit_count_30d': 0, 'source': 'manual', 'confidence': 1.0},
{'name': '百川智能', 'aliases': ['百川', 'Baichuan'], 'category': 'AI', 'created_at': '2026-08-08', 'last_verified_at': '2026-08-08', 'last_seen_at': '2026-08-08', 'hit_count_30d': 0, 'source': 'manual', 'confidence': 1.0},
{'name': '商汤科技', 'aliases': ['商汤', 'SenseTime'], 'category': 'AI', 'created_at': '2026-08-08', 'last_verified_at': '2026-08-08', 'last_seen_at': '2026-08-08', 'hit_count_30d': 0, 'source': 'manual', 'confidence': 1.0},
{'name': '旷视科技', 'aliases': ['旷视', 'Megvii'], 'category': 'AI', 'created_at': '2026-08-08', 'last_verified_at': '2026-08-08', 'last_seen_at': '2026-08-08', 'hit_count_30d': 0, 'source': 'manual', 'confidence': 1.0},

    # 钢铁/制造
{'name': '宝钢', 'aliases': ['宝钢股份', 'Baosteel', '宝山钢铁'], 'category': 'STEEL', 'created_at': '2026-08-08', 'last_verified_at': '2026-08-08', 'last_seen_at': '2026-08-08', 'hit_count_30d': 0, 'source': 'manual', 'confidence': 1.0},
{'name': '首钢', 'aliases': ['首钢集团', 'Shougang'], 'category': 'STEEL', 'created_at': '2026-08-08', 'last_verified_at': '2026-08-08', 'last_seen_at': '2026-08-08', 'hit_count_30d': 0, 'source': 'manual', 'confidence': 1.0},
{'name': '河钢', 'aliases': ['河钢集团', 'HBIS'], 'category': 'STEEL', 'created_at': '2026-08-08', 'last_verified_at': '2026-08-08', 'last_seen_at': '2026-08-08', 'hit_count_30d': 0, 'source': 'manual', 'confidence': 1.0},
{'name': '鞍钢', 'aliases': ['鞍钢集团', 'Ansteel'], 'category': 'STEEL', 'created_at': '2026-08-08', 'last_verified_at': '2026-08-08', 'last_seen_at': '2026-08-08', 'hit_count_30d': 0, 'source': 'manual', 'confidence': 1.0},
{'name': '武钢', 'aliases': ['武钢集团', 'Wuhan Steel'], 'category': 'STEEL', 'created_at': '2026-08-08', 'last_verified_at': '2026-08-08', 'last_seen_at': '2026-08-08', 'hit_count_30d': 0, 'source': 'manual', 'confidence': 1.0},
{'name': 'ArcelorMittal', 'aliases': ['arcelormittal', 'Arcelor Mittal'], 'category': 'STEEL', 'created_at': '2026-08-08', 'last_verified_at': '2026-08-08', 'last_seen_at': '2026-08-08', 'hit_count_30d': 0, 'source': 'manual', 'confidence': 1.0},
{'name': 'Posco', 'aliases': ['posco', '浦项'], 'category': 'STEEL', 'created_at': '2026-08-08', 'last_verified_at': '2026-08-08', 'last_seen_at': '2026-08-08', 'hit_count_30d': 0, 'source': 'manual', 'confidence': 1.0},
{'name': 'Nippon Steel', 'aliases': ['nippon steel', '日本制铁'], 'category': 'STEEL', 'created_at': '2026-08-08', 'last_verified_at': '2026-08-08', 'last_seen_at': '2026-08-08', 'hit_count_30d': 0, 'source': 'manual', 'confidence': 1.0},
{'name': 'JFE Steel', 'aliases': ['jfe steel', 'JFE'], 'category': 'STEEL', 'created_at': '2026-08-08', 'last_verified_at': '2026-08-08', 'last_seen_at': '2026-08-08', 'hit_count_30d': 0, 'source': 'manual', 'confidence': 1.0},

    # 金融
{'name': '中金公司', 'aliases': ['中金', 'CICC', '中金证券'], 'category': 'FINANCE', 'created_at': '2026-08-08', 'last_verified_at': '2026-08-08', 'last_seen_at': '2026-08-08', 'hit_count_30d': 0, 'source': 'manual', 'confidence': 1.0},
{'name': '中信证券', 'aliases': ['中信', 'CITIC Securities', '中信证券'], 'category': 'FINANCE', 'created_at': '2026-08-08', 'last_verified_at': '2026-08-08', 'last_seen_at': '2026-08-08', 'hit_count_30d': 0, 'source': 'manual', 'confidence': 1.0},
{'name': '招商证券', 'aliases': ['招商', 'CMS', '招商证券'], 'category': 'FINANCE', 'created_at': '2026-08-08', 'last_verified_at': '2026-08-08', 'last_seen_at': '2026-08-08', 'hit_count_30d': 0, 'source': 'manual', 'confidence': 1.0},
{'name': '海通证券', 'aliases': ['海通', 'Haitong'], 'category': 'FINANCE', 'created_at': '2026-08-08', 'last_verified_at': '2026-08-08', 'last_seen_at': '2026-08-08', 'hit_count_30d': 0, 'source': 'manual', 'confidence': 1.0},
{'name': '华泰证券', 'aliases': ['华泰', 'Huatai'], 'category': 'FINANCE', 'created_at': '2026-08-08', 'last_verified_at': '2026-08-08', 'last_seen_at': '2026-08-08', 'hit_count_30d': 0, 'source': 'manual', 'confidence': 1.0},
{'name': '宁德时代', 'aliases': ['宁德时代', 'CATL', '宁德'], 'category': 'AUTO', 'created_at': '2026-08-08', 'last_verified_at': '2026-08-08', 'last_seen_at': '2026-08-08', 'hit_count_30d': 0, 'source': 'manual', 'confidence': 1.0},
{'name': '比亚迪', 'aliases': ['比亚迪', 'BYD'], 'category': 'AUTO', 'created_at': '2026-08-08', 'last_verified_at': '2026-08-08', 'last_seen_at': '2026-08-08', 'hit_count_30d': 0, 'source': 'manual', 'confidence': 1.0},
{'name': '特斯拉', 'aliases': ['特斯拉', 'Tesla', 'TSLA'], 'category': 'AUTO', 'created_at': '2026-08-08', 'last_verified_at': '2026-08-08', 'last_seen_at': '2026-08-08', 'hit_count_30d': 0, 'source': 'manual', 'confidence': 1.0},

    # 设备厂商
{'name': 'SMS group', 'aliases': ['sms group', 'sms-group'], 'category': 'EQUIPMENT', 'created_at': '2026-08-08', 'last_verified_at': '2026-08-08', 'last_seen_at': '2026-08-08', 'hit_count_30d': 0, 'source': 'manual', 'confidence': 1.0},
{'name': 'Andritz', 'aliases': ['andritz'], 'category': 'EQUIPMENT', 'created_at': '2026-08-08', 'last_verified_at': '2026-08-08', 'last_seen_at': '2026-08-08', 'hit_count_30d': 0, 'source': 'manual', 'confidence': 1.0},
{'name': 'Mitsubishi-Hitachi', 'aliases': ['mhi', 'mitsubishi-hitachi', '三菱'], 'category': 'EQUIPMENT', 'created_at': '2026-08-08', 'last_verified_at': '2026-08-08', 'last_seen_at': '2026-08-08', 'hit_count_30d': 0, 'source': 'manual', 'confidence': 1.0},
{'name': '西门子', 'aliases': ['siemens'], 'category': 'EQUIPMENT', 'created_at': '2026-08-08', 'last_verified_at': '2026-08-08', 'last_seen_at': '2026-08-08', 'hit_count_30d': 0, 'source': 'manual', 'confidence': 1.0},
{'name': 'ABB', 'aliases': ['abb'], 'category': 'EQUIPMENT', 'created_at': '2026-08-08', 'last_verified_at': '2026-08-08', 'last_seen_at': '2026-08-08', 'hit_count_30d': 0, 'source': 'manual', 'confidence': 1.0},

    # 行业协会
{'name': '中国金属学会', 'aliases': ['中国金属学会', '金属学会', 'CSM'], 'category': 'ASSOCIATION', 'created_at': '2026-08-08', 'last_verified_at': '2026-08-08', 'last_seen_at': '2026-08-08', 'hit_count_30d': 0, 'source': 'manual', 'confidence': 1.0},
    {'name': 'AIST', 'patterns': ['aist.org'], 'category': 'ASSOCIATION', 'created_at': '2026-08-08', 'last_verified_at': '2026-08-08', 'last_seen_at': '2026-08-08', 'hit_count_30d': 0, 'source': 'manual', 'confidence': 1.0},
    {'name': 'MPIF', 'patterns': ['mpif.org'], 'category': 'ASSOCIATION', 'created_at': '2026-08-08', 'last_verified_at': '2026-08-08', 'last_seen_at': '2026-08-08', 'hit_count_30d': 0, 'source': 'manual', 'confidence': 1.0},

    # v2.0.1 扩充：咨询/智库/媒体
{'name': '罗兰贝格', 'aliases': ['roland berger', 'RolandBerger'], 'category': 'CONSULTING', 'created_at': '2026-08-08', 'last_verified_at': '2026-08-08', 'last_seen_at': '2026-08-08', 'hit_count_30d': 0, 'source': 'manual', 'confidence': 1.0},
{'name': '埃森哲', 'aliases': ['accenture', 'Accenture'], 'category': 'CONSULTING', 'created_at': '2026-08-08', 'last_verified_at': '2026-08-08', 'last_seen_at': '2026-08-08', 'hit_count_30d': 0, 'source': 'manual', 'confidence': 1.0},
{'name': '毕马威', 'aliases': ['kpmg', 'KPMG'], 'category': 'CONSULTING', 'created_at': '2026-08-08', 'last_verified_at': '2026-08-08', 'last_seen_at': '2026-08-08', 'hit_count_30d': 0, 'source': 'manual', 'confidence': 1.0},
{'name': '普华永道', 'aliases': ['pwc', 'PwC'], 'category': 'CONSULTING', 'created_at': '2026-08-08', 'last_verified_at': '2026-08-08', 'last_seen_at': '2026-08-08', 'hit_count_30d': 0, 'source': 'manual', 'confidence': 1.0},
{'name': '德勤', 'aliases': ['deloitte', 'Deloitte'], 'category': 'CONSULTING', 'created_at': '2026-08-08', 'last_verified_at': '2026-08-08', 'last_seen_at': '2026-08-08', 'hit_count_30d': 0, 'source': 'manual', 'confidence': 1.0},
{'name': '亿欧', 'aliases': ['亿欧', 'EO intelligence', 'yiou'], 'category': 'MEDIA', 'created_at': '2026-08-08', 'last_verified_at': '2026-08-08', 'last_seen_at': '2026-08-08', 'hit_count_30d': 0, 'source': 'manual', 'confidence': 1.0},
{'name': '投中网', 'aliases': ['投中网', 'chinaventure', 'ChinaVenture'], 'category': 'MEDIA', 'created_at': '2026-08-08', 'last_verified_at': '2026-08-08', 'last_seen_at': '2026-08-08', 'hit_count_30d': 0, 'source': 'manual', 'confidence': 1.0},
{'name': 'IT桔子', 'aliases': ['itjuzi', 'IT桔子'], 'category': 'MEDIA', 'created_at': '2026-08-08', 'last_verified_at': '2026-08-08', 'last_seen_at': '2026-08-08', 'hit_count_30d': 0, 'source': 'manual', 'confidence': 1.0},
{'name': 'PingWest', 'aliases': ['pingwest', 'PingWest'], 'category': 'MEDIA', 'created_at': '2026-08-08', 'last_verified_at': '2026-08-08', 'last_seen_at': '2026-08-08', 'hit_count_30d': 0, 'source': 'manual', 'confidence': 1.0},
{'name': '爱范儿', 'aliases': ['爱范儿', 'ifanr'], 'category': 'MEDIA', 'created_at': '2026-08-08', 'last_verified_at': '2026-08-08', 'last_seen_at': '2026-08-08', 'hit_count_30d': 0, 'source': 'manual', 'confidence': 1.0},

    # v2.0.1 扩充：新能源/电池
{'name': '宁德新能源', 'aliases': ['ATL', 'Amperex', '新能源科技'], 'category': 'BATTERY', 'created_at': '2026-08-08', 'last_verified_at': '2026-08-08', 'last_seen_at': '2026-08-08', 'hit_count_30d': 0, 'source': 'manual', 'confidence': 1.0},
{'name': '比亚迪电子', 'aliases': ['BYD Electronic'], 'category': 'BATTERY', 'created_at': '2026-08-08', 'last_verified_at': '2026-08-08', 'last_seen_at': '2026-08-08', 'hit_count_30d': 0, 'source': 'manual', 'confidence': 1.0},
{'name': '国轩高科', 'aliases': ['国轩高科', 'Gotion'], 'category': 'BATTERY', 'created_at': '2026-08-08', 'last_verified_at': '2026-08-08', 'last_seen_at': '2026-08-08', 'hit_count_30d': 0, 'source': 'manual', 'confidence': 1.0},
{'name': '蜂巢能源', 'aliases': ['蜂巢能源', 'SVOLT'], 'category': 'BATTERY', 'created_at': '2026-08-08', 'last_verified_at': '2026-08-08', 'last_seen_at': '2026-08-08', 'hit_count_30d': 0, 'source': 'manual', 'confidence': 1.0},
{'name': '亿纬锂能', 'aliases': ['亿纬锂能', 'EVE Energy'], 'category': 'BATTERY', 'created_at': '2026-08-08', 'last_verified_at': '2026-08-08', 'last_seen_at': '2026-08-08', 'hit_count_30d': 0, 'source': 'manual', 'confidence': 1.0},

    # v2.0.1 扩充：互联网/社交
{'name': '字节跳动', 'aliases': ['字节跳动', 'ByteDance', '字节'], 'category': 'INTERNET', 'created_at': '2026-08-08', 'last_verified_at': '2026-08-08', 'last_seen_at': '2026-08-08', 'hit_count_30d': 0, 'source': 'manual', 'confidence': 1.0},
{'name': '腾讯', 'aliases': ['腾讯', 'Tencent'], 'category': 'INTERNET', 'created_at': '2026-08-08', 'last_verified_at': '2026-08-08', 'last_seen_at': '2026-08-08', 'hit_count_30d': 0, 'source': 'manual', 'confidence': 1.0},
{'name': '阿里巴巴', 'aliases': ['阿里巴巴', 'Alibaba', '阿里'], 'category': 'INTERNET', 'created_at': '2026-08-08', 'last_verified_at': '2026-08-08', 'last_seen_at': '2026-08-08', 'hit_count_30d': 0, 'source': 'manual', 'confidence': 1.0},
{'name': '百度', 'aliases': ['百度', 'Baidu'], 'category': 'INTERNET', 'created_at': '2026-08-08', 'last_verified_at': '2026-08-08', 'last_seen_at': '2026-08-08', 'hit_count_30d': 0, 'source': 'manual', 'confidence': 1.0},
{'name': '京东', 'aliases': ['京东', 'JD.com', 'JD'], 'category': 'INTERNET', 'created_at': '2026-08-08', 'last_verified_at': '2026-08-08', 'last_seen_at': '2026-08-08', 'hit_count_30d': 0, 'source': 'manual', 'confidence': 1.0},
{'name': '美团', 'aliases': ['美团', 'Meituan'], 'category': 'INTERNET', 'created_at': '2026-08-08', 'last_verified_at': '2026-08-08', 'last_seen_at': '2026-08-08', 'hit_count_30d': 0, 'source': 'manual', 'confidence': 1.0},
{'name': '拼多多', 'aliases': ['拼多多', 'Pinduoduo', 'PDD'], 'category': 'INTERNET', 'created_at': '2026-08-08', 'last_verified_at': '2026-08-08', 'last_seen_at': '2026-08-08', 'hit_count_30d': 0, 'source': 'manual', 'confidence': 1.0},
{'name': '快手', 'aliases': ['快手', 'Kuaishou'], 'category': 'INTERNET', 'created_at': '2026-08-08', 'last_verified_at': '2026-08-08', 'last_seen_at': '2026-08-08', 'hit_count_30d': 0, 'source': 'manual', 'confidence': 1.0},
{'name': '小红书', 'aliases': ['小红书', 'Xiaohongshu', 'RED'], 'category': 'INTERNET', 'created_at': '2026-08-08', 'last_verified_at': '2026-08-08', 'last_seen_at': '2026-08-08', 'hit_count_30d': 0, 'source': 'manual', 'confidence': 1.0},
{'name': '哔哩哔哩', 'aliases': ['bilibili', 'B站', '哔哩哔哩'], 'category': 'INTERNET', 'created_at': '2026-08-08', 'last_verified_at': '2026-08-08', 'last_seen_at': '2026-08-08', 'hit_count_30d': 0, 'source': 'manual', 'confidence': 1.0},

    # v2.0.1 扩充：半导体/硬件
{'name': '台积电', 'aliases': ['台积电', 'TSMC'], 'category': 'SEMI', 'created_at': '2026-08-08', 'last_verified_at': '2026-08-08', 'last_seen_at': '2026-08-08', 'hit_count_30d': 0, 'source': 'manual', 'confidence': 1.0},
{'name': '中芯国际', 'aliases': ['中芯国际', 'SMIC'], 'category': 'SEMI', 'created_at': '2026-08-08', 'last_verified_at': '2026-08-08', 'last_seen_at': '2026-08-08', 'hit_count_30d': 0, 'source': 'manual', 'confidence': 1.0},
{'name': '英特尔', 'aliases': ['intel', 'Intel', '英特尔'], 'category': 'SEMI', 'created_at': '2026-08-08', 'last_verified_at': '2026-08-08', 'last_seen_at': '2026-08-08', 'hit_count_30d': 0, 'source': 'manual', 'confidence': 1.0},
{'name': 'AMD', 'aliases': ['amd', 'AMD'], 'category': 'SEMI', 'created_at': '2026-08-08', 'last_verified_at': '2026-08-08', 'last_seen_at': '2026-08-08', 'hit_count_30d': 0, 'source': 'manual', 'confidence': 1.0},
{'name': '高通', 'aliases': ['高通', 'Qualcomm'], 'category': 'SEMI', 'created_at': '2026-08-08', 'last_verified_at': '2026-08-08', 'last_seen_at': '2026-08-08', 'hit_count_30d': 0, 'source': 'manual', 'confidence': 1.0},
{'name': '联发科', 'aliases': ['联发科', 'MediaTek', 'MTK'], 'category': 'SEMI', 'created_at': '2026-08-08', 'last_verified_at': '2026-08-08', 'last_seen_at': '2026-08-08', 'hit_count_30d': 0, 'source': 'manual', 'confidence': 1.0},
{'name': '英伟达', 'aliases': ['英伟达', 'NVIDIA'], 'category': 'SEMI', 'created_at': '2026-08-08', 'last_verified_at': '2026-08-08', 'last_seen_at': '2026-08-08', 'hit_count_30d': 0, 'source': 'manual', 'confidence': 1.0},
{'name': 'AMD', 'aliases': ['amd', '超微'], 'category': 'SEMI', 'created_at': '2026-08-08', 'last_verified_at': '2026-08-08', 'last_seen_at': '2026-08-08', 'hit_count_30d': 0, 'source': 'manual', 'confidence': 1.0},

    # v2.0.1 扩充：教育/科研
{'name': '清华大学', 'aliases': ['清华大学', 'Tsinghua', 'THU'], 'category': 'EDU', 'created_at': '2026-08-08', 'last_verified_at': '2026-08-08', 'last_seen_at': '2026-08-08', 'hit_count_30d': 0, 'source': 'manual', 'confidence': 1.0},
{'name': '北京大学', 'aliases': ['北京大学', 'Peking University', 'PKU'], 'category': 'EDU', 'created_at': '2026-08-08', 'last_verified_at': '2026-08-08', 'last_seen_at': '2026-08-08', 'hit_count_30d': 0, 'source': 'manual', 'confidence': 1.0},
{'name': 'MIT', 'aliases': ['mit', 'MIT'], 'category': 'EDU', 'created_at': '2026-08-08', 'last_verified_at': '2026-08-08', 'last_seen_at': '2026-08-08', 'hit_count_30d': 0, 'source': 'manual', 'confidence': 1.0},
{'name': '斯坦福', 'aliases': ['stanford', '斯坦福', 'Stanford'], 'category': 'EDU', 'created_at': '2026-08-08', 'last_verified_at': '2026-08-08', 'last_seen_at': '2026-08-08', 'hit_count_30d': 0, 'source': 'manual', 'confidence': 1.0},
{'name': '中科院', 'aliases': ['中科院', 'CAS', 'Chinese Academy of Sciences'], 'category': 'EDU', 'created_at': '2026-08-08', 'last_verified_at': '2026-08-08', 'last_seen_at': '2026-08-08', 'hit_count_30d': 0, 'source': 'manual', 'confidence': 1.0},
]


# ═══════════════════════════════════════════════════════════════
# PRODUCT: 产品/品牌（30+）
# ═══════════════════════════════════════════════════════════════

PRODUCT_ENTITIES = [
{'name': 'GPT-4', 'aliases': ['gpt-4', 'GPT4', 'gpt4'], 'category': 'AI_MODEL', 'created_at': '2026-08-08', 'last_verified_at': '2026-08-08', 'last_seen_at': '2026-08-08', 'hit_count_30d': 0, 'source': 'manual', 'confidence': 1.0},
{'name': 'GPT-4o', 'aliases': ['gpt-4o', 'GPT4o'], 'category': 'AI_MODEL', 'created_at': '2026-08-08', 'last_verified_at': '2026-08-08', 'last_seen_at': '2026-08-08', 'hit_count_30d': 0, 'source': 'manual', 'confidence': 1.0},
{'name': 'Claude 3', 'aliases': ['claude 3', 'claude-3', 'Claude3'], 'category': 'AI_MODEL', 'created_at': '2026-08-08', 'last_verified_at': '2026-08-08', 'last_seen_at': '2026-08-08', 'hit_count_30d': 0, 'source': 'manual', 'confidence': 1.0},
{'name': 'Claude 3.5', 'aliases': ['claude 3.5', 'claude-3.5', 'claude 3.5 sonnet'], 'category': 'AI_MODEL', 'created_at': '2026-08-08', 'last_verified_at': '2026-08-08', 'last_seen_at': '2026-08-08', 'hit_count_30d': 0, 'source': 'manual', 'confidence': 1.0},
{'name': 'Gemini', 'aliases': ['gemini', 'gemini pro', 'gemini ultra'], 'category': 'AI_MODEL', 'created_at': '2026-08-08', 'last_verified_at': '2026-08-08', 'last_seen_at': '2026-08-08', 'hit_count_30d': 0, 'source': 'manual', 'confidence': 1.0},
{'name': 'Llama', 'aliases': ['llama', 'llama 2', 'llama 3', 'meta llama'], 'category': 'AI_MODEL', 'created_at': '2026-08-08', 'last_verified_at': '2026-08-08', 'last_seen_at': '2026-08-08', 'hit_count_30d': 0, 'source': 'manual', 'confidence': 1.0},
{'name': 'Mistral 7B', 'aliases': ['mistral 7b', 'mistral-7b'], 'category': 'AI_MODEL', 'created_at': '2026-08-08', 'last_verified_at': '2026-08-08', 'last_seen_at': '2026-08-08', 'hit_count_30d': 0, 'source': 'manual', 'confidence': 1.0},
{'name': 'Mixtral', 'aliases': ['mixtral'], 'category': 'AI_MODEL', 'created_at': '2026-08-08', 'last_verified_at': '2026-08-08', 'last_seen_at': '2026-08-08', 'hit_count_30d': 0, 'source': 'manual', 'confidence': 1.0},
{'name': 'GLM-4', 'aliases': ['glm-4', 'GLM4', 'chatglm-4'], 'category': 'AI_MODEL', 'created_at': '2026-08-08', 'last_verified_at': '2026-08-08', 'last_seen_at': '2026-08-08', 'hit_count_30d': 0, 'source': 'manual', 'confidence': 1.0},
{'name': 'Notion', 'aliases': ['notion', 'Notion AI'], 'category': 'PRODUCTIVITY', 'created_at': '2026-08-08', 'last_verified_at': '2026-08-08', 'last_seen_at': '2026-08-08', 'hit_count_30d': 0, 'source': 'manual', 'confidence': 1.0},
{'name': 'Obsidian', 'aliases': ['obsidian'], 'category': 'PRODUCTIVITY', 'created_at': '2026-08-08', 'last_verified_at': '2026-08-08', 'last_seen_at': '2026-08-08', 'hit_count_30d': 0, 'source': 'manual', 'confidence': 1.0},
{'name': 'Slack', 'aliases': ['slack'], 'category': 'PRODUCTIVITY', 'created_at': '2026-08-08', 'last_verified_at': '2026-08-08', 'last_seen_at': '2026-08-08', 'hit_count_30d': 0, 'source': 'manual', 'confidence': 1.0},
{'name': '飞书', 'aliases': ['飞书', 'Lark', 'feishu'], 'category': 'PRODUCTIVITY', 'created_at': '2026-08-08', 'last_verified_at': '2026-08-08', 'last_seen_at': '2026-08-08', 'hit_count_30d': 0, 'source': 'manual', 'confidence': 1.0},
{'name': '钉钉', 'aliases': ['钉钉', 'DingTalk'], 'category': 'PRODUCTIVITY', 'created_at': '2026-08-08', 'last_verified_at': '2026-08-08', 'last_seen_at': '2026-08-08', 'hit_count_30d': 0, 'source': 'manual', 'confidence': 1.0},
{'name': '企业微信', 'aliases': ['企业微信', 'WeCom'], 'category': 'PRODUCTIVITY', 'created_at': '2026-08-08', 'last_verified_at': '2026-08-08', 'last_seen_at': '2026-08-08', 'hit_count_30d': 0, 'source': 'manual', 'confidence': 1.0},
{'name': 'SUS316L', 'aliases': ['sus316l', 'SUS 316L', '316L', '316l'], 'category': 'MATERIAL', 'created_at': '2026-08-08', 'last_verified_at': '2026-08-08', 'last_seen_at': '2026-08-08', 'hit_count_30d': 0, 'source': 'manual', 'confidence': 1.0},
{'name': 'Q235', 'aliases': ['q235', 'Q235'], 'category': 'MATERIAL', 'created_at': '2026-08-08', 'last_verified_at': '2026-08-08', 'last_seen_at': '2026-08-08', 'hit_count_30d': 0, 'source': 'manual', 'confidence': 1.0},
{'name': 'DC01', 'aliases': ['dc01', 'DC01'], 'category': 'MATERIAL', 'created_at': '2026-08-08', 'last_verified_at': '2026-08-08', 'last_seen_at': '2026-08-08', 'hit_count_30d': 0, 'source': 'manual', 'confidence': 1.0},
{'name': 'SPCC', 'aliases': ['spcc', 'SPCC'], 'category': 'MATERIAL', 'created_at': '2026-08-08', 'last_verified_at': '2026-08-08', 'last_seen_at': '2026-08-08', 'hit_count_30d': 0, 'source': 'manual', 'confidence': 1.0},
{'name': 'Inconel 718', 'aliases': ['inconel 718', 'inconel718', 'IN718'], 'category': 'MATERIAL', 'created_at': '2026-08-08', 'last_verified_at': '2026-08-08', 'last_seen_at': '2026-08-08', 'hit_count_30d': 0, 'source': 'manual', 'confidence': 1.0},
{'name': 'Monel 400', 'aliases': ['monel 400', 'monel400'], 'category': 'MATERIAL', 'created_at': '2026-08-08', 'last_verified_at': '2026-08-08', 'last_seen_at': '2026-08-08', 'hit_count_30d': 0, 'source': 'manual', 'confidence': 1.0},
]


# ═══════════════════════════════════════════════════════════════
# TECH: 技术/框架（20+）
# ═══════════════════════════════════════════════════════════════

TECH_ENTITIES = [
{'name': 'RAG', 'aliases': ['rag', 'RAG', 'Retrieval-Augmented Generation'], 'category': 'TECH_AI', 'created_at': '2026-08-08', 'last_verified_at': '2026-08-08', 'last_seen_at': '2026-08-08', 'hit_count_30d': 0, 'source': 'manual', 'confidence': 1.0},
{'name': 'MCP', 'aliases': ['mcp', 'MCP', 'Model Context Protocol'], 'category': 'PROTOCOL', 'created_at': '2026-08-08', 'last_verified_at': '2026-08-08', 'last_seen_at': '2026-08-08', 'hit_count_30d': 0, 'source': 'manual', 'confidence': 1.0},
{'name': 'Transformer', 'aliases': ['transformer', 'Transformer'], 'category': 'ARCH', 'created_at': '2026-08-08', 'last_verified_at': '2026-08-08', 'last_seen_at': '2026-08-08', 'hit_count_30d': 0, 'source': 'manual', 'confidence': 1.0},
{'name': 'LoRA', 'aliases': ['lora', 'LoRA', 'Low-Rank Adaptation'], 'category': 'TECH_AI', 'created_at': '2026-08-08', 'last_verified_at': '2026-08-08', 'last_seen_at': '2026-08-08', 'hit_count_30d': 0, 'source': 'manual', 'confidence': 1.0},
{'name': 'RLHF', 'aliases': ['rlhf', 'RLHF'], 'category': 'TECH_AI', 'created_at': '2026-08-08', 'last_verified_at': '2026-08-08', 'last_seen_at': '2026-08-08', 'hit_count_30d': 0, 'source': 'manual', 'confidence': 1.0},
{'name': 'Function Calling', 'aliases': ['function calling', 'function call'], 'category': 'TECH_AI', 'created_at': '2026-08-08', 'last_verified_at': '2026-08-08', 'last_seen_at': '2026-08-08', 'hit_count_30d': 0, 'source': 'manual', 'confidence': 1.0},
{'name': 'Prompt Engineering', 'aliases': ['prompt engineering', '提示工程'], 'category': 'TECH_AI', 'created_at': '2026-08-08', 'last_verified_at': '2026-08-08', 'last_seen_at': '2026-08-08', 'hit_count_30d': 0, 'source': 'manual', 'confidence': 1.0},
{'name': 'RNN', 'aliases': ['rnn', 'RNN'], 'category': 'ARCH', 'created_at': '2026-08-08', 'last_verified_at': '2026-08-08', 'last_seen_at': '2026-08-08', 'hit_count_30d': 0, 'source': 'manual', 'confidence': 1.0},
{'name': 'CNN', 'aliases': ['cnn', 'CNN', '卷积神经网络'], 'category': 'ARCH', 'created_at': '2026-08-08', 'last_verified_at': '2026-08-08', 'last_seen_at': '2026-08-08', 'hit_count_30d': 0, 'source': 'manual', 'confidence': 1.0},
{'name': 'Diffusion', 'aliases': ['diffusion', 'Diffusion'], 'category': 'ARCH', 'created_at': '2026-08-08', 'last_verified_at': '2026-08-08', 'last_seen_at': '2026-08-08', 'hit_count_30d': 0, 'source': 'manual', 'confidence': 1.0},
{'name': 'YOLO', 'aliases': ['yolo', 'YOLO'], 'category': 'TECH_CV', 'created_at': '2026-08-08', 'last_verified_at': '2026-08-08', 'last_seen_at': '2026-08-08', 'hit_count_30d': 0, 'source': 'manual', 'confidence': 1.0},
{'name': 'PyTorch', 'aliases': ['pytorch', 'PyTorch'], 'category': 'FRAMEWORK', 'created_at': '2026-08-08', 'last_verified_at': '2026-08-08', 'last_seen_at': '2026-08-08', 'hit_count_30d': 0, 'source': 'manual', 'confidence': 1.0},
{'name': 'TensorFlow', 'aliases': ['tensorflow', 'TF', 'TensorFlow'], 'category': 'FRAMEWORK', 'created_at': '2026-08-08', 'last_verified_at': '2026-08-08', 'last_seen_at': '2026-08-08', 'hit_count_30d': 0, 'source': 'manual', 'confidence': 1.0},
{'name': 'LangChain', 'aliases': ['langchain', 'LangChain'], 'category': 'FRAMEWORK', 'created_at': '2026-08-08', 'last_verified_at': '2026-08-08', 'last_seen_at': '2026-08-08', 'hit_count_30d': 0, 'source': 'manual', 'confidence': 1.0},
{'name': 'LlamaIndex', 'aliases': ['llamaindex', 'LlamaIndex'], 'category': 'FRAMEWORK', 'created_at': '2026-08-08', 'last_verified_at': '2026-08-08', 'last_seen_at': '2026-08-08', 'hit_count_30d': 0, 'source': 'manual', 'confidence': 1.0},
{'name': 'Hugging Face', 'aliases': ['huggingface', 'HF', 'HuggingFace'], 'category': 'FRAMEWORK', 'created_at': '2026-08-08', 'last_verified_at': '2026-08-08', 'last_seen_at': '2026-08-08', 'hit_count_30d': 0, 'source': 'manual', 'confidence': 1.0},
{'name': '钢卷分切', 'aliases': ['钢卷分切', 'slitting', '分切工艺', '纵剪'], 'category': 'PROCESS', 'created_at': '2026-08-08', 'last_verified_at': '2026-08-08', 'last_seen_at': '2026-08-08', 'hit_count_30d': 0, 'source': 'manual', 'confidence': 1.0},
{'name': '轧制', 'aliases': ['轧制', 'rolling', '热轧', '冷轧'], 'category': 'PROCESS', 'created_at': '2026-08-08', 'last_verified_at': '2026-08-08', 'last_seen_at': '2026-08-08', 'hit_count_30d': 0, 'source': 'manual', 'confidence': 1.0},
{'name': '退火', 'aliases': ['退火', 'annealing'], 'category': 'PROCESS', 'created_at': '2026-08-08', 'last_verified_at': '2026-08-08', 'last_seen_at': '2026-08-08', 'hit_count_30d': 0, 'source': 'manual', 'confidence': 1.0},

    # v2.0.1 扩充：AI 模型/工具
{'name': 'Qwen', 'aliases': ['qwen', '通义千问', 'Qwen'], 'category': 'AI_MODEL', 'created_at': '2026-08-08', 'last_verified_at': '2026-08-08', 'last_seen_at': '2026-08-08', 'hit_count_30d': 0, 'source': 'manual', 'confidence': 1.0},
{'name': 'ERNIE', 'aliases': ['ernie', '文心一言', 'ERNIE'], 'category': 'AI_MODEL', 'created_at': '2026-08-08', 'last_verified_at': '2026-08-08', 'last_seen_at': '2026-08-08', 'hit_count_30d': 0, 'source': 'manual', 'confidence': 1.0},
{'name': 'DeepSeek', 'aliases': ['deepseek', 'DeepSeek', '深度求索'], 'category': 'AI_MODEL', 'created_at': '2026-08-08', 'last_verified_at': '2026-08-08', 'last_seen_at': '2026-08-08', 'hit_count_30d': 0, 'source': 'manual', 'confidence': 1.0},
{'name': 'Stable Diffusion', 'aliases': ['stable diffusion', 'sd', 'SD', 'StableDiffusion'], 'category': 'AI_MODEL', 'created_at': '2026-08-08', 'last_verified_at': '2026-08-08', 'last_seen_at': '2026-08-08', 'hit_count_30d': 0, 'source': 'manual', 'confidence': 1.0},
{'name': 'Midjourney', 'aliases': ['midjourney', 'MJ', 'Midjourney'], 'category': 'AI_MODEL', 'created_at': '2026-08-08', 'last_verified_at': '2026-08-08', 'last_seen_at': '2026-08-08', 'hit_count_30d': 0, 'source': 'manual', 'confidence': 1.0},
{'name': 'DALL-E', 'aliases': ['dall-e', 'dalle', 'DALL-E', 'DALLE'], 'category': 'AI_MODEL', 'created_at': '2026-08-08', 'last_verified_at': '2026-08-08', 'last_seen_at': '2026-08-08', 'hit_count_30d': 0, 'source': 'manual', 'confidence': 1.0},
{'name': 'Whisper', 'aliases': ['whisper', 'Whisper'], 'category': 'AI_MODEL', 'created_at': '2026-08-08', 'last_verified_at': '2026-08-08', 'last_seen_at': '2026-08-08', 'hit_count_30d': 0, 'source': 'manual', 'confidence': 1.0},

    # v2.0.1 扩充：开发工具/框架
{'name': 'Cursor', 'aliases': ['cursor', 'Cursor IDE'], 'category': 'TOOL', 'created_at': '2026-08-08', 'last_verified_at': '2026-08-08', 'last_seen_at': '2026-08-08', 'hit_count_30d': 0, 'source': 'manual', 'confidence': 1.0},
{'name': 'VSCode', 'aliases': ['vscode', 'vs code', 'VSCode', 'Visual Studio Code'], 'category': 'TOOL', 'created_at': '2026-08-08', 'last_verified_at': '2026-08-08', 'last_seen_at': '2026-08-08', 'hit_count_30d': 0, 'source': 'manual', 'confidence': 1.0},
{'name': 'GitHub Copilot', 'aliases': ['copilot', 'github copilot', 'Copilot'], 'category': 'TOOL', 'created_at': '2026-08-08', 'last_verified_at': '2026-08-08', 'last_seen_at': '2026-08-08', 'hit_count_30d': 0, 'source': 'manual', 'confidence': 1.0},
{'name': 'Docker', 'aliases': ['docker', 'Docker'], 'category': 'TOOL', 'created_at': '2026-08-08', 'last_verified_at': '2026-08-08', 'last_seen_at': '2026-08-08', 'hit_count_30d': 0, 'source': 'manual', 'confidence': 1.0},
{'name': 'Kubernetes', 'aliases': ['kubernetes', 'k8s', 'K8s'], 'category': 'TOOL', 'created_at': '2026-08-08', 'last_verified_at': '2026-08-08', 'last_seen_at': '2026-08-08', 'hit_count_30d': 0, 'source': 'manual', 'confidence': 1.0},
{'name': 'WebAssembly', 'aliases': ['webassembly', 'wasm', 'WASM'], 'category': 'TOOL', 'created_at': '2026-08-08', 'last_verified_at': '2026-08-08', 'last_seen_at': '2026-08-08', 'hit_count_30d': 0, 'source': 'manual', 'confidence': 1.0},
]


# ═══════════════════════════════════════════════════════════════
# PERSON: 人物（10+）
# ═══════════════════════════════════════════════════════════════

PERSON_ENTITIES = [
{'name': 'Sam Altman', 'aliases': ['sam altman', 'altman'], 'category': 'AI_PERSON', 'created_at': '2026-08-08', 'last_verified_at': '2026-08-08', 'last_seen_at': '2026-08-08', 'hit_count_30d': 0, 'source': 'manual', 'confidence': 1.0},
{'name': 'Dario Amodei', 'aliases': ['dario amodei', 'amodei'], 'category': 'AI_PERSON', 'created_at': '2026-08-08', 'last_verified_at': '2026-08-08', 'last_seen_at': '2026-08-08', 'hit_count_30d': 0, 'source': 'manual', 'confidence': 1.0},
{'name': 'Demis Hassabis', 'aliases': ['demis hassabis', 'hassabis'], 'category': 'AI_PERSON', 'created_at': '2026-08-08', 'last_verified_at': '2026-08-08', 'last_seen_at': '2026-08-08', 'hit_count_30d': 0, 'source': 'manual', 'confidence': 1.0},
{'name': 'Yann LeCun', 'aliases': ['yann lecun', 'lecun'], 'category': 'AI_PERSON', 'created_at': '2026-08-08', 'last_verified_at': '2026-08-08', 'last_seen_at': '2026-08-08', 'hit_count_30d': 0, 'source': 'manual', 'confidence': 1.0},
{'name': 'Andrej Karpathy', 'aliases': ['andrej karpathy', 'karpathy'], 'category': 'AI_PERSON', 'created_at': '2026-08-08', 'last_verified_at': '2026-08-08', 'last_seen_at': '2026-08-08', 'hit_count_30d': 0, 'source': 'manual', 'confidence': 1.0},
{'name': 'Andrew Ng', 'aliases': ['andrew ng', '吴恩达'], 'category': 'AI_PERSON', 'created_at': '2026-08-08', 'last_verified_at': '2026-08-08', 'last_seen_at': '2026-08-08', 'hit_count_30d': 0, 'source': 'manual', 'confidence': 1.0},
{'name': 'Geoffrey Hinton', 'aliases': ['geoffrey hinton', 'hinton'], 'category': 'AI_PERSON', 'created_at': '2026-08-08', 'last_verified_at': '2026-08-08', 'last_seen_at': '2026-08-08', 'hit_count_30d': 0, 'source': 'manual', 'confidence': 1.0},
{'name': 'Yoshua Bengio', 'aliases': ['yoshua bengio', 'bengio'], 'category': 'AI_PERSON', 'created_at': '2026-08-08', 'last_verified_at': '2026-08-08', 'last_seen_at': '2026-08-08', 'hit_count_30d': 0, 'source': 'manual', 'confidence': 1.0},
]


# ═══════════════════════════════════════════════════════════════
# METRIC: 度量/单位
# ═══════════════════════════════════════════════════════════════

METRIC_ENTITIES = [
{'name': 'PE', 'aliases': ['pe', 'PE', '市盈率'], 'category': 'FIN_METRIC', 'created_at': '2026-08-08', 'last_verified_at': '2026-08-08', 'last_seen_at': '2026-08-08', 'hit_count_30d': 0, 'source': 'manual', 'confidence': 1.0},
{'name': 'PB', 'aliases': ['pb', 'PB', '市净率'], 'category': 'FIN_METRIC', 'created_at': '2026-08-08', 'last_verified_at': '2026-08-08', 'last_seen_at': '2026-08-08', 'hit_count_30d': 0, 'source': 'manual', 'confidence': 1.0},
{'name': 'EPS', 'aliases': ['eps', 'EPS', '每股收益'], 'category': 'FIN_METRIC', 'created_at': '2026-08-08', 'last_verified_at': '2026-08-08', 'last_seen_at': '2026-08-08', 'hit_count_30d': 0, 'source': 'manual', 'confidence': 1.0},
{'name': 'ROI', 'aliases': ['roi', 'ROI', '投资回报率'], 'category': 'FIN_METRIC', 'created_at': '2026-08-08', 'last_verified_at': '2026-08-08', 'last_seen_at': '2026-08-08', 'hit_count_30d': 0, 'source': 'manual', 'confidence': 1.0},
{'name': 'CAGR', 'aliases': ['cagr', 'CAGR', '复合年均增长率'], 'category': 'FIN_METRIC', 'created_at': '2026-08-08', 'last_verified_at': '2026-08-08', 'last_seen_at': '2026-08-08', 'hit_count_30d': 0, 'source': 'manual', 'confidence': 1.0},
]


# ═══════════════════════════════════════════════════════════════
# 公开 API
# ═══════════════════════════════════════════════════════════════

_ALL_ENTITIES_CACHE = None
_LEARNED_CACHE = None


def _learned_path() -> Path:
    """动态回流实体文件（v1.7.7 包B）：INFOSEEK_DATA_DIR / ~/.infoseek。"""
    d = os.environ.get('INFOSEEK_DATA_DIR')
    base = Path(d) if d else (Path.home() / '.infoseek')
    return base / 'entities_learned.json'


def get_learned_entities(force: bool = False) -> List[Dict]:
    """动态回流实体（v1.7.7 包B）。文件缺失/损坏 → []。"""
    global _LEARNED_CACHE
    if _LEARNED_CACHE is not None and not force:
        return _LEARNED_CACHE
    try:
        p = _learned_path()
        if p.exists():
            data = json.loads(p.read_text(encoding='utf-8'))
            if isinstance(data, list):
                _LEARNED_CACHE = data
                return data
    except Exception:
        pass
    _LEARNED_CACHE = []
    return []


def learn_entity(name: str, aliases=None, category: str = 'AUTO',
                 confidence: float = 0.5, min_len: int = 2) -> bool:
    """回流单个实体（v1.7.7 包B：防噪声门控 + 幂等）。

    门控：name 非空 / 长度 ≥ min_len / 非纯数字符号 / 不与静态词典重名。
    幂等：已存在 → 合并 aliases + 刷新 last_seen_at。返回 True 表示发生写入。
    """
    global _LEARNED_CACHE, _ALL_ENTITIES_CACHE
    name = (name or '').strip()
    if len(name) < min_len or re.fullmatch(r'[\d\W_]+', name or ''):
        return False
    static_names = {e.get('name', '').lower() for e in
                    (ORG_ENTITIES + PRODUCT_ENTITIES + TECH_ENTITIES
                     + PERSON_ENTITIES + METRIC_ENTITIES)}
    if name.lower() in static_names:
        return False
    today = date.today().isoformat()
    learned = list(get_learned_entities(force=True))
    aliases = [a for a in (aliases or []) if a and a != name]
    # v1.7.7 包B：机构后缀自动衍生短名 alias（提升 query 命中率，
    # 如「无限工坊科技」→「无限工坊」）
    for _sfx in ('科技', '公司', '集团', '股份', '协会', '研究院', '大学', '实验室'):
        if name.endswith(_sfx) and len(name) > len(_sfx) + 1:
            _short = name[:-len(_sfx)]
            if _short != name and _short not in aliases:
                aliases.append(_short)
            break
    for e in learned:
        if e.get('name', '').lower() == name.lower():
            e['aliases'] = list(dict.fromkeys(list(e.get('aliases', [])) + aliases))
            e['last_seen_at'] = today
            break
    else:
        learned.append({
            'name': name, 'aliases': aliases, 'category': category,
            'created_at': today, 'last_seen_at': today,
            'source': 'learned', 'confidence': float(confidence),
        })
    try:
        p = _learned_path()
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps(learned, ensure_ascii=False, indent=2), encoding='utf-8')
    except Exception:
        return False
    _LEARNED_CACHE = learned
    _ALL_ENTITIES_CACHE = None   # 失效合并缓存（下次 NER 即见新实体）
    return True


def prune_learned_entities(max_age_days: int = 180,
                           min_confidence: float = 0.3,
                           active_names: Optional[set] = None,
                           dry_run: bool = True) -> Dict:
    """清理 learned 层冷 / 噪声实体（v2.0.0 实体持久层收尾，FreshnessCron 第 7 步）。

    learn_entity 此前只增不减，entities_learned.json 会无限累积自动回流的候选
    （pipeline reflow / person 运行时注册）。本函数给 learned 层补「冷条目清理」，
    与 EntityTracker.apply_decay（state 层 hit 衰减）共同构成实体持久层生命周期闭环。

    清理候选（两类，静态词典永不触碰）：
      1. 冷条目：last_seen_at 距今 > max_age_days，且名字不在 active_names
         （active_names 由调用方传入近期命中实体，如 tracker.get_stale_entities
         的补集 / record_hit 热集合）；
      2. 低置信噪声：confidence < min_confidence 且超龄（age > max_age_days），
         高价值实体（person 注册等 confidence 较高）受 min_confidence 门控保护。

    安全：默认 dry_run=True 只返回候选不落盘；FreshnessCron 默认即以此模式运行，
    需显式 dry_run=False（或 env INFOSEEK_LEARNED_PRUNE_APPLY=1）才真正删除。
    落盘采用 tmp + os.replace 原子写。返回 {'pruned','candidates','remaining','dry_run'}。
    """
    global _LEARNED_CACHE, _ALL_ENTITIES_CACHE
    learned = list(get_learned_entities(force=True))
    active = {n.lower() for n in (active_names or set())}
    today = date.today()
    candidates = []
    kept = []
    for e in learned:
        name = e.get('name', '')
        try:
            age = (today - date.fromisoformat(e.get('last_seen_at', ''))).days
        except Exception:
            age = max_age_days + 1  # 日期缺失/损坏视为超龄候选
        # active（近期仍命中）的实体完全保护：活跃即有用，噪声判据让位
        is_active = name.lower() in active
        cold = age > max_age_days and not is_active
        low_conf = float(e.get('confidence', 0.5) or 0.0) < min_confidence
        reason = None
        if not is_active and age > max_age_days and low_conf:
            reason = 'cold_low_conf'
        elif cold:
            # 超龄冷条目（含高置信长期未用）；低置信已在上面合并为 cold_low_conf
            reason = 'cold'
        if reason:
            candidates.append({'name': name, 'age_days': age,
                               'confidence': e.get('confidence', 0.5),
                               'reason': reason})
        else:
            kept.append(e)

    apply_env = os.environ.get('INFOSEEK_LEARNED_PRUNE_APPLY', '') in ('1', 'true', 'True')
    do_apply = (not dry_run) or apply_env
    written = False
    if do_apply and candidates:
        try:
            p = _learned_path()
            p.parent.mkdir(parents=True, exist_ok=True)
            tmp = p.with_suffix('.tmp')
            tmp.write_text(json.dumps(kept, ensure_ascii=False, indent=2),
                           encoding='utf-8')
            os.replace(str(tmp), str(p))
            written = True
            _LEARNED_CACHE = kept
            _ALL_ENTITIES_CACHE = None
        except Exception:
            written = False
    return {'pruned': len(candidates) if written else 0,
            'candidates': candidates,
            'remaining': len(kept) if written else len(learned),
            'dry_run': not written,
            'applied': written}


def get_all_entities() -> List[Dict]:
    """获取所有实体（v1.7.7 包B：静态词典 + 动态回流实体）

    v2.4.1 PATCH (DEF-E): 模块级缓存（NER 热路径）。
    """
    global _ALL_ENTITIES_CACHE
    if _ALL_ENTITIES_CACHE is None:
        static = (ORG_ENTITIES + PRODUCT_ENTITIES + TECH_ENTITIES
                  + PERSON_ENTITIES + METRIC_ENTITIES)
        _ALL_ENTITIES_CACHE = static + get_learned_entities()
    return _ALL_ENTITIES_CACHE


def get_entities_by_type(entity_type: str) -> List[Dict]:
    """按类型获取实体"""
    # G8-apply: 类型契约守卫（拒绝 None/非 str → 受控 TypeError，替代 None.upper 崩溃）
    require_text(entity_type, "entity_type")
    mapping = {
        'ORG': ORG_ENTITIES,
        'PRODUCT': PRODUCT_ENTITIES,
        'TECH': TECH_ENTITIES,
        'PERSON': PERSON_ENTITIES,
        'METRIC': METRIC_ENTITIES,
    }
    return mapping.get(entity_type.upper(), [])


def entity_count() -> dict:
    """统计实体数量"""
    return {
        'ORG': len(ORG_ENTITIES),
        'PRODUCT': len(PRODUCT_ENTITIES),
        'TECH': len(TECH_ENTITIES),
        'PERSON': len(PERSON_ENTITIES),
        'METRIC': len(METRIC_ENTITIES),
        'total': len(ORG_ENTITIES) + len(PRODUCT_ENTITIES) + len(TECH_ENTITIES) + len(PERSON_ENTITIES) + len(METRIC_ENTITIES),
    }