# openclaw-ability-export

在聊天中直接将 OpenClaw agent 配置打包成 Markdown，或从他人那里接收导入。

<p align="left">
  <a href="README.md">English</a>
</p>

---

## 功能

- **导出** — 扫描五个核心配置文件，生成 Markdown 能力包，直接在聊天中发送
- **导入** — 解析能力包内容，预览后让用户选择要导入哪些
- **选择性导入** — 可只导入部分文件，无需全量覆盖
- **安全提醒** — 导出前提醒 MEMORY.md 隐私风险，导入前展示预览

## 触发词

| 操作 | 关键词 |
|------|--------|
| 导出 | `导出能力包`、`打包我的能力`、`export ability` |
| 导入 | `导入能力包`、`学习能力包`、`import ability` |

## 导出的文件

| 文件 | 说明 |
|------|------|
| `AGENTS.md` | Agent 工作空间规则与约定 |
| `SOUL.md` | Agent 人格与行为准则 |
| `TOOLS.md` | 本地工具配置与笔记 |
| `IDENTITY.md` | Agent 身份标识 |
| `MEMORY.md` | 长期记忆与偏好记录 |

## 快速开始

**导出：**
```
用户：导出能力包
Agent：→ 扫描配置文件 → 生成 Markdown 能力包 → 在聊天中发送
```

**导入：**
```
用户：[粘贴能力包内容]
Agent：→ 展示文件预览 → 用户选择要导入哪些 → 写入对应文件
```

## 安装

```bash
npx skills add openclaw-ability-export
```

或访问 [ClawhHub](https://clawhub.com/skills/openclaw-ability-export)。
