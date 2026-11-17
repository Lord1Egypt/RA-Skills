---
name: "invoice-issue"
description: "发票开具与开票权限处理。当用户提出以下需求时触发：发票开具、数电票开具、数电票开票、蓝字发票开具、单张开票、批量开票、开票二维码获取、开票二维码状态查询、开票授权、开票权限校验、开票权限延长、扫码授权开票"
version: "0.1.0"
---
# 发票开具

## 安装与更新文档（强制）

首次执行本 skill 前，必须先阅读远端 Markdown 文档 `https://download.ningmengyun.com/Skills/invoice-issue/invoice-issue-install.md`，并将远端文档中的 `version` 与当前 `SKILL.md` front matter 中的本地 version `0.1.0` 比较。若 version 不一致，先提醒用户是否需要更新 skill；如需更新，必须按远端 Markdown 文档要求执行。

## README 说明文档（强制）

若本 skill 是通过 ZIP 发布包直接解压安装，或当前会话首次加载本地 `SKILL.md` 且尚未确认已按安装文档完成 `README.md` 全文输出，必须先阅读同级 `README.md`，并立即将 `README.md` 全文完整原样输出给用户；不得修改、概括、精简、重排、删减或只说明其中要求；不得等到用户开始业务执行、收集开票信息或生成命令时才输出。

首次执行本 skill 前，仍必须确认同级 `README.md` 已阅读且全文已完整原样输出给用户。在收集开票信息或生成任何业务命令前，若用户尚未满足 `README.md` 中列出的前置要求，应先完整原样输出 `README.md` 全文，再提示用户按 `README.md` 完成准备后继续。

当任一业务命令、预检报告、接口响应、命令输出或错误信息中出现“无权调用该能力”时，必须立即停止当前业务流程，按同级 `README.md` 中的 API Key 获取方式告知用户为当前 API Key 绑定对应能力权限及企业（如 `README.md` 要求绑定企业）后再重试；不得将该响应解释为税局登录失败，不得引导用户去登录或重新登录，也不得继续执行预检、快速登录、开票或其它后续业务命令。

## 平台说明

- 本 Skill 中所有执行命令的示例均以 Windows 平台为例；若运行在其它平台，可将示例中的 `.\bin\windows-amd64\invoice-assistant_windows_amd64.exe` 替换为当前平台对应的二进制：Linux x64 使用 `./bin/linux-amd64/invoice-assistant_linux_amd64`，Linux ARM64 使用 `./bin/linux-arm64/invoice-assistant_linux_arm64`，macOS x64 使用 `./bin/darwin-amd64/invoice-assistant_darwin_amd64`，macOS ARM64 使用 `./bin/darwin-arm64/invoice-assistant_darwin_arm64`。


- 若本地 `bin/<platform>/` 下缺少当前平台二进制、二进制不可执行，或用户询问二进制下载路径，必须读取远端安装文档 `https://download.ningmengyun.com/Skills/invoice-issue/invoice-issue-install.md` 中的“当前平台二进制下载表”，按当前 OS/CPU 只下载一个匹配平台的外置二进制，并保存为上方平台说明声明的本地路径；不得在 `SKILL.md` 中猜测、拼接或硬编码下载地址。

### PowerShell 下载约束（强制）

在安装或更新流程中，若使用 PowerShell 下载任何资源（包括 ZIP 包和外置二进制文件），必须且只能使用以下规则：

请帮我把以下文件下载到本地指定路径。

要求：

将 PowerShell 下载脚本写入临时 `.ps1` 文件，脚本内容格式如下：

```powershell
[System.Net.ServicePointManager]::SecurityProtocol = [System.Net.SecurityProtocolType]::Tls12
$binUrl = "<下载地址>"
$binPath = "<本地保存绝对路径>"
Invoke-WebRequest -Uri $binUrl -OutFile $binPath -UseBasicParsing
Write-Output "download complete"
```

通过以下方式执行脚本（避免直接 exec 触发 EPERM 权限问题）：

```powershell
powershell -ExecutionPolicy Bypass -File "<临时ps1脚本路径>"
```

下载完成后删除临时 `.ps1` 脚本文件。

验证目标文件已存在。

## 任务开始硬门禁（高优先级）

