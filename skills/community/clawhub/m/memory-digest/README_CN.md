# Memory Digest（记忆周报）

**从 AI agent 的记忆里生成周报——给拥有它的那个人看。**

[English](./README.md) | [中文](./README_CN.md)

---

有长期记忆的 agent 每天产出没人读的日志。Memory Digest 把这堆记忆变成一页报告：发生了什么、哪些项目在推进、什么还悬着、哪些数字变了。

大部分记忆工具是给 agent 自己存取用的。这个是替**主人**读同一批文件。

## 产出什么

| 板块 | 含义 |
|---|---|
| **活动时间线** | 按天列出条目、章节数、话题、一句话摘要 |
| **项目动量** | 项目/话题名 + 动量标记：🆕 新起、▶️ 推进中、⏸️ 停滞 |
| **未闭环线索** | 待办/待确认事项 + 记录日期 |
| **数字变化** | 窗口期内提到的指标（下载量、用户数、星标……） |

## 快速开始

```bash
git clone https://github.com/Thomaszhou22/memory-digest.git
python3 memory-digest/scripts/memory_digest.py --memory-dir /path/to/agent/workspace --days 7
```

参数：`--days N`（窗口，默认 7）｜ `--out report.md`（存文件）｜ `--json`（机器可读）。

适用于任何按日期命名的日志结构（`memory/YYYY-MM-DD.md`）。脚本**只读**。

## 实测验证

在一个 130+ 记忆文件的活跃 agent 工作区上开发验证。首次真实运行即正确产出：七天活动时间线、一个停滞六天的项目、以及所有仍未得到主人回复的待确认事项——包括五天前记下、否则会被彻底遗忘的那些。

## 适合挂 cron

```bash
# 每周一 09:00 生成周报
0 9 * * 1 python3 /path/to/memory-digest/scripts/memory_digest.py --memory-dir ~/agent --days 7 --out ~/reports/week.md
```

## 作为 OpenClaw / Claude Code skill 使用

把本文件夹复制或软链到 skills 目录。`SKILL.md` 在"weekly digest""what did my agent do""记忆周报""述职报告"等请求时触发。skill 流程在交付前加了一步核验：未闭环线索是启发式抽取的，agent 呈现前会确认待办是否真的还没解决。

## 设计要点

- **只读。** 报告绝不改动记忆文件。
- **中英双语抽取。** 待办标记（待办/待确认/pending/TODO）与指标单位（下载/users/星/stars）中英文都认。
- **启发式，不是真理。** 动量和未闭环是供人复核的候选；skill 的任务是把一周压缩成一页，不是永远不出错。

## 姊妹 skill

- [memory-checkup](https://github.com/Thomaszhou22/memory-checkup) — 记忆库一致性审计：过期数字、悬空引用、归档断档
- 组合用法：checkup 找出哪里不对，digest 呈现发生了什么。

## 目录结构

```
├── SKILL.md                    # agent 用的 skill 说明
├── scripts/
│   └── memory_digest.py        # 只读周报生成脚本
├── README.md
└── README_CN.md
```

## 局限

- 假设每天文件用 Markdown `#`-`##` 标题组织
- 项目提取基于关键词，特殊命名可能需要调参
- 不做向量检索，读的是文本不是 embedding

## 许可

MIT
