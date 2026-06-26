# Message Chunker Skill

智能消息分段工具，自动将长消息拆分成多条发送。

## 安装

将此目录复制到 OpenClaw 的 skills 目录：

```bash
cp -r message-chunker ~/.openclaw/workspace/skills/
```

或使用 OpenClaw CLI：

```bash
openclaw skill install message-chunker.tar.gz
```

## 功能

- 自动检测消息长度
- 智能分段（按章节、表格、段落）
- 多平台适配（飞书、Telegram、Discord等）
- 手动分段标记支持

## 配置

在 `TOOLS.md` 中添加：

```yaml
message-chunker:
  maxChunkSize: 4000
  splitOnHeadings: true
  splitOnTables: true
```

## 版本

- v1.0.0 - 2026-03-10 - 初始版本

## 作者

01-老鹰 (孔明)
