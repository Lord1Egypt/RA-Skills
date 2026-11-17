# 多语言质量评测

新增 `critique`（只诊断）、`compare-blind`（随机 A/B 提示和独立版本密钥）及
`evaluate-editorial`（人工评票汇总）。盲评时仅发送 `comparison.md`，评审不能知道
修改历史；允许原稿胜出、平局与证据不足。六项评分为原意、声音、可读性、冗余控制、
事实支持和修辞克制。无评票为 pending，不提供质量证据；母语评审记录需两位
独立评审和材料来源。完整数据格式见[编辑质量评估](editorial-evaluation.md)。
当前没有附带真实母语编辑评票，工具不会调用模型或自动编造评分。

`evaluate` 可以运行带标签的本地 JSON 样例集。仓库附带的
`tests/fixtures/quality/multilingual-benchmark.json` 是**开发者编写的种子用例**，
只用于发现规则回归，不能据此宣称真实世界准确率或母语编辑质量。

```powershell
human-writing-skills evaluate --cases tests/fixtures/quality/multilingual-benchmark.json
```

每条用例需要唯一 `id`、`kind`、`language`、`genre`、`review_status` 和
`expected`。`serious-detection` 用 `text` 检查严肃文体的自动触发，期望值为
布尔值；`fidelity` 用 `source` 和 `candidate` 检查改写风险分流，期望值为
`pass-exact`、`needs-review` 或 `fail-literal`。后者不是自动判定“语义一致”。

## 母语盲审录入规则

1. 分语言和文体收集合法可用的自然文本，同时收录含数字、引文、破折号、学术词
   的小说等反例。不要把受版权或隐私保护的全文直接提交到公开仓库。
2. 至少两名熟悉该语言和文体的审稿人独立标注，不先展示程序判断；分歧另行裁定。
3. 改写对照单独标注主体、否定、可能性、适用范围、归因、时间顺序、来源支持、
   信息遗漏，以及只是换词的无害变化。必须包含“数字和引文完全未变，但意思变了”的反例。
4. 经独立复核后才把 `review_status` 设为 `native-reviewed`，并填写
   `reviewer`（匿名 ID 即可）、`annotation_date` 和 `source_provenance`。
5. 按语言与文体分别报告样本量、精确率、召回率、误报和漏报；样本很少时不要
   合并宣传一个总准确率。规则修改后重跑，并保留有意复沓、方言、正式语体、
   语码切换和刻意含混的反例。

种子用例跑出 `21/21` 只说明这些具体示例没有回归，不是经母语盲审的有效性结论。
