# 历史错误复盘（参考）

## Error 1：品牌级数据从Excel解析而非从raw_records
- 问题：brand_audit 从Excel解析，跳过首列空白的记录
- 后果：202308魅KTV只捕获1/4条，萱昀商贸只捕获部分
- 规则：品牌级数据必须从 `raw_records` 逐行GROUP BY计算

## Error 2：中快系列支付宝间连返佣被忽略
- 问题：中快Sheet第16列"支付宝间连返佣"未提取
- 后果：中快餐饮所有月份差异为+间连金额
- 规则：中快记录直接用 total_rebate（包含间连）

## Error 3：异常表数据被错误计入重算
- 问题：异常表记录直接加到brand_audit重算中
- 规则：calc_method=abnormal 默认不计入，仅 audit_note=历史差额调整 的补充

## Error 4：SUM(txn)×SUM(ratio) 而非逐行ROUND
- 问题：GROUP BY后 SUM(txn)×SUM(ratio) 导致重算膨胀数倍
- 规则：必须逐行 ROUND(txn×ratio,2) 再按品牌SUM

## Error 5：品牌级与月度重算逻辑不一致
- 规则：每个calc_method的处理方式必须与 batch_summaries.py 保持统一

## Error 6：大客户品牌映射失效
- 问题：brand="大客户" 未映射到实际品牌
- 修复：取level1_name作为实际品牌，修改解析器后需重新解析对应月份

## Error 7：异常及调账Sheet全局误判+区块标题遗漏
- 问题：（1）sheet名含"调账"→全表标记为调账（2）A列区块标题未被识别
- 修复：逐行判断，不依赖sheet名；增加section_note追踪机制

## Error 8：Excel列顺序错误
- 当前顺序（2026-05-11更新）：月份 | 品牌 | 原始表金额 | 审计重算金额 | 汇总表金额 | 差额 | 审计备注

## Error 9：少发记录未排除
- 规则：diff_note LIKE '%少发%' 的记录从明细和摘要中排除

## Error 10：数据已修改但未重新解析
- 规则：修改解析器后必须 DELETE+重新解析受影响月份

## Error 11：corrected_fail/real_diff阈值使用0.01
- 问题：舍入误差（0.01~0.53）被误判为差异，16个月误标记
- 规则：两处阈值统一为 > 1 或 > 100

## Error 12：历史调整金额只取了已知3个品牌
- 规则：KNOWN_HIST_ADJ只用于3个特殊品牌，其他从audit_note记录独立计算

## Error 13：统计阈值只改了一处
- 规则：修改阈值时检查 corrected_real_diff 和 diff_months 两处

## Error 14：审计摘要items数变更后行号未对齐
- 规则：修改items列表后必须检查correction块引用的行号