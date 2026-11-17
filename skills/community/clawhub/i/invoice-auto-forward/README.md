# invoice-auto-forward

> 自动扫描邮箱发票邮件，解析发票（PDF / OFD / XML 三种格式）后按模板转发给指定收件人（财务/行政），支持抬头白名单过滤、链接型发票自动下载与定时无人值守运行。

## Features

- **全自动发票转发**：IMAP 扫描 + 发票解析 + SMTP 转发，一次配置永久运行
- **三种发票格式**：PDF / OFD / XML 全支持；OFD、XML 用 Python 内置库解析，零额外依赖
- **链接型发票**：邮件无附件时自动扫描正文链接下载发票（如腾讯云电子发票），仅接受确为发票格式的响应
- **一键配置**：`setup` 子命令收集全部配置 + 验证 IMAP/SMTP 连通后才落盘（授权码 chmod 600 隔离存储）
- **智能去重**：按 Message-ID + 发票号双重去重，重复执行不重复转发
- **抬头白名单**：可按购买方抬头过滤，只转发匹配的发票
- **干跑预览**：`scan` 模式预览将发送清单，确认后再 `run`
- **定时无人值守**：支持 crontab / agent automation 定时执行；发送节奏控制（interval/jitter/batch_limit）防反垃圾风控
- **多邮箱支持**：QQ / Foxmail / 163 / 126 / Yeah provider 预设一键切换（163/126 已适配网易 IMAP ID 要求）

## Quick Start

```bash
# Install (clawhub)
clawhub install invoice-auto-forward

# Or clone directly
git clone https://github.com/Songhonglei/better-office-work-flow.git
```

## Usage

详细使用方法见 [SKILL.md](./SKILL.md)。

## Install in your AI agent

| Agent | Install |
|---|---|
| OpenClaw | `clawhub install invoice-auto-forward` |
| Claude Code | Manual: copy to `~/.claude/skills/` |
| Cursor | Manual: copy to `.cursor/skills/` |

## License

MIT (see [LICENSE](../../LICENSE))

## Author

Evan Song · [github.com/Songhonglei](https://github.com/Songhonglei)

## Changelog

See [CHANGELOG.md](./CHANGELOG.md) for the full version history.
