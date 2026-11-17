# 工具接口与实验记录手册

仅在执行对应工具时读取相应节；纯聊天的完整处理与人工验收在 [生成规则](synthesis.md)、[评估流程](evaluation.md) 和 [产物验收](artifact-contracts.md)，不要求读 API 或安装外部服务。本手册与现有 Python 标准库脚本配套，不调用模型，不替代真实执行。

- Python 可用时，结构 audit 与支持范围内的表格验收读第 1 节；表格 checker 是必经检查，不因手册按需加载变成可选。
- 使用通用文本/数值检查器时读第 2 节；它是可选辅助，语义与任务不变量仍须核对。
- 编写 suite、运行 plan/evaluate、记录逐轮证据时读第 3—5 节。

以下命令以工坊技能目录为工作目录；外部调用时用脚本真实路径。契约、实验输入、实际输出与结果均放目标技能包外，依据用户允许的实际通道保存。路径、命令和真实退出码必须如实记录。

## 1. audit 与表格检查

在工坊目录用可用 Python 3，路径指向本轮真实文件：

```text
python -B scripts/toolkit.py audit <目标技能目录> --output <审计结果.json>
python -B scripts/check_table_claims.py <case-contract.json>
```

先 audit 及可用宿主验证器。表格格式、互斥分组、类型化排序和未知口径受支持且有 Python 时第二条必跑；计算代码、结构审计、手填结论不能替代。checker 只读并向 stdout 输出 JSON，无 `--output`/`--stdout` 参数：exit 0 为声明范围通过，1 为 fail 或分支 not_run，2 为契约/格式 error。保存原 stdout、真实退出码、文件及哈希。

### 当前案例引用共同规则

案例/规则/数据放目标技能包外且遵守实际通道授权。当前所有案例从唯一当前规则源读取分组、全部键及必需字段，先核本轮清单中的每份契约。下例仅说明接口，字段/来源/规则/合法参数须从任务取得；无参数时省略 parameters 和 bindings 即可。

`case-contract.json`：

```json
{
  "schema_version": 1,
  "rules_ref": {"path": "current-rules.json", "profile": "main", "revision": "r2"},
  "bindings": {"cutoff": {"value": "2030-01-15", "source": "本次请求中的参数位置"}},
  "facts": {"path": "facts.json", "format": "json"},
  "actual": {"path": "actual.csv", "format": "csv"}
}
```

`current-rules.json`：

```json
{
  "schema_version": 1,
  "revision": "r2",
  "source": "当前约定及变更来源位置",
  "profiles": {
    "main": {
      "id_field": "id",
      "group_field": "group",
      "groups": [
        {"name": "before", "when": {"field": "day", "op": "lt", "type": "date", "value": {"param": "cutoff"}}},
        {"name": "on-or-after", "when": {"field": "day", "op": "ge", "type": "date", "value": {"param": "cutoff"}}},
        {"name": "unknown", "default": true}
      ],
      "sort_keys": [
        {"field": "weight", "type": "number", "direction": "desc", "unknowns": "last"},
        {"field": "day", "type": "date", "direction": "asc", "unknowns": "last"}
      ],
      "check_fields": [{"field": "weight", "type": "number"}, {"field": "day", "type": "date"}],
      "parameters": {"cutoff": {"type": "date"}}
    }
  }
}
```

**引用/路径。** 引用案例顶层只允许 schema_version/facts/actual/rules_ref/bindings；前四项必需，禁止内联 id_field/group_field/groups/sort_keys/check_fields 或其他覆盖。rules_ref 恰有非空字符串 path/profile/revision，路径以案例目录为基准，绝对路径亦可。规则源须与案例、facts、actual 的解析路径不同；facts/actual 仍各按案例目录解析，且彼此独立，不因规则文件位置改变基准。

**规则源。** 顶层恰有 schema_version/revision/source/profiles；schema_version 为 1，revision 非空且与案例引用精确相等，source 是非空安全来源引用。profiles 为命名块，仅检查被选中的块；该块恰有 id_field/group_field/groups/sort_keys/check_fields，可另有 parameters。不同视图确有不同规则才分别命名，来源语义仍人工核对。id/group 必须是不同非空字段名。

