# 法律计算器流程

## 处理上传案件材料

用户在当前任务上传事故认定书、病历、鉴定意见、医疗票据、工资证明或其他文件时，先读 `references/case-materials.md`。调用 `case-materials`，或把当前任务的 `filePaths` 和宿主生成的 `extractedTexts` 直接传给 `catalog`、`question-start`。材料会保存在当前任务的 `interaction.caseContext`，用于自动回答地区、责任、年龄、伤残等级、金额、期限、收入等题目。`query` 必须忠实使用当前任务中用户的本次表达，禁止用全局记忆、其他任务、其他线程、旧案例或示例扩写。

材料中没有明确数值时不得自行估算；多个票据或材料数值冲突时先让用户确认。脚本返回 `stage=needs_material_extraction` 时必须先读取未解析文件，不得静默跳过。

## 选择计算器

将以下数据传给 `catalog`：

```json
{"capability":"calculator","query":"养老保险待遇测算"}
```

技能调用 `/app/projects/{appId}` 时固定传 `m=1`。计算器包括赔偿、费用以及社会保险待遇测算；养老保险相关请求应以用户原话查询目录，并从返回的企业职工养老保险、基础养老金、个人账户养老金、过渡性养老金或退休待遇等具体项目中选择。目录和项目编号都以接口返回为准；结合 `parentName`、`name` 和 `displayName` 选择项目，不选择仅用于分组且没有 `projectId` 的父级节点。

`catalog` 返回完整目录，不做关键词排序或截断。每个候选只有 `id` 和 `displayName` 两个字段，`displayName` 形如“父级领域 > 具体项目”，已经包含打分所需的全部信息；内部编号、分类和价格默认不下发，需要完整记录时在输入里加 `"verbose": true`。必须由宿主大模型结合用户原话与候选的 `displayName` 做语义打分，不得按分词结果、关键词命中数量或目录原始顺序选择。仅当第一名的语义置信度不低于 `0.85`、且比第二名高至少 `0.15` 时，才直接以该候选的 `id` 作为 `projectId` 调用 `question-start`；否则把 2 至 4 个确实存在于 `data.candidates` 中的项目交给用户确认，或只问一个能区分它们的简短问题，不得把“不清楚”“其他”当作默认项。脚本会在 `data.selection` 中回传该判定门槛。

## 开始逐题计算

```json
{
  "capability":"calculator",
  "projectId":"从目录取得的 id",
  "query":"用户原始问题",
  "filePaths":["/绝对路径/病历.pdf","/绝对路径/医疗票据.png"],
  "extractedTexts":[
    {"filePath":"/绝对路径/病历.pdf","text":"从病历忠实提取的诊疗信息"},
    {"filePath":"/绝对路径/医疗票据.png","text":"票据识别出的项目和金额"}
  ]
}
```

传给 `question-start`。脚本与法律咨询报告统一调用 `/question/answer`，每次只取得当前一道题，不再调用 `/question/form`，也不在大模型侧维护计算表单分页。题目返回后只用当前任务消息、当前任务材料、当前 `sessionId` 已保存答案和当前任务更正尝试自动回答；只有没有可靠答案时才展示给用户。

## 逐题回答

先按 `references/interaction.md` 匹配当前任务证据。例如用户在当前任务已明确“对方全责、医疗费四万元”，对应题目出现时直接提交现有选项或规范化数值。禁止读取或使用全局记忆、其他任务、其他线程、旧案例或示例。当前 `fields[0]` 在当前任务中没有唯一匹配时，直接调用 `interaction.native.batches[0]`；普通填空题已由脚本转换为带 2 至 4 个建议选项的标准 `single_select`，宿主不得再次生成候选。多填题每轮只处理一个字段，全部回答完成前不提交后端。非必填空姓名、电话、手机号、身份证号、证件号码由脚本跳过；居住地、户籍地等地区字段必须保留。若当前任务明确排除了某个条件类别，字段会返回 `notApplicable=true` 并以空值推进，不能强行填零或选择默认数量；单纯未提到该类别仍需询问。渲染时按 `optionManifest` 核对选项完整性。

用户回答当前一道题后，将字段传给 `question-reply`：

```json
{
  "sessionId":"任务编号",
  "answers":{
    "字段键":"字段值"
  }
}
```

没有追加题时，脚本会把当前答案提交给 `/question/answer` 并返回下一题；继续只用当前任务证据自动作答。若所选选项包含追加题，脚本先返回 `stage=needs_follow_up`，仍先尝试用当前任务证据回答新的追加题，确实缺少答案时才一次显示一道；继续使用同一 `sessionId` 调用 `question-reply`。追加题全部完成前不会调用后端，完成后脚本才把主答案和各追加答案放回完整父题节点并一次提交。

重复此过程，直到 `stage=ready_for_report`。如果返回 `needs_input`，先再次用当前任务证据匹配 `data.missing` 指明的所有未回答内容，仍缺失时按 `interaction.renderPlan.units` 逐项询问；影响计算的普通非必填字段不能跳过，只有非必填空敏感字段或明确 `notApplicable` 的条件字段可由脚本直接跳过，居住地和户籍地等地区字段除外。如果返回 `needs_follow_up`，同样先尝试用当前任务证据回答当前追加题。每轮最多向用户展示一道未解决题，不一次性展开后端题目或当前选项下的多道追加题。

## 计算和报告

`stage=ready_for_report` 后调用 `question-report`。

最终展示总额、分项金额、计算依据、关键参数，并在同一轮原样输出 `data.delivery.markdown`，固定显示为 `[法律计算报告](链接地址)`。上述内容只能来自本次计算报告及报告中已经列出的法规和依据；不得在报告生成后搜索网页、查询法律数据库或补充报告外的计算规则、法规、案例或结论。该链接必须在生成当轮出现，不得等用户再次索取。`data.delivery.autoOpen=true`，发出链接后立即用宿主可用的浏览器或导航能力打开 `data.delivery.url`；宿主没有该能力时仍必须发出链接，用户在网页中自行决定是否下载离线报告。

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
