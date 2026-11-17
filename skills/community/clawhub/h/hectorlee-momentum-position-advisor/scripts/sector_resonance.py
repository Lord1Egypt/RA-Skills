"""
板块共振检测 V1.2
目标：当同板块多只股票同时触发卖出信号时，自动降级其他持仓/减仓标的。

逻辑：
1. 批量诊断后，按板块分组
2. 同一板块内 ≥2 只触发 SELL → 板块系统性风险确认
3. 该板块内 HOLD/REDUCE 标的自动-10分（共振降级）
"""

from typing import List, Dict, Optional, Tuple

# ─── 板块分类 ───

# 优先使用的精确映射（常见标的）
CODE_SECTOR_MAP: Dict[str, str] = {
    # 半导体/AI芯片
    '688256': '半导体/AI芯片',
    '688981': '半导体制造',
    '688041': '半导体/AI芯片',
    '688047': '半导体/AI芯片',
    '002436': '半导体/PCB',
    '688608': '半导体/芯片设计',
    '688521': '半导体/芯片设计',
    '603986': '半导体/存储',
    '688012': '半导体设备',
    '002371': '半导体设备',
    '688200': '半导体材料',
    # 消费电子
    '688036': '消费电子/手机',
    '002475': '消费电子/连接器',
    '300433': '消费电子/玻璃',
    # 电池/新能源
    '300207': '电池/消费电子',
    '300750': '电池/新能源',
    '300014': '电池/新能源',
    # 汽车零部件
    '000559': '汽车零部件',
    '002920': '汽车电子',
    # 新材料
    '300328': '新材料/液态金属',
    # 通信
    '600941': '通信/运营商',
    '600050': '通信/运营商',
    # AI/光模块
    '300502': '光模块/CPO',
    '300308': '光模块/CPO',
    '300394': '光模块/CPO',
}

# 板块关键词匹配（基于股票名称）
NAME_KEYWORDS: Dict[str, str] = {
    '寒武纪': '半导体/AI芯片',
    '海光': '半导体/AI芯片',
    '中芯': '半导体制造',
    '华虹': '半导体制造',
    '长鑫': '半导体/存储',
    '兆易': '半导体/存储',
    '韦尔': '半导体/芯片设计',
    '卓胜': '半导体/芯片设计',
    '圣邦': '半导体/芯片设计',
    '北方华创': '半导体设备',
    '中微': '半导体设备',
    '兴森': '半导体/PCB',
    '深南': '半导体/PCB',
    '恒玄': '半导体/芯片设计',
    '晶晨': '半导体/芯片设计',
    '澜起': '半导体/芯片设计',
    '新易盛': '光模块/CPO',
    '中际': '光模块/CPO',
    '天孚': '光模块/CPO',
    '欣旺达': '电池/消费电子',
    '宁德': '电池/新能源',
    '比亚迪': '汽车/新能源',
    '万向': '汽车零部件',
    '德赛': '汽车电子',
    '信科': '通信/设备',
    '中兴': '通信/设备',
}


def classify_sector(code: str, name: str = '') -> str:
    """
    板块分类：优先级: 精确映射 > 名称关键词 > 代码前缀推断
    
    返回板块名称，未匹配返回 '其他'
    """
    # 1. 精确代码映射
    if code in CODE_SECTOR_MAP:
        return CODE_SECTOR_MAP[code]
    
    # 2. 名称关键词匹配
    for keyword, sector in NAME_KEYWORDS.items():
        if keyword in name:
            return sector
    
    # 3. 代码前缀推断（弱信号，仅作分类参考）
    if code.startswith('688'):
        return '科创板/科技'
    elif code.startswith('300') or code.startswith('301'):
        return '创业板'
    elif code.startswith('000') or code.startswith('001'):
        return '主板'
    elif code.startswith('002') or code.startswith('003'):
        return '中小板'
    elif code.startswith('600') or code.startswith('601') or code.startswith('603') or code.startswith('605'):
        return '沪市主板'
    
    return '其他'


