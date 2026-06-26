---
name: hr-recruiting-tracker
description: >
  HR 招聘数据整理技能。用于本地解析 PDF/DOCX/TXT/Markdown 简历为 Markdown/JSON
  简历包、生成候选人资料草稿、将确定性候选人草稿录入腾讯文档智能表格，以及初始化或维护岗位信息库。
  Use when: resume ingestion, candidate draft extraction, Tencent Docs candidate upload,
  recruiting job table setup. 当前已实现工作流：resume-ingest、candidate-upload、job-management。
version: 0.1.0
license: MIT-0
metadata:
  openclaw:
    requires:
      bins:
        - python3
    envVars:
      - name: TENCENT_DOCS_TOKEN
        description: "腾讯文档 MCP 授权令牌；仅在手动配置 candidate-upload 或 job-management 时需要。"
        required: false
        sensitive: true
      - name: TENCENT_DOCS_SKILL_DIR
        description: "tencent-docs skill 安装目录；未设置时脚本会尝试常见 OpenClaw/Codex skill 路径。"
        required: false
        sensitive: false
---

# HR 招聘跟踪器

## 目的

使用此技能标准化招聘数据整理。已实现三个工作流：

1. **`resume-ingest`**：将简历文件转换为 AI 可读的 Markdown、原始 JSON 和候选人草稿，不写入任何外部招聘系统。
2. **`candidate-upload`**：将简历包中的确定性候选人草稿写入腾讯文档智能表格，支持招聘阶段跟踪；需 HR 审核的记录必须确认后才能上传。
3. **`job-management`**：初始化或维护固定岗位信息智能表格，并可显式导入真实岗位记录。

核心简历解析流程只依赖本地文件和 Python。腾讯文档上传和岗位库维护需要 OpenClaw 兼容 MCP 环境、`mcporter` CLI，以及已授权的 `tencent-docs` skill；高保真简历解析可选依赖 Docling，PDF 文本层回退可选依赖 `pdftotext`。引用此技能内部文件时使用 `{baseDir}`。

## 未来工作

以下能力尚未实现，只作为路线图记录，不要承诺已经可用：

- 搜索、分析和汇总已有候选人记录。
- 追加招聘事件，形成完整阶段流转日志。
- 企业微信通知。
- 面试日程或会议创建。

## 核心规则

1. 不要编造候选人事实。字段缺失时使用 `null`，或明确指出缺失字段。
2. 将生成的简历包视为机密招聘数据。
3. 默认优先使用本地安全解析器，避免意外触发外部模型下载。
4. Docling 仅作为高保真增强能力使用；当显式指定 `--parser docling` 或允许模型下载时才尝试。
5. 仅允许将回退解析器用于本地草稿提取；必须标记回退输出供 HR 审核。
6. 候选人上传工作流 (`candidate-upload`) 可将数据写入腾讯文档智能表格。写入前需先完成 `resume-ingest`。
7. 在任何工作流之前，先运行相关依赖检查。
8. 将原始证据与 AI 摘要分开保存。
9. 候选人表和岗位表的数据模型统一维护在 `assets/schemas/recruiting_tables.json`；操作腾讯文档字段时必须以该文件为准。
10. 教育经历必须拆分后入表：`毕业院校` 只能填学校名，`专业` 只能填专业名，`最高学历` 只能填学历，`毕业年份` 只能填年份。不要把整段教育经历写入单个字段。
11. 终端输出默认脱敏；只有用户明确要求排查映射细节时才使用 `--show-sensitive`。
12. `candidate-upload` 遇到 `review_required=true` 时默认禁止实际上传；HR 审核后必须显式传入 `--confirmed-reviewed`。

## 工作流判定

