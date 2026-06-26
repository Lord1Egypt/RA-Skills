# 候选人上传工作流 (candidate-upload)

将 `resume-ingest` 生成的简历包中的确定性候选人草稿，上传到腾讯文档智能表格。

## 目录

- 目标
- 输入
- 前置条件
- 流程
- 数据映射规则
- 智能表格管理
- 隐私考量
- 错误处理
- 预期回复

## 目标

将候选人简历包中的确定性草稿映射为智能表格记录，实现招聘流程的结构化跟踪。HR/LLM 审核输出用于人工补全，不会被 `upload_to_smartsheet.py` 自动消费。

## 输入

- 简历包目录（由 `resume-ingest` 生成）
- 默认固定智能表格名：`HR候选人库`
- 可选：已有智能表格 `file_id`，用于覆盖默认搜索结果
- 可选：知识库 `space_id`

## 前置条件

### 1. mcporter CLI

```bash
npm install -g mcporter
```

验证：

```bash
mcporter --version
```

### 2. 腾讯文档授权

先确保已安装 `tencent-docs` skill。优先使用当前运行器支持的 skill registry，例如：

```bash
openclaw skills install tencent-docs
openclaw skills info tencent-docs
```

如果使用 SkillHub、ClawHub 或其他 registry，也可安装同名 skill。安装后不要假设 `tencent-docs` 一定与 `hr-recruiting-tracker` 是兄弟目录；优先用 `TENCENT_DOCS_SKILL_DIR` 显式指定，未指定时再尝试 OpenClaw 默认路径。

以下是外部依赖的授权排障流程。只运行已安装且已审阅的 `tencent-docs` skill 中的脚本；参考该技能的 `references/auth.md`：

```bash
# 检查授权状态
export TENCENT_DOCS_SKILL_DIR="${TENCENT_DOCS_SKILL_DIR:-$HOME/.openclaw/workspace/skills/tencent-docs}"
bash "$TENCENT_DOCS_SKILL_DIR/setup.sh" tdoc_check_and_start_auth

# 如果返回 AUTH_REQUIRED，让用户在浏览器完成授权
# 授权完成后，获取 Token
bash "$TENCENT_DOCS_SKILL_DIR/setup.sh" tdoc_fetch_token

# 手动配置 Token（备选）
mcporter config add tencent-docs "https://docs.qq.com/openapi/mcp" \
    --header "Authorization=$TENCENT_DOCS_TOKEN" \
    --transport http --scope home
```

### 3. 已完成 resume-ingest

确保简历包目录存在且包含：
- `candidate_draft.json`
- `extraction_report.json`

## 流程

### 完整流程（首次使用）

```
1. 运行依赖检查
   → python3 {baseDir}/scripts/dependency_check.py --workflow candidate-upload
   → python3 {baseDir}/scripts/dependency_check.py --workflow candidate-upload --probe-remote

2. 授权排障（仅在腾讯文档未授权或远程探测失败时）
   → export TENCENT_DOCS_SKILL_DIR="${TENCENT_DOCS_SKILL_DIR:-$HOME/.openclaw/workspace/skills/tencent-docs}"
   → bash "$TENCENT_DOCS_SKILL_DIR/setup.sh" tdoc_check_and_start_auth

3. 先离线预览脱敏草稿数据
   → python3 {baseDir}/scripts/upload_to_smartsheet.py "/path/to/bundle" --dry-run

4. HR 确认需审核记录后，搜索固定候选人库并上传草稿
   → python3 {baseDir}/scripts/upload_to_smartsheet.py "/path/to/bundle" --confirmed-reviewed

说明：

- 脚本必须先通过 `manage.search_file` 查找标题精确等于 `HR候选人库` 的智能表格。
- 如果找到，复用该 `file_id` 并追加一条候选人草稿记录。
- 如果找不到，才创建新的 `HR候选人库`。
- 只有显式传入 `--create-new` 时，才允许跳过搜索并创建新候选人库。
- 如果找到多个同名 `HR候选人库`，使用搜索结果中的第一个，并提示 HR 可用 `--file-id` 指定唯一候选人库。
- `--dry-run` 默认不联网，且默认脱敏；需要探测远程表时显式加 `--probe-remote`。
- 如果 `extraction_report.json` 显示 `review_required=true`，实际上传必须加 `--confirmed-reviewed`。
```

