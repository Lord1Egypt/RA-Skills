# 更新日志

该文件记录 `kmind-markdown-to-mindmap-cn` skill 的对外可见变更。

## 0.1.1 - 2026-05-18

### 变更

- 明确推荐输入为 Markdown 标题大纲。
- 说明非标题正文会转换为节点备注。
- 推荐普通图片需求默认导出 PNG。
- 对齐卡片式节点正文布局，说明导出图片中备注以备注图标展示。

## 0.1.0 - 2026-04-04

### 新增

- 发布 `kmind-markdown-to-mindmap-cn` 的首个公开版本。
- 支持将 Markdown 大纲或纯文本离线转换为 KMind 导图。
- 支持导出 `SVG`、`PNG` 和可继续编辑的 `.kmindz.svg`。
- 提供适合 agent 使用的安全布局、连线和主题参数集合。
- 打包 `scripts/vendor/` 运行时。
- 提供中文导向的 `SKILL.md` 和 `agents/openai.yaml`。

### 说明

- 自动 `SVG` / `PNG` 导出依赖本机可用的 Chromium 浏览器。
- `.kmindz.svg` 导出不依赖浏览器渲染。