def _get_broad_sector(fine_sector: str) -> str:
    """获取大类板块（合并细分板块做共振检测）"""
    # 半导体相关的合并为一类
    if any(kw in fine_sector for kw in ['半导体', '芯片', 'PCB']):
        return '半导体板块'
    if any(kw in fine_sector for kw in ['光模块', 'CPO']):
        return '光模块/CPO'
    if any(kw in fine_sector for kw in ['电池', '新能源']):
        return '新能源板块'
    if any(kw in fine_sector for kw in ['汽车']):
        return '汽车板块'
    if any(kw in fine_sector for kw in ['通信']):
        return '通信板块'
    if any(kw in fine_sector for kw in ['消费电子']):
        return '消费电子板块'
    return fine_sector


def detect_sector_resonance(
    diagnoses: List[dict],
    downgrade_pts: int = -10,
    sell_threshold: int = 2
) -> Tuple[Dict[str, int], List[dict]]:
    """
    检测板块共振，对同板块HOLD/REDUCE标的降级。
    
    参数:
        diagnoses: 诊断结果列表 [{'code':..., 'name':..., 'score':..., 'decision':...}, ...]
        downgrade_pts: 降级扣分值，默认-10
        sell_threshold: 同板块卖出阈值，默认≥2只触发共振
    
    返回:
        (resonance_report, adjusted_diagnoses)
        resonance_report: {'半导体板块': 3, '新能源板块': 1} 各板块卖出数量
        adjusted_diagnoses: 调整后的诊断结果列表
    """
    if len(diagnoses) < 2:
        return {}, list(diagnoses)
    
    # 分组：大类板块 → [诊断结果]
    groups: Dict[str, List[dict]] = {}
    for d in diagnoses:
        code = d.get('code', '')
        name = d.get('name', '')
        fine_sector = classify_sector(code, name)
        broad = _get_broad_sector(fine_sector)
        if broad not in groups:
            groups[broad] = []
        groups[broad].append(d)
    
    # 检测共振
    resonance_report = {}
    adjusted = []
    
    for sector, members in groups.items():
        if len(members) < 2:
            adjusted.extend(members)
            continue
        
        sell_count = sum(1 for m in members 
                        if m.get('score', {}).get('decision', '') == 'sell')
        resonance_report[sector] = sell_count
        
        if sell_count >= sell_threshold:
            # 共振确认：该板块内非卖出标的降级
            for m in members:
                score_data = m.get('score', {})
                decision = score_data.get('decision', '')
                
                if decision in ('hold', 'hold_buy', 'reduce'):
                    # 记录原始分数
                    orig_total = score_data.get('total', 0)
                    orig_decision = decision
                    
                    # 扣分
                    new_total = max(0, orig_total + downgrade_pts)
                    score_data = dict(score_data)
                    score_data['total'] = new_total
                    score_data['sector_downgrade'] = {
                        'reason': f'板块共振：同板块{sell_count}只触发卖出，系统性风险-{abs(downgrade_pts)}分',
                        'sector': sector,
                        'sell_count': sell_count,
                        'original_total': orig_total,
                        'original_decision': orig_decision,
                    }
                    
                    # 决策可能改变
                    if new_total < 50 and decision != 'sell':
                        score_data['decision'] = 'sell'
                        score_data['sector_forced_sell'] = True
                    elif new_total < 75 and decision == 'hold':
                        score_data['decision'] = 'reduce'
                    
                    m = dict(m)
                    m['score'] = score_data
                
                adjusted.append(m)
        else:
            adjusted.extend(members)
    
    return resonance_report, adjusted


def format_resonance_report(resonance_report: Dict[str, int]) -> str:
    """格式化共振报告为文本"""
    if not resonance_report:
        return ''
    
    lines = ['\n─── 板块共振检测 ───']
    for sector, count in sorted(resonance_report.items(), key=lambda x: -x[1]):
        if count >= 2:
            lines.append(f'  ⚠️  {sector}: {count}只卖出 → 共振降级激活')
        elif count == 1:
            lines.append(f'  👁   {sector}: {count}只卖出 → 关注')
    return '\n'.join(lines)
