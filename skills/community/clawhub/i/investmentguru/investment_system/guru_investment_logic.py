#!/usr/bin/env python3
"""
AI投资大师系统 - 投资逻辑总结
基于ai-hedge-fund项目研究
"""

# ==================== 投资大师配置 ====================

GURUS_CONFIG = {
    "巴菲特": {
        "name_en": "Warren Buffett",
        "method": "合理价格买伟大公司",
        "core_metrics": ["ROE", "自由现金流", "毛利率", "PE"],
        "buy_criteria": "PE<25, ROE>15%, 毛利率>40%",
        "sell_criteria": "PE>40, 基本面恶化"
    },
    "彼得林奇": {
        "name_en": "Peter Lynch",
        "method": "寻找10倍股(GARP)",
        "core_metrics": ["PEG", "营收增长", "EPS增长"],
        "buy_criteria": "PEG<1, 营收增长>15%",
        "sell_criteria": "PEG>2, 增长放缓"
    },
    "木头姐": {
        "name_en": "Cathie Wood",
        "method": "创新颠覆",
        "core_metrics": ["创新指数", "TAM", "研发投入", "增速"],
        "buy_criteria": "创新颠覆、赛道够大",
        "sell_criteria": "创新放缓、估值泡沫"
    },
    "格雷厄姆": {
        "name_en": "Ben Graham",
        "method": "安全边际",
        "core_metrics": ["PE", "PB", "流动比率"],
        "buy_criteria": "PE<15, PB<1.5",
        "sell_criteria": "PE>20"
    },
    "芒格": {
        "name_en": "Charlie Munger",
        "method": "Wonderful Business",
        "core_metrics": ["商业模式", "护城河", "管理层"],
        "buy_criteria": "商业模式优秀、护城河宽",
        "sell_criteria": "商业模式变差"
    },
    "费雪": {
        "name_en": "Phil Fisher",
        "method": "成长股调研",
        "core_metrics": ["研发投入", "毛利率", "市场份额"],
        "buy_criteria": "研发>10%营收, 高成长",
        "sell_criteria": "成长放缓"
    },
    "伯里": {
        "name_en": "Michael Burry",
        "method": "深度价值+逆向",
        "core_metrics": ["隐蔽资产", "PB", "清算价值"],
        "buy_criteria": "隐蔽资产低估、困境反转",
        "sell_criteria": "估值修复"
    },
    "阿克曼": {
        "name_en": "Bill Ackman",
        "method": "激进投资",
        "core_metrics": ["催化剂", "估值修复空间"],
        "buy_criteria": "有催化剂、估值低估",
        "sell_criteria": "催化剂消失"
    },
    "索罗斯": {
        "name_en": "George Soros",
        "method": "宏观对冲",
        "core_metrics": ["宏观周期", "流动性", "政策"],
        "buy_criteria": "宏观拐点、流动性宽松",
        "sell_criteria": "趋势反转"
    },
    "达里奥": {
        "name_en": "Ray Dalio",
        "method": "全天候",
        "core_metrics": ["经济周期", "利率", "通胀"],
        "buy_criteria": "复苏初期、降息周期",
        "sell_criteria": "通胀上升、紧缩"
    },
    "达摩达兰": {
        "name_en": "Aswath Damodaran",
        "method": "DCF估值",
        "core_metrics": ["DCF", "EV/EBITDA", "相对估值"],
        "buy_criteria": "价格低于DCF 20%",
        "sell_criteria": "价格高于DCF"
    },
    "米勒": {
        "name_en": "Bill Miller",
        "method": "价值成长合一",
        "core_metrics": ["ROIC", "成长性", "估值"],
        "buy_criteria": "ROIC>15%, 成长好",
        "sell_criteria": "估值泡沫"
    },
    "邓普顿": {
        "name_en": "John Templeton",
        "method": "逆向投资",
        "core_metrics": ["PE", "PB", "VIX"],
        "buy_criteria": "极度悲观、PE历史低位",
        "sell_criteria": "PE历史高位"
    }
}

# ==================== 分析维度 ====================

DIMENSIONS_CONFIG = {
    "估值": {
        "metrics": ["PE", "PB", "PS", "EV/EBITDA", "DCF", "股息率"]
    },
    "基本面": {
        "metrics": ["ROE", "ROA", "毛利率", "净利率", "营收增长", "净利润增长"]
    },
    "技术面": {
        "metrics": ["MA5", "MA20", "MA60", "RSI", "MACD", "成交量"]
    },
    "情绪": {
        "metrics": ["新闻情绪", "机构评级", "资金流向", "VIX"]
    }
}


