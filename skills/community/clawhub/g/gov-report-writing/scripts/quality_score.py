#!/usr/bin/env python3
"""
gov-report-writing（公文写作）内容质量评分脚本

基于 references/quality-scoring.md 定义的五维 100 分制评分标准，
对公文/报告的内容质量进行自动评分，输出分数、问题清单与改进建议。

检查层: 文本内容层（合规/完整/规范/准确/文风）
对应维度: E 有效性（与 format_check.py 的 DOCX 排版层检查互补）

用法:
    python quality_score.py <文件路径>
    python quality_score.py <文件路径> --type 年度工作总结   # 指定报告类型
    python quality_score.py <文件路径> --json                # JSON 输出
    python quality_score.py <文件路径> --quiet               # 仅输出问题项
    python quality_score.py <文件路径> --verbose             # 输出全部检查项（含通过项）
    python quality_score.py <文件路径> --draft               # 草稿模式（跳过占位符检查）

支持输入:
    .docx（自动提取正文文本，无需依赖 python-docx）/ .md / .txt

兼容性:
    - 平台: Windows / macOS / Linux
    - Python: 3.7+
    - 路径: 绝对/相对路径、~ 展开、含空格路径、中文路径、Windows 拖拽带引号

退出码:
    0 = A/B 档（≥80 分）  1 = C/D/E 档（<80 分）  2 = 参数或文件错误
"""
import sys
import os
import re
import io
import json
import platform
import zipfile
import argparse
import xml.etree.ElementTree as ET

# ============================================================
# 跨平台控制台编码兼容（与 format_check.py 保持一致）
# ============================================================
def _setup_console():
    for stream_name in ('stdout', 'stderr'):
        stream = getattr(sys, stream_name, None)
        if stream is None:
            continue
        try:
            reconfigure = getattr(stream, 'reconfigure', None)
            if reconfigure is not None:
                reconfigure(encoding='utf-8', errors='replace')
        except Exception:
            pass

_setup_console()

PLATFORM = platform.system()
PY_VERSION = platform.python_version()

W_NS = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
W = '{' + W_NS + '}'

# ============================================================
# 维度一：合规度（30 分）
# ============================================================

# 政治术语错误（错误模式, 正确表述, 说明）每项 -5，可扣至负分
# 注：均加否定前后缀，避免误伤正确表述中的子串（如"党的二十大精神"含"二十大精神"）
POLITICAL_TERMS = [
    # 注意："党的二十大精神"中"二十大精神"前紧邻的两个字符是"党的"，
    # 单用 (?<!党) 无法排除（其前一字符是"的"），必须用 (?<!党的)
    (r'(?<!党的)二十大精神', '应为"党的二十大精神"（缺"党"字）'),
    (r'高速增长', '应为"高质量发展"（旧表述已废弃）'),
    (r'(?<!全面推进)中国式现代化(?!全面推进)', '建议用完整表述"以中国式现代化全面推进中华民族伟大复兴"'),
    (r'监察委(?!员会)', '应为"国家监察委员会"'),
    (r'(?s)四个意识(?!.*四个自信)', '"四个意识"需与"四个自信""两个维护"完整连用'),
]

# 机构名称不规范 每项 -2
ORG_NAME_ISSUES = [
    (r'(?<!全国人民代)全国人大(?!常委会|代表|代表大会)', '首次出现应使用全称"全国人民代表大会"'),
    (r'(?<!中国人民政治协商会议)全国政协(?!全国委员会)', '首次出现应使用全称"中国人民政治协商会议全国委员会"'),
    (r'(?<!中共中央纪律检查)纪委(?!书记|委员会)', '首次出现应使用全称"中共中央纪律检查委员会"'),
]

# 禁用词（词, 建议替代）每项 -1
BANNED_WORDS = {
    '搞': '开展 / 推进',
    '弄': '办理 / 处理',
    '干': '推进 / 落实',
    '整': '整顿 / 处理',
    '很多': '较大幅度 / 显著',
    '有点': '一定 / 部分',
    '不够': '有待加强 / 尚需提升',
    '没做好': '存在不足 / 尚有差距',
    '完全': '基本 / 较为',
    '绝对': '一定 / 较',
    '100%': '全面 / 全部',
    '史无前例': '（删除，用事实说话）',
    '前所未有': '（删除）',
    '极大': '显著 / 明显',
    '非常': '（删除程度助词）',
    '特别': '（删除程度助词）',
    '极其': '（删除程度助词）',
    '大概': '（删除或替换为数据）',
    '可能': '（删除）',
    '好像': '（删除）',
    '差不多': '（删除或替换为数据）',
    '简直': '（删除）',
    '超级': '（删除）',
}

# 禁用词的「合法组合白名单」：这些词在公文中属正常用法，检测时先剔除再统计
# 例："干部""骨干"含"干"字，但均为规范表述，不应扣分
BANNED_SAFE_COMBOS = {
    '干': ['干部', '骨干', '实干', '干事', '能干', '精干', '干警', '干线'],
    '整': ['整体', '整合', '整顿', '调整', '完整', '整治', '整数', '整套'],
    '弄': ['弄清', '弄懂'],
    '做': ['做法', '做出', '做到'],
    '非常': ['非常规', '非经常性'],
    '可能': ['可能性'],
}

