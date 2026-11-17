# 法律咨询报告流程

## 处理上传案件材料

用户在当前任务上传文件时先读 `references/case-materials.md`。调用 `case-materials` 提取内容，或把当前任务的 `filePaths` 与宿主生成的 `extractedTexts` 直接传给 `catalog` 和 `question-start`。材料内容要参与项目选择，并在任务创建后保存在每一道题的 `interaction.caseContext` 中。`query` 必须忠实使用当前任务中用户的本次表达，禁止用全局记忆、其他任务、其他线程、旧案例或示例扩写。

PDF、Word、表格和图片没有 `extractedTexts` 时，脚本会返回 `stage=needs_material_extraction`；先用宿主文件工具读取后重试，不得跳过附件继续问卷。

## 获取项目

```json
{"capability":"consultation","query":"离婚财产"}
```

传给 `catalog`。从 `data.candidates` 中选择最匹配项目；存在实质歧义时让用户确认。

技能调用 `/app/projects/{appId}` 时固定传 `m=2`。返回数据含父子关系，候选项中的 `parentName` 是父级法律领域，`name` 是具体项目，`displayName` 按“父级领域 > 具体项目”组合。选择时同时匹配两级名称，并忽略没有 `projectId` 的分类节点。

`catalog` 返回完整目录，不做关键词排序或截断。每个候选只有 `id` 和 `displayName` 两个字段，`displayName` 形如“父级领域 > 具体项目”，已经包含打分所需的全部信息；内部编号、分类和价格默认不下发，需要完整记录时在输入里加 `"verbose": true`。必须由宿主大模型结合用户原话与候选的 `displayName` 做语义打分，不得按分词结果、关键词命中数量或目录原始顺序选择。仅当第一名的语义置信度不低于 `0.85`、且比第二名高至少 `0.15` 时，才直接以该候选的 `id` 作为 `projectId` 调用 `question-start`；否则把 2 至 4 个确实存在于 `data.candidates` 中的项目交给用户确认，或只问一个能区分它们的简短问题，不得把“不清楚”“其他”当作默认项。脚本会在 `data.selection` 中回传该判定门槛。

## 开始咨询

```json
{
  "capability":"consultation",
  "projectId":"从目录取得的 id",
  "query":"用户原始问题",
  "filePaths":["/绝对路径/判决书.pdf"],
  "extractedTexts":[
    {"filePath":"/绝对路径/判决书.pdf","text":"从判决书忠实提取的案情文字"}
  ]
}
```

传给 `question-start`。保存返回的 `sessionId`。题目通过 `/question/answer` 逐题获取。

## 回答问题

先按 `references/interaction.md` 匹配当前任务证据。当前 `fields[0]` 在当前任务内有直接、明确、唯一答案时立即调用 `question-reply`；禁止读取或使用全局记忆、其他任务、其他线程、旧案例或示例。当前任务内没有匹配时直接调用 `interaction.native.batches[0]`，不先解释。普通填空题已由脚本转换为带 2 至 4 个建议选项的标准 `single_select`，宿主不得再次生成候选。多填题和追加题每轮只处理一个字段，全部回答完后脚本才提交完整父题。非必填空姓名、电话、手机号、身份证号、证件号码由脚本跳过；居住地、户籍地等地区字段必须保留。若当前任务明确排除了某个条件类别，字段会返回 `notApplicable=true` 并以空值推进，不能强行填零或选择默认数量；单纯未提到该类别仍需询问。渲染时按 `optionManifest` 核对选项完整性。

```json
{
  "sessionId":"任务编号",
  "answers":{"字段键":"答案"}
}
```

传给 `question-reply`。连续自动处理当前任务中已有明确答案的新问题，直到遇到确实缺失的字段或 `stage=ready_for_report`。

如果选项包含追加题，`question-reply` 会先返回 `stage=needs_follow_up`，并把追加题放在新的 `interaction` 中。此时仍只用当前任务证据自动回答；无法自动回答时才一题一页呈现。继续使用同一 `sessionId`，不要调用其他命令，也不要自行请求后端下一题。全部追加题完成后，脚本会把答案写回所选选项的 `add` 节点，并将包含主答案与追加答案的完整父题一次提交给 `/question/answer`。

例如“您是男方还是女方？”选择“男方”后触发“您的年龄是多少？”时，第一次 `question-reply` 只保存“男方”并返回年龄题，不调用后端；用户填写年龄后再次调用 `question-reply`，脚本才把性别和年龄一起提交。

咨询题目可能随答案分支变化，因此展示当前主题和后端返回的进度，不承诺固定题目总数。

## 生成报告

```json
{"sessionId":"任务编号"}
```

传给 `question-report`。最终回复包含：

- 核心结论
- 主要法律分析
- 建议采取的行动
- 相关法规和案例
- Markdown 超链接 `data.delivery.markdown`，固定显示为 `[法律咨询报告](链接地址)`

最终摘要、关键结论、法律分析、行动建议和法规案例只能来自本次报告正文及报告中已经列出的法规和案例。报告生成后不得再搜索网页、查询法律数据库或调用其他外部检索，不得补充报告未包含的法律依据；与模型既有知识冲突时以报告为准。

该链接必须在报告生成当轮的用户可见回复中原样出现，不得等用户再次索取。`data.delivery.autoOpen=true`，因此发出链接后要立即用宿主可用的浏览器、网页打开或导航能力打开 `data.delivery.url`；宿主没有该能力时仍必须发出链接，由用户点击查看，并在网页中自行决定是否下载离线报告。

## 题目取值契约

后端对不同题型的取值形状要求不同，脚本会按题目的 `component` 和 `config` 自动转换，
宿主直接提交用户的原始写法即可，但提问时要问到正确的粒度。字段上的 `valueContract` 说明了这一点：

| 题型 | `valueContract.submit` | 提问要点 |
| --- | --- | --- |
| 日期 | `unix_seconds` | `granularity` 为 `year_month` 时只问到年月，不要追问"哪一天" |
| 日期区间 | `range_object` | 同时问开始和结束日期 |
| 地区 | `area_id` | 必须问到 `areaLevel` 指定的层级：1 只到省，2 到省市，3 到省市区县 |
| 数值加单位 | `value_unit_object` | 单位只能取 `units` 中列出的值 |

地区题的取值是后端地区表里的 id。脚本会把"云南省昆明市""云南昆明""杭州"这类写法解析成对应 id；
解析不出来时返回 `AREA_NOT_MATCHED`，`error.details[].candidates` 是该层级真实存在的地区，
必须把这些候选交给用户选择，不能改写或猜测地名后重试。
