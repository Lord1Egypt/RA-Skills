"""
投标人侧·招标文件风险自查工具（tender risk self-check）

定位：政府采购「盲投参谋」的防御模块。仅从投标人视角，基于招标文件公开文本，
做两类自查：
  1. 时间节点合规自查 —— 验证发售期/投标截止/澄清时限/中标公示/合同签订时限
     是否符合《政府采购法》及实施条例的法定最低要求（投标人有义务核对，避免误期废标）。
  2. 排他性 / 萝卜坑条款扫描 —— 识别可能为特定供应商量体裁衣、构成歧视或排斥潜在
     投标人的条款信号，供投标人判断是否值得投入、或依法提出质疑。

安全边界（重要）：
  - 本工具【不】检测、不提供任何"投标人之间串标/围标"的识别或规避方法。
    原版"围标串标检测（比对其他投标人电话/MAC/报价规律）"因涉及无权限获取他人
    数据、且信号可被反向利用规避合规审查，已从本技能移除。
  - 所有输出仅为风险提示与法条依据，最终是否投标 / 是否质疑由投标人自行决定。

使用方式：
  python compliance_checker.py --project "project.json" --output "risk_selfcheck.json"
"""

import argparse
import json
import os
import re
from datetime import datetime
from typing import Optional  # noqa: F401


# === 时间节点合规规则（法定最低要求，已按现行法纠偏） ===
# 注：原版"发售期≥5日/中标公示≥1日"未区分"日"与"工作日"，已修正为工作日口径。
TIME_COMPLIANCE_RULES = [
    {
        'id': 'T001',
        'name': '招标文件发售期',
        'description': '招标文件发售期不得少于 5 个工作日',
        'law': '《政府采购法实施条例》第31条',
        'min_workdays': 5,
        'check': lambda p: _check_workdays(p.get('sale_start'), p.get('sale_end'), 5),
    },
    {
        'id': 'T002',
        'name': '投标截止时限',
        'description': '自招标文件开始发出之日起至投标截止，不得少于 20 日',
        'law': '《政府采购法》第35条',
        'min_days': 20,
        'check': lambda p: _check_calendar_days(p.get('notice_date'), p.get('bid_deadline'), 20),
    },
    {
        'id': 'T003',
        'name': '澄清/修改发出时限',
        'description': '澄清或修改应在投标截止至少 15 日前发出',
        'law': '《政府采购法实施条例》第31条',
        'min_workdays': 15,
        'check': lambda p: _check_workdays(p.get('clarification_date'), p.get('bid_deadline'), 15),
    },
    {
        'id': 'T004',
        'name': '中标公示期',
        'description': '中标结果公告公示期不得少于 1 个工作日',
        'law': '《政府采购法实施条例》第43条',
        'min_workdays': 1,
        'check': lambda p: _check_workdays(p.get('result_date'), p.get('result_end_date'), 1),
    },
    {
        'id': 'T005',
        'name': '合同签订时限',
        'description': '采购合同应自中标通知书发出之日起 30 日内签订',
        'law': '《政府采购法》第46条',
        'max_days': 30,
        'check': lambda p: _check_max_calendar_days(p.get('notice_date'), p.get('contract_date'), 30),
    },
]


def _parse_date(s):
    if not s:
        return None
    for fmt in ('%Y-%m-%d', '%Y/%m/%d', '%Y-%m-%d %H:%M', '%Y/%m/%d %H:%M'):
        try:
            return datetime.strptime(s[:16] if ' ' in s else s[:10], fmt)
        except (ValueError, TypeError):
            continue
    return None


def _is_workday(d):
    return d.weekday() < 5  # 0-4 为周一至周五


def _count_workdays(start, end):
    """含端点的工作日数（排除周末，未排除法定节假日——投标人有义务进一步核对）"""
    days = 0
    cur = start
    while cur <= end:
        if _is_workday(cur):
            days += 1
        cur = cur.fromordinal(cur.toordinal() + 1)
    return days


