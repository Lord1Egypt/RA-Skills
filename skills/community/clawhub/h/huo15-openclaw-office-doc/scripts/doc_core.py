#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
doc_core.py — 火一五企业文档生成共用核心 (v7.0)

提供 Word / PDF 两套渲染器共用的：
  1. 文档规范预设（FormatPreset） — 12 种规范
  2. Block AST Markdown 解析器（修复 CJK 软换行 + 硬换行支持）
  3. 内联 token 拆分器（粗体 / 斜体 / 行内代码）
  4. 公司信息读取（委托给 company-info.py）

Word / PDF 渲染端各自处理"如何画"，本模块只负责"该画什么"。
"""

import os
import re
import sys
import json
import importlib.util


# ============================================================
# 一、文档规范预设
# ============================================================

class FormatPreset:
    """每种规范的版式参数。Word 与 PDF 渲染共用。

    v7.3 新增：把"是否显示 banner/meta/title/version/approval"做成 preset 级别开关，
    每种文体按真实场景默认。比如合同没有红色【内部】banner、没有 文档编号/版本/密级
    顶部表，演讲稿/手册/制度/信函都各自有合适的默认。CLI 仍可用 --with-* / --no-*
    覆盖。
    """

    def __init__(self, name,
                 margin_top=3.7, margin_bottom=3.5,
                 margin_left=2.8, margin_right=2.6,
                 font_body='仿宋', font_title='黑体', font_heading='黑体',
                 size_title=22, size_chapter=16, size_section=14, size_body=12,
                 line_spacing=1.5,
                 has_version_history=False, has_approval=False,
                 header_layout='company', heading_patterns=None,
                 first_line_indent_cm=0.74,
                 paragraph_spacing_pt=6,
                 table_of_contents=False,
                 # v7.3 新增的"文档壳"开关
                 show_classification_banner=True,   # 顶部右上 【内部】红字
                 show_doc_meta_table=True,          # 文档编号/版本/密级/日期 2 列表
                 show_title_block=True,             # --title 渲染成大标题
                 dedupe_h1_title=True,              # markdown 首个 H1 与 --title 同
                                                    # 文则跳过，避免重复
                 title_alignment='center',          # 'center' / 'left'
                 description=''):
        self.name = name
        self.margin_top = margin_top
        self.margin_bottom = margin_bottom
        self.margin_left = margin_left
        self.margin_right = margin_right
        self.font_body = font_body
        self.font_title = font_title
        self.font_heading = font_heading
        self.size_title = size_title
        self.size_chapter = size_chapter
        self.size_section = size_section
        self.size_body = size_body
        self.line_spacing = line_spacing
        self.has_version_history = has_version_history
        self.has_approval = has_approval
        # 'company'：LOGO + 名称（左对齐）
        # 'centered'：仅公司名（居中）— 保留备选
        # 'minimal'：仅 LOGO + 公司名（左），不带编号 / 密级
        self.header_layout = header_layout
        self.heading_patterns = heading_patterns or []
        self.first_line_indent_cm = first_line_indent_cm
        self.paragraph_spacing_pt = paragraph_spacing_pt
        self.table_of_contents = table_of_contents
        self.show_classification_banner = show_classification_banner
        self.show_doc_meta_table = show_doc_meta_table
        self.show_title_block = show_title_block
        self.dedupe_h1_title = dedupe_h1_title
        self.title_alignment = title_alignment
        self.description = description


# 公文：通知、请示、函件
PRESET_GONGWEN = FormatPreset(
    name='公文',
    description='正式公文（通知 / 请示 / 函件 / 决定 / 公告）：含密级 banner、'
                '元数据表、版本历史、审批记录。',
    heading_patterns=[
        (r'^第[一二三四五六七八九十百千]+[章节篇款]', 'chapter'),
        (r'^[一二三四五六七八九十百千]+[、．]', 'section'),
        (r'^[（\(][一二三四五六七八九十百千]+[）\)]', 'article'),
    ],
    has_version_history=True,
    has_approval=True,
    show_classification_banner=True,
    show_doc_meta_table=True,
)

# 合同 / 协议
PRESET_HETONG = FormatPreset(
    name='合同',
    description='商业合同 / 协议 / 协议书 / 补充协议：宋体、Word 标准页边距，'
                '不显示密级 banner / 元数据表（合同信息一律放在正文里）。',
    margin_top=2.54, margin_bottom=2.54, margin_left=3.17, margin_right=3.17,
    font_body='宋体', font_title='宋体', font_heading='宋体',
    size_title=22, size_chapter=15, size_section=13, size_body=12,
    heading_patterns=[
        (r'^第[一二三四五六七八九十百千]+[章节条款]', 'chapter'),
        (r'^[一二三四五六七八九十百千]+[、]', 'section'),
    ],
    has_version_history=False,
    has_approval=False,
    # v7.2: minimal（LOGO + 公司名、左对齐）；旧 'centered' 在多数中文合同里
    # 反而显得不正式，且与正文左对齐冲突。
    header_layout='minimal',
    # v7.3: 合同正文里通常已有"合同编号 / 签订日期 / 双方信息"，再加顶部
    # 密级 banner 和 文档编号/版本/密级 表只会显得花哨。
    show_classification_banner=False,
    show_doc_meta_table=False,
)

# === v7.5 合同细分（共享合同基础版式：宋体、Word 边距、无文档壳）===
# 所有合同子类视觉上等同于"合同"，差异在：keyword 自动识别 + 各自的 markdown 范本。

def _make_contract_subtype(name, description):
    """合同子类工厂：复用 PRESET_HETONG 的所有字段，只改 name / description。"""
    return FormatPreset(
        name=name,
        description=description,
        margin_top=2.54, margin_bottom=2.54, margin_left=3.17, margin_right=3.17,
        font_body='宋体', font_title='宋体', font_heading='宋体',
        size_title=22, size_chapter=15, size_section=13, size_body=12,
        heading_patterns=[
            (r'^第[一二三四五六七八九十百千]+[章节条款]', 'chapter'),
            (r'^[一二三四五六七八九十百千]+[、]', 'section'),
        ],
        has_version_history=False,
        has_approval=False,
        header_layout='minimal',
        show_classification_banner=False,
        show_doc_meta_table=False,
    )


# 劳动合同 / 雇佣合同 / 用工合同
PRESET_LAODONG = _make_contract_subtype(
    '劳动合同',
    '劳动合同 / 雇佣合同 / 用工协议 / 实习协议：HR 用，含'
    '岗位 / 工资 / 工时 / 试用期 / 保密 / 竞业限制 / 解除条款；'
    '视觉同合同基础版式，差异在结构与范本。'
)

# 服务合同 / 技术服务合同 / 咨询合同
PRESET_FUWU = _make_contract_subtype(
    '服务合同',
    '服务合同 / 技术服务合同 / 咨询合同 / 实施合同 / 维保合同：长期服务，'
    '含服务内容 / SLA / 工时 / 验收标准 / 续约条款；典型 ToB 软件 / 咨询业务用。'
)

# 技术开发合同 / 软件开发合同 / 委托开发合同
PRESET_KAIFA = _make_contract_subtype(
    '技术开发合同',
    '技术开发合同 / 软件开发合同 / 委托开发合同 / 定制开发合同：一次性开发，'
    '含开发内容 / 交付物 / 知识产权归属 / 验收 / 源码交付 / 售后维护期；'
    '可参考国家《技术合同认定登记办法》格式。'
)

# 销售合同 / 货物销售合同 / 软件许可合同
PRESET_XIAOSHOU = _make_contract_subtype(
    '销售合同',
    '销售合同 / 货物销售合同 / 产品销售合同 / 软件许可合同 / 经销合同：'
    '售方角度，含产品 / 数量 / 单价 / 总价 / 交货 / 质保 / 退换货 / 售后。'
)

# 采购合同 / 物资采购合同 / 服务采购合同
PRESET_CAIGOU = _make_contract_subtype(
    '采购合同',
    '采购合同 / 物资采购合同 / 设备采购合同 / 服务采购合同 / 框架采购协议：'
    '购方角度，含规格 / 数量 / 价格 / 交付 / 验收 / 质保 / 违约。'
)

# 保密协议 / NDA / 信息保密协议
PRESET_BAOMI = _make_contract_subtype(
    '保密协议',
    '保密协议 / NDA / 信息保密协议 / 双向保密协议 / 单向保密协议：短篇协议，'
    '含保密信息定义 / 保密义务 / 保密期限 / 例外情形 / 违约责任 / 争议解决。'
)

# 合作协议 / 战略合作协议 / 联营协议
PRESET_HEZUO = _make_contract_subtype(
    '合作协议',
    '合作协议 / 战略合作协议 / 联营协议 / 项目合作协议：有法律约束力的合作合同，'
    '区别于"备忘录 / MOU"（无约束力意向）；含合作内容 / 双方投入 / 收益分配 / '
    '退出机制 / 违约。'
)


# 会议纪要
PRESET_HUIYI = FormatPreset(
    name='会议纪要',
    description='会议纪要 / 议事记录 / 周会纪要：保留 文档编号/版本/日期 元数据表，'
                '便于追溯；不显示红色密级 banner。',
    font_body='仿宋', font_title='方正小标宋简体', font_heading='黑体',
    size_title=22, size_chapter=14, size_section=12, size_body=12,
    heading_patterns=[
        (r'^【[^】]+】', 'chapter'),
        (r'^[一二三四五六七八九十]+[、]', 'section'),
        (r'^[（\(][一二三四五六七八九十]+[）\)]', 'article'),
    ],
    has_version_history=False,
    has_approval=False,
    show_classification_banner=False,
    show_doc_meta_table=True,
)

# 技术方案 / 解决方案 / 实施方案
PRESET_FANGAN = FormatPreset(
    name='技术方案',
    description='技术方案 / 实施方案 / 解决方案 / 设计文档 / 架构设计：'
                '完整文档壳 — 密级 banner / 元数据表 / TOC / 版本历史 / 审批记录。',
    font_body='仿宋', font_title='黑体', font_heading='黑体',
    size_title=22, size_chapter=16, size_section=14, size_body=12,
    heading_patterns=[
        (r'^[一二三四五六七八九十百]+[．、]', 'chapter'),
        (r'^[0-9]+[．、](?!\d)', 'section'),
        (r'^[0-9]+\.[0-9]+', 'article'),
    ],
    has_version_history=True,
    has_approval=True,
    table_of_contents=True,
    show_classification_banner=True,
    show_doc_meta_table=True,
)

# 需求文档 / SRS / PRD
PRESET_XUQIU = FormatPreset(
    name='需求文档',
    description='需求规格 / SRS / PRD / 需求说明：完整文档壳，便于追溯与评审。',
    font_body='仿宋', font_title='黑体', font_heading='黑体',
    size_title=22, size_chapter=16, size_section=14, size_body=12,
    heading_patterns=[
        (r'^[一二三四五六七八九十百]+[．、]', 'chapter'),
        (r'^[0-9]+[．、](?!\d)', 'section'),
        (r'^[0-9]+\.[0-9]+', 'article'),
    ],
    has_version_history=True,
    has_approval=True,
    table_of_contents=True,
    show_classification_banner=True,
    show_doc_meta_table=True,
)

# 工作报告 / 周报 / 月报 / 季报 / 年报 / 述职
PRESET_GONGZUO = FormatPreset(
    name='工作报告',
    description='工作报告 / 周报 / 月报 / 季报 / 年报 / 述职报告：保留 报送对象/'
                '版本/日期 元数据；不显示红色密级 banner。',
    font_body='仿宋', font_title='方正小标宋简体', font_heading='楷体',
    size_title=22, size_chapter=16, size_section=14, size_body=12,
    heading_patterns=[
        (r'^[一二三四五六七八九十百]+[、．]', 'chapter'),
        (r'^[（\(][一二三四五六七八九十]+[）\)]', 'section'),
    ],
    has_version_history=False,
    has_approval=False,
    show_classification_banner=False,
    show_doc_meta_table=True,
)

# === v7.0 新增 6 种规范 ===

# 商业计划书 / BP / 融资计划书
PRESET_SHANGYE = FormatPreset(
    name='商业计划书',
    description='商业计划书 / BP / 融资计划书 / 路演稿：版本历史 + TOC，'
                '不显示红色密级 banner / 元数据表（投资人看的不是合规要素）。',
    font_body='仿宋', font_title='黑体', font_heading='黑体',
    size_title=24, size_chapter=18, size_section=14, size_body=12,
    line_spacing=1.5,
    heading_patterns=[
        (r'^第[一二三四五六七八九十]+部分', 'chapter'),
        (r'^[一二三四五六七八九十]+[、．]', 'chapter'),
        (r'^[0-9]+[．、](?!\d)', 'section'),
        (r'^[0-9]+\.[0-9]+', 'article'),
    ],
    has_version_history=True,
    has_approval=False,
    table_of_contents=True,
    show_classification_banner=False,
    show_doc_meta_table=False,
)

# 用户手册 / 操作手册 / 使用说明
PRESET_SHOUCE = FormatPreset(
    name='用户手册',
    description='用户手册 / 操作手册 / 使用说明 / 用户指南 / 产品手册：'
                '简洁页眉（仅 LOGO + 公司名）+ TOC + 版本历史；不显示密级 banner '
                '与文档编号表（用户看的是怎么用，不是元数据）。',
    margin_top=2.5, margin_bottom=2.5, margin_left=2.5, margin_right=2.5,
    font_body='仿宋', font_title='黑体', font_heading='黑体',
    size_title=24, size_chapter=18, size_section=14, size_body=11,
    line_spacing=1.5,
    heading_patterns=[
        (r'^第[一二三四五六七八九十百]+章', 'chapter'),
        (r'^[0-9]+\.(?!\d)', 'section'),
        (r'^[0-9]+\.[0-9]+', 'article'),
    ],
    has_version_history=True,
    has_approval=False,
    header_layout='minimal',
    table_of_contents=True,
    show_classification_banner=False,
    show_doc_meta_table=False,
)

# 培训手册 / 培训教材 / 教学大纲
PRESET_PEIXUN = FormatPreset(
    name='培训手册',
    description='培训手册 / 培训教材 / 教学大纲 / 员工手册 / 入职手册：TOC + '
                '版本历史；不显示密级 banner / 文档编号表。',
    font_body='仿宋', font_title='方正小标宋简体', font_heading='黑体',
    size_title=22, size_chapter=18, size_section=14, size_body=12,
    line_spacing=1.5,
    heading_patterns=[
        (r'^(?:模块|单元|第)[一二三四五六七八九十0-9]+(?:模块|单元|课|节)?', 'chapter'),
        (r'^[一二三四五六七八九十百]+[、．]', 'section'),
        (r'^[0-9]+\.[0-9]+', 'article'),
    ],
    has_version_history=True,
    has_approval=False,
    table_of_contents=True,
    show_classification_banner=False,
    show_doc_meta_table=False,
)

# 招投标书 / 招标书 / 投标书
PRESET_ZHAOTOU = FormatPreset(
    name='招投标书',
    description='招标书 / 投标书 / 招标文件 / 投标文件 / 响应文件：完整文档壳，'
                '密级 banner + 元数据表 + TOC + 版本历史 + 审批记录。',
    margin_top=3.7, margin_bottom=3.5, margin_left=3.0, margin_right=2.8,
    font_body='仿宋', font_title='方正小标宋简体', font_heading='黑体',
    size_title=22, size_chapter=16, size_section=14, size_body=12,
    line_spacing=1.5,
    heading_patterns=[
        (r'^第[一二三四五六七八九十百]+[章篇部分]', 'chapter'),
        (r'^[一二三四五六七八九十]+[、]', 'section'),
        (r'^[（\(][一二三四五六七八九十]+[）\)]', 'article'),
    ],
    has_version_history=True,
    has_approval=True,
    table_of_contents=True,
    show_classification_banner=True,
    show_doc_meta_table=True,
)

# 演讲稿 / 致辞稿 / 主题分享
PRESET_YANJIANG = FormatPreset(
    name='演讲稿',
    description='演讲稿 / 致辞稿 / 讲话稿 / 主题分享 / 开闭幕辞 / 颁奖辞：'
                '大字号、宽行距、无首行缩进；不带任何文档壳（banner / 元数据 / '
                '版本 / 审批），讲台前用最干净的视觉。',
    margin_top=3.0, margin_bottom=3.0, margin_left=3.0, margin_right=3.0,
    font_body='仿宋', font_title='方正小标宋简体', font_heading='黑体',
    size_title=26, size_chapter=20, size_section=16, size_body=14,
    line_spacing=1.75,
    heading_patterns=[
        (r'^[一二三四五六七八九十]+[、]', 'chapter'),
        (r'^[（\(][一二三四五六七八九十]+[）\)]', 'section'),
    ],
    has_version_history=False,
    has_approval=False,
    header_layout='minimal',
    first_line_indent_cm=0.0,
    paragraph_spacing_pt=10,
    show_classification_banner=False,
    show_doc_meta_table=False,
)

# 研究报告 / 学术论文 / 调研报告 / 白皮书
PRESET_YANJIU = FormatPreset(
    name='研究报告',
    description='研究报告 / 学术论文 / 调研报告 / 白皮书 / 行业报告：'
                'TOC + 版本历史 + 元数据表（课题/作者/日期）；不显示密级 banner '
                '（白皮书面向公众）。',
    margin_top=2.5, margin_bottom=2.5, margin_left=3.0, margin_right=3.0,
    font_body='仿宋', font_title='黑体', font_heading='黑体',
    size_title=22, size_chapter=16, size_section=14, size_body=11,
    line_spacing=1.5,
    heading_patterns=[
        (r'^摘\s*要$|^Abstract$|^关键词$|^Keywords$|^引言$|^结论$|^参考文献$|^References$',
         'chapter'),
        (r'^[一二三四五六七八九十百]+[、．]', 'chapter'),
        (r'^[0-9]+\.(?!\d)', 'section'),
        (r'^[0-9]+\.[0-9]+', 'article'),
    ],
    has_version_history=True,
    has_approval=False,
    table_of_contents=True,
    show_classification_banner=False,
    show_doc_meta_table=True,
)


# === v7.3 新增 5 种规范 ===

# 验收单 / 交付确认书 / 验收报告
PRESET_YANSHOU = FormatPreset(
    name='验收单',
    description='软件 / 硬件 / 项目交付的验收单 / 交付确认书 / 验收报告：'
                '正文里通常已有合同编号、双方信息、交付清单、验收意见、'
                '签字盖章；不再加密级 banner / 文档元数据表 / 版本历史 / 审批。',
    margin_top=2.54, margin_bottom=2.54, margin_left=2.8, margin_right=2.8,
    font_body='仿宋', font_title='黑体', font_heading='黑体',
    size_title=22, size_chapter=15, size_section=13, size_body=12,
    line_spacing=1.5,
    heading_patterns=[
        (r'^[一二三四五六七八九十]+[、]', 'chapter'),
        (r'^[（\(][一二三四五六七八九十]+[）\)]', 'section'),
        (r'^[0-9]+\.[0-9]+', 'article'),
    ],
    has_version_history=False,
    has_approval=False,
    header_layout='minimal',
    show_classification_banner=False,
    show_doc_meta_table=False,
)

# 项目立项书 / 立项申请 / 项目可行性报告
PRESET_LIXIANG = FormatPreset(
    name='项目立项书',
    description='项目立项书 / 立项申请 / 可行性研究报告 / 项目建议书：'
                '正式立项流程文件 — 密级 banner + 元数据表 + TOC + 版本历史 + '
                '审批记录。',
    margin_top=3.5, margin_bottom=3.0, margin_left=2.8, margin_right=2.6,
    font_body='仿宋', font_title='黑体', font_heading='黑体',
    size_title=22, size_chapter=16, size_section=14, size_body=12,
    line_spacing=1.5,
    heading_patterns=[
        (r'^第[一二三四五六七八九十百]+[章节部分篇]', 'chapter'),
        (r'^[一二三四五六七八九十百]+[、．]', 'chapter'),
        (r'^[0-9]+[．、](?!\d)', 'section'),
        (r'^[0-9]+\.[0-9]+', 'article'),
    ],
    has_version_history=True,
    has_approval=True,
    table_of_contents=True,
    show_classification_banner=True,
    show_doc_meta_table=True,
)

# 操作 SOP / 标准作业指导书 / 工艺文件
PRESET_SOP = FormatPreset(
    name='操作SOP',
    description='标准作业程序 / SOP / 标准作业指导书 / 工艺文件 / 操作规程：'
                '生产 / 运维 / 客服现场使用，简洁页眉 + 文档编号/版本/日期 元数据'
                '（追溯用）+ 版本历史；步骤式编号正文。',
    margin_top=2.5, margin_bottom=2.5, margin_left=2.5, margin_right=2.5,
    font_body='仿宋', font_title='黑体', font_heading='黑体',
    size_title=22, size_chapter=16, size_section=14, size_body=11,
    line_spacing=1.4,
    heading_patterns=[
        (r'^第[一二三四五六七八九十]+步', 'chapter'),
        (r'^步骤\s*\d+', 'chapter'),
        (r'^[0-9]+\.(?!\d)', 'chapter'),
        (r'^[0-9]+\.[0-9]+', 'section'),
        (r'^[0-9]+\.[0-9]+\.[0-9]+', 'article'),
    ],
    has_version_history=True,
    has_approval=False,
    header_layout='company',
    table_of_contents=True,
    show_classification_banner=False,
    show_doc_meta_table=True,
)

# 公司制度 / 规章制度 / 管理办法 / 流程规范
PRESET_ZHIDU = FormatPreset(
    name='公司制度',
    description='公司制度 / 规章制度 / 管理办法 / 流程规范 / 实施细则：'
                '完整文档壳（密级 banner + 元数据 + TOC + 版本历史 + 审批），'
                '法务 / HR 引用必备。',
    margin_top=3.5, margin_bottom=3.0, margin_left=2.8, margin_right=2.6,
    font_body='仿宋', font_title='方正小标宋简体', font_heading='黑体',
    size_title=22, size_chapter=16, size_section=14, size_body=12,
    line_spacing=1.5,
    heading_patterns=[
        (r'^第[一二三四五六七八九十百]+[章条款节]', 'chapter'),
        (r'^[一二三四五六七八九十]+[、]', 'section'),
        (r'^[（\(][一二三四五六七八九十]+[）\)]', 'article'),
    ],
    has_version_history=True,
    has_approval=True,
    table_of_contents=True,
    show_classification_banner=True,
    show_doc_meta_table=True,
)

# 信函 / 公函 / 商务函件 / 求职信 / 推荐信
PRESET_XINHAN = FormatPreset(
    name='信函',
    description='公函 / 商务函件 / 求职信 / 推荐信 / 感谢信 / 致客户函：'
                'letterhead 版式 — 大字号、抬头 + 称谓 + 正文 + 落款；'
                '不带任何文档壳，无 TOC / 版本 / 审批。',
    margin_top=3.5, margin_bottom=3.5, margin_left=3.5, margin_right=3.5,
    font_body='仿宋', font_title='黑体', font_heading='黑体',
    size_title=20, size_chapter=14, size_section=13, size_body=12,
    line_spacing=1.75,
    heading_patterns=[
        # 信函常见的"尊敬的xxx：" / "此致 敬礼" 等被识别为段落即可
    ],
    has_version_history=False,
    has_approval=False,
    header_layout='minimal',
    first_line_indent_cm=0.74,
    paragraph_spacing_pt=8,
    show_classification_banner=False,
    show_doc_meta_table=False,
    title_alignment='center',
)


# =============================================================
# === v7.4 新增 15 种规范（HR / Sales / PR / Ops / PM / Tech）===
# =============================================================

# 个人简历 / 简历 / CV
PRESET_JIANLI = FormatPreset(
    name='个人简历',
    description='个人简历 / 简历 / CV / Resume：紧凑单页布局，分基本信息 / '
                '教育经历 / 工作经历 / 项目经验 / 技能特长 / 自我评价；'
                '不挂任何文档壳，无 TOC / 版本史 / 审批。',
    margin_top=2.0, margin_bottom=2.0, margin_left=2.0, margin_right=2.0,
    font_body='仿宋', font_title='黑体', font_heading='黑体',
    size_title=22, size_chapter=14, size_section=12, size_body=11,
    line_spacing=1.3,
    heading_patterns=[],
    has_version_history=False,
    has_approval=False,
    header_layout='minimal',
    first_line_indent_cm=0.0,
    paragraph_spacing_pt=4,
    show_classification_banner=False,
    show_doc_meta_table=False,
)

# 报价单 / 商务报价 / 询价回复
PRESET_BAOJIA = FormatPreset(
    name='报价单',
    description='报价单 / 商务报价 / 报价书 / 询价回复：表格驱动，'
                '正文里通常已有报价编号 / 报价日期 / 有效期 / 客户信息 / 合计金额；'
                '不挂密级 banner / 元数据表（避免与正文重复）。',
    margin_top=2.5, margin_bottom=2.5, margin_left=2.5, margin_right=2.5,
    font_body='仿宋', font_title='黑体', font_heading='黑体',
    size_title=20, size_chapter=14, size_section=12, size_body=11,
    line_spacing=1.4,
    heading_patterns=[
        (r'^[一二三四五六七八九十]+[、]', 'chapter'),
    ],
    has_version_history=False,
    has_approval=False,
    header_layout='minimal',
    show_classification_banner=False,
    show_doc_meta_table=False,
)

# 新闻稿 / 媒体通稿 / 发布稿
PRESET_XINWEN = FormatPreset(
    name='新闻稿',
    description='新闻稿 / 媒体通稿 / 发布稿 / 媒体稿：dateline + 主体 + '
                '媒体联系人，面向公众发布；不挂任何内部文档壳。',
    margin_top=2.5, margin_bottom=2.5, margin_left=3.0, margin_right=3.0,
    font_body='仿宋', font_title='黑体', font_heading='黑体',
    size_title=22, size_chapter=14, size_section=12, size_body=12,
    line_spacing=1.6,
    heading_patterns=[
        (r'^[一二三四五六七八九十]+[、]', 'chapter'),
    ],
    has_version_history=False,
    has_approval=False,
    header_layout='minimal',
    show_classification_banner=False,
    show_doc_meta_table=False,
)

# 复盘报告 / 项目复盘 / 项目总结
PRESET_FUPAN = FormatPreset(
    name='复盘报告',
    description='项目复盘 / 复盘报告 / 项目总结 / 月度复盘 / 年度复盘：'
                '保留项目名 / 复盘日期 / 参与人 元数据，TOC + 版本史；'
                '典型结构 — 背景 / 目标 / 结果 / 亮点 / 问题 / 根因 / 改进项。',
    margin_top=3.0, margin_bottom=3.0, margin_left=2.8, margin_right=2.6,
    font_body='仿宋', font_title='黑体', font_heading='黑体',
    size_title=22, size_chapter=16, size_section=14, size_body=12,
    line_spacing=1.5,
    heading_patterns=[
        (r'^[一二三四五六七八九十百]+[、．]', 'chapter'),
        (r'^[0-9]+[．、](?!\d)', 'section'),
        (r'^[0-9]+\.[0-9]+', 'article'),
    ],
    has_version_history=True,
    has_approval=False,
    table_of_contents=True,
    show_classification_banner=False,
    show_doc_meta_table=True,
)

# 测试报告 / QA 报告 / 验证报告
PRESET_CESHI = FormatPreset(
    name='测试报告',
    description='测试报告 / QA 报告 / 验证报告 / 性能测试 / 功能测试报告：'
                '完整文档壳 — banner + meta + TOC + 版本史 + 审批；'
                '典型结构 — 测试范围 / 测试方法 / 测试用例 / 缺陷统计 / 结论。',
    margin_top=3.0, margin_bottom=3.0, margin_left=2.8, margin_right=2.6,
    font_body='仿宋', font_title='黑体', font_heading='黑体',
    size_title=22, size_chapter=16, size_section=14, size_body=12,
    line_spacing=1.5,
    heading_patterns=[
        (r'^[一二三四五六七八九十百]+[、．]', 'chapter'),
        (r'^[0-9]+[．、](?!\d)', 'section'),
        (r'^[0-9]+\.[0-9]+', 'article'),
    ],
    has_version_history=True,
    has_approval=True,
    table_of_contents=True,
    show_classification_banner=True,
    show_doc_meta_table=True,
)

# 故障报告 / 事故报告 / postmortem
PRESET_GUZHANG = FormatPreset(
    name='故障报告',
    description='故障报告 / 事故报告 / 故障复盘 / 事故分析 / postmortem：'
                'banner 标"内部"，事件编号 / 发生时间 / 影响范围 / 严重程度 元数据；'
                '典型结构 — 事件经过 / 根因分析 / 影响评估 / 处置措施 / 改进项。',
    margin_top=3.0, margin_bottom=3.0, margin_left=2.8, margin_right=2.6,
    font_body='仿宋', font_title='黑体', font_heading='黑体',
    size_title=22, size_chapter=16, size_section=14, size_body=12,
    line_spacing=1.5,
    heading_patterns=[
        (r'^[一二三四五六七八九十百]+[、．]', 'chapter'),
        (r'^[0-9]+[．、](?!\d)', 'section'),
        (r'^[0-9]+\.[0-9]+', 'article'),
    ],
    has_version_history=False,
    has_approval=False,
    table_of_contents=False,
    show_classification_banner=True,
    show_doc_meta_table=True,
)

# 任命书 / 聘任书 / 委任书
PRESET_RENMING = FormatPreset(
    name='任命书',
    description='任命书 / 聘任书 / 聘用书 / 委任书 / 任命决定：letterhead 版式，'
                '正文 + 落款 + 签字盖章；标题居中加大；无文档壳。',
    margin_top=3.5, margin_bottom=3.5, margin_left=3.5, margin_right=3.5,
    font_body='仿宋', font_title='方正小标宋简体', font_heading='黑体',
    size_title=24, size_chapter=14, size_section=12, size_body=13,
    line_spacing=1.75,
    heading_patterns=[],
    has_version_history=False,
    has_approval=False,
    header_layout='minimal',
    first_line_indent_cm=0.74,
    paragraph_spacing_pt=10,
    show_classification_banner=False,
    show_doc_meta_table=False,
    title_alignment='center',
)

# 应急预案 / 应急响应预案
PRESET_YINGJI = FormatPreset(
    name='应急预案',
    description='应急预案 / 应急响应预案 / 应急处置方案 / 应急响应方案：'
                '完整文档壳；典型结构 — 适用范围 / 分级标准 / 组织机构 / '
                '响应流程 / 处置措施 / 通讯录 / 演练。',
    margin_top=3.0, margin_bottom=3.0, margin_left=2.8, margin_right=2.6,
    font_body='仿宋', font_title='黑体', font_heading='黑体',
    size_title=22, size_chapter=16, size_section=14, size_body=12,
    line_spacing=1.5,
    heading_patterns=[
        (r'^第[一二三四五六七八九十百]+[章节部分]', 'chapter'),
        (r'^[一二三四五六七八九十百]+[、．]', 'chapter'),
        (r'^[0-9]+[．、](?!\d)', 'section'),
        (r'^[0-9]+\.[0-9]+', 'article'),
    ],
    has_version_history=True,
    has_approval=True,
    table_of_contents=True,
    show_classification_banner=True,
    show_doc_meta_table=True,
)

# 在职证明 / 离职证明 / 工作证明
PRESET_ZAIZHI = FormatPreset(
    name='在职证明',
    description='在职证明 / 离职证明 / 工作证明 / 收入证明 / 实习证明：'
                'letterhead 版式，单页，无文档壳，落款盖章。',
    margin_top=3.5, margin_bottom=3.5, margin_left=3.5, margin_right=3.5,
    font_body='仿宋', font_title='黑体', font_heading='黑体',
    size_title=22, size_chapter=14, size_section=12, size_body=13,
    line_spacing=1.75,
    heading_patterns=[],
    has_version_history=False,
    has_approval=False,
    header_layout='minimal',
    first_line_indent_cm=0.74,
    paragraph_spacing_pt=10,
    show_classification_banner=False,
    show_doc_meta_table=False,
    title_alignment='center',
)

# 风险评估报告 / 风险报告
PRESET_FENGXIAN = FormatPreset(
    name='风险评估报告',
    description='风险评估报告 / 风险报告 / 风险分析 / 安全评估：'
                '完整文档壳；典型结构 — 评估范围 / 风险识别 / 风险矩阵 / '
                '应对措施 / 残余风险。',
    margin_top=3.0, margin_bottom=3.0, margin_left=2.8, margin_right=2.6,
    font_body='仿宋', font_title='黑体', font_heading='黑体',
    size_title=22, size_chapter=16, size_section=14, size_body=12,
    line_spacing=1.5,
    heading_patterns=[
        (r'^[一二三四五六七八九十百]+[、．]', 'chapter'),
        (r'^[0-9]+[．、](?!\d)', 'section'),
        (r'^[0-9]+\.[0-9]+', 'article'),
    ],
    has_version_history=True,
    has_approval=True,
    table_of_contents=True,
    show_classification_banner=True,
    show_doc_meta_table=True,
)

# 项目计划书 / 项目执行计划
PRESET_JIHUA = FormatPreset(
    name='项目计划书',
    description='项目计划书 / 项目执行计划 / 项目实施计划 / 项目章程：'
                '完整文档壳；典型结构 — 项目背景 / 目标 / 范围 / 里程碑 / '
                '资源 / 风险 / 沟通计划。',
    margin_top=3.0, margin_bottom=3.0, margin_left=2.8, margin_right=2.6,
    font_body='仿宋', font_title='黑体', font_heading='黑体',
    size_title=22, size_chapter=16, size_section=14, size_body=12,
    line_spacing=1.5,
    heading_patterns=[
        (r'^[一二三四五六七八九十百]+[、．]', 'chapter'),
        (r'^[0-9]+[．、](?!\d)', 'section'),
        (r'^[0-9]+\.[0-9]+', 'article'),
    ],
    has_version_history=True,
    has_approval=True,
    table_of_contents=True,
    show_classification_banner=True,
    show_doc_meta_table=True,
)

# 项目结项报告 / 项目验收 / 项目收尾
PRESET_JIEXIANG = FormatPreset(
    name='项目结项报告',
    description='项目结项报告 / 项目收尾报告 / 项目交付总结 / 项目结题：'
                '保留 meta + 版本史 + 审批；典型结构 — 项目概况 / 目标完成情况 / '
                '交付物 / 经验教训 / 后续支持。',
    margin_top=3.0, margin_bottom=3.0, margin_left=2.8, margin_right=2.6,
    font_body='仿宋', font_title='黑体', font_heading='黑体',
    size_title=22, size_chapter=16, size_section=14, size_body=12,
    line_spacing=1.5,
    heading_patterns=[
        (r'^[一二三四五六七八九十百]+[、．]', 'chapter'),
        (r'^[0-9]+[．、](?!\d)', 'section'),
        (r'^[0-9]+\.[0-9]+', 'article'),
    ],
    has_version_history=True,
    has_approval=True,
    table_of_contents=True,
    show_classification_banner=False,
    show_doc_meta_table=True,
)

# API 文档 / 接口文档
PRESET_API = FormatPreset(
    name='API文档',
    description='API 文档 / 接口文档 / 接口规范 / Open API：'
                '简洁页眉 + 元数据 + TOC + 版本史；典型结构 — 概述 / 鉴权 / '
                '端点列表 / 请求 / 响应 / 错误码 / 变更日志。',
    margin_top=2.5, margin_bottom=2.5, margin_left=2.5, margin_right=2.5,
    font_body='仿宋', font_title='黑体', font_heading='黑体',
    size_title=22, size_chapter=16, size_section=14, size_body=11,
    line_spacing=1.5,
    heading_patterns=[
        (r'^[A-Z]+\s+/\S+', 'section'),  # `GET /api/foo` 风格
        (r'^[0-9]+\.(?!\d)', 'chapter'),
        (r'^[0-9]+\.[0-9]+', 'section'),
        (r'^[0-9]+\.[0-9]+\.[0-9]+', 'article'),
    ],
    has_version_history=True,
    has_approval=False,
    header_layout='minimal',
    table_of_contents=True,
    show_classification_banner=False,
    show_doc_meta_table=True,
)

# 部署文档 / 上线手册 / 运维手册
PRESET_BUSHU = FormatPreset(
    name='部署文档',
    description='部署文档 / 部署手册 / 上线手册 / 运维手册 / 运维操作 / Runbook：'
                '简洁页眉 + 元数据 + TOC + 版本史；典型结构 — 环境要求 / 依赖 / '
                '步骤 / 验证 / 回滚 / 故障排查。',
    margin_top=2.5, margin_bottom=2.5, margin_left=2.5, margin_right=2.5,
    font_body='仿宋', font_title='黑体', font_heading='黑体',
    size_title=22, size_chapter=16, size_section=14, size_body=11,
    line_spacing=1.5,
    heading_patterns=[
        (r'^第[一二三四五六七八九十]+步', 'chapter'),
        (r'^步骤\s*\d+', 'chapter'),
        (r'^[0-9]+\.(?!\d)', 'chapter'),
        (r'^[0-9]+\.[0-9]+', 'section'),
    ],
    has_version_history=True,
    has_approval=False,
    header_layout='minimal',
    table_of_contents=True,
    show_classification_banner=False,
    show_doc_meta_table=True,
)

# 备忘录 / MOU / 合作意向书
PRESET_BEIWANG = FormatPreset(
    name='备忘录',
    description='备忘录 / MOU / 合作意向书 / 战略合作备忘录：letterhead 版式，'
                '段落式表述，无文档壳；典型结构 — 双方信息 / 合作背景 / '
                '合作内容 / 双方责任 / 有效期 / 落款。',
    margin_top=3.0, margin_bottom=3.0, margin_left=3.0, margin_right=3.0,
    font_body='仿宋', font_title='黑体', font_heading='黑体',
    size_title=22, size_chapter=14, size_section=12, size_body=12,
    line_spacing=1.6,
    heading_patterns=[
        (r'^[一二三四五六七八九十]+[、]', 'chapter'),
        (r'^[（\(][一二三四五六七八九十]+[）\)]', 'section'),
    ],
    has_version_history=False,
    has_approval=False,
    header_layout='minimal',
    show_classification_banner=False,
    show_doc_meta_table=False,
)


FORMAT_PRESETS = {
    '公文': PRESET_GONGWEN,
    '合同': PRESET_HETONG,
    '会议纪要': PRESET_HUIYI,
    '技术方案': PRESET_FANGAN,
    '需求文档': PRESET_XUQIU,
    '工作报告': PRESET_GONGZUO,
    '商业计划书': PRESET_SHANGYE,
    '用户手册': PRESET_SHOUCE,
    '培训手册': PRESET_PEIXUN,
    '招投标书': PRESET_ZHAOTOU,
    '演讲稿': PRESET_YANJIANG,
    '研究报告': PRESET_YANJIU,
    # v7.3 新增
    '验收单': PRESET_YANSHOU,
    '项目立项书': PRESET_LIXIANG,
    '操作SOP': PRESET_SOP,
    '公司制度': PRESET_ZHIDU,
    '信函': PRESET_XINHAN,
    # v7.4 新增（HR / Sales / PR / Ops / PM / Tech 共 15 类）
    '个人简历': PRESET_JIANLI,
    '报价单': PRESET_BAOJIA,
    '新闻稿': PRESET_XINWEN,
    '复盘报告': PRESET_FUPAN,
    '测试报告': PRESET_CESHI,
    '故障报告': PRESET_GUZHANG,
    '任命书': PRESET_RENMING,
    '应急预案': PRESET_YINGJI,
    '在职证明': PRESET_ZAIZHI,
    '风险评估报告': PRESET_FENGXIAN,
    '项目计划书': PRESET_JIHUA,
    '项目结项报告': PRESET_JIEXIANG,
    'API文档': PRESET_API,
    '部署文档': PRESET_BUSHU,
    '备忘录': PRESET_BEIWANG,
    # v7.5 合同细分（7 类）
    '劳动合同': PRESET_LAODONG,
    '服务合同': PRESET_FUWU,
    '技术开发合同': PRESET_KAIFA,
    '销售合同': PRESET_XIAOSHOU,
    '采购合同': PRESET_CAIGOU,
    '保密协议': PRESET_BAOMI,
    '合作协议': PRESET_HEZUO,
}


# 命中顺序：先具体的、独占词；再宽松词。'auto' 命中后立即返回。
FORMAT_KEYWORDS = [
    # ==== v7.5 合同细分（必须在通用"合同"之前，避免被截胡）====
    ('劳动合同', ['劳动合同', '雇佣合同', '用工合同', '用工协议',
                '实习协议', '实习合同', '兼职合同']),
    ('技术开发合同', ['技术开发合同', '软件开发合同', '委托开发合同',
                    '定制开发合同', '开发合同', '软件定制合同',
                    '硬件开发合同']),
    ('服务合同', ['服务合同', '技术服务合同', '咨询合同', '咨询服务合同',
                '实施合同', '实施服务合同', '维保合同', '维护合同',
                '运维合同', 'SaaS合同', 'SaaS服务合同']),
    ('销售合同', ['销售合同', '货物销售合同', '产品销售合同',
                '软件许可合同', '软件许可协议', 'license协议', '经销合同',
                '代销合同']),
    ('采购合同', ['采购合同', '物资采购合同', '设备采购合同',
                '服务采购合同', '框架采购协议', '采购协议',
                '采购订单合同']),
    ('保密协议', ['保密协议', 'NDA', '信息保密协议', '双向保密协议',
                '单向保密协议', '保密合同', '保密承诺书']),
    ('合作协议', ['战略合作协议', '联营协议', '项目合作协议', '合作协议',
                '联合开发协议', '合作合同']),
    # ==== v7.4 新增（最高优先级；文体名比 "合同/方案/报告" 等更具体）====
    ('个人简历', ['个人简历', '简历', 'resume', 'curriculum vitae', 'CV']),
    ('报价单', ['报价单', '商务报价', '报价书', '询价回复', '报价回复',
            '商业报价']),
    ('新闻稿', ['新闻稿', '媒体通稿', '发布稿', '媒体稿', '宣传稿',
            'press release']),
    ('复盘报告', ['复盘报告', '项目复盘', '复盘', '项目总结',
                '月度复盘', '年度复盘', '季度复盘']),
    ('测试报告', ['测试报告', 'QA报告', '验证报告', '功能测试报告',
                '性能测试报告', '集成测试报告', '回归测试报告']),
    ('故障报告', ['故障报告', '事故报告', '故障复盘', '事故分析',
                '事后分析', '根因分析报告', 'postmortem',
                'post-mortem', '故障复盘报告']),
    ('任命书', ['任命书', '聘任书', '聘用书', '委任书', '任命决定',
            '任命通知']),
    ('应急预案', ['应急预案', '应急响应预案', '应急处置方案',
                '应急响应方案', '应急处置预案']),
    ('在职证明', ['在职证明', '离职证明', '工作证明', '收入证明',
                '实习证明', '解除劳动关系证明']),
    ('风险评估报告', ['风险评估报告', '风险评估', '风险分析', '风险报告',
                    '安全评估', '安全评估报告', '信息安全评估']),
    ('项目计划书', ['项目计划书', '项目执行计划', '项目实施计划',
                '项目章程', '项目作战计划']),
    ('项目结项报告', ['项目结项报告', '项目收尾报告', '项目交付总结',
                '项目结题', '项目结项', '结项报告']),
    ('API文档', ['API文档', 'API 文档', '接口文档', '接口规范',
              'open api', 'openapi', 'API spec', 'API规范']),
    ('部署文档', ['部署文档', '部署手册', '上线手册', '运维手册',
                '运维操作手册', 'runbook', '部署指南', '上线指南']),
    ('备忘录', ['备忘录', 'MOU', '合作意向书', '战略合作备忘录',
            '合作备忘录', 'memorandum of understanding']),
    # ==== v7.3 新增 ====
    ('验收单', ['验收单', '验收报告', '交付确认书', '交付单', '验收意见书',
            '项目验收', '系统验收']),
    ('项目立项书', ['项目立项', '立项申请', '立项书', '项目建议书',
                '可行性研究报告', '可行性报告', '立项报告']),
    ('操作SOP', ['操作SOP', 'SOP', '标准作业指导书', '标准作业程序',
              '工艺文件', '操作规程', '作业指导书']),
    ('公司制度', ['公司制度', '规章制度', '管理办法', '管理规定',
              '实施细则', '管理细则', '工作流程规范', '管理规范',
              '章程', '议事规则', '议事章程', '会议章程',
              '员工守则', '行为准则']),
    ('信函', ['公函', '商务函件', '求职信', '推荐信', '感谢信',
            '致客户函', '致合作伙伴', '致供应商', '致股东', '邀请函']),
    # ==== 既有（注意 v7.3 把"协议书"放进了"合同"，所以"补充协议"也走合同）====
    ('招投标书', ['招标书', '投标书', '招投标', '投标文件', '招标文件', '响应文件']),
    ('商业计划书', ['商业计划书', '商业计划', 'BP', '融资计划书', '融资计划', '路演稿']),
    ('用户手册', ['用户手册', '操作手册', '使用说明', '用户指南', '使用手册',
              'manual', '产品手册']),
    ('培训手册', ['培训手册', '培训教材', '培训方案', '教学大纲', '员工手册',
              '入职手册']),
    ('演讲稿', ['演讲稿', '致辞稿', '讲话稿', '主题分享', '演讲提纲', '开幕辞',
            '开幕词', '闭幕辞', '欢迎辞', '颁奖辞']),
    ('研究报告', ['研究报告', '学术论文', '调研报告', '白皮书', 'whitepaper',
              '行业报告', '分析报告', '论文']),
    ('合同', ['合同', '协议', '协议书', '补充协议']),
    ('会议纪要', ['会议纪要', '纪要']),
    ('技术方案', ['技术方案', '实施方案', '解决方案', '设计文档', '架构设计']),
    ('需求文档', ['需求规格', '需求说明', 'srs', 'prd', '需求文档']),
    ('工作报告', ['工作报告', '周报', '月报', '季报', '年报', '述职报告',
              '汇报材料']),
]


def detect_format(title='', content=''):
    """根据标题和正文前 800 字猜测规范类型，默认公文。"""
    text = (title + ' ' + (content or '')[:800]).lower()
    for fmt, keywords in FORMAT_KEYWORDS:
        for kw in keywords:
            if kw.lower() in text:
                return fmt
    return '公文'


def get_preset(format_name):
    return FORMAT_PRESETS.get(format_name, PRESET_GONGWEN)


def list_format_names():
    return list(FORMAT_PRESETS.keys())


# ============================================================
# 二、Block AST 解析（修复 CJK 软换行 + 硬换行）
# ============================================================

_HEADING_MD_RE = re.compile(r'^(#{1,6})\s*(.+?)\s*#*\s*$')
_HR_RE = re.compile(r'^\s*([-*_])\1{2,}\s*$')
_UL_ITEM_RE = re.compile(r'^\s*[-*+]\s+(.+)$')
_OL_ITEM_RE = re.compile(r'^\s*(\d+)[\.．)]\s+(.+)$')
_FENCE_RE = re.compile(r'^\s*```([\w+-]*)\s*$')
_BLOCKQUOTE_RE = re.compile(r'^\s*>\s?(.*)$')
_TABLE_SEP_CELL_RE = re.compile(r'^[:\s]*[\-−–—―]{3,}[:\s]*$')
# v7.6.1：抽出关键词常量；后面 _is_known_metadata_key 会用 `(?:^|\s)` 边界搜索，
# 让 `WordPress 版本：` / `服务合同编号：` 这类带前缀的 key 也能识别。
_DOC_META_WORDS_RAW = (
    '文档编号|文件编号|项目编号|发文字号|合同编号|合同号|协议编号|订单编号|'
    '报价编号|工单编号|发票编号|凭证编号|编号|'
    '版本|版次|密级|机密等级|分类|类型|类别|状态|阶段|'
    '日期|时间|签订日期|签约日期|签署日期|生效日期|失效日期|验收日期|'
    '交付日期|出版日期|提交日期|有效期|截止日期|期限|起止时间|起草日期|'
    '起止日期|完成日期|'
    '作者|编制|起草|审核|批准|签发|提交人|主送|抄送|联系人|负责人|'
    '甲方|乙方|丙方|签约方|发包方|承包方|采购方|供应商|'
    '客户|项目|课题|主题|标题|副标题|关键词|摘要|背景|目的|备注|说明|'
    '金额|总价|单价|数量|币种|含税|税率|税额|付款方式|付款条件|'
    '单位|部门|公司|地址|电话|邮箱|手机|传真|网址|官网|联系方式|'
    # v7.6.1 web/通用补充
    '站点|站点名称|网站|网站名称|域名|URL|链接|名称|类目|品牌|'
    'Title|Subject|Author|Date|Version|Keywords|Abstract|Department|'
    'Owner|Reviewer|Approver|Status|ContractNo|ContractNumber'
)

_DOC_META_RE = re.compile(r'(?:' + _DOC_META_WORDS_RAW + r')\s*[:：]')

# v7.6.1：词边界搜索版 — 允许 'XXX 版本：' / 'XXX 编号：' 这种带前缀的 key
_DOC_META_BOUNDARY_RE = re.compile(
    r'(?:^|[\s,，、；;])(?:' + _DOC_META_WORDS_RAW + r')\s*[:：]'
)

# 单行 'Key: Value' 模式（Key 须 ≤24 字、不含分隔符）
# v7.2 把上限从 16 → 24，覆盖 `**合同编号**` / `***甲    方***` 这类 markdown 包裹的 key。
_SHORT_KV_RE = re.compile(r'^\s*([^：:|<>\n]{1,24}?)\s*[:：]\s*(.+?)\s*$')

# v7.2 markdown 包裹标记：粗体 `**` / 斜体 `*` / 删除线 `~~` / 行内代码 ` ` `
_MD_WRAP_CHARS = '*~` '

# CJK 字符范围：常见汉字 + 全角标点 + 扩展
_CJK_CHAR_RE = re.compile(
    r'[一-鿿㐀-䶿　-〿＀-｠゠-ヿ'
    r'぀-ゟ]'
)


def _is_cjk_char(c):
    return bool(c and _CJK_CHAR_RE.match(c))


def _detect_hard_break(line):
    """识别行尾硬换行标记，返回 (有效正文, has_hard_break)。

    支持两种约定：
      - Markdown 标准：行尾 2 个及以上空格
      - CommonMark 扩展：行尾反斜杠 `\\`
    """
    s = line.rstrip('\r\n')
    if s.endswith('\\'):
        return s[:-1].rstrip(), True
    trimmed = s.rstrip(' \t')
    if len(s) - len(trimmed) >= 2:
        return trimmed, True
    return trimmed, False


def _smart_join_paragraph(items):
    """合并段落多行：

    items: [(text, hard_break_after), ...]
    - hard_break_after=True 处插入 '\n'（渲染端转 <w:br/> 或 <br/>）
    - 否则按 CJK 边界智能拼接：CJK ↔ CJK 不加空格；其余加单空格
    """
    if not items:
        return ''
    out = items[0][0]
    for i in range(1, len(items)):
        prev_text, prev_hb = items[i - 1]
        cur_text, _ = items[i]
        if not cur_text and not prev_hb:
            continue
        if prev_hb:
            sep = '\n'
        else:
            last = out[-1] if out else ''
            first = cur_text[0] if cur_text else ''
            if _is_cjk_char(last) and _is_cjk_char(first):
                sep = ''
            elif not last or not first:
                sep = ''
            else:
                sep = ' '
        out += sep + cur_text
    return out


def _split_table_cells(line):
    r"""智能分割表格行；保留前后 | 之间的内容；允许 `\|` 转义。"""
    s = line.strip()
    leading = s.startswith('|')
    trailing = s.endswith('|') and not s.endswith(r'\|')
    if leading and trailing and len(s) >= 2:
        s = s[1:-1]
    elif leading:
        s = s[1:]
    elif trailing:
        s = s[:-1]

    cells, buf, i = [], '', 0
    while i < len(s):
        ch = s[i]
        if ch == '\\' and i + 1 < len(s) and s[i + 1] == '|':
            buf += '|'
            i += 2
            continue
        if ch == '|':
            cells.append(buf.strip())
            buf = ''
        else:
            buf += ch
        i += 1
    cells.append(buf.strip())
    return cells


def _is_table_separator(line):
    t = line.strip()
    if not t or '|' not in t:
        return False
    cells = _split_table_cells(t)
    if len(cells) < 2:
        return False
    has_sep = False
    for c in cells:
        if not c:
            continue
        if _TABLE_SEP_CELL_RE.match(c):
            has_sep = True
        else:
            return False
    return has_sep


def _looks_like_table_row(line):
    t = line.strip()
    if '|' not in t:
        return False
    if _is_table_separator(t):
        return False
    cells = _split_table_cells(t)
    return len(cells) >= 2


def _is_metadata_line(line):
    """style A：单行 pipe 分隔的元数据。"""
    t = line.strip()
    if '|' not in t:
        return False
    segments = [seg.strip() for seg in _split_table_cells(t) if seg.strip()]
    if len(segments) < 2:
        return False
    meta_hits = sum(1 for seg in segments if _DOC_META_RE.search(seg))
    return meta_hits >= 2


def _is_known_metadata_key(key):
    """key 是否在已知元数据关键词表内（用于识别 style B 多行元数据）。

    v7.6.1：用词边界搜索取代严格起首匹配，`WordPress 版本` / `服务合同编号`
    这类带前缀的 key 也能匹配。前缀必须是开头或空白 / 中文标点之一，避免
    `今天版本` 这种非词边界拼接被误判。
    """
    return bool(_DOC_META_BOUNDARY_RE.search(key.strip() + '：'))


def _try_kv_line(line):
    """style B：单行 'Key: Value' 形式；要求 Key 是已知关键词。

    返回 (key, value) 或 None。

    v7.2：兼容 markdown 包裹形式（`**合同编号：** value` / `*Key:* value`），
    剥掉首尾的 `*` / `~` / `` ` `` 之后再判断 key 是否在白名单。
    """
    if not line:
        return None
    s = line.strip()
    if '|' in s:
        return None
    m = _SHORT_KV_RE.match(s)
    if not m:
        return None
    key = m.group(1).strip(_MD_WRAP_CHARS).strip()
    value = m.group(2).strip(_MD_WRAP_CHARS).strip()
    if not key:
        return None
    if not _is_known_metadata_key(key):
        return None
    return key, value


def _try_kv_line_lenient(line):
    """v7.6.1: lenient KV 检测 — 不要求 key 在白名单，只看形式。

    用作 fallback：当 ≥3 行连续的 Key:Value 形式出现时（即使 key 不在白名单），
    用户意图就是 "每行单独一行" / 元数据列表。常见场景：
        站点名称：xxx
        WordPress 版本：6.9.4
        WooCommerce 版本：10.6.1
        主题：WoodMart 8.4.1
        ...
    旧版只走严格白名单，第一行 `站点名称` 不在白名单 → 整段被 _smart_join_paragraph
    合成单行。lenient 兜底解决这个 case。

    阈值由调用方控制（建议 ≥3，避免单条对话 / 定义被误判）。
    """
    if not line:
        return None
    s = line.strip()
    if '|' in s:
        return None
    m = _SHORT_KV_RE.match(s)
    if not m:
        return None
    key = m.group(1).strip(_MD_WRAP_CHARS).strip()
    value = m.group(2).strip(_MD_WRAP_CHARS).strip()
    if not key or not value:
        return None
    # 排除明显不是元数据的：key 含空格 + 长度 > 30、或 value 是引号包裹的对话
    if len(key) > 30:
        return None
    return key, value


def parse_blocks(content):
    """把 Markdown 文本切成块节点列表。

    每个节点是 dict，含 `type` 与对应负载：
      - heading      : {level: 1..6, text}
      - paragraph    : {text}      文本中的 '\n' 表示硬换行
      - list         : {ordered: bool, items: [text, ...]}
      - table        : {rows: [[cell, ...], ...], has_header: bool}
      - code_block   : {lang, code}
      - blockquote   : {lines: [text, ...]}
      - metadata     : {pairs: [(key, value), ...]}
      - hr           : {}
      - page_break   : {}    (---PAGE--- 或 \\pagebreak)
    """
    lines = (content or '').split('\n')
    blocks = []
    i = 0
    n = len(lines)

    while i < n:
        raw = lines[i]
        stripped = raw.strip()

        if not stripped:
            i += 1
            continue

        # 显式分页符
        if stripped.lower() in ('---page---', '\\pagebreak', '<!-- pagebreak -->'):
            blocks.append({'type': 'page_break'})
            i += 1
            continue

        # 代码块
        fence = _FENCE_RE.match(raw)
        if fence:
            lang = fence.group(1) or ''
            i += 1
            code_lines = []
            while i < n and not _FENCE_RE.match(lines[i]):
                code_lines.append(lines[i])
                i += 1
            if i < n:
                i += 1
            blocks.append({'type': 'code_block', 'lang': lang,
                           'code': '\n'.join(code_lines)})
            continue

        if _HR_RE.match(raw):
            blocks.append({'type': 'hr'})
            i += 1
            continue

        bq_match = _BLOCKQUOTE_RE.match(raw)
        if bq_match:
            bq_lines = [bq_match.group(1)]
            i += 1
            while i < n:
                m = _BLOCKQUOTE_RE.match(lines[i])
                if m:
                    bq_lines.append(m.group(1))
                    i += 1
                elif not lines[i].strip():
                    break
                else:
                    bq_lines.append(lines[i].strip())
                    i += 1
            blocks.append({'type': 'blockquote', 'lines': bq_lines})
            continue

        md_heading = _HEADING_MD_RE.match(raw)
        if md_heading:
            blocks.append({
                'type': 'heading',
                'level': len(md_heading.group(1)),
                'text': md_heading.group(2).strip(),
            })
            i += 1
            continue

        if _is_metadata_line(stripped):
            cells = [c for c in _split_table_cells(stripped) if c.strip()]
            pairs = []
            for cell in cells:
                if '：' in cell:
                    idx = cell.index('：')
                    pairs.append((cell[:idx].strip(),
                                  cell[idx + 1:].strip()))
                elif ':' in cell:
                    idx = cell.index(':')
                    pairs.append((cell[:idx].strip(),
                                  cell[idx + 1:].strip()))
                else:
                    pairs.append(('', cell.strip()))
            blocks.append({'type': 'metadata', 'pairs': pairs})
            i += 1
            continue

        # style B：连续多行 'Key: Value'（Key 在已知关键词表内）→ 合并为元数据
        kv = _try_kv_line(stripped)
        if kv:
            kv_pairs = [kv]
            j = i + 1
            while j < n:
                nxt = lines[j]
                if not nxt.strip():
                    break
                nxt_kv = _try_kv_line(nxt)
                if not nxt_kv:
                    break
                kv_pairs.append(nxt_kv)
                j += 1
            if len(kv_pairs) >= 2:
                blocks.append({'type': 'metadata', 'pairs': kv_pairs})
                i = j
                continue
            # 单行 KV 不强制转 metadata，保留按段落处理

        # v7.6.1 style C / lenient fallback：连续 ≥3 行 form-only 的 Key:Value
        # （不要求 key 在白名单），LLM 常这样写 "站点名称/WordPress 版本/.../负责人"
        # 这种混白名单 + 自定义 key 的元数据。阈值 3 防止单条对话被误归并。
        kv_lenient = _try_kv_line_lenient(stripped)
        if kv_lenient:
            lenient_pairs = [kv_lenient]
            j = i + 1
            while j < n:
                nxt = lines[j]
                if not nxt.strip():
                    break
                nxt_kv = _try_kv_line_lenient(nxt)
                if not nxt_kv:
                    break
                lenient_pairs.append(nxt_kv)
                j += 1
            if len(lenient_pairs) >= 3:
                blocks.append({'type': 'metadata', 'pairs': lenient_pairs})
                i = j
                continue

        if _looks_like_table_row(stripped):
            rows = [_split_table_cells(stripped)]
            i += 1
            has_header = False
            if i < n and _is_table_separator(lines[i]):
                has_header = True
                i += 1
            while i < n and _looks_like_table_row(lines[i]):
                rows.append(_split_table_cells(lines[i]))
                i += 1
            blocks.append({'type': 'table', 'rows': rows,
                           'has_header': has_header})
            continue

        ul = _UL_ITEM_RE.match(raw)
        ol = _OL_ITEM_RE.match(raw)
        if ul or ol:
            ordered = bool(ol)
            items = []
            while i < n:
                m_ul = _UL_ITEM_RE.match(lines[i])
                m_ol = _OL_ITEM_RE.match(lines[i])
                if ordered and m_ol:
                    items.append(m_ol.group(2).strip())
                    i += 1
                elif not ordered and m_ul:
                    items.append(m_ul.group(1).strip())
                    i += 1
                elif not lines[i].strip():
                    break
                else:
                    break
            blocks.append({'type': 'list', 'ordered': ordered,
                           'items': items})
            continue

        # 普通段落：吃到下一空行或 block 标记；保留 CJK 软换行 + 硬换行
        clean, hb = _detect_hard_break(raw)
        para_items = [(clean.strip(), hb)]
        i += 1
        while i < n:
            nxt = lines[i]
            nxt_strip = nxt.strip()
            if not nxt_strip:
                break
            if (_HEADING_MD_RE.match(nxt) or _HR_RE.match(nxt)
                    or _FENCE_RE.match(nxt) or _BLOCKQUOTE_RE.match(nxt)
                    or _UL_ITEM_RE.match(nxt) or _OL_ITEM_RE.match(nxt)
                    or _is_metadata_line(nxt_strip)
                    or _looks_like_table_row(nxt_strip)):
                break
            clean, hb = _detect_hard_break(nxt)
            para_items.append((clean.strip(), hb))
            i += 1

        text = _smart_join_paragraph(para_items)
        if text:
            blocks.append({'type': 'paragraph', 'text': text})

    return blocks


# ============================================================
# 三、内联 token 拆分（**bold** / *italic* / `code`）
# ============================================================

_INLINE_RE = re.compile(
    r'(\*\*[^*\n]+?\*\*|'
    r'\*[^*\n]+?\*|'
    r'`[^`\n]+?`)'
)


