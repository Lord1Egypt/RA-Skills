# -*- coding: utf-8 -*-
"""
PPT 版式智能匹配系统
基于45页设计版式库，根据输入内容自动推荐最适合的版式

用法:
    from ppt_layout_matcher import LayoutMatcher
    matcher = LayoutMatcher()
    recommendations = matcher.match(content_analysis)
"""

import json
import re
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple
from enum import Enum


class ContentType(Enum):
    """内容类型枚举"""
    COVER = "cover"               # 封面
    SECTION_DIVIDER = "divider"   # 章节分隔
    DATA_METRICS = "metrics"      # 数据指标
    COMPARISON_2 = "compare_2"    # 2项对比
    COMPARISON_3 = "compare_3"    # 3项对比
    COMPARISON_4 = "compare_4"    # 4项对比
    PROCESS_3 = "process_3"       # 3步流程
    PROCESS_4 = "process_4"       # 4步流程
    PROCESS_5 = "process_5"       # 5步流程
    LIST_3 = "list_3"             # 3项列表
    LIST_4 = "list_4"             # 4项列表
    LIST_N = "list_n"             # 多项列表
    GRID_2x2 = "grid_2x2"         # 2×2网格
    GRID_3x2 = "grid_3x2"         # 3×2网格
    GRID_4xN = "grid_4xn"         # 4×N网格
    GALLERY = "gallery"           # 图片画廊
    TIMELINE = "timeline"         # 时间线
    CHART_DATA = "chart_data"     # 图表+数据
    SWOT = "swot"                 # SWOT/四象限
    ONE_PAGER = "one_pager"       # 综合信息页
    TABLE = "table"               # 表格
    RADIAL = "radial"             # 中心辐射


@dataclass
class LayoutTemplate:
    """版式模板定义"""
    name: str
    slide_ref: int  # 参考Slide编号
    content_type: ContentType
    structure: str  # 布局结构描述
    keywords: List[str] = field(default_factory=list)
    n_pics: int = 0
    n_text_blocks: int = 0
    data_capacity: str = ""  # 数据承载量描述


