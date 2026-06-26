#!/usr/bin/env python3
"""
国际投资大师模块
基于 ai-hedge-fund 项目研究 (55,797 Stars)

包含13位国际投资大师的投资逻辑和分析方法
"""

from typing import Dict, Optional, List
import random


# ==================== 投资大师配置 ====================

INTERNATIONAL_GURUS = {
    "巴菲特": {
        "name_en": "Warren Buffett",
        "method": "合理价格买伟大公司 (Wonderful Business at Fair Price)",
        "core_principles": [
            "买自己能理解的简单生意",
            "护城河要宽且可持续",
            "管理层要诚实有能力",
            "ROE > 15%",
            "自由现金流充裕",
            "长期持有"
        ],
        "metrics": ["ROE", "自由现金流", "毛利率", "净利率", "资产负债率"],
        "buy_criteria": "PE < 25, ROE > 15%, 毛利率 > 40%, 护城河明显",
        "sell_criteria": "PE > 40, 基本面恶化, 找到更好标的"
    },
    
    "彼得林奇": {
        "name_en": "Peter Lynch",
        "method": "寻找10倍股 (GARP - Growth at Reasonable Price)",
        "core_principles": [
            "投资你了解的",
            "PEG < 1",
            "找营收和EPS持续增长的公司",
            "留意隐蔽的成长股",
            "10倍股来自日常可接触的公司"
        ],
        "metrics": ["PEG", "营收增长率", "EPS增长率", "毛利率", "存货周转"],
        "buy_criteria": "PEG < 1, 营收增长 > 15%, 稳定盈利",
        "sell_criteria": "PEG > 2, 增长放缓, 估值太高"
    },
    
    "木头姐": {
        "name_en": "Cathie Wood",
        "method": "创新颠覆 (Innovation & Disruption)",
        "core_principles": [
            "寻找颠覆性创新",
            "看长期5年+的赛道",
            "不在意短期估值",
            "看创始人和团队",
            "赢家通吃"
        ],
        "metrics": ["创新指数", "TAM(潜在市场)", "研发投入", "增速", "市场地位"],
        "buy_criteria": "创新足够颠覆、赛道够大、团队优秀",
        "sell_criteria": "创新放缓、竞争加剧、估值泡沫"
    },
    
    "格雷厄姆": {
        "name_en": "Ben Graham",
        "method": "价值投资 + 安全边际",
        "core_principles": [
            "安全边际",
            "买烟蒂股",
            "Net Current Assets > 市值",
            "PE < 15",
            "分散投资"
        ],
        "metrics": ["PE", "PB", "Net Current Assets", "流动比率", "股息率"],
        "buy_criteria": "PE < 15, PB < 1.5, NCAV > 市值2/3",
        "sell_criteria": "PE > 20, 达到目标价"
    },
    
    "芒格": {
        "name_en": "Charlie Munger",
        "method": "买Wonderful Business at Fair Price",
        "core_principles": [
            "买伟大的公司",
            "等待合理价格",
            "逆向思维",
            "多学科思维模型",
            "避免愚蠢"
        ],
        "metrics": ["商业模式", "竞争优势", "管理层", "定价权"],
        "buy_criteria": "商业模式优秀、可持续竞争优势、合理价格",
        "sell_criteria": "商业模式变差、价格太贵"
    },
    
    "费雪": {
        "name_en": "Phil Fisher",
        "method": "成长股投资 (Scuttlebutt)",
        "core_principles": [
            "深入调研(scuttlebutt)",
            "买成长股",
            "关注研发和营销",
            "长期持有",
            "不要频繁交易"
        ],
        "metrics": ["研发投入占比", "毛利率", "营收增长", "市场份额", "产品管线"],
        "buy_criteria": "研发 > 10%营收、高成长、管理层优秀",
        "sell_criteria": "成长放缓、管理层变动"
    },
    
    "伯里": {
        "name_en": "Michael Burry",
        "method": "深度价值 + 逆向",
        "core_principles": [
            "寻找深度价值",
            "逆境反转",
            "隐蔽资产",
            "不受市场关注",
            "独立思考"
        ],
        "metrics": ["隐蔽资产", "PB", "现金流", "债务结构", "清算价值"],
        "buy_criteria": "隐蔽资产被低估、破产风险低、困境有望反转",
        "sell_criteria": "估值修复、风险加大"
    },
    
    "阿克曼": {
        "name_en": "Bill Ackman",
        "method": "激进投资 (Activist)",
        "core_principles": [
            "深入研究",
            "下重注",
            "推动变革",
            "催化剂",
            "长期持有"
        ],
        "metrics": ["催化剂", "估值修复空间", "管理层", "股权结构"],
        "buy_criteria": "有明确催化剂、估值严重低估、管理层可推动变革",
        "sell_criteria": "催化剂消失、估值合理"
    },
    
    "索罗斯": {
        "name_en": "George Soros",
        "method": "宏观对冲 + 反身性",
        "core_principles": [
            "看宏观经济",
            "反身性理论",
            "敢于下重注",
            "止损要快",
            "不对称风险"
        ],
        "metrics": ["宏观周期", "流动性", "政策变化", "市场情绪"],
        "buy_criteria": "宏观拐点、流动性宽松、政策利好",
        "sell_criteria": "趋势反转、流动性收紧"
    },
    
    "达里奥": {
        "name_en": "Ray Dalio",
        "method": "全天候 + 风险平价",
        "core_principles": [
            "分散配置",
            "跟着央行走",
            "债务周期",
            "风险平价",
            "不要和央行对抗"
        ],
        "metrics": ["利率", "通胀", "经济增长", "资产负债表"],
        "buy_criteria": "经济复苏初期、降息周期、债券上涨",
        "sell_criteria": "通胀上升、紧缩周期"
    },
    
    "达摩达兰": {
        "name_en": "Aswath Damodaran",
        "method": "估值专家 (DCF + 相对估值)",
        "core_principles": [
            "DCF估值是核心",
            "相对估值作参考",
            "增长预期要合理",
            "风险调整很重要",
            "不要迷信单一指标"
        ],
        "metrics": ["DCF估值", "EV/EBITDA", "PE", "PB", "增长预期"],
        "buy_criteria": "当前价格低于DCF估值20%以上",
        "sell_criteria": "当前价格高于DCF估值"
    },
    
    "米勒": {
        "name_en": "Bill Miller",
        "method": "价值成长合一",
        "core_principles": [
            "价值+成长不矛盾",
            "寻找不对称机会",
            "长期持有优质股",
            "相信自己的研究",
            "不要频繁交易"
        ],
        "metrics": ["ROIC", "成长性", "估值", "自由现金流"],
        "buy_criteria": "ROIC > 15%、成长好、估值合理",
        "sell_criteria": "估值泡沫、基本面恶化"
    },
    
    "邓普顿": {
        "name_en": "John Templeton",
        "method": "逆向投资",
        "core_principles": [
            "在悲观时买入",
            "极度悲观=极度机会",
            "全球分散投资",
            "长期投资",
            "便宜是硬道理"
        ],
        "metrics": ["PE", "PB", "股息率", "市场情绪", "VIX"],
        "buy_criteria": "极度悲观、PE历史低位、恐慌指数高",
        "sell_criteria": "乐观情绪、PE历史高位"
    }
}


