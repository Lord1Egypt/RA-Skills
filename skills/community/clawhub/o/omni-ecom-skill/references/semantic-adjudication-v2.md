# 2.0：口径和趋势裁决

遇到 caliber 或 direction 类型的 hard 冲突，先完成 [定向质疑](challenge-round-v2.md)，再使用以下裁决方式。数据质量、深度和真实回传要求不因新增裁决方法而跳过。此校验核对声明口径和来源，不证明数据来自真实平台，也不把趋势计算当成因果证明。

## 调度前的计算口径

在 baseline-pack.json 的对应 metric_contract 中，明确 definition、formula、unit、denominator、dedupe_rule、attribution_window，并增加 calculation。例为转化率的百分数展示：

```json
{
  "expression": "buyers / visitors * 100",
  "inputs": {
    "buyers": {"source_field":"支付买家数","unit":"人","aggregation":"value"},
    "visitors": {"source_field":"访客数","unit":"人","aggregation":"value"}
  }
}
```

这是 `calculation` 字段内容，不是完整基线。unit=% 输出 20 表示 20%；unit=ratio 输出 0.2。金额元/人和 ROAS 倍数也必须明确。字段映射由当前原始报表确定，不照搬示例列名。JSON 来源的 source_field 写明确指针，例如 `/buyers`。

已支持明确公式：GMV=gmv，访客=visitors，转化率=buyers/visitors，客单价=gmv/buyers，退款率=refund_amount/gmv，ROAS=attributed_gmv/ad_spend，UV价值=gmv/visitors，净销售=gmv-refund_amount，ROI=profit/total_cost。比例指标只接受 ratio 或 %；ROI 必须另有 profit_scope 和 total_cost_scope，且利润、总成本来自实际财务来源。没有花费不算 ROAS，没有成本不算利润 ROI。不同定义或未支持的指标不可硬套名称，应保持待确认并补充对应契约。

人数只接受原始期间去重汇总值，不允许通过 sum 加总日访客或多个商品访客代替期间去重人数。金额允许明确的 value 或 sum。基线应在派工前下发，变更后必须按新基线重新分析和质疑，不能只更新旧回执哈希。

## 裁决字段

裁决文件本身使用 `omni-ecom.conflict-verdict@2.0`，其 client_scope、run_id、team_version、report_revision 必须与当前报告一致；旧 1.0 裁决只可阅读，不能投影到当前报告或作为质量复算依据。verdicts 中的一项保留 conflict_id、decision、not_adopted_disposition、residual_risk、challenge_review、downstream，以及没有下游时的 no_downstream_reason。新增：

- method：口径冲突用 `caliber_recomputation`，方向冲突用 `trend_recomputation`。
- metric、unit：与扫描冲突和基线一致。
- baseline_sha256：确切基线文件指纹。
- current：本期 measurement；趋势还必须有 previous。
- 趋势另填 direction（up/down/flat）和 comparability_note，说明天数、活动节奏及对比限制。

measurement 示例：

```json
{
  "period":"2026-07",
  "value":20,
  "inputs":{
    "buyers":{"report_id":"R001","file":"原表.csv","sha256":"实际指纹","column":"支付买家数","rows":[0],"aggregation":"value","period_column":"月份"},
    "visitors":{"report_id":"R001","file":"原表.csv","sha256":"实际指纹","column":"访客数","rows":[0],"aggregation":"value","period_column":"月份"}
  }
}
```

period 支持明确年、月、日，或 `{start:"YYYY-MM-DD",end:"YYYY-MM-DD"}`。程序读取所选原始行的期间列，核对其覆盖完整期间；选了六月的数据不能只改 period 标签说是七月。CSV 目前要求第一行为表头；Excel 使用明确 sheet 和一基 header_row；rows 从表头后的第一条数据按零计数。JSON 使用数值 pointer 和 period_pointer。原表期间不明确或缺日时不能伪造完整比较，应补数据或明确改为有证据的范围。

report_id 必须出现在报表清单，清单 file_path、sha256 必须对应同一个当前来源。只碰巧文件同名不算匹配。当前期间必须与基线 scope.period 一致；对比期必须在当前期之前且不重叠。可以比较长度不同的自然月，但必须解释限制，并展示实际天数。

## 同步报告并复核

report.adjudicated_claims[conflict_id] 写入 metric、unit、value、period、baseline_sha256、caliber_sha256（该指标完整契约的规范 JSON SHA256，使用 adjudication_guard.fingerprint）。趋势另外写 previous_value、previous_period、direction、absolute_change、comparability_note、current_days、previous_days。

absolute_change 是本期减对比期，单位与原指标相同；百分数转化率的差值是百分点，不是相对增幅。下游公式可引用 adjudicated、previous、change，以及 previous_ 前缀的对比期输入；列出的结果必须同步 report.adjudicated_downstream。

正文/PDF 中的结论也应更新，交付复核员需要逐项对照冻结清单。程序当前核对结构化裁决，不声称能凭字段一致证明整篇自然语言正确。因果互斥、样本不足或不能比较的问题仍需证据审查，不能把这个模块的通过当成因果结论。

## 生成用户可见的裁决章节

调用 build_report_package.py 时传入 `--decision-pack 本次裁决.json`。该文件保留本次 run_id/client_scope/team_version/report_revision、verdicts，并同时包含 adjudicated_claims、adjudicated_downstream、unresolved_conflicts。quality-inputs.json 的 adjudication 指向同一份裁决文件。

生成器只把裁决结论、限制、未采纳意见及专家回复处理映射到公开报告，不复制复算输入路径或宿主观察。Markdown 与 PDF 使用同一展示逻辑；PDF 短裁决尽量保持完整一页，长裁决允许自然分页。质量检查会核对已展示的 adjudication_summary 与裁决文件一致。导入成功或展示成功不代表验证通过，仍须原始数据、质疑、冻结及独立复核。

尚未传入 decision-pack 的旧调用不会自动补出裁决展示，也不能以此视为完整 2.0 报告验收。最终发布整合须确保实际调度流程传入该文件，并检查整篇正文、图表和数字索引是否已同步，不能只看新增章节。
