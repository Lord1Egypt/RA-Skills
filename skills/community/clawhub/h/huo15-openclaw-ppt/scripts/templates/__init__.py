"""
templates/ — 火一五 PPT v3.0 页面模板库

每个模板接收 (prs, pack, data) -> slide，根据 StylePack 的 tokens 自动出设计。

可用模板：
  hero_cover        封面 hero 大字
  section_divider   分章大字页
  big_stat          单数字大字页（Apple 发布会最爱）
  kpi_triple        3 宫格 KPI
  quote_card        引用金句卡
  content_list      编号列表
  compare_columns   左右对比栏
  product_shot      产品摄影页（图占大块）
  timeline          时间线
  call_to_action    行动号召（封底）
"""

from .hero_cover import build as hero_cover
from .section_divider import build as section_divider
from .big_stat import build as big_stat
from .kpi_triple import build as kpi_triple
from .quote_card import build as quote_card
from .content_list import build as content_list
from .compare_columns import build as compare_columns
from .product_shot import build as product_shot
from .timeline import build as timeline
from .call_to_action import build as call_to_action
from .code_block import build as code_block


TEMPLATES = {
    'hero_cover': hero_cover,
    'cover': hero_cover,              # alias
    'section_divider': section_divider,
    'section': section_divider,
    'big_stat': big_stat,
    'stat': big_stat,
    'kpi_triple': kpi_triple,
    'kpi': kpi_triple,
    'quote_card': quote_card,
    'quote': quote_card,
    'content_list': content_list,
    'list': content_list,
    'compare_columns': compare_columns,
    'compare': compare_columns,
    'product_shot': product_shot,
    'product': product_shot,
    'image': product_shot,
    'timeline': timeline,
    'call_to_action': call_to_action,
    'cta': call_to_action,
    'end': call_to_action,
    'code_block': code_block,
    'code': code_block,
}


def get_template(name: str):
    """拿一个 template builder。未知名回落到 content_list。"""
    return TEMPLATES.get(name, content_list)


def list_templates():
    """主模板名（去别名）。"""
    return (
        'hero_cover', 'section_divider', 'big_stat', 'kpi_triple',
        'quote_card', 'content_list', 'compare_columns', 'product_shot',
        'timeline', 'call_to_action', 'code_block',
    )
