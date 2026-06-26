---
name: process-data-monitor-claw
description: |
  过程数据监控虾 — 实时监控业务运行中的全链路数据状态，像雷达一样扫描业务流程每个节点，第一时间发现异常并告警。

  **当以下情况时使用此 Skill**：
  (1) 需要监控业务流程节点状态（订单履约、库存同步、支付链路、数据管道等）
  (2) 需要设置数据异常阈值告警（数值超限、状态卡顿、趋势恶化）
  (3) 需要配置多渠道告警推送（飞书群/私信、邮件、短信）
  (4) 需要生成监控报告（日报/周报，异常汇总、响应时效）
  (5) 用户提到"监控"、"实时监控"、"链路追踪"、"异常检测"、"告警"、"预警"、"数据状态"、"流程监控"、"业务监控"、"全链路"、"节点状态"

  **典型触发示例**：
  - "帮我监控订单履约流程，超过24小时未发货就告警"
  - "实时监控库存同步状态，发现差异立即通知"
  - "监控支付成功率，低于95%立即预警"
  - "设置数据管道监控，ETL任务失败立即告警"
---

# 过程数据监控虾

业务流程的"哨兵"，负责发现问题并及时预警。

## 工作流程

**Step 1 — 定义监控对象**：明确监控的流程节点、数据指标、业务对象（订单状态、库存数量、支付成功率、任务执行状态等）。

**Step 2 — 设置监控规则**：为每个监控对象配置正常范围、异常阈值、检查频率、告警级别。参考 `references/alert-rules.md` 中的规则模板。

**Step 3 — 数据采集方式**：根据数据源类型选择采集方式，参考 `references/data-sources.md`：
- 数据库轮询（MySQL/PostgreSQL/MongoDB）
- API 接口调用（REST/GraphQL）
- 消息队列监听（Kafka/RabbitMQ）
- 日志文件解析

**Step 4 — 异常检测**：将实时数据与规则对比，识别数值异常、状态异常、趋势异常、关联异常。

**Step 5 — 告警推送**：根据告警级别推送，使用 `scripts/alert-sender.sh`：
- 紧急（urgent）：飞书群消息 + 私信
- 重要（warning）：飞书私信
- 一般（info）：飞书群消息

**Step 6 — 生成报告**：定期汇总异常事件、响应时效、改进建议。

## 监控配置格式

用户提供自然语言需求时，将其转化为标准配置结构：

```yaml
monitor_name: "监控任务名称"
check_interval: 300  # 秒，默认5分钟
data_source:
  type: "mysql"  # mysql/postgresql/api/log
  connection: "..."
rules:
  - name: "规则名称"
    metric: "指标名或SQL查询"
    operator: "gt"  # gt/lt/eq/ne/gte/lte
    threshold: 0
    alert_level: "urgent"  # urgent/warning/info
    message: "告警消息模板，支持 {value} {count} 等变量"
    cooldown: 300  # 告警降噪间隔（秒），默认5分钟
notify:
  feishu_webhook: "https://open.feishu.cn/open-apis/bot/v2/hook/..."
  feishu_users: []  # open_id 列表，用于私信
```

## 关键设计原则

- **告警降噪**：相同问题 `cooldown` 秒内只告警一次，避免告警风暴
- **可追溯性**：所有告警记录写入日志，支持回溯分析
- **自适应阈值**：建议根据历史数据定期调整阈值，减少误报

## References

- `references/metrics-library.md` — 常见业务场景预定义监控指标体系（电商/SaaS/营销）
- `references/alert-rules.md` — 告警规则配置模板（阈值/趋势/关联/时间窗口）
- `references/data-sources.md` — 各类数据源接入指南

## Scripts

- `scripts/monitor-daemon.sh` — 监控守护进程（start/stop/status/reload）
- `scripts/alert-sender.sh` — 多渠道告警推送（飞书 Webhook）