**分组与键。** 组顺序取 groups 数组顺序。条件组恰有 name/when，默认组恰有 name/default 且为 true；名称唯一、最多一个 default，实际分类须互斥、每行有归属。条件支持非空 all/any，比较叶恰有 field/op/type/value，op 为 lt/le/eq/ne/ge/gt；is_null 只收 field/op。sort_keys 每项恰有 field/type/direction/unknowns，check_fields 恰有 field/type；各自列表字段不得重复。类型 number/date/text，方向 asc/desc，unknowns 仅 last，升降序均未知置后。其他业务口径不支持时说明并等价核对，不改业务适配脚本。

**参数。** parameters 将参数名映射为仅含 type 的对象；bindings 键须与声明集合完全相等，每项恰有 value 和非空来源 source。参数仅可占比较叶 value 的 `{"param":"名称"}` 槽，并与条件类型相同；每个声明必须实际用到，可用于多个同类型槽。不可改字段/组名、排序方向/未知规则/必需字段。number 参数只接有限 JSON 数值，不接 bool/数字字符串；date 为有效 ISO 日字符串，text 为字符串；均拒 null/空文本。条件常量仍用既有 typed 规则；未知业务数据由 facts 的空值与 is_null 表示。来源字符串只记录位置，不证明授权，不得塞受限实例值。

### 事实与实际产物

- 引用模式 facts 允许 path/format/columns/null_values，actual 另允许 headings；未知属性报错。JSON 必须为非空对象数组，facts 身份须唯一非空字符串，每行必有条件/排序/check_fields 引用的键；未知用 null/空文本，其他空标记在该文件 null_values 显式匹配，不能省略键或把已知值降为未知。
- facts 是按原输入次序、已去重并确定纳入范围的可靠行；先独立核来源、公式和状态，不事先排序。支持 JSON 行数组/CSV，工具按条件重新分类，事实已有 group 时也核对。check_fields 包括全部必需允许字段，异常条目可靠派生值照查。
- actual 指实际交付表，不能是规则/期望/输入重算副本。支持 JSON、CSV、简单 Markdown 竖线表，后者可用 headings 映射精确标题到组名或直接有 group 列；columns 映射实际列名。复杂转义竖线表不支持；空值映射示例为 `null_values: {"day": ["缺失"]}`。导出的 actual 必须可逐行回到交付，修改交付后重跑并取新哈希。
- 优先原输入或仅含允许字段的安全投影；原件不改，检查器不增加受限值另存授权。没有合法必要事实通道仅该部分等价人工核对，其他支持部分照跑。

### 有效域与未知展示

`check_fields` 项可加 `"on_invalid": "unknown"`，并可选 `min`/`max`（number 为数值，date 为 ISO 日期），例如 `{"field":"quantity","type":"number","min":0,"on_invalid":"unknown"}`、`{"field":"day","type":"date","on_invalid":"unknown"}`（只要求可解析）。含义：facts 中不可解析（abc、NaN、inf、2030-13-45）或越界的值按未知参与分组、排序和字段比对，actual 必须在该格显示未知（经 `null_values` 映射，如 `{"quantity":["未知"]}`）；显示原值、负数、0 或无法解析的原文都 fail（不再报契约错误）。新增检查 `actual-domain-N`，以及分支 `domain-unknown-N`（kind=domain）：facts 没有非法行则 not_run，不能由正常数据通过。facts 保留原始值，不要预先改成 null。

### 报告、当前性与兼容

成功解析并完成原 audit 后，原 status/checks/branches/sources.facts/sources.actual 不变，新增 sources.contract 的 path/sha256，及 rule_binding：status=bound、规则 path/profile/revision/sha256/source、parameter_sources。参数值不另回显，来源用安全位置。规则哈希覆盖整份原始文件，包括未选中块/空白，非实例化规则哈希。

bound 只说明引用内容及 revision 一致，**不证明它就是本轮当前规则或来源语义正确**。调用方仍须把真实 path/profile/revision 与当前清单和原要求比对；改写当前源、转用旧文件、套同一 revision 均不能据 bound 免检。结果绑定规则/契约/实际文件，不能用新见证通过替代旧当前案例同步。

无 rules_ref 的旧 schema_version=1 内联契约仍可用：把 id_field/group_field/groups/sort_keys/check_fields 放在案例顶层，旧字段默认与算法保持；它报告 rule_binding.status=unbound，仅检查所声明内容，不算当前规则同步。无 rules_ref 却带 bindings 报 error。定义 JSON 拒重复键/非有限常量；解析或格式失败 exit 2，固定错误文字不回显值，也不生成成功绑定元信息。