# 占位符 每处 -0.5
PLACEHOLDER_PATTERN = re.compile(r'X{2,}(?:\s*[、，。]|\s*%|\s*万元|\s*人|\s*个|\s*年)?')

# 涉密信号：严重警告 + 总分扣 50 分（不采用一票否决，避免单位名误伤）
SECRET_SIGNALS = [
    (r'(绝密|机密|秘密)(?!\s*级\s*别)', '密级标注'),
    (r'密级\s*[:：]', '密级字段'),
    (r'〔?\d{4}?〕?\s*第?\s*\d+\s*号\s*密', '含密字文件编号'),
    (r'(武器|装备|弹药|导弹|战斗机|舰艇)\s*(型号|编号|代号)', '武器型号'),
    (r'(项目代号|工程代号)\s*[:：]', '项目/工程代号'),
]

# ============================================================
# 维度二：完整度（25 分）
# ============================================================

# 必备要素（名称, 正则）6 项 × 2 分
# 注：「正文」用字符总数判定（正则 None），避免因换行/标点导致误报
REQUIRED_ELEMENTS = [
    ('标题', re.compile(r'^.{2,60}$', re.M)),
    ('主送机关', re.compile(r'[\u4e00-\u9fa5]{2,20}(部|局|处|科|室|委|办|集团|公司|单位)\s*[:：]')),
    ('正文', None),
    ('发文机关署名', re.compile(r'[\u4e00-\u9fa5]{2,20}(部|局|处|委|办|集团|公司|院|所|中心)\s*$', re.M)),
    ('成文日期', re.compile(r'(19|20)\d{2}\s*年\s*\d{1,2}\s*月\s*\d{1,2}\s*日')),
    ('印章', re.compile(r'[（(]\s*印章\s*[）)]|印章位置|（盖章）')),
]

# 正文字数下限（中文字符数）
MIN_BODY_CHARS = 100

# 不强制要求「主送机关」的文种
# 内部总结、发言类材料通常无主送对象，强行要求会造成误报
NO_RECIPIENT_TYPES = {
    '年度工作总结', '述职报告', '调研报告', '会议纪要',
    '心得体会', '党课讲稿', '整改方案',
}

# 类型专属章节（同义词列表，任一命中即算该章存在）
REPORT_TYPE_CHAPTERS = {
    '年度工作总结': [
        ['主要工作', '工作成效', '主要成效', '工作开展情况', '工作完成情况'],
        ['工作亮点', '亮点工作', '重点工作亮点', '特色亮点'],
        ['存在问题', '问题与不足', '不足之处', '薄弱环节'],
        ['下一步', '下步工作', '工作计划', '下步打算', '下一步打算'],
    ],
    '述职报告': [
        ['履职情况', '履职尽责', '工作职责', '履职'],
        ['工作亮点', '创新', '亮点'],
        ['问题与不足', '存在不足', '不足之处', '问题'],
        ['改进措施', '努力方向', '整改措施', '下一步'],
    ],
    '党建报告': [
        ['工作开展情况', '主要工作', '党建工作开展', '主要成效'],
        ['存在问题', '问题与不足', '不足'],
        ['下一步', '下步工作', '工作思路', '下步打算'],
    ],
    '调研报告': [
        ['调研背景', '背景与目的', '调研目的', '背景'],
        ['现状分析', '现状', '基本情况', '主要特点'],
        ['存在问题', '问题及原因', '原因分析', '问题'],
        ['对策建议', '意见建议', '建议'],
        ['结论', '展望'],
    ],
    '工作方案': [
        ['总体要求', '指导思想', '基本原则'],
        ['主要任务', '工作任务', '重点任务'],
        ['实施步骤', '工作安排', '推进步骤', '阶段'],
        ['责任分工', '职责分工', '责任部门'],
        ['保障措施', '组织保障', '保障机制'],
    ],
    '整改方案': [
        ['整改目标', '目标'],
        ['整改任务', '任务及分工', '整改措施', '整改清单'],
        ['整改步骤', '工作步骤', '阶段'],
        ['保障措施', '组织保障', '长效机制'],
    ],
    '会议纪要': [
        ['会议议题', '议题'],
        ['会议内容', '讨论', '会议议程'],
        ['决议事项', '决议', '议定事项'],
        ['待办事项', '任务分工', '落实事项'],
    ],
    '通知': [
        ['事由', '根据', '为'],
        ['具体内容', '事项', '安排'],
        ['要求', '请', '特此通知'],
    ],
    '请示': [
        ['缘由', '根据', '由于', '为'],
        ['事项', '请示事项', '拟'],
        ['结语', '妥否', '请批示', '请审批', '请批准'],
    ],
    '汇报材料': [
        ['基本情况', '概况', '基本情况介绍'],
        ['主要做法', '主要工作', '工作成效', '主要成效'],
        ['存在问题', '问题', '不足'],
        ['下步打算', '下一步', '下步工作', '工作思路'],
    ],
}

