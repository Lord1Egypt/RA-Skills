# 记忆系统三件套 更新流程规范

> 本规范旨在确保：skill 文件、GitHub、ClawhHub 三端的版本和描述始终保持一致。

---

## ⚠️ 核心原则

**每次更新必须同时检查并同步以下四处（任何一处不一致都是 bug）：**

| 位置 | 路径 | 说明 |
|------|------|------|
| **本地开发文件** | `D:\OpenClaw\workspace\openclaw-cc-contrib\` | 所有更新的起点 |
| **运行时 skill** | `~/.openclaw/skills/` | OpenClaw 实际加载的版本 |
| **GitHub** | `github.com/Jofiction918/openclaw-cc-contrib` | 公开发布仓库 |
| **ClawhHub** | clawdhub.com | 商店展示版本 |

---

## 📋 标准更新流程

### 第一步：改本地开发文件

在 `D:\OpenClaw\workspace\openclaw-cc-contrib\` 下对应技能的 `SKILL.md` 中修改。

**每次修改必须检查以下 5 项：**

1. `version:` — 版本号（每次发布递增）
2. `description:` — 一句话描述（ClawhHub 展示用，不能有误导信息）
3. 正文内容 — 触发机制、Cron 命令、频率等描述
4. 正文内所有 cron 频率/ID — 必须与实际运行的 cron 一致
5. 版本号在正文中出现的地方（如标题 `# xxx v3.0.0`）

### 第二步：本地确认

在 OpenClaw 里验证：
- skill 内容是否正确
- cron 命令格式是否可用
- 版本号是否递增

### 第三步：同步三处

确认本地无误后，按顺序执行：

```bash
# 1. 同步到 runtime skills（让本地 OpenClaw 加载最新）
cp SKILL.md ~/.openclaw/skills/[skill-name]/SKILL.md

# 2. 推送 GitHub
cd D:\OpenClaw\workspace\openclaw-cc-contrib
git add -A && git commit -m "[描述]" && git push

# 3. 推送 ClawhHub（先临时移走冲突的 skill 目录）
cd D:\OpenClaw\workspace
mv skills/buddy /tmp/buddy && mv skills/pet /tmp/pet && mv skills/volc-vision /tmp/volc
clawdhub sync --all --changelog "[描述]"
mv /tmp/buddy skills/ && mv /tmp/pet skills/ && mv /tmp/volc skills/
```

### 第四步：验证三端一致

推送后检查：
- GitHub repo 上的 SKILL.md 版本号
- ClawhHub 页面显示的版本号
- runtime `~/.openclaw/skills/` 里的版本号

---

## 🔢 版本号规则

格式：`主版本.次版本.修订号`

- **修订号 (3.0.x)**：修 bug、改描述、调整文案 → 递增修订号
- **次版本 (3.x.0)**：改动触发机制、cron 参数、输出格式等核心逻辑 → 递增次版本
- **主版本 (x.0.0)**：不常用，重大重构才变

---

## ❌ 禁止事项

1. **禁止跳过本地文件直接改 runtime** — 一切从本地文件出发
2. **禁止只推 GitHub 不推 ClawhHub**（反之亦然）— 两边都要一致
3. **禁止 description 里写具体频率/数字** — 正文里写，description 保持简洁
4. **禁止 version 号倒退** — 每次必须 >= 上次
5. **禁止只推不验证** — 推送后必须检查三端是否一致

---

## 📝 Git Commit 规范

```
[类型] 简短描述

类型：feat / fix / docs / style / refactor
示例：
- docs: 更新cron命令格式
- fix: 修正触发机制描述
- style: 修模板颜色对比度
```

---

## 🆘 出错怎么办

**ClawhHub 和 GitHub 不一致**：以本地文件为准，重新 push 落后的一方

**Runtime 和 ClawhHub 不一致**：重新 cp 本地文件到 runtime，再 push

**版本号冲突**：检查 ~/.openclaw/skills/ 里的实际 version，ClawhHub 会自动递增

---

## 📁 技能目录对应关系

| 技能名 | 本地路径 | Runtime 路径 |
|--------|---------|-------------|
| extract-memories | `.../openclaw-cc-contrib/extract-memories/` | `~/.openclaw/skills/extract-memories/` |
| dream-rem | `.../openclaw-cc-contrib/dream-rem/` | `~/.openclaw/skills/dream/` |
| memory-sorting | `.../openclaw-cc-contrib/memory-sorting/` | `~/.openclaw/skills/memory-review/` |

> 注意：dream-rem 安装后映射到 `dream/` 目录，memory-sorting 映射到 `memory-review/` 目录。

---

*本规范制定于 2026-04-07*
