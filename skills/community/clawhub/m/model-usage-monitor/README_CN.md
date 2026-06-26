# 模型用量监控

[![版本](https://img.shields.io/badge/version-1.0.1-blue)](https://clawhub.ai)
[![许可证](https://img.shields.io/badge/license-MIT--0-green)](https://spdx.org/licenses/MIT-0.html)

> **OpenClaw 模型使用监控与告警技能**

监控并统计 AI 模型调用次数和成本，计算缓存命中率，支持实时监控与每小时自动告警。

## ⚠️ 安全与权限声明

**本技能对本地日志文件执行只读监控：**

| 操作 | 目的 | 范围 |
|------|------|------|
| 读取 `semantic_check.log` | 解析模型使用统计 | 只读，本地文件 |
| 读取 OpenClaw 网关日志 | 检测使用异常 | 只读，本地文件 |
| 发送告警通知 | 通知用户成本峰值 | 仅本地 OpenClaw API |
| 创建 Cron Job（可选） | 每小时自动检查 | 仅本地 Cron |

**本技能不会做什么：**
- 不会修改任何配置或日志文件
- 不会访问外部服务器或 API
- 不使用加密或混淆代码
- 不需要付费或授权
- 不访问模型凭证
- **完全透明** — 所有源代码均可读

## 功能

- 解析语义路由日志，统计模型使用分布
- 估算各模型调用次数和成本
- 计算缓存命中率
- 每小时自动告警检查
- 支持实时监控模式

## 安装

```bash
# 技能包含监控脚本和自动配置
bash ~/.openclaw/workspace/skills/model-usage-monitor/install.sh
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
├── README.md           # 本文件（英文）
├── README_CN.md        # 本文件（中文）
├── SKILL.md            # 技能文档
├── install.sh          # 透明安装脚本
├── monitor.py          # 核心监控脚本
├── setup.py            # 自动安装/配置
└── config.json         # 默认配置
```

## 技术细节

- 仅使用本地文件操作
- 只读日志分析 — 零系统影响
- 基于 semantic_check.log 和 gateway.log 分析
- 无外部网络调用
- 无加密或混淆代码

## 📄 许可证

MIT-0 — 可自由使用、修改和分发。无需署名。

---

**维护者**: halfmoon82  
**最后更新**: 2026-03-12