# ==================== 分析维度 ====================

ANALYSIS_DIMENSIONS = {
    "估值": {
        "name": "Valuation Agent",
        "metrics": ["PE", "PB", "PS", "EV/EBITDA", "DCF", "股息率"],
        "description": "计算股票的内在价值"
    },
    "基本面": {
        "name": "Fundamentals Agent",
        "metrics": ["ROE", "ROA", "毛利率", "净利率", "营收增长", "净利润增长", "资产负债率"],
        "description": "分析公司财务健康状况"
    },
    "技术面": {
        "name": "Technical Agent",
        "metrics": ["MA5", "MA20", "MA60", "RSI", "MACD", "布林带", "成交量"],
        "description": "分析价格走势和趋势"
    },
    "情绪": {
        "name": "Sentiment Agent",
        "metrics": ["新闻情绪", "机构评级", "资金流向", "VIX", "期权仓位"],
        "description": "分析市场情绪和资金动向"
    }
}


# ==================== 核心分析函数 ====================

def get_guru_info(guru_name: str) -> Optional[Dict]:
    """获取大师信息"""
    return INTERNATIONAL_GURUS.get(guru_name)


def get_all_gurus() -> List[str]:
    """获取所有大师列表"""
    return list(INTERNATIONAL_GURUS.keys())


