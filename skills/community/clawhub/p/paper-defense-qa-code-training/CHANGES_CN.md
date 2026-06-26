# 更新记录

## v1.1.0

- 补充 Codex / CLI 生图交接规则：在 Codex 内实际生图时优先调用 `imagegen` skill；非 Codex 场景再使用 ChatGPT Images 2.0 / `gpt-image-2` 或用户批准的高级文生图 API。
- 同步 ClawHub 发布版本到 `1.1.0`，继续使用 MIT-0 / MIT No Attribution 许可证。

## v1.0.0

- 初始发布版本，面向计算机类论文答辩、审稿式追问、代码审计与训练过程追问。
- 包含论文主张-证据映射、paper attack surface、code/training attack surface、defense Q&A bank、mock defense script、backup slide plan、evidence gap triage。
- 加入图文答辩卡片 / Visual Q&A Storyboard 功能，可把高风险问题与回答转换为 16:9 辅助答辩插图的 storyboard 和 prompt pack。
- 保留“先文字、后生图”的工作流：先输出问题、回答、证据边界与提示词；只有用户后续单独请求时才进入生图。
- 最终生图提示语统一为：`请用chatgpt images 2.0 生成一系列 16:9 辅助答辩的插图，这些插图可以图文并茂的覆盖上面文字中的问题以及用生动的图表来解释回答，有助于更好准备答辩回答。`
- ClawHub 打包兼容：包含 `SKILL.md` frontmatter、`_meta.json`、`LICENSE`（MIT-0 / MIT No Attribution）、验证脚本与打包脚本。
