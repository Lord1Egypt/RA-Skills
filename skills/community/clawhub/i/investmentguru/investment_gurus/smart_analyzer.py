"""
投资大师综合分析器 - 第2步：整合实时数据 + 大师方法

功能：
1. 自动抓取股票实时数据
2. 结合7位大师的投资方法
3. 生成具体投资建议报告
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from investment_gurus.base import StockAnalysis
from investment_gurus.data_fetcher import StockDataFetcher, StockAnalyzer


class SmartGuruAnalyzer:
    """
    智能投资大师分析器
    
    自动抓取数据 + 大师方法 = 个性化投资建议
    
    Usage:
        analyzer = SmartGuruAnalyzer()
        
        # 用户问"茅台怎么样"
        report = analyzer.analyze("贵州茅台")
        
        # 指定大师方法
        report = analyzer.analyze("宁德时代", guru="张磊")
    """
    
    # 大师擅长领域
    GURU_EXPERTISE = {
        "duan": {
            "name": "段永平",
            "best_sectors": ["消费", "白酒", "互联网", "高端制造"],
            "key_focus": ["商业模式", "竞争壁垒", "管理层"],
            "valuation_method": "现金流折现+成长性",
        },
        "zhanglei": {
            "name": "张磊",
            "best_sectors": ["科技", "新能源", "医疗", "互联网"],
            "key_focus": ["长期增长", "企业家精神", "动态护城河"],
            "valuation_method": "长期主义+赛道空间",
        },
        "linyuan": {
            "name": "林园",
            "best_sectors": ["白酒", "医药", "食品饮料", "消费"],
            "key_focus": ["嘴巴经济", "垄断成瘾", "定价权"],
            "valuation_method": "垄断+成瘾性",
        },
        "danbing": {
            "name": "但斌",
            "best_sectors": ["消费", "互联网", "科技", "高端制造"],
            "key_focus": ["伟大企业", "长期持有", "时间玫瑰"],
            "valuation_method": "伟大企业+长期",
        },
        "qiuguoluo": {
            "name": "邱国鹭",
            "best_sectors": ["金融", "地产", "周期股", "消费"],
            "key_focus": ["三好原则", "逆向投资", "估值"],
            "valuation_method": "好行业+好公司+好价格",
        },
        "wangguobin": {
            "name": "王国斌",
            "best_sectors": ["消费", "科技", "先进制造"],
            "key_focus": ["幸运的行业", "能干的企业", "合理价格"],
            "valuation_method": "行业+企业+价格",
        },
        "lilu": {
            "name": "李录",
            "best_sectors": ["消费", "科技", "金融"],
            "key_focus": ["安全边际", "跨市场", "文明视角"],
            "valuation_method": "极度安全边际",
        },
    }
    
    def __init__(self):
        self.data_fetcher = StockDataFetcher()
        self.stock_analyzer = StockAnalyzer()
    
    def analyze(
        self, 
        stock: str, 
        guru: str = "auto",
        verbose: bool = True
    ) -> str:
        """
        完整分析股票
        
        Args:
            stock: 股票名称/代码
            guru: 指定大师方法 ("auto"=自动匹配)
            verbose: 是否输出详细报告
            
        Returns:
            str: 完整分析报告
        """
        # 1. 抓取实时数据
        data = self._fetch_data(stock)
        
        # 2. 自动匹配最合适的大师
        if guru == "auto":
            guru = self._match_guru(data)
        
        # 3. 生成分析报告
        report = self._generate_report(stock, data, guru, verbose)
        
        return report
    
    def _fetch_data(self, stock: str) -> Dict:
        """抓取股票数据"""
        return self.stock_analyzer.full_analysis(stock)
    
    def _match_guru(self, data: Dict) -> str:
        """
        根据股票行业/特性自动匹配最合适的大师
        
        Returns:
            str: 大师名称 (duan/linyuan/zhanglei等)
        """
        sector = data.get("sector", {}).get("sector", "")
        quote = data.get("quote", {})
        trend = data.get("trend", {})
        
        # 根据行业匹配
        sector_guru_map = {
            "Consumer Defensive": "linyuan",  # 消费 -> 林园
            "Consumer Cyclical": "linyuan",   # 消费周期 -> 林园
            "Healthcare": "linyuan",          # 医药 -> 林园
            "Technology": "zhanglei",         # 科技 -> 张磊
            "Communication Services": "danbing",  # 互联网 -> 但斌
            "Consumer Goods": "duan",         # 消费品 -> 段永平
            "Financial": "qiuguoluo",         # 金融 -> 邱国鹭
            "Basic Materials": "qiuguoluo",   # 原材料 -> 邱国鹭
            "Energy": "zhanglei",             # 能源 -> 张磊
        }
        
        matched = sector_guru_map.get(sector, "duan")  # 默认段永平
        
        # 根据走势调整
        trend_type = trend.get("trend", "sideways")
        change_1m = trend.get("change_1m", 0)
        
        # 如果涨幅太大（>30%），谨慎推荐
        if change_1m > 30:
            matched = "lilu"  # 用李录的安全边际方法
        
        return matched
    
    def _generate_report(
        self, 
        stock: str, 
        data: Dict, 
        guru: str,
        verbose: bool = True
    ) -> str:
        """生成分析报告"""
        
        quote = data.get("quote", {})
        trend = data.get("trend", {})
        ma = data.get("ma", {})
        sector = data.get("sector", {})
        market = data.get("market", {})
        
        guru_info = self.GURU_EXPERTISE.get(guru, self.GURU_EXPERTISE["duan"])
        guru_name = guru_info["name"]
        
        # 构建报告
        lines = []
        lines.append("=" * 50)
        lines.append(f"📊 {stock} - {guru_name}式投资分析")
        lines.append("=" * 50)
        
        # === 1. 实时数据 ===
        lines.append("\n📈 【实时行情】")
        price = quote.get("price", "N/A")
        change_pct = quote.get("change_pct", 0)
        change_str = f"+{change_pct}%" if change_pct > 0 else f"{change_pct}%"
        lines.append(f"  当前价: {price}元 ({change_str})")
        
        pe = quote.get("pe")
        if pe:
            pe_str = f"{pe:.1f}" if pe else "N/A"
            lines.append(f"  PE估值: {pe_str}")
        
        market_cap = quote.get("market_cap")
        if market_cap:
            if market_cap > 1e12:
                lines.append(f"  市值: {market_cap/1e12:.1f}万亿")
            elif market_cap > 1e11:
                lines.append(f"  市值: {market_cap/1e11:.1f}千亿")
        
        # === 2. 近期走势 ===
        lines.append("\n📉 【近期走势】")
        trend_val = trend.get("trend", "震荡")
        trend_emoji = {"up": "📈", "down": "📉", "sideways": "➡️"}.get(trend_val, "➡️")
        lines.append(f"  趋势: {trend_emoji} {trend_val}")
        
        change_5d = trend.get("change_5d", 0)
        change_1m = trend.get("change_1m", 0)
        change_3m = trend.get("change_3m", 0)
        
        lines.append(f"  5日: {self._fmt_pct(change_5d)}")
        lines.append(f"  1月: {self._fmt_pct(change_1m)}")
        lines.append(f"  3月: {self._fmt_pct(change_3m)}")
        
        # === 3. 均线位置 ===
        if ma:
            lines.append("\n📊 【均线位置】")
            current = ma.get("current_price", 0)
            ma5 = ma.get("MA5", 0)
            ma10 = ma.get("MA10", 0)
            ma20 = ma.get("MA20", 0)
            ma60 = ma.get("MA60", 0)
            
            # 判断均线多头/空头
            if ma5 > ma20 > ma60:
                ma_signal = "多头排列 🔼"
            elif ma5 < ma20 < ma60:
                ma_signal = "空头排列 🔽"
            else:
                ma_signal = "震荡整理 ➡️"
            
            lines.append(f"  {ma_signal}")
            lines.append(f"  当前: {current} / MA5: {ma5} / MA20: {ma20}")
        
        # === 4. 板块信息 ===
        lines.append("\n🏭 【板块信息】")
        sector_name = sector.get("sector", "未知")
        industry = sector.get("industry", "未知")
        lines.append(f"  行业: {sector_name}")
        lines.append(f"  细分: {industry}")
        
        # === 5. 大师方法分析 ===
        lines.append(f"\n🧠 【{guru_name}分析】")
        lines.append(f"  核心理念: {', '.join(guru_info['key_focus'])}")
        
        # 根据不同大师给出不同角度的分析
        analysis = self._guru_specific_analysis(stock, data, guru)
        lines.append(f"\n  {analysis}")
        
        # === 6. 综合建议 ===
        lines.append("\n" + "=" * 50)
        recommendation = self._generate_recommendation(stock, data, guru)
        lines.append(f"💡 【综合建议】")
        lines.append(f"  {recommendation}")
        lines.append("=" * 50)
        
        return "\n".join(lines)
    
    def _fmt_pct(self, v: float) -> str:
        """格式化涨跌幅"""
        if v is None or v == 0:
            return "0.00%"
        sign = "+" if v > 0 else ""
        return f"{sign}{v:.2f}%"
    
    def _guru_specific_analysis(self, stock: str, data: Dict, guru: str) -> str:
        """大师特定分析"""
        quote = data.get("quote", {})
        trend = data.get("trend", {})
        ma = data.get("ma", {})
        
        price = quote.get("price", 0)
        pe = quote.get("pe")
        trend_val = trend.get("trend", "sideways")
        
        if guru == "duan":  # 段永平
            # 看重商业模式和竞争力
            return f"从段永平视角：当前价格{price}元，PE={pe}。关键是是否看懂商业模式、是否有竞争壁垒。是否在能力圈内？"
        
        elif guru == "linyuan":  # 林园
            # 看重嘴巴经济和垄断
            return f"从林园视角：是否与嘴巴相关？是否有垄断地位/成瘾性？当前趋势{trend_val}，符合'长期持有'条件吗？"
        
        elif guru == "zhanglei":  # 张磊
            # 看重长期增长和企业家
            return f"从张磊视角：是否有10年增长空间？企业家是否靠谱？是否是'幸运的行业+能干的企业'？"
        
        elif guru == "danbing":  # 但斌
            # 看重伟大企业
            return f"从但斌视角：是否是'世界改变不了的公司'？能否持有5-10年？时间是否是朋友？"
        
        elif guru == "qiuguoluo":  # 邱国鹭
            # 看重三好原则
            return f"从邱国鹭视角：好行业+好公司+好价格？当前是否足够'好价格'？"
        
        elif guru == "lilu":  # 李录
            # 看重安全边际
            return f"从李录视角：是否有足够安全边际？能否承受50%下跌？是否'宁可错过不要买贵'？"
        
        else:
            return f"基于{guru}方法分析：综合考量估值、成长性、竞争力。"
    
    def _generate_recommendation(self, stock: str, data: Dict, guru: str) -> str:
        """生成综合建议"""
        quote = data.get("quote", {})
        trend = data.get("trend", {})
        ma = data.get("ma", {})
        
        price = quote.get("price", 0)
        pe = quote.get("pe")
        trend_val = trend.get("trend", "sideways")
        change_1m = trend.get("change_1m", 0)
        
        # 简单判断逻辑
        reasons = []
        action = "持有观察"
        
        # 趋势判断
        if trend_val == "up":
            reasons.append("趋势向上")
            if change_1m < 15:
                action = "可以买入"
        
        # 估值判断
        if pe:
            if pe < 20:
                reasons.append(f"PE={pe:.1f}，估值合理")
            elif pe > 50:
                reasons.append(f"PE={pe:.1f}，估值偏高")
                action = "谨慎买入"
        
        # 短期涨幅
        if change_1m > 30:
            reasons.append(f"近1月涨{change_1m:.1f}%，短期涨幅大")
            action = "建议观望"
        
        if not reasons:
            reasons.append("需要更多数据")
        
        return f"{action}（{', '.join(reasons)}）"
    
    def compare_methods(self, stock: str) -> str:
        """
        对比所有大师的方法
        
        一次分析，展现7位大师的不同视角
        """
        data = self._fetch_data(stock)
        
        lines = []
        lines.append("=" * 60)
        lines.append(f"🔍 {stock} - 七大师多维分析")
        lines.append("=" * 60)
        
        quote = data.get("quote", {})
        lines.append(f"\n当前价: {quote.get('price')}元，PE: {quote.get('pe')}")
        
        # 7位大师逐一分析
        for guru_key, guru_info in self.GURU_EXPERTISE.items():
            lines.append(f"\n--- {guru_info['name']}: ---")
            lines.append(f"  擅长: {', '.join(guru_info['best_sectors'][:3])}")
            lines.append(f"  重点: {', '.join(guru_info['key_focus'])}")
            
            # 简短点评
            analysis = self._guru_specific_analysis(stock, data, guru_key)
            lines.append(f"  观点: {analysis[:50]}...")
        
        lines.append("\n" + "=" * 60)
        
        return "\n".join(lines)


# === 便捷函数 ===

def smart_analyze(stock: str, guru: str = "auto") -> str:
    """
    智能分析股票（自动抓取数据 + 大师方法）
    
    Example:
        report = smart_analyze("贵州茅台")
        print(report)
    """
    analyzer = SmartGuruAnalyzer()
    return analyzer.analyze(stock, guru=guru)


def compare_all_methods(stock: str) -> str:
    """
    对比所有大师方法
    """
    analyzer = SmartGuruAnalyzer()
    return analyzer.compare_methods(stock)


if __name__ == "__main__":
    # 测试
    print(smart_analyze("贵州茅台"))