#!/usr/bin/env python3
"""
KT 合同审查脚本
基于 100 条修改习惯（#1-#220）+ 7 大修改原则

用法:
    python3 contract_review.py <合同文件> [--position 甲方|乙方] [--output report.md]
    
示例:
    python3 contract_review.py ~/Downloads/合作合同.docx --position 乙方
"""

import sys
import os
import re
import argparse
from pathlib import Path
from docx import Document


# ===== 7 大原则检查器 =====
PRINCIPLES = {
    '①过错责任原则': {
        'desc': '把乙方全责改为"乙方在过错范围内承担"',
        'patterns': [
            (r'(全部|所有).{0,10}(责任|赔偿).{0,15}(乙方|乙方承担)', '❌ 绝对化责任表述，应改为"在过错范围内承担"'),
            (r'(乙方|乙方承担).{0,5}(全部|所有|无限).{0,5}(责任|连带)', '❌ 无限连带责任，应设上限'),
        ]
    },
    '②双向约束': {
        'desc': '原版只约束乙方，同步加甲方对等义务',
        'patterns': [
            (r'乙方.{0,20}(篡改|隐瞒|干扰|伪造)', '⚠️ 单向约束乙方，应同步加甲方对应义务'),
            (r'甲方.{0,5}(有权|可以).{0,15}(查看|查阅|检查).{0,5}乙方.{0,15}(数据|后台|凭证)', '⚠️ 甲方权限无对应约束'),
        ]
    },
    '③7 日催告': {
        'desc': '解约前给 7 日补救期',
        'patterns': [
            (r'(有权|可以).{0,10}(单方|立即).{0,10}(解除|终止).{0,10}(合同|协议)', '❌ 单方立即解约，应加 7 日书面催告'),
            (r'(未达|不符合|不符合约定).{0,20}(有权|可).{0,10}(解除|终止)', '⚠️ 解约门槛过低，建议加催告程序'),
        ]
    },
    '④责任上限': {
        'desc': '累计赔偿不超过 12 个月已支付分成',
        'patterns': [
            (r'(违约金|赔偿金|补偿金).{0,30}(无上限|不设上限)', '❌ 赔偿无上限，应设上限'),
            (r'累计.{0,10}(赔偿|责任).{0,20}(不超过|不高于).{0,20}(合同|总额)', '⚠️ 责任上限条款需明确'),
        ]
    },
    '⑤甲方免责': {
        'desc': '非乙方原因导致的不担责',
        'patterns': [
            (r'(因|由于).{0,15}(甲方|发包人).{0,15}(原因|过错).{0,15}(乙方.{0,10}(承担|负责|赔偿))', '❌ 因甲方原因乙方担责，违反免责原则'),
            (r'(不可抗力|政府|政策).{0,30}(乙方.{0,10}(承担|负责))', '⚠️ 不可抗力/政府原因乙方担责'),
        ]
    },
    '⑥紧急补偿': {
        'desc': '甲方单方免责改为补偿合理损失',
        'patterns': [
            (r'(紧急|应急|突发).{0,20}(甲方.{0,10}(免责|无需担责|无需承担))', '❌ 紧急情形甲方单方免责，应加补偿机制'),
            (r'(领导|消防|规划).{0,20}(乙方.{0,10}(无条件|必须|立即)(配合|撤离))', '⚠️ 紧急情形乙方无条件配合，应加补偿'),
        ]
    },
    '⑦格式规范': {
        'desc': '统一用语、编号、空白格式',
        'patterns': [
            (r'本协议|本合同', '⚠️ "本协议"和"本合同"混用，建议统一'),
            (r'\d+\.\d+[^\s]', '⚠️ 编号后缺空格（应统一为"1.1 标题"格式）'),
        ]
    },
}