def strip_unbalanced_emphasis(text):
    """v7.5.2 防御：剥掉孤立未闭合的 markdown 强调标记。

    LLM 时常生成 `**Key | value` 这种 markdown 表格行，cell 内 `**` 没有闭合；
    旧 tokenize_inline 不匹配 → 字面 `**` 落到输出。本函数在 tokenize 之前
    把孤立标记清掉，避免漏 `**` / `*` / `` ` `` 到字面。

    规则：每种标记 (`**`, `` ` ``) 出现次数为奇数时，全部替换为空字符串
    （视为格式错乱，按纯文本处理）。`*` 单星不处理（容易误伤合法文本）。
    """
    if not text:
        return text
    if text.count('**') % 2 == 1:
        text = text.replace('**', '')
    if text.count('`') % 2 == 1:
        text = text.replace('`', '')
    return text


def tokenize_inline(text):
    """把一段文本拆成 [(kind, text), ...]。

    kind ∈ {'plain', 'bold', 'italic', 'code'}
    供 Word / PDF 各自渲染。

    v7.5.2：内部先调 `strip_unbalanced_emphasis` 把孤立 `**` / `` ` `` 清掉，
    避免格式错乱时字面残留。
    """
    if not text:
        return []
    text = strip_unbalanced_emphasis(text)
    out = []
    parts = _INLINE_RE.split(text)
    for part in parts:
        if not part:
            continue
        if part.startswith('**') and part.endswith('**') and len(part) >= 4:
            out.append(('bold', part[2:-2]))
        elif part.startswith('*') and part.endswith('*') and len(part) >= 2:
            out.append(('italic', part[1:-1]))
        elif part.startswith('`') and part.endswith('`') and len(part) >= 2:
            out.append(('code', part[1:-1]))
        else:
            out.append(('plain', part))
    return out