def analyze_guru_signal(guru_name: str, stock_data: Dict) -> Dict:
    """
    根据大师的投资逻辑判断信号
    
    Args:
        guru_name: 大师名称
        stock_data: 股票数据，包含 pe, roe, revenue_growth, peg, pb 等
    
    Returns:
        {"signal": "买入/持有/卖出", "reason": "原因", "confidence": 置信度}
    """
    
    signal = "持有"
    reason = "数据不足"
    confidence = 50
    
    # 提取数据（转换为百分比格式）
    pe = stock_data.get('pe', 0)
    roe = stock_data.get('roe', 0)
    # 统一转换为百分比形式 (0.18 -> 18)
    if roe and roe < 1:
        roe_pct = roe * 100
    else:
        roe_pct = roe
    
    growth = stock_data.get('revenue_growth', 0)
    # 统一转换为百分比形式
    if growth and growth < 1:
        growth_pct = growth * 100
    else:
        growth_pct = growth
    
    peg = stock_data.get('peg', 0)
    pb = stock_data.get('pb', 0)
    gross_margin = stock_data.get('gross_margin', 0)
    # 统一转换为百分比形式
    if gross_margin and gross_margin < 1:
        gross_margin_pct = gross_margin * 100
    else:
        gross_margin_pct = gross_margin
    
    fcf = stock_data.get('fcf', 0)  # 自由现金流
    
    if guru_name == "巴菲特":
        # 巴菲特：PE < 25, ROE > 15%, 毛利率 > 40%
        if pe > 0 and pe < 25 and roe_pct > 15:
            signal = "买入"
            reason = f"PE={pe}<25, ROE={roe_pct:.1f}%>15%"
            confidence = 85
        elif pe > 40:
            signal = "卖出"
            reason = f"PE={pe}>40，太贵"
            confidence = 80
        else:
            reason = f"PE={pe}, ROE={roe_pct:.1f}%"
    
    elif guru_name == "彼得林奇":
        # 彼得林奇：PEG < 1, 营收增长 > 15%
        if peg is not None and peg > 0 and peg < 1 and growth_pct > 15:
            signal = "买入"
            reason = f"PEG={peg:.2f}<1, 增长{growth_pct:.1f}%"
            confidence = 80
        elif peg is not None and peg > 2:
            signal = "卖出"
            reason = f"PEG={peg}>2，估值高"
            confidence = 75
        elif peg is not None and peg > 0 and peg < 1:
            reason = f"PEG={peg:.2f}合理, 增长{growth_pct:.1f}%"
        else:
            reason = f"PEG={peg if peg else 'N/A'}, 增长{growth_pct:.1f}%"
    
    elif guru_name == "木头姐":
        # 木头姐：看高成长和创新
        if growth_pct is not None and growth_pct > 30:
            signal = "买入"
            reason = f"高成长{growth_pct:.1f}%，有创新潜力"
            confidence = 75
        elif growth_pct is not None and growth_pct < 10:
            signal = "持有"
            reason = "成长性不足"
            confidence = 60
        else:
            reason = f"增长{growth_pct if growth_pct else 0}%，需观察创新"
    
    elif guru_name == "格雷厄姆":
        # 格雷厄姆：PE < 15, PB < 1.5
        if pe > 0 and pe < 15 and pb < 1.5:
            signal = "买入"
            reason = f"PE={pe}<15, PB={pb}<1.5"
            confidence = 85
        elif pe > 25:
            signal = "卖出"
            reason = f"PE={pe}>25"
            confidence = 80
        else:
            reason = f"PE={pe}, PB={pb}"
    
    elif guru_name == "芒格":
        # 芒格：看商业模式（简化判断）
        if pe > 0 and pe < 30 and roe_pct > 12:
            signal = "买入"
            reason = f"PE={pe}<30, ROE={roe_pct:.1f}%>12%"
            confidence = 75
        else:
            reason = f"需更多商业模式数据"
    
    elif guru_name == "费雪":
        # 费雪：研发投入 > 10%
        rd_ratio = stock_data.get('rd_ratio', 0)
        if rd_ratio > 10 and growth > 15:
            signal = "买入"
            reason = f"研发{rd_ratio}%>10%, 增长{growth}%"
            confidence = 80
        else:
            reason = f"研发{rd_ratio}%, 增长{growth}%"
    
    elif guru_name == "伯里":
        # 伯里：深度价值，PB < 1
        if pb < 1:
            signal = "买入"
            reason = f"PB={pb}<1，深度价值"
            confidence = 80
        elif pb > 3:
            signal = "卖出"
            reason = f"PB={pb}>3，估值高"
            confidence = 70
        else:
            reason = f"PB={pb}"
    
    elif guru_name == "阿克曼":
        # 阿克曼：看催化剂
        catalyst = stock_data.get('catalyst', '')
        if catalyst:
            signal = "买入"
            reason = f"有催化剂: {catalyst}"
            confidence = 75
        else:
            reason = "需催化剂信息"
    
    elif guru_name == "索罗斯":
        # 索罗斯：宏观判断
        macro = stock_data.get('macro', 'neutral')
        if macro == 'easing':
            signal = "买入"
            reason = "流动性宽松周期"
            confidence = 70
        elif macro == 'tightening':
            signal = "卖出"
            reason = "流动性收紧"
            confidence = 70
        else:
            reason = "宏观中性"
    
    elif guru_name == "达里奥":
        # 达里奥：经济周期
        cycle = stock_data.get('cycle', 'neutral')
        if cycle == 'recovery':
            signal = "买入"
            reason = "经济复苏初期"
            confidence = 70
        elif cycle == 'inflation':
            signal = "卖出"
            reason = "通胀上升期"
            confidence = 70
        else:
            reason = "周期中性"
    
    elif guru_name == "达摩达兰":
        # 达摩达兰：DCF估值
        dcf = stock_data.get('dcf_price', 0)
        current = stock_data.get('price', 0)
        if dcf > 0 and current > 0:
            margin = (dcf - current) / current * 100
            if margin > 20:
                signal = "买入"
                reason = f"当前{dcf/current*100:.0f}%低于DCF估值"
                confidence = 80
            elif margin < -20:
                signal = "卖出"
                reason = f"当前价格高于DCF估值{-margin:.0f}%"
                confidence = 75
            else:
                reason = f"接近DCF估值"
        else:
            reason = "需DCF估值数据"
    
    elif guru_name == "米勒":
        # 米勒：ROIC > 15%
        roic = stock_data.get('roic', 0)
        if roic > 15 and growth > 10:
            signal = "买入"
            reason = f"ROIC={roic}%>15%, 增长{growth}%"
            confidence = 80
        elif roic < 5:
            signal = "卖出"
            reason = f"ROIC={roic}%太低"
            confidence = 70
        else:
            reason = f"ROIC={roic}%, 增长{growth}%"
    
    elif guru_name == "邓普顿":
        # 邓普顿：逆向投资
        vix = stock_data.get('vix', 0)
        if vix > 30:
            signal = "买入"
            reason = f"VIX={vix}>30，极度恐慌"
            confidence = 75
        elif vix < 15:
            signal = "卖出"
            reason = f"VIX={vix}<15，市场乐观"
            confidence = 70
        else:
            reason = f"VIX={vix}"
    
    return {"signal": signal, "reason": reason, "confidence": confidence}