# 报告类型识别关键词（类型, 关键词列表）
TYPE_KEYWORDS = [
    ('述职报告', ['述职', '履职', '述廉']),
    ('党建报告', ['党建', '党委', '支部', '思想政治', '党纪']),
    ('调研报告', ['调研', '课题', '研究报告', '调研分析']),
    ('工作方案', ['方案', '实施方案', '工作计划', '工作安排']),
    ('会议纪要', ['纪要', '会议记录', '会议备忘']),
    ('通知', ['通知', '公告', '通报']),
    ('请示', ['请示', '请批', '报请']),
    ('整改方案', ['整改', '整改方案', '整改措施']),
    ('汇报材料', ['汇报', '上报', '呈报']),
    ('年度工作总结', ['总结', '年度总结', '全年总结', '工作总结', '回顾']),
]

# 信息密度 5 项（名称, 正则, 缺失说明）
INFO_DENSITY = [
    ('数据支撑', re.compile(r'\d+(\.\d+)?\s*%|\d+(\.\d+)?\s*(万元|亿元|元|人|人次|个|项|台|套)|同比|环比|增长\s*\d|完成率|达标率|覆盖率|占比'),
     '建议补充百分比、绝对数或同比数据'),
    ('具体事例', re.compile(r'《[^》]{2,30}》|“[^”]{4,40}”|"[^"]{4,40}"|项目|专项|工程|活动|试点|案例|典型'),
     '建议补充具体项目、事例或案例'),
    ('责任分工', re.compile(r'牵头|负责|责任人|责任部门|责任单位|分工|主责|配合部门|[\u4e00-\u9fa5]{2,10}(部|局|处|科|室|委|办)\s*(牵头|负责|落实)'),
     '建议明确牵头部门或责任人'),
    ('时间节点', re.compile(r'\d{1,2}\s*月\s*\d{1,2}\s*日前|\d{1,2}\s*月底前|\d{1,2}\s*月之前|季度|半年|年底前|年内|20\d{2}\s*年\s*(底|末|前)|第一阶段|第二阶段|第三阶段'),
     '建议补充完成时限或阶段节点'),
    ('量化成效', re.compile(r'完成率|达标率|合格率|覆盖率|增长率|节约|降低成本|提升\s*\d|\d+\s*%'),
     '建议用量化的结果描述成效'),
]

# ============================================================
# 维度三：规范度（20 分）
# ============================================================

CONVENTION_CHECKS = [
    # 层级序号（5 分）
    ('层级序号', 5, 2, re.compile(r'[一二三四五六七八九十]+\.\s'), '一级标题序号误用点号，应为顿号（一、）'),
    ('层级序号', 5, 2, re.compile(r'（[一二三四五六七八九十]+）、'), '二级标题序号带顿号，应为（一）'),
    ('层级序号', 5, 1, re.compile(r'1、'), '三级标题序号应用下脚点，应为 1.'),
    # 数字用法（4 分）
    ('数字用法', 4, 2, re.compile(r'(?<!\d)[1-9]\d年'), '年份未用全称，如"25年"应为"2025年"'),
    ('数字用法', 4, 1, re.compile(r'(19|20)\d{2}[-/]\d{1,2}[-/]\d{1,2}'), '日期格式应为"2025年7月24日"'),
    ('数字用法', 4, 1, re.compile(r'0\d+\s*(号|名|个|项)'), '序号不编虚位，如"01号"应为"1号"'),
    # 标点符号（4 分）
    ('标点符号', 4, 2, re.compile(r'\[\s*(19|20)\d{2}\s*\]'), '年份括号应为六角括号〔〕，非方括号[]'),
    ('标点符号', 4, 1, re.compile(r'附件\s*[:：]?\s*[^\n。]{2,30}。'), '附件名称后不加句号'),
    # 引用规范（4 分）
    ('引用规范', 4, 2, re.compile(r'根据《[^》]{4,40}》(?!\s*[（(]\s*[^\n）)]{0,30}〔?\d{4}〕?)'), '引用公文应先引标题，后引发文字号'),
    ('引用规范', 4, 2, re.compile(r'根据《[^》]{0,60}法》'), '引用法律法规应使用全称'),
    # 公文规范（3 分）
    ('公文规范', 3, 2, re.compile(r'(报告|汇报)[^\n]{0,40}(请批示|请审批|请批准)'), '报告不得夹带请示事项'),
    ('公文规范', 3, 1, re.compile(r'请示[^\n]{0,200}(?:同时|另外|此外)[^\n]{0,60}(?:请|拟)'), '请示应一事一请'),
]

# ============================================================
# 维度四：准确度（15 分）
# ============================================================

# 单位统一（同类数据单位混用）
# 注：仅保留「万元/亿元」这一项。
# 「% 与 百分点」「人 与 人次」在公文中属正常搭配（占比用 %、增幅用百分点；
# 招聘人数用"人"、培训覆盖用"人次"），检测会大量误报，已从扣分规则中移除，
# 如需人工复核可由 --verbose 的通过项明细中查看。
UNIT_CONFLICTS = [
    (re.compile(r'(\d+(?:\.\d+)?)\s*万元'), re.compile(r'(\d+(?:\.\d+)?)\s*亿元'), '金额单位混用（万元/亿元）'),
]

# 时间表述（年份写法不统一）
YEAR_INCONSISTENT = re.compile(r'(?<!\d)(19|20)\d{2}\s*年')

# ============================================================
# 维度五：文风度（10 分）
# ============================================================

