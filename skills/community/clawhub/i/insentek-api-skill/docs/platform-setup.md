# Platform Setup Guide — 各 Agent 平台配置指南

> 将 insentek skill 安装到不同 Agent 平台的完整步骤，含安装路径、卸载方法和故障排查。

---

## 通用前置：CLI 安装与凭据配置（推荐）

无论使用哪个 Agent 平台，都建议先完成 CLI 安装和本地凭据配置：

```bash
# 安装 skill 到 Claude Code / OpenClaw（交互式）
npx @insentek/openapi-skill

# 配置 API 凭据（加密本地保存，不要在对话中发送 secret）
npx @insentek/openapi-skill login

# 查看连接状态
npx @insentek/openapi-skill auth status
```

凭据保存在 `~/.config/insentek/credentials.json`。Agent 通过 `scripts/insentek_cli.py` 自动读取，**不会**在对话中索要 appid/secret。

---

## 目录

- [OpenClaw](#openclaw)
- [Claude Code](#claude-code)
- [ChatGPT](#chatgpt)
- [Hermes-Agent](#hermes-agent)
- [平台兼容性速查](#平台兼容性速查)
- [故障排查](#故障排查)

---

## OpenClaw

### 安装

#### 方式一：CLI 安装（推荐）

```bash
npx @insentek/openapi-skill install -r openclaw -s global -y
npx @insentek/openapi-skill login
```

#### 方式二：从 ClawHub 安装

```bash
# 安装最新版本（slug 见 .github/workflows/publish.yml）
clawhub skill install insentek-api-skill

# 安装指定版本
clawhub skill install insentek-api-skill@1.2.2

# 从 ClawHub 搜索确认
clawhub skill search insentek
```

安装完成后，skill 会自动注册到 OpenClaw 的技能列表中。

> 注意：ClawHub 上的 slug 是 `insentek-api-skill`，但 skill 本身的 id（`skill.json` / SKILL.md frontmatter 中的 `name`）始终是 `insentek-openapi`。两者均合法，只是用途不同。

#### 方式三：本地文件安装

```bash
# 从本地 SKILL.md 安装
clawhub skill add ./SKILL.md

# 或使用绝对路径
clawhub skill add /path/to/SKILL.md
```

#### 方式四：Web UI 安装

1. 打开 OpenClaw 客户端，进入 **Skills** 页面
2. 点击 **Import Skill** → 选择文件
3. 选择项目根目录的 `SKILL.md` 文件
4. 确认导入

### 卸载

```bash
# CLI 卸载（npm 包安装方式）
npx @insentek/openapi-skill uninstall -r openclaw -s workspace -y
# 或 ClawHub 安装方式
clawhub skill remove insentek-api-skill
```

或在 Web UI 中：Skills → 找到 "insentek-api-skill" → **Remove**。

### 配置参数

| 参数 | 值 | 说明 |
|------|-----|------|
| API Base URL | `https://openapi.ecois.info` | 默认即可 |

### 首次使用

先在本机配置 API 凭据：

```bash
npx @insentek/openapi-skill login
```

然后在 OpenClaw 中直接查询：

```
User: 查看所有设备
```

---

## Claude Code

### 安装

Claude Code 通过读取 skill 文件来加载技能上下文，支持项目级和全局级两种方式。

#### 方式一：CLI 安装（推荐）

```bash
npx @insentek/openapi-skill install -r claude -s global -y
npx @insentek/openapi-skill login
```

#### 方式二：全局 Skills 目录（手动）

Claude Code 会从全局 skills 目录自动加载所有 skill 文件，无需在每个项目中重复放置。

**Windows:**
```powershell
# 创建 skills 目录（如果不存在）
New-Item -ItemType Directory -Force -Path "$env:USERPROFILE\.claude\skills"

# 复制 skill 文件
Copy-Item skill.md "$env:USERPROFILE\.claude\skills\insentek-api-skill.md"
```

**macOS:**
```bash
mkdir -p ~/.claude/skills
cp skill.md ~/.claude/skills/insentek-api-skill.md
```

**Linux:**
```bash
mkdir -p ~/.claude/skills
cp skill.md ~/.claude/skills/insentek-api-skill.md
```

放置后重启 Claude Code 或重新打开对话即可生效。

#### 方式三：项目目录加载

将 `skill.md` 放入当前工作项目的根目录，Claude Code 会自动识别为项目上下文：

```bash
# 任意项目目录
cp skill.md ./skill.md
```

#### 方式四：对话中直接引用

```
# 在 Claude Code 对话中执行
/load skill.md
```

或直接将 `skill.md` 内容粘贴到对话中。

### 卸载

- **全局级（推荐）**：从 `~/.claude/skills/` 目录移除对应文件
  ```bash
  # Windows
  Remove-Item "$env:USERPROFILE\.claude\skills\insentek-api-skill.md"

  # macOS / Linux
  rm ~/.claude/skills/insentek-api-skill.md
  ```
- **项目级**：删除项目根目录的 `skill.md` 文件
- **对话级**：执行 `/clear` 清除当前对话上下文

### 首次使用

```bash
npx @insentek/openapi-skill login
```

```
User: 查看所有设备
```

Claude Code 会读取 skill.md 中的 tool definitions，脚本自动使用本地凭据。

### 注意事项

- 确保 skill.md 中的 YAML frontmatter 被正确解析
- 如果 function calling 未触发，尝试明确说出工具名称如 "query_device"

---

## ChatGPT

### 安装

#### 方式一：创建 GPT（推荐，需 Plus 订阅）

1. 打开 [ChatGPT](https://chat.openai.com) → **Explore GPTs** → **Create**
2. 在 Configure 标签页：
   - **Name**: Insentek Device Query
   - **Description**: 查询 insentek 物联网设备数据
   - **Instructions**: 粘贴 `skill.md` 的完整内容
3. 在 **Capabilities** 中启用 "Code Interpreter"（如需数据处理）
4. 保存并发布（可选设为 Private）

#### 方式二：Actions（API 直连，需 Plus 订阅）

1. 创建 GPT 时，在 Configure 页面点击 **Add actions**
2. 粘贴由 `skill.md` function schema 生成的 OpenAPI schema
3. 设置认证方式：API Key（Header: `Authorization`）— **不要将 appid/secret 写入 GPT 配置或对话**
4. 在本机运行 `npx @insentek/openapi-skill login`，由脚本管理 token
5. 保存后 GPT 可直接调用 insentek API

#### 方式三：Custom Instructions（个人使用）

适合临时使用，无需创建 GPT。

1. 打开 ChatGPT → 点击头像 → **Custom Instructions**
2. 在 "How would you like ChatGPT to respond?" 中粘贴 `skill.md` 的 Prompt 区内容
3. 在 "What would you like ChatGPT to know about you?" 中说明你有 insentek 物联网设备即可（**不要**写入 appid/secret）
4. 在本机运行 `npx @insentek/openapi-skill login` 配置凭据
5. 保存后开始新对话

**限制：** Custom Instructions 不支持真正的 function calling，API 调用需要手动复制 URL。

### 卸载

- **GPTs 方式**：ChatGPT → Explore GPTs → 找到对应 GPT → 右上角 ⋮ → **Delete GPT**
- **Actions 方式**：编辑 GPT → Configure → Actions → **删除对应 Action**
- **Custom Instructions**：ChatGPT → 头像 → Custom Instructions → **清空内容**

### 首次使用

```
User: 查看我的所有设备
```

如果已在本地运行 `npx @insentek/openapi-skill login`，脚本会自动认证并查询。

---

## Hermes-Agent

### 安装

Hermes-Agent 通过读取 skills 目录下的 skill 文件来加载技能。

#### 步骤

**Windows:**
```powershell
# 创建 skills 目录（如果不存在）
New-Item -ItemType Directory -Force -Path "$env:USERPROFILE\.hermes\skills"

# 复制 skill 文件
Copy-Item skill.md "$env:USERPROFILE\.hermes\skills\insentek-api-skill.md"
```

**macOS:**
```bash
mkdir -p ~/.hermes/skills
cp skill.md ~/.hermes/skills/insentek-api-skill.md
```

**Linux:**
```bash
mkdir -p ~/.hermes/skills
cp skill.md ~/.hermes/skills/insentek-api-skill.md
```

**重启或刷新：**
```bash
hermes skill reload
# 或重启 Hermes-Agent 服务
```

### 卸载

**Windows:**
```powershell
Remove-Item "$env:USERPROFILE\.hermes\skills\insentek-api-skill.md"
```

**macOS / Linux:**
```bash
rm ~/.hermes/skills/insentek-api-skill.md
hermes skill reload
```

### 配置环境变量（可选）

```bash
export INSENTEK_API_BASE=https://openapi.ecois.info
```

### 首次使用

```bash
npx @insentek/openapi-skill login
```

```
User: 查看设备
```

---

## 平台兼容性速查

| 特性 | OpenClaw | Claude Code | ChatGPT (GPTs) | Hermes-Agent |
|------|----------|-------------|----------------|--------------|
| Function Schema | Native | Native | Via Actions | Native |
| YAML Frontmatter | ✅ | ✅ | ⚠️ | ✅ |
| Auto Token Refresh | ✅ | ✅ | Manual | ✅ |
| Alias Resolution | ✅ | ✅ | ✅ | ✅ |
| Time Parsing | ✅ | ✅ | ✅ | ✅ |
| Chain Calling | ✅ | ✅ | ✅ | ✅ |
| CLI 凭据管理 | ✅ | ✅ | ⚠️ 需本机 login | ✅ |
| ClawHub 一键安装 | ✅ | ❌ | ❌ | ❌ |

**图例：** ✅ 原生支持 | ⚠️ 需额外配置 | ❌ 不支持

---

## 故障排查

### Function Schema 未被识别

- **Claude Code**: 确保 skill.md 位于项目根目录，且文件名为 `skill.md`
- **ChatGPT**: 使用 GPTs 的 Actions 功能，或手动粘贴 Instructions
- **通用**: 检查 YAML frontmatter 格式是否正确（`---` 开头和结尾）

### 认证失败

1. 运行 `npx @insentek/openapi-skill auth status` 检查连接状态
2. 重新配置：`npx @insentek/openapi-skill login`
3. 检查网络是否能访问 `https://openapi.ecois.info`
4. **不要在对话中发送 secret**，凭据仅通过 CLI 配置

### 查询无数据返回

1. 确认设备已正确接入 insentek 平台
2. 检查时间范围是否合理（默认最近 24 小时可能无数据）
3. 尝试扩大时间范围如 "最近7天"

---

*配置问题请联系：参考 insentek 官方支持渠道*
