# 依赖契约

此技能依赖能力，而不是特定供应商。只要行为符合契约，能力可以由 CLI、Python 包、MCP 服务器或另一个技能提供。

## 目录

- OpenClaw 打包说明
- resume.parse
- resume.parse_high_fidelity
- fallback.pdf_text
- fallback.docx_text
- tencent_docs.upsert_record
- 路线图依赖

## OpenClaw 打包说明

即使未安装 Docling、mcporter 或 tencent-docs，也要保持此技能可加载，因为 `resume-ingest` 仍可只用本地解析器运行。`metadata.openclaw.requires.bins` 只声明所有脚本都需要的 `python3`；腾讯文档授权变量写在 `metadata.openclaw.envVars`，腾讯文档和高保真解析依赖作为可选依赖写在本参考文档中。

当前项目开发时可放在仓库内的 `skills/hr-recruiting-tracker`。OpenClaw 的默认工作区通常位于 `~/.openclaw/workspace/skills`，可将技能目录复制或安装到该位置让 `openclaw skills info hr-recruiting-tracker` 发现它；不要把这个路径写死为唯一部署路径。

其他技能依赖也要按“可安装、可定位、可验证”的方式声明。不要只写“依赖 tencent-docs”，还要说明安装命令、授权排障、MCP 健康检查和替代定位方式。

当需要 PDF、DOCX、图像、OCR 或版式感知提取时，在 OpenClaw 主机或沙盒环境中安装 Docling。常见安装方式包括 `pipx install docling`、`uv tool install docling-slim --with docling`，或将 Docling 添加到 agent 沙盒镜像。

默认处理私人简历时只运行本地脚本。调用 `openclaw agent --local` 可能会把简历内容发送到已配置的模型 provider；只有在用户明确授权后才允许这样做。

---

## resume.parse

`resume-ingest` 工作流必需。

输入：
- 本地简历文件路径
- 可选输出目录

输出：
- `resume.md`
- `resume.raw.json`
- `candidate_draft.json`
- `extraction_report.json`

首选提供方：
- Docling Python 包
- Docling CLI

回退提供方：
- PyMuPDF
- pypdf 或 PyPDF2
- pdftotext
- python-docx

健康检查：

```bash
python3 {baseDir}/scripts/dependency_check.py --workflow resume-ingest
python3 {baseDir}/scripts/dependency_check.py --workflow resume-ingest --probe-file "/path/to/resume.pdf"
```

## resume.parse_high_fidelity

建议用于扫描版简历、复杂版式、表格和中英混合简历。

提供方：
- Docling

备注：
- Docling CLI 能启动不代表真实 PDF 转换可用；`docling.pdf_conversion` 只有真实文件探测成功后才视为可用。
- 默认 `resume_extract.py` 不主动使用 Docling，避免意外触发 HuggingFace、ModelScope 或其他模型下载。
- 如果 Docling 不可用，回退文本提取在带文本层的 PDF 上仍可能成功。
- 在写入任何数据库之前，必须将回退输出标记为需要 HR 审核。

## fallback.pdf_text

PDF 文本层解析能力。

提供方：
- pypdf 或 PyPDF2
- PyMuPDF
- pdftotext

默认 PDF 解析顺序：

```text
pypdf/PyPDF2 → PyMuPDF → pdftotext
```

输出质量必须标记为 `fallback`。

## fallback.docx_text

DOCX 文本解析能力。

提供方：
- python-docx

输出质量必须标记为 `fallback`。

---

## ✅ tencent_docs.upsert_record

`candidate-upload` 和 `job-management` 工作流使用。**已实现。**

将确定性候选人草稿写入腾讯文档智能表格。HR/LLM 审核输出仅供人工补全，不会被上传脚本自动消费。

提供方：
- 腾讯文档 MCP（`tencent-docs` 技能）
- 通过 `mcporter` CLI 调用

前置条件：
- 已安装 `tencent-docs` skill
- 已安装 `mcporter`（`npm install -g mcporter`）
- 已配置并授权腾讯文档 MCP

OpenClaw 常用安装：

```bash
openclaw skills install tencent-docs
openclaw skills info tencent-docs
```

如果使用 SkillHub、ClawHub 或其他 registry，也可安装同名 skill。安装后定位顺序：

