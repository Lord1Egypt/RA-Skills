#!/usr/bin/env python3
"""
裁判文书质量自检清单模块
功能：
  1. 格式规范检查（案号、当事人、落款等）
  2. 内容完整性检查（各部分是否齐全）
  3. 逻辑一致性检查（判决主文与说理是否一致）
  4. 法律术语规范性检查
  5. 输出结构化质量报告
"""

import json
import re
from dataclasses import dataclass, field
from typing import Optional
from rapidfuzz import fuzz


# ─── 数据结构 ──────────────────────────────────────────
@dataclass
class CheckItem:
    """单项检查结果"""
    name: str              # 检查项名称
    category: str          # 分类（格式/内容/逻辑/术语）
    passed: bool           # 是否通过
    severity: str          # 严重程度: error / warning / info
    message: str           # 说明
    fix_suggestion: str = ''  # 修复建议


@dataclass
class QualityReport:
    """质量检查报告"""
    total_checks: int = 0
    passed_checks: int = 0
    errors: int = 0
    warnings: int = 0
    infos: int = 0
    score: float = 0.0      # 0-100
    items: list = field(default_factory=list)  # List[CheckItem]
    summary: str = ''


# ─── 核心函数 ──────────────────────────────────────────
def check_quality(text: str, cause: str = '', elements: dict = None) -> QualityReport:
    """对判决书进行全方位质量自检。"""
    report = QualityReport()
    _check_format(text, report)
    _check_completeness(text, report)
    _check_logic_consistency(text, report)
    _check_legal_terms(text, report)
    if elements:
        _check_elements(elements, report)

    report.total_checks = len(report.items)
    report.passed_checks = sum(1 for item in report.items if item.passed)
    report.errors = sum(1 for item in report.items if item.severity == 'error' and not item.passed)
    report.warnings = sum(1 for item in report.items if item.severity == 'warning' and not item.passed)
    report.infos = sum(1 for item in report.items if item.severity == 'info' and not item.passed)

    if report.total_checks > 0:
        base = (report.passed_checks / report.total_checks) * 100
        error_penalty = report.errors * 10
        warning_penalty = report.warnings * 3
        report.score = max(0, min(100, base - error_penalty - warning_penalty))

    if report.errors > 0:
        report.summary = f'存在 {report.errors} 个严重问题需修复，{report.warnings} 个警告建议处理'
    elif report.warnings > 0:
        report.summary = f'无严重问题，{report.warnings} 个警告建议处理'
    else:
        report.summary = '质量检查全部通过'
    return report


def _add(report, name, cat, passed, sev, msg, fix=''):
    report.items.append(CheckItem(name=name, category=cat, passed=passed,
                                  severity=sev, message=msg, fix_suggestion=fix))


def _check_format(text, report):
    """格式规范检查"""
    has_court = bool(re.search(r'人民法院', text))
    _add(report, '法院名称', '格式', has_court, 'error',
         '法院名称存在' if has_court else '缺少法院名称（应在首部）',
         '在文书首部添加法院全称')

    case_no_pat = r'（\d{4}）[\u4e00-\u9fa5×]+初字第?\d+号'
    has_case_no = bool(re.search(case_no_pat, text))
    _add(report, '案号格式', '格式', has_case_no, 'error',
         '案号格式正确' if has_case_no else '案号格式不规范或缺失',
         '案号格式：（年份）法院简称+案件性质+初字第X号')

    has_title = bool(re.search(r'(民事|刑事|行政|执行)\s*(判决|裁定|调解|决定|通知)\s*书', text))
    _add(report, '文书标题', '格式', has_title, 'error',
         '文书标题格式正确' if has_title else '缺少规范的文书标题',
         '标题应为法院全称+案件性质+文书类型')

    has_cause_label = bool(re.search(r'\*{0,2}案由\*{0,2}[：:]', text))
    _add(report, '案由标识', '格式', has_cause_label, 'warning',
         '包含案由标识' if has_cause_label else '缺少案由标识（建议在当事人后标注）',
         '在当事人部分后添加案由')

    has_judge = bool(re.search(r'(审判长|审判员|代理审判员|人民陪审员)', text))
    _add(report, '审判人员', '格式', has_judge, 'error',
         '包含审判人员信息' if has_judge else '缺少审判人员落款',
         '尾部应包含审判长、审判员/代理审判员、人民陪审员署名')

    has_date = bool(re.search(r'\d{4}年\d{1,2}月\d{1,2}日', text))
    _add(report, '裁判日期', '格式', has_date, 'error',
         '包含裁判日期' if has_date else '缺少裁判日期',
         '尾部应标注裁判日期')

    has_clerk = bool(re.search(r'书记员', text))
    _add(report, '书记员', '格式', has_clerk, 'warning',
         '包含书记员信息' if has_clerk else '缺少书记员署名',
         '尾部应添加书记员署名')

    has_appeal = bool(re.search(r'(上诉|上诉状|中级人民法院)', text))
    _add(report, '上诉权利告知', '格式', has_appeal, 'error',
         '包含上诉权利告知' if has_appeal else '缺少上诉权利告知条款',
         '应告知当事人上诉权利、上诉期限和上诉法院')

    has_delay = bool(re.search(r'(加倍支付|迟延履行|债务利息|民事诉讼法.*264)', text))
    _add(report, '迟延履行利息条款', '格式', has_delay, 'warning',
         '包含迟延履行利息条款' if has_delay else '缺少加倍支付迟延履行利息条款',
         '给付金钱义务的判决应附迟延履行利息条款')


