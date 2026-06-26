---
name: heycube-setup
description: >
  引导安装 HeyCube 黑方体个人档案管理服务到 OpenClaw。分步配置：设置环境变量、安装 SQLite 工具、安装口令触发 Skill。
  用户主动说"安装黑方体"、"配置 HeyCube"、"heycube setup"时触发。
---

# HeyCube 黑方体 — 引导安装

交互式引导用户完成配置，每一步需用户确认后才执行。

## 安装流程

### Step 1：设置 API Key

提示用户设置环境变量 `HEYCUBE_API_KEY`（从 https://heifangti.com 获取）。

Windows PowerShell 永久生效：
```powershell
[System.Environment]::SetEnvironmentVariable('HEYCUBE_API_KEY', 'hey_xxx', 'User')
```

Mac/Linux：
```bash
echo 'export HEYCUBE_API_KEY=hey_xxx' >> ~/.zshrc
source ~/.zshrc
```

验证：`$env:HEYCUBE_API_KEY`（PowerShell）或 `echo $HEYCUBE_API_KEY`（bash）

### Step 2：安装 SQLite 管理工具

1. 复制本 skill 的 `scripts/personal-db.js` → `{workspace}/scripts/personal-db.js`
2. 复制本 skill 的 `scripts/package.json` → `{workspace}/scripts/package.json`
3. 运行：
```powershell
cd "{workspace}/scripts"; npm install; node personal-db.js init
```

预期输出：`{"status":"ok","db":"..."}`

### Step 3：安装档案 Skill

将以下两个 Skill 复制到 `~/.agents/skills/`：

- `assets/hook-skills/get-config.md` → `~/.agents/skills/heycube-get-config-0.1.0/SKILL.md`
- `assets/hook-skills/update-data.md` → `~/.agents/skills/heycube-update-data-0.1.0/SKILL.md`

### Step 4：修改 TOOLS.md

在 `{workspace}/TOOLS.md` 追加：
```markdown
## HeyCube Server
- BASE_URL: https://heifangti.com/api/api/v1/heifangti
- API_KEY: 通过环境变量 HEYCUBE_API_KEY 配置
- DB_PATH: {workspace}/personal-db.sqlite
```

> ⚠️ 如果 TOOLS.md 已有 HeyCube 段，只更新缺失部分。

### 完成输出

```
✅ HeyCube 黑方体配置完成
- API Key: 已设置环境变量
- SQLite 工具: 已安装并初始化
- 档案 Skill: 已就位

📋 使用方式：
- 说"提取黑方体档案" — 从 API 获取维度配置，查询本地已有档案，注入上下文辅助对话
- 说"存入黑方体档案" — 脱敏总结当前对话，调用黑方体 API ，提取个人数据写入本地档案
- 说"查看黑方体档案" — 查看所有已采集数据
- 说"关闭黑方体" — 临时关闭（创建 .heycube-off）
- 说"开启黑方体" — 重新启用
```
