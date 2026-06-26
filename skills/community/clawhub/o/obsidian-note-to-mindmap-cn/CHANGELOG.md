# 更新日志

该文件记录 `obsidian-note-to-mindmap-cn` 的对外可见变更。

## 0.1.0 - 2026-04-22

### 新增

- 发布 `obsidian-note-to-mindmap-cn` 的首个公开 wrapper 版本。
- 提供面向中文 Obsidian 工作流的轻量入口，并将实际导图转换委托给已审核 core skill `suka233/kmind-markdown-to-mindmap`。
- 提供首次安装前必须征求确认的明确规则。
- 收紧安全边界：不扫描 vault、不隐藏安装、不改写笔记。

### 说明

- 首次安装 core skill 需要 `clawhub` CLI 与网络连接。
- 实际导图生成的运行时要求由已审核 core skill 定义。