def _check_completeness(text, report):
    """内容完整性检查"""
    has_claims = bool(re.search(r'(诉讼请求|请求判令|请求判决)', text))
    _add(report, '诉讼请求', '内容', has_claims, 'error',
         '包含诉讼请求' if has_claims else '缺少诉讼请求部分',
         '判决书应包含诉讼请求部分')

    has_facts = bool(re.search(r'(经审理查明|本院认定|经查明|查明)', text))
    _add(report, '事实认定', '内容', has_facts, 'error',
         '包含事实认定' if has_facts else '缺少事实认定部分',
         '应有经审理查明或本院认定的事实认定段落')

    has_reasoning = bool(re.search(r'本院认为', text))
    _add(report, '本院认为', '内容', has_reasoning, 'error',
         '包含说理部分' if has_reasoning else '缺少本院认为说理部分',
         '这是判决书最核心的部分，不可省略')

    has_verdict = bool(re.search(r'(判决如下|裁定如下|调解协议如下)', text))
    _add(report, '判决主文', '内容', has_verdict, 'error',
         '包含判决主文' if has_verdict else '缺少判决主文',
         '应有明确的判决如下部分')

    has_evidence = bool(re.search(r'(证据|以上事实|证据证明|举证)', text))
    _add(report, '证据认证', '内容', has_evidence, 'warning',
         '包含证据认证' if has_evidence else '缺少证据认证部分',
         '建议在事实认定后附证据认证段落')

    has_parties = bool(re.search(r'(原告|被告|上诉人|被上诉人)', text))
    _add(report, '当事人信息', '内容', has_parties, 'error',
         '包含当事人信息' if has_parties else '缺少当事人信息',
         '首部应列明原告、被告等当事人基本信息')


def _check_logic_consistency(text, report):
    """逻辑一致性检查"""
    reasoning_match = re.search(r'本院认为[：:]?(.+?)(?=判决如下|裁定如下)', text, re.DOTALL)
    verdict_match = re.search(r'(?:判决如下|裁定如下)[：:]?(.+?)(?=如果未按|案件受理|如不服|审\s*判)', text, re.DOTALL)

    if reasoning_match and verdict_match:
        verdict_text = verdict_match.group(1)
        has_amount = bool(re.search(r'(\d+[\.,]?\d*\s*(?:万|元|美元))', verdict_text))
        has_specific = bool(re.search(r'(解除|确认|停止|赔偿|支付|返还|驳回)', verdict_text))
        _add(report, '说理与主文对应', '逻辑', has_amount or has_specific, 'error',
             '判决主文包含具体判决内容' if (has_amount or has_specific) else '判决主文缺少具体判决内容',
             '判决主文应包含明确的给付金额、行为要求或驳回内容')

    has_confirm = bool(re.search(r'(合同有效|合同效力|确认.*有效)', text))
    has_reject = bool(re.search(r'驳回.*诉讼请求', text))
    has_reject_others = bool(re.search(r'驳回.*其他.*诉讼请求', text))
    if has_confirm and has_reject:
        if has_reject_others:
            # "驳回其他诉讼请求"是正常表述——法院支持部分请求、驳回其余
            _add(report, '效力认定与判决一致性', '逻辑', True, 'info',
                 '文书中存在合同有效认定及驳回其他诉讼请求，属正常部分支持判决',
                 '确认合同有效不等于支持全部诉讼请求，驳回其他属正常')
        else:
            _add(report, '效力认定与判决一致性', '逻辑', False, 'warning',
                 '文书中存在合同有效认定但也有驳回诉讼请求，请确认逻辑是否一致',
                 '确认合同有效不等于支持全部诉讼请求')

    interest_refs = re.findall(r'(?:利息|违约金|资金占用费)[^。]*?(\d+[\.,]?\d*)\s*(?:万|元)', text)
    if interest_refs:
        _add(report, '利息与本金一致性', '逻辑', True, 'info',
             '检测到利息/违约金引用，请人工核对计算是否正确',
             '建议附利息计算明细（本金x利率x天数）')