### 追加流程（已有表格）

```
1. 上传候选人草稿
   → python3 {baseDir}/scripts/upload_to_smartsheet.py "/path/to/bundle" --file-id "file_id" --confirmed-reviewed
```

### 强制新建流程

```
1. 强制创建新候选人库
   → python3 {baseDir}/scripts/upload_to_smartsheet.py "/path/to/bundle" --create-new --sheet-title "候选人库-测试" --confirmed-reviewed
```

### 空间内强制新建流程

```
1. 在知识库空间内创建新的候选人库
   → python3 {baseDir}/scripts/upload_to_smartsheet.py "/path/to/bundle" --create-new --sheet-title "候选人库" --space-id "space_id" --confirmed-reviewed
```

### 预览流程

```
1. 离线预览草稿数据（不写入、不联网、默认脱敏）
   → python3 {baseDir}/scripts/upload_to_smartsheet.py "/path/to/bundle" --dry-run

2. 需要确认远程候选人库解析逻辑时，显式探测远程
   → python3 {baseDir}/scripts/upload_to_smartsheet.py "/path/to/bundle" --dry-run --probe-remote
```

## 数据映射规则

候选人表字段模型统一维护在：

```text
assets/schemas/recruiting_tables.json
```

`upload_to_smartsheet.py` 必须从该文件读取 `candidates` 字段定义，不要在脚本或 Agent 回复中临时创造字段。

当前版本只消费 `candidate_draft.json` 和 `extraction_report.json`。`assets/templates/prompts/resume_extract_prompt.md` 生成的审核 JSON 供 HR/LLM 审核和人工补全使用，不会被上传脚本自动写入。

### 从 candidate_draft.json 提取

| 目标字段 | 来源路径 | 映射规则 |
|----------|---------|---------|
| 姓名 | `identity.name` | 直接映射 |
| 电话 | `identity.phone` | 直接映射（注意隐私） |
| 邮箱 | `identity.email` | 直接映射 |
| 当前公司 | `profile.current_company` | 直接映射 |
| 工作年限 | `profile.years_of_experience` | 直接映射（数字类型） |
| 技能标签 | `profile.skill_mentions` | 取前 8 个技能，顿号连接 |
| 简历来源 | `source.file_name` | 直接映射 |

### 从 education_evidence 推断

| 目标字段 | 推断逻辑 |
|----------|---------|
| 最高学历 | 归一化 PDF 空格后匹配 "博士/硕士/本科/大专" 关键字，取最高者，写入文本字段 |
| 毕业院校 | 只写学校名，例如 `长 沙 学 院 计 算 机科学与技 术(本科)` 应写为 `长沙学院` |
| 专业 | 只写专业名，例如上例应写为 `计算机科学与技术` |
| 毕业年份 | 从教育时间段中取结束年份，例如 `2017.09 - 2023.06` 应写为 `2023` |

教育字段拆分规则：

- 先修复 PDF 文本层引入的中文空格，例如 `中 南 大学` → `中南大学`、`计 算 机科学与技 术` → `计算机科学与技术`。
- 再按学校后缀（如 `大学`、`学院`、`学校`）拆出学校名。
- 再按学历关键词（如 `博士`、`硕士`、`本科`、`大专`）拆出学历。
- 学校名与学历之间的内容通常是专业名，应填入 `专业`。
- 不得把整段教育经历原文写入 `毕业院校`、`专业`、`最高学历` 或 `毕业年份`。无法可靠拆分时留空，并让 HR 审核。
- 多段教育经历同时存在时，默认选择最高学历对应的学校、专业和毕业年份。

### 从 extraction_report.json 提取