def _check_workdays(start_str, end_str, min_wd):
    start, end = _parse_date(start_str), _parse_date(end_str)
    if not start or not end:
        return {'compliant': None, 'message': '日期信息不完整，无法检查（请补充招标文件中的对应日期）'}
    wd = _count_workdays(start, end)
    ok = wd >= min_wd
    return {
        'compliant': ok,
        'actual_workdays': wd,
        'required_workdays': min_wd,
        'message': f'实际 {wd} 个工作日，要求 ≥{min_wd} 个工作日' + (' ✅' if ok else ' ❌ 不足，可质疑'),
    }


def _check_calendar_days(start_str, end_str, min_days):
    start, end = _parse_date(start_str), _parse_date(end_str)
    if not start or not end:
        return {'compliant': None, 'message': '日期信息不完整，无法检查'}
    delta = (end - start).days
    ok = delta >= min_days
    return {
        'compliant': ok,
        'actual_days': delta,
        'required_days': min_days,
        'message': f'实际 {delta} 日历日，要求 ≥{min_days} 日' + (' ✅' if ok else ' ❌ 不足'),
    }


def _check_max_calendar_days(start_str, end_str, max_days):
    start, end = _parse_date(start_str), _parse_date(end_str)
    if not start or not end:
        return {'compliant': None, 'message': '日期信息不完整，无法检查'}
    delta = (end - start).days
    ok = delta <= max_days
    return {
        'compliant': ok,
        'actual_days': delta,
        'required_days': max_days,
        'message': f'实际 {delta} 日，要求 ≤{max_days} 日' + (' ✅' if ok else ' ❌ 超期'),
    }


# === 排他性 / 萝卜坑条款扫描（投标人防御视角） ===
# 仅做"信号提示"，不替代法律判断；命中后建议投标人结合全文语境判断是否构成歧视。
EXCLUSIVITY_PATTERNS = [
    {
        'id': 'E001',
        'name': '限定特定品牌/型号',
        'risk_level': 'high',
        'pattern': re.compile(r'(指定|限定|仅限|必须采用|原厂|同品牌|同型号|某某品牌|特定品牌)'),
        'hint': '可能排斥潜在供应商，除非有合理技术必要性并允许等效替代。',
    },
    {
        'id': 'E002',
        'name': '特定地域业绩/本地注册门槛',
        'risk_level': 'medium',
        'pattern': re.compile(r'(本地注册|本地纳税|本地服务|须在.*(省市区)注册|当地业绩|本省业绩)'),
        'hint': '以地域限制排斥外地供应商，通常违法（除法定例外情形）。',
    },
    {
        'id': 'E003',
        'name': '过高/无关的资质门槛',
        'risk_level': 'medium',
        'pattern': re.compile(r'(须具有|要求具备).{0,20}(甲级|一级|涉密|原厂授权|独家代理)'),
        'hint': '资质要求应与项目规模/性质匹配，过高门槛可能构成变相排斥。',
    },
    {
        'id': 'E004',
        'name': '奖项/认证与履约无关',
        'risk_level': 'low',
        'pattern': re.compile(r'(须获得|必须提供).{0,25}(驰名商标|奖项|特定荣誉|指定奖项)'),
        'hint': '将无关奖项作为加分/门槛，可能构成以不合理条件限制竞争。',
    },
    {
        'id': 'E005',
        'name': '技术参数指向性',
        'risk_level': 'high',
        'pattern': re.compile(r'(技术指标须与.{0,15}完全一致|唯一供应商|唯一专利|专有技术)'),
        'hint': '技术参数高度指向特定方案/专利，需核实是否具有唯一合理性。',
    },
]


def scan_exclusivity_clauses(text: str) -> list:
    """扫描招标文件文本，返回命中的排他性信号列表"""
    if not text:
        return []
    hits = []
    for rule in EXCLUSIVITY_PATTERNS:
        for m in rule['pattern'].finditer(text):
            snippet = text[max(0, m.start() - 25): m.end() + 25].replace('\n', ' ')
            hits.append({
                'rule_id': rule['id'],
                'name': rule['name'],
                'risk_level': rule['risk_level'],
                'snippet': snippet.strip(),
                'hint': rule['hint'],
            })
            break  # 同一规则命中一次即记录，避免重复刷屏
    return hits


