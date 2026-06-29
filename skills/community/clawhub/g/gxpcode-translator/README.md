这是一个适合Agent的专业翻译工具SKILL。

---
name: gxpcode-translator
description: 专业翻译工具 — 支持文本和 PDF 输入，PDF 输出双语对照 HTML + Markdown。触发关键词：翻译、术语保护、更新术语、词典、glossary、保留特定词。
agent_created: true
allowed-tools:
  - Read
  - Write
  - Edit
  - PowerShell
  - WebFetch
---

# Gxpcode-translator

专业翻译工具。核心能力：**翻译**。使用术语词典，AC 机，OCR、LLM等组件来完成文本翻译和PDF翻译。
- 术语词典我们使用.csv格式进行维护
- AC机在SKILL内自带
- OCR在线服务我们选择PaddleOCR的API服务。（经过多方实测，目前免费且效果不错）。本地部署ORC：如果您的翻译内容有保密需要，可以联系我们（zhonghe1991@qq.com）提供本地部署的适配该项目的OCR本地模型（精度与PaddleOCR持平，在翻译任务上有更好效果）。
- LLM用户自行选择


## 🛑 前置检查：首次配置

> **触发条件**：`config.json` 中 `configured` 为 `false`。
> **适用范围**：所有路由（text、PDF、及未来新增）。进入任何路由前先执行本检查。

当检测到 `configured` 为 `false` 时，**必须以对话形式依次询问用户以下 4 项配置**，不得跳过，每项提供默认值和示例：

> **交互约定**：所有带默认值的项，用户回复 `Y` / `y` / `默认` 即采用默认值。领域（第 3 项）无默认值，必须用户显式填写。

### 1. 输出目录
询问："请输入翻译输出目录，回复 Y 使用默认值 [默认: ./translation-output]"
- 用户回复 `Y` / `y` / `默认` 或未提供路径 → 采用默认值
- 自动创建目录及 logs 子目录

### 2. 术语库路径
询问："请选择术语词典 CSV 文件，回复 Y 使用内置术语库 [默认: Gxpcode-dict.csv]"
- 示例：`Gxpcode-dict.csv`（内置制药） / `/path/to/my-dict.csv`（自定义）
- 用户回复 `Y` / `y` / `默认` → 使用内置 `Gxpcode-dict.csv`

### 3. 领域（🛑 强制必填，无默认值）
> ⚠️ **领域配置对翻译结果有重大影响。必须认真填写，不可跳过。**

询问："翻译所属专业领域是什么？（必填，对翻译质量影响重大）"
- 示例：`制药` / `半导体` / `医疗器械` / `化工` / `生物技术` / `法律` / `金融`
- **不可为空**，为空或回复 `Y` 则重新提示，直到用户显式填写
- 如果用户不确定，引导其描述所翻译文档的主题，帮助确定领域

### 4. 领域子模块（可空）
询问："领域内的细分方向是什么？可填写多个，回复 Y 跳过 [可空]（不建议跳过）"
- 示例：`GMP` / `药品研发` / `药品注册` / `工艺验证` / `临床前研究`
- 用户回复 `Y` / `y` / `默认` / `无` → 跳过（不推荐）
- 支持多个子模块，用 `、` 或 `,` 分隔，如 `药品研发、药品注册`

全部完成后，写入 `config.json` 并将 `configured` 设为 `true`，输出配置摘要供用户确认。

<details>
<summary>参考：PowerShell 写入逻辑</summary>

```powershell
$configPath = "$env:USERPROFILE\.workbuddy\skills\gxpcode-translator\config.json"
$config = Get-Content $configPath | ConvertFrom-Json

# ... 对话收集上述 4 项后 ...

$config.output_dir = $outDir
$config.dict_path = $dictPath
$config.domain = $domain
$config.subdomain = $subdomain
$config.configured = $true
$config | ConvertTo-Json | Set-Content $configPath -Encoding UTF8
```
</details>