AI_TRACE_PATTERNS = [
    (re.compile(r'——'), 1, '破折号滥用，公文一般用逗号或冒号'),
    (re.compile(r'首先[，,].{0,80}其次[，,].{0,80}(最后|再次)[，,]'), 1, '"首先/其次/最后"机械三段式'),
    (re.compile(r'一是[^。；]{0,80}[。；]\s*二是[^。；]{0,80}[。；]\s*三是'),
     1, '"一是/二是/三是"机械三段式，建议改为小标题分述'),
    (re.compile(r'值得注意的是|需要指出的是|值得一提的是'), 0.5, 'AI 高频套语，建议删除'),
    (re.compile(r'总(而言|而|的来)之|综上所述'), 0.5, '空洞总结句，若无实质内容建议删除'),
    (re.compile(r'[\U0001F300-\U0001FAFF\u2600-\u27BF]'), 1, '正文中混入 emoji'),
]

SECRET_DEDUCTION = 50  # 涉密信号扣分（非一票否决）


# ============================================================
# 工具函数
# ============================================================
def resolve_path(raw_path):
    """路径规范化：去引号、展开 ~、转绝对路径（支持中文路径）"""
    if not raw_path:
        return None
    p = raw_path.strip()
    if len(p) >= 2 and p[0] in ('"', "'") and p[-1] == p[0]:
        p = p[1:-1]
    p = os.path.expanduser(p)
    return os.path.abspath(p)


def extract_text(path):
    """提取文本：支持 .docx / .md / .txt，返回 (文本, 错误信息)"""
    ext = os.path.splitext(path)[1].lower()

    if ext == '.docx':
        try:
            with zipfile.ZipFile(path) as z:
                try:
                    raw_xml = z.read('word/document.xml')
                except KeyError:
                    return None, '无效 DOCX：缺少 word/document.xml'
                doc_xml = raw_xml.decode('utf-8-sig', errors='replace')
            root = ET.fromstring(doc_xml)
            # 按段落提取，保留换行结构
            paragraphs = []
            for p in root.findall('.//' + W + 'p'):
                texts = [t.text or '' for t in p.findall('.//' + W + 't')]
                line = ''.join(texts).strip()
                if line:
                    paragraphs.append(line)
            return '\n'.join(paragraphs), None
        except zipfile.BadZipFile:
            return None, '无法打开文件（不是有效的 zip/DOCX）'
        except ET.ParseError:
            return None, 'XML 解析失败（文档可能损坏）'
        except Exception as e:
            return None, f'读取 DOCX 失败: {e}'
    else:
        for enc in ('utf-8-sig', 'utf-8', 'gbk'):
            try:
                with io.open(path, 'r', encoding=enc) as f:
                    return f.read(), None
            except UnicodeDecodeError:
                continue
            except Exception as e:
                return None, f'读取文件失败: {e}'
        return None, '无法解码文件（尝试过 UTF-8 / GBK）'


def detect_report_type(text):
    """
    自动识别报告类型，返回 (类型, 置信度)

    识别策略（两级）：
    1. 标题优先：在文档前 2 行内匹配类型词，命中即返回 high 置信度
       （避免正文中的 incidental 词干扰，如年度总结里出现"薪酬套改方案"
         导致误判为"工作方案"）
    2. 全文统计：标题未命中时，统计各类型关键词出现次数，取最高者
    """
    # 第一级：标题优先
    head = '\n'.join(text.strip().split('\n')[:2])
    head_hits = []
    for rtype, keywords in TYPE_KEYWORDS:
        for kw in keywords:
            if kw in head:
                head_hits.append((rtype, len(kw)))
                break
    if head_hits:
        # 标题命中多个时，取匹配词最长的（更具体）
        head_hits.sort(key=lambda x: -x[1])
        return head_hits[0][0], 'high'

    # 第二级：全文统计
    scores = {}
    for rtype, keywords in TYPE_KEYWORDS:
        hit = sum(1 for kw in keywords if kw in text)
        if hit:
            scores[rtype] = hit
    if not scores:
        return None, 'none'
    best = max(scores, key=scores.get)
    best_score = scores[best]
    if best_score >= 3:
        confidence = 'high'
    elif best_score == 2:
        confidence = 'medium'
    else:
        confidence = 'low'
    return best, confidence


def get_line_no(text, match_start):
    """根据字符偏移量计算行号（1-based）"""
    return text.count('\n', 0, match_start) + 1


