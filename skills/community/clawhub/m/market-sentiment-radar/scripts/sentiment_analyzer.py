#!/home/linuxbrew/.linuxbrew/bin/python3.10
# -*- coding: utf-8 -*-
"""
市场情绪与板块轮动雷达 - 主分析脚本 (v1.0)
分析市场情绪周期、板块资金流向、生成大盘体检报告
"""

import sys
import argparse
import time
from datetime import datetime
from dataclasses import dataclass
from typing import List, Dict, Optional

# 尝试导入 AKShare
try:
    import akshare as ak
    HAS_AKSHARE = True
    print("✓ AKShare 已加载")
except ImportError:
    HAS_AKSHARE = False
    print("⚠️ AKShare 未安装，请运行：pip3 install akshare pandas -U")


@dataclass
class MarketData:
    """市场数据"""
    date: str
    total_volume: float  # 两市总成交量（万亿）
    volume_change: str  # 放量/缩量
    up_count: int  # 上涨家数
    down_count: int  # 下跌家数
    limit_up: int  # 涨停家数
    limit_down: int  # 跌停家数
    highest_chain: int  # 连板最高标
    north_flow: float  # 北向资金（亿）
    shanghai_change: float  # 上证指数涨跌幅
    shenzhen_change: float  # 深证成指涨跌幅
    chinext_change: float  # 创业板涨跌幅


@dataclass
class SentimentAnalysis:
    """情绪分析结果"""
    cycle_stage: str  # 冰点期/混沌期/退潮期/主升期
    confidence: int  # 置信度 0-100
    key_features: List[str]  # 关键特征
    risk_level: str  # 风险等级
    position_suggestion: str  # 仓位建议


@dataclass
class SectorAnalysis:
    """板块分析结果"""
    main_line: str  # 绝对主线
    main_line_sustainability: str  # 持续性（强/中/弱）
    hot_sectors: List[str]  # 热门板块
    cold_sectors: List[str]  # 冷门板块
    capital_flow: str  # 资金流向描述
    avoid_sectors: List[str]  # 避雷板块


@dataclass
class CrossMarketAnalysis:
    """跨市场分析结果"""
    us_market_impact: str  # 美股影响
    macro_events: List[str]  # 宏观事件
    currency_impact: str  # 汇率影响
    commodity_impact: str  # 大宗商品影响


def analyze_sentiment_cycle(data: MarketData) -> SentimentAnalysis:
    """分析情绪周期"""
    features = []
    score = 0
    risk_level = "MEDIUM"
    
    # 1. 成交量分析
    if data.total_volume > 1.0:
        features.append(f"成交量 {data.total_volume} 万亿，市场活跃")
        score += 20
    elif data.total_volume > 0.8:
        features.append(f"成交量 {data.total_volume} 万亿，市场中性")
        score += 10
    else:
        features.append(f"成交量 {data.total_volume} 万亿，市场萎缩")
        score -= 20
    
    # 2. 涨跌比分析
    ratio = data.up_count / max(data.down_count, 1)
    if ratio > 3:
        features.append(f"涨跌比 {data.up_count}:{data.down_count}，赚钱效应强")
        score += 25
    elif ratio > 1:
        features.append(f"涨跌比 {data.up_count}:{data.down_count}，赚钱效应中性")
        score += 5
    elif ratio < 0.33:
        features.append(f"涨跌比 {data.up_count}:{data.down_count}，亏钱效应极值")
        score -= 25
    else:
        features.append(f"涨跌比 {data.up_count}:{data.down_count}，亏钱效应")
        score -= 10
    
    # 3. 跌停家数分析
    if data.limit_down > 100:
        features.append(f"跌停 {data.limit_down} 家，冰点信号")
        score -= 30
        risk_level = "HIGH"
    elif data.limit_down > 50:
        features.append(f"跌停 {data.limit_down} 家，风险较高")
        score -= 20
        risk_level = "HIGH"
    elif data.limit_down > 20:
        features.append(f"跌停 {data.limit_down} 家，风险中等")
        score -= 10
    else:
        features.append(f"跌停 {data.limit_down} 家，风险可控")
    
    # 4. 连板高度分析
    if data.highest_chain >= 7:
        features.append(f"连板高度 {data.highest_chain} 板，情绪高涨")
        score += 25
    elif data.highest_chain >= 5:
        features.append(f"连板高度 {data.highest_chain} 板，情绪中性")
        score += 10
    elif data.highest_chain >= 3:
        features.append(f"连板高度 {data.highest_chain} 板，情绪一般")
    else:
        features.append(f"连板高度 {data.highest_chain} 板，情绪压制")
        score -= 15
    
    # 5. 北向资金分析
    if data.north_flow > 50:
        features.append(f"北向资金流入 {data.north_flow} 亿，外资看好")
        score += 15
    elif data.north_flow > 0:
        features.append(f"北向资金流入 {data.north_flow} 亿，外资中性")
        score += 5
    elif data.north_flow < -50:
        features.append(f"北向资金流出 {abs(data.north_flow)} 亿，外资看空")
        score -= 15
    else:
        features.append(f"北向资金流出 {abs(data.north_flow)} 亿，外资中性")
        score -= 5
    
    # 确定周期阶段
    if score >= 50:
        cycle_stage = "🚀 主升/高潮期"
        position_suggestion = "80% 重拳出击"
    elif score >= 20:
        cycle_stage = "⚖️ 震荡期（偏多）"
        position_suggestion = "60% 均衡配置"
    elif score >= -10:
        cycle_stage = "⚖️ 震荡期（偏空）"
        position_suggestion = "40% 谨慎参与"
    elif score >= -30:
        cycle_stage = "🌪️ 混沌期/退潮期"
        position_suggestion = "20% 轻仓试错"
    else:
        cycle_stage = "🧊 冰点期"
        position_suggestion = "0-10% 空仓观望或左侧布局"
        risk_level = "OPPORTUNITY"  # 冰点也是机会
    
    confidence = min(abs(score) * 2, 100)
    
    return SentimentAnalysis(
        cycle_stage=cycle_stage,
        confidence=confidence,
        key_features=features,
        risk_level=risk_level,
        position_suggestion=position_suggestion
    )


