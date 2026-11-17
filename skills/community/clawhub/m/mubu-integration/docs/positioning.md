# 定位纠偏建议（给主理人 / QA）

## 核心判断
当前 README 把 `save` 写回放在 Use Case ① 首位，但 `save` 需 `MUBU_MEMBER_ID`（服务端限制、采用率最低），与"幕布用户最想要的零配置备份 / 读取"错位。应把**零配置读取 / 备份 / 导出**作为首要叙事。

## 建议的 Use Case 新排序
1. **零配置备份与读取**：`export-tree` 整树导出、`get` 导出 Markdown、`list` / `search` 浏览——只需手机号 + 密码，无需 memberId。
2. **进 Obsidian / 给 AI 当长期记忆**：Markdown 往返保真，知识库可进 Obsidian，AI 可直接读。
3. **写回（power-user 选装）**：`save` 写回——明确前置 `MUBU_MEMBER_ID` 说明，放在靠后位置并加 ⚠️。

## 一句话 hero 标语
"零配置把幕布变成可被命令行与 AI 操控的 Markdown 大纲——备份、检索、写回，一条命令搞定。"

## 落地建议
- README Use Cases 三段按上述顺序重排；首段前置"只需手机号密码，无需 memberId"。
- Reliability 章节已含 Auto-refresh auth，可在首屏 hero 下方补一句"读取 / 备份 / 导出零配置"。
- `save` 写回相关示例保留，但统一加 memberId 前置说明（已在 Troubleshooting 表覆盖）。