| 目标字段 | 来源路径 | 映射规则 |
|----------|---------|---------|
| 解析质量 | `quality` | "high"→"高保真", "fallback"→"回退解析", 其他→"纯文本" |
| 需HR审核 | `review_required` | 直接映射为复选框状态 |

如果 `review_required` 为 `true`，脚本会阻止实际上传，直到 HR 审核后显式传入 `--confirmed-reviewed`。`--dry-run` 不受此限制，可用于预览映射结果。

### 系统生成的字段

| 目标字段 | 生成规则 |
|----------|---------|
| 招聘阶段 | 默认"简历筛选"，写入文本字段 |
| 求职意向 | 当前版本为 null（待 LLM 提取） |
| 简历包路径 | `file://` 协议的本地路径，写入文本字段 |
| 录入时间 | 当前时间的毫秒时间戳 |
| 记录ID | `{姓名}-{简历 sha256 前 12 位}` |

## 智能表格管理

### 新建表格时自动执行

只有固定表名搜索不到，或用户显式指定 `--create-new` 时才执行新建。

1. 创建智能表格文档（`smartsheet` 类型）
2. 获取默认工作表 `sheet_id`
3. 批量添加 18 个候选人字段
4. 删除默认空行（建表自动生成的无内容行）
5. 删除默认列（不在候选人字段定义中的列）

### 追加到已有表格时

1. 默认按固定标题 `HR候选人库` 检索已有表格，或使用用户传入的 `--file-id`
2. 检查已有字段，只添加缺失的字段
3. 不修改已有字段定义
4. 不删除任何已有数据
5. 直接追加草稿记录

### 字段冲突处理

- 字段名已存在：跳过，不修改
- 选项值不一致：使用已有选项定义（写入时 `text` 必须匹配）
- 字段类型不一致：报错，提示手动处理

当前实测注意：

- `tencent-docs` 1.0.33 的 `smartsheet.add_fields` 在新建 `singleSelect/select` 字段时可能返回 `22020: Smartsheet invalid select field`。因此本工作流默认把 `最高学历`、`招聘阶段`、`解析质量` 建为文本字段，先保证候选人入库可用。
- 本地 `file://` 简历包路径无法被腾讯文档云端访问，本工作流将其作为文本证据路径保存，不使用超链接字段。
- 终端输出默认脱敏；如确需核对完整电话、邮箱、路径和记录 ID，可在本地安全终端中显式加 `--show-sensitive`。

## 隐私考量

- ⚠️ 候选人姓名、电话、邮箱会直接写入腾讯文档在线表格
- ⚠️ 写入前需确认 HR 已获得候选人授权
- ⚠️ 建议在展示层对电话做脱敏（如只显示后 4 位）
- ⚠️ dry-run 默认不会连接腾讯文档，也不会打印完整敏感字段
- ⚠️ `resume.md` 和 `resume.raw.json` 不会上传，仅保留在本地
- ⚠️ `resume_extract_prompt.md` 的输出不会自动上传；需要 HR 在表格中人工补全或修正

## 错误处理

### 常见错误

| 错误 | 原因 | 解决 |
|------|------|------|
| `mcporter: command not found` | mcporter 未安装 | `npm install -g mcporter` |
| `MCP 错误: 400006` | Token 鉴权失败 | 按授权排障流程重新检查 |
| `MCP 错误: 400007` | VIP 权限不足 | 升级腾讯文档 VIP |
| `找不到 candidate_draft.json` | 未完成 resume-ingest | 先运行 resume_extract.py |
| `智能表格中没有工作表` | 文件不是智能表格 | 检查 file_id 是否正确 |
| `候选人记录尚未确认审核` | 解析报告要求 HR 审核 | HR 审核后加 `--confirmed-reviewed` |

## 预期回复

成功上传草稿后，回复以下内容：

- 候选人姓名（默认脱敏）
- 腾讯文档链接 `https://docs.qq.com/smartsheet/{file_id}`
- 解析质量（高保真/回退解析）
- 是否需 HR 审核
- 缺失的关键字段（如邮箱、电话为空）
- 提示 HR 可在智能表格中补充求职意向等信息