- 如果用户提供简历文件，并要求将其变得可读、解析、提取文本或准备候选人字段 → 使用 `resume-ingest`。
- 如果用户已拥有简历包，要求将候选人草稿录入腾讯文档智能表格 → 使用 `candidate-upload`。
- 如果用户要求初始化、维护、录入或查询岗位信息库 → 使用 `job-management`。
- 如果用户提供简历并直接要求"解析后录入系统" → 先执行 `resume-ingest`，再执行 `candidate-upload`。
- 如果用户要求搜索候选人、分析候选人库、发送企业微信消息或安排面试 → 说明这些路线图能力尚未实现。

## 统一表模型

腾讯文档智能表格字段统一维护在：

```text
{baseDir}/assets/schemas/recruiting_tables.json
```

当前表模型：

| 表 | 固定智能表格名 | 用途 |
|----|----------------|------|
| candidates | HR候选人库 | 候选人核心信息、解析质量、招聘阶段 |
| jobs | HR岗位信息库 | 岗位 JD、要求、面试流程和状态 |

脚本和 Agent 都不得临时创造字段名。若需要新增字段，先修改该模型文件，再同步更新对应 workflow 文档和测试。

## 简历导入 (resume-ingest)

运行工作流前先阅读 `references/workflow_resume_ingestion.md`。

运行：

```bash
python3 {baseDir}/scripts/dependency_check.py --workflow resume-ingest
python3 {baseDir}/scripts/resume_extract.py "/path/to/resume.pdf" --out-dir "/path/to/output-bundle"
```

默认 `auto` 策略只使用本地安全解析器。需要 Docling 高保真解析时，使用：

```bash
python3 {baseDir}/scripts/resume_extract.py "/path/to/resume.pdf" --parser docling --out-dir "/path/to/output-bundle"
```

生成的简历包：

```text
original.<ext>
resume.md
resume.raw.json
candidate_draft.json
extraction_report.json
manifest.json
```

将 `resume.md` 作为模型推理的主要来源。仅将 `candidate_draft.json` 用作确定性的提示。当用户要求结构化候选人字段时，使用 `assets/templates/prompts/resume_extract_prompt.md`。

## 候选人上传 (candidate-upload)

运行工作流前先阅读 `references/workflow_candidate_upload.md`。

此工作流将 `resume-ingest` 生成的简历包中的确定性候选人草稿写入腾讯文档智能表格；HR/LLM 审核输出仅用于人工补全，不会被上传脚本自动消费。

### 前置条件

1. 已安装 `tencent-docs` skill。可使用当前运行器支持的 skill registry 安装，例如：

   ```bash
   openclaw skills install tencent-docs
   openclaw skills info tencent-docs
   ```

   如果使用 SkillHub 或其他 registry，也可安装同名 skill。
2. 已安装 `mcporter` CLI
3. 已配置并授权腾讯文档 MCP（参考已安装且已审阅的 `tencent-docs` 技能的 `references/auth.md`）
4. 已完成 `resume-ingest`，拥有简历包目录

### 快速使用

将候选人草稿上传到已有智能表格：

```bash
python3 {baseDir}/scripts/upload_to_smartsheet.py "/path/to/bundle" --file-id "your_file_id" --confirmed-reviewed
```

默认上传到固定候选人库。脚本会先搜索 `HR候选人库`，存在则追加一条记录；不存在才创建：

```bash
python3 {baseDir}/scripts/upload_to_smartsheet.py "/path/to/bundle" --confirmed-reviewed
```

强制创建新的智能表格并上传：

```bash
python3 {baseDir}/scripts/upload_to_smartsheet.py "/path/to/bundle" --create-new --sheet-title "2025届校招-候选人库" --confirmed-reviewed
```

在知识库空间内强制创建：

```bash
python3 {baseDir}/scripts/upload_to_smartsheet.py "/path/to/bundle" --create-new --sheet-title "候选人库" --space-id "your_space_id" --confirmed-reviewed
```

预览模式（不实际写入、默认不联网、默认脱敏）：

```bash
python3 {baseDir}/scripts/upload_to_smartsheet.py "/path/to/bundle" --dry-run
```