# ============================================================
# 五维检查
# ============================================================
def check_compliance(text, draft=False):
    """维度一：合规度（30 分）"""
    issues = []
    passed = []
    score = 30.0
    secret_hits = []

    # 涉密信号（单独收集，不计入本维度，改为总分扣 50）
    for pattern, label in SECRET_SIGNALS:
        m = re.search(pattern, text)
        if m:
            secret_hits.append({
                'signal': label,
                'found': m.group(0)[:30],
                'line': get_line_no(text, m.start()),
            })

    # 政治术语（每项 -5，可扣至负分）
    for pattern, suggestion in POLITICAL_TERMS:
        m = re.search(pattern, text)
        if m:
            score -= 5
            issues.append({
                'priority': 'P0', 'dimension': '合规度',
                'location': f'第 {get_line_no(text, m.start())} 段',
                'found': m.group(0), 'suggestion': suggestion, 'deduction': 5,
            })

    # 机构名称（每项 -2）
    for pattern, suggestion in ORG_NAME_ISSUES:
        m = re.search(pattern, text)
        if m:
            score -= 2
            issues.append({
                'priority': 'P1', 'dimension': '合规度',
                'location': f'第 {get_line_no(text, m.start())} 段',
                'found': m.group(0), 'suggestion': suggestion, 'deduction': 2,
            })

    # 禁用词（每项 -1）
    # 先剔除「合法组合白名单」中的出现，避免误伤"干部""整体"等规范表述
    for word, suggestion in BANNED_WORDS.items():
        safes = BANNED_SAFE_COMBOS.get(word, [])
        safe_spans = []
        for safe in safes:
            idx = text.find(safe)
            while idx != -1:
                safe_spans.append((idx, idx + len(safe)))
                idx = text.find(safe, idx + 1)
        hits = []
        for m in re.finditer(re.escape(word), text):
            start, end = m.start(), m.end()
            if any(s <= start and end <= e for s, e in safe_spans):
                continue  # 落在合法组合内，跳过
            hits.append(get_line_no(text, start))
        if hits:
            count = len(hits)
            score -= count
            issues.append({
                'priority': 'P2', 'dimension': '合规度',
                'location': f'第 {hits[0]} 段' + (f' 等 {count} 处' if count > 1 else ''),
                'found': f'{word}（{count} 处）', 'suggestion': f'建议改为：{suggestion}',
                'deduction': count,
            })

    # 占位符（每处 -0.5，草稿模式跳过）
    if not draft:
        placeholders = PLACEHOLDER_PATTERN.findall(text)
        if placeholders:
            deduction = min(len(placeholders) * 0.5, 2)
            score -= deduction
            issues.append({
                'priority': 'P3', 'dimension': '合规度',
                'location': '全文',
                'found': f'未替换占位符 {len(placeholders)} 处（如 {placeholders[0].strip()}）',
                'suggestion': '替换为实际信息；草稿可用 --draft 跳过',
                'deduction': deduction,
            })
    else:
        passed.append('占位符检查: 已跳过（草稿模式）')

    score = max(score, -10)  # 允许负分但设下限，便于展示严重程度
    if not issues:
        passed.append('未发现合规问题')
    return score, 30, issues, passed, secret_hits


def check_completeness(text, report_type):
    """维度二：完整度（25 分）"""
    issues = []
    passed = []
    score = 0.0

    # 4.1 必备要素（6 项 × 2 = 12 分）
    for name, pattern in REQUIRED_ELEMENTS:
        if name == '正文':
            # 正文按中文字符总数判定，避免换行/标点导致的误报
            cn_count = len(re.findall(r'[\u4e00-\u9fa5]', text))
            if cn_count >= MIN_BODY_CHARS:
                score += 2
                passed.append(f'必备要素 正文: ✓（{cn_count} 字）')
            else:
                issues.append({
                    'priority': 'P2', 'dimension': '完整度',
                    'location': '全文', 'found': f'正文过短（{cn_count} 字，建议 ≥{MIN_BODY_CHARS} 字）',
                    'suggestion': '补充正文内容', 'deduction': 2,
                })
            continue
        if name == '主送机关' and report_type in NO_RECIPIENT_TYPES:
            # 该文种通常无主送对象，豁免此项
            score += 2
            passed.append(f'必备要素 主送机关: ✓（{report_type} 豁免）')
            continue
        if pattern.search(text):
            score += 2
            passed.append(f'必备要素 {name}: ✓')
        else:
            issues.append({
                'priority': 'P2', 'dimension': '完整度',
                'location': '全文', 'found': f'缺少{name}',
                'suggestion': f'补充{name}要素', 'deduction': 2,
            })

    # 4.2 类型专属章节（8 分）
    chapters = REPORT_TYPE_CHAPTERS.get(report_type) if report_type else None
    if chapters:
        per_chapter = 8.0 / len(chapters)
        for synonyms in chapters:
            if any(syn in text for syn in synonyms):
                score += per_chapter
                passed.append(f'章节「{synonyms[0]}」: ✓')
            else:
                issues.append({
                    'priority': 'P2', 'dimension': '完整度',
                    'location': '全文', 'found': f'缺少章节：{synonyms[0]}',
                    'suggestion': f'补充「{synonyms[0]}」章节（可写作 {" / ".join(synonyms[1:3])} 等）',
                    'deduction': round(per_chapter, 1),
                })
    else:
        # 未识别类型：给满分但提示
        score += 8
        passed.append('章节校验: 未识别报告类型，已跳过（可用 --type 指定）')
        issues.append({
            'priority': 'P3', 'dimension': '完整度',
            'location': '全文', 'found': '未识别报告类型，章节校验跳过',
            'suggestion': '用 --type <类型> 指定后可校验章节完整性', 'deduction': 0,
        })

    # 4.3 信息密度（5 项 × 1 = 5 分）
    for name, pattern, suggestion in INFO_DENSITY:
        if pattern.search(text):
            score += 1
            passed.append(f'信息密度 {name}: ✓')
        else:
            issues.append({
                'priority': 'P1', 'dimension': '完整度',
                'location': '全文', 'found': f'缺少{name}',
                'suggestion': suggestion, 'deduction': 1,
            })

    return min(score, 25), 25, issues, passed


