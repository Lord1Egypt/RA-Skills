"""
极简版涨停板分析模块
直接查询问财首板涨停数据
"""

import pywencai
import pandas as pd
from datetime import datetime
from typing import List, Dict


class SimpleLimitUpAnalyzer:
    """极简涨停板分析器"""

    def __init__(self):
        self.today = datetime.now()

    def get_first_limit_stocks(self) -> List[Dict]:
        """
        获取首板涨停股票列表（核心功能）
        一行代码搞定！
        """
        try:
            # 直接查询首板涨停，并包含涨停时间等详细信息
            df = pywencai.get(
                query="首板涨停，首次涨停时间",
                loop=True,
                max_retries=3
            )

            if df is None or df.empty:
                return []

            # 转换为列表格式
            stocks = []
            for idx, row in df.iterrows():
                stock = {
                    'code': str(row.get('股票代码', '')),
                    'name': str(row.get('股票简称', '')),
                    'price': float(row.get('最新价', 0)) if pd.notna(row.get('最新价')) else 0,
                    'change_percent': float(row.get('最新涨跌幅', 0)) if pd.notna(row.get('最新涨跌幅')) else 0,
                    'consecutive_days': int(row.get(f'连续涨停天数[{self.today.strftime("%Y%m%d")}]', 1)),
                    'market_cap': float(row.get(f'a股市值(不含限售股)[{self.today.strftime("%Y%m%d")}]', 0)) if pd.notna(row.get(f'a股市值(不含限售股)[{self.today.strftime("%Y%m%d")}]', 0)) else 0,
                }

                # 提取涨停详细信息
                for col in df.columns:
                    if '首次涨停时间' in col:
                        stock['first_limit_time'] = str(row[col]) if pd.notna(row[col]) else None
                    if '最终涨停时间' in col:
                        stock['final_limit_time'] = str(row[col]) if pd.notna(row[col]) else None
                    if '涨停封单量' in col:
                        stock['seal_volume'] = float(row[col]) if pd.notna(row[col]) else 0
                    if '涨停封单额' in col:
                        stock['seal_amount'] = float(row[col]) if pd.notna(row[col]) else 0
                    if '涨停开板次数' in col:
                        stock['open_times'] = int(row[col]) if pd.notna(row[col]) else 0
                    if '涨停明细数据' in col:
                        stock['limit_detail'] = str(row[col]) if pd.notna(row[col]) else None

                # 计算首板评分
                stock['first_limit_score'] = self._calculate_score(stock)
                stock['features'] = self._extract_features(stock)

                stocks.append(stock)

            # 按首板评分排序
            stocks.sort(key=lambda x: x['first_limit_score'], reverse=True)

            return stocks

        except Exception as e:
            print(f"获取首板涨停失败: {e}")
            import traceback
            traceback.print_exc()
            return []

    def _calculate_score(self, stock: Dict) -> int:
        """计算首板评分"""
        score = 0

        # 涨停时间评分
        first_time = stock.get('first_limit_time')
        if first_time:
            try:
                # 假设时间格式为 "09:30:00"
                hour = int(str(first_time).split(':')[0])
                if hour < 9:
                    score += 3  # 9点前涨停
                elif hour < 10:
                    score += 2  # 9-10点涨停
                elif hour < 11:
                    score += 1  # 10-11点涨停
            except:
                pass

        # 封板质量评分
        seal_volume = stock.get('seal_volume', 0)
        if seal_volume > 10000:  # 封单量>1万手
            score += 1

        # 开板次数评分
        open_times = stock.get('open_times', 0)
        if open_times == 0:
            score += 2  # 0次开板，强势封板
        elif open_times <= 2:
            score += 1  # 少量开板

        return score

    def _extract_features(self, stock: Dict) -> List[str]:
        """提取首板特征"""
        features = []

        # 涨停时间特征
        first_time = stock.get('first_limit_time')
        if first_time:
            try:
                hour = int(str(first_time).split(':')[0])
                if hour < 9:
                    features.append('开盘即涨停')
                elif hour < 10:
                    features.append('早盘涨停')
                elif hour < 11:
                    features.append('午前涨停')
                else:
                    features.append('午盘涨停')
            except:
                pass

        # 开板次数特征
        open_times = stock.get('open_times', 0)
        if open_times == 0:
            features.append('一字封板')
        elif open_times == 1:
            features.append('开板1次')
        elif open_times > 3:
            features.append(f'频繁开板{open_times}次')

        # 市值特征
        market_cap = stock.get('market_cap', 0)
        if market_cap > 0:
            cap = market_cap / 100000000  # 转换为亿
            if cap < 30:
                features.append('小市值')
            elif cap > 200:
                features.append('大盘股')

        return features

    def get_full_analysis(self) -> Dict:
        """获取完整分析报告"""
        stocks = self.get_first_limit_stocks()

        if not stocks:
            return {
                'success': False,
                'message': '无法获取首板数据',
                'timestamp': datetime.now().isoformat()
            }

        # 按时间分类
        morning_limit = []  # 早盘涨停（9:30-10:00）
        early_limit = []    # 早盘涨停（10:00-11:30）
        noon_limit = []     # 午盘涨停（11:00-13:00）
        afternoon_limit = [] # 午后涨停（13:00-15:00）

        for stock in stocks:
            time = stock.get('first_limit_time', '')
            if not time:
                noon_limit.append(stock)
                continue

            try:
                hour = int(str(time).split(':')[0])
                if hour < 9:
                    morning_limit.append(stock)
                elif hour < 10:
                    early_limit.append(stock)
                elif hour < 13:
                    noon_limit.append(stock)
                else:
                    afternoon_limit.append(stock)
            except:
                noon_limit.append(stock)

        return {
            'success': True,
            'total_count': len(stocks),
            'first_limit_candidates': stocks[:30],  # 返回前30只
            'summary': {
                'total': len(stocks),
                'morning_9': len(morning_limit),  # 9点前
                'morning': len(early_limit),       # 9-10点
                'noon': len(noon_limit),          # 10-13点
                'afternoon': len(afternoon_limit) # 13点后
            },
            'time_distribution': {
                '9点前涨停': [s['name'] for s in morning_limit[:5]],
                '9-10点涨停': [s['name'] for s in early_limit[:5]],
                '10-13点涨停': [s['name'] for s in noon_limit[:5]],
                '13点后涨停': [s['name'] for s in afternoon_limit[:5]],
            },
            'timestamp': datetime.now().isoformat()
        }


def test_simple_analyzer():
    """测试极简分析器"""
    print("=" * 80)
    print("极简涨停板分析器测试")
    print("=" * 80)

    analyzer = SimpleLimitUpAnalyzer()
    result = analyzer.get_full_analysis()

    if result['success']:
        print(f"\n✅ 分析成功！")
        print(f"今日首板股票总数: {result['total_count']}")

        print(f"\n📊 首板时间分布:")
        for key, value in result['summary'].items():
            if key != 'total':
                print(f"  {key}: {value}只")

        print(f"\n🔥 前10只首板股票:")
        for i, stock in enumerate(result['first_limit_candidates'][:10], 1):
            print(f"{i:2d}. {stock['name']:10s}({stock['code']:12s}) | "
                  f"评分:★{stock['first_limit_score']} | "
                  f"涨停:{stock['first_limit_time']} | "
                  f"{','.join(stock['features'][:2])}")

        print(f"\n📈 时间分布示例:")
        for period, names in result['time_distribution'].items():
            if names:
                print(f"  {period}: {', '.join(names)}")

    else:
        print(f"\n❌ 分析失败: {result.get('message')}")


if __name__ == "__main__":
    test_simple_analyzer()