# 版式模板库 — 基于45页PPT提炼
LAYOUT_TEMPLATES: List[LayoutTemplate] = [
    # ===== 封面 =====
    LayoutTemplate(
        name="封面-左文右图",
        slide_ref=1,
        content_type=ContentType.COVER,
        structure="左侧40%: 主标题+副标题+标签 | 右侧60%: 主视觉图",
        keywords=["封面", "首页", "标题页", "cover"],
        n_pics=1, n_text_blocks=6
    ),
    LayoutTemplate(
        name="封面-左文右图(变体)",
        slide_ref=4,
        content_type=ContentType.COVER,
        structure="同Slide1, 排版微调",
        keywords=["封面", "首页", "备选"],
        n_pics=1, n_text_blocks=6
    ),

    # ===== 过渡页 =====
    LayoutTemplate(
        name="过渡页-大数字",
        slide_ref=10,
        content_type=ContentType.SECTION_DIVIDER,
        structure="居中: 超大数字(60pt+) + 章节标题 + 半幅背景图",
        keywords=["章节", "过渡", "Part", "部分", "分隔"],
        n_pics=2, n_text_blocks=2
    ),

    # ===== 数据展示 =====
    LayoutTemplate(
        name="数据卡-左文右三卡",
        slide_ref=3,
        content_type=ContentType.DATA_METRICS,
        structure="左40%: 大段说明文字 | 右60%: 3个纵向数据卡(65%/33%/25%)",
        keywords=["数据", "指标", "百分比", "业绩", "KPI"],
        n_pics=1, n_text_blocks=17,
        data_capacity="3-5个核心指标"
    ),
    LayoutTemplate(
        name="2×2数据模块",
        slide_ref=5,
        content_type=ContentType.GRID_2x2,
        structure="2×2网格: 01-04编号 + 标题 + 描述文字 + 大图背景",
        keywords=["四象限", "矩阵", "模块", "2x2"],
        n_pics=1, n_text_blocks=15,
        data_capacity="4个并列要点"
    ),
    LayoutTemplate(
        name="图表+数据要点",
        slide_ref=16,
        content_type=ContentType.CHART_DATA,
        structure="顶部横幅标题 | 下方: 01-03编号 + 图表/数据说明",
        keywords=["图表", "柱状图", "趋势", "分析"],
        n_pics=0, n_text_blocks=13,
        data_capacity="图表+3个要点"
    ),
    LayoutTemplate(
        name="五大指标卡",
        slide_ref=28,
        content_type=ContentType.DATA_METRICS,
        structure="5列等宽: 大数字(31,178/1,121/489...) + 标签",
        keywords=["看板", "Dashboard", "指标", "数字"],
        n_pics=0, n_text_blocks=29,
        data_capacity="5个核心数字+说明"
    ),
    LayoutTemplate(
        name="3×3指标矩阵",
        slide_ref=30,
        content_type=ContentType.GRID_3x2,
        structure="3行×3列: 指标卡片矩阵",
        keywords=["矩阵", "指标", "多维"],
        n_pics=2, n_text_blocks=22,
        data_capacity="9个指标项"
    ),
    LayoutTemplate(
        name="六大指标+对比图",
        slide_ref=32,
        content_type=ContentType.DATA_METRICS,
        structure="6组数据指标 + 左右对比柱状图",
        keywords=["对比", "同比", "环比", "增长"],
        n_pics=0, n_text_blocks=29,
        data_capacity="6组对比数据"
    ),
    LayoutTemplate(
        name="表格+数据卡片",
        slide_ref=34,
        content_type=ContentType.TABLE,
        structure="顶部表格 + 4个数据卡片",
        keywords=["表格", "数据表", "汇总"],
        n_pics=0, n_text_blocks=17,
        data_capacity="表格数据+4个摘要"
    ),
    LayoutTemplate(
        name="大图背景+数据叠加",
        slide_ref=18,
        content_type=ContentType.DATA_METRICS,
        structure="左侧3叠卡 + 右侧详细数据列表",
        keywords=["年度", "总结", "概览", "核心数据"],
        n_pics=1, n_text_blocks=8,
        data_capacity="3+多行数据详情"
    ),
    LayoutTemplate(
        name="双大图+数据标签",
        slide_ref=35,
        content_type=ContentType.DATA_METRICS,
        structure="两张大图并列 + 底部数据标签",
        keywords=["案例", "展示", "对比"],
        n_pics=1, n_text_blocks=16,
        data_capacity="2组图+4-6个标签"
    ),

    # ===== 流程/步骤 =====
    LayoutTemplate(
        name="四列流程",
        slide_ref=22,
        content_type=ContentType.PROCESS_4,
        structure="4列等宽: 01-04编号 + 标题 + 描述",
        keywords=["流程", "步骤", "阶段", "项目阶段", "process"],
        n_pics=1, n_text_blocks=29
    ),
    LayoutTemplate(
        name="流程步骤+右侧详情",
        slide_ref=27,
        content_type=ContentType.PROCESS_4,
        structure="左侧: 步骤1-4+图标 | 右侧: 详细内容区",
        keywords=["功能", "特性", "说明", "产品特性"],
        n_pics=0, n_text_blocks=17
    ),
    LayoutTemplate(
        name="四步横向流程",
        slide_ref=29,
        content_type=ContentType.PROCESS_4,
        structure="横向: 01→02→03→04 + 标签+描述",
        keywords=["旅程", "路径", "横向流程", "journey"],
        n_pics=1, n_text_blocks=26
    ),
    LayoutTemplate(
        name="STEP阶梯流程",
        slide_ref=36,
        content_type=ContentType.PROCESS_4,
        structure="两行STEP01-04 + 底部4个数据指标(10年/2500+/...)",
        keywords=["里程碑", "发展", "阶段", "历程"],
        n_pics=0, n_text_blocks=27
    ),
    LayoutTemplate(
        name="左右对比+流程(混合)",
        slide_ref=23,
        content_type=ContentType.COMPARISON_2,
        structure="左侧: 流程步骤 | 右侧: 对比内容 + 底部时间线",
        keywords=["方案", "对比", "实施", "路径"],
        n_pics=1, n_text_blocks=28
    ),
    LayoutTemplate(
        name="双流程对比",
        slide_ref=41,
        content_type=ContentType.COMPARISON_4,
        structure="上下两组镜像流程: 01-04各2组",
        keywords=["业务流程", "前后对比", "优化"],
        n_pics=0, n_text_blocks=21
    ),

    # ===== 对比分析 =====
    LayoutTemplate(
        name="双栏对比要点(2×2)",
        slide_ref=15,
        content_type=ContentType.COMPARISON_4,
        structure="2×2四宫格: L1-L4对比",
        keywords=["对比", "优劣", "方案对比", "选型"],
        n_pics=0, n_text_blocks=15
    ),
    LayoutTemplate(
        name="三栏对比+说明",
        slide_ref=26,
        content_type=ContentType.COMPARISON_3,
        structure="3栏横向: 方案A/B/C + 特性列表",
        keywords=["竞品", "对比", "三选一", "方案"],
        n_pics=2, n_text_blocks=27
    ),
    LayoutTemplate(
        name="左右对比详述",
        slide_ref=33,
        content_type=ContentType.COMPARISON_2,
        structure="左右两组并列 + 连线指向内容",
        keywords=["A/B", "二选一", "对比分析"],
        n_pics=4, n_text_blocks=24
    ),
    LayoutTemplate(
        name="四象限对比(ABCD)",
        slide_ref=40,
        content_type=ContentType.SWOT,
        structure="ABCD四象限: 图标+说明文字",
        keywords=["SWOT", "矩阵", "优先级", "象限", "波士顿"],
        n_pics=0, n_text_blocks=13
    ),
    LayoutTemplate(
        name="综合对比(混合)",
        slide_ref=44,
        content_type=ContentType.COMPARISON_2,
        structure="左右对比 + 底部5行对比要点",
        keywords=["全面对比", "综合分析"],
        n_pics=1, n_text_blocks=23
    ),

    # ===== 网格/卡片 =====
    LayoutTemplate(
        name="四图网格+编号",
        slide_ref=2,
        content_type=ContentType.GRID_4xN,
        structure="4图等宽: 01-04编号 + 底部4组说明",
        keywords=["产品", "案例", "团队", "展示", "成员"],
        n_pics=4, n_text_blocks=15
    ),
    LayoutTemplate(
        name="图片矩阵陈列",
        slide_ref=13,
        content_type=ContentType.GALLERY,
        structure="大量图片矩阵排列 + 分类标签",
        keywords=["作品集", "汇总", "图集", "portfolio"],
        n_pics=18, n_text_blocks=14
    ),
    LayoutTemplate(
        name="多行网格要点",
        slide_ref=14,
        content_type=ContentType.LIST_N,
        structure="4列×多行: 密集网格",
        keywords=["功能列表", "规格", "参数", "清单"],
        n_pics=0, n_text_blocks=50
    ),
    LayoutTemplate(
        name="四象限布局",
        slide_ref=19,
        content_type=ContentType.GRID_2x2,
        structure="2×2四象限 + 中央连接区域",
        keywords=["生态", "矩阵", "布局", "平台"],
        n_pics=0, n_text_blocks=21
    ),
    LayoutTemplate(
        name="5×2网格卡片",
        slide_ref=24,
        content_type=ContentType.GRID_3x2,
        structure="5列×2行卡片网格",
        keywords=["多项目", "并列", "分类"],
        n_pics=0, n_text_blocks=36
    ),
    LayoutTemplate(
        name="四象限图标卡",
        slide_ref=38,
        content_type=ContentType.GRID_2x2,
        structure="4组: 图标+标题+描述",
        keywords=["优势", "能力", "特色", "四大"],
        n_pics=0, n_text_blocks=20
    ),
    LayoutTemplate(
        name="图片矩阵+标签",
        slide_ref=43,
        content_type=ContentType.GALLERY,
        structure="多图矩阵 + 分类标签 + 连接线",
        keywords=["品牌矩阵", "产品矩阵"],
        n_pics=16, n_text_blocks=21
    ),

    # ===== 图片展示 =====
    LayoutTemplate(
        name="时间轴画廊",
        slide_ref=9,
        content_type=ContentType.TIMELINE,
        structure="年份时间轴 + 图片矩阵 + 每项标题描述",
        keywords=["时间线", "历程", "里程碑", "历史", "发展"],
        n_pics=5, n_text_blocks=35
    ),

    # ===== 列表/要点 =====
    LayoutTemplate(
        name="三列要点",
        slide_ref=12,
        content_type=ContentType.LIST_3,
        structure="3列等宽: 01-03编号 + 标题+描述",
        keywords=["三大", "方向", "优势", "要点"],
        n_pics=1, n_text_blocks=9
    ),
    LayoutTemplate(
        name="三列+底部六卡",
        slide_ref=39,
        content_type=ContentType.LIST_N,
        structure="上部: 3列内容 | 下部: 6个卡片(01-06)",
        keywords=["总结", "分类", "总览"],
        n_pics=0, n_text_blocks=22
    ),
    LayoutTemplate(
        name="左列表+右详情卡",
        slide_ref=42,
        content_type=ContentType.LIST_N,
        structure="左侧纵向列表 + 右侧详情卡片",
        keywords=["目录", "索引", "内容概览"],
        n_pics=0, n_text_blocks=25
    ),
    LayoutTemplate(
        name="三行图文列表",
        slide_ref=45,
        content_type=ContentType.LIST_3,
        structure="3行: 大图+编号+标题+说明",
        keywords=["案例", "列表", "总结"],
        n_pics=3, n_text_blocks=6
    ),

    # ===== 综合信息图 =====
    LayoutTemplate(
        name="全景信息图",
        slide_ref=21,
        content_type=ContentType.ONE_PAGER,
        structure="复杂综合: 多图+多文本+两侧导航",
        keywords=["总览", "One Pager", "公司介绍", "项目总览"],
        n_pics=7, n_text_blocks=67
    ),

    # ===== 特殊布局 =====
    LayoutTemplate(
        name="中心辐射式",
        slide_ref=7,
        content_type=ContentType.RADIAL,
        structure="中心图标 + 四周环绕标签",
        keywords=["中心", "枢纽", "平台", "核心"],
        n_pics=0, n_text_blocks=31
    ),
    LayoutTemplate(
        name="中心图+环绕说明",
        slide_ref=8,
        content_type=ContentType.RADIAL,
        structure="中心大图 + 周围说明标签(思维导图风)",
        keywords=["思维导图", "关系", "连接", "生态"],
        n_pics=1, n_text_blocks=37
    ),
    LayoutTemplate(
        name="双图上下+说明",
        slide_ref=6,
        content_type=ContentType.COMPARISON_2,
        structure="两张图上下排列 + 左右说明",
        keywords=["对比", "案例对比"],
        n_pics=2, n_text_blocks=9
    ),
    LayoutTemplate(
        name="左标签+右详情",
        slide_ref=25,
        content_type=ContentType.LIST_N,
        structure="左侧: 分类标签列 | 右侧: 详细内容",
        keywords=["分类", "标签", "目录"],
        n_pics=0, n_text_blocks=28
    ),
    LayoutTemplate(
        name="左右双列卡",
        slide_ref=37,
        content_type=ContentType.COMPARISON_2,
        structure="左右各3个卡片",
        keywords=["双列", "卡片", "对称"],
        n_pics=0, n_text_blocks=13
    ),
    LayoutTemplate(
        name="中心焦点+三向展开",
        slide_ref=20,
        content_type=ContentType.RADIAL,
        structure="中心标题 + 三个方向展开说明",
        keywords=["总分", "展开", "聚焦"],
        n_pics=1, n_text_blocks=9
    ),
    LayoutTemplate(
        name="中心标题+四角模块",
        slide_ref=11,
        content_type=ContentType.RADIAL,
        structure="中心标题 + 四角模块+底部标签",
        keywords=["核心", "围绕", "体系"],
        n_pics=0, n_text_blocks=24
    ),
]