def split_paragraph_lines(text):
    """段落 text 中的 '\n' 是硬换行；返回行列表。"""
    if not text:
        return ['']
    return text.split('\n')


# ============================================================
# 三-补、Pygments 代码高亮（VS Code Light 风格 token → RGB）
# ============================================================

# 同时供 Word（python-docx 的 RGBColor）和 PDF（reportlab 的 HexColor）用，
# 这里用 'RRGGBB' hex 字符串描述，渲染端各自转换。
PYGMENTS_TOKEN_COLORS = {
    # 关键字
    'Keyword': 'AF00DB',
    'Keyword.Constant': '0000FF',
    'Keyword.Declaration': '0000FF',
    'Keyword.Namespace': 'AF00DB',
    'Keyword.Pseudo': 'AF00DB',
    'Keyword.Reserved': 'AF00DB',
    'Keyword.Type': '267199',
    # 标识符
    'Name.Builtin': '267199',
    'Name.Builtin.Pseudo': '267199',
    'Name.Class': '267199',
    'Name.Decorator': '7957D5',
    'Name.Function': '7957D5',
    'Name.Function.Magic': '7957D5',
    'Name.Variable': '001080',
    'Name.Variable.Class': '001080',
    'Name.Variable.Instance': '001080',
    'Name.Tag': '800000',
    'Name.Attribute': 'FF0000',
    'Name.Constant': '0070C1',
    'Name.Exception': '267199',
    # 字面量
    'String': 'A31415',
    'String.Doc': '008000',
    'String.Heredoc': 'A31415',
    'String.Backtick': 'A31415',
    'String.Char': 'A31415',
    'String.Escape': 'EE0000',
    'String.Interpol': '0451A5',
    'String.Regex': 'EE0000',
    'Number': '09885A',
    'Number.Integer': '09885A',
    'Number.Float': '09885A',
    'Number.Hex': '09885A',
    # 注释
    'Comment': '008000',
    'Comment.Single': '008000',
    'Comment.Multiline': '008000',
    'Comment.Special': '008000',
    'Comment.Preproc': '0451A5',
    # 操作符 / 标点
    'Operator': '000000',
    'Operator.Word': 'AF00DB',
    'Punctuation': '000000',
    # 通用
    'Generic.Heading': '000080',
    'Generic.Subheading': '800080',
    'Generic.Inserted': '008000',
    'Generic.Deleted': 'FF0000',
}


