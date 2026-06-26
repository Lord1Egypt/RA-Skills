# Log To Alert

[English](./README.md)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
![版本](https://img.shields.io/badge/version-1.0-blue)

> 从服务器日志中提取错误模式并转换为结构化的告警规则 — 用于监控告警系统

## 解决什么问题

日志中的重复错误不断出现，但没人有时间手动创建告警规则。这个技能解析日志条目，识别错误/警告模式（≥3 次出现 = 重复），并输出可直接使用的告警规格，支持 Prometheus、Grafana 或 PagerDuty。

**触发条件：** 日志文本 + 告警/监控/创建规则意图。

## 功能特性

- **多格式日志解析** — 处理 JSON 日志、半结构化日志（Nginx/Apache）和纯文本日志
- **自动去重** — 将相同错误消息分组为一个规则，设置频率阈值
- **严重性分类** — ERROR/FATAL → critical，WARN → warning，INFO/DEBUG → 跳过
- **动态值提取** — 将硬编码的 IP、主机名、用户 ID 转换为正则变量

## 快速开始

```bash
# 通过 ClawHub 安装
clawhub install log-to-alert

# 或手动复制
cp -r log-to-alert ~/.openclaw/skills/
```

### 使用方法

```
/log-to-alert
```

粘贴日志，要求创建告警规则。

```
/log-to-alert/dedupe
```

将相似日志行分组为一个告警，消除重复。

## 工作模式

| 模式 | 说明 |
|------|------|
| `/log-to-alert` | 解析日志，输出告警规则（Prometheus、Grafana 等） |
| `/log-to-alert/dedupe` | 将相似错误分组为一个规则，设置阈值 |

## 示例

| 场景 | 输出 |
|------|------|
| 500 条相同错误 | 1 条告警规则 `threshold: 3`——不是 500 条单独告警 |
| 动态错误："user 123 not found" | 模式：`user \d+ not found`（不是字面字符串） |
| 日志中多个服务 | 按服务命名告警：`auth-DB-connection-failed` |
| 一条 INFO 日志 | 跳过——INFO 级别不值得告警 |

## 目录结构

```
log-to-alert/
├── SKILL.md
├── LICENSE
├── README.md
├── README_zh.md
├── CONTRIBUTING.md
├── .gitignore
├── references/       # 正则提取模式、告警格式 schema
└── tests/
```

## 许可证

MIT 许可证 — 详见 [LICENSE](LICENSE)。