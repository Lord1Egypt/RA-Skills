# GitHub PR 文档自动生成与知识库同步

> 一条命令完成 PR → 代码分析 → 技术文档 → 飞书/Wiki 同步全流程

## 🎯 业务场景

**痛点**：每次 GitHub PR 合并后，团队都需要手动编写变更记录、更新文档、上传到 Wiki。这个过程繁琐且容易被遗忘，导致知识库与实际代码脱节。

**解决**：开发者只需提供一个 PR 链接，AI 自动完成从抓取 PR 内容、分析代码变更、生成结构化技术文档，到同步到飞书 Wiki 或企业微信文档的全流程。

## 🧩 Skill 编排图谱

```
[用户输入 PR 链接]
        │
        ▼
┌──────────────────┐
│     github       │ → 获取 PR 标题、描述、作者、状态、变更文件列表
└────────┬─────────┘
         │ PR 详情 JSON
         ▼
┌──────────────────┐
│   code-review    │ → 分析 diff，提取关键变更、风险点、影响范围
└────────┬─────────┘
         │ 变更分析结果
         ▼
┌──────────────────┐
│    summarize     │ → 将变更内容结构化，生成技术文档草稿
└────────┬─────────┘
         │ 技术文档 Markdown
         ▼
    【分支路由】按用户偏好选择输出目标
         │
    ┌────┴────┐
    ▼         ▼
┌────────┐ ┌─────────────────┐
│feishu-  │ │  wecom-doc      │
│  wiki   │ │  (企业微信文档)  │
└────────┘ └─────────────────┘
         │
         ▼
   【知识库文档创建成功】
```

## 📦 依赖 Skills

| Skill | 用途 | 调用方式 |
|-------|------|---------|
| `github` | 调用 `gh pr` 获取 PR 详情、文件列表、diff | `exec` / `gh` CLI |
| `code-review` | 分析代码变更，提取关键逻辑和风险点 | 内部逻辑 |
| `summarize` | 将非结构化内容转为结构化技术文档 | `summarize` skill |
| `feishu-wiki` | 在飞书知识库创建/更新文档 | `feishu_wiki` tool |
| `wecom-doc` | 在企业微信文档创建文档 | `wecom-doc` skill |

## 💡 使用示例

### 场景：合并了一个重要 PR，需要同步到团队知识库

**用户输入**：
```
帮我生成这个PR的变更文档：https://github.com/myorg/backend/pull/234
同步到飞书Wiki，文档库是"技术文档"
```

**AI 自动执行**：
1. `gh pr view 234 --repo myorg/backend --json title,body,files,commits,state`
2. `gh pr diff 234 --repo myorg/backend` 获取完整 diff
3. AI 分析关键文件变更（如 `src/api/users.go` 新增了用户认证逻辑）
4. 生成结构化 Markdown 文档
5. 调用 `feishu_wiki` 在"技术文档"知识库下创建文档

**输出文档预览**：
```
# [PR #234] 新增用户 JWT 认证模块

## 📋 基本信息
- 仓库：myorg/backend
- 作者：@zhangsan
- 状态：✅ Merged

## 📝 变更摘要
新增基于 JWT 的用户认证模块，支持 token 刷新和权限验证...

## 📂 变更文件
| 文件 | 类型 | 说明 |
|------|------|------|
| src/auth/jwt.go | ✨ 新增 | JWT 核心实现 |
| src/auth/middleware.go | ✨ 新增 | 认证中间件 |
| src/config/auth.go | ✏️ 修改 | 新增 auth 配置项 |
```

## ⚙️ 配置要求

- `gh` CLI 已完成 GitHub 账号授权 (`gh auth login`)
- 飞书 App 拥有目标知识空间的写入权限
- 企业微信已配置文档管理权限
