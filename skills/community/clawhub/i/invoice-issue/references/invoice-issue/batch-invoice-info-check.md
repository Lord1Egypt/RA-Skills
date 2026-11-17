# 场景：invoice-issue-batch-invoice-info-check（批量开票信息检查与 JSON 生成）

## 模板用途

用于在正式开票前，对一批发票信息进行逐张提取、逐张完整性检查、字段标准化与批量 JSON 草稿生成。

本场景只负责两件事：

1. 从用户输入中提取多张可落入开票接口的数据；
2. 产出 1 个可供后续批量预览或正式开票使用的标准化 JSON，其中 `info` 为数组。

本场景不直接发起 HTTP 请求。

## 二进制 CLI 实现

本场景必须通过已打包的 `invoice-assistant` 二进制执行。Windows 环境优先使用：

```bash
.\bin\windows-amd64\invoice-assistant_windows_amd64.exe issue-batch-invoice-info-check --input <临时输入文件>.json --pretty
```

Linux 环境使用：

```bash
./bin/linux-amd64/invoice-assistant_linux_amd64 issue-batch-invoice-info-check --input <临时输入文件>.json --pretty
```

Linux arm64 环境使用：

```bash
./bin/linux-arm64/invoice-assistant_linux_arm64 issue-batch-invoice-info-check --input <临时输入文件>.json --pretty
```

二进制内部会统一维护：

- `ISSUE_TASK_STATE_DIR`：任务状态 JSON 目录
- `CURRENT_ISSUE_TASK_POINTER_PATH`：当前任务路径指针文件

执行规则补充：

1. 本场景必须优先使用上面的二进制命令执行，不得擅自改成源码命令。
2. 本场景会复用单张检查能力逐张生成标准化结果，该能力已经打包进 `invoice-assistant` 二进制。
3. 只有在目标平台二进制明确不可用时，才允许报告无法执行；不得自行回退到源码路径。
4. 本场景是“新开票任务”的唯一建档入口。只要用户当前消息里出现新的开票内容，就必须重新准备 input JSON 并重新执行本命令创建新的任务状态 JSON；不得在执行本命令前先读取旧的 `CURRENT_ISSUE_TASK_POINTER_PATH`，再用历史任务结果代替本次检查。
5. 只有当用户明确是在继续刚才同一批发票任务，例如“确认开票”“继续上一条预览”“查看刚才开票结果”时，才允许继续使用已经创建好的当前任务指针；若无法确定，默认按新任务处理并重新建 task。
6. 正式开票前必须先生成并展示本次任务对应的开票预览，等待用户明确确认开票后，才允许调用 `issue-from-output` 等正式开票脚本；不得未经过预览、未取得用户确认，就直接发起开票。

## 输入约束

批量场景的原始输入必须是单个 JSON 对象，而不是顶层数组。原始输入统一使用以下结构：

```json
{
  "uscc": "销售方税号",
  "invoices": [
    { "invoiceType": "普通发票", "purchaserInfo": {}, "details": [] },
    { "invoiceType": "增值税专用发票", "purchaserInfo": {}, "details": [] }
  ]
}
```

其中：

1. 顶层统一使用 `invoices[]` 承载发票对象。
2. 每张发票的原始明细统一使用 `details[]` 承载；金额、单价、税率、税额等字段都应写在 `details[]` 内，不在原始输入阶段写入 `invoiceDetail.data[]`。
3. 脚本标准化后会将 `invoices[].details[]` 转换为正式 payload 中的 `info[].invoiceDetail.data[]`。

禁止把以下结构作为本命令原始输入：`params.info[]`、`params.goods[]`、`params.purchaserName`、`params.projectName`、顶层 `info[]`、`invoice_payload_json.info[]`、`invoiceDetail.data[]`。这些要么是其他场景的包装方式，要么是脚本标准化后的正式 payload 结构；正常开票检查只能从顶层 `invoices[]` 和每张票的 `details[]` 进入。

适用规则：