def get_guru_signal(guru_name: str, stock_data: dict) -> dict:
    """
    根据大师的投资逻辑判断信号
    """
    signal = "持有"
    reason = ""
    
    # 简化判断逻辑（实际需要完整数据）
    pe = stock_data.get('pe', 0)
    roe = stock_data.get('roe', 0)
    growth = stock_data.get('revenue_growth', 0)
    peg = stock_data.get('peg', 0)
    
    if guru_name == "巴菲特":
        if pe < 25 and roe > 15:
            signal = "买入"
            reason = f"PE={pe}<25, ROE={roe}%>15%"
        elif pe > 40:
            signal = "卖出"
            reason = f"PE={pe}>40，太贵"
        else:
            reason = f"PE={pe}，ROE={roe}%"
    
    elif guru_name == "彼得林奇":
        if peg < 1 and growth > 15:
            signal = "买入"
            reason = f"PEG={peg}<1, 增长{growth}%"
        elif peg > 2:
            signal = "卖出"
            reason = f"PEG={peg}>2，估值高"
        else:
            reason = f"PEG={peg}，增长{growth}%"
    
    elif guru_name == "木头姐":
        # 木头姐看创新和成长
        if growth > 30:
            signal = "买入"
            reason = f"高成长{growth}%，有创新潜力"
        else:
            reason = "需要更多创新数据"
    
    elif guru_name == "格雷厄姆":
        pb = stock_data.get('pb', 0)
        if pe < 15 and pb < 1.5:
            signal = "买入"
            reason = f"PE={pe}<15, PB={pb}<1.5"
        elif pe > 25:
            signal = "卖出"
            reason = f"PE={pe}>25"
        else:
            reason = f"PE={pe}, PB={pb}"
    
    # ... 其他大师逻辑
    
    return {"signal": signal, "reason": reason}


def generate_multi_guru_report(stock_name: str, stock_data: dict) -> str:
    """
    生成多大师验证报告
    """
    report = f"""
╔══════════════════════════════════════════════════════════════╗
║           📈 {stock_name} 多大师验证报告                    ║
╚══════════════════════════════════════════════════════════════╝

【基础数据】
  PE: {stock_data.get('pe', 'N/A')}
  ROE: {stock_data.get('roe', 'N/A')}%
  营收增长: {stock_data.get('revenue_growth', 'N/A')}%
  PEG: {stock_data.get('peg', 'N/A')}

【大师验证】
"""
    
    signals = []
    for guru_name in GURUS_CONFIG.keys():
        result = get_guru_signal(guru_name, stock_data)
        emoji = "✅" if result['signal'] == "买入" else "❌" if result['signal'] == "卖出" else "➡️"
        report += f"  {emoji} {guru_name}: {result['signal']} - {result['reason']}\n"
        
        if result['signal'] == "买入":
            signals.append(guru_name)
    
    # 统计
    buy_count = len(signals)
    total = len(GURUS_CONFIG)
    
    report += f"""
【综合结论】
  买入信号: {buy_count}/{total} 位大师
"""
    
    if buy_count >= total * 0.6:
        report += "  🚀 综合信号: 强烈买入\n"
    elif buy_count >= total * 0.4:
        report += "  ➡️ 综合信号: 持有观望\n"
    else:
        report += "  🛑 综合信号: 建议观望\n"
    
    return report


if __name__ == "__main__":
    print("=" * 60)
    print("🎓 AI投资大师系统 - 投资逻辑")
    print("=" * 60)
    print(f"\n已整合 {len(GURUS_CONFIG)} 位投资大师")
    print(f"已整合 {len(DIMENSIONS_CONFIG)} 个分析维度")
    
    print("\n📊 大师列表:")
    for name, info in GURUS_CONFIG.items():
        print(f"  • {name} ({info['name_en']})")
        print(f"    方法: {info['method']}")
    
    # 测试
    test_data = {
        'pe': 18,
        'roe': 22,
        'revenue_growth': 25,
        'peg': 0.72,
        'pb': 3.5
    }
    
    print("\n" + "=" * 60)
    print("📈 测试报告")
    print("=" * 60)
    print(generate_multi_guru_report("测试股票", test_data))