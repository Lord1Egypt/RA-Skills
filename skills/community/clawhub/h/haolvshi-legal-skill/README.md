# 好律狮法律技能包

好律狮法律技能包是一个面向 Agent Skills 的法律服务技能。用户用自然语言提出法律问题、上传案件材料或合同后，技能会调用好律狮服务完成项目匹配、事实收集、材料识别和结果生成。

当前技能包版本为 `1.17`，采用 MIT-0 许可证。

`1.17` 修复条件字段误追问：当前任务明确只涉及某类财产时，其他类别的数量或明细字段会保留空值并自动推进；仅未提到某类别仍会正常询问，不会擅自填零或默认数量。

`1.16` 增加多能力请求的串行确认闸门：同一请求需要多份报告或文书时，每次只运行一项能力；当前交付完成后必须询问用户是否继续下一项，明确同意前不得创建后续任务或调用下一能力。能够由同一份报告回答的多个子问题仍保留在一个流程中，不因提到起诉状写作要点等咨询内容就自动生成另一份文书。

`1.15` 继续缩短决策时间并收紧交付：运行环境准备会一次性补齐脚本执行位和状态目录，不再中途卡在权限错误；案情里已能判断的题目改由宿主大模型做语义作答（如“拖欠工资5年了”直接选中“超过三年”，“老板”对应“用人单位”），脚本只在 `interaction.answerPolicy` 里声明门槛和边界，不用关键词或正则代答；报告链接只允许用宿主内置浏览器打开，并禁止模型自行生成任何报告文件；每次进入技能必须先清空上一轮的技能记忆。同时修正文书模板目录被关键词过滤成空的问题。

`1.14` 压缩喂给宿主模型的载荷：目录候选只保留 `id` 和 `displayName`，同一响应里重复三次的证据边界声明与选项文字去重。一次完整咨询的上下文从约 87KB 降到约 30KB，宿主的选型和逐题判断明显更快；行为和取值完全不变，需要完整载荷时传 `"verbose": true`。

`1.13` 修正日期题、地区题、日期区间题和数值单位题的取值填充：脚本按题目组件和配置把答案转换成后端要求的形状（日期转 unix 秒、地区按 `areaLevel` 解析成地区 id），此前会导致报告出现 Invalid Date、未匹配到地区和 NaN 金额。

`1.12` 将咨询与计算器项目选择改为大模型语义评分：只有第一候选置信度足够高且明显领先时才自动启动，否则由用户在少量真实候选中确认；不再用分词排序截断项目目录。

当前支持五类能力：

| 能力 | 典型请求 | 交互方式 | 最终产物 |
| --- | --- | --- | --- |
| 法律咨询报告 | “离婚财产如何分割？” | 按当前问题逐题收集必要事实 | 在线法律咨询报告 |
| 法律计算器 | “交通事故能赔多少钱？”、“养老保险怎么算？” | 按当前问题逐题收集计算参数 | 在线计算报告 |
| 智能合同审核 | “帮我审核这份合同，我方是乙方” | 先确认甲方/乙方，再上传合同 | 在线合同审核报告 |
| 起诉状生成 | “帮我生成民事起诉状” | 提取案情，分步骤核对文书字段 | 可直接下载的 Word 文件 |
| 答辩状生成 | “帮我写答辩状” | 提取案情，分步骤核对文书字段 | 可直接下载的 Word 文件 |

## 服务地址