1. 顶层共享字段当前只强制要求 `uscc`；`areaCode`、`personalAccount` 会在 input JSON 转 task JSON 阶段按 `uscc` 从 `.invoice-config/workspace-config.json` 的 `companyInfo[uscc]` 中补齐，并写入任务状态 JSON 的 `raw_input_json`，再由批量脚本复用到每张发票。若配置文件不存在，会在首次读取时自动创建默认配置文件。若用户已知纳税人类型，也可在顶层额外提供 `taxpayerType`，仅用于后续税率自动匹配，不写入正式开票 payload。
2. 每张发票仍必须独立满足接口字段要求；不得因为属于同一批就省略本应逐张校验的业务字段。
3. 若某一值只对其中一张发票成立，不得写到批量顶层共享字段。
4. 若用户通过编号列表、换行段落或分号段落连续给出多组“商品/金额/税率/发票类型/购方”等信息，应按“每组可独立成票的信息 = 1 张发票”拆分为批量输入，不得误并入单张发票的多条明细。
5. 开票场景下，用户输入的金额与单价在批量场景中同样默认按含税口径识别；不得自动改判为不含税金额/单价。
6. 对普通零税率，用户在原始输入阶段写成 `0` 或 `0%` 均可，均应识别为 `taxRate` 的合法输入。
7. 对“免税”“不征税”，用户在原始输入阶段必须将原始名称直接写入对应明细的 `taxRate`；不得在 input JSON 阶段预先改写为 `0`、`0%` 或其他数值税率，这一步只能由后续脚本标准化完成。
8. 涉及煤炭相关明细时，Skill 必须在原始输入转 input JSON 阶段补出 `mtzlDm`；可接受用户直接提供编码，或提供可唯一映射的标准名称后按煤炭种类字典转换。当前允许的标准映射为：`政府保供煤 -> 0100`、`市场煤 -> 0300`、`长协煤-协议期不足半年 -> 0201`、`长协煤-协议期在半年至一年之间 -> 0202`、`长协煤-协议期在一年至两年之间 -> 0203`、`长协煤-协议期在两年以上 -> 0204`。同时，煤炭类明细的 `unit` 不得为空，且仅允许 `吨`、`千克（公斤）`。
9. 除用户明确输入可识别字段外，Agent 不得为任一发票自行推理并补写其他开票字段；缺失字段必须交由批量检查命令自动补全并做完整性校验。税率缺失时同样先交由命令处理，不得在编排层直接追问或臆断常见税率；若用户没有明确说明税率，也不得在 input JSON 阶段把 `taxRate` 识别成“免税”“不征税”或其他具体税率。
10. 若用户提供的是图片、扫描件、截图、PDF、Excel、Word 或其他文件并要求据此开票，Skill 必须先从文件中提取出每张发票可落位的关键字段，整理成文字版结果后，再写入批量 input JSON；不得把原始文件内容未经提取直接映射为结构化字段。
11. 批量 input JSON 中允许出现的 key，必须严格限定在本场景声明的原始输入结构内，并且这些 key 必须能稳定映射到 [issue.md](issue.md) 的请求字段语义；对非关键字段，若无特殊说明，允许缺失，但不得额外生成 `items`、`invoiceDetails`、`buyerName`、`taxAmount`、`extra`、`metadata` 等脚本未声明支持的 key。

## Skill 与二进制 CLI 串联步骤

### Step 1. 准备原始输入

Skill 必须先把当前已提取到的字段组织为 1 个 JSON 对象。

写入内容要求：