def generate_multi_guru_report(stock_name: str, stock_data: Dict) -> str:
    """
    生成多大师验证报告
    
    Args:
        stock_name: 股票名称
        stock_data: 股票数据
    
    Returns:
        多大师验证报告字符串
    """
    report = f"""
╔══════════════════════════════════════════════════════════════════╗
║              📈 {stock_name} 多大师验证报告                      ║
╚══════════════════════════════════════════════════════════════════╝

【基础数据】
  PE: {stock_data.get('pe', 'N/A')}
  ROE: {stock_data.get('roe', 'N/A')}%
  营收增长: {stock_data.get('revenue_growth', 'N/A')}%
  PEG: {stock_data.get('peg', 'N/A')}
  PB: {stock_data.get('pb', 'N/A')}
  毛利率: {stock_data.get('gross_margin', 'N/A')}%

【多大师验证】
"""
    
    # 收集所有大师信号
    buy_count = 0
    sell_count = 0
    hold_count = 0
    signals = []
    
    for guru_name in INTERNATIONAL_GURUS.keys():
        result = analyze_guru_signal(guru_name, stock_data)
        
        emoji = "✅" if result['signal'] == "买入" else "❌" if result['signal'] == "卖出" else "➡️"
        report += f"  {emoji} {guru_name}: {result['signal']} - {result['reason']}\n"
        
        if result['signal'] == "买入":
            buy_count += 1
            signals.append(guru_name)
        elif result['signal'] == "卖出":
            sell_count += 1
        else:
            hold_count += 1
    
    # 统计
    total = len(INTERNATIONAL_GURUS)
    buy_ratio = buy_count / total * 100
    
    # 综合结论
    if buy_count >= total * 0.6:
        final_signal = "🚀 强烈买入"
        final_action = "分批建仓，把握机会"
    elif buy_count >= total * 0.4:
        final_signal = "➡️ 持有/轻度买入"
        final_action = "观望为主，谨慎操作"
    elif sell_count >= total * 0.5:
        final_signal = "🛑 建议卖出"
        final_action = "减仓或清仓，规避风险"
    else:
        final_signal = "➡️ 持有观望"
        final_action = "继续持有，等待更明确信号"
    
    report += f"""
【综合统计】
  买入: {buy_count}/{total} ({buy_ratio:.0f}%)
  持有: {hold_count}/{total}
  卖出: {sell_count}/{total}

【综合结论】
  信号: {final_signal}
  行动: {final_action}
  
  {f"买入的大师: {', '.join(signals)}" if signals else ""}
"""
    
    return report