def _check_legal_terms(text, report):
    """法律术语规范性检查（含模糊匹配）"""
    # 精确匹配规则
    term_fixes = [
        ('被告方', '被告', True),
        ('原告方', '原告', True),
        ('精神损失费', '精神损害赔偿金', False),
        ('抚养费', '抚养费（应区分抚养/赡养/扶养）', True),
    ]
    for wrong, correct, is_ok in term_fixes:
        if wrong in text:
            _add(report, f'术语：{wrong}', '术语', is_ok, 'info' if is_ok else 'warning',
                 f'建议使用规范术语：{correct}' if not is_ok else f'术语使用可接受：{correct}',
                 f'将{wrong}替换为规范表述')

    # 模糊匹配规则（判决书中常见的非规范表述）
    fuzzy_term_rules = [
        # (非规范表述模式, 规范术语, 匹配阈值)
        ('精神损害赔偿', '精神损害赔偿金', 85),
        ('残疾赔偿', '残疾赔偿金', 85),
        ('死亡赔偿', '死亡赔偿金', 85),
        ('误工费', '误工费', 90),
        ('护理费', '护理费', 90),
        ('交通费', '交通费', 90),
        ('住院伙食补助', '住院伙食补助费', 85),
        ('营养费', '营养费', 90),
        ('丧葬费', '丧葬费', 90),
        ('被扶养人生活费', '被扶养人生活费', 90),
    ]

    # 提取文书中的赔偿相关短语进行模糊比对
    赔偿片段 = re.findall(r'[\u4e00-\u9fa5]{2,10}(?:费|金|赔偿)[^。，]{0,15}', text)
    for fragment in 赔偿片段:
        for pattern, standard, threshold in fuzzy_term_rules:
            if fuzz.partial_ratio(pattern, fragment) >= threshold:
                # 模式本身在片段中（精确子串匹配），检查片段是否就是标准术语
                if pattern in fragment and standard in fragment:
                    continue  # 已经是规范表述，跳过
                # 已被 term_fixes 精确匹配的跳过
                if any(w in fragment for w, _, _ in term_fixes):
                    continue
                _add(report, f'术语模糊：{fragment}', '术语', False, 'info',
                     f'「{fragment}」可能应为规范术语「{standard}」',
                     f'确认是否应使用规范表述')
                break  # 一个片段只报一次

    uncertain = ['大概', '可能', '也许', '或许', '应该', '似乎', '好像']
    # 排除法律术语中的不确定用语
    legal_exceptions = ['高度可能性', '高度盖然性', '合理可能性', '排除合理怀疑']
    # 只检查判决书正文部分（排除参考入库案例和优秀文书范式部分）
    judgment_text = text.split('## 📚 参考入库案例')[0] if '## 📚 参考入库案例' in text else text
    judgment_text = judgment_text.split('## ✍️ 参考优秀文书范式')[0] if '## ✍️ 参考优秀文书范式' in judgment_text else judgment_text
    for word in uncertain:
        if word in judgment_text:
            # 检查是否在法律术语中
            is_legal = False
            for exception in legal_exceptions:
                if exception in judgment_text and word in exception:
                    is_legal = True
                    break
            if not is_legal:
                _add(report, f'不确定用语：{word}', '术语', False, 'warning',
                     f'判决书中使用了不确定用语：{word}',
                     '裁判文书应使用确定性语言，避免模糊表述')


def _check_elements(elements, report):
    """检查 pipeline 解析出的要素完整性"""
    cause = elements.get('cause', '')
    _add(report, '案由识别', '要素', bool(cause) and cause != '民事纠纷', 'warning',
         f'案由：{cause}' if cause else '案由未识别',
         '请明确案由')

    parties = elements.get('parties', {})
    has_p = bool(parties.get('原告'))
    has_d = bool(parties.get('被告'))
    _add(report, '当事人提取', '要素', has_p and has_d, 'error',
         f'原告: {parties.get("原告", [])}, 被告: {parties.get("被告", [])}',
         '确保案情描述中包含明确的原告和被告信息')

    facts = elements.get('facts', [])
    _add(report, '关键事实提取', '要素', len(facts) >= 3, 'warning' if len(facts) >= 1 else 'error',
         f'提取到 {len(facts)} 条关键事实',
         '案情描述应包含至少3条关键事实')

    disputes = elements.get('disputes', [])
    _add(report, '争议焦点识别', '要素', len(disputes) >= 1, 'warning',
         f'识别到 {len(disputes)} 个争议焦点',
         '建议明确争议焦点以提升说理针对性')

    claims = elements.get('claims', [])
    _add(report, '诉讼请求提取', '要素', len(claims) >= 1, 'error',
         f'提取到 {len(claims)} 项诉讼请求',
         '请提供明确的诉讼请求')