- 官网与技能包下载：[https://skills.ai.lvpin100.com](https://skills.ai.lvpin100.com)
- 法律咨询、计算器和合同审核的在线结果页面：`https://skill.ai.lvpin100.com`
- 技能包安装说明：[`INSTALL.md`](INSTALL.md)
- 技能编排规则：[`SKILL.md`](SKILL.md)
- 参考流程：`references/`
- 托管和发布说明：[`PUBLISHING.md`](PUBLISHING.md)

技能下载域名和在线应用域名是两套地址，不要混用。技能包内置的是生产环境配置；测试环境可以通过环境变量覆盖。

## 五分钟开始使用

### 让支持技能安装的人工智能助手安装

将下面的地址交给支持 Agent Skills 的人工智能助手：

```text
请根据 https://skills.ai.lvpin100.com/skills/haolvshi-legal-skill/INSTALL.md
帮我安装“好律狮法律技能包”。
```

### 命令行安装

```bash
npx skills add https://skills.ai.lvpin100.com/skills/haolvshi-legal-skill/haolvshi-legal-skill.zip --skill haolvshi-legal-skill
```

也可以先下载以下压缩包，再从人工智能工具的技能管理页面导入：

```text
https://skills.ai.lvpin100.com/skills/haolvshi-legal-skill/haolvshi-legal-skill.zip
```

无需预装 Node.js。技能首次运行时会检查 Node.js 版本；没有可用版本，或版本低于 20 时，会在用户目录准备技能专用的 Node.js 22 运行环境。

### 安装后验证

进入技能目录执行：

```bash
sh scripts/bootstrap.sh --ensure
sh scripts/run.sh health
```

Windows 使用：

```powershell
powershell -ExecutionPolicy Bypass -File scripts/bootstrap.ps1 -Ensure
powershell -ExecutionPolicy Bypass -File scripts/run.ps1 health
```

健康检查会访问服务目录，并返回以下状态：`consultation`、`calculator`、`complaint`、`defense` 和 `contract`。其中合同审核状态只检查站点是否存在可用配置，不会返回密钥，也不会发起真实合同审核。

验证通过后，可以直接对人工智能助手说：

```text
发生交通事故，帮我计算一下可以获得多少赔偿。
```

## 使用方式

### 普通用户

直接描述目标即可。建议一次性提供已知事实和相关文件，例如：

```text
我在杭州发生交通事故，对方全责，已经构成十级伤残，医疗费约 12000 元。
请根据我上传的事故认定书和医疗票据，计算可以主张的赔偿项目。
```

技能会优先使用当前任务/当前线程内的用户消息、当前任务已上传材料、当前 `sessionId` 已确认答案和当前任务更正自动填写已知字段；只在信息缺失、互相冲突或无法唯一对应选项时提问。用户不需要重复描述本任务中已经说过的案情。

五类能力全部采用当前任务证据隔离：禁止读取、搜索、引用或推断 WorkBuddy/宿主全局记忆、长期记忆、用户画像、其他任务、其他线程、旧案例、旧报告、示例、评测、交接文档、测试记录或日志，也不得把这些内容混入 `query`、`content`、`caseContext`、答案、文书字段、合同立场、项目或模板选择。新任务只有概括性问题时会重新询问必要事实，不会自动套用旧案例。

自动填写必须有直接、明确、唯一的案情依据。没有匹配答案时，除非是非必填且为空的姓名、电话、手机号、身份证号、证件号码等敏感字段，技能都会把完整题目返回给用户本人选择或填写；这些敏感字段会自动隐藏、保留空值并直接推进，不会阻塞流程。居住地、实际居住地、户籍地、住所地等地区字段不属于可跳过的敏感信息，即使非必填也必须保留，因为地区可能影响政策、地方法规和计算标准；重复记录或当事人卡片中的姓名同样不能跳过。技能不会自动选择“不清楚”“不知道”“其他”“无”“否”“不适用”等兜底或默认答案。

### 交互原则

- 法律咨询和计算器始终按当前后端返回的问题推进，不预设固定题目数量。
- 当前任务证据没有唯一匹配时，普通填空题会由脚本直接组装为带 2 至 4 个建议选项的标准单选题，使用与后端普通选择题相同的原生组件结构；宿主不再二次生成候选。
- 多填题和追加题每轮只显示一个小题，所有子字段回答完成前只保存本地状态，完成后才一次提交后端。
- 选项包含追加题时，技能先在本地完成追加题，再把主答案和追加答案一起提交；不会提前请求下一道后端题目。
- 原生选择器、输入框或表单能完整表达当前问题时必须使用；显示前后按 `optionManifest` 核对选项数量、顺序和完整标签，少一项都不得让用户作答。选择器容量不足时改用其他原生组件，或在原生表单/输入组件中完整列出编号选项；只有确认全部原生方案不兼容后才展示完整编号文本。
- 文书流程按“案件材料、当事人、诉讼请求或答辩意见、事实与理由、证据、法院与送达、其他信息、确认生成”分步处理。
- 当事人很多时一次只展开一张卡片；普通字段较多时自动分页，避免把整份文书一次性铺开。
- 起诉状和答辩状生成前必须展示完整摘要并取得用户明确确认。

### 结果形式

- 法律咨询、计算器和合同审核：展示关键摘要，并在同一轮回复中原样输出 `data.delivery.markdown`，名称分别为“法律咨询报告”“法律计算报告”“合同审核报告”；随后立即用宿主可用的浏览器或导航能力打开 `data.delivery.url`。
- 起诉状和答辩状：展示文书摘要，并在同一轮回复中原样输出 `data.delivery.markdown`，名称分别为“起诉状（Word）”“答辩状（Word）”。
- 宿主不具备浏览器或导航能力时，在线报告仍必须在生成当轮发送链接；文书下载链接不自动打开。
- 最终摘要、结论和法律依据只取自本次生成的报告或文书及其中已有法规、案例；生成后不再联网搜索、查询法律数据库或补充报告之外的内容。
- 不要把长报告全文直接铺满聊天窗口，也不要用本地临时文件路径替代用户可访问的结果链接。

本技能输出的报告和文书基于用户提供的信息生成，不能替代律师针对完整材料作出的正式法律意见；涉及诉讼时效、财产处分、人身安全或其他重大权益时，应进一步咨询专业律师并核对原始材料。

## 案件材料

### 支持格式和限制

案件咨询、计算器、起诉状和答辩状最多接收 20 个材料文件，单个文件不超过 10MB。脚本直接读取的文本格式包括：

```text
TXT、MD、CSV、JSON、HTML、HTM、XML
```

以下格式需要宿主提供真实的文件阅读、表格阅读或图像识别能力：

```text
PDF、DOC、DOCX、RTF、XLS、XLSX、JPG、JPEG、PNG
```

案件材料识别最多保留每个文件 120,000 个字符，所有材料合计最多保留 300,000 个字符。超过限制时，结果会在 `warnings` 中说明，不会静默假装已经读取全部内容。

合同审核使用单独的文件限制：

- PDF、DOC、DOCX 每次只能提交一个合同正文文件；
- JPG、JPEG、PNG 最多提交十张合同图片；
- 合同正文与合同图片不能混合提交；
- 每个文件不超过 10MB。

### 不同文件的处理方式

| 文件类型 | 咨询/计算器 | 起诉状/答辩状 |
| --- | --- | --- |
| 纯文本 | 脚本直接提取并参与项目选择、自动作答 | 脚本直接提取并参与文书要素提取 |
| PDF、Word、表格 | 先由宿主提取文字，再通过 `extractedTexts` 传入 | 先由宿主提取文字，再通过 `extractedTexts` 传入 |
| 图片 | 先由宿主进行图像理解或文字识别 | 可由后端视觉接口直接提取，也可同时传入宿主识别文字 |

如果返回 `stage=needs_material_extraction`，必须先读取 `data.unresolvedFiles` 中的文件，再把忠实提取的文字按下面的格式传回原命令：

```json
{
  "extractedTexts": [
    {
      "filePath": "/绝对路径/事故认定书.pdf",
      "text": "从文件中提取的原文信息"
    }
  ]
}
```

不能读取某种文件时，应请用户提供可复制文字或转换后的文件，不要静默跳过附件，也不要根据材料没有记载就填写“否”“无”或零。

## 命令行接口

脚本位于 `scripts/`，统一通过运行封装调用。macOS 或 Linux：

```bash
sh scripts/run.sh <命令> [--json '<JSON>' | --input <JSON文件>]
```

Windows：

```powershell
powershell -ExecutionPolicy Bypass -File scripts/run.ps1 <命令> --json '<JSON>'
```

也可以通过标准输入传 JSON。涉及案情、合同内容或身份信息时，优先使用标准输入或 `--input` 文件，避免把敏感内容写入命令行历史。

### 命令总览

| 命令 | 用途 | 常用能力 |
| --- | --- | --- |
| `health` | 检查服务目录、能力和合同审核配置 | 全部 |
| `case-materials` | 单独提取案件材料并生成可复用 `caseContext` | 咨询、计算器、文书 |
| `catalog` | 查询并排序咨询项目、计算器项目或文书模板 | 全部（合同审核除外） |
| `question-start` | 创建咨询或计算器任务并取得第一题 | `consultation`、`calculator` |
| `question-reply` | 提交当前题答案并取得下一题或追加题 | `consultation`、`calculator` |
| `question-report` | 生成咨询或计算器报告 | `consultation`、`calculator` |
| `contract-review` | 上传合同并发起审核 | `contract` |
| `pleading-start` | 创建起诉状或答辩状任务并读取模板 | `complaint`、`defense` |
| `pleading-extract` | 提取案情和材料中的文书要素 | `complaint`、`defense` |
| `pleading-update` | 更新字段、切换步骤、维护多个当事人 | `complaint`、`defense` |
| `pleading-generate` | 在确认后生成 Word 文书 | `complaint`、`defense` |
| `resume` | 用 `sessionId` 恢复未完成或已完成任务 | 全部 |
| `cleanup` | 删除指定任务或清理过期任务材料 | 全部 |

### 输入形式示例

查询法律咨询或计算器项目：

```bash
printf '%s' '{"capability":"consultation","query":"离婚财产"}' \
  | sh scripts/run.sh catalog
```

使用案件材料查询计算器项目：

```bash
printf '%s' '{"capability":"calculator","query":"交通事故赔偿","filePaths":["/绝对路径/事故经过.txt"]}' \
  | sh scripts/run.sh catalog
```

把 JSON 放入文件后运行：

```bash
sh scripts/run.sh question-start --input /绝对路径/request.json
```

### 会话和返回阶段

除 `health`、`catalog` 和 `case-materials` 外，工作流通常会返回 `sessionId`。收到后必须在后续调用中原样保留，并且不要把一个能力的任务编号用于另一种能力。

常见阶段如下：

| 阶段 | 含义 | 下一步 |
| --- | --- | --- |
| `needs_selection` | 存在多个项目或模板候选 | 选择候选项后重新调用开始命令 |
| `needs_material_extraction` | 文件需要宿主先读取 | 提取文字后用 `extractedTexts` 重试 |
| `collecting` | 正在收集问题或文书字段 | 自动填写已知值，必要时提交答案 |
| `needs_input` | 仍有必填字段未解决 | 只询问 `data.missing` 或交互中的未决字段 |
| `needs_follow_up` | 当前选项触发了本地追加题 | 继续使用同一个 `sessionId` 回答追加题 |
| `ready_for_report` | 咨询或计算器问题已完成 | 调用 `question-report` |
| `ready_to_generate` | 文书字段已到确认步骤 | 展示完整摘要，确认后调用生成命令 |
| `needs_confirmation` | 文书尚未得到明确确认 | 用户确认后传入 `confirmed: true` |
| `completed` | 结果已生成 | 同一轮展示 `data.delivery.markdown`；在线报告立即打开，文书链接仅供下载 |

所有命令都返回 JSON。成功结果通常包含 `ok: true`、`stage` 和 `data`；失败结果包含 `ok: false`、`stage: "error"` 以及：

```json
{
  "error": {
    "code": "错误代码",
    "message": "面向用户的错误说明",
    "retryable": false,
    "details": null
  }
}
```

`retryable=true` 只能说明网络或服务异常可能暂时可重试。答案提交、合同审核和文书生成不要盲目重复提交；合同审核请求超时或连接中断时，优先根据错误详情中的 `sessionId` 调用一次 `resume`。

## 能力流程速查

### 法律咨询和法律计算器

1. 用 `catalog` 查询项目；咨询的后端目录模块为 `m=2`，计算器为 `m=1`。
2. 选择有实际 `projectId` 的具体项目，不要选择只有分类用途的父级节点。
3. 用 `question-start` 创建任务并保存 `sessionId`。
4. 处理返回的 `interaction`：只依据当前任务消息、当前任务材料和当前 `sessionId` 答案自动作答，再询问真正缺失的字段；禁止跨任务记忆。
5. 用 `question-reply` 逐题推进；出现 `needs_follow_up` 时先完成本地追加题。
6. 到达 `ready_for_report` 后调用 `question-report`。

详细的字段匹配、控件降级和追加题规则见 [`references/interaction.md`](references/interaction.md)、[`references/consultation.md`](references/consultation.md) 和 [`references/calculator.md`](references/calculator.md)。

### 智能合同审核

1. 用户没有说明立场时，先询问“我方是甲方还是乙方”。甲方传 `contractualStanding: 1`，乙方传 `2`。
2. 确认立场后再收集合同文件；立场未知时不得上传文件或创建审核记录。
3. 用 `contract-review` 发起审核。正常情况下接口会阻塞等待并直接返回完整结果，不需要轮询详情接口。
4. 按高、中、低风险展示风险条款、风险说明、修改建议和 `data.delivery.markdown`；同一轮发送链接后立即用宿主可用的浏览器或导航能力打开在线报告。
5. 只有请求结果不确定且错误详情明确允许恢复时，才用原 `sessionId` 调用一次 `resume`。

详细限制和结果字段见 [`references/contract-review.md`](references/contract-review.md)。

### 起诉状和答辩状

1. 用 `catalog` 查询模板，分别使用 `complaint` 或 `defense`。
2. 用 `pleading-start` 创建任务并读取模板字段。
3. 将用户已描述的全部案情、案件材料和宿主提取文字传给 `pleading-extract`。
4. 用 `pleading-update` 分步骤更新普通字段；用 `partyActions` 和 `focus` 管理多个当事人，用 `fieldPage` 切换字段页。
5. 进入确认步骤后展示完整摘要，取得用户明确确认。
6. 用 `pleading-generate` 传入 `confirmed: true`，最后在同一轮展示 `data.delivery.markdown`；文书下载链接不自动打开或预览。

文书步骤、字段分页、当事人操作和材料处理见 [`references/pleading.md`](references/pleading.md) 和 [`references/case-materials.md`](references/case-materials.md)。

## 配置

技能内置生产环境地址。只有部署测试环境或需要隔离本地任务目录时才需要覆盖配置。

| 环境变量 | 默认值 | 用途 |
| --- | --- | --- |
| `HAOLVSHI_API_BASE` | `https://front.ai.lvpin100.com/api/speed-front` | 好律狮接口根地址 |
| `HAOLVSHI_SITE_BASE` | `https://skill.ai.lvpin100.com` | 在线结果页面根地址 |
| `HAOLVSHI_SITE_ROUTE_BASE` | `''` | 在线结果页面路由前缀；为空时直接使用站点根路径 |
| `HAOLVSHI_APP_ID` | `9BED559BDD9CE535B3E5BE25A63ED00E` | 站点应用编号 |
| `HAOLVSHI_DEVICE_TYPE` | `1` | 设备类型 |
| `HAOLVSHI_STATE_DIR` | `系统临时目录/haolvshi-legal-skill` | 任务状态、身份和文书模板缓存目录 |
| `HAOLVSHI_REQUEST_TIMEOUT_MS` | `30000` | 普通接口超时时间，单位毫秒 |
| `HAOLVSHI_AUDIT_TIMEOUT_MS` | `180000` | 合同审核超时时间，单位毫秒 |
| `HAOLVSHI_NODE_MIN_MAJOR` | `20` | 可复用 Node.js 的最低主版本 |
| `HAOLVSHI_NODE_RELEASE_LINE` | `22` | 自动准备的 Node.js 发布线 |
| `HAOLVSHI_RUNTIME_DIR` | macOS/Linux：`~/.local/share/haolvshi-legal-skill/runtime`；Windows：`%LOCALAPPDATA%\haolvshi-legal-skill\runtime` | 独立 Node.js 运行环境位置 |
| `HAOLVSHI_NODE_BIN` | 空 | 指定可复用的 Node.js 可执行文件 |

旧版 `LVPIN_*` 环境变量仍可兼容读取，包括对应的接口、站点、任务目录、超时和运行时变量；新部署建议统一使用 `HAOLVSHI_*`。

本地任务状态会写入 `HAOLVSHI_STATE_DIR`，默认保存 24 小时。状态文件和文书模板缓存用于恢复任务，不应提交到代码仓库；不要在客户端配置中放置服务端工作流密钥。

## 开发和测试

在 `haolvshi-legal-skill/` 目录执行。开发机需要 Node.js 20 或更高版本。

```bash
# 检查主入口语法
npm run check

# 运行单元测试和工作流测试
npm test

# 准备技能运行环境
npm run environment

# 访问真实服务进行健康检查
npm run health
```

测试覆盖环境准备、健康检查、项目路由、当前任务证据复用、跨任务记忆隔离、材料识别、追加题、合同审核恢复、多当事人文书字段和 Word 下载链接等行为。`npm test` 中的工作流测试使用模拟接口；`npm run health` 会访问真实服务，需要网络连接。

核心目录：

```text
SKILL.md                 AI 编排规则
INSTALL.md               安装与验证
PUBLISHING.md            托管与下载要求
scripts/legal-skill.mjs  命令分发入口
scripts/*-workflow.mjs  各能力工作流
scripts/case-materials.mjs
                         案件材料识别与上下文复用
references/              面向 AI 编排的详细流程规范
tests/                   自动化测试
assets/                  报告模板和技能图标
```

## 打包与发布

所有打包产物都放在仓库根目录的 `dist/`，不要输出到 `/tmp` 等临时目录：通用包 `dist/haolvshi-legal-skill.zip`，WorkBuddy SkillHub 兼容包 `dist/haolvshi-legal-skill-workbuddy-skillhub-<版本>.zip`，开放平台专用包 `dist/haolvshi-workbuddy-open-platform-<SemVer>.zip`。

发布规则以仓库根目录的 [`AGENTS.md`](../AGENTS.md) 为准。本节只给出通用包的服务器托管操作。用户要求正式发布时，还必须继续完成 GitHub 和 ClawHub；Claude 不发布，WorkBuddy 两类包只在本地生成和校验，不打开页面或上传。

### 打包

以下命令在仓库根目录 `lvpin-skills/` 执行：

发布前先递增 `package.json`、`SKILL.md`、`_skillhub_meta.json` 和项目 README 中的版本号；线上文件名保持不变。

```bash
zip -r dist/haolvshi-legal-skill.zip haolvshi-legal-skill \
  -x '*.DS_Store' \
  -x 'haolvshi-legal-skill/assets/candidates/*' \
  -x 'haolvshi-legal-skill/assets/candidates'

shasum -a 256 dist/haolvshi-legal-skill.zip | tee dist/checksums.txt
```

约束：

- 压缩包内路径必须以 `haolvshi-legal-skill/` 开头；
- 不得将 `assets/candidates/` 打入发布包；
- `README.md`、`INSTALL.md` 和 `PUBLISHING.md` 的变更只有在重新打包后才会进入技能包。

### 发布到 SSH 服务器

通用技能包发布到 SSH 主机 `baidu-zx-1`：

```bash
rsync -av \
  dist/haolvshi-legal-skill.zip \
  haolvshi-legal-skill/INSTALL.md \
  haolvshi-legal-skill/assets/haolvshi-legal-skill-icon.png \
  baidu-zx-1:/www/lvpin_data/docker/nginx/html/skill/skills/haolvshi-legal-skill/
```

不要使用 `--delete` 清理服务器的 `/skills/` 目录；静态文件覆盖后不需要重新加载 nginx。

服务器发布只是完整发布的一部分；随后按根目录 `发布平台说明.md` 同步 GitHub 公开仓库并创建 Release、提交 ClawHub 新版本。仓库层面不再重复询问发布确认。Claude 不发布；WorkBuddy 两个专用包只生成到 `dist/` 并完成内容校验。

### 发布官网

只有修改官网源码、页头 logo 或 favicon 时才需要重新构建官网：

```bash
cd haolvshi-legal-skill-site
pnpm build
cd ..

rsync -av --delete --exclude 'skills/' \
  haolvshi-legal-skill-site/dist/client/ \
  baidu-zx-1:/www/lvpin_data/docker/nginx/html/skill/
```

构建命令会将静态导出结果整理到 `dist/client/`；发布时必须同步 `dist/client/`，不要直接同步 `out/`。官网同步时必须保留 `--exclude 'skills/'`，避免删除已上传的技能包。

### 发布后检查

```bash
curl -sI https://skills.ai.lvpin100.com/skills/haolvshi-legal-skill/INSTALL.md
curl -sI https://skills.ai.lvpin100.com/skills/haolvshi-legal-skill/haolvshi-legal-skill.zip
curl -sI https://skills.ai.lvpin100.com/skills/haolvshi-legal-skill/haolvshi-legal-skill-icon.png

curl -sL https://skills.ai.lvpin100.com/skills/haolvshi-legal-skill/haolvshi-legal-skill.zip \
  | shasum -a 256
```

线上 zip 的校验值必须与 `dist/checksums.txt` 一致。线上安装使用 zip 地址：

```bash
npx skills add https://skills.ai.lvpin100.com/skills/haolvshi-legal-skill/haolvshi-legal-skill.zip --skill haolvshi-legal-skill
```

改过技能包后，已安装用户不会自动更新，需要重新导入 zip。

## 常见排障

### 返回 `needs_material_extraction`

说明脚本无法直接读取某个 PDF、Word、表格或图片。使用宿主真实可用的文件工具提取文字，将结果放入 `extractedTexts` 后重试；不要直接跳过该文件。

### 返回 `needs_selection`

说明关键词对应多个项目或模板。结合父级领域、具体项目名称和用户完整案情选择唯一候选；不要把没有实际项目编号的分类节点当成可执行项目。

### 返回 `needs_follow_up`

说明主选项触发了追加题。继续使用原 `sessionId` 调用 `question-reply`，直到追加题全部完成。`data.backendRequestPending=true` 时不要另行请求后端下一题。

### 任务无法恢复

- `SESSION_NOT_FOUND`：任务已不存在或已被清理，需要重新开始；
- `SESSION_CORRUPTED`：本地状态文件损坏，需要重新开始；
- `SESSION_CAPABILITY_MISMATCH`：不要跨能力复用任务编号；
- 合同审核网络中断：仅在错误详情中的 `canResume=true` 时调用一次 `resume`。

更多错误代码和处理策略见 [`references/errors.md`](references/errors.md)。

## 隐私和清理

- 只向好律狮服务发送完成当前流程所需的信息；
- 不在聊天回复和日志中输出身份证号、合同全文、服务端配置或密钥；
- 用户要求删除本地任务材料时，调用 `cleanup`；
- 不需要指定任务编号时，`cleanup` 会清理超过 24 小时的任务；
- 返回登录、验证码、付费或服务端配置错误时，应说明实际限制，不绕过服务端校验。

指定任务清理：

```bash
printf '%s' '{"sessionId":"任务编号"}' | sh scripts/run.sh cleanup
```

清理全部过期任务：

```bash
sh scripts/run.sh cleanup
```