> `skill_dir` 和 `python_exe` 自动检测写入。配置仅执行一次，后续可通过编辑 `config.json` 修改。

## 🛑 输出铁律（最高优先级，不可违反）

### 纯文本模式

**对话框中仅允许输出纯译文。禁止输出术语表、匹配统计、自检表格、翻译说明、日志路径等任何其他内容。**

唯一例外：术语库中找不到对应译法、需要向用户确认时，可输出询问信息。

### PDF 翻译模式

**任何译文内容不得出现在对话中。**

| 允许在对话框中输出 | 禁止在对话框中输出 |
|---|---|
| 进度行（`🌐 翻译中... 3/10`） | 任何翻译文本 |
| 状态行（`✅ 翻译完成: 10/10`） | HTML/MD/表格内容 |
| 校验结果（`P5: 4/4 ✅`） | 术语表 |
| 文件路径 | 单个术语译文 |

> **自检**：每次回复前，扫描回复内容是否包含译文字符。如有 → 删除，替换为文件路径引用。

## 禁止行为（执行前必读）

1. **禁止手写译文**：翻译必须调用 AI（用下方 Prompt 模板），不得自己写或猜译文
2. **禁止多余 PowerShell**：只在实际需要执行逻辑时调用 PowerShell；`Write-Output` 打印验证一律跳过
3. **纯文本模式仅输出纯译文**：禁止输出术语表、匹配统计、自检表格、解释说明、日志路径等任何非译文内容。唯一例外是术语库找不到译法需确认时
4. **禁止在对话框展示 PDF 翻译内容**：PDF 逐页翻译仅写入 `*_trans.md` 文件，对话框仅显示进度（每页一行）
5. **文件写入尽量合并**：日志写入尽量在一次 PowerShell/Python 调用中完成
6. **禁止机翻痕迹**：严禁出现以下机械直译模式——
   - "to be X" → "待X"（如 "to be steamed" ≠ "待蒸汽灭菌"，应为"需蒸汽灭菌"）
   - "be done" → "被XX"（中文尽量用主动语态）
   - 不考虑上下文直接套固定译法

## 触发方式

用户通过 `/trans` 指令或自然语言（"翻译这段话"、"translate this"）触发。

## 词典

- **路径**：从 `config.json` 读取 `dict_path`，默认 `Gxpcode-dict.csv`（skill 安装目录下）
- **格式**：CSV（UTF-8 with BOM），三列 `en,cn,explain`
- **记录数**：（持续维护中）
- **CSV 已按 en 长度降序排列**，长词在前，保证长词优先匹配

## 路径约定

> 本文档中所有 PowerShell 示例使用以下变量，实际运行前由主流程赋值：

| 变量 | 含义 | 示例 |
|---|---|---|
| `$SkillDir` | gxpcode-translator 安装目录 | `~/.workbuddy/skills/gxpcode-translator` |
| `$PythonExe` | Python 可执行文件 | `~/.workbuddy/binaries/python/envs/default/Scripts/python.exe` |

> 跨平台时只需修改这两个变量，其余路径自动跟随。

**读取方式（每次使用 Skill 时）**：

```powershell
$config = Get-Content "$env:USERPROFILE\.workbuddy\skills\gxpcode-translator\config.json" | ConvertFrom-Json
$SkillDir = $config.skill_dir
$PythonExe = $config.python_exe
$DictPath = $config.dict_path
if (-not [System.IO.Path]::IsPathRooted($DictPath)) { $DictPath = "$SkillDir\$DictPath" }
$Domain = $config.domain
$Subdomain = $config.subdomain
```

> `skill_dir` 和 `python_exe` 由首次配置自动检测写入。`dict_path`、`domain`、`subdomain` 在首次对话中由用户指定。换平台时编辑 `config.json` 即可。

## 领域配置（Prompt 身份适配符）