开始本次任务后，在任何业务命令、HTTP 请求、任务初始化、文件落盘或轮询动作之前，必须先完成以下门禁：

1. 若本机会话尚未完成 `.\bin\windows-amd64\invoice-assistant_windows_amd64.exe` 可用性检测，先执行 `.\bin\windows-amd64\invoice-assistant_windows_amd64.exe --help` 确认二进制可运行。
2. 环境就绪后，必须先严格按 [任务执行前初始化检测](./references/common/preflight-initialization-check.md) 执行预检：`.\bin\windows-amd64\invoice-assistant_windows_amd64.exe task-preflight-check`。
3. 仅当 `preflight_passed=true` 或预检命令返回成功状态时，才允许继续后续场景步骤。
4. 若配置中已有 `uscc` 且用户未明确切换企业，预检前必须先告知用户本次继续使用该税号；若用户明确切换企业，则重新执行预检，必要时追加 `--enterprise-name "企业名称或税号"`。
5. 若未配置 `workspace_dir`，不视为失败；应先告诉用户本次将默认使用 `workspace` 目录作为工作区。只有当用户明确要求改用其他目录，或目录实际不可写时，才调用 `.\bin\windows-amd64\invoice-assistant_windows_amd64.exe workspace-config-writer` 更新配置后重新预检。

## 输出内容规范

- **严禁向用户展示任何技术细节**，包括但不限于：英文字段名（如 `businessType`、`bizTypeSceneTag`、`goodTypes`、`goodsWeight`）、JSON 结构、命令行内容、命令路径、技术参数。执行过程中的中间状态（构造参数、调用接口）不展示，只展示用户需要知道的结果。
- **原样展示二进制命令生成的 Markdown**，当待展示内容来自 本地二进制命令生成的 Markdown（如预检结果文档）时，Agent **禁止一以任何目的对 Markdown 正文做任何改写**如脱敏、重排、摘要、截断或润色，必须原样渲染；不得因任何理由改写正文内容，和补充额外的内容。
- **禁止输出内容规范细节**，按照内容规范输出内容即可，不必解释规范细节；不得输出“按 SKILL.md 要求原样展示”类似的说明。
- 即使二进制命令生成的 Markdown 内容较长，也必须完整原样渲染；**禁止**以“总结版”“精简版”“关键信息摘录”等形式替代原文展示。
- Agent 所在的 WebUI 在任务执行结束后，**不得**对任务执行过程中已经输出到对话框的消息做折叠、截断、收起或仅展示摘要；必须保证用户可以正常完整回看、滚动查看和查阅全部历史回显内容。
- 若二进制命令生成的 Markdown 正文中已使用反斜杠对星号等 Markdown 特殊符号进行转义，则在输出预览或最终回显时，必须正确保留这些转义符，禁止去掉反斜杠后重新渲染或改写原文。
- 展示本地文件链接形式时，必须使用 `[本地路径](本地路径)` 形式输出，即链接文本与链接目标都使用同一个本地绝对路径字符串，以触发链接高亮；除展示形式外，不得改写路径值本身；本地路径禁止以file://开头；当路径中含有转义字符时，必须正确处理。
- **禁止输出json文件的路径**。
- 当流程出错导致 skill 意外无法继续执行时，最终回复末尾必须追加以下提示：遇到问题请点击 https://www.nmy.cn/contactService 扫码添加我们的专属客服企业微信联系我们

## 长流程执行策略

**需要在预检通过后再组织长流程执行策略**。长流程任务必须采用“先输出、再执行；先核对、再推进”的串行策略，避免工具已执行但对话框遗漏关键内容。

### 阶段推进规则（强制）

将一次任务拆分为以下 7 个阶段，任一阶段未完成“用户可见输出”前，禁止进入下一阶段：

1. 场景识别阶段：必须先输出主场景、已识别输入、待补充信息。
2. 任务清单阶段：必须先输出完整任务清单，再进入参数校验或执行。
3. 参数确认阶段：必须输出最终执行参数摘要，再发起本地二进制命令或 HTTP 请求。
4. 执行中阶段：凡是进入新子步骤、切换执行路径、开始轮询、触发兜底、生成文件，必须先在对话框说明“当前已完成什么、正在做什么、下一步是什么”。
5. 阶段结果阶段：每个子步骤一旦产出用户需要感知的结果，必须立即输出，不得缓存到最后统一补发。
6. 最终汇总阶段：必须基于前面已输出过的内容补足缺失项，不得仅说“已完成”而不展示结果。
7. 结束检查阶段：结束前必须逐项核对本场景要求输出的内容是否都已出现在对话框中；若缺任一项，先补发再结束。