class LayoutMatcher:
    """PPT版式智能匹配器"""
    
    def __init__(self):
        self.templates = LAYOUT_TEMPLATES
    
    def analyze_content(self, raw_content: str) -> Dict:
        """
        分析输入内容，提取关键特征
        
        返回:
        {
            'type': ContentType,
            'n_items': int,        # 内容项数量
            'has_numbers': bool,   # 是否有数字/数据
            'has_images': bool,    # 是否提及图片
            'has_chart': bool,     # 是否需要图表
            'has_comparison': bool, # 是否涉及对比
            'has_process': bool,   # 是否涉及流程
            'has_timeline': bool,  # 是否涉及时间线
            'keywords': List[str], # 提取的关键词
        }
        """
        result = {
            'n_items': 0,
            'has_numbers': False,
            'has_images': False,
            'has_chart': False,
            'has_comparison': False,
            'has_process': False,
            'has_timeline': False,
            'keywords': [],
        }
        
        text_lower = raw_content.lower()
        
        # 检测数据/数字
        number_pattern = r'(\d+[\.,]?\d*\s*[%％万亿千百]|\d+[\.,]?\d*\s*[%％])'
        numbers = re.findall(number_pattern, raw_content)
        if numbers:
            result['has_numbers'] = True
            result['n_items'] = len(numbers)
        
        # 检测图片
        if re.search(r'图|照片|图片|展示|image|photo|pic', text_lower):
            result['has_images'] = True
        
        # 检测图表
        if re.search(r'图表|柱状|折线|饼图|chart|graph|趋势', text_lower):
            result['has_chart'] = True
        
        # 检测对比
        if re.search(r'对比|比较|vs|A/B|二选一|竞品|优劣|方案对比', text_lower):
            result['has_comparison'] = True
        
        # 检测流程
        if re.search(r'流程|步骤|阶段|step|过程|工艺', text_lower):
            result['has_process'] = True
        
        # 检测时间线
        if re.search(r'时间线|历程|发展|历史|timeline|里程碑|年', text_lower):
            result['has_timeline'] = True
        
        # 统计项数 (检测编号)
        items = re.findall(r'(?:^|\n)\s*(?:\d+[\.\、\)]|第[一二三四五六七八九十]|[一二三四五六七八九十][\.\、\)])', raw_content)
        if items:
            result['n_items'] = max(result['n_items'], len(items))
        
        # 检测2×2/四象限模式
        if re.search(r'四象限|2\s*[×xX]\s*2|swot|矩阵|四宫格', text_lower):
            result['n_items'] = 4
        
        # 提取关键词
        keyword_patterns = [
            (r'封面|首页|标题页', '封面'),
            (r'过渡|章节|分隔|part', '章节'),
            (r'指标|KPI|看板|dashboard|数据', '数据'),
            (r'产品|案例|项目|展示', '展示'),
            (r'团队|成员|组织', '团队'),
            (r'总结|回顾|复盘|总览', '总结'),
            (r'swot|矩阵|象限', '矩阵'),
            (r'竞品|对手|市场', '竞品'),
        ]
        for pattern, keyword in keyword_patterns:
            if re.search(pattern, text_lower):
                result['keywords'].append(keyword)
        
        return result
    
    def match(self, content_analysis: Dict, top_k: int = 3) -> List[Tuple[LayoutTemplate, float]]:
        """
        根据内容分析结果匹配最佳版式
        
        返回: 按匹配度排序的 (模板, 分数) 列表
        """
        scores = []
        
        for template in self.templates:
            score = 0.0
            
            # 关键词匹配 (权重: 0.3)
            keyword_hits = sum(
                1 for kw in content_analysis.get('keywords', [])
                if kw in ' '.join(template.keywords)
            )
            if keyword_hits > 0:
                score += 0.3 * (keyword_hits / max(len(content_analysis['keywords']), 1))
            
            # 数量匹配 (权重: 0.25)
            n_items = content_analysis.get('n_items', 0)
            if n_items > 0:
                # 根据模板类型判断匹配度
                ct = template.content_type
                if ct == ContentType.GRID_2x2 and n_items == 4:
                    score += 0.25
                elif ct == ContentType.GRID_3x2 and 5 <= n_items <= 9:
                    score += 0.25
                elif ct == ContentType.GRID_4xN and n_items >= 4:
                    score += 0.25
                elif ct == ContentType.PROCESS_3 and n_items == 3:
                    score += 0.25
                elif ct == ContentType.PROCESS_4 and n_items == 4:
                    score += 0.25
                elif ct == ContentType.PROCESS_5 and n_items == 5:
                    score += 0.25
                elif ct == ContentType.COMPARISON_2 and n_items == 2:
                    score += 0.25
                elif ct == ContentType.COMPARISON_3 and n_items == 3:
                    score += 0.25
                elif ct == ContentType.COMPARISON_4 and n_items == 4:
                    score += 0.25
                elif ct == ContentType.LIST_3 and n_items == 3:
                    score += 0.25
                elif ct == ContentType.LIST_4 and n_items == 4:
                    score += 0.25
                elif ct == ContentType.LIST_N and n_items >= 5:
                    score += 0.25
                elif ct == ContentType.DATA_METRICS and n_items >= 3:
                    score += 0.2
            
            # 特征匹配 (权重: 0.25)
            if content_analysis.get('has_numbers') and template.content_type in [
                ContentType.DATA_METRICS, ContentType.CHART_DATA, ContentType.TABLE
            ]:
                score += 0.25
            if content_analysis.get('has_images') and template.content_type in [
                ContentType.GALLERY, ContentType.GRID_4xN, ContentType.ONE_PAGER
            ]:
                score += 0.25
            if content_analysis.get('has_chart') and template.content_type == ContentType.CHART_DATA:
                score += 0.25
            if content_analysis.get('has_comparison') and template.content_type in [
                ContentType.COMPARISON_2, ContentType.COMPARISON_3, ContentType.COMPARISON_4
            ]:
                score += 0.25
            if content_analysis.get('has_process') and template.content_type in [
                ContentType.PROCESS_3, ContentType.PROCESS_4, ContentType.PROCESS_5
            ]:
                score += 0.25
            if content_analysis.get('has_timeline') and template.content_type == ContentType.TIMELINE:
                score += 0.25
            
            # 封面/过渡特殊匹配 (权重: 0.2)
            if '封面' in content_analysis.get('keywords', []) and template.content_type == ContentType.COVER:
                score += 0.2
            if '章节' in content_analysis.get('keywords', []) and template.content_type == ContentType.SECTION_DIVIDER:
                score += 0.2
            
            if score > 0:
                scores.append((template, round(score, 2)))
        
        # 按分数降序排列
        scores.sort(key=lambda x: x[1], reverse=True)
        return scores[:top_k]
    
    def recommend(self, raw_content: str, top_k: int = 3) -> List[Tuple[LayoutTemplate, float, Dict]]:
        """
        一步式推荐: 输入原始内容 → 返回推荐版式
        
        返回: [(模板, 分数, 内容分析结果), ...]
        """
        analysis = self.analyze_content(raw_content)
        matches = self.match(analysis, top_k)
        return [(t, s, analysis) for t, s in matches]


