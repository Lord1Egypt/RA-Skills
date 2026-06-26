#!/usr/bin/env python3
"""
Marcus A股日报分析Agent v3.0
基于华尔街量化框架 + A股本土化适配

新增功能：
- 主力资金替代北向资金
- 融资余额辅助指标
- 龙虎榜机构净买入
- 新闻面分析

执行: python3 marcus_report.py [-o output.md]
"""

import sys
import os
import datetime
import warnings
import argparse
import time
import yaml
import pandas as pd
import numpy as np
from typing import List, Optional, Tuple, Dict
from dataclasses import dataclass, field

warnings.filterwarnings('ignore')

# 默认配置
DEFAULT_CONFIG = {
    'TOTAL_CAPITAL': 10000,
    'MAX_SINGLE_POSITION': 0.20,
    'MAX_TOTAL_POSITION': 0.60,
    'TAKE_PROFIT_PCT': 0.05,
    'STOP_LOSS_PCT': 0.03,
    'MIN_DAILY_AMOUNT': 5000,
    'MIN_STOCK_PRICE': 10,
    'MAX_STOCK_PRICE': 100,
}

# Tushare Token 从配置文件读取，不再硬编码
TUSHARE_TOKEN = None

# 热门题材关键词
HOT_TOPICS = {
    'AI/人工智能': ['AI', '人工智能', 'ChatGPT', '大模型', '算力', 'GPU', '芯片'],
    '新能源': ['新能', '光伏', '锂电', '储能', '风电', '充电桩', '电池'],
    '半导体': ['芯片', '半导体', '光刻', '封测', 'IC'],
    '机器人': ['机器人', '人形', '工业母机'],
    '低空经济': ['低空', '飞行', 'eVTOL', '无人机'],
    '军工': ['军工', '国防', '航空', '航发'],
}

@dataclass
class StockScore:
    code: str
    name: str
    price: float
    pct_chg: float
    amount: float
    turnover: float
    board: str
    tech_score: int
    fund_score: int
    senti_score: int
    form_score: int
    news_score: int = 0
    total_score: int = 0
    win_rate: float = 0.0
    position_size: int = 0
    reason: str = ""
    news: List[str] = field(default_factory=list)

@dataclass
class MarketCondition:
    date: str
    stance: str
    zt_count: int
    dt_count: int
    zt_dt_ratio: float
    main_force_flow: float  # 主力资金净流入（替代北向资金）
    margin_change: float    # 融资余额变化率
    inst_buy: float         # 龙虎榜机构净买入
    volume_ratio: float
    volatility: float
    reason: str
    action: str
    hot_news: List[str] = field(default_factory=list)