1. `TENCENT_DOCS_SKILL_DIR`
2. 与本 skill 同一 skills 根目录下的 `tencent-docs`
3. `$HOME/.openclaw/workspace/skills/tencent-docs`

授权排障：

仅在需要检查腾讯文档授权时，运行已安装且已审阅的 `tencent-docs` skill 中的脚本。

```bash
export TENCENT_DOCS_SKILL_DIR="${TENCENT_DOCS_SKILL_DIR:-$HOME/.openclaw/workspace/skills/tencent-docs}"
bash "$TENCENT_DOCS_SKILL_DIR/setup.sh" tdoc_check_and_start_auth
```

如果返回 `AUTH_REQUIRED:<url>`，必须把链接给用户，等待用户明确回复已完成授权后再运行：

```bash
bash "$TENCENT_DOCS_SKILL_DIR/setup.sh" tdoc_fetch_token
```

智能表格结构：

表模型统一维护在：

```text
assets/schemas/recruiting_tables.json
```

### candidates 表

| 字段 | 类型 | 来源 |
|------|------|------|
| 姓名 | 文本 | `candidate_draft.json` → identity.name |
| 电话 | 电话 | `candidate_draft.json` → identity.phone |
| 邮箱 | 邮件 | `candidate_draft.json` → identity.email |
| 当前公司 | 文本 | `candidate_draft.json` → profile.current_company |
| 工作年限 | 数字 | `candidate_draft.json` → profile.years_of_experience |
| 最高学历 | 文本 | 从 profile.education_evidence 推断 |
| 毕业院校 | 文本 | 从 profile.education_evidence 推断 |
| 专业 | 文本 | 从 profile.education_evidence 推断 |
| 毕业年份 | 数字 | 从 profile.education_evidence 推断 |
| 技能标签 | 文本 | `candidate_draft.json` → profile.skill_mentions |
| 求职意向 | 文本 | 待 LLM 提取 |
| 招聘阶段 | 文本 | 默认"简历筛选" |
| 简历来源 | 文本 | `candidate_draft.json` → source.file_name |
| 解析质量 | 文本 | `extraction_report.json` → quality |
| 需HR审核 | 复选框 | `extraction_report.json` → review_required |
| 简历包路径 | 文本 | 本地 bundle 路径 |
| 录入时间 | 日期 | 自动填充 |
| 记录ID | 文本 | 唯一标识 |

固定智能表格名：`HR候选人库`

### jobs 表

固定智能表格名：`HR岗位信息库`

| 字段 | 类型 | 来源 |
|------|------|------|
| job_id | 文本 | 岗位唯一标识 |
| job_title | 文本 | 岗位名称 |
| department | 文本 | 部门 |
| hiring_manager | 文本 | 用人经理 |
| must_have | 文本 | 必须条件 |
| nice_to_have | 文本 | 加分条件 |
| responsibilities | 文本 | 工作职责 |
| level | 文本 | 职级 |
| location | 文本 | 地点 |
| salary_range | 文本 | 薪资范围 |
| interview_process | 文本 | 面试流程 |
| status | 文本 | 开放/暂停/关闭 |
| updated_at | 日期 | 自动填充 |

实测限制：

- `tencent-docs` 1.0.33 新建 `singleSelect/select` 字段时可能返回 `22020: Smartsheet invalid select field`。当前实现默认使用文本字段保存枚举值，以保证候选人记录可写入。
- `file://` 本地路径不适合作为腾讯文档云端超链接，当前实现保存为文本。
- 教育字段必须先归一化 PDF 空格并拆分；`毕业院校` 不得写入包含专业、学历或日期的整段教育经历。

健康检查：

```bash
python3 {baseDir}/scripts/dependency_check.py --workflow candidate-upload
python3 {baseDir}/scripts/dependency_check.py --workflow candidate-upload --probe-remote
python3 {baseDir}/scripts/dependency_check.py --workflow job-management
python3 {baseDir}/scripts/dependency_check.py --workflow job-management --probe-remote
mcporter call "tencent-docs" "smartsheet.list_tables" --args '{"file_id":"your_file_id"}'
```

---

## 路线图依赖

候选人库搜索、招聘事件追加、消息通知、面试日程等路线图能力尚未实现，也不属于当前发布版依赖契约。仅当对应工作流实现、测试和安全门完成后，再在本文件新增具体契约。
