---
name: openclaw-ability-export
slug: openclaw-ability-export
version: 1.0.0
homepage: https://clawic.com/skills/openclaw-ability-export
description: >
  能力包导出/导入工具。在聊天中直接打包或接收 agent 配置，支持选择性导入、合并规则与隐私提醒。
  触发场景：
  - 导出："导出能力包"、"打包我的能力"、"export ability"
  - 导入："导入能力包"、"学习能力包"、"import ability"
changelog: |
  1.0.0 - 初始版本，支持 AGENTS.md、SOUL.md、TOOLS.md、IDENTITY.md、MEMORY.md 的导出与选择性导入
metadata:
  clawdbot:
    emoji: "📦"
    requires:
      bins: []
    os: ["linux", "darwin", "win32"]
    configPaths: []
---

# Ability Package - 能力包导出 / 导入工具

在聊天中直接完成 agent 配置的打包分享与接收导入，无需手动文件传输。导出的能力包为纯 Markdown 格式，导入方可预览内容后再决定写入哪些文件。

---

## When to Use

在以下场景使用本 skill：

| 场景 | 操作 |
|------|------|
| 希望与他人分享你的 agent 配置 | 导出能力包 |
| 获得了他人的能力包文件 | 导入能力包 |
| 需要在多个 agent 实例间同步配置 | 导出 + 导入 |
| 备份当前工作环境 | 导出能力包存档 |
| 尝试他人的配置风格 | 导入能力包 |

**触发词：**
- 导出：`导出能力包`、`打包我的能力`、`export ability`
- 导入：`导入能力包`、`学习能力包`、`import ability`

---

## How It Works

### 导出流程

1. **扫描核心文件**：读取 workspace 根目录下的五个核心配置文件
2. **生成 Markdown**：按统一模板拼接为单 `.md` 文件
3. **发送到聊天**：直接发送生成的文档，无需文件上传

**导出的文件列表：**

| 文件 | 说明 |
|------|------|
| `AGENTS.md` | Agent 工作空间规则与约定 |
| `SOUL.md` | Agent 人格与行为准则 |
| `TOOLS.md` | 本地工具配置与笔记 |
| `IDENTITY.md` | Agent 身份标识 |
| `MEMORY.md` | 长期记忆与偏好记录 |

### 导入流程

1. **读取能力包**：获取用户发送的 `.md` 格式文档内容
2. **解析 Section**：识别并切分各配置区块
3. **预览与询问**：展示包含的文件列表，询问用户希望导入哪些
4. **写入文件**：将选中的 section 内容写入 workspace 根目录对应文件
5. **确认完成**：汇报写入结果

**合并规则：**
- 文件不存在时，直接创建
- 文件已存在时，**覆盖写入**（非追加）
- 用户选择哪些，就只写入哪些，未选中的不处理

---

## Examples

### 导出示例

```
用户：导出能力包
Agent：→ 生成 Markdown 格式能力包，直接发送到聊天窗口
```

导出的 Markdown 模板：

```markdown
# 能力包：{名称}
- 版本：1.0
- 导出时间：{时间}
- 来源：{agent 标识}

---

## AGENTS.md
{文件完整内容}

---

## SOUL.md
{文件完整内容}

---

## TOOLS.md
{文件完整内容}

---

## IDENTITY.md
{文件完整内容}

---

## MEMORY.md
{文件完整内容}
```

### 导入交互示例

```
用户：[粘贴能力包文档内容]

Agent：
收到一个能力包，包含以下内容：

📦 能力包概览
- AGENTS.md ✓ (可用)
- SOUL.md ✓ (可用)
- TOOLS.md ✓ (可用)
- IDENTITY.md ✓ (可用)
- MEMORY.md ✓ (可用)

请告诉我想导入哪些？（回复"全部"或具体文件名，如"SOUL.md 和 TOOLS.md"）
```

```
用户：全部

Agent：
正在写入...
✓ AGENTS.md 已更新
✓ SOUL.md 已更新
✓ TOOLS.md 已更新
✓ IDENTITY.md 已更新
✓ MEMORY.md 已更新

导入完成！agent 配置已更新，重启 session 后生效。
```

```
用户：只要 SOUL.md 和 TOOLS.md

Agent：
正在写入...
✓ SOUL.md 已更新
✓ TOOLS.md 已更新

其他文件未变动。
```

---

## Options

### 导出选项

| 选项 | 说明 |
|------|------|
| 默认导出 | 导出全部五个核心文件 |
| 排除 MEMORY.md | 如果用户说"不导 memory"，跳过 MEMORY.md section |

### 导入选项

| 选项 | 说明 |
|------|------|
| `全部` | 导入能力包中所有包含的文件 |
| 部分文件 | 指定要导入的文件名，如 `SOUL.md`、`TOOLS.md 和 IDENTITY.md` |
| 跳过 | 用户选择不导入任何文件 |

---

## Security Considerations

1. **隐私提醒**：导出前应告知用户 `MEMORY.md` 可能包含个人偏好、对话历史等敏感信息，建议用户确认后再分享。

2. **来源审查**：导入前应要求用户提供能力包内容全文，不执行匿名或来源不明的压缩包/脚本。

3. **覆盖风险**：导入会直接覆盖同名已有文件，操作不可逆。应在写入前向用户确认。

4. **范围限制**：本 skill 仅操作 workspace 根目录下的五个核心配置文件，不访问其他目录或敏感系统文件。

5. **传输安全**：能力包以纯 Markdown 文本在聊天中传输，不经过第三方存储或中转。

---

## Related Skills

| Skill | 说明 |
|-------|------|
| `openclaw-ability-export`（本 skill） | 导出/导入 agent 配置包 |
| `memory-setup` | 配置 agent 长期记忆与向量搜索 |
| `self-improving` | 自动从纠正中学习，优化 agent 行为 |
| `find-skills` | 搜索和安装其他 agent skill |
