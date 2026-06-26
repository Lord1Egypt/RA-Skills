---
name: novel-architect
description: "爽文小说全流程工坊：整合 FBS 工作流 + 爽文生成器。从方向提炼 → 大纲规划 → 逐章生成 → 质检收口，全程追踪。Trigger: 用户提及写小说/写书/章节/大纲/爽文/写作/架构。"
version: 1.0.0
license: MIT
language: zh-CN
---

# Novel Workshop · 爽文全流程工坊

整合 **FBS 工作流引擎**（S→P→C→B 全流程追踪、质检门禁）与 **爽文生成器**（提示词完善、世界观构建、逐章生成），实现从方向到大纲到成稿的完整闭环。

---

## 架构

```
用户方向
    ↓
[FBS intake-router]  ← 项目初始化，确定 bookRoot
    ↓
世界观 & 提示词完善（novel-generator 逻辑）
    ↓
章节大纲（FBS S1 输出 → novel-generator 大纲模板）
    ↓
逐章生成（novel-generator 逐章逻辑 + FBS 章节追踪）
    ↓
质检 & 收口（FBS polish-gate / release-governor）
```

---

## 记忆系统（统一）

**书稿根目录**：`{bookRoot}/`

```
{bookRoot}/
├── .fbs/                        # FBS 工作流核心
│   ├── workbuddy-resume.json    # 会话恢复点
│   ├── esm-state.md             # 当前阶段（S0-S4）
│   ├── chapter-status.md        # 各章进度台账
│   ├── plan/                    # 大纲（来自 S1）
│   └── expansion-plan.md       # 扩写计划（来自 S3.5）
├── .learnings/                  # novel-generator 记忆（内置于 FBS）
│   ├── CHARACTERS.md            # 角色设定（随写作更新）
│   ├── LOCATIONS.md            # 地点设定
│   ├── PLOT_POINTS.md          # 关键情节点
│   └── ERRORS.md               # 生成失败记录 & 改进
├── output/                      # 章节正文（每章一个 .md）
└── deliverables/               # 交付物
```

> 所有写作上下文统一存在 `{bookRoot}/.learnings/`，FBS 和 novel-generator 共用同一套记忆，无需重复维护。

---

## 工作流阶段（FBS 标准）

### S0 · 素材收集
- 用户输入方向（题材/关键词/灵感/一句话）
- 执行 `intake-router.mjs --book-root "{bookRoot}" --intent auto --json`
- 整理为初始素材（来自 novel-generator 的"提示词完善"逻辑）
- **门禁**：素材数 ≥ 赛道数 × 2

### S1 · 规划
- 生成完整大纲（使用 novel-generator 的大纲结构）
- 包含：章节目录、每章目标字数、起承转合设计、爽点分布
- 写入 `.fbs/plan/`
- **门禁**：`s1-exit-gate`（章标题 + 目标字数确认）

### S2 · 写作
- 按章顺序逐章生成
- 每章生成前读取 `.learnings/` 更新上下文
- 生成后写入 `output/第XX章.md`
- 用 `chapter-status.md` 更新进度
- **门禁**：`s2-exit-gate`（章数 ≥ 3 + 字数达标）

### S3 · 扩写 & 精修
- **扩写**：基于 `expansion-plan.md` 增加字数/情节深度
- **精修**：执行 `polish-gate.mjs` 质检后再改稿
- 扩写前必须备份：`source-write-backup.mjs`
- **门禁**：扩写字数以脚本实测为准，不许纯模型估算

### S4 · 质检 & 交付
- 执行 `final-manuscript-clean-gate.mjs`（检测过程标注，有则不交付）
- 执行 `material-marker-governor.mjs --fix`（清理待核实标注）
- 执行 `release-governor.mjs`（终稿唯一版本 + 归档）
- 交付前确认无残留 `[DISCARDED-*]` / `待核实-MAT` 标注

---

## 提示词完善流程（novel-generator 逻辑）

收到用户方向后，自动补全：

```
1. 题材定位    → 主类型 + 子类型（如：都市 + 修仙）
2. 世界观设定  → 力量体系、社会规则、时代背景
3. 主角人设    → 初始身份、性格、金手指/挂
4. 核心冲突    → 主线矛盾 + 前3章即时冲突
5. 爽点设计    → 打脸节奏、升级频率、装逼方式
6. 节奏规划    → 每N章一个小高潮、每M章一个大高潮
7. 配角框架    → 对手/盟友/红颜各至少1人
8. 开篇钩子    → 第一章用什么抓住读者
```

完善后请用户确认，再进入大纲阶段。

---

## 执行命令速查

| 场景 | 命令 |
|------|------|
| 初始化项目 | `node scripts/intake-router.mjs --book-root "{bookRoot}" --intent auto --json --enforce-required` |
| 门禁检查 | `node scripts/s0-exit-gate.mjs --book-root "{bookRoot}" --json --confirm-advance` |
| 进入下一阶段 | 按 esm-state.md 中的阶段推进阈值判断 |
| 章节进度 | `node scripts/chapter-status-drift.mjs --book-root "{bookRoot}"` |
| 精修质检 | `node scripts/polish-gate.mjs --book-root "{bookRoot}"` |
| 扩写备份 | `node scripts/source-write-backup.mjs --book-root "{bookRoot}" --scope expansion --json` |
| 扩写门禁 | `node scripts/expansion-gate.mjs --book-root "{bookRoot}"` |
| 终稿清理 | `node scripts/final-manuscript-clean-gate.mjs --book-root "{bookRoot}"` |
| 交付收口 | `node scripts/release-governor.mjs --book-root "{bookRoot}"` |
| 退出/保存 | `node scripts/fbs-cli-bridge.mjs exit -- --book-root "{bookRoot}" --json` |

> `scripts/` 在本技能根目录下，直接使用 `node scripts/<file>` 调用，`cwd` 为 novel-architect 技能根目录。

> ⚠️ 依赖已嵌入：`node_modules/` 和 `references/` 已复制到本技能根目录，**无需依赖外部 fbs_bookwriter 目录**。

---

## 规则

1. **串行优先**：每轮最多改 2 个文件，不要并行生成多章
2. **先备份再精修**：执行 `polish-gate` 前必须先 `source-write-backup`
3. **门禁不可绕过**：任何"已完成/已通过"结论必须附脚本证据
4. **统一记忆**：角色/地点/情节统一写入 `.learnings/`，不要散落在别处
5. **交付前检查**：`final-manuscript-clean-gate` 检测到标注则不得交付

---

## Trigger

- 用户说：写小说/写书/章节/大纲/爽文/写作/续写
- 用户说：开始下一章/继续写/这个情节怎么发展
- 用户说：检查章节进度/质量审核
- 用户说：导出终稿/打印/交付