# ===== 34 条具体习惯检查器（#187-#220）=====
HABITS = [
    # A. 责任分配类（7 条）
    (187, '过错责任原则统一贯彻', r'(全部|所有)责任.{0,10}(由乙方承担|乙方独立承担)', '"全部由乙方承担" → "乙方在过错范围内承担"'),
    (188, '双向约束条款', r'乙方.{0,20}(篡改|隐瞒|伪造)', '同步加甲方对等义务（如甲方干扰后台要赔）'),
    (191, '甲方原因免责条款', r'因.{0,15}甲方.{0,10}(原因|过错)', '确保加"乙方不承担责任"或类似免责'),
    (196, '消防责任范围缩窄', r'乙方.{0,10}(整体|全部).{0,5}消防', '限乙方只对设备部分负责，不扩大到场地整体'),
    (208, '保险投保资料配合义务', r'(乙方|投保人).{0,20}自行.{0,5}(投保|办理)', '加甲方资料配合义务'),
    (209, '审批手续抗辩权', r'(被.{0,10}查处|被.{0,10}处罚).{0,15}(乙方.{0,10}(违约|担责))', '加乙方抗辩权（甲方场地/协助问题）'),
    (210, '知识产权素材瑕疵责任', r'(使用甲方|因使用).{0,15}素材.{0,15}(全部|所有).{0,5}乙方承担', '素材本身瑕疵应由甲方担责'),
    # B. 催告+程序类（5 条）
    (189, '7 日书面催告程序', r'(有权|可).{0,5}(立即|单方).{0,5}(解除|终止)', '解约前必须先发书面催告'),
    (197, '图纸审查默示同意', r'(图纸|方案).{0,10}(审查|审核)', '加"7 工作日内未出具意见视为同意"'),
    (202, '紧急抢修豁免通知前置', r'(安装|拆除).{0,15}(未经.{0,5}同意|书面同意)', '加"紧急抢修情况除外"豁免'),
    (214, '接收确认表催告程序', r'(未签|未办理|未签署).{0,15}(视为.{0,5}交付)', '加催告程序'),
    (215, '维修催告程序', r'(不能.{0,5}使用|停止.{0,5}工作).{0,10}(\d+).{0,3}日', '加书面催告后仍不修才可解约'),
    # C. 赔偿与上限类（4 条）
    (190, '累计赔偿责任上限', r'(违约金|赔偿金).{0,20}(总额|累计).{0,15}(超过|无上限)', '建议加 12 个月已付分成上限'),
    (199, '逾期付款违约金上限', r'每逾期.{0,5}1.{0,3}日.{0,15}(1‰|千分之一)', '加"但总额不超过 20%"'),
    (200, '赔偿范围排除间接/商誉', r'(全部|所有)损失.{0,20}(商誉|间接|预期)', '建议改为"直接经济损失"'),
    (218, '责任上限与具体上限关系', r'(当期|本月).{0,10}(分配|收益).{0,10}(限额|上限)', '与 12 个月总额上限取较低者'),
    # D. 风险隔离类（4 条）
    (192, '紧急情形补偿机制', r'(紧急|应急).{0,15}(无需.{0,5}承担|免责)', '加"补偿合理直接损失"'),
    (194, '甲方电力/场地义务量化', r'(提供|保障).{0,5}(电力|场地)', '加"未提前通知中断要赔"'),
    (198, '政府原因举证倒置', r'(政府|政策).{0,15}(原因).{0,15}(免责|不视为违约)', '加"甲方必须提供政府批文"'),
    (205, '物品清理双向免责', r'视为.{0,5}(自动|乙方).{0,5}(放弃|放弃物品)', '加"不可抗力/甲方原因乙方不担责"'),
    # E. 退出与补偿类（4 条）
    (193, '优先续约权', r'(续签|续约).{0,15}(协商|双方)', '加"乙方享有同等条件下优先续约权"'),
    (211, '改造后退出权', r'(调整|改造|变更).{0,15}(无条件|必须).{0,5}(配合|接受)', '加"新点位不满足基本要求乙方可退出"'),
    (212, '设备调整提前通知期', r'(调整|变更|移动).{0,15}点位', '加"至少提前 15 工作日书面通知"'),
    (219, '终止补偿协商机制', r'(补偿|赔偿).{0,15}(金额|费用)', '加"由双方协商确定"'),
    # F. 数据/技术类（4 条）
    (195, '数据查阅范围限制', r'(永久|长期).{0,5}(查阅|查看).{0,15}(数据|后台)', '限"核对账目"目的，加"协议终止后仍有效"'),
    (206, '数据后台双向保护', r'(查阅|查看|登录).{0,5}后台', '加"甲方不得干扰后台，否则赔乙方损失"'),
    (213, '抗辩+赔偿反制条款', r'(视为|构成).{0,5}(重大|根本).{0,5}违约', '加乙方抗辩+反诉条款'),
    (220, '不可抗力定义程序化', r'不可抗力.{0,15}(及时|立即).{0,5}通知', '加"通知+证明+持续期+结算"四要素'),
    # G. 其他（6 条）
    (201, '履约保证金+履约保函', None, '长期合作类合同建议加 5-10% 履约保证金'),
    (203, '改造调整双向友好协商', r'(改造|调整).{0,15}(无条件|必须)配合', '加"友好协商+通知期+费用分担"'),
    (204, '调价机制加重违约成本', r'(调整|修改).{0,5}价格.{0,10}(书面通知|协商)', '加"私自改价要赔直接损失"'),
    (207, '协助义务具体化', r'(必要|合理).{0,5}协助', '具体列出协助内容（监控/证明等）'),
    (216, '过失责任分级', r'(乙方).{0,10}(任何|所有).{0,5}过失', '加"重大过失/故意+直接/单独+可证明"'),
    (217, '过错认定主体明确', r'(乙方|甲方).{0,15}(责任|赔偿)', '加"经有权机关认定或双方确认"'),
]


