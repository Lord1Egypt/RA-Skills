# SKILL.md 文件规范

本文档详细说明 LegionClaw 技能文件 `SKILL.md` 的格式规范和编写要求。

## 一、Frontmatter 规范

SKILL.md 必须以 YAML frontmatter 开头，包含以下字段：

```yaml
---
name: <skill-name>
version: <semver>
description: <描述>
disable-model-invocation: <true|false>
---
```

### 字段说明

| 字段 | 必填 | 格式 | 说明 |
|------|------|------|------|
| `name` | 是 | kebab-case | 技能唯一标识，必须与目录名一致 |
| `version` | 是 | semver | 语义化版本号，如 `1.0.0` |
| `description` | 是 | 字符串 | 一句话说明技能用途和触发场景 |
| `disable-model-invocation` | 否 | boolean | 是否禁用模型调用，默认 `false` |

### name 命名规则

- 只能包含小写字母、数字、连字符
- 必须以字母开头
- 不能以连字符开头或结尾
- 不能包含连续连字符
- 示例：`my-skill-name`、`fetch-legionclaw-invite-code`

### version 语义化版本

遵循 `MAJOR.MINOR.PATCH` 格式：

- `MAJOR`：不兼容的 API 变更
- `MINOR`：向后兼容的功能新增
- `PATCH`：向后兼容的问题修复

### description 编写要点

- 一句话说明技能用途
- 包含触发关键词，便于用户识别
- 长度建议 20-100 字

示例：

```yaml
description: 在 LegionClaw 中为用户创建智能会议。
description: 在 LegionClaw 里帮用户向通付盾申请 LegionClaw 使用权限的邀请码。
```

## 二、章节结构规范

SKILL.md 正文应包含以下核心章节（按顺序）：

### 1. 标题（必需）

```markdown
# <技能标题>
```

标题应简明扼要，体现技能核心功能。

### 2. 何时使用（必需）

说明技能的触发条件和常见说法：

```markdown
## 何时使用

- **技能名**：用户点名 `<skill-name>`，或需要**<核心功能>**。
- **常见说法**（不限于此）：<说法1>、<说法2>、<说法3>...
- **运行前提**：<如有特殊要求，说明运行环境要求>
```

**编写要点**：

- 技能名：说明用户如何点名调用
- 常见说法：列举 3-5 个用户可能的表述方式
- 运行前提：如有特殊环境要求（如 LegionClaw 内执行），需明确说明

### 3. 目标（必需）

说明技能要完成的任务：

```markdown
## 目标

<简明描述技能要完成的核心任务>
```

**编写要点**：

- 一段话概括技能目标
- 如涉及多个子任务，可用编号列表
- 说明关键输入/输出

### 4. 执行步骤（必需）

详细说明操作流程：

```markdown
## 执行步骤

1. <步骤1>
2. <步骤2>
3. <步骤3>
```

**编写要点**：

- 步骤编号清晰
- 包含可执行的代码/命令示例
- 代码块使用正确的语言标记（如 `bash`、`json`）
- 变量使用占位符并说明替换规则

示例：

```markdown
## 执行步骤

1. 获取会话标识串，解析出 `userId`。

2. 执行以下命令：

```bash
curl -sS -X POST "https://example.com/api" \
  -H "Content-Type: application/json" \
  -d '{"userId":"${USER_ID}"}'
```

3. 根据响应结果处理：
   - 成功：输出结果
   - 失败：提示错误
```

### 5. 错误处理（必需）

说明各种异常情况的处理方式：

```markdown
## 错误处理

- **<错误类型1>**：<处理方式>
- **<错误类型2>**：<处理方式>
- **<错误类型3>**：<处理方式>
```

**编写要点**：

- 列举常见错误场景
- 说明每种错误的处理方式
- 对用户友好的错误提示

### 6. 其他章节（可选）

根据需要添加：

- **接口说明**：如涉及 API 调用
- **配置项**：如有可配置参数
- **变更接口时**：说明接口变更时的更新要求
- **安全要求**：如有安全相关的注意事项

## 三、代码示例规范

### 1. Bash 命令

```bash
# 使用变量替换
USER_ID="abc123"
curl -sS -X POST "https://example.com/api?userId=${USER_ID}"
```

### 2. JSON 示例

```json
{
  "code": "000000",
  "message": "成功",
  "data": {
    "field1": "value1",
    "field2": "value2"
  }
}
```

### 3. 表格格式

使用 Markdown 表格说明字段：

```markdown
| 字段 | 含义 |
|------|------|
| `code` | 业务状态码 |
| `message` | 提示信息 |
| `data.field1` | 数据字段1 |
```

## 四、命名规范

### 1. 技能名称（name）

- kebab-case：`my-skill-name`
- 与目录名一致：`skills/my-skill-name/`

### 2. 章节标题

- 使用中文
- 层级清晰：`##` 为主章节，`###` 为子章节
- 简明扼要

### 3. 变量名

- 代码中使用大写下划线：`USER_ID`、`API_KEY`
- 说明中使用反引号包裹：`` `userId` ``

## 五、目录结构规范

```
skills/<skill-name>/
├── SKILL.md              # 必需：技能主文件
├── references/           # 可选：按需加载的参考文档
│   ├── spec.md
│   └── api-doc.md
├── scripts/              # 可选：可执行脚本
│   ├── script1.py
│   └── script2.sh
└── assets/               # 可选：输出用模板/资源（不加载进上下文）
    ├── template.pptx
    └── boilerplate/
```

### 何时使用 references/

- SKILL.md 内容较多（超过 200 行或接近 500 行）
- 需要引用详细规范文档、API 文档、数据库 schema
- 内容仅在某些场景下才需要（条件性加载）
- 同一信息不要同时在 SKILL.md 和 references 中重复

