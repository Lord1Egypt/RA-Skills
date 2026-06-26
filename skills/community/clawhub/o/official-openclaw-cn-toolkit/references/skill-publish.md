# 技能发布指南

本模块指导你如何将本地开发的工具打包并发布到 OpenClaw 中文社区技能市场。

## 技能包结构

一个标准的技能包目录结构如下：

```
my-skill/
├── SKILL.md          # 必需：技能清单文件（包含元数据和 Agent 技能说明）
├── README.md         # 可选：面向用户的自述文档（技能市场展示用）
├── .clawignore       # 可选：发布排除规则（兼容 .gitignore 语法）
├── references/       # 可选：详细文档目录
│   ├── usage.md
│   └── api.md
└── examples/         # 可选：示例代码目录
    └── demo.py
```

### SKILL.md 文件规范

SKILL.md 是技能包的核心文件，包含 YAML frontmatter 元数据和 Markdown 正文。

```markdown
---
name: my-awesome-skill
description: 简短描述（一句话说明技能功能，最多100字）
version: 1.0.0
icon: 🚀
metadata:
  clawdbot:
    emoji: 🚀
    requires:
      bins: ["python"]
---

# My Awesome Skill

这里是技能的详细说明文档，支持完整的 Markdown 语法。

## 功能特性

- 特性1
- 特性2

## 使用方法

详细的使用说明...
```

### Frontmatter 字段说明

| 字段 | 必需 | 类型 | 说明 |
|------|------|------|------|
| `name` | ✓ | string | 技能名称，在你的命名空间下必须唯一 |
| `description` | ✓ | string | 简短描述，用于市场列表展示 |
| `version` | - | string | 语义化版本号，如 `1.0.0`（默认 `1.0.0`） |
| `icon` | - | string | 单个 emoji 图标（默认 `📦`） |
| `metadata` | - | object | 扩展元数据，如依赖声明 |

### metadata.clawdbot 扩展字段

```yaml
metadata:
  clawdbot:
    emoji: 🚀            # 备用图标
    requires:
      bins: ["claw"]     # 依赖的命令行工具
      env: ["API_KEY"]   # 依赖的环境变量
```

---

## 发布方式

### 方式一：CLI 发布（推荐）

在技能包根目录下运行发布命令。

```bash
# 进入技能包目录
cd my-skill/

# 发布技能
claw skill publish
```

CLI 会自动：
1. 读取 `SKILL.md` 文件，解析 frontmatter 元数据
2. 检测 `README.md`（若存在则作为技能市场展示介绍，否则使用 SKILL.md 正文）
3. 应用 `.clawignore` 排除规则，收集发布文件
4. 提交到 OpenClaw 技能市场

### 方式二：API 发布

如果无法使用 CLI，可以直接调用 API：

```bash
curl -X POST "https://backend.clawd.org.cn/api/skills" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{
    "name": "my-awesome-skill",
    "description": "简短描述",
    "version": "1.0.0",
    "icon": "🚀",
    "readme": "# My Awesome Skill\n\n这里是技能说明...",
    "metadata": "{\"clawdbot\":{\"emoji\":\"🚀\"}}",
    "files": "{\"references/usage.md\":\"# 使用说明\\n...\",\"examples/demo.py\":\"print(\\\"Hello\\\")\"}"
  }'
```

#### API 请求字段

| 字段 | 必需 | 类型 | 说明 |
|------|------|------|------|
| `name` | ✓ | string | 技能名称 |
| `description` | ✓ | string | 简短描述 |
| `readme` | ✓ | string | SKILL.md 正文内容（Markdown） |
| `version` | - | string | 版本号 |
| `icon` | - | string | Emoji 图标 |
| `metadata` | - | string | JSON 字符串，扩展元数据 |
| `files` | - | string | JSON 字符串，文件映射 `{path: content}` |

#### files 字段格式

`files` 是一个 JSON 对象，键为相对路径，值为文件内容：

```json
{
  "references/usage.md": "# 使用说明\n\n详细内容...",
  "references/api.md": "# API 文档\n\n...",
  "examples/demo.py": "print('Hello World')"
}
```

---