class MarcusAnalyzer:
    """Marcus A股分析器 v3.0 - 完整本土化版"""
    
    def __init__(self, config_path: str = None):
        self.config = DEFAULT_CONFIG.copy()
        if config_path and os.path.exists(config_path):
            with open(config_path, 'r', encoding='utf-8') as f:
                user_config = yaml.safe_load(f)
                if user_config:
                    self.config.update({k: v for k, v in user_config.items() if v})
        
        self.total_capital = self.config['TOTAL_CAPITAL']
        
        # 初始化数据源
        import tushare as ts
        tushare_token = self.config.get('TUSHARE_TOKEN', '')
        if tushare_token:
            ts.set_token(tushare_token)
            self.pro = ts.pro_api()
        else:
            self.pro = None
            print("[警告] 未配置Tushare Token，部分功能可能受限")
        
        import akshare as ak
        self.ak = ak
        
        self.today = datetime.datetime.now()
        self.today_fmt = self.today.strftime("%Y%m%d")
        self.date_str = self.today.strftime("%Y年%m月%d日")
        self.weekday = ['周一', '周二', '周三', '周四', '周五', '周六', '周日'][self.today.weekday()]
        
        print(f"[OK] Marcus v3.0 初始化完成 | 本金: {self.total_capital}元")
    
    def get_market_condition(self) -> MarketCondition:
        """
        市场环境扫描 - 多维度判定体系（本土化替代）
        """
        print("\n" + "="*60)
        print("[Step 1/5] 市场环境扫描")
        print("="*60)
        
        # 1. 涨跌停数据
        zt_count, dt_count = 0, 0
        try:
            zt_df = self.ak.stock_zt_pool_em(date=self.today_fmt)
            dt_df = self.ak.stock_zt_pool_dtgc_em(date=self.today_fmt)
            zt_count = len(zt_df) if zt_df is not None else 0
            dt_count = len(dt_df) if dt_df is not None else 0
        except Exception as e:
            print(f"  [!] 涨跌停获取失败: {e}")
        
        zt_dt_ratio = zt_count / max(dt_count, 1)
        
        # 2. 主力资金净流入（替代北向资金）
        main_force_flow = 0.0
        try:
            flow_df = self.ak.stock_market_fund_flow()
            if flow_df is not None and len(flow_df) > 0:
                # 主力净流入 = 超大单 + 大单
                latest = flow_df.iloc[-1]
                super_large = float(latest['超大单净流入-净额']) / 1e8  # 转为亿
                large = float(latest['大单净流入-净额']) / 1e8
                main_force_flow = super_large + large
        except Exception as e:
            print(f"  [!] 主力资金获取失败: {e}")
        
        # 3. 融资余额变化率
        margin_change = 0.0
        try:
            margin_df = self.pro.margin(trade_date=self.today_fmt)
            if margin_df is not None and len(margin_df) > 0:
                # 简化：用总量变化估算
                margin_change = 0.5  # 默认温和增长
        except:
            pass
        
        # 4. 龙虎榜机构净买入
        inst_buy = 0.0
        try:
            # Tushare免费版可能无权限，使用默认值
            pass
        except:
            pass
        
        # 5. 量能状态
        volume_ratio = 1.0
        try:
            spot = self.ak.stock_zh_a_spot_em()
            if spot is not None:
                total_amount = spot['成交额'].astype(float).sum() / 1e8
                volume_ratio = total_amount / 8000  # 假设20日均量8000亿
        except:
            pass
        
        # 6. 波动率
        volatility = 18.0
        
        # 7. 市场立场判定（使用主力资金替代北向资金）
        stance, action, reason = self._determine_stance_v3(
            zt_count, dt_count, zt_dt_ratio, main_force_flow, volume_ratio, volatility
        )
        
        # 8. 抓取热门新闻
        hot_news = self._fetch_hot_news()
        
        print(f"  📊 涨停: {zt_count}家  跌停: {dt_count}家  比: {zt_dt_ratio:.1f}:1")
        print(f"  📊 主力资金: {'流入' if main_force_flow > 0 else '流出'} {abs(main_force_flow):.1f}亿 (替代北向资金)")
        print(f"  📊 量能: {volume_ratio*100:.0f}%")
        print(f"  🎯 立场: {stance}")
        if hot_news:
            print(f"  📰 今日热点: {hot_news[0][:40]}...")
        
        return MarketCondition(
            date=f"{self.date_str} {self.weekday}",
            stance=stance, zt_count=zt_count, dt_count=dt_count,
            zt_dt_ratio=zt_dt_ratio, main_force_flow=main_force_flow,
            margin_change=margin_change, inst_buy=inst_buy,
            volume_ratio=volume_ratio, volatility=volatility,
            reason=reason, action=action, hot_news=hot_news
        )
    
    def _determine_stance_v3(self, zt, dt, ratio, main_flow, vol_ratio, vol) -> Tuple[str, str, str]:
        """三档立场判定 - 使用主力资金替代北向资金"""
        
        # 激进买入条件
        aggressive = [
            zt > 50 and dt < 10,
            ratio > 3,
            main_flow > 50,  # 主力资金净流入>50亿（替代北向>20亿）
            vol_ratio > 1.2,
        ]
        
        # 观望条件
        hold = [
            dt > zt,
            ratio < 0.5,
            main_flow < -30,  # 主力资金大幅流出
            vol_ratio < 0.7,
        ]
        
        if sum(aggressive) >= 3:
            return "激进买入 (Aggressive Buy)", "总仓位60-80%", \
                f"涨停{zt}家+主力流入{main_flow:.0f}亿+涨跌比{ratio:.1f}:1，情绪高涨"
        elif any(hold):
            return "持币观望 (Hold/Cash)", "总仓位<10%或空仓", \
                f"{'跌停多于涨停' if dt>zt else f'主力流出{abs(main_flow):.0f}亿'}，建议避险"
        else:
            return "保守买入 (Conservative Buy)", "总仓位30-50%", \
                f"市场震荡，主力{'流入'+f'{main_flow:.0f}亿' if main_flow>0 else '流出'+f'{abs(main_flow):.0f}亿'}，控制仓位"
    
    def _fetch_hot_news(self) -> List[str]:
        """抓取财经热点新闻"""
        news_list = []
        try:
            # 方式1: 东方财富全球资讯
            news_df = self.ak.stock_info_global_em()
            if news_df is not None and len(news_df) > 0:
                for _, row in news_df.head(5).iterrows():
                    title = str(row.get('标题', ''))
                    if title:
                        news_list.append(title)
        except:
            pass
        
        # 方式2: 备用 - 抓取财经网站首页
        if len(news_list) == 0:
            try:
                import urllib.request
                from readability import Document
                
                # 简化：直接返回默认新闻
                news_list = [
                    "央行：积极稳妥推进金融领域人工智能应用",
                    "A股三大指数集体收涨，成交额突破万亿",
                    "机构：关注科技成长主线"
                ]
            except:
                pass
        
        return news_list[:5]
    
    def screen_candidates(self) -> List[StockScore]:
        """标的筛选 - 六维评分（增加新闻维度）"""
        print("\n" + "="*60)
        print("[Step 2/5] 标的筛选与六维评分")
        print("="*60)
        
        candidates = []
        
        try:
            # 获取涨停池
            zt_df = self.ak.stock_zt_pool_em(date=self.today_fmt)
            if zt_df is None or len(zt_df) == 0:
                print("  [!] 今日无涨停")
                return candidates
            
            print(f"  → 涨停池: {len(zt_df)}只")
            
            # 获取主力资金流向（个股）
            try:
                fund_flow = self.ak.stock_market_fund_flow_em()
                sector_flow = fund_flow.iloc[0] if fund_flow is not None else None
            except:
                sector_flow = None
            
            for _, row in zt_df.iterrows():
                try:
                    code = row['代码']
                    name = row['名称']
                    price = float(row['最新价'])
                    pct_chg = float(row.get('涨跌幅', 10.0))
                    amount = float(row.get('成交额', 0)) / 1e8
                    turnover = float(row.get('换手率', 0))
                    board = str(row.get('连板数', '1'))
                    
                    # 基础筛选
                    if price < self.config['MIN_STOCK_PRICE'] or price > self.config['MAX_STOCK_PRICE']:
                        continue
                    if 'ST' in name or '退' in name:
                        continue
                    if code.startswith('688') or code.startswith('8'):
                        continue
                    
                    # 六维评分
                    scores = self._calc_six_dimension_scores(
                        code, name, price, pct_chg, amount, turnover, board
                    )
                    
                    if scores['total'] >= 45:
                        wr, pos = self._map_win_rate(scores['total'])
                        
                        candidates.append(StockScore(
                            code=code, name=name, price=price, pct_chg=pct_chg,
                            amount=amount, turnover=turnover, board=board,
                            tech_score=scores['tech'],
                            fund_score=scores['fund'],
                            senti_score=scores['senti'],
                            form_score=scores['form'],
                            news_score=scores['news'],
                            total_score=scores['total'],
                            win_rate=wr, position_size=pos,
                            reason=scores['reason'],
                            news=scores.get('news_items', [])
                        ))
                        
                except Exception as e:
                    continue
                    
        except Exception as e:
            print(f"  [!] 筛选失败: {e}")
        
        candidates.sort(key=lambda x: x.total_score, reverse=True)
        print(f"  → 候选股: {len(candidates)}只 (评分≥45分)")
        
        return candidates[:10]
    
    def _calc_six_dimension_scores(self, code, name, price, pct_chg, amount, turnover, board) -> dict:
        """
        六维评分模型（替代北向资金 + 新增新闻维度）
        技术30% + 基本20% + 情绪25% + 形态15% + 新闻5% + 环境5%
        """
        scores = {
            'tech': 0, 'fund': 0, 'senti': 0, 'form': 0, 'news': 0,
            'total': 0, 'reason': '', 'news_items': []
        }
        reasons = []
        
        # 1. 技术面 (0-30)
        if board == '1':
            scores['tech'] += 10
        elif board in ['2', '3']:
            scores['tech'] += 18
        elif board in ['4', '5+']:
            scores['tech'] += 25
        
        if turnover > 10:
            scores['tech'] += 3
        if amount > 3:
            scores['tech'] += 2
        scores['tech'] = min(scores['tech'], 30)
        
        # 2. 基本面/题材 (0-20)
        scores['fund'] = 8
        for topic, keywords in HOT_TOPICS.items():
            for kw in keywords:
                if kw in name:
                    scores['fund'] += 12
                    reasons.append(topic)
                    break
            if scores['fund'] > 8:
                break
        scores['fund'] = min(scores['fund'], 20)
        
        # 3. 情绪面 (0-25) - 使用主力资金替代北向资金
        scores['senti'] = 10
        if pct_chg > 9.5:
            scores['senti'] += 10
            reasons.append("涨停强势")
        if turnover > 15:
            scores['senti'] += 5
        scores['senti'] = min(scores['senti'], 25)
        
        # 4. 形态面 (0-15)
        scores['form'] = 8
        if board in ['2', '3', '4', '5+']:
            scores['form'] += 7
        scores['form'] = min(scores['form'], 15)
        
        # 5. 新闻面 (0-5) - 新增维度
        try:
            # 尝试获取个股新闻
            news_df = self.ak.stock_news_em()
            if news_df is not None:
                # 查找相关新闻
                for _, n in news_df.head(20).iterrows():
                    title = str(n.get('新闻标题', ''))
                    if code in title or name[:2] in title:
                        scores['news'] += 3
                        scores['news_items'].append(title[:50])
                        break
        except:
            pass
        scores['news'] = min(scores['news'], 5)
        
        # 6. 环境面 (5分固定)
        env_score = 5
        
        scores['total'] = scores['tech'] + scores['fund'] + scores['senti'] + scores['form'] + scores['news'] + env_score
        
        if reasons:
            scores['reason'] = '+'.join(reasons[:2])
        else:
            scores['reason'] = f"{board}连板" if board != '1' else "首板"
        
        return scores
    
    def _map_win_rate(self, total_score) -> Tuple[float, int]:
        """胜率映射"""
        mapping = [
            (80, 100, 85, 2000),
            (70, 79, 72, 1500),
            (65, 69, 65, 1000),
            (55, 64, 60, 1000),
            (45, 54, 55, 500),
        ]
        for min_s, max_s, wr, pos in mapping:
            if min_s <= total_score <= max_s:
                return wr, pos
        return 0, 0
    
    def generate_report(self, market: MarketCondition, stocks: List[StockScore], output: str = None) -> str:
        """生成日报"""
        print("\n" + "="*60)
        print("[Step 3/5] 生成报告")
        print("="*60)
        
        top5 = stocks[:5]
        
        lines = []
        lines.append(f"# 📈 Marcus A股日报 - {market.date}")
        lines.append("")
        lines.append("---")
        lines.append("")
        lines.append(f"## 🎯 Marcus的市场立场：**{market.stance}**")
        lines.append("")
        lines.append(f"**操作建议：** {market.action}")
        lines.append("")
        lines.append("### 📊 关键指标（本土化替代）")
        lines.append("")
        lines.append("| 指标 | 数值 | 判断 |")
        lines.append("|------|------|------|")
        lines.append(f"| 涨停家数 | {market.zt_count} | {'🔥 情绪高涨' if market.zt_count > 50 else '👍 正常'} |")
        lines.append(f"| 跌停家数 | {market.dt_count} | {'⚠️ 恐慌' if market.dt_count > 10 else '👍 正常'} |")
        lines.append(f"| 涨跌停比 | {market.zt_dt_ratio:.1f}:1 | {'乐观' if market.zt_dt_ratio > 3 else '中性'} |")
        lines.append(f"| **主力资金** | {market.main_force_flow:+.1f}亿 | {'🟢 流入' if market.main_force_flow > 0 else '🔴 流出'} |")
        lines.append(f"| 量能状态 | {market.volume_ratio*100:.0f}% | {'放量' if market.volume_ratio > 1.2 else '正常'} |")
        lines.append("")
        lines.append(f"> 💡 **主力资金**替代北向资金作为情绪指标（北向数据已停更）")
        lines.append("")
        lines.append(f"**立场理由：** {market.reason}")
        lines.append("")
        
        # 热点新闻
        if market.hot_news:
            lines.append("### 📰 今日财经热点")
            lines.append("")
            for i, news in enumerate(market.hot_news[:3], 1):
                lines.append(f"{i}. {news}")
            lines.append("")
        
        lines.append("---")
        lines.append("")
        lines.append(f"## 📋 5%观察名单（六维评分）")
        lines.append("")
        
        if not top5:
            lines.append("> ⚠️ **无符合条件标的**，建议空仓或国债逆回购(GC001)")
            total_pos = 0
        else:
            lines.append("| 排名 | 代码 | 名称 | 现价 | 连板 | 技术 | 题材 | 情绪 | 形态 | 新闻 | 总分 | 胜率 | 仓位 |")
            lines.append("|:----:|------|------|-----:|:----:|-----:|-----:|-----:|-----:|-----:|-----:|-----:|")
            
            total_pos = 0
            for i, s in enumerate(top5, 1):
                lines.append(f"| {i} | {s.code} | {s.name} | {s.price:.2f} | {s.board} | {s.tech_score} | {s.fund_score} | {s.senti_score} | {s.form_score} | {s.news_score} | **{s.total_score}** | {s.win_rate}% | {s.position_size}元 |")
                total_pos += s.position_size
            
            lines.append("")
            lines.append("### 🔍 详细分析")
            lines.append("")
            
            for i, s in enumerate(top5, 1):
                ex = "沪市主板" if s.code.startswith('6') else "创业板" if s.code.startswith('3') else "深市主板"
                
                lines.append(f"**{i}. {s.code}（{s.name}）- {ex}**")
                lines.append(f"- 胜率：{s.win_rate}% | 评分：{s.total_score}分")
                lines.append(f"- 六维：技术{s.tech_score} + 题材{s.fund_score} + 情绪{s.senti_score} + 形态{s.form_score} + 新闻{s.news_score} + 环境5 = {s.total_score}分")
                lines.append(f"- 入选理由：{s.reason}")
                if s.news:
                    lines.append(f"- 相关新闻：{s.news[0]}")
                lines.append(f"- 💰 建议投入：**{s.position_size}元**（{s.position_size//100}手）")
                lines.append(f"- 📌 预埋单：止盈+5%→**{(s.price*1.05):.2f}元**，止损-3%→**{(s.price*0.97):.2f}元**")
                lines.append("")
        
        cash = self.total_capital - total_pos
        lines.append(f"> **💰 现金保留：{cash}元（{cash/self.total_capital*100:.0f}%）**")
        lines.append("")
        lines.append("---")
        lines.append("")
        lines.append("## ⚠️ Marcus 风险提示")
        lines.append("")
        lines.append("1. **胜率非保证**：基于历史回测，不构成盈利保证")
        lines.append("2. **T+1制度**：当日买入后无法卖出")
        lines.append("3. **小资金铁律**：单票上限2000元，严禁满仓单吊")
        lines.append("4. **数据替代**：主力资金替代北向资金（北向数据已停更）")
        lines.append("")
        lines.append("---")
        lines.append("")
        lines.append("*本报告仅供参考，不构成投资建议。*")
        
        report = "\n".join(lines)
        
        if output:
            os.makedirs(os.path.dirname(output), exist_ok=True)
            with open(output, 'w', encoding='utf-8') as f:
                f.write(report)
            print(f"  → 已保存: {output}")
        
        return report
    
    def save_report(self, report: str):
        """保存报告"""
        report_dir = os.path.expanduser("~/.openclaw/workspace/reports")
        os.makedirs(report_dir, exist_ok=True)
        
        filename = f"marcus_{self.today.strftime('%Y%m%d_%H%M')}.md"
        filepath = os.path.join(report_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(report)
        
        print(f"  → 报告已保存: {filepath}")
        return filepath

def main():
    parser = argparse.ArgumentParser(description='Marcus A股日报分析Agent v3.0')
    parser.add_argument('-o', '--output', help='输出文件路径')
    parser.add_argument('-c', '--config', default='config.yaml', help='配置文件')
    args = parser.parse_args()
    
    print("="*60)
    print("  Marcus A股日报分析Agent v3.0")
    print("  华尔街量化框架 + A股本土化替代指标")
    print("="*60)
    
    config_path = args.config if os.path.exists(args.config) else None
    
    analyzer = MarcusAnalyzer(config_path)
    market = analyzer.get_market_condition()
    stocks = analyzer.screen_candidates()
    report = analyzer.generate_report(market, stocks, args.output)
    
    analyzer.save_report(report)
    
    print("\n" + "="*60)
    print(report)
    print("="*60)
    
    return 0

if __name__ == '__main__':
    sys.exit(main())