def analyze_stock_international(stock_name: str, stock_data: Dict) -> Dict:
    """
    综合分析股票（国际大师视角）
    
    Args:
        stock_name: 股票名称
        stock_data: 股票数据
    
    Returns:
        分析结果字典
    """
    buy_count = 0
    all_signals = {}
    
    for guru_name in INTERNATIONAL_GURUS.keys():
        result = analyze_guru_signal(guru_name, stock_data)
        all_signals[guru_name] = result
        if result['signal'] == "买入":
            buy_count += 1
    
    total = len(INTERNATIONAL_GURUS)
    
    return {
        "stock_name": stock_name,
        "stock_data": stock_data,
        "signals": all_signals,
        "buy_count": buy_count,
        "total": total,
        "buy_ratio": buy_count / total,
        "final_signal": "买入" if buy_count >= total * 0.5 else "持有" if buy_count >= total * 0.3 else "卖出"
    }


# ==================== 测试 ====================

if __name__ == "__main__":
    print("=" * 70)
    print("🎓 国际投资大师系统 - 测试")
    print("=" * 70)
    print(f"\n已整合 {len(INTERNATIONAL_GURUS)} 位国际大师")
    print(f"已整合 {len(ANALYSIS_DIMENSIONS)} 个分析维度")
    
    # 测试数据
    test_data = {
        'pe': 18,
        'roe': 22,
        'revenue_growth': 25,
        'peg': 0.72,
        'pb': 3.5,
        'gross_margin': 45,
        'roic': 18,
        'vix': 16
    }
    
    print("\n" + "=" * 70)
    print("📈 测试报告")
    print("=" * 70)
    print(generate_multi_guru_report("测试股票", test_data))