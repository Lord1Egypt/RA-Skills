# model-usage-monitor Skill

OpenClaw 模型使用监控与告警技能

## ⚠️ Security & Permissions Declaration

**This skill monitors log files and sends alerts. All operations are read-only except notifications:**

| Operation | Purpose | Scope |
|-----------|---------|-------|
| Read semantic router log (`semantic_check.log`) | Parse model usage statistics | Read-only, local file |
| Read OpenClaw logs | Detect usage anomalies | Read-only, local files |
| Send alert notifications via OpenClaw messaging | Notify user of cost spikes | Local OpenClaw API only |

**What this skill does NOT do:**
- Does NOT modify any configuration or log files
- Does NOT access external servers or APIs
- Does NOT access model credentials directly
- Does NOT require elevated privileges
- **Read-only monitoring** — zero side effects on system state

## 功能

- 解析语义路由日志，统计模型使用分布
- 估算各模型调用次数和成本
- 计算缓存命中率
- 每小时自动告警检查
- 支持实时监控模式

## 安装

```bash
# 技能已包含监控脚本和自动配置
# 安装后自动创建每小时检查的 Cron Job
```

## 使用

### 查看监控报告

```bash
# 完整报告
python3 ~/.openclaw/workspace/.lib/model_usage_monitor_v2.py

# JSON 格式
python3 ~/.openclaw/workspace/.lib/model_usage_monitor_v2.py --format json

# 仅检查告警
python3 ~/.openclaw/workspace/.lib/model_usage_monitor_v2.py --alert-check
```

### 实时监控

```bash
python3 ~/.openclaw/workspace/.lib/model_usage_monitor_v2.py --live
```

## 告警阈值

| 类型 | 阈值 | 说明 |
|------|------|------|
| Opus 调用频繁 | >5 次/小时 | 防止意外大量使用昂贵模型 |
| Opus 成本过高 | >$0.50/小时 | 成本控制 |
| 总成本过高 | >$2.00/小时 | 总体预算控制 |

## 文件结构

```
.skills/model-usage-monitor/
├── SKILL.md              # 本文件
├── monitor.py            # 核心监控脚本
├── setup.py              # 自动安装/配置
└── config.json           # 默认配置
```

## 技术细节

- 全部使用本地 Ollama 模型，零 API 调用
- 只读日志文件，零侵入
- 基于 semantic_check.log 和 gateway.log 分析