### 输出门禁规则（强制）

- 只要某一步调用了工具、命令、接口、轮询或文件生成，并且该步骤按场景定义本应让用户知道结果，就必须在进入下一步前先把该结果发到对话框。
- 工具返回成功不等于用户已经看见结果；“tool output 已存在”不能替代“Agent 已在对话框中明确输出”。
- 若某一步生成了 Markdown、表格、摘要、分析结论、任务编号、下载路径、预览内容，必须在该步完成后立即输出，不能等到后续步骤结束后再一次性补发。
- 若场景文档要求“原样展示”二进制命令生成的 Markdown，则必须直接发送原文；不得只做总结或引用文件路径代替正文。
- 若进入下一步前发现上一阶段尚未向用户回显必要结果，必须立即中断当前推进，先补齐输出，再继续。

### 长流程最小输出清单（强制）

长流程中，Agent 至少必须在对话框中显式输出以下节点内容：

1. 主场景判定结果。
2. 本次任务清单。
3. 待补充参数或“参数已齐全”的确认结果。
4. 最终执行参数摘要。
5. 每个关键子步骤的完成反馈。
6. 每个关键子步骤的实际产出结果。
7. 异步任务的任务编号、轮询状态变化、终态结果。
8. 本地生成文件、下载文件、预览文件、报告 Markdown 等用户需感知的交付物。
9. 失败结果、影响范围、下一步建议。
10. 最终结果正文。

缺少任一必需节点输出，都视为长流程未完成。

### 子步骤完成后的自检问题（强制）

每完成一个子步骤，进入下一步前，Agent 必须先自检以下问题：

1. 这一步有没有产出新的、用户应该知道的信息？
2. 这些信息是否已经真正发送到对话框，而不是只存在于工具结果里？
3. 如果现在对话中断，用户是否已经看到了当前阶段所需的全部内容？
4. 下一步是否依赖当前步骤的用户可见结果作为上下文？

任一问题答案为“否”或“不确定”，都必须先补充对话框输出，再继续。

### 工具结果转用户可见内容规则（强制）

- 任务状态 JSON、命令 stdout、接口 JSON、轮询结果、文件路径、Markdown 文件内容，均属于“原始执行结果”；只有当 Agent 将其整理并发送到对话框后，才算完成该步输出。
- 若结果是结构化 JSON，必须提炼出场景要求回显的字段发送给用户；禁止只说“返回成功”。
- 若结果是 Markdown 正文且场景要求原样展示，必须完整粘贴正文到对话框。
- 若结果同时包含“用户必看字段”和“仅供内部继续执行字段”，必须先输出用户必看字段，再继续用内部字段驱动后续步骤。

### 结束前最终核对（强制）

在准备发送最终回复前，必须逐项核对：

1. 场景文档要求的成功/失败/部分成功模板内容，是否已经完整覆盖。
2. 本次流程中每个关键子步骤的结果，是否都已经在对话框回显。
3. 任何命令生成且要求展示的 Markdown，是否都已经原样输出。
4. 任何应让用户知道的任务编号、文件、预览、结论、建议，是否都已经出现。
5. 本次对话 Markdown 记录文件是否已保存到本地，且文件路径是否已经回显给用户。

若发现遗漏，禁止直接结束；必须先补充缺失输出，再发送最终答复。

## 整体执行流程

1. **首次加载 Skill 的执行环境检测（仅首次会话执行）**

- 检测本机是否可用 `.\bin\windows-amd64\invoice-assistant_windows_amd64.exe`：执行 `.\bin\windows-amd64\invoice-assistant_windows_amd64.exe --help`。
- 若不可用，请重新安装skill包或联系客服。

2. **任务执行前初始化检测（每次进入执行阶段均执行）**