def check_convention(text):
    """维度三：规范度（20 分）"""
    issues = []
    passed = []
    deductions = {}

    for cat, max_score, deduction, pattern, suggestion in CONVENTION_CHECKS:
        m = re.search(pattern, text)
        if m:
            deductions[cat] = deductions.get(cat, 0) + deduction
            issues.append({
                'priority': 'P2', 'dimension': '规范度',
                'location': f'第 {get_line_no(text, m.start())} 段',
                'found': m.group(0)[:30], 'suggestion': suggestion,
                'deduction': deduction,
            })

    # 按类别上限封顶扣分（类别分值在 CONVENTION_CHECKS 中取该类别的 max_score）
    cat_max = {}
    for cat, max_score, _, _, _ in CONVENTION_CHECKS:
        cat_max[cat] = max_score
    total_deduction = sum(min(deductions.get(cat, 0), cat_max[cat]) for cat in cat_max)

    score = 20 - total_deduction
    if not issues:
        passed.append('未发现规范问题')
    return max(score, 0), 20, issues, passed


def check_accuracy(text):
    """维度四：准确度（15 分）"""
    issues = []
    passed = []
    score = 15.0

    # 6.1 数据前后一致性（规则化近似：同名指标多处出现且数值不同）
    metric_pattern = re.compile(r'([\u4e00-\u9fa5]{2,8})(?:为|达|约|共计|总计|合计)?\s*(\d+(?:\.\d+)?)\s*(%|万元|亿元|元|人|人次|个|项|台|套)')
    metrics = {}
    for m in metric_pattern.finditer(text):
        name, value, unit = m.group(1), m.group(2), m.group(3)
        key = (name, unit)
        if key not in metrics:
            metrics[key] = []
        metrics[key].append((value, get_line_no(text, m.start())))
    inconsistent = 0
    for (name, unit), occurrences in metrics.items():
        values = {v for v, _ in occurrences}
        if len(values) > 1 and len(occurrences) >= 2:
            inconsistent += 1
            lines = [str(ln) for _, ln in occurrences[:3]]
            issues.append({
                'priority': 'P1', 'dimension': '准确度',
                'location': f'第 {"、".join(lines)} 段',
                'found': f'{name} 出现 {len(occurrences)} 次数值不一致：{"/".join(sorted(values))} {unit}',
                'suggestion': '核对并统一为该指标的准确数值', 'deduction': 3,
            })
    score -= min(inconsistent * 3, 5)
    if inconsistent == 0:
        passed.append('数据前后一致: ✓')

    # 6.3 单位统一
    unit_conflict = 0
    for p1, p2, label in UNIT_CONFLICTS:
        if p1.search(text) and p2.search(text):
            unit_conflict += 1
            issues.append({
                'priority': 'P2', 'dimension': '准确度',
                'location': '全文', 'found': label,
                'suggestion': '统一金额/比例/人数单位', 'deduction': 1,
            })
    score -= min(unit_conflict, 3)
    if unit_conflict == 0:
        passed.append('单位统一: ✓')

    # 6.4 时间表述
    short_year = re.search(r'(?<!\d)[1-9]\d\s*年', text)
    full_year = YEAR_INCONSISTENT.search(text)
    if short_year and full_year:
        score -= 1
        issues.append({
            'priority': 'P2', 'dimension': '准确度',
            'location': f'第 {get_line_no(text, short_year.start())} 段',
            'found': f'年份写法不统一：{short_year.group(0)} 与 {full_year.group(0)}',
            'suggestion': '年份统一用全称（2025年 非 25年）', 'deduction': 1,
        })
    else:
        passed.append('时间表述一致: ✓')

    if not issues:
        passed.append('未发现准确性问题')
    return max(score, 0), 15, issues, passed


def check_style(text):
    """维度五：文风度（10 分）"""
    issues = []
    passed = []
    score = 10.0

    # 7.1 AI 痕迹
    for pattern, deduction, suggestion in AI_TRACE_PATTERNS:
        m = re.search(pattern, text)
        if m:
            score -= deduction
            issues.append({
                'priority': 'P3', 'dimension': '文风度',
                'location': f'第 {get_line_no(text, m.start())} 段',
                'found': m.group(0)[:30], 'suggestion': suggestion,
                'deduction': deduction,
            })

    # 7.2 小标题对仗（同级一级标题字数差异）
    headings = re.findall(r'^\s*([一二三四五六七八九十]+、[^\n]{2,30})$', text, re.M)
    if len(headings) >= 3:
        lengths = [len(h) for h in headings]
        if max(lengths) - min(lengths) > 4:
            score -= 1
            issues.append({
                'priority': 'P3', 'dimension': '文风度',
                'location': '各级标题', 'found': f'一级标题字数差异 {max(lengths) - min(lengths)} 字',
                'suggestion': '同级标题建议统一为四字或六字动宾短语', 'deduction': 1,
            })
        else:
            passed.append('小标题对仗: ✓')
    else:
        passed.append('小标题对仗: 标题数量不足，跳过')

    # 7.3 句式节奏（长句占比）
    sentences = [s for s in re.split(r'[。！？；]', text) if len(s.strip()) > 0]
    if sentences:
        long_sentences = [s for s in sentences if len(s) > 80]
        ratio = len(long_sentences) / len(sentences)
        if ratio > 0.3:
            score -= 1
            issues.append({
                'priority': 'P3', 'dimension': '文风度',
                'location': '全文', 'found': f'长句占比 {ratio:.0%}（{len(long_sentences)}/{len(sentences)}）',
                'suggestion': '适当拆分长句，长短句搭配', 'deduction': 1,
            })
        else:
            passed.append('句式节奏: ✓')

    if not issues:
        passed.append('未发现文风问题')
    return max(score, 0), 10, issues, passed