**每次加载 Prompt 模板前**，从 `config.json` 读取 `domain` 和 `subdomain`，将模板中的 `{domain}` 和 `{subdomain}` 替换为实际值。

| 配置项 | config.json 字段 | 默认值 | 说明 |
|---|---|---|---|
| 领域 | `domain` | `""`（空，强制必填） | 翻译所属专业领域，对译文质量有重大影响 |
| 子模块 | `subdomain` | `""` | 领域内的细分方向，如 `药品研发`、`GMP`、`药品注册` 等 |

**替换规则**：

| 条件 | 模板替换结果 |
|---|---|
| `subdomain` 非空 | `你是{domain}领域({subdomain})专业翻译` → `你是制药领域(GMP)专业翻译` |
| `subdomain` 为空 | `你是{domain}领域专业翻译` → `你是制药领域专业翻译`（去掉空括号） |

> 受影响的 Prompt 模板位于 `modules/translate-core.md`：模式一 Agent Prompt、模式二文本翻译 Prompt、表格拆行翻译 Prompt。

### 翻译质量反馈 → 提示修改领域

当用户反馈译文不准确、术语错误、"翻译得不对"时，主动询问：

> "当前领域配置为「{domain}」子模块「{subdomain}」，是否准确？如需修改，我可以更新 `config.json` 中的 `domain` 和 `subdomain`。"

- 用户确认新领域后，更新 `config.json` 并重新翻译

## 输出路径配置

> 首次使用 PDF 路由时，自动触发配置采集（见 `modules/Gxpcode-pdf-input.md` 步骤 0.6）。
> **PaddleOCR API Token 仅在 PDF 路由首次使用时询问**，不属于 SKILL 通用首次配置。
> 所有路径从 `config.json` 读取，不硬编码。

| 配置项 | config.json 字段 | 默认值 | 说明 |
|---|---|---|---|
| PaddleOCR Token | `paddleocr_token` | （必填） | PDF 解析 API 令牌 |
| 输出根目录 | `output_dir` | `./translation-output/` | 双语 HTML/MD + 日志 + 中间产物，全部在此目录下 |
| HTML 文件 | `{output_dir}/{ts}-{slug}/Gxpcode-{title}.html` | — | 双语对照 HTML |
| MD 文件 | `{output_dir}/{ts}-{slug}/Gxpcode-{title}.md` | — | 双语对照 Markdown |
| 日志 | `{output_dir}/logs/{ts}_trans.md` | — | 翻译日志 |
| 中间产物 | `{output_dir}/{ts}-{slug}/` | — | paddleocr/、pages/、translated.json |

---

## 工作流

本 Skill 采用**渐进式加载**——SKILL.md 只做路由，实现细节在子模块中按需加载。

### 步骤 1：解析输入 → 路由决策

从用户消息中提取：
- 待翻译文本（可能来自直接输入或 PDF 附件）
- 翻译方向：英→中 / 中→英（如未指定，自动检测）

**输入类型检测**：用户上传 `.pdf` 文件？→ PDF 路径；否则 → 文本路径。

#### 路由表

> **加载铁律**：以下 MANDATORY 标记的文件必须在对应阶段读取后才能继续。不读 = 走的是空壳分支。