- 本步骤受上文“任务开始硬门禁”约束，必须先执行，禁止跳过。
- 预检统一执行命令：`.\bin\windows-amd64\invoice-assistant_windows_amd64.exe task-preflight-check`。
- 具体的企业切换、默认工作区目录、失败中止、配置更新与重跑规则，统一以 [任务执行前初始化检测](./references/common/preflight-initialization-check.md) 为准。
- 只有当预检通过时，才允许继续读取场景定义文件、生成任务清单和执行后续业务步骤。

3. **读取场景定义文件**：读取 `references/{category}/{scene}.md`，获取参数规格、模糊处理规则、调用方式、输出模板。
4. **生成任务清单并展示给用户**

- 基于“用户已明确输入 + 场景定义文件”整理本次任务的完整执行清单。
- 清单必须覆盖：已识别主场景、当前已确认参数、待补充参数、后续主要执行步骤、可能产出的结果类型。
- 若流程较长或包含异步任务，必须按执行顺序列出关键节点，防止遗漏目录确认、参数校验、预览确认、任务轮询、结果获取等步骤。
- 展示后再进入参数补齐或正式执行。

5. **参数提取 & 完整性校验**

- 有缺失、模糊或无法完成编码转换时，一次性提示用户并重新校验。
- 若缺失项属于非必填参数，或属于后续命令/配置/接口/字典可自动补齐的参数（例如销售方上下文、购买方企业名称/税号、商品编码、税率、金额税额或整票汇总），不得因此中止流程；应标记为“可继续/待自动补齐”，继续进入后续检查、补全、预览或场景规定的下一步。
- 购买方企业搜索必须使用独立查公司能力；返回 1 个候选时可默认选择并继续，返回多个候选时必须展示候选并由用户选择，不得自动取第一条继续。
- 只有缺失原始输入阶段必填参数、存在明确冲突/歧义、或命令检查后确认无法自动补齐的前置必填参数时，才允许暂停并向用户一次性补问。
- 参数完整后进入下一步。

6. **参数展示**：必须将确认后的参数以清晰格式展示给用户。
7. **格式化输出**：严格按照场景描述输出对应内容；多步骤任务在进入下一步前，必须先检查当前步骤输出内容是否到位、完整。

## 接口响应异常处理

- 当响应对象中出现 `statusCode` 字段时，通常视为异常情况，按照[处理接口响应异常](./references/common/handle-response-exception.md)中的说明进行处理。
- Agent 给出异常提示后，必须立即终止后续流程，无需自行尝试修复问题。
- 若用户提供了新的输入，必须重新进行场景识别和参数校验，**不得**直接继续之前的流程。

## 任务清单展示（强制）

- 在预检通过后，必须先向用户展示一次“本次任务清单”，大致说明后续流程将如何展开，有哪些关键步骤

## 开票检查 input JSON 结构门禁（强制）

正常开票流程中，Agent 写入 `issue-batch-invoice-info-check --input <file>.json` 的文件时，必须构造“开票检查原始 input JSON”，不得构造正式开票接口 payload，也不得照抄任务状态 JSON 中的 `check_result.invoice_payload_json`。

开票检查原始 input JSON 必须满足：

1. 根对象必须是一个 JSON object，不得是顶层数组。
2. 根对象必须使用顶层 `invoices[]` 承载发票；即使只有 1 张发票，也必须写成只含 1 个元素的 `invoices[]`。
3. 每张发票的购方信息写入 `invoices[].purchaserInfo`。
4. 每张发票的明细写入 `invoices[].details[]`；金额、单价、税率、税额等明细字段都必须落到对应 `details[]` 元素里。
5. 用户只说“金额”“1 元”“含税金额”时，默认写入 `invoices[].details[].taxInclusiveAmount`；只有用户明确说“不含税金额”时，才写入 `amount`。
6. 顶层共享字段当前至少写入 `uscc`；`areaCode`、`personalAccount` 若用户或配置已明确可写入，未明确时交由检查脚本按 `uscc` 从配置补齐。

禁止写入以下形状作为开票检查原始 input JSON：

1. `params.info[]`、`params.goods[]`、`params.purchaserName`、`params.projectName` 等 `params` 包装结构。
2. 顶层 `info[]` 或 `invoice_payload_json.info[]` 这类正式开票 payload 结构。
3. `invoiceDetail.data[]` 作为原始明细入口；正式 payload 中的 `info[].invoiceDetail.data[]` 只能由检查脚本从 `invoices[].details[]` 标准化生成。
4. `goods[]`、`items[]`、`invoiceDetails[]`、`buyerName`、`goodsName`、`amount` 占位等自造或兼容性字段。

