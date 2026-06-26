---
name: heycube-setup
description: >
  一键安装 HeyCube 黑方体个人档案管理服务到 OpenClaw。
  创建 GET_CONFIG/UPDATE_DATA 两个 Hook Skill、SQLite 管理工具、修改 TOOLS.md 和 AGENTS.md。
  触发场景："安装黑方体"、"配置 HeyCube"、"heycube setup"、"安装个人档案管理"。
---

# HeyCube 黑方体 — 一键安装

将黑方体个人档案服务完整配置到当前 OpenClaw 实例。

## 概览

安装完成后，每次对话自动执行：
1. **GET_CONFIG**（前置）→ 调用 API 获取维度 → 查本地 SQLite → 注入用户画像
2. **UPDATE_DATA**（后置）→ 脱敏摘要 → 调用 API 获取更新维度 → 提取数据写入 SQLite

隐私：脱敏摘要发服务端，结构化档案完全存本地 SQLite。

## 安装步骤

### 1. 确认环境

```powershell
node --version
```

### 2. 创建 Hook Skill 目录

```powershell
New-Item -ItemType Directory -Force -Path "$env:USERPROFILE\.agents\skills\heycube-get-config-0.1.0"
New-Item -ItemType Directory -Force -Path "$env:USERPROFILE\.agents\skills\heycube-update-data-0.1.0"
New-Item -ItemType Directory -Force -Path "{workspace}/scripts"
```

### 3. 写入 Hook Skill 文件

将本 skill 的 `assets/hook-skills/get-config.md` 复制到：
`~/.agents/skills/heycube-get-config-0.1.0/SKILL.md`

将本 skill 的 `assets/hook-skills/update-data.md` 复制到：
`~/.agents/skills/heycube-update-data-0.1.0/SKILL.md`

> ⚠️ 复制前检查目标是否已存在同名文件，若存在且内容非空则提示用户确认覆盖。

### 4. 写入 SQLite 管理工具

将 `scripts/personal-db.js` 复制到 `{workspace}/scripts/personal-db.js`。
将 `scripts/package.json` 复制到 `{workspace}/scripts/package.json`。

### 5. 安装依赖 & 初始化数据库

```powershell
cd "{workspace}/scripts" && npm install
cd "{workspace}/scripts" && node personal-db.js init
```

预期输出：`{"status":"ok","db":"<path>/personal-db.sqlite"}`

### 6. 修改 TOOLS.md — 添加 HeyCube 配置段

在 `{workspace}/TOOLS.md` 末尾追加：

```markdown
## HeyCube Server
- BASE_URL: https://heifangti.com/api/api/v1/heifangti
- API_KEY: (未配置 — 在此填入黑方体 API Key)
- DB_PATH: {workspace}/personal-db.sqlite
- 说明: 配置 API_KEY 后启用黑方体服务端分析；未配置则静默跳过
```

> ⚠️ 如果 TOOLS.md 中已有 `HeyCube Server` 段，只更新缺失字段，不覆盖用户已填写的 API_KEY。

### 7. 修改 AGENTS.md — 添加 Hook 执行规则

在 `{workspace}/AGENTS.md` 的 `## Make It Yours` 之前插入：

```markdown
## 🔮 HeyCube 档案管理 Hook（每次对话必执行）

由 AGENTS.md 硬规则驱动，**不依赖 skill description 匹配**。

### 执行顺序

```
用户消息 → ① GET_CONFIG → ② 主任务 skill → ③ 回复用户 → ④ UPDATE_DATA
```

### ① GET_CONFIG（对话处理前）
1. 读取 `~/.agents/skills/heycube-get-config-0.1.0/SKILL.md`
2. 按其中流程执行：对话分类 → 前置检查 → 调用 API → 查询 SQLite → 注入上下文
3. **出错则静默跳过，不阻塞主流程**

### ② 主任务
正常匹配 skill → 处理用户请求 → 回复用户

### ④ UPDATE_DATA（回复完成后）
1. 读取 `~/.agents/skills/heycube-update-data-0.1.0/SKILL.md`
2. 按其中流程执行：脱敏摘要 → 调用 API → 提取数据 → 写入 SQLite
3. **出错则静默跳过**

### 关键规则
- **不阻塞主流程**：任何环节出错都静默跳过
- **严格脱敏**：发送到服务端的内容绝不含真实个人信息
- **开关控制**：文件 `.heycube-off` 存在则跳过全部
```

> ⚠️ 如果 AGENTS.md 中已有 `HeyCube` 相关段，不重复添加。

### 8. 验证安装

```powershell
Test-Path "$env:USERPROFILE\.agents\skills\heycube-get-config-0.1.0\SKILL.md"
Test-Path "$env:USERPROFILE\.agents\skills\heycube-update-data-0.1.0\SKILL.md"
Test-Path "{workspace}/scripts/personal-db.js"
Test-Path "{workspace}/scripts/node_modules/better-sqlite3"
cd "{workspace}/scripts"; node personal-db.js get-all
```

全部通过后输出：

```
✅ HeyCube 黑方体配置完成
- GET_CONFIG Skill: 已就位
- UPDATE_DATA Skill: 已就位
- SQLite 工具: 已安装并初始化
- TOOLS.md: 已配置（请填写 API_KEY 以启用服务端分析）
- AGENTS.md: 已添加 Hook 规则

⚠️ 下一步：在 TOOLS.md 中填写 HeyCube API_KEY
获取地址：https://heifangti.com
格式：hey_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

## 故障排除

| 问题 | 排查 |
|------|------|
| Hook 未触发 | 检查 AGENTS.md 是否包含 HeyCube 执行规则段 |
| API 返回 402 | 黑方体账户黑点不足 |
| SQLite 报错 | 重新执行 `cd scripts && node personal-db.js init` |
| better-sqlite3 安装失败 | 需 C++ 编译工具（Windows: Visual Studio Build Tools） |
| 临时关闭 Hook | 在 workspace 根目录创建 `.heycube-off` 文件 |
| 查看已采集档案 | `cd scripts && node personal-db.js get-all` |