1. 顶层共享字段至少写入 `uscc`；若上游已明确带出 `areaCode`、`personalAccount` 也可保留，但默认由脚本按 `uscc` 从配置补齐。
2. 多张发票应统一写入 `invoices[]`，不得拆成多次单张调用后再在编排层自行拼接。
3. 每张发票的购方、明细、备注等字段必须只落到对应项中，不得跨票复制。
4. 若用户明确提供“备注”，原始 input JSON 中必须写入对应发票的 `noteInfo.note`；不得改写为 `remark`、`remarks`、`memo` 等别名，也不得放到批量顶层或发票对象顶层。
5. 不得写入示例值或占位符冒充用户真实输入。
6. 若存在 2 个候选值但无法确定它们分别属于哪张发票，应保留缺失并继续追问，而不是擅自按顺序分配。
7. 若用户原始输入采用“1. ... 2. ... 3. ...”等编号形式，且每段都能独立识别出商品、金额、税率或票种等核心信息，Skill 必须先按段拆成多张发票后再写入 `invoices[]`。
8. 煤炭相关明细的 `mtzlDm` 只能在编排层按煤炭种类字典做精确识别与转换，不得手工猜测最相近编码。若用户输入仅为“长协煤”“普通煤”“常见煤种”等无法唯一映射的描述，或未提供单位、单位不是 `吨`/`千克（公斤）`，必须在写入 input JSON 前追问澄清，不得保留到后续步骤再处理。
9. 若用户明确提供“折扣”“折扣比例”，应先将其归一化为百分比数值后写入对应明细的 `discountInfo.discount`，例如 `0.5 -> 50`、`50% -> 50`、`88折 -> 88`、`12.5% -> 12.5`。若明确提供“折扣金额”“优惠金额”，应写入对应明细的 `discountInfo.discountAmount`。若用户只表达“有折扣”但未给出比例或金额，必须在写入 input JSON 前追问，不得直接忽略。
10. 除用户输入中明确可识别字段外，不得在编排层新增推理字段；所有待补字段一律由脚本补全并通过 `check_result` 校验后再进入后续流程。
11. 对任一发票中用户未明确提供的字段，禁止写入 `0`、`0.00`、`"0"` 等默认占位值；尤其金额、单价、税额、数量等数值字段不得以 `0` 占位，必须保持缺失并由脚本补全与校验。
12. 对非必填字段，若用户未提供、且当前也未从图片或文件中无歧义识别出该字段，Skill 在生成 input JSON 阶段可直接保持缺失，不需要反复追问；但只要用户已明确提供，或文件/图片中已稳定识别出且能够无歧义落位，即使属于可选字段，也必须写入 input JSON，避免遗漏。例如 `purchaserInfo.uscc` 在普通发票场景下虽属于可选字段，但用户若已给出，或文件中已明确识别出该值，就必须写入；同理，购方地址、电话、开户行账号、备注、明细税额、折扣比例、折扣金额等一旦已识别出，也必须按受支持键名写入。对非关键字段，若当前规则未另行指定特殊落位方式，必须优先参照 [issue.md](issue.md) 的“请求参数说明”选择对应的原始输入键，不得因为表达方便而擅自改名、改层级，或混入正式 payload 才存在的其他包装结构。
13. 对原始输入阶段允许缺失的字段，应先进入脚本 check；只有当 `check_result` 明确返回缺失项、冲突项或校验失败原因时，才一次性向用户确认。对税率字段，只有在用户明确说明税率语义时才允许写入 `taxRate`；若用户未说明，则必须保持缺失。脚本会在商品编码补全完成后优先按“纳税人类型 + 商品字典”自动匹配最低参考税率，匹配失败时才转为待补充。
14. 若任一发票未提供发票类型，Skill 不得仅因票种缺失暂停写入并追问；应保持该发票 `invoiceType` 缺失并进入脚本 check，由脚本查询销方企业画像。销方为小规模纳税人时脚本默认补“普通发票”；用户已明确指定“普票/专票”等票种时，以用户指定为准。
15. 若原始来源是图片或文件，Skill 必须先输出或在内部形成一版“提取后的文字版开票字段”，再据此写入 input JSON；凡是文件中已经无歧义识别出的字段，不论必填还是非必填，只要存在受支持落位，都必须写入 input JSON；例如文件里已明确识别出购方地址、购方电话、备注、折扣金额、税额等，即使它们不是必填，也不得遗漏。识别不清的字段才必须保持缺失。
16. 若文件提取后仍无法稳定区分多张发票边界，或购方、商品、金额、税率等核心字段识别不完整，必须暂停写入并向用户追问；必要时应明确建议用户改用文字输入，或手动补充缺失关键信息。若仅票种缺失，应先交由 check 脚本按销方企业画像处理。