class TenderRiskSelfChecker:
    """招标文件风险自查（投标人防御视角）"""

    def __init__(self, project: dict):
        self.project = project

    def check(self) -> dict:
        result = {
            'project_id': self.project.get('id', ''),
            'project_name': self.project.get('title', self.project.get('project_name', '')),
            'time_compliance': [],
            'exclusivity_alerts': [],
            'overall_risk': 'low',
        }

        # 1. 时间节点合规
        for rule in TIME_COMPLIANCE_RULES:
            result['time_compliance'].append({
                'rule_id': rule['id'],
                'name': rule['name'],
                'law': rule['law'],
                'result': rule['check'](self.project),
            })

        # 2. 排他性条款扫描
        text = self.project.get('full_text') or self.project.get('description', '')
        if text:
            result['exclusivity_alerts'] = scan_exclusivity_clauses(text)

        # 综合风险
        time_violations = sum(1 for t in result['time_compliance']
                              if t['result'].get('compliant') is False)
        high_excl = sum(1 for a in result['exclusivity_alerts'] if a['risk_level'] == 'high')
        med_excl = sum(1 for a in result['exclusivity_alerts'] if a['risk_level'] == 'medium')

        if high_excl >= 1 or time_violations >= 1:
            result['overall_risk'] = 'high'
        elif med_excl >= 1:
            result['overall_risk'] = 'medium'
        else:
            result['overall_risk'] = 'low'

        return result

    @staticmethod
    def generate_report(result: dict) -> str:
        lines = ['# 招标文件风险自查报告（投标人防御视角）', '']
        lines.append(f"项目：{result['project_name']}（{result['project_id']}）")
        risk_icon = {'high': '🔴', 'medium': '🟡', 'low': '🟢'}.get(result['overall_risk'], '⚪')
        lines.append(f"综合风险：{risk_icon} {result['overall_risk']}")
        lines.append('')

        lines.append('## 一、时间节点合规自查')
        for t in result['time_compliance']:
            r = t['result']
            mark = '✅' if r.get('compliant') is True else ('❌' if r.get('compliant') is False else '⚠️')
            lines.append(f"- [{t['rule_id']}] {t['name']}（{t['law']}）{mark} {r.get('message','')}")
        lines.append('')

        if result['exclusivity_alerts']:
            lines.append('## 二、排他性 / 萝卜坑条款信号')
            for a in result['exclusivity_alerts']:
                icon = {'high': '🔴', 'medium': '🟡', 'low': '🟢'}.get(a['risk_level'], '⚪')
                lines.append(f"- {icon} [{a['rule_id']}] {a['name']}：{a['hint']}")
                lines.append(f"  原文片段：…{a['snippet']}…")
            lines.append('')
            lines.append('> 上述为信号提示，不构成违法认定。是否构成歧视性条款需结合全文与法定例外判断；')
            lines.append('> 如确有排斥性，可在法定期限内依法提出质疑/投诉。')
            lines.append('')
        else:
            lines.append('## 二、排他性条款扫描')
            lines.append('未发现明显排他性信号（不替代逐条人工审阅）。')
            lines.append('')

        lines.append('---')
        lines.append('> ⚠️ 本报告仅基于公开招标文件做风险提示，不构成法律意见。最终投标/质疑决策由投标人自行作出。')
        return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(description='招标文件风险自查（投标人防御视角）')
    parser.add_argument('--project', required=True, help='项目 JSON（含时间字段与可选 full_text）')
    parser.add_argument('--output', default='tender_risk_selfcheck.json', help='输出 JSON')
    parser.add_argument('--report', default='tender_risk_selfcheck.md', help='输出 Markdown 报告')
    args = parser.parse_args()

    with open(args.project, 'r', encoding='utf-8') as f:
        project = json.load(f)

    checker = TenderRiskSelfChecker(project)
    result = checker.check()

    with open(args.output, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    with open(args.report, 'w', encoding='utf-8') as f:
        f.write(TenderRiskSelfChecker.generate_report(result))

    print(f"风险自查完成：综合风险 {result['overall_risk']}")
    print(f"  时间违规：{sum(1 for t in result['time_compliance'] if t['result'].get('compliant') is False)} 项")
    print(f"  排他性信号：{len(result['exclusivity_alerts'])} 条")
    print(f"结果已保存：{os.path.abspath(args.output)}")
    print(f"报告已保存：{os.path.abspath(args.report)}")


if __name__ == '__main__':
    main()