def get_token_color(token_type_str):
    """token_type 形如 'Token.Keyword.Constant'，向上回落到第一个命中的颜色。"""
    if not token_type_str:
        return None
    s = token_type_str
    if s.startswith('Token.'):
        s = s[6:]
    while s:
        if s in PYGMENTS_TOKEN_COLORS:
            return PYGMENTS_TOKEN_COLORS[s]
        if '.' in s:
            s = s.rsplit('.', 1)[0]
        else:
            return None
    return None


# ============================================================
# 四、规范专属中文编号 → MD level 推断
# ============================================================

_LEVEL_KEY_TO_MD = {'chapter': 1, 'section': 2, 'article': 3}


def detect_heading_from_preset(text, preset):
    """返回 (md_level, cleaned_text) 或 None。"""
    for pattern, level_key in preset.heading_patterns:
        if re.match(pattern, text):
            md_level = _LEVEL_KEY_TO_MD.get(level_key, 2)
            if level_key == 'chapter':
                return md_level, text
            cleaned = re.sub(pattern, '', text).strip()
            return md_level, cleaned or text
    return None


# ============================================================
# 五、公司信息（委托给同目录 company-info.py）
# ============================================================

_CI_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        'company-info.py')
_ci_spec = importlib.util.spec_from_file_location('company_info', _CI_PATH)
_ci_module = importlib.util.module_from_spec(_ci_spec)
_ci_spec.loader.exec_module(_ci_module)


def resolve_company_info(overrides=None, use_odoo=True):
    info = _ci_module.resolve(use_odoo=use_odoo)
    if overrides:
        for key, value in overrides.items():
            if value:
                info[key] = value
    return info


def company_info_missing(info):
    missing = [k for k in _ci_module.REQUIRED_FIELDS if not info.get(k)]
    if info.get('logo_path') and not _ci_module.logo_is_valid(
            info.get('logo_path')):
        if 'logo_path' not in missing:
            missing.append('logo_path')
    return missing


def company_info_error_payload(missing):
    """构造给 Claude 看的结构化错误，便于触发补录流程。"""
    return json.dumps({
        'error': 'company_info_missing',
        'missing': missing,
        'hint': '请先填写 ~/.huo15/company-info.json 或用 '
                '--company-name / --logo-path 覆盖',
        'config_path': _ci_module.CONFIG_PATH,
    }, ensure_ascii=False)