### Step 2. 调用二进制 CLI

Skill 准备好原始输入后，必须调用以下二进制命令：

```bash
.\bin\windows-amd64\invoice-assistant_windows_amd64.exe issue-batch-invoice-info-check --input <临时输入文件>.json --pretty
```

命令执行后会：

1. 对 `invoices[]` 中的每张发票逐张调用公共检查逻辑；
2. 生成 1 个统一的任务状态 JSON；
3. 将合并后的 `check_result` 写入任务状态 JSON；
4. 将该任务文件路径写入 `CURRENT_ISSUE_TASK_POINTER_PATH`。

二进制内部自动补全顺序补充：

1. 先补销售方必填上下文；
2. 若购买方名称非空且不是 18 位统一社会信用代码，或购买方名称/购买方税号本身是 18 位统一社会信用代码，则调用独立企业搜索能力（底层接口 `/share/search-enterprise`）查询购买方企业；仅当返回 1 个候选时才默认选择并补齐购买方名称/税号；返回多个候选时不得取首条，必须在 `check_result.purchaser_autofill.candidates` 中保留候选并要求用户选择正确企业后重试；
3. 若用户未提供发票类型，则查询销方企业画像；销方为小规模纳税人时默认补“普通发票”，用户已明确指定票种时不覆盖；
4. 再按项目名称补商品编码；
5. 在商品编码已确定、用户未提供税率时，按纳税人类型与商品字典自动匹配最低参考税率；
6. 随后再按金额与税率关系补不含税金额、税额、单价及整票汇总。

自动补全触发说明：

1. 只有执行本 Step 2 的 `issue-batch-invoice-info-check` 二进制命令，才会触发上述自动补全；仅生成 input JSON、读取旧任务 JSON、展示预览或执行 `issue-from-output` 都不会重新触发补全。
2. 命令执行时会先按 `uscc` 从 workspace 配置补齐 `areaCode` 与 `personalAccount`，再进入每张发票的字段检查和补全流程。
3. 若销售方信息、购买方企业名称/税号、商品编码、税率、税额或汇总金额缺失，但当前已有足够上下文进入检查命令，Skill 必须先运行本命令，不得在 check 前把这些可由命令补全的字段逐项追问用户。
4. 补全结果只以本次命令写入的 `check_result` 为准；后续正式开票必须复用 `check_result.invoice_payload_json`，不得在正式开票阶段重新拼装或期待再次补全。
5. 若需要在检查前单独查询购买方企业候选，使用独立命令：`.\\bin\\windows-amd64\\invoice-assistant_windows_amd64.exe issue-search-enterprise --query "<购买方名称或税号>"`。该命令输出 `candidate_count`、`candidates`、`needs_user_selection` 和 `selected_candidate`；`candidate_count=1` 可默认选择，`candidate_count>1` 必须让用户选择。

补充约束：

1. 这里写入的 `CURRENT_ISSUE_TASK_POINTER_PATH` 只代表“刚刚由本次检查命令创建出来的当前任务”；不得把它理解为“任意时候都可以直接读取的历史最近任务”。
2. 对新的开票请求，只有本次 Step 2 成功执行完成后，才允许进入 Step 3 读取当前任务 JSON。

### Step 3. 读取任务状态 JSON

命令执行完成后，Skill 必须读取：

- `CURRENT_ISSUE_TASK_POINTER_PATH` 指向的当前任务状态 JSON

读取规则：