# ============================================================
# 报告渲染
# ============================================================
def grade_of(total, secret_hits):
    if total >= 90:
        return 'A', '优秀', '可直接提交', '🟢'
    if total >= 80:
        return 'B', '良好', '小修后可提交', '🔵'
    if total >= 70:
        return 'C', '合格', '需修改后复审', '🟡'
    if total >= 60:
        return 'D', '待改进', '较大修改，建议重写部分章节', '🟠'
    return 'E', '不合格', '建议按模板重新生成', '🔴'


def bar(score, max_score, width=12):
    filled = int(round(score / max_score * width)) if max_score else 0
    filled = max(0, min(filled, width))
    return '█' * filled + '░' * (width - filled)


def render_report(path, result, verbose=False):
    """文本报告输出"""
    print(f"\n{'=' * 62}")
    print(f"  公文质量评分报告: {os.path.basename(path)}")
    print(f"{'=' * 62}")

    rtype = result['report_type'] or '未识别'
    conf = {'high': '高', 'medium': '中', 'low': '低', 'none': '无'}.get(result['type_confidence'], '-')
    print(f"  报告类型: {rtype}（自动识别，置信度 {conf}）")

    if result['secret_hits']:
        print(f"\n{'!' * 62}")
        print("  ⛔⚠️  严重警告：检测到疑似涉密信号，已扣 50 分")
        for s in result['secret_hits']:
            print(f"      · {s['signal']}（第 {s['line']} 段）：{s['found']}")
        print("     请确认文档是否已脱敏。如确认可公开，可忽略本提示。")
        print(f"{'!' * 62}")

    print(f"\n## 五维评分")
    for dim in result['dimensions']:
        d = result['dimensions'][dim]
        mark = '✅' if d['issues'] == 0 else '⚠️'
        print(f"  {d['label']:<6} {bar(d['score'], d['max'])}  {d['score']:>5.1f}/{d['max']:<3} {mark} {d['issue_summary']}")

    g = result['grade']
    print(f"\n## 总分  {result['total_score']}/100    评级  {g['icon']} {g['grade']}（{g['label']}）")
    print(f"  判定: {g['verdict']}")
    if result['secret_deduction'] > 0:
        print(f"  （含涉密扣分 -{result['secret_deduction']} 分）")

    # 问题清单
    blocking = [i for i in result['issues'] if i['priority'] == 'P0']
    others = [i for i in result['issues'] if i['priority'] != 'P0']
    others.sort(key=lambda x: x['priority'])

    if blocking:
        print(f"\n{'-' * 62}")
        print("## ⛔ 红线问题（必须修复，无论总分多少）")
        for i in blocking:
            print(f"  [{i['dimension']}] {i['location']}: {i['found']}")
            print(f"      → {i['suggestion']}")

    if others:
        print(f"\n{'-' * 62}")
        print(f"## 问题清单（{len(others)} 项，按优先级排序）")
        for i in others:
            print(f"  {i['priority']}  {i['location']:<10} [{i['dimension']}] {i['found']}")
            print(f"      → {i['suggestion']}  （-{i['deduction']}）")
    elif not blocking:
        print(f"\n{'-' * 62}")
        print("## 🎉 未发现内容质量问题！")

    # 改进建议
    if result['suggestions']:
        print(f"\n{'-' * 62}")
        print("## 改进建议（按提分效率排序）")
        for idx, s in enumerate(result['suggestions'], 1):
            print(f"  {idx}. {s['action']}（{s['count']} 处，预计 +{s['expected_gain']:.1f} 分）")
        print(f"  → 全部修复后预计可达 {result['potential_score']:.0f} 分")

    if verbose:
        print(f"\n{'-' * 62}")
        print("## 通过项明细")
        for p in result['passed']:
            print(f"  ✅ {p}")

    print(f"\n{'=' * 62}\n")