| 场景 | 加载模块 | 说明 |
|---|---|---|
| **PDF 输入** |  **MANDATORY**: [modules/Gxpcode-pdf-input.md](modules/Gxpcode-pdf-input.md) 步骤 0 | 文件存在性检查 |
| PDF → 加密检测 |  **MANDATORY**（不可跳过）: [modules/Gxpcode-pdf-input.md](modules/Gxpcode-pdf-input.md) 步骤 0.5 | pdfplumber 检测加密，加密则立即终止 |
| PDF → 解析 | **MANDATORY**: [modules/Gxpcode-pdf-input.md](modules/Gxpcode-pdf-input.md) 步骤 1 | paddleocr-parser 解析 |
| PDF → 截断修复 |  **MANDATORY**（不可跳过）: 运行 `scripts/fix_truncations.py` | 修复所有截断页的 md 文件 |
| PDF → Agent 自扫自译 | → **MANDATORY**: [modules/translate-core.md](modules/translate-core.md) 步骤 3 模式一 | 5页/组，Agent自扫术语+翻译（并发 ≤8） |
| PDF → merge + 校验 | → **MANDATORY**（`merge_translations.py` 强制内置）: ① 完整性 → ② 合并 → ③ 类型分布 → ④ 表格行数 | 出口有 3 种可能（见下方 merge 出口表） |
| PDF → 导出 | → **MANDATORY**: [modules/Gxpcode-export.md](modules/Gxpcode-export.md) 步骤 B/C | 生成 Gxpcode.html + Gxpcode.md |
| 文本输入 |  **MANDATORY**: [modules/translate-core.md](modules/translate-core.md) | 术语扫描 → AI 翻译 → 自检 → 输出 |
| 文本 → 日志 |  **MANDATORY**: [modules/logging.md](modules/logging.md) | 日志写入 |

**merge 出口表**（`merge_translations.py` 的 3 种结果）：

| 出口 | 条件 | 主流程动作 |
|---|---|---|
| exit 0 无告警 | 全部通过 | → 直接导出 |
| exit 0 有告警 | 验表不通过（`_fix_pages.json` 存在） | → 读 `_fix_pages.json` → 重译问题页 → 回写 → 重新 merge（最多 2 轮） |
| exit 2 | 完整性不通过（缺页/空页，`_retry_pages.json` 存在） | → 读 `_retry_pages.json` → 起 Agent 补跑缺失页 → 重新 merge（最多 2 轮） |

> **循环上限**：同一问题最多 2 轮修复。2 轮后仍失败 → 报告用户，标注遗留问题，跳过继续导出。
| PDF → 日志 | → **MANDATORY**: [modules/logging.md](modules/logging.md) | 日志写入 |
| **文本输入** |  **MANDATORY**: [modules/translate-core.md](modules/translate-core.md) | 术语扫描 → AI 翻译 → 自检 → 输出 |
| 文本 → 日志 |  **MANDATORY**: [modules/logging.md](modules/logging.md) | 日志写入 |

**加载顺序**：按路由表自上而下逐条触发，不得预加载所有模块。

### PDF 路由完整流程与分支

```
用户提交 PDF
  │
  ├─ 步骤 0   文件存在性检查              【强制】
  ├─ 步骤 0.5 PDF 加密检测（加密→终止）   【强制】
  ├─ 步骤 1   paddleocr 解析              【强制】
  ├─ 步骤 1.5 fix_truncations 截断修复    【强制】
  ├─ 步骤 2   5页切组 → Agent 自扫自译    【强制】（并发≤8，79页=16组分2批）
  │
  └─ 步骤 3   merge + 校验               【强制】
        │
        ├── 出口A: exit 0 无告警 ──→ 步骤 4 导出
        │
        ├── 出口B: exit 0 + _fix_pages.json ──→ 修复循环 ──→ 重 merge
        │         （类型分布/表格行数不一致，最多 2 轮）
        │
        └── 出口C: exit 2 + _retry_pages.json ──→ 补跑循环 ──→ 重 merge
                  （缺页/空页，最多 2 轮）

  ├─ 步骤 4   导出 HTML + MD              【强制】
  └─ 步骤 5   写日志 + preview_url        【强制】
```