def extract_text(filepath):
    """从 docx/txt/md 文件提取文本"""
    filepath = str(filepath)
    if filepath.endswith('.docx'):
        doc = Document(filepath)
        return '\n'.join(p.text for p in doc.paragraphs if p.text.strip())
    else:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()


def detect_position(text):
    """检测 Kent 的立场（甲方/乙方）"""
    # 默认启发式：
    # - 如果合同大量提到"乙方"做坏事（如"乙方负责"、"乙方违约"），Kent 可能是甲方
    # - 如果合同大量提到"甲方"做坏事，Kent 可能是乙方
    # 简化版：根据合同主体识别
    
    # 简单模式：检查甲方是否有强势条款
    strong_party_patterns = [
        r'甲方.{0,5}(单方|无需|不必)',
        r'甲方.{0,10}(免责|免责条款)',
    ]
    
    weak_party_patterns = [
        r'乙方.{0,10}(全部|所有).{0,5}责任',
        r'乙方.{0,10}(无条件|必须).{0,5}配合',
    ]
    
    strong_count = sum(1 for p in strong_party_patterns if re.search(p, text))
    weak_count = sum(1 for p in weak_party_patterns if re.search(p, text))
    
    if strong_count > weak_count:
        return '甲方'  # 甲方强势，Kent 是乙方（受保护方）
    elif weak_count > strong_count:
        return '乙方'  # 乙方强势，Kent 是甲方（受保护方）
    else:
        return '需人工判断'


def check_principles(text):
    """7 大原则检查"""
    results = {}
    for principle, info in PRINCIPLES.items():
        issues = []
        for pattern, message in info['patterns']:
            matches = re.finditer(pattern, text)
            for match in matches:
                # 截取上下文
                start = max(0, match.start() - 20)
                end = min(len(text), match.end() + 20)
                context = text[start:end].replace('\n', ' ')
                issues.append({
                    'pattern': pattern,
                    'context': context,
                    'message': message
                })
        results[principle] = {
            'desc': info['desc'],
            'issues': issues
        }
    return results


def check_habits(text):
    """34 条具体习惯检查"""
    results = []
    for num, name, pattern, suggestion in HABITS:
        if pattern is None:
            # 仅建议
            results.append({
                'num': num,
                'name': name,
                'pattern': None,
                'matches': [],
                'suggestion': suggestion,
                'severity': '低'
            })
            continue
        
        matches = []
        for match in re.finditer(pattern, text):
            start = max(0, match.start() - 30)
            end = min(len(text), match.end() + 30)
            context = text[start:end].replace('\n', ' ')
            matches.append(context)
        
        # 判断严重程度
        if matches:
            severity = '高' if num in [187, 189, 190, 200] else '中'
        else:
            severity = None
        
        results.append({
            'num': num,
            'name': name,
            'pattern': pattern,
            'matches': matches,
            'suggestion': suggestion,
            'severity': severity
        })
    
    return results