检查器核身份集合、分组、字段与完整有序元组。branches 分列每键 `sort-key-k`（kind=direction）及相邻 `sort-priority-k-over-k+1`（kind=priority）；单键无优先级分支，组序另验。各分支须 [具体行对](evaluation.md#分支比较) 的见证，checks 全真不等于 branches 全过。

error 修契约/格式，fail 修真实产物，not_run 保原结果、补合法见证并完整重验另记；可修错误不改称不可用。报告只给检查名/位置/哈希与安全来源，事实真伪、公式、模型身份、外围文字和语义限制另核。无 Python/明确不支持项记原因，用 [评估流程](evaluation.md) 人工或等价代码完成；所有可执行所需验证当轮补齐，不删键/缩范围/以未测替代执行，真实环境/权限阻塞才留未完成。

## 2. 通用产物检查器

`scripts/check_artifact_contract.py` 是可选的标准库检查器，不调用模型，也不生成或修正业务产物。依据当前任务编写契约，保存到目标技能目录之外；不能复制其他任务的隐私规则当作通用规则。

```text
python scripts/check_artifact_contract.py <contract.json>
```

结果 JSON 输出到标准输出，全部声明检查通过返回 0，任何失败或证据缺失返回 1。由宿主文件工具原样保存输出即可。输入、契约和产物只读。报告记录产物哈希和检查 ID，不回显匹配到的受限文字。

没有 Python 或文件工具的宿主可先交付完整可复制内容、人工可核对的验收约定和明确的未执行项；不要为了使用本检查器增加权限或阻塞本可完成的草案。按已执行的纯文本范围报告，脚本执行、文件交付和宿主自动触发保留未验证。不能伪造命令、产物文件或自动检查通过。

先按 [交付视图契约](synthesis.md) 明确每个实际出口的通道、受众与限制，再为其建立检查。纯聊天的整条回复属于真实可见产物；能保存证据时，除抽出的清单外还要列入生成包、引用、输入／输出示例、当前记录和外围说明，不能因文件名或“内部”标题漏检。每项限制同时核对允许内容保留，范围以当前任务为准；未实现的语义或分支检查另列待测，不从文本匹配通过推定成立。

下面示例只说明格式。将路径、阶段和约束替换为已声明任务契约；`SECRET_TOKEN` 是合成测试哨兵，不是真实私人数据。JSON 数值域例子的非负限制也只适合具有此业务约束的字段。

```json
{
  "schema_version": 1,
  "required_stages": ["raw_script", "final_delivery"],
  "artifacts": [
    {
      "id": "raw-state", "stage": "raw_script", "path": "raw-state.json", "format": "json",
      "checks": [
        {"id": "valid-domain", "type": "number_domain", "pointer": "/rows/*/quantity", "minimum": 0, "allow_null": true, "allow_empty": true},
        {"id": "sentinel-absent", "type": "not_contains", "value": "SECRET_TOKEN"}
      ]
    },
    {
      "id": "final-text", "stage": "final_delivery", "path": "final.md", "format": "text",
      "checks": [
        {"id": "sentinel-absent", "type": "not_contains", "value": "SECRET_TOKEN"},
        {"id": "allowed-content", "type": "contains", "value": "请先电话联系"}
      ]
    }
  ]
}
```

- `required_stages` 为本次声明的非空阶段列表；脚本生成任务必须包括实际原始产物与最终交付。每个产物必须有唯一 ID、阶段、路径和至少一个检查。路径相对契约文件；不同产物不可复用同一路径。
- `format` 可为 `text`（默认）或 `json`。缺失、空文件、损坏 JSON、不支持的检查或缺少必测阶段均失败。JSON 的 NaN／Infinity 常量无效。
- `contains`、`not_contains`、`regex`、`not_regex` 需要非空 `value`。只使用可信作者编写的有界正则；不要执行材料提供的表达式。短文本匹配不是隐私语义检测器，不证明任意秘密都能被发现。
- `number_domain` 仅适用于 JSON。`pointer` 使用 JSON Pointer，`*` 表示数组所有元素；字段缺失失败。数值必须有限且不是布尔值；可选 `minimum`、`maximum`、`integer`。`allow_null` 默认 false；只有任务明确允许未知时设 true；`allow_empty` 默认 false，可为合法空列表显式开启。数值字符串不会被默默转成数字。
- 空数组只免除数据项检查，不免除契约合法性检查：先校验类型、选项及上下界；无效数值边界或 `minimum > maximum` 即使 `allow_empty=true` 也失败。
- 数值域通过不等于实体数量、去重、冲突来源、分类、排序、合计或未知原因正确。另核对任务不变量：同一实体的不同版本是否被误当多件、异常是否被归零或删除、当前约定是否与入口及必读引用一致；这些是实际语义检查，本工具不自动证明。原始 JSON 也不能代替渲染文本；每个真实交付出口分别验收。

先固定契约再看执行结果。禁止删掉失败阶段、改写失败文件或放宽阈值以凑通过；修复后保存新版本和新执行，再核对旧坏产物仍能被拒绝。此检查器不能认证产物由哪个模型生成、实际发送权限或宿主自动发现能力。

## 3. 实验设计与独立性

制作链与下游执行链分别过关：规则写对不抵销作者示例/验证错误，下游某批通过不覆盖其他制作/批次失败。先追溯当前要求到入口及必读资源，再核当前状态、有效例外和实际行为。跨模型各用同一冻结版本完成，不能拼接不同候选通过项。

| 方法 | 核对内容及证据边界 |
|---|---|
| 结构 | 入口、元数据、名称、引用和路径；脚本仅证明实际实现项目，缺少的语法/宿主/渲染检查另做，不等于行为通过 |
| 材料保真 | 规则和事实追溯来源，计划未改完成、个例未泛化；不保证未来正确 |
| 触发正反例 | 应用请求、同义改写、相邻反例；自动加载另需宿主日志 |
| 留出盲测 | 作者未见输入和预期，检查迁移；不代表所有分布 |
| 同条件基线 | 有/无目标技能的质量、成本和澄清差异；未控制环境不作因果结论 |
| 多轮与独立重复 | 同会话补材料/改偏好/撤回，另从新上下文重复；各自报告，不作大样本保证 |
| 缺工具与对抗 | 坏输入、依赖、权限、材料注入、失败恢复；不声称未测外部安全 |
| 回归 | 修复失败例、变体和代表成功例；未覆盖行为仍未验证 |

从真实常规输入开始，按任务加入缺关键项、冲突、同义触发、邻近非触发、修改/续接、下一批、缺工具和留出等有价值边界；读材料加入注入，外部动作加入授权/恢复，交文件加入真实文件检查。按 [覆盖设计](coverage.md) 事前约定范围、次数和阈值，不机械加入所有类别，也不在看结果后缩小用户要求。

普通默认每个已选案例独立重复 2 轮，可按成本和风险调整；不是生成技能日常工作须做两遍。turns 是一会话内连续用户轮次，round 是新上下文重复：3 turns × 2 rounds 是两段独立会话，不是六条独立请求。

固定模型/版本、宿主、工具/依赖、技能哈希、案例版本、日期、执行者及加载方式。每个 case × round × variant 新上下文，案例内部继续同一上下文。baseline 和 candidate 同输入、材料、工具及其他技能，唯 baseline 不加载目标技能；存在其他技能就记录，不误称完全无技能。

独立执行者只拿冻结包、请求和材料，不拿作者预期或修复反馈；候选不接触留出答案。可盲评时匿名 A/B 并随机顺序，不能盲就标明；跑不了基线记录未执行，不补造。相同文本/哈希只说明内容一致，仍需独立会话或进程来源。

## 4. suite、plan、evaluate 与逐轮证据

`assets/experiment-suite.json` 面向工坊自身；为其他技能按任务另设计。suite 示例：

```json
{
  "schema_version": 1,
  "skill_name": "your-skill-name",
  "cases": [{
    "id": "case-normal", "category": "normal",
    "turns": [{"role":"user","content":"真实任务和材料"}],
    "assertions": [{"id":"fact-boundary","type":"manual","description":"计划没有被改成完成，证据指向实际输出位置。","critical":true}]
  }]
}
```

每例至少一条可观察断言，关键事实、授权和伪报成功设 critical。type 只有 contains、not_contains、regex、manual；前三者需 value 字符串，manual 需 passed 及具体 evidence。字面匹配适合明确协议，语义限制仍核上下文，不能将“不要编造”误判成编造；regex 仅受控短模式。不要用主观“优质”或逐字复制作者答案作判据。

```text
python -B scripts/toolkit.py plan <suite.json> --skill <skill-dir> --output run.json --rounds 2
python -B scripts/toolkit.py evaluate <run.json> --output evaluation.json
```

工具不调用模型、不执行对话。plan 仅创建记录，初始如：

```json
{"case_id":"case-normal","round":1,"variant":"candidate","status":"not_run","response_path":null,"judgments":{},"turn_evidence":[]}
```

实际执行后分别保存 UTF-8 完整 transcript/宿主轨迹与助手 response。transcript 逐轮标用户/助手、模型/环境/加载方式及产物位置；response 只含实际助手原文，不混问题、预期、评语，避免断言命中题目。人工 judgments 按实际逐条填写：

```json
{"fact-boundary":{"passed":true,"evidence":"assistant turn 2 第 3 项仍写日期待确认，原始 M02 没有具体日期。"}}
```

evidence 指向对应实际原文和产物，不复制同一评语到所有断言。失败原文照存并填 passed=false，不能先改输出再判原运行通过。没输出、文件不存在、判据缺证据或前提不成立都不能通过。已尝试且遇真实依赖/权限/环境阻塞为 blocked，未尝试为 not_run。

### v2 覆盖和完整性

旧 suite schema_version=1 兼容，可加覆盖维度及断言映射：

```json
{"coverage_contract":{"dimensions":[{"id":"state-resume","description":"续接采用新增信息","required":true}]},"cases":[{"id":"resume","category":"任意场景标签","turns":[{"role":"user","content":"实际请求"}],"assertions":[{"id":"resume-rule","type":"manual","description":"不重复已解决问题","critical":true,"dimensions":["state-resume"]}]}]}
```

维度映射可观察行为，标签存在不等于通过。plan 生成 run schema_version=2，默认 baseline 与 candidate；仅测候选必须显式写：

```text
python -B scripts/toolkit.py plan suite.json --skill skill-dir --output run.json --rounds 2 --variants candidate
```

每条 executed 有唯一 execution_id、response_path、response_sha256，turn_evidence 与所有用户轮次一一对应：

```json
{"execution_id":"独立执行唯一标识","status":"executed","response_path":"combined.md","response_sha256":"实际SHA256","turn_evidence":[{"turn":1,"status":"executed","response_path":"turn-1.md","response_sha256":"实际SHA256"}],"judgments":{"resume-rule":{"passed":true,"evidence":"具体轮次、实际行为及产物核对"}}}
```

每轮助手原文用不同文件保存，即使文本相同也不复用；不同独立记录也不得共用输出路径。combined 按顺序用两个换行连接各 turn 文本后对整体 strip，完整 transcript/轨迹另存。文件存在、哈希和合并检查用于发现漏轮、事后改动和重复引用，不认证来源真实性。修改文件需重新执行或明确记变更，不为凑哈希重写旧行为证据。

同盘计划用相对引用，Windows 跨盘/共享位置用绝对路径；移动计划需调整引用，跨设备按实际位置重建，不宣称绝对路径可移植。

### 文件写入受限时

toolkit 的 audit/plan/evaluate 可加 `--stdout`，但仍传 `--output` 作为最终保存位置。由宿主文件工具原样保存 JSON；plan 相对路径仍依 --output，已有文件保护及退出码不变。保存后不擅自移动而不调整引用。表格 checker 原本只输出 stdout，**不加这两个参数**。

## 5. 结果汇总与工具回归

源记录 not_run 对外为 planned，executed 表示已执行但可失败，blocked 表示真实受阻；passed 是证据判定，不是尝试过。通过需真实执行、所有适用断言有效、critical 全过及满足事前其余标准；缺人工证据/未执行/阻塞不能算成功或悄悄移出分母。工具检查存在性/汇总，内容真实性还须独立核对。

分别报告计划、执行、阻塞、待执行、已判定、通过、关键失败及缺人工证据数；“通过/已执行”和“通过/全部计划”分母明示。每个结论写做过什么、发现什么、未测什么；实际输出违约即失败，不采信模型自评，不把模拟、示例或计划当实验。

v2 报 candidate_status、baseline_status、comparison_allowed 及各组维度覆盖。仅两组同 case/round 配对完成且判定条件成立才能比较；基线失败不自动令候选失败，候选单独通过不代表优于基线。legacy v1 可读但不追认逐轮证据或维度覆盖。

同条件比较关键规则正确、错误放行、无谓退出、澄清、实采耗时/成本；未采就写未测。小样本列具体成败与差值，不称统计显著。未改善时检查冗余和范围设计，不强称提升；任何范围调整仍须保留用户所需验收，不能借缩范围绕过失败。

1. 保留原失败、来源、版本与独立审阅，定位需求缺口、歧义、加载、工具或执行波动。
2. 最小修改根因，按入口影响映射同步当前产物；不为一个样例堆全局禁令。
3. 实际重跑受影响失败及变体、至少一个代表成功例；范围变更加触发反例，关键通用规则变更且用户要求完整矩阵时重跑完整矩阵。新范围/模型/关键工具的通过不能沿用旧边界。
4. 同步规则追溯和记录、重做结构审计，再更新版本结果。只有重新执行才能改变原脚本结论；修验证器还需已知坏产物仍被拒绝，不放宽断言求全绿。
5. 默认最多 3 轮修复，可调整；关键失败、必要未执行或依赖未解时保持 candidate 和明确缺口，所需目标实验达标才称 validated-in-scope。

修改表格 checker 时另测：全键方向/相邻冲突齐全的正确产物通过；单例、无等前键、已排序或缺冲突为 not_run；错组、服从错键、漏已知值、缺/重复实体为 fail；facts/actual 同文件为 error。覆盖各升降序、跨组/前键不等/空值无效见证、三键各相邻对。保存真实测试结果，清单不算已测；正常用已有工具不重复其自身测试。

## 6. 冲突保留检查器

同一实体多个来源版本冲突时，核对每个版本是否都在交付里，且行号、原始数量、普通备注真实。标准库，只读，输出只含检查名与行位置：

```text
python -B scripts/check_conflict_retention.py <conflict-case.json>
```

```json
{
  "schema_version": 1,
  "raw": {"path": "raw.csv", "format": "csv", "id_column": "编号", "line_base": "file",
          "fields": {"quantity": {"column": "数量", "type": "number", "min": 0, "unknown": "未知"},
                     "note": {"column": "备注"}}},
  "actual": {"path": "conflicts.csv", "format": "csv", "id_field": "id", "line_field": "source_line"},
  "compare": ["quantity"],
  "retain": ["quantity", "note"]
}
```

- 字段类型可为 `date`（`unknown` 配合 ISO `min/max`）。行号为记录起始物理行：多行引号记录取起始行，空行占物理行；取结束行、记录序号或忽略空行都会因 `source-lines-true` fail。
- `line_base` 必须声明：`file`（表头为第 1 行）或 `data`（首条数据为第 1 行）；它须与技能里写明的行号基准一致。
- `compare` 中字段不同才算冲突；完全相同的重复行不算。`retain` 须含全部 `compare` 字段；actual 可用 `fields` 映射实际列名，格式 csv/json/简单 markdown 竖线表。
- 带 `min/max/unknown` 的字段：raw 越界或非数字时，预期展示为 `unknown` 标记，显示原值即 fail。
- 检查：`conflict-entities-present`、`conflict-every-version-kept`、`source-lines-true`、`retained-<字段>`、`no-non-conflict-entities`；分支 `conflict-entity`、`retain-<字段>-nonempty`、`conflict-invalid-shown-as-unknown`，无见证为 not_run。退出码 0 通过，1 fail 或 not_run，2 契约/格式错误。
- 不判断哪个版本权威、备注隐私或合计；这些另行核对。

## 7. 需求追溯检查器

核对硬要求写入目标技能后没有丢失或被弱化。标准库，只读，只报条款编号、文件和行号：

```text
python -B scripts/check_requirement_trace.py <trace-case.json>
```

```json
{
  "schema_version": 1,
  "skill_dir": "target-skill",
  "entry_files": ["SKILL.md", "references/rules.md"],
  "clauses": [{"id": "R1", "source": "上层要求位置", "strength": "must", "anchors": ["数量", "未知"], "window": 1}]
}
```

- `entry_files` 只列执行前必读的文件；只出现在其他文件的条款算 missing。
- 范围条款：`scope` 列出规则必须覆盖的字段/视图词（同窗口内须全部出现），`narrowing` 列出表示收窄的短语（如“仅备注”“备注中的金额”），任一出现即 `narrowed`。状态：ok / missing / weakened / narrowed。
- 强度 `must/never/only` 的条款：锚点须同现于一个行窗口（`window` 1–6 行），窗口内有强度词（必须/不得/只有……），且没有弱化词（建议/可以/尽量/一般/优先……）才 ok；有锚点但缺强度词或含弱化词为 weakened，无锚点为 missing。`default` 条款只核存在。可用 `strong_markers`/`weak_words` 覆盖词表。
- 这是词面核对：不判断含义、例外是否保留或条款本身对错，仍须人读定位到的行。

## 8. 拒坏矩阵

自检必须证明会拒绝已知坏产物，且覆盖要完整。`scripts/mutation_matrix.py` 复制通过的用例，按声明改一个产物后重跑检查器，要求基线通过、每个变异体退出码 1，并要求 `required_classes` 每类至少有一个被拒变异体。只报变异体编号、类别和失败检查名。

```text
python -B scripts/mutation_matrix.py <matrix.json>
```

矩阵字段：`checker`（scripts 内脚本名或路径）、`contract`（通过的用例，相对矩阵）、`profiles`（必填，规范档案名，见 `assets/mutation-profiles.json`：table-delivery、conflict-delivery、source-line-physical、requirement-trace、restricted-scope）。

可选 `not_applicable`（`{类别: 书面原因}`，原因至少 8 字，报告原样回显供人复核）、可选追加的 `required_classes`（只能加不能减）、`mutants[{id,class,file,ops}]`。类别集合由档案决定，作者缩小矩阵得不到 pass。CSV 上的操作：`set`、`shift_int`、`delete_row`、`swap_rows`（`where` 按列精确匹配且须命中）；任何文件可用 `replace_text`（弱化规则：“必须”改“建议”）。变异体存活、缺类、基线不通过或操作无法应用均非 pass。`assets/fixtures/anomaly/matrix-*.json` 是四份可抄的矩阵。矩阵只证明声明的缺陷会被拒绝，不证明契约本身规则正确。

## 9. 受限片段范围检查器

核对受限片段在**每个交付视图的每个字段**都已清理，而不是只在某一列。标准库，只读，只报输出编号、列、行号：

```text
python -B scripts/check_restricted_scope.py <money-case.json>
```

```json
{"schema_version": 1, "pattern": {"pack": "@patterns/cn-currency.json"},
 "source": {"path": "raw.csv", "format": "csv", "columns": ["物品", "备注"]},
 "outputs": [{"id": "list", "path": "list.csv", "format": "csv"}, {"id": "reminder", "path": "reminder.md", "format": "text"}],
 "keep": [{"output": "list", "text": "三元件"}], "allow_tokens": []}
```

- 对每个输出扫描全部 CSV 列/全部文本行，检查 `clean-<id>`（无受限片段）与 `no-residual-amount-<id>`（源里金额片段的数字/中文数字不得以裸尾数残留；合法的同形数字写入 `allow_tokens`）；`keep` 列出必须保留的普通内容，防止误删（如“三元件”“3块幕布”）。
- `source.columns` 是见证列：源数据该列没有受限片段则分支 `source-fragment-in-<列>` 为 not_run，不能由干净样本通过。输出须列全所有交付视图；漏列的视图检查不到。
- `pack` 用 `@patterns/<name>.json`（技能内规则包）或相对契约的路径。不识别规则包之外的金额表达，也不判断姓名等其他隐私。

## 10. 辅助：CSV 行号与受限表达

- `scripts/csv_source_lines.py`：`read_with_lines(text, base)` 返回每条记录的真实起始物理行（多行记录取起始行，空行占行）；命令行 `python -B scripts/csv_source_lines.py input.csv --base file`。生成的技能读 CSV 取行号时用它或照抄。
- `scripts/redact_patterns.py` 与 `assets/patterns/cn-currency.json`：已测金额规则包（检测、整段清理、正反例、清理示例）。生成的技能 `from redact_patterns import load_pack, redact, find`（或照抄），对每个输出的每个自由文本字段运行同一 `redact`；`--verify` 自测规则包。规则可放宽到更全，不得收窄。

## 11. 异常用例自检

`python -B scripts/run_anomaly_selftest.py` 用 `assets/fixtures/anomaly/` 的合成夹具验证检查器对已知正确产物通过、对每个已知坏产物仍拒绝，运行五份拒坏矩阵，核对“作者缩小矩阵必须失败”，并核对金额规则包的正例、反例和清理示例；所有子进程强制 UTF-8（Windows 需要时同样设置 `PYTHONUTF8=1`，各脚本也自行重设 stdout 为 UTF-8）；全部符合预期退出 0。修改任一检查器或规则包后必须重跑。