| 步骤 | 性质 | 触发条件 |
|---|---|---|
| 0 文件检查 | 强制 | 无条件 |
| 0.5 加密检测 | 强制 | 无条件；加密即终止 |
| 1 paddleocr | 强制 | 无条件 |
| 1.5 截断修复 | 强制 | 无条件 |
| 2 Agent 自扫自译 | 强制 | 无条件 |
| 3 merge+校验 | 强制 | 无条件；按出口分叉 |
| ↳ 补跑循环 | 条件强制 | exit 2 触发，读 `_retry_pages.json`，最多 2 轮 |
| ↳ 修复循环 | 条件强制 | `_fix_pages.json` 存在触发，最多 2 轮 |
| 4 导出 | 强制 | merge exit 0 无告警，或循环用尽后 |
| 5 日志 | 强制 | 导出完成后 |

**循环上限**：同一问题最多 2 轮。2 轮后仍失败 → 报告用户，标注遗留问题，跳过继续导出。

**merge 三项校验**（`merge_translations.py` 内置，顺序执行）：

| 顺序 | 校验项 | 失败时 |
|---|---|---|
| ① | 完整性（缺页/空文件） | exit 2，写 `_retry_pages.json` |
| ② | 合并（按元素对齐） | 打印 `[missing]`/`[continuation]`，不阻塞 |
| ③④ | 元素类型分布 + 表格行数 | return False，写 `_fix_pages.json` |

---

## 术语匹配实现

脚本：`term_match.py`（位于 skill 目录下）

**设计原则**：使用 pyahocorasick 库实现真正的 Aho-Corasick 自动机。术语一次遍历完成全部匹配。长词优先，大小写不敏感。`quick_check` 子串预判跳过无需匹配的文本。输出 JSON 格式与旧版兼容。

**调用方式**：
```powershell
& "$env:USERPROFILE\.workbuddy\binaries\python\envs\default\Scripts\python.exe" `
  "$env:USERPROFILE\.workbuddy\skills\gxpcode-translator\term_match.py" "<原文>"
```

**输出 JSON**：
```json
{
  "source_text": "原文",
  "placeholder_text": "{{T001}} integrity testing should be performed before use.",
  "matches": [{"start": 0, "end": 20, "en": "sterilization filter", "cn": "除菌过滤器"}],
  "placeholder_map": [{"pid": "{{T001}}", "en": "sterilization filter", "cn": "除菌过滤器"}],
  "match_count": 1
}
```

流程中仅消费 `matches` 字段提取 `en→cn` 映射对。占位符替换功能保留可供手动调试用。

## 词典维护

用户可通过以下方式维护词典：
1. 直接编辑 `Gxpcode-dict.csv`（推荐用 Excel 打开 CSV 编辑）
2. 新增行追加到文件末尾即可
3. 修改后无需重建索引，下次翻译自动生效

**CSV 格式要求**：
```csv
en,cn,explain
sterilization filter,除菌过滤器,
qualification,确认,
bio-decontamination,去生物污染,通过使用杀孢子剂消除活性生物负荷的工艺。
```

## 交互示例

**示例 1（文本，默认）**
用户：`/trans Sterilization filter integrity testing should be performed before use.`
输出：`除菌过滤器完整性测试应在使用前执行。`
日志：自动写入 `~/.workbuddy/skills/gxpcode-translator/logs/YYYY-MM-DD_HH-MM-SS_trans.md`

**示例 2（PDF）**
用户上传 `SOP-Validation.pdf` 并说 `/trans`
1. 加载 `modules/Gxpcode-pdf-input.md` → paddleocr-parser 解析 PDF（步骤 0~1.4）
2. **必须执行** `fix_truncations.py` 修复截断页（步骤 1.5，不可跳过）
3. 按 5 页切组（79 页 → 16 组）→ 分 2 批并发 Agent（每批 ≤ 8）
   - Agent 内部：term_match 自扫 → 翻译 → 输出 `_pXXX_trans.md`
4. 完整性检测：缺失页自动补跑（最多 2 轮）
5. merge + 表格行数校验（自动验表 → 不通过则修复循环）
6. 导出 Gxpcode.html + Gxpcode.md
7. 写日志 + `preview_url`