预览时也探测腾讯文档目标表：

```bash
python3 {baseDir}/scripts/upload_to_smartsheet.py "/path/to/bundle" --dry-run --probe-remote
```

HR 已确认 `review_required=true` 的草稿记录后再实际上传：

```bash
python3 {baseDir}/scripts/upload_to_smartsheet.py "/path/to/bundle" --file-id "your_file_id" --confirmed-reviewed
```

### 智能表格字段

上传的候选人草稿包含以下字段：

| 字段 | 类型 | 说明 |
|------|------|------|
| 姓名 | 文本 | 候选人姓名 |
| 电话 | 电话 | 联系电话 |
| 邮箱 | 邮件 | 电子邮箱 |
| 当前公司 | 文本 | 当前/最近任职公司 |
| 工作年限 | 数字 | 工作年限 |
| 最高学历 | 文本 | 博士/硕士/本科/大专/高中及以下 |
| 毕业院校 | 文本 | 毕业学校 |
| 专业 | 文本 | 专业名称 |
| 毕业年份 | 数字 | 毕业年份 |
| 技能标签 | 文本 | 技能关键词（顿号分隔） |
| 求职意向 | 文本 | 目标岗位 |
| 招聘阶段 | 文本 | 简历筛选/HR初筛/技术一面/技术二面/HR面/Offer/入职/不合适 |
| 简历来源 | 文本 | 简历文件名 |
| 解析质量 | 文本 | 高保真/回退解析/纯文本 |
| 需HR审核 | 复选框 | 回退解析时自动勾选 |
| 简历包路径 | 文本 | 本地简历包目录路径 |
| 录入时间 | 日期 | 自动填充记录创建时间 |
| 记录ID | 文本 | 唯一标识（姓名+简历 sha256 前缀） |

### 工作流步骤

1. **检查依赖**

   ```bash
   python3 {baseDir}/scripts/dependency_check.py --workflow candidate-upload
   python3 {baseDir}/scripts/dependency_check.py --workflow candidate-upload --probe-remote
   ```

2. **授权排障（外部依赖）**

   仅在腾讯文档授权缺失或需要排障时，运行已安装且已审阅的 `tencent-docs` 技能授权排障命令。不要假设 `tencent-docs` 与本 skill 一定是兄弟目录；优先使用环境变量或 OpenClaw 默认目录定位：

   ```bash
   export TENCENT_DOCS_SKILL_DIR="${TENCENT_DOCS_SKILL_DIR:-$HOME/.openclaw/workspace/skills/tencent-docs}"
   bash "$TENCENT_DOCS_SKILL_DIR/setup.sh" tdoc_check_and_start_auth
   ```

3. **上传候选人草稿**

   ```bash
   python3 {baseDir}/scripts/upload_to_smartsheet.py "/path/to/bundle" --file-id "your_file_id" --confirmed-reviewed
   ```

4. **验证结果**

   打开脚本输出的腾讯文档链接，确认数据是否正确录入。

### 注意事项

- ⚠️ 首次创建智能表格时会自动定义字段并清理默认行列
- ⚠️ 默认必须先搜索固定表名 `HR候选人库`；只有找不到或显式传入 `--create-new` 时才新建候选人库
- ⚠️ 如果搜索到多个同名 `HR候选人库`，脚本会使用搜索结果中的第一个；生产环境建议通过 `--file-id` 指定唯一候选人库
- ⚠️ 已有表格只新增字段，不会修改或删除已有字段
- ⚠️ `tencent-docs` 1.0.33 通过 MCP 新建单选字段可能返回 `22020: Smartsheet invalid select field`，本工作流默认使用文本字段保存枚举值
- ⚠️ 回退解析的候选人会自动标记"需HR审核"
- ⚠️ 如果 `extraction_report.json` 显示 `review_required=true`，脚本会阻止实际上传，直到显式传入 `--confirmed-reviewed`
- ⚠️ `--dry-run` 默认不联网，且默认脱敏；需要检查远程目标时传 `--probe-remote`
- ⚠️ PDF 文本层可能把中文拆成空格，例如 `长 沙 学 院 计 算 机科学与技 术(本科)`；写入前必须归一化并拆分为 `长沙学院`、`计算机科学与技术`、`本科`
- ⚠️ 电话号码按原文写入腾讯文档；终端输出默认脱敏，展示层仍建议脱敏
- ⚠️ 多条候选人可重复调用脚本，记录会追加到表格

