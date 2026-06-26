import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
import jqdatasdk as jq
import pandas as pd
from datetime import datetime, timedelta

jq.auth('13918681158', 'Yindb1158')

stocks = [
    '600519.XSHG', '000001.XSHE', '601318.XSHG', '600036.XSHG',
    '000333.XSHE', '601012.XSHG', '600900.XSHG', '600276.XSHG',
    '300750.XSHE', '601888.XSHG', '600309.XSHG', '000651.XSHE',
    '601166.XSHG', '600030.XSHG', '002415.XSHE', '601398.XSHG',
    '601288.XSHG', '601988.XSHG', '600048.XSHG', '002594.XSHE'
]

name_map = {
    '600519.XSHG': '贵州茅台', '000001.XSHE': '平安银行',
    '601318.XSHG': '中国平安', '600036.XSHG': '招商银行',
    '000333.XSHE': '美的集团', '601012.XSHG': '隆基绿能',
    '600900.XSHG': '长江电力', '600276.XSHG': '恒瑞医药',
    '300750.XSHE': '宁德时代', '601888.XSHG': '中国中免',
    '600309.XSHG': '万华化学', '000651.XSHE': '格力电器',
    '601166.XSHG': '兴业银行', '600030.XSHG': '中信证券',
    '002415.XSHE': '海康威视', '601398.XSHG': '工商银行',
    '601288.XSHG': '农业银行', '601988.XSHG': '中国银行',
    '600048.XSHG': '保利发展', '002594.XSHE': '比亚迪',
}

end_date = '2026-02-10'
start_date = '2026-02-09'

df_auction = jq.get_call_auction(stocks, start_date=start_date, end_date=end_date)

results = []
for code in stocks:
    stock_df = df_auction[df_auction['code'] == code]
    if len(stock_df) == 0:
        continue
    
    latest_auction = stock_df.iloc[-1]
    auction_volume = latest_auction['volume']
    auction_price = latest_auction['current']
    auction_time = latest_auction['time']
    auction_money = latest_auction['money']
    
    try:
        daily_df = jq.get_price(code, count=10, frequency='daily', 
                                end_date=start_date, 
                                fields=['volume', 'money'])
        if daily_df is not None and len(daily_df) >= 5:
            avg_volume_5d = daily_df['volume'].tail(5).mean()
            avg_money_5d = daily_df['money'].tail(5).mean()
            # 近5日平均每分钟成交量 (240分钟交易日)
            avg_per_min = avg_volume_5d / 240.0
            # 近5日平均每分钟成交额
            avg_money_per_min = avg_money_5d / 240.0
            
            # 集合竞价量比 = 集合竞价每分钟成交量 / 近5日平均每分钟成交量
            # 集合竞价约25分钟
            auction_per_min = auction_volume / 25.0
            volume_ratio = auction_per_min / avg_per_min if avg_per_min > 0 else 0
            
            # 成交额量比
            auction_money_per_min = auction_money / 25.0
            money_ratio = auction_money_per_min / avg_money_per_min if avg_money_per_min > 0 else 0
            
            try:
                val = jq.get_fundamentals(
                    jq.query(jq.valuation.circulating_share)
                    .filter(jq.valuation.code == code),
                    date=start_date
                )
                if val is not None and len(val) > 0:
                    circ_shares = val['circulating_share'].iloc[0]  # 万股
                    turnover_rate = auction_volume / (circ_shares * 10000) * 100
                else:
                    turnover_rate = 0
            except:
                turnover_rate = 0
            
            results.append({
                '代码': code.split('.')[0],
                '名称': name_map.get(code, ''),
                '集合竞价时间': str(auction_time)[:19],
                '集合竞价成交价': auction_price,
                '集合竞价成交量': int(auction_volume),
                '集合竞价成交额': round(auction_money, 0),
                '集合竞价每分钟量': round(auction_per_min, 0),
                '近5日每分钟量': round(avg_per_min, 0),
                '量比': round(volume_ratio, 3),
                '成交额量比': round(money_ratio, 3),
                '集合换手率': round(turnover_rate, 4),
                '买一量': int(latest_auction.get('b1_v', 0)),
                '卖一量': int(latest_auction.get('a1_v', 0)),
                '买一价': latest_auction.get('b1_p', 0),
                '卖一价': latest_auction.get('a1_p', 0),
            })
    except Exception as e:
        print('%s 计算失败: %s' % (code, e))