def generate_report(filepath, position, principle_results, habit_results, output_path=None):
    """生成审查报告"""
    lines = []
    
    lines.append(f"# 合同审查报告")
    lines.append(f"\n> **审查日期：** 2026-08-19  ")
    lines.append(f"> **审查工具：** KT 合同审查脚本 v1.0.0  ")
    lines.append(f"> **合同文件：** {filepath}  ")
    lines.append(f"> **Kent 立场：** {position}\n")
    
    lines.append("## 一、风险总览\n")
    
    # 统计风险数
    high_count = sum(1 for h in habit_results if h['severity'] == '高')
    mid_count = sum(1 for h in habit_results if h['severity'] == '中')
    low_count = sum(1 for h in habit_results if h['severity'] == '低')
    
    lines.append(f"- 🔴 高风险：{high_count} 条")
    lines.append(f"- 🟡 中风险：{mid_count} 条")
    lines.append(f"- 🟢 低风险（建议）：{low_count} 条\n")
    
    # 7 大原则得分
    lines.append("## 二、7 大原则检查\n")
    for principle, info in principle_results.items():
        status = '✅ 通过' if not info['issues'] else f'❌ {len(info["issues"])} 个问题'
        lines.append(f"### {principle} - {status}")
        lines.append(f"*{info['desc']}*")
        if info['issues']:
            for issue in info['issues'][:5]:  # 最多 5 个
                lines.append(f"- {issue['message']}")
                lines.append(f"  - 上下文：`...{issue['context']}...`")
        lines.append("")
    
    # 34 条具体习惯
    lines.append("## 三、34 条具体习惯检查\n")
    
    # 高风险
    high_risks = [h for h in habit_results if h['severity'] == '高']
    if high_risks:
        lines.append("### 🔴 高风险（必须修改）\n")
        for h in high_risks:
            lines.append(f"**#{h['num']} {h['name']}**")
            lines.append(f"- 建议：{h['suggestion']}")
            if h['matches']:
                lines.append(f"- 出现 {len(h['matches'])} 处，例：`...{h['matches'][0]}...`")
            lines.append("")
    
    # 中风险
    mid_risks = [h for h in habit_results if h['severity'] == '中']
    if mid_risks:
        lines.append("### 🟡 中风险（强烈建议修改）\n")
        for h in mid_risks[:10]:  # 最多 10 个
            lines.append(f"**#{h['num']} {h['name']}**")
            lines.append(f"- 建议：{h['suggestion']}")
            if h['matches']:
                lines.append(f"- 出现 {len(h['matches'])} 处")
            lines.append("")
    
    # 低风险建议
    low_risks = [h for h in habit_results if h['severity'] == '低']
    if low_risks:
        lines.append("### 🟢 低风险（可选优化）\n")
        for h in low_risks:
            lines.append(f"- **#{h['num']} {h['name']}**：{h['suggestion']}")
    
    # 修改优先级
    lines.append("\n## 四、修改优先级建议\n")
    lines.append("1. **必须改（高风险）**：先解决 7 大原则违反 + 高风险条款")
    lines.append("2. **强烈建议改（中风险）**：按 #189-#200 顺序优化")
    lines.append("3. **可选优化（低风险）**：根据合同金额和重要性决定")
    
    lines.append("\n## 五、整体评估\n")
    if high_count >= 5:
        lines.append("⚠️ **高风险条款较多**，建议优先修改。如谈判压力大，可分批处理。")
    elif high_count >= 1:
        lines.append("⚠️ **存在少量高风险条款**，建议针对性修改。")
    else:
        lines.append("✅ **合同基础框架良好**，按建议继续优化细节。")
    
    report = '\n'.join(lines)
    
    if output_path:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(report)
        print(f"✅ 报告已保存：{output_path}")
    else:
        print(report)
    
    return report


def main():
    parser = argparse.ArgumentParser(description='KT 合同审查脚本')
    parser.add_argument('filepath', help='合同文件路径（docx/txt/md）')
    parser.add_argument('--position', choices=['甲方', '乙方'], help='Kent 立场（不填自动检测）')
    parser.add_argument('--output', '-o', help='输出报告路径（默认打印到 stdout）')
    
    args = parser.parse_args()
    
    filepath = Path(args.filepath).expanduser()
    if not filepath.exists():
        print(f"❌ 文件不存在：{filepath}")
        sys.exit(1)
    
    print(f"📄 审查文件：{filepath}")
    
    # 1. 提取文本
    text = extract_text(filepath)
    print(f"📊 文本长度：{len(text)} 字符")
    
    # 2. 检测立场
    position = args.position or detect_position(text)
    print(f"🎯 Kent 立场：{position}")
    
    # 3. 7 大原则检查
    principle_results = check_principles(text)
    
    # 4. 34 条习惯检查
    habit_results = check_habits(text)
    
    # 5. 生成报告
    print("\n" + "="*60)
    generate_report(filepath, position, principle_results, habit_results, args.output)


if __name__ == '__main__':
    main()