## 岗位信息管理 (job-management)

运行工作流前先阅读 `references/workflow_job_management.md`。

此工作流维护固定腾讯文档智能表格 `HR岗位信息库`。字段定义来自 `assets/schemas/recruiting_tables.json`。

### 快速使用

检查依赖：

```bash
python3 {baseDir}/scripts/dependency_check.py --workflow job-management
python3 {baseDir}/scripts/dependency_check.py --workflow job-management --probe-remote
```

初始化或校验岗位表结构：

```bash
python3 {baseDir}/scripts/manage_jobs.py
```

导入真实岗位记录：

```bash
python3 {baseDir}/scripts/manage_jobs.py --records-json "/path/to/jobs.json"
```

指定已有岗位表：

```bash
python3 {baseDir}/scripts/manage_jobs.py --file-id "your_file_id"
```

预览模式：

```bash
python3 {baseDir}/scripts/manage_jobs.py --dry-run
```

### 岗位字段

| 字段 | 说明 |
|------|------|
| job_id | 岗位唯一标识 |
| job_title | 岗位名称 |
| department | 部门 |
| hiring_manager | 用人经理 |
| must_have | 必须条件 |
| nice_to_have | 加分条件 |
| responsibilities | 工作职责 |
| level | 职级 |
| location | 地点 |
| salary_range | 薪资范围 |
| interview_process | 面试流程 |
| status | 开放/暂停/关闭 |
| updated_at | 岗位记录更新时间 |

`status` 当前使用文本字段保存，避免 `tencent-docs` 1.0.33 新建单选字段时触发 `22020` 错误。

## 依赖策略

添加或检查提供方时阅读 `references/dependency_contracts.md`。

第一个工作流需要 `resume.parse` 能力。默认路径优先使用本地文本层解析器，避免意外联网下载模型。Docling 能启动不等于真实 PDF 转换可用；如需验证，请使用 `dependency_check.py --probe-file "/path/to/resume.pdf"`。

腾讯文档工作流的依赖检查默认只做本地检查；需要验证 MCP 连通性和授权时显式加 `--probe-remote`。

处理私人简历时，默认只运行本地脚本。调用 `openclaw agent --local` 可能经过已配置的模型 provider，除非用户明确授权，不要把私人简历交给 agent 端到端处理。

## 输出风格

### resume-ingest 成功时

告知 HR：
- 简历包目录
- 使用的解析器
- 质量等级
- 生成的文件
- 缺失或不明确的字段
- 是否需要 HR 审核
- `extraction_report.json` 中的 `review_reasons`

### resume-ingest 失败时

报告解析器错误；如果已创建 `extraction_report.json`，同时报告其路径。

### candidate-upload 成功时

告知 HR：
- 腾讯文档链接
- 录入的候选人姓名
- SmartSheet file_id 和 record_id
- 解析质量及是否需要审核
- 缺失字段提示

### candidate-upload 失败时

报告具体错误：
- 如果是授权问题，引导完成腾讯文档授权
- 如果是 MCP 调用失败，检查 mcporter 和网络连接
- 如果是数据问题，检查简历包完整性

### job-management 成功时

告知 HR：
- 固定岗位表名
- 腾讯文档链接
- SmartSheet file_id 和 sheet_id
- 新写入岗位数量
- 被跳过的重复 job_id
