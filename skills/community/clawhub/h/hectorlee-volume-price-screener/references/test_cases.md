# 测试用例库（test_cases.md）

## 单元测试（pytest，31 用例，全部通过）

### 形态识别（tests/test_pattern_detect.py，15 用例）

| 用例 | 场景构造 | 预期 |
|:-----|:---------|:-----|
| test_standard_hit | 第45日放量+7%量比2.2，后14日缩量横盘 | 命中，锚点45 |
| test_insufficient_volume | 涨幅5%达标但量比1.2 | 不命中 |
| test_insufficient_surge | 量比2.5但涨幅3% | 不命中 |
| test_insufficient_shrink | 放量后仅1日缩量 | 不命中 |
| test_excessive_amplitude | 横盘期制造15%振幅K线 | 不命中 |
| test_gem_threshold | 涨幅7%创业板(<8%) | 不命中；同条件主板命中 |
| test_gem_threshold_boundary | 科创板恰好8% | 命中 |
| test_boundary_values | 恰好5%涨幅+1.5量比 | 命中（含等号） |
| test_multiple_anchors | 窗口内2根放量日 | 取最近锚点(50) |
| test_insufficient_data | 仅20根K线 | 不命中 |
| test_is_gem | 板块判定 | 300/301/688=True |
| test_rise_threshold | 板块涨幅阈值 | 主板5/创科8 |
| test_consecutive_signals | 窗口内构造3日量价齐升 | conc_rise_3d=True |
| test_divergence_warning | 横盘期放量滞涨 | 背离预警=True |
| test_low_point_rise | 后半段低点抬高 | low_point_rise=True |

### 风险过滤 + 评分（tests/test_risk_scoring.py，16 用例）

| 用例 | 场景 | 预期 |
|:-----|:-----|:-----|
| test_st_name_detection | ST/*ST 名称 | 识别正确 |
| test_check_st | ST华业 / 贵州茅台 | 排除 / 放行 |
| test_new_stock | 30根K vs 90根K | 剔除 / 放行 |
| test_one_word_limit | 放量日一字涨停 | 剔除 |
| test_not_one_word_limit | 正常放量日 | 放行 |
| test_consecutive_limit | 放量日前2日涨停 | 剔除（连板） |
| test_not_consecutive_limit | 正常走势 | 放行 |
| test_downtrend_rebound | 前10日-15%趋势 | 剔除（跌势反弹） |
| test_not_downtrend | 温和上涨 | 放行 |
| test_turnover | 2% / 5% / None | 剔除 / 放行 / 跳过 |
| test_comprehensive_st | 综合过滤含ST | 剔除 |
| test_comprehensive_turnover_skip | 无换手数据 | 放行+跳过标记 |
| test_comprehensive_pass | 全通过 | 放行 |
| test_score_standard | 标准命中评分 | 0<总分≤100 |
| test_score_components_bounds | 极端高分场景 | 各模块不超上限 |
| test_score_levels | 高质量 vs 低质量 | 高低分层正确 |

## 合成 K 线生成器（conftest.py）

`build_kline()` 参数化构造可复现的合成行情：

| 参数 | 默认 | 说明 |
|:-----|:----:|:-----|
| n | 60 | 总 K 线数 |
| anchor | 45 | 放量日索引 |
| surge_pct | 7.0 | 放量日涨幅(%) |
| vol_ratio | 2.2 | 量比 |
| post_days | auto | 横盘天数 |
| post_vol_ratio | 0.4 | 横盘量/放量日量 |
| post_amp | 0.005 | 横盘波动幅度 |
| trend | 0.005 | 放量前日涨幅 |
| base_vol | 1000 | 基础量 |
| base_price | 10.0 | 起始价 |

## 历史回测（设计方案 6.2 节，待实施）

- 区间：近 3 年逐日滚动全市场扫描
- 指标：命中率、命中后 5/10/20 日收益率 vs 沪深300、胜率、盈亏比
- 对照组：随机股票池同窗口收益 → 超额收益显著性检验
- 输出：命中分布 + 收益直方图 + 分位数报告

## 实盘金丝雀（设计方案 6.3 节，待实施）

- 连续 4 周每日实盘扫描，只输出不交易
- 与人工复盘对比确认逻辑一致
- 收集命中后 20 日走势，校准胜率

## 性能基准（设计方案 6.4 节）

| 场景 | 基准 | 实测 |
|:-----|:----:|:-----|
| 全市场4591只拉K线(90根,12并发) | < 3 分钟 | ~2 分钟 |
| 形态检测单只 | < 1ms | < 1ms |
| 单股诊断 | < 5s | ~0.5s |