df_results = pd.DataFrame(results)
if len(df_results) > 0:
    df_sorted = df_results.sort_values('量比', ascending=False)
    
    print("=" * 100)
    print("  沪深300成分股 集合竞价量比分析")
    print("  数据日期: 2026-02-10 (JQData免费版最后可用日期)")
    print("=" * 100)
    print()
    print("全部股票按量比排序:")
    print(df_sorted[['代码', '名称', '集合竞价成交价', '集合竞价成交量', 
                      '集合竞价每分钟量', '近5日每分钟量', '量比', '集合换手率']].to_string(index=False))
    
    print()
    df_filtered = df_sorted[df_sorted['量比'] > 1]
    print("量比 > 1 的股票: %d 只" % len(df_filtered))
    if len(df_filtered) > 0:
        print(df_filtered[['代码', '名称', '集合竞价成交价', '集合竞价成交量',
                           '量比', '集合换手率', '买一量', '卖一量']].to_string(index=False))
    else:
        print("  无 (所有股票量比均小于1，说明集合竞价阶段成交较清淡)")
    
    print()
    print("量比分布:")
    bins = [0, 0.05, 0.1, 0.2, 0.5, 1, 100]
    labels = ['<0.05', '0.05-0.1', '0.1-0.2', '0.2-0.5', '0.5-1', '>1']
    df_sorted['区间'] = pd.cut(df_sorted['量比'], bins=bins, labels=labels)
    dist = df_sorted['区间'].value_counts().sort_index()
    for label, count in dist.items():
        print("  %s: %d 只" % (label, count))
    
    print()
    print("=" * 100)
    print("  数据提取过程与参数说明")
    print("=" * 100)
    print()
    print("【数据源】")
    print("  - JQData (聚宽数据) get_call_auction() 接口")
    print("  - 接口文档: https://www.joinquant.com/help/api/help#name:api")
    print("  - 数据范围: 2026-02-09 至 2026-02-10")
    print()
    print("【股票池】")
    print("  - 沪深300成分股，20只代表性个股")
    print("  - 代码格式: JQData格式 (如 600519.XSHG, 000001.XSHE)")
    print()
    print("【计算公式】")
    print("  1. 量比 = 集合竞价每分钟成交量 / 近5日平均每分钟成交量")
    print("     其中: 集合竞价每分钟成交量 = 集合竞价总成交量 / 25分钟")
    print("           近5日平均每分钟成交量 = 近5日总成交量 / (5 × 240分钟)")
    print("  2. 集合换手率 = 集合竞价成交量 / 流通股本 × 100%")
    print("  3. 成交额量比 = 集合竞价每分钟成交额 / 近5日平均每分钟成交额")
    print()
    print("【输出字段】")
    print("  代码 | 名称 | 集合竞价成交价 | 集合竞价成交量 | 量比")
    print("  集合换手率 | 买一量 | 卖一价 | 集合竞价成交额")
    print()
    print("【当前限制】")
    print("  ⚠ JQData免费版数据截止2026-02-10，无法获取今日(2026-05-14)实时数据")
    print("  ⚠ 东方财富push2 API被公司防火墙拦截")
    print("  ✅ 深交所(szse.cn)公告API可正常访问")
    print("  ✅ 上交所(sse.com.cn)股票列表可正常访问")
    print()
    print("【获取今日实时数据的方案】")
    print("  方案A: 升级JQData会员 (约298元/年，支持实时数据)")
    print("  方案B: 配置网络代理访问东方财富push2 API")
    print("  方案C: 使用同花顺iFinD、Wind等专业终端")
    print("  方案D: 在开放网络环境下运行脚本")
else:
    print("未获取到数据")