**最佳实践**：references 保持一层深度，全部从 SKILL.md 直接链接；超过 100 行的 reference 文件建议在顶部加目录。

### 何时使用 scripts/

- 相同代码会被反复重写
- 需要确定性、可重复执行的逻辑
- 需要执行 Python/Shell 数据处理或文件生成

脚本可直接执行而无需读入上下文，但大模型仍可能需要阅读脚本以做环境适配。

### 何时使用 assets/

- 技能输出需要模板文件（PPT、DOCX、HTML 脚手架）
- 需要图片、图标、字体等品牌资源
- 文件用于最终输出而非指导大模型思考

assets 不加载进上下文，大模型在产出结果时直接引用路径。

### 禁止创建的文件

不要创建 `README.md`、`CHANGELOG.md`、`INSTALLATION_GUIDE.md` 等与技能执行无关的辅助文档。

## 五（附）、渐进式披露模式

### 模式 1：高层指南 + references 链接

```markdown
## 执行步骤

1. 基础操作：[代码示例]
2. 高级功能：
   - **表单填充**：见 [forms.md](references/forms.md)
   - **API 详情**：见 [api-doc.md](references/api-doc.md)
```

### 模式 2：按领域/变体拆分

多框架或多场景时，SKILL.md 保留选择与导航，细节放 references：

```
my-skill/
├── SKILL.md
└── references/
    ├── aws.md
    └── gcp.md
```

### 模式 3：条件性详情

```markdown
## 执行步骤

基础编辑直接修改 XML。

**需要修订追踪时**：见 [redlining.md](references/redlining.md)
```

## 六、编写检查清单

创建或修改技能后，检查以下项目：

### Frontmatter

- [ ] `name` 为 kebab-case，与目录名一致
- [ ] `version` 为语义化版本格式
- [ ] `description` 简明扼要，包含触发关键词
- [ ] `disable-model-invocation` 设置正确（如需要）

### 章节结构

- [ ] 包含「何时使用」章节
- [ ] 包含「目标」章节
- [ ] 包含「执行步骤」章节
- [ ] 包含「错误处理」章节
- [ ] 章节顺序正确

### 内容质量

- [ ] 常见说法列举 3-5 个
- [ ] 执行步骤包含可执行代码示例
- [ ] 错误处理覆盖主要异常场景
- [ ] 代码示例可直接执行（变量替换后）

### 格式规范

- [ ] 代码块使用正确的语言标记
- [ ] 变量使用反引号或代码块包裹
- [ ] 表格格式正确
- [ ] 已运行 `validate_skill.py` 校验通过
- [ ] 无 README/CHANGELOG 等辅助文档

## 七、示例模板

### 简单技能模板

```markdown
---
name: my-simple-skill
version: 1.0.0
description: 简短描述技能用途。
disable-model-invocation: false
---

# 技能标题

## 何时使用

- **技能名**：用户点名 `my-simple-skill`，或需要**<核心功能>**。
- **常见说法**（不限于此）：说法1、说法2、说法3。

## 目标

<一句话说明技能目标>

## 执行步骤

1. <步骤1>
2. <步骤2>
3. <步骤3>

## 错误处理

- **<错误类型>**：<处理方式>
```

### API 调用技能模板

```markdown
---
name: my-api-skill
version: 1.0.0
description: 调用 API 完成特定任务。
disable-model-invocation: false
---

# API 技能标题

## 何时使用

- **技能名**：用户点名 `my-api-skill`，或需要**<核心功能>**。
- **常见说法**（不限于此）：说法1、说法2、说法3。
- **运行前提**：<运行环境要求>

## 目标

<说明要调用的 API 和完成的任务>

## 接口

- **URL**: `<API 地址>`
- **方法**: `POST`
- **Content-Type**: `application/json`
- **请求体**:

```json
{
  "field1": "<值1>",
  "field2": "<值2>"
}
```

### 成功响应

```json
{
  "code": "000000",
  "message": "成功",
  "data": {
    "result": "<结果>"
  }
}
```

## 执行步骤

1. 准备请求参数。
2. 执行以下命令：

```bash
curl -sS -X POST "<API_URL>" \
  -H "Content-Type: application/json" \
  -d '{"field1":"value1","field2":"value2"}'
```

3. 根据响应结果处理：
   - 成功（`code == "000000"`）：输出结果
   - 失败：提示错误

## 错误处理

- **连接失败**：提示检查网络
- **业务失败**：根据 `message` 提示错误
- **格式错误**：提示参数格式问题
```

## 八、常见问题

### Q: name 可以修改吗？

A: 不可以。`name` 是技能的唯一标识，一旦创建不可修改。如需改名，需创建新技能。

### Q: version 什么时候更新？

A: 
- 修改技能功能时更新 `MAJOR` 或 `MINOR`
- 修复问题时更新 `PATCH`
- 仅修改文档时可不更新版本号

### Q: 什么时候使用 references/？

A: 当 SKILL.md 内容较多（超过 200 行），或需要引用详细规范、API 文档时，使用 references/ 子目录。

### Q: 什么时候使用 scripts/？

A: 当技能需要执行 Python/Shell 脚本完成复杂逻辑时，使用 scripts/ 子目录。

### Q: 什么时候使用 assets/？

A: 当技能输出需要模板文件（PPT、HTML 脚手架）、图片、字体等资源，且这些文件用于最终输出而非指导大模型思考时，使用 assets/ 子目录。

### Q: description 写多长合适？

A: 一句话说明用途，长度建议 20-100 字，包含触发关键词。