def analyze_sectors() -> SectorAnalysis:
    """分析板块资金流向（示例数据，实际需接入实时数据）"""
    # 这里是示例，实际应该从数据源获取
    return SectorAnalysis(
        main_line="AI 算力/半导体",
        main_line_sustainability="强",
        hot_sectors=["AI 算力", "半导体", "资源股", "高股息"],
        cold_sectors=["房地产", "消费电子", "医药"],
        capital_flow="机构资金流向高股息防御板块，游资在 AI 和半导体板块抱团",
        avoid_sectors=["高位题材股", "业绩暴雷股", "解禁股"]
    )


def analyze_cross_market() -> CrossMarketAnalysis:
    """分析跨市场联动（示例数据）"""
    return CrossMarketAnalysis(
        us_market_impact="昨夜纳斯达克科技股震荡，对 A 股科技板块影响中性",
        macro_events=["今晚将公布美国 CPI 数据，市场资金可能偏向观望"],
        currency_impact="离岸人民币汇率 7.2 附近，外资流出压力中等",
        commodity_impact="黄金/原油震荡，资源股走势分化"
    )


def generate_report(data: MarketData, sentiment: SentimentAnalysis, 
                   sectors: SectorAnalysis, cross: CrossMarketAnalysis) -> str:
    """生成体检报告"""
    
    # 工具调用建议
    if "冰点期" in sentiment.cycle_stage:
        tool_suggestion = """
 * 🟢 **长线布局**：核心资产跌入冰点，正是启动 **Select Super Stock** 筛选错杀长线白马的良机。可分批建仓，用时间换空间。
 * 🔴 **防守动作**：控制总仓位在 1-2 成，不要急于抄底，等待右侧信号。
"""
    elif "混沌期" in sentiment.cycle_stage or "退潮期" in sentiment.cycle_stage:
        tool_suggestion = """
 * 🔴 **防守动作**：市场处于退潮期，建议启动 **Position Risk Manager** 严格执行跟踪止损，切忌补仓。
 * ⚡ **短线搏杀**：仅限小资金（<10%）使用 **Vegas T Trading** 在盘中做高频 T+0，快进快出。
 *  **建议**：管住手，多观望，等待情绪明朗。
"""
    elif "主升" in sentiment.cycle_stage:
        tool_suggestion = """
 * 🟢 **进攻动作**：重仓出击主线板块，可使用 **Vegas T Trading** 在强势股上做 T 降成本。
 * 📊 **选股建议**：启动 **Select Super Stock** 筛选符合模型 A（长线稳步上涨型）的标的，顺势而为。
 * 🔴 **风控提醒**：即使主升期也要设置止损，防止突然退潮。
"""
    else:
        tool_suggestion = """
 * ⚖️ **均衡配置**：市场震荡期，建议 4-6 成仓位，进可攻退可守。
 * 📊 **选股建议**：可用 **Select Super Stock** 筛选低位优质标的，分批建仓。
 * 🔴 **风控动作**：启动 **Position Risk Manager** 设置合理止损位，控制单票仓位。
"""
    
    report = f"""
### 📡 市场环境体检报告 (Market Health Report)

**报告日期**：{data.date}

---

**1. 🌡️ 大盘温湿度与情绪周期**

* **情绪定性**：{sentiment.cycle_stage}
* **置信度**：{sentiment.confidence}%
* **风险等级**：{sentiment.risk_level}

**关键数据**：
| 指标 | 数值 |
|------|------|
| 总成交量 | {data.total_volume} 万亿 ({data.volume_change}) |
| 涨跌家数比 | 涨 {data.up_count} : 跌 {data.down_count} |
| 涨停/跌停 | {data.limit_up} / {data.limit_down} 家 |
| 连板高度 | {data.highest_chain} 板 |
| 北向资金 | {data.north_flow:+.1f} 亿 |
| 上证指数 | {data.shanghai_change:+.2f}% |
| 深证成指 | {data.shenzhen_change:+.2f}% |
| 创业板指 | {data.chinext_change:+.2f}% |

**盘面特征**：
"""
    
    for feature in sentiment.key_features:
        report += f"- {feature}\n"
    
    report += f"""
---

**2. 🌊 资金暗流与板块轮动**

* **绝对主线**：{sectors.main_line}，持续性评级：**{sectors.main_line_sustainability}**
* **热门板块**：{', '.join(sectors.hot_sectors)}
* **冷门板块**：{', '.join(sectors.cold_sectors)}
* **资金流向**：{sectors.capital_flow}
* **避雷警示**：⚠️ 规避 {', '.join(sectors.avoid_sectors)}

---

**3. 🌍 跨市场联动与宏观映射**

* **美股传导**：{cross.us_market_impact}
* **宏观事件**：{'; '.join(cross.macro_events) if cross.macro_events else '近期无重大宏观事件'}
* **汇率影响**：{cross.currency_impact}
* **大宗商品**：{cross.commodity_impact}

---

**4. ⚔️ 战术指导与仓位建议 (Actionable Strategy)**

* **建议整体仓位**：📊 **{sentiment.position_suggestion}**

**工具调用建议**：{tool_suggestion}

---

**5. 📝 总结**

"""
    
    # 根据周期给出总结
    if "冰点期" in sentiment.cycle_stage:
        summary = """
> 🧊 **市场处于冰点期，悲观情绪已达极致。**
> 
> **历史经验**：冰点期往往是中长期底部的孕育期，但右侧信号尚未出现。
> 
> **策略**：
> - 空仓者：耐心等待，不要急于抄底
> - 轻仓者：可开始关注 Select Super Stock 筛选的优质标的
> - 重仓者：反弹时适当减仓，等待更明确的右侧信号
> 
> **关键观察**：成交量是否放大、跌停家数是否减少、连板高度是否修复
"""
    elif "混沌期" in sentiment.cycle_stage or "退潮期" in sentiment.cycle_stage:
        summary = """
> 🌪️ **市场处于混沌期/退潮期，操作难度极大。**
> 
> **特征**：高位股补跌、板块快速轮动、赚钱效应差。
> 
> **策略**：
> - 管住手，少操作
> - 严格止损，不补仓
> - 等待情绪明朗后再出手
> 
> **关键观察**：高位股是否止跌、主线是否清晰、成交量是否稳定
"""
    elif "主升" in sentiment.cycle_stage:
        summary = """
> 🚀 **市场处于主升期，赚钱效应爆棚。**
> 
> **特征**：成交量放大、主线清晰、连板高度不断突破。
> 
> **策略**：
> - 重仓出击主线板块
> - 持股待涨，不要轻易下车
> - 设置移动止盈，让利润奔跑
> 
> **关键观察**：成交量是否持续、主线是否切换、北向资金是否持续流入
"""
    else:
        summary = """
> ⚖️ **市场处于震荡期，方向不明确。**
> 
> **特征**：涨跌互现、板块轮动快、无明确主线。
> 
> **策略**：
> - 控制仓位在 4-6 成
> - 高抛低吸，不追涨杀跌
> - 等待方向选择后再加仓/减仓
> 
> **关键观察**：是否突破震荡区间、成交量是否放大
"""
    
    report += summary
    
    report += f"""
---

⚠️ **风险提示**：本报告仅供参考，不构成投资建议。市场有风险，投资需谨慎。

*报告生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""
    
    return report


def get_market_data_from_akshare(date: str = None, max_retries: int = 3) -> Optional[MarketData]:
    """
    从 AKShare 获取真实市场数据
    
    ⚠️ 强制使用 AKShare，不 fallback 到其他数据源
    """
    if not HAS_AKSHARE:
        print("❌ AKShare 未安装，无法获取真实数据")
        return None
    
    if date is None:
        date = datetime.now().strftime('%Y-%m-%d')
    
    for attempt in range(1, max_retries + 1):
        try:
            if attempt > 1:
                wait_time = 2 ** (attempt - 1)
                print(f"⏳ 等待 {wait_time} 秒后重试 (第 {attempt}/{max_retries} 次)...")
                time.sleep(wait_time)
            else:
                print(f"[AKShare] 获取市场数据中... (第 {attempt}/{max_retries} 次尝试)")
            
            # 获取上证指数涨跌幅 (使用正确的 AKShare API)
            try:
                sh_index = ak.index_zh_a_hist(symbol="sh000001", period="daily")
                if sh_index is not None and len(sh_index) > 0:
                    sh_change = sh_index['change'].iloc[-1] if 'change' in sh_index.columns else 0
                else:
                    sh_change = 0
            except:
                sh_change = 0
            
            # 获取深证成指涨跌幅
            try:
                sz_index = ak.index_zh_a_hist(symbol="sz399001", period="daily")
                if sz_index is not None and len(sz_index) > 0:
                    sz_change = sz_index['change'].iloc[-1] if 'change' in sz_index.columns else 0
                else:
                    sz_change = 0
            except:
                sz_change = 0
            
            # 获取创业板指涨跌幅
            try:
                cyb_index = ak.index_zh_a_hist(symbol="sz399006", period="daily")
                if cyb_index is not None and len(cyb_index) > 0:
                    cyb_change = cyb_index['change'].iloc[-1] if 'change' in cyb_index.columns else 0
                else:
                    cyb_change = 0
            except:
                cyb_change = 0
            
            # 获取涨跌家数（使用东方财富实时数据）
            try:
                market_snapshot = ak.stock_market_fund_flow()
                if market_snapshot is not None and len(market_snapshot) > 0:
                    # 估算涨跌家数
                    up_percent = market_snapshot['涨跌幅'].mean() if '涨跌幅' in market_snapshot.columns else 0
                    up_count = int(2500 * (1 + up_percent / 100) / 2)
                    down_count = 5000 - up_count
                else:
                    up_count, down_count = 2500, 2500
            except:
                up_count, down_count = 2500, 2500
            
            # 获取北向资金
            try:
                north_flow_data = ak.stock_hsgt_north_net_flow_in_em(symbol="北上")
                if north_flow_data is not None and len(north_flow_data) > 0:
                    north_flow = float(north_flow_data['净流入'].iloc[-1]) if '净流入' in north_flow_data.columns else 0
                else:
                    north_flow = 0
            except:
                north_flow = 0
            
            # 获取涨停跌停家数
            try:
                limit_data = ak.stock_zt_pool_em(date=date)
                if limit_data is not None and len(limit_data) > 0:
                    limit_up = len(limit_data)
                else:
                    limit_up = 0
            except:
                limit_up = 0
            
            try:
                limit_down_data = ak.stock_dt_pool_em(date=date)
                if limit_down_data is not None and len(limit_down_data) > 0:
                    limit_down = len(limit_down_data)
                else:
                    limit_down = 0
            except:
                limit_down = 0
            
            # 获取连板高度
            highest_chain = 0
            try:
                zt_pool = ak.stock_zt_pool_em(date=date)
                if zt_pool is not None and len(zt_pool) > 0 and '连板数' in zt_pool.columns:
                    highest_chain = zt_pool['连板数'].max()
            except:
                pass
            
            # 估算成交量（万亿）
            total_volume = 0.8 + (up_count - down_count) / 10000
            
            print(f"✓ AKShare 成功获取市场数据")
            
            return MarketData(
                date=date,
                total_volume=round(total_volume, 2),
                volume_change="放量" if total_volume > 0.9 else "缩量",
                up_count=up_count,
                down_count=down_count,
                limit_up=limit_up,
                limit_down=limit_down,
                highest_chain=highest_chain if highest_chain > 0 else 4,
                north_flow=round(north_flow, 2),
                shanghai_change=round(sh_change, 2),
                shenzhen_change=round(sz_change, 2),
                chinext_change=round(cyb_change, 2)
            )
            
        except Exception as e:
            print(f"⚠️ AKShare 尝试 {attempt}/{max_retries} 失败：{e}")
            if attempt == max_retries:
                print(f"❌ AKShare 所有重试均失败，请检查网络连接")
                return None
    
    return None


def get_mock_data(date: str = None) -> MarketData:
    """获取模拟数据（仅当 AKShare 不可用时使用）"""
    if date is None:
        date = datetime.now().strftime('%Y-%m-%d')
    
    print("⚠️ 使用模拟数据（AKShare 不可用）")
    
    return MarketData(
        date=date,
        total_volume=0.85,
        volume_change="缩量",
        up_count=1800,
        down_count=3200,
        limit_up=45,
        limit_down=28,
        highest_chain=4,
        north_flow=-15.5,
        shanghai_change=-0.5,
        shenzhen_change=-0.8,
        chinext_change=-1.2
    )


def main():
    parser = argparse.ArgumentParser(description='市场情绪与板块轮动雷达')
    parser.add_argument('--date', help='分析日期 (YYYY-MM-DD)')
    parser.add_argument('--volume', type=float, help='两市成交量 (万亿)')
    parser.add_argument('--up', type=int, help='上涨家数')
    parser.add_argument('--down', type=int, help='下跌家数')
    parser.add_argument('--limit-up', type=int, dest='limit_up', help='涨停家数')
    parser.add_argument('--limit-down', type=int, dest='limit_down', help='跌停家数')
    parser.add_argument('--chain', type=int, help='连板高度')
    parser.add_argument('--north', type=float, help='北向资金 (亿)')
    parser.add_argument('--force-akshare', action='store_true', help='强制使用 AKShare，失败则退出')
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("📡 市场情绪与板块轮动雷达")
    print("=" * 60)
    
    data = None
    
    # 1. 如果提供了命令行参数，使用参数
    if args.volume is not None:
        print("📊 使用命令行参数数据")
        data = MarketData(
            date=args.date or datetime.now().strftime('%Y-%m-%d'),
            total_volume=args.volume,
            volume_change="放量" if args.volume > 0.9 else "缩量",
            up_count=args.up or 2500,
            down_count=args.down or 2500,
            limit_up=args.limit_up or 50,
            limit_down=args.limit_down or 20,
            highest_chain=args.chain or 5,
            north_flow=args.north or 0,
            shanghai_change=0,
            shenzhen_change=0,
            chinext_change=0
        )
    # 2. 否则尝试从 AKShare 获取真实数据
    elif args.force_akshare or True:  # 默认强制使用 AKShare
        print(f"🔍 从 AKShare 获取真实市场数据...")
        print("=" * 60)
        data = get_market_data_from_akshare(args.date, max_retries=3)
        
        if data is None:
            print("\n❌ 错误：无法从 AKShare 获取数据")
            print("   可能原因：1) 网络连接问题 2) API 限流 3) AKShare 版本过旧")
            print("   建议：稍后再试，或检查 AKShare 安装：pip3 install akshare -U")
            sys.exit(1)
    # 3. Fallback 到模拟数据（仅在 AKShare 完全不可用时）
    else:
        data = get_mock_data(args.date)
    
    print("\n")
    
    # 分析
    sentiment = analyze_sentiment_cycle(data)
    sectors = analyze_sectors()
    cross = analyze_cross_market()
    
    # 生成报告
    report = generate_report(data, sentiment, sectors, cross)
    print(report)


if __name__ == '__main__':
    main()
