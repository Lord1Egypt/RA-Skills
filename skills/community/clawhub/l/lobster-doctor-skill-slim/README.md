---
name: lobster-doctor
version: 1.2.0
description: |
  🦞 龙虾医生 — OpenClaw workspace 健康管家。体检诊断+安全清理+技能瘦身+cron巡检。说句话就能用。
tags: [maintenance, cleanup, workspace, health, automation, optimization, token-saving]
---

# 🦞 龙虾医生

你的 OpenClaw workspace 会越来越臃肿——临时文件堆积、技能描述膨胀、cron 任务遗忘。龙虾医生帮你自动治理。

**一句话**：「给龙虾做个体检」「清理一下」「技能太多了」——剩下的交给它。

---

## 为什么需要它？

用久了你会遇到这些问题：

| 痛点 | 后果 |
|------|------|
| 临时脚本、测试文件堆积 | workspace 一团乱 |
| 安装了很多技能 | 每轮对话白烧几千 token |
| cron 任务忘了清理 | 僵尸任务占资源 |
| 不知道 workspace 有多大 | 磁盘悄悄爆满 |

龙虾医生就是来解决这些的。

---

## 核心功能

### 🩺 体检诊断
一句话：「给龙虾做个体检」

自动扫描并报告：
- 废弃文件（超过3天未改的临时脚本）
- 重复文件（内容相同）
- 空目录、大文件
- 僵尸 cron 任务
- token 消耗估算

### 🧹 安全清理
一句话：「帮我清理一下」

**四重保障，绝不误删**：
- 核心文件白名单保护（MEMORY.md、SOUL.md 等）
- skills/、memory/、node_modules/ 绝不碰
- 清理前必须预览确认
- 自动备份，随时可恢复

### ✂️ 技能瘦身 ⭐ 独家功能
一句话：「技能太多了 / token 太贵」

**这是龙虾医生的杀手锏**——其他工具都没有。

**问题**：每个技能的 description 都注入系统提示。136 个技能 = 每轮 ~11K tokens 白白烧掉。

**解法**：精简 description，只保留核心功能句和触发关键词。description 是"门牌号"，不是"说明书"，精简不影响调用准确性。

**效果**：每轮节省 ~3,200 tokens，一天几十轮对话就是几万 tokens。

### 🔍 cron 巡检
一句话：「检查有没有僵尸任务」

发现已禁用、临时创建、长期未运行的任务。

---

## 使用方式

**直接说人话**，龙虾医生会自动理解并执行：

| 你说 | 它做 |
|------|------|
| 「做个体检」 | 扫描并输出健康报告 |
| 「清理一下」 | 预览待清理文件 → 你确认 → 执行清理 |
| 「技能太多了」 | 分析技能描述体积 → 给出瘦身建议 |
| 「检查僵尸任务」 | 扫描 cron 任务列表 |

---

## 安装

```bash
# 从 ClawHub 一键安装
openclaw skill install lobster-doctor

# 或从 GitHub 克隆
git clone https://github.com/Masongmx/lobster-doctor.git
cp -r lobster-doctor/skill ~/.openclaw/workspace/skills/lobster-doctor
```

---

## 安全机制

- **预览优先**：任何修改操作都先展示预览
- **自动备份**：清理前自动备份到 `.cleanup-backup/`
- **白名单保护**：核心文件永远不会被删除
- **零 API 调用**：纯本地运行，不花钱

---

## 实测数据

技能瘦身效果（136个技能）：

| 指标 | 精简前 | 精简后 |
|------|--------|--------|
| Description 总字符 | 22,387 | 9,919 |
| 每轮消耗 tokens | ~10,312 | ~7,195 |
| **每轮节省** | — | **~3,200 tokens** |

---

## 技术规格

- Python 3.8+，零外部依赖
- 纯本地运行，零 API 调用
- 支持 macOS / Linux / WSL

---

## 相关项目

- [Memory Tree](https://github.com/Masongmx/memory-tree) — 记忆生命周期管理，和龙虾医生搭配使用效果更好

---

## License

MIT
