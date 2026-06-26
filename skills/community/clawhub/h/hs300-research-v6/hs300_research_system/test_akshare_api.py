import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
import akshare as ak
import pandas as pd

print("=" * 80)
print("  AKShare 核心接口数据质量测试")
print("  版本:", ak.__version__)
print("=" * 80)

test_results = []

# ========== 1. stock_zh_a_hist — 日K线 ==========
print("\n[1/8] stock_zh_a_hist — 个股日K线")
try:
    df = ak.stock_zh_a_hist(symbol="600519", period="daily", start_date="20260201", end_date="20260210", adjust="qfq")
    if df is not None and len(df) > 0:
        print("  状态: OK | 记录数: %d" % len(df))
        print("  列名:", list(df.columns))
        print("  样例:")
        print("  ", df.tail(2).to_string().replace('\n', '\n  '))
        test_results.append(('日K线', 'OK', len(df)))
    else:
        print("  状态: FAIL | 返回空数据")
        test_results.append(('日K线', 'FAIL', 0))
except Exception as e:
    print("  状态: ERROR | %s" % e)
    test_results.append(('日K线', 'ERROR', 0))

# ========== 2. stock_zh_a_spot_em — 实时行情 ==========
print("\n[2/8] stock_zh_a_spot_em — A股实时行情")
try:
    df = ak.stock_zh_a_spot_em()
    if df is not None and len(df) > 0:
        print("  状态: OK | 股票数: %d" % len(df))
        print("  列名:", list(df.columns))
        # 找几个典型股票
        sample = df[df['代码'].isin(['600519','000001','300750'])]
        if len(sample) > 0:
            print("  样例:")
            for _, row in sample.iterrows():
                print("  %s | %s | %.2f | %.2f%%" % (row['代码'], row['名称'], row['最新价'], row['涨跌幅']))
        test_results.append(('实时行情', 'OK', len(df)))
    else:
        print("  状态: FAIL | 返回空数据")
        test_results.append(('实时行情', 'FAIL', 0))
except Exception as e:
    print("  状态: ERROR | %s" % e)
    test_results.append(('实时行情', 'ERROR', 0))

# ========== 3. index_stock_cons_csindex — 沪深300成分股 ==========
print("\n[3/8] index_stock_cons_csindex — 沪深300成分股")
try:
    df = ak.index_stock_cons_csindex(symbol="000300")
    if df is not None and len(df) > 0:
        print("  状态: OK | 成分股数: %d" % len(df))
        print("  列名:", list(df.columns))
        print("  前5只:")
        for i, row in df.head(5).iterrows():
            code_col = [c for c in df.columns if '代' in c or 'code' in c.lower()]
            name_col = [c for c in df.columns if '名' in c or 'name' in c.lower()]
            code = row[code_col[0]] if code_col else ''
            name = row[name_col[0]] if name_col else ''
            print("  %s | %s" % (code, name))
        test_results.append(('沪深300成分股', 'OK', len(df)))
    else:
        print("  状态: FAIL | 返回空数据")
        test_results.append(('沪深300成分股', 'FAIL', 0))
except Exception as e:
    print("  状态: ERROR | %s" % e)
    test_results.append(('沪深300成分股', 'ERROR', 0))

# ========== 4. stock_financial_analysis_indicator — 财务指标 ==========
print("\n[4/8] stock_financial_analysis_indicator — 财务分析指标")
try:
    df = ak.stock_financial_analysis_indicator(symbol="600519")
    if df is not None and len(df) > 0:
        print("  状态: OK | 记录数: %d" % len(df))
        print("  列名:", list(df.columns)[:15], '...')
        print("  最近一期:")
        row = df.iloc[0]
        print("  日期:", row.get('报告期', row.iloc[0]))
        # 打印关键字段
        for col in df.columns:
            if any(k in col for k in ['净资产收益率', '总资产', '营业', '净利', '每股']):
                print("  %s: %s" % (col, row[col]))
        test_results.append(('财务指标', 'OK', len(df)))
    else:
        print("  状态: FAIL | 返回空数据")
        test_results.append(('财务指标', 'FAIL', 0))
except Exception as e:
    print("  状态: ERROR | %s" % e)
    test_results.append(('财务指标', 'ERROR', 0))