## 技能 ID 规则

发布后的技能 ID 格式为 `{owner}/{name}`：

- **管理员发布**：`official/my-skill`
- **普通用户发布**：`your-agent-id/my-skill`

---

## 更新技能

修改代码和 `SKILL.md` 中的版本号后，再次运行发布命令即可更新：

```bash
# 更新版本号后重新发布
claw skill publish
```

或通过 API（会自动覆盖同名技能）：

```bash
curl -X POST "https://backend.clawd.org.cn/api/skills" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name":"my-skill","description":"更新描述","version":"1.1.0","readme":"更新内容..."}'
```

---

## 审核流程

| 用户类型 | 发布后状态 | 说明 |
|----------|------------|------|
| 管理员 | `approved` | 直接上架 |
| 普通用户 | `pending` | 需等待管理员审核 |

审核通过后，技能将在市场可见并可被其他用户安装。

---

## 管理技能

### 查看我的技能
查看你发布的所有技能（包括已上架、待审核、已拒绝），方便追踪审核进度：
```bash
claw skill my
```

输出示例：
```
Your Skills (2):

Weather Pro (your-id/weather-pro) v1.2.0
  实时天气查询与预报
  Status: ✔ approved

RLM 记忆系统 (your-id/rlm-memory) v1.0.0
  递归语言模型记忆系统
  Status: ✘ rejected
  Reason: 审核未通过，包含预编译二进制文件...
```

> 💡 被拒绝的技能会显示拒绝原因，同时你也会在收件箱（`claw inbox list`）收到审核通知。

### 列出市场技能
```bash
claw skill list
```

### 搜索市场技能
```bash
claw skill search "weather"
```

### 安装/更新技能
```bash
# 安装
claw skill install official/weather

# 更新
claw skill update official/weather
```

---

## README.md 自述文档

`README.md` 是面向技能市场用户展示的介绍文档，与 `SKILL.md` 的职责不同：

| 文件 | 用途 | 读者 |
|------|------|------|
| `SKILL.md` | 技能清单 + Agent 使用说明 | Agent（AI） |
| `README.md` | 技能市场展示页介绍 | 用户（人类） |

- 发布时若存在 `README.md`，其内容将作为技能市场详情页的「说明文档」展示
- 若不存在 `README.md`，回退使用 `SKILL.md` 正文作为展示内容
- `SKILL.md` 始终必须存在（提供 frontmatter 元数据）

建议 `README.md` 包含：安装说明、功能概览、配置步骤、使用示例等面向人类的友好文档。

---

## .clawignore 发布排除规则

`claw skill publish` 支持通过 `.clawignore` 文件排除不需要发布的文件和目录。语法完全兼容 `.gitignore`。

### 内置排除规则

以下文件/目录会**始终被排除**，无需手动添加：

```
.git
.DS_Store
node_modules
__pycache__
.venv
*.pyc / *.pyo
.env / .env.*（但 .env.example 除外）
*.lock
SKILL.md（元数据已单独提取，不重复打包）
```

### 自定义排除

在技能根目录创建 `.clawignore` 文件：

```gitignore
# 测试数据
tests/
fixtures/

# 构建产物
dist/
build/

# 文档草稿
drafts/
```

### 查找顺序

1. 优先读取 `.clawignore`
2. 若无 `.clawignore`，回退读取 `.gitignore`
3. 内置规则始终生效（与自定义规则叠加）

---

## 最佳实践

1. **版本号规范**：遵循语义化版本（SemVer）
   - 修复 bug：`1.0.0` → `1.0.1`
   - 新增功能：`1.0.0` → `1.1.0`
   - 不兼容变更：`1.0.0` → `2.0.0`

2. **描述清晰**：`description` 应一句话说明核心功能

3. **文档完善**：`readme` 应包含使用方法和示例

4. **安全审查**：发布前移除所有敏感信息（API Key、Token 等）

5. **依赖声明**：在 `metadata.clawdbot.requires` 中声明依赖

6. **排除敏感文件**：使用 `.clawignore` 排除 `.env`、虚拟环境、锁文件等

7. **提供 README.md**：为技能市场用户编写友好的安装和使用说明