1. 这里读取的必须是“紧接着本次 Step 2 刚创建并刷新指针的任务状态 JSON”；若当前用户请求属于新任务，而本轮还没有重新执行 Step 2，则不得直接读取旧指针对应的历史任务文件。
2. 若 `check_result.validation_passed=false`，必须优先根据 `check_result.missing_fields_by_module` 一次性追问缺失项。
3. 缺失项必须保留“第几张发票”的索引，不得把多张发票的缺失项混在一起。
4. 对 input JSON 阶段已允许保持缺失的非必填字段，只有当脚本在 `check_result` 中明确将其列为待补充或返回相关校验失败原因时，才需要向用户追问；不得在 check 前后对同一可选字段重复确认。
5. 后续流程一律以 `check_result.invoice_payload_json` 作为标准化后的批量开票草稿，不再重复从自然语言重新拼装。
6. 若 `check_result.purchaser_autofill.needs_user_selection=true`，必须把 `check_result.purchaser_autofill.candidates` 中的候选企业展示给用户选择；用户选定后将对应 `name`、`uscc` 写回原始 input JSON 并重新执行本检查命令，不得自行取第一个候选继续。
7. 若 `check_result.validation_passed=true` 且 `check_result.invoice_preview_markdown_generated=true`，Skill 必须先读取 `check_result.invoice_preview_markdown_path` 指向的本地 Markdown 文件，再原样展示文件内容，并提示用户核对整批内容；只有在用户明确输入“确认开票”后，才允许继续后续正式开票流程。
8. 正常对话输出中，Skill **不得**主动展示当前任务状态、任务状态 JSON 文件路径、预览文件路径、预览 Markdown 文件路径或 `check_result.invoice_payload_json` 全量内容；这些内容仅用于内部编排。
9. 若任一发票明细属于煤炭类且在用户输入转 input JSON 阶段仍未得到 `mtzlDm`，或单位缺失/不属于 `吨`、`千克（公斤）`，必须判定整批“待补充”，不得跳过该票继续后续正式开票。
10. 若 `check_result.validation_passed=false` 或任务状态为 `check_failed`，`invoice_preview_markdown_path` 为空是预期结果；Skill 必须先处理缺失项、校验错误或待确认项并重新执行本检查命令，不得调用 `issue-invoice-preview-generator` 试图补生成 Markdown。
11. `issue-invoice-preview-generator` 不是本检查场景的后续步骤：它只接受 `--input` 与 `--output`，只生成 HTML，不支持 `--task-file` / `--pretty`，也不会回写任务状态 JSON 或生成 `invoice_preview_markdown_path`。

## 缺失项输出要求

批量场景的缺失项必须按“第几张发票 + 模块”分组。例如：

```text
我需要以下信息才能生成批量开票 JSON：

【第1张发票 / 发票基础信息】
- info.0.basicInfo.invoiceType：请提供发票类型

【第2张发票 / 发票明细】
- invoiceDetail.data[0].spbm：请提供商品编码；若项目名称明确，脚本会先尝试自动赋码
```

## 输出目标

输出必须包含以下四部分：

1. 是否整批通过校验
2. 缺失字段清单（按“第几张发票 + 模块”分组）
3. 标准化后的批量开票 JSON 草稿
4. `item_results`：逐张发票的检查结果摘要，供后续编排排错使用

## 与主开票编排的衔接

1. 主场景在识别出“批量开票”意图后，必须优先调用本场景，而不是循环调用单张场景。
2. 本场景会复用单张字段提取、自动赋码、金额校验等公共能力，但输出为整批统一任务状态 JSON。
3. 当整批校验通过后，应先展示批量预览，再等待用户明确回复“确认开票”。
4. 当整批校验未通过时，应根据 `check_result` 一次性补问，不得手动拼预览或调用预览生成器。
5. 用户确认后，继续复用 `.\bin\windows-amd64\invoice-assistant_windows_amd64.exe issue-from-output --pretty` 发起正式开票，不再区分单张或批量提交命令。

## 输出模板

### 信息完整

```text
{check_result.invoice_preview_markdown}
```

### 信息不完整

```text
已完成批量开票信息初步提取，但仍有字段缺失。

校验结果：未通过

待补充内容：
{missing_fields_by_module}
```