# ========== 5. stock_fhps_em — 分红送配 ==========
print("\n[5/8] stock_fhps_em — 分红送配")
try:
    df = ak.stock_fhps_em()
    if df is not None and len(df) > 0:
        print("  状态: OK | 记录数: %d" % len(df))
        print("  列名:", list(df.columns))
        print("  前3条:")
        print("  ", df.head(3).to_string().replace('\n', '\n  '))
        test_results.append(('分红送配', 'OK', len(df)))
    else:
        print("  状态: FAIL | 返回空数据")
        test_results.append(('分红送配', 'FAIL', 0))
except Exception as e:
    print("  状态: ERROR | %s" % e)
    test_results.append(('分红送配', 'ERROR', 0))

# ========== 6. stock_individual_fund_flow — 个股资金流 ==========
print("\n[6/8] stock_individual_fund_flow — 个股资金流向")
try:
    df = ak.stock_individual_fund_flow(stock="600519", market="sh")
    if df is not None and len(df) > 0:
        print("  状态: OK | 记录数: %d" % len(df))
        print("  列名:", list(df.columns))
        print("  最近3日:")
        print("  ", df.tail(3).to_string().replace('\n', '\n  '))
        test_results.append(('个股资金流', 'OK', len(df)))
    else:
        print("  状态: FAIL | 返回空数据")
        test_results.append(('个股资金流', 'FAIL', 0))
except Exception as e:
    print("  状态: ERROR | %s" % e)
    test_results.append(('个股资金流', 'ERROR', 0))

# ========== 7. stock_board_concept_hist_em — 概念板块 ==========
print("\n[7/8] stock_board_concept_hist_em — 概念板块历史行情")
try:
    # 先获取概念板块列表，取第一个测试
    board_df = ak.stock_board_concept_name_em()
    if board_df is not None and len(board_df) > 0:
        first_board = board_df.iloc[0]
        code_col = [c for c in board_df.columns if '代' in c or 'code' in c.lower()]
        name_col = [c for c in board_df.columns if '名' in c or 'name' in c.lower()]
        code = first_board[code_col[0]] if code_col else ''
        name = first_board[name_col[0]] if name_col else ''
        print("  测试板块: %s (%s)" % (name, code))
        df = ak.stock_board_concept_hist_em(symbol=code)
        if df is not None and len(df) > 0:
            print("  状态: OK | 记录数: %d" % len(df))
            print("  列名:", list(df.columns))
            print("  最近3日:")
            print("  ", df.tail(3).to_string().replace('\n', '\n  '))
            test_results.append(('概念板块', 'OK', len(df)))
        else:
            print("  状态: FAIL | 返回空数据")
            test_results.append(('概念板块', 'FAIL', 0))
    else:
        print("  状态: FAIL | 无法获取板块列表")
        test_results.append(('概念板块', 'FAIL', 0))
except Exception as e:
    print("  状态: ERROR | %s" % e)
    test_results.append(('概念板块', 'ERROR', 0))

# ========== 8. stock_lhb_detail_em — 龙虎榜 ==========
print("\n[8/8] stock_lhb_detail_em — 龙虎榜详情")
try:
    df = ak.stock_lhb_detail_em(start_date="20260209", end_date="20260210")
    if df is not None and len(df) > 0:
        print("  状态: OK | 记录数: %d" % len(df))
        print("  列名:", list(df.columns))
        print("  前3条:")
        print("  ", df.head(3).to_string().replace('\n', '\n  '))
        test_results.append(('龙虎榜', 'OK', len(df)))
    else:
        print("  状态: FAIL | 返回空数据")
        test_results.append(('龙虎榜', 'FAIL', 0))
except Exception as e:
    print("  状态: ERROR | %s" % e)
    test_results.append(('龙虎榜', 'ERROR', 0))

# ========== 汇总 ==========
print("\n" + "=" * 80)
print("  测试汇总")
print("=" * 80)
ok_count = sum(1 for r in test_results if r[1] == 'OK')
fail_count = sum(1 for r in test_results if r[1] in ('FAIL', 'ERROR'))
for name, status, count in test_results:
    icon = 'OK' if status == 'OK' else 'FAIL'
    print("  [%s] %s — 记录数: %d" % (icon, name, count))
print("-" * 80)
print("  通过: %d/%d | 失败: %d/%d" % (ok_count, len(test_results), fail_count, len(test_results)))
