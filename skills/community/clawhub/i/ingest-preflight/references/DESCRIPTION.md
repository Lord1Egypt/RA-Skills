# ingest-preflight — 资源说明

- **内容来源**：本次 OpenClaw 会话中原创编写，作为"业务流程处理 → 数字资源入库"协作链路的真实入库样本。
- **用途**：在执行 `clawhub publish` 之前，对已打包的 skill 目录做结构、元数据、体积、登录态、slug 唯一性与 dry-run 的一站式预检。
- **处理方（上游）**：OpenClaw 工作空间 + TaskFlow 风格流程处理（审核 → 元数据填充 → 打包）。
- **入库目标（下游）**：ClawHub 资源中心（skill 发布仓库），通过 `clawhub publish` 完成。
- **可执行入口**：`scripts/preflight.sh <skill-folder> [--slug <slug>]`
- **退出约定**：0 = 可发布；1 = 需先修复列出的失败项；2 = 参数错误。
