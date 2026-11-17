# Skill Handoff: 数字内容处理到 ClawHub 资源中心入库（process-to-ingest）

> 本文件由 `workflow-structurer` 的五阶段渐进式澄清方法产出。
> 主题：把一份"可用的数字内容"经过业务流程处理，最终入库（发布）到 ClawHub 资源中心。

## Goal
把一份已有的数字内容（Markdown 说明/文档）经过流程化处理、打包并发布为 ClawHub 上可检索、可安装的 skill 资源，形成可复现的端到端链路。

## Trigger Phrases
- "把这份内容入库到资源中心"
- "梳理流程然后发布到 ClawHub"
- "process content and ingest into resource center"

## Step Skeleton（步骤骨架）
1. 目标与内容确认
2. 流程结构化（workflow-structurer）
3. 按 skill 规范打包（demo-asset-ingest）
4. dry-run 预检
5. 发布入库（clawhub publish）
6. 入库验证（clawhub search）

---

## Step 1: 目标与内容确认

**Input:**
- 一份可用的数字内容（本例为 Markdown 流程说明）
- 目标资源中心（ClawHub）与登录身份（`clawhub whoami`）

**Output:**
- 明确的入库用途、唯一 slug、内容清单

**Responsibilities:**
- 负责人确认内容非机密、可公开发布；确定唯一 slug 与展示名

**Risks:**
- 内容含机密或个人数据
- slug 全局不唯一导致发布冲突

**Validation:**
- `clawhub whoami` 返回有效身份
- `clawhub search <slug>` 无同名结果（确认为空/无冲突）

**Rules:**
- slug 必须 kebab-case 且全局唯一
- 发布前必须脱敏，不得包含凭证/客户数据

---

## Step 2: 流程结构化（workflow-structurer）

**Input:**
- 自然语言描述的模糊需求
- 6 步骨架

**Output:**
- 含 Input/Output/Responsibilities/Risks/Validation/Rules 的结构化步骤文档（本文件）

**Responsibilities:**
- 按 Phase 1→5 渐进澄清：逐个步骤钻取，每步补全 6 个字段后汇总确认

**Risks:**
- 跳步直接生成完整流程，导致字段缺失或假设错误
- 在 Risks 未识别前先写 Rules（违反工具约束）

**Validation:**
- 每个步骤 6 个字段全部填写
- 不混写 Validation 与 Rules

**Rules:**
- 一次只处理一个步骤
- 不臆造缺失细节，必须澄清
- 先有 Risks 再有 Rules

---

## Step 3: 按 skill 规范打包（demo-asset-ingest）

**Input:**
- Step 2 产出的结构化 handoff（DESCRIPTION 素材）

**Output:**
- skill 目录：`<slug>/SKILL.md` + `<slug>/references/DESCRIPTION.md`

**Responsibilities:**
- 按最小可用 skill 形状创建目录；SKILL.md 含 frontmatter + 操作说明；DESCRIPTION.md 放上游产物

**Risks:**
- 目录结构错误（缺少 references/ 或 SKILL.md）
- DESCRIPTION.md 与 SKILL.md 内容不一致

**Validation:**
- `ls -R <slug>` 显示 SKILL.md 与 references/DESCRIPTION.md

**Rules:**
- 目录必须同时包含 SKILL.md 与 references/DESCRIPTION.md
- 内容用 UTF-8 Markdown

---

## Step 4: dry-run 预检

**Input:**
- 已打包的 skill 目录

**Output:**
- 预检结果（元数据、结构、slug 可用性），不真正发布

**Responsibilities:**
- 运行 dry-run，核对 slug、name、tags、topics、结构

**Risks:**
- 跳过 dry-run 直接发布，遇到结构/元数据错误才失败

**Validation:**
- dry-run 退出码 0 且无报错

**Rules:**
- 正式发布前必须先 dry-run

---

## Step 5: 发布入库（clawhub publish）

**Input:**
- 通过 dry-run 的 skill 目录 + 唯一 slug/name/tags/topics

**Output:**
- ClawHub 资源中心中的新 skill 条目（可能进入审核）

**Responsibilities:**
- 执行 `clawhub publish <path> --slug ... --name ... --tags ... --topics ...`

**Risks:**
- 审核延迟导致搜索暂时不可见
- 网络/鉴权失败

**Validation:**
- 命令输出发布成功

**Rules:**
- 使用 `clawhub publish`（或等价 `clawhub skill publish`）
- 必须在有效登录身份下执行

---

## Step 6: 入库验证（clawhub search）

**Input:**
- 已发布的 slug

**Output:**
- 资源中心可检索到该条目（允许审核延迟）

**Responsibilities:**
- 搜索确认条目可发现；必要时重试

**Risks:**
- 新条目标记为需要审核，立即搜索可能为空

**Validation:**
- `clawhub search <slug>` 返回对应条目或确认处于审核队列

**Rules:**
- 若首次搜索为空，等待审核后重试而非反复发布

---

## Key Rules
- 不跳步：先结构化后打包
- slug kebab-case、全局唯一、发布前查重
- 发布前脱敏
- 先 dry-run 后正式 publish
- 一次只处理一个流程步骤；Validation 与 Rules 不混写

## Key Risks
- 内容泄露（机密/凭证/客户数据）
- slug 冲突导致发布失败
- 跳步导致产物低价值或误导
- 目录结构畸形导致发布失败
- 审核延迟被误判为失败

## Validation Summary
- `clawhub whoami` 有效；
- `ls -R` 目录含 SKILL.md 与 references/DESCRIPTION.md；
- dry-run 退出码 0；
- publish 成功；
- `clawhub search <slug>` 命中或处于审核队列。

## Suggested Skill Name
process-to-ingest
