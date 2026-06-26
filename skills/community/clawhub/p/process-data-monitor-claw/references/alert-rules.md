# 告警规则模板

开箱即用的告警规则配置模板，覆盖常见监控场景。

## 1. 阈值告警

单指标超出范围时触发。

### 示例：库存低于安全线

```yaml
rules:
  - name: "库存不足告警"
    metric: "SELECT COUNT(*) FROM products WHERE stock < safety_stock"
    operator: "gt"
    threshold: 0
    alert_level: "warning"
    message: "当前有 {count} 个商品库存低于安全线"
    cooldown: 1800  # 30分钟内不重复告警
```

### 示例：支付成功率低于阈值

```yaml
rules:
  - name: "支付成功率异常"
    metric: |
      SELECT 
        ROUND(SUM(CASE WHEN status='success' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) as rate
      FROM payments 
      WHERE created_at > NOW() - INTERVAL 5 MINUTE
    operator: "lt"
    threshold: 95
    alert_level: "urgent"
    message: "支付成功率 {value}%，低于 95% 阈值"
    cooldown: 300
```

## 2. 趋势告警

指标持续恶化时触发。

### 示例：转化率连续下降

```yaml
rules:
  - name: "转化率持续下降"
    metric: |
      SELECT 
        DATE(created_at) as date,
        COUNT(CASE WHEN status='paid' THEN 1 END) * 100.0 / COUNT(*) as rate
      FROM orders
      WHERE created_at > NOW() - INTERVAL 3 DAY
      GROUP BY DATE(created_at)
      ORDER BY date DESC
      LIMIT 3
    operator: "trend_down"  # 自定义操作符，需在监控脚本中实现
    threshold: 3  # 连续3天下降
    alert_level: "warning"
    message: "转化率连续 {days} 天下降，当前 {value}%"
    cooldown: 86400  # 24小时内不重复告警
```

## 3. 关联告警

多指标联动异常时触发。

### 示例：流量暴增但转化率骤降

```yaml
rules:
  - name: "流量转化异常"
    metric: |
      SELECT 
        COUNT(*) as pv,
        COUNT(CASE WHEN status='paid' THEN 1 END) * 100.0 / COUNT(*) as rate
      FROM page_views pv
      LEFT JOIN orders o ON pv.user_id = o.user_id AND o.created_at > pv.created_at
      WHERE pv.created_at > NOW() - INTERVAL 5 MINUTE
    conditions:
      - field: "pv"
        operator: "gt"
        threshold: 10000  # 流量 > 10000
      - field: "rate"
        operator: "lt"
        threshold: 1  # 转化率 < 1%
    alert_level: "urgent"
    message: "流量 {pv} 但转化率仅 {rate}%，疑似异常流量或系统故障"
    cooldown: 300
```

## 4. 时间窗口告警

特定时段异常时触发。

### 示例：夜间订单量异常

```yaml
rules:
  - name: "夜间订单异常"
    metric: "SELECT COUNT(*) FROM orders WHERE created_at > NOW() - INTERVAL 1 HOUR"
    operator: "gt"
    threshold: 100
    alert_level: "warning"
    message: "夜间（23:00-06:00）订单量 {count}，超过正常范围"
    time_window:
      start: "23:00"
      end: "06:00"
    cooldown: 3600
```

## 5. 状态监控告警

流程卡顿或任务失败时触发。

### 示例：订单超时未发货

```yaml
rules:
  - name: "订单发货超时"
    metric: |
      SELECT COUNT(*) 
      FROM orders 
      WHERE status='paid' 
        AND created_at < NOW() - INTERVAL 24 HOUR
        AND shipped_at IS NULL
    operator: "gt"
    threshold: 0
    alert_level: "urgent"
    message: "当前有 {count} 个订单超过24小时未发货"
    cooldown: 300
```

### 示例：ETL 任务失败

```yaml
rules:
  - name: "ETL任务失败"
    metric: "SELECT COUNT(*) FROM etl_jobs WHERE status='failed' AND updated_at > NOW() - INTERVAL 10 MINUTE"
    operator: "gt"
    threshold: 0
    alert_level: "urgent"
    message: "ETL任务失败：{count} 个任务执行失败"
    cooldown: 600
```

## 6. 数据质量告警

数据异常或缺失时触发。

### 示例：数据量突增突降

```yaml
rules:
  - name: "数据量异常"
    metric: |
      SELECT 
        COUNT(*) as current_count,
        (SELECT AVG(cnt) FROM (
          SELECT COUNT(*) as cnt 
          FROM orders 
          WHERE created_at > NOW() - INTERVAL 7 DAY 
          GROUP BY DATE(created_at)
        ) t) as avg_count
      FROM orders 
      WHERE created_at > NOW() - INTERVAL 1 HOUR
    conditions:
      - field: "current_count"
        operator: "gt"
        threshold_expr: "avg_count * 2"  # 超过均值2倍
      - field: "current_count"
        operator: "lt"
        threshold_expr: "avg_count * 0.5"  # 低于均值50%
    alert_level: "warning"
    message: "数据量异常：当前 {current_count}，历史均值 {avg_count}"
    cooldown: 1800
```

## 配置说明

### 操作符（operator）

- `gt` — 大于
- `lt` — 小于
- `eq` — 等于
- `ne` — 不等于
- `gte` — 大于等于
- `lte` — 小于等于

### 告警级别（alert_level）

- `urgent` — 紧急，飞书群消息 + 私信
- `warning` — 重要，飞书私信
- `info` — 一般，飞书群消息

### 降噪间隔（cooldown）

单位：秒。相同规则在 cooldown 秒内只触发一次告警，避免告警风暴。

### 消息模板变量

- `{value}` — 指标值
- `{count}` — 计数值
- `{threshold}` — 阈值
- 自定义字段名（如 `{pv}`, `{rate}`）
