# workflow-handoff — 数字内容入库到 ClawHub 资源中心

> 本文件由「业务流程处理工具（TaskFlow 式工作空间编排）」生成，是流程梳理阶段的结构化交接物，
> 也是后续「数字资源入库工具（clawhub CLI）」的直接输入。

## 目标（Objective）
把一份工作空间内已经处理好的数字内容，打包成符合 ClawHub skill 规范的文件夹，
并通过 `clawhub` CLI 发布到 ClawHub 资源中心，使其可被检索、可被安装。

## 适用场景
- 需要把一次性产物沉淀成可复用、可检索的资源条目；
- 需要演示/固化「先把模糊需求跑成可执行步骤，再把成果入库」的协作链路；
- 作者从零开始做一个最小可用的 skill 包。

## 前置条件（Preconditions）
- 已安装 OpenClaw 且工作空间可读写；
- `clawhub` CLI 可用（`clawhub --help` 正常）；
- 已登录：`clawhub whoami` 返回有效身份；
- 待入库内容已就绪，并已确认 slug 在 ClawHub 全局唯一。

## 结构化步骤（Steps）

| # | 步骤 | 输入 | 输出 | 职责 | 风险 | 校验 |
|---|------|------|------|------|------|------|
| 1 | 澄清目标与范围 | 模糊需求/素材 | 一句话目标 | 明确“入库什么、发到哪” | 范围漂移 | 目标可一句话复述 |
| 2 | 提取步骤骨架 | 目标 | 有序步骤列表 | 列出处理→入库主干 | 漏步 | 主干无断链 |
| 3 | 逐层钻取每步 | 步骤骨架 | 每步的输入/输出/职责/风险/校验/规则 | 补全可执行细节 | 细节缺失 | 每步六项齐全 |
| 4 | 本地打包 | 上游产物 | skill 形文件夹（SKILL.md + references/） | 按规范落盘 | 缺 SKILL.md 或结构错 | `ls -R` 结构正确 |
| 5 | dry-run 预览 | skill 文件夹 | 预览结果 | 校验元数据与结构 | 提前发布出错误 | dry-run 无报错 |
| 6 | 正式发布 | dry-run 通过的文件夹 | 资源中心条目 | `clawhub skill publish` | slug 冲突/未登录 | 命令返回成功 |
| 7 | 验证入库 | 发布返回 | 可检索条目 | `clawhub search` | 审核延迟 | 搜索命中 |

## 关键规则（Rules）
- 不跳步：必须先完成流程梳理与本地打包，再发布。
-dry-run 先行：正式发布前必须 `--dry-run`。
- slug 全局唯一：发布前用 `clawhub inspect <slug>` 确认未占用。
- 最小包结构：必须含 `SKILL.md`（frontmatter + 正文），支撑材料放 `references/`。
- 登录有效：发布前 `clawhub whoami` 必须返回身份。

## 关键风险（Risks）
- 未登录或 token 过期 → 发布失败；先 `whoami`。
- slug 撞名 → 冲突报错；换名或确认属主。
- 新发布需审核 → 搜索有短暂延迟，属正常。
- DESCRIPTION.md 质量低 → 入库后检索价值低；它是上游梳理的直接产物。

## 校验总结（Validation）
- 本地结构：`ls -R <folder>` 显示 `SKILL.md` 与 `references/`。
- 发布前：`clawhub skill publish --dry-run <folder> ...` 通过。
- 发布后：`clawhub search <slug>` 命中该条目。