最小示例：

```json
{
  "uscc": "914403000838959104",
  "invoices": [
    {
      "invoiceType": "普通发票",
      "purchaserInfo": {
        "name": "深圳市时课教育科技有限公司",
        "uscc": "91440300MAD5WRCR0A"
      },
      "details": [
        {
          "projectName": "果汁",
          "taxInclusiveAmount": 1.00
        }
      ]
    }
  ]
}
```

写入 input JSON 前必须自检：根对象是否有 `invoices[]`、每张票是否有 `details[]`、是否没有 `params` 包装、是否没有直接写正式 payload 的 `info[].invoiceDetail.data[]`。任一项不满足，必须先修正 input JSON，禁止通过反复执行命令试错。

## Windows 编码与 JSON 输入规范（强制）

- 在 Windows 下执行命令时，若输入包含中文，**禁止**优先使用 stdin 管道直传 JSON（如 `.\bin\windows-amd64\invoice-assistant_windows_amd64.exe <command> --input <file>`）；应优先使用 `--input` 读取 JSON 文件。
- 传入 `--input` 的 JSON 文件必须使用 UTF-8 编码；推荐 UTF-8 无 BOM。若误写入 BOM，命令也应兼容解析，不得因此中断业务流程。
- 在 PowerShell 中生成 JSON 入参文件时，**禁止**手写内联 JSON 字符串或复杂 here-string 转义；应优先使用对象 + `ConvertTo-Json` 后落盘，规避引号和反斜杠转义问题。
- 推荐使用 .NET UTF-8 无 BOM 写文件，避免 `Set-Content -Encoding UTF8` 在 Windows PowerShell 5.1 下写入 BOM。
- `ConvertTo-Json` 输出中文原文或 `\uXXXX` Unicode 转义都属于合法 JSON，不是编码损坏；不得因为看到 `\u6df1\u5733` 这类转义就改用手写 here-string。
- 若控制台或 `Get-Content` 显示 `深圳` 变成 `娣卞湷` 这类乱码，优先判断为读取/终端显示编码不一致，而不是 JSON 文件损坏；必须用 `Get-Content -Raw -Encoding UTF8 <input.json> | ConvertFrom-Json` 做 round-trip 验证，或直接执行二进制命令验证。
- 推荐示例：

```powershell
$payload = @{
  uscc = "914403000838959104"
  areaCode = 4403
  personalAccount = "13297429706"
  invoices = @(
    @{
      invoiceType = "普通发票"
      purchaserInfo = @{
        name = "深圳市时课教育科技有限公司"
        uscc = "91440300MAD5WRCR0A"
      }
      details = @(
        @{
          projectName = "果汁"
          taxInclusiveAmount = 1.00
        }
      )
    }
  )
}
$json = $payload | ConvertTo-Json -Depth 10
$utf8NoBom = New-Object System.Text.UTF8Encoding($false)
$inputPath = "D:\\skill-test\\workspace\\workspace\\temporary\\20260424113112-9e21b8f3\\20260424113130\\input.json"
[System.IO.File]::WriteAllText($inputPath, $json, $utf8NoBom)

# 验证：必须能 round-trip 回原始中文；不要只凭控制台显示判断乱码。
$check = Get-Content -Raw -Encoding UTF8 -LiteralPath $inputPath | ConvertFrom-Json
$check.invoices[0].purchaserInfo.name
$check.invoices[0].details[0].projectName
```

- 若执行后出现中文字段变为 `????`、`??` 或接口参数异常，优先排查是否使用了 stdin 管道、`Set-Content`/`Out-File` 默认编码、或未指定 `-Encoding UTF8` 读取验证导致编码不一致，并改为“对象 -> `ConvertTo-Json` -> .NET UTF-8 无 BOM 文件 + `--input`”重试。
- 若执行报错包含 `Unexpected UTF-8 BOM`，说明输入文件含 BOM 且读取方式不兼容；应统一改为 BOM 兼容读取或重写为 UTF-8 无 BOM 后重试。