# ─── 格式化输出 ────────────────────────────────────────
def format_report_text(report):
    """格式化为文本报告"""
    lines = [
        '=' * 50,
        '裁判文书质量自检报告',
        '=' * 50,
        f'总检查项: {report.total_checks}',
        f'通过: {report.passed_checks} | 严重: {report.errors} | 警告: {report.warnings} | 提示: {report.infos}',
        f'质量得分: {report.score:.0f}/100',
        f'结论: {report.summary}',
        '-' * 50,
    ]
    categories = {}
    for item in report.items:
        categories.setdefault(item.category, []).append(item)
    for cat, items in categories.items():
        lines.append(f'\n【{cat}】')
        for item in items:
            icon = 'PASS' if item.passed else ('ERR ' if item.severity == 'error' else ('WARN' if item.severity == 'warning' else 'INFO'))
            lines.append(f'  [{icon}] {item.name}: {item.message}')
            if not item.passed and item.fix_suggestion:
                lines.append(f'         -> {item.fix_suggestion}')
    return '\n'.join(lines)


def format_report_html(report):
    """格式化为 HTML 报告"""
    html = [
        '<!DOCTYPE html><html lang="zh-CN"><head><meta charset="UTF-8">',
        '<title>裁判文书质量自检报告</title>',
        '<style>body{font-family:sans-serif;padding:20px;max-width:800px;margin:0 auto}',
        '.score{font-size:36px;font-weight:700}.pass{color:green}.fail{color:red}.warn{color:orange}',
        '.cat{background:#f8f9fa;border-radius:8px;margin:12px 0;padding:12px}',
        '.item{padding:6px 0;border-bottom:1px solid #eee}</style></head><body>',
        '<h1>裁判文书质量自检报告</h1>',
        f'<p><span class="score">{report.score:.0f}</span>/100</p>',
        f'<p>通过 {report.passed_checks}/{report.total_checks} | 错误 {report.errors} | 警告 {report.warnings}</p>',
        f'<p><strong>{report.summary}</strong></p>',
    ]
    categories = {}
    for item in report.items:
        categories.setdefault(item.category, []).append(item)
    for cat, items in categories.items():
        html.append(f'<div class="cat"><h3>{cat}</h3>')
        for item in items:
            cls = 'pass' if item.passed else ('fail' if item.severity == 'error' else 'warn')
            html.append(f'<div class="item"><span class="{cls}">{"PASS" if item.passed else "FAIL"}</span> {item.name}: {item.message}</div>')
            if not item.passed and item.fix_suggestion:
                html.append(f'<div style="margin-left:40px;color:#2563eb;font-size:13px">-> {item.fix_suggestion}</div>')
        html.append('</div>')
    html.append('</body></html>')
    return '\n'.join(html)


# ─── CLI ───────────────────────────────────────────────
def main():
    import argparse
    parser = argparse.ArgumentParser(description='裁判文书质量自检')
    parser.add_argument('--input', '-i', help='判决书文本')
    parser.add_argument('--file', '-f', help='判决书文件路径')
    parser.add_argument('--cause', '-c', help='案由')
    parser.add_argument('--format', choices=['text', 'html'], default='text')
    parser.add_argument('--json', action='store_true')
    args = parser.parse_args()

    text = ''
    if args.input:
        text = args.input
    elif args.file:
        from pathlib import Path
        text = Path(args.file).read_text(encoding='utf-8')
    else:
        print('请提供判决书文本：--input 或 --file')
        return

    report = check_quality(text, args.cause or '')

    if args.json:
        print(json.dumps({
            'score': report.score, 'total': report.total_checks,
            'passed': report.passed_checks, 'errors': report.errors,
            'warnings': report.warnings, 'summary': report.summary,
            'items': [{'name': i.name, 'category': i.category, 'passed': i.passed,
                       'severity': i.severity, 'message': i.message, 'fix': i.fix_suggestion}
                      for i in report.items],
        }, ensure_ascii=False, indent=2))
    elif args.format == 'html':
        print(format_report_html(report))
    else:
        print(format_report_text(report))


if __name__ == '__main__':
    main()
