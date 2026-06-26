---
name: dream-rem
version: 3.1.0
description: "深度整合记忆，将 daily 日记提炼到 topic 文件，清理过时内容 / 触发词：深度整合、梦境整理 / 命令：/dream-rem"
license: MIT
triggers:
  - 深度整合记忆
  - 梦境整理
  - 整合记忆
  - dream-rem
  - "/dream-rem"
---

# dream-rem v3.1.0 — 睡梦式记忆深度整合

定时深度整合：将分散的 daily 日记提炼合并到 topic 文件，删除过时内容，保持 `MEMORY.md` 简洁可用。

---

## 线性工作流

```
触发：Cron 满足条件 OR 用户输入 "/dream-rem"
         ↓
Step 1 — 准备
         读取 heartbeat-state.json
         读取 MEMORY.md 索引
         扫描 topics/ 目录，建立 topic 清单
         ↓
Step 2 — Orient（建立视野）
         输出 topic 清单（文件名 + type + description）
         检查 MEMORY.md 是否超限（200行/25KB）
         ↓
Step 3 — Gather（收集信号）【含核查清单】
         确定扫描窗口：最近14天的 daily 文件
         执行 ls memory/*.md，列出窗口内所有文件
         逐个读取每个文件（不得跳过任何文件）
         输出"已扫描文件清单（共 N 个）"
         对照 topics/，识别：新信息 / 过时内容 / 矛盾
         ↓ [必须输出核查清单，才能进入下一步]
         ↓
Step 4 — Consolidate（整合执行）
         按核查清单结果执行：
         - 新信息 → 追加到已有 topic 或新建 topic
         - 过时内容 → 更新或删除
         - 矛盾 → 保留正确版本，删除错误版本
         ↓
Step 5 — Prune & Index（精简索引）
         重写 MEMORY.md（≤200行 + ≤25KB）
         更新 heartbeat-state.json
         ↓
Step 6 — 输出执行报告
         扫描N个文件 / 新增N个 topic / 删除N个 / MEMORY.md行数
```

---

## Step 1 — 准备

1. 读取 `memory/heartbeat-state.json`
2. 自增 `sessionCount`（每次心跳代表一个新会话）
3. 检测是否满足整合条件：
   - sessionCount >= 5 **且** 距 lastDreamAt > 24小时
   - 或距 lastDreamAt > 72小时（强制整合）
4. 若不满足条件 → 回复 HEARTBEAT_OK，流程结束
5. 若满足条件 → 继续 Step 2

---

## Step 2 — Orient（建立视野）

1. 读取 `MEMORY.md` 索引，了解当前主题覆盖情况
2. 扫描 `topics/` 目录，建立已有 topic 清单（文件名 + type + description）
3. 确认 daily logs 位置（`memory/` 或 `memory/logs/`）

**MEMORY.md 超限警告**：若超过 200 行或 25KB，在提案中标记。

---

## Step 3 — Gather（收集信号）

**硬性要求：在扫描窗口内不得跳过任何文件。**

1. **确定扫描窗口**：取最近 14 天的 daily 文件（不得扩大也不缩小）
2. **列出窗口内所有文件**：先执行 `ls memory/*.md` 得到完整清单
3. **逐个读取每个文件**：窗口内所有文件都要读，不得只读最新或只读部分
4. **建立扫描记录**：输出格式：
   > 已扫描文件（共 N 个，窗口14天）：
   > - memory/2026-04-01.md ✓
   > - memory/2026-04-03.md ✓
5. **识别新信息**：对照已有 topic 清单，标记值得新增/追加的内容
6. **识别过时内容**：逐个对比 topic 文件和 daily 新结论，标记矛盾或被推翻的内容
7. **识别矛盾**：同一事实在不同文件说法不一致，标记冲突

**【核查清单 Gate】进入 Step 4 前，必须输出以下全部项，缺少任何一项不得进入整合：**

- [ ] **已扫描文件清单**：列出所有文件名，证明窗口内无遗漏
- [ ] **新信息摘要**：每条新信息一行，证明确实读了内容
- [ ] **过时 topic 清单**：含文件路径和过时原因，证明逐个对比过
- [ ] **矛盾 topic 清单**：含涉及的两个文件路径和矛盾内容

若核查清单任何一项为空，必须重新确认，不得跳过。

---

## Step 4 — Consolidate（整合执行）

按 Step 3 核查清单结果执行：

- **新信息 → 有对应 topic** → 合并追加进去
- **新信息 → 无对应 topic** → 新建 topic 文件（含 frontmatter）
- **过时内容** → 更新为最新结论，或删除旧版本
- **矛盾** → 保留正确版本，删除错误版本（不保留两个）

---

## Step 5 — Prune & Index（精简索引）

1. 重写 `MEMORY.md`：
   - 每行一个指针：`- [名称](topics/文件名.md) — 一句话 hook`（≤150字符）
   - 总行数 ≤200，大小 ≤25KB
   - 删除过时 topic 的指针，补充新增 topic 的指针
2. 验证修改后文件可读
3. 更新 `heartbeat-state.json` 的 `lastDreamAt`，重置 `sessionCount`

---

## Step 6 — 输出执行报告

> ## 🌙 Dream 完成 · YYYY-MM-DD HH:MM
> **扫描窗口**：14天
> **已扫描文件**：N个
> **本次耗时**：N分钟
>
> ### 整合结果
> | 类型 | 数量 | 说明 |
> |------|------|------|
> | 🌟 新增/更新 topic | N个 | - |
> | 🗑 清理过时记忆 | N条 | - |
> | 📋 MEMORY.md | N行（之前 M行） | ✅ 精简 |
>
> ### 本次主要变化
> - **新增**：topics/xxx.md
> - **更新**：topics/ccc.md
> - **删除**：topics/ddd.md（过时）
>
> ### 下次整合预计
> YYYY-MM-DD HH:MM（≥5会话 + ≥24小时后自动触发）

---

## 核心原则

1. **MEMORY.md = 纯索引**——不是记忆文件，每行一个指针
2. **topic 文件 = 真实记忆**——所有记忆内容存在 `topics/` 下
3. **删除被推翻的**——不保留矛盾的两个版本
4. **相对日期 → 绝对日期**——`"昨天"` → `"2026-04-04"`

---

## 安装后配置

首次安装后，请在终端执行以下命令创建定时任务：

```bash
openclaw cron add --name "记忆深度整合（Dream）" --every 12h --session isolated --timeout-seconds 600 --message "检查并执行记忆深度整合（dream-rem）。..." --announce
```

**心跳状态文件**：`memory/heartbeat-state.json`，内容如下：
```json
{ "lastExtraction": null, "lastDreamAt": null, "sessionCount": 0 }
```

---

## 触发条件

- sessionCount >= 5 **且** 距上次整合 > 24小时
- 或距上次整合 > 72小时（强制整合）

---

## 权限要求

- `FileRead`：读取 MEMORY.md、topics/、daily 文件
- `FileWrite` / `FileEdit`：修改 topics/、`MEMORY.md`、`memory/heartbeat-state.json`

## 触发词

- 自动：Cron 每 12 小时检测（需手动创建）
- 手动：`/dream-rem`

---

*本 Skill 基于 CC 记忆系统设计，适配 OpenClaw v3.1.0*