# ===== 便捷函数 =====

_matcher = LayoutMatcher()

def recommend_layout(content: str, top_k: int = 3):
    """快捷版式推荐"""
    return _matcher.recommend(content, top_k)

def list_all_layouts():
    """列出所有可用版式"""
    return _matcher.templates

def get_layout_by_slide(slide_num: int):
    """根据Slide编号获取版式"""
    for t in _matcher.templates:
        if t.slide_ref == slide_num:
            return t
    return None


# ===== 测试 =====
if __name__ == "__main__":
    print("=" * 60)
    print("PPT版式匹配系统 - 测试")
    print("=" * 60)
    
    test_cases = [
        "封面页：2024年度产品设计总结报告",
        "核心数据展示：用户增长65%，营收增长33%，利润率25%",
        "四个发展阶段：探索期→成长期→成熟期→突破期",
        "三大产品方案对比：方案A/B/C的优劣势分析",
        "SWOT分析：优势、劣势、机会、威胁",
        "团队四名核心成员介绍",
        "时间线：2019-2024公司发展历程",
        "章节过渡：Part 2 市场分析",
        "产品销售数据表格",
        "One Pager：项目总览",
    ]
    
    for content in test_cases:
        print(f"\n📝 输入: {content}")
        results = recommend_layout(content, top_k=2)
        for i, (template, score, analysis) in enumerate(results):
            print(f"  {'🥇' if i==0 else '🥈'} {template.name} (Slide {template.slide_ref}) - 匹配度: {score}")
            print(f"     结构: {template.structure[:80]}...")