def main(argv=None):
    parser = argparse.ArgumentParser(
        description='gov-report-writing（公文写作）内容质量评分（五维 100 分制）',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='示例: python quality_score.py 年度总结.docx\n'
               '      python quality_score.py 年度总结.docx --type 年度工作总结\n'
               '      python quality_score.py 年度总结.docx --json')
    parser.add_argument('file', nargs='?', help='待评分的文件路径（.docx / .md / .txt）')
    parser.add_argument('--type', dest='report_type',
                        help=f'指定报告类型，可选: {", ".join(REPORT_TYPE_CHAPTERS.keys())}')
    parser.add_argument('--json', action='store_true', dest='json_out', help='以 JSON 格式输出')
    parser.add_argument('--quiet', action='store_true', help='仅输出问题项（文本模式）')
    parser.add_argument('--verbose', action='store_true', help='输出全部检查项（含通过项）')
    parser.add_argument('--draft', action='store_true', help='草稿模式：跳过占位符检查')
    parser.add_argument('--version', action='version',
                        version=f'quality_score.py | Python {PY_VERSION} | {PLATFORM}')
    args = parser.parse_args(argv)

    if not args.file:
        parser.print_help()
        return 2

    path = resolve_path(args.file)
    if not path or not os.path.exists(path):
        print(f'❌ 文件不存在: {args.file}')
        return 2
    if not os.path.isfile(path):
        print(f'❌ 不是有效文件: {args.file}')
        return 2

    text, err = extract_text(path)
    if err:
        print(f'❌ {err}')
        return 2
    if not text or len(text.strip()) < 20:
        print('❌ 文档内容过少，无法评分（至少需要 20 字）')
        return 2

    # 报告类型
    if args.report_type:
        rtype = args.report_type if args.report_type in REPORT_TYPE_CHAPTERS else None
        confidence = 'manual' if rtype else 'none'
        if not rtype:
            print(f'⚠️ 未识别的报告类型: {args.report_type}，将跳过章节校验')
            print(f'   可选类型: {", ".join(REPORT_TYPE_CHAPTERS.keys())}')
    else:
        rtype, confidence = detect_report_type(text)

    # 五维评分
    comp_score, comp_max, comp_issues, comp_passed, secret_hits = check_compliance(text, args.draft)
    cmpl_score, cmpl_max, cmpl_issues, cmpl_passed = check_completeness(text, rtype)
    conv_score, conv_max, conv_issues, conv_passed = check_convention(text)
    acc_score, acc_max, acc_issues, acc_passed = check_accuracy(text)
    style_score, style_max, style_issues, style_passed = check_style(text)

    subtotal = comp_score + cmpl_score + conv_score + acc_score + style_score
    secret_deduction = SECRET_DEDUCTION if secret_hits else 0
    total = max(0, round(subtotal - secret_deduction, 1))

    dimensions = {
        'compliance': {'label': '合规度', 'score': round(comp_score, 1), 'max': comp_max,
                       'issues': len([i for i in comp_issues if i['deduction'] > 0]),
                       'issue_summary': f"合规问题 {len([i for i in comp_issues if i['deduction'] > 0])} 项"},
        'completeness': {'label': '完整度', 'score': round(cmpl_score, 1), 'max': cmpl_max,
                         'issues': len([i for i in cmpl_issues if i['deduction'] > 0]),
                         'issue_summary': f"缺失要素/信息 {len([i for i in cmpl_issues if i['deduction'] > 0])} 项"},
        'convention': {'label': '规范度', 'score': round(conv_score, 1), 'max': conv_max,
                       'issues': len([i for i in conv_issues if i['deduction'] > 0]),
                       'issue_summary': f"规范问题 {len([i for i in conv_issues if i['deduction'] > 0])} 项"},
        'accuracy': {'label': '准确度', 'score': round(acc_score, 1), 'max': acc_max,
                     'issues': len([i for i in acc_issues if i['deduction'] > 0]),
                     'issue_summary': f"数据问题 {len([i for i in acc_issues if i['deduction'] > 0])} 项"},
        'style': {'label': '文风度', 'score': round(style_score, 1), 'max': style_max,
                  'issues': len([i for i in style_issues if i['deduction'] > 0]),
                  'issue_summary': f"文风问题 {len([i for i in style_issues if i['deduction'] > 0])} 项"},
    }

    all_issues = comp_issues + cmpl_issues + conv_issues + acc_issues + style_issues
    all_passed = comp_passed + cmpl_passed + conv_passed + acc_passed + style_passed

    # 改进建议（按可挽回分数排序，取前 5）
    gain_map = {}
    for i in all_issues:
        if i['deduction'] <= 0:
            continue
        key = f"[{i['dimension']}] {i['suggestion']}"
        if key not in gain_map:
            gain_map[key] = {'action': key, 'count': 0, 'expected_gain': 0.0}
        gain_map[key]['count'] += 1
        gain_map[key]['expected_gain'] += i['deduction']
    suggestions = sorted(gain_map.values(), key=lambda x: -x['expected_gain'])[:5]
    potential = min(100, total + sum(s['expected_gain'] for s in suggestions))

    grade, grade_label, verdict, icon = grade_of(total, secret_hits)

    result = {
        'file': path,
        'report_type': rtype,
        'type_confidence': confidence,
        'total_score': total,
        'subtotal_before_secret': round(subtotal, 1),
        'secret_deduction': secret_deduction,
        'secret_hits': secret_hits,
        'dimensions': dimensions,
        'issues': all_issues,
        'passed': all_passed,
        'suggestions': suggestions,
        'potential_score': round(potential, 1),
        'grade': {'grade': grade, 'label': grade_label, 'verdict': verdict, 'icon': icon},
    }

    if args.json_out:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    elif args.quiet:
        for i in all_issues:
            print(f"{i['priority']} [{i['dimension']}] {i['location']}: {i['found']} → {i['suggestion']}")
        if secret_hits:
            for s in secret_hits:
                print(f"⛔ [涉密] 第 {s['line']} 段: {s['signal']}（{s['found']}）")
        if not all_issues:
            print('✅ 未发现内容质量问题')
    else:
        render_report(path, result, verbose=args.verbose)

    return 0 if total >= 80 else 1


if __name__ == '__main__':
    sys.exit(main())
