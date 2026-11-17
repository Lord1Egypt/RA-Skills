# 数字内容入库到 ClawHub 资源中心 — 流程交接摘要

- 内容来源：本工作空间内由「业务流程处理工具（TaskFlow 式编排）」梳理生成
- 用途示例：演示并固化「先把需求跑成可执行步骤，再把成果入库到可检索仓库」的协作链路
- 处理方：OpenClaw 工作空间流程（上游）
- 入库目标：ClawHub 资源中心（skill 发布仓库）

## 摘要
目标：把工作空间内处理好的数字内容打包为 ClawHub skill 形文件夹，经 `clawhub skill publish`
发布并可被检索。

主干步骤：澄清目标 → 提取骨架 → 逐层钻取（输入/输出/职责/风险/校验/规则）→ 本地打包
→ dry-run 预览 → 正式发布 → `clawhub search` 验证。

关键规则：不跳步；dry-run 先行；slug 全局唯一；发布前确认 `clawhub whoami`；
最小包必须含 `SKILL.md`（frontmatter+正文），支撑材料放 `references/`。

主要风险：未登录/token 过期、slug 撞名、新发布需审核导致搜索短暂延迟、DESCRIPTION 质量影响检索价值。

完整可复现步骤见本包 `SKILL.md` 内的操作说明；上游完整梳理见 `workflow-handoff.md`。
