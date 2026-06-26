# 监控架构规划

适用于使用 Prometheus + Grafana 监控 Java 游戏服 JVM 运行时和 MySQL 的场景。

## 当前架构（测试阶段）

**监控服务器配置**：8C16G + 500G 数据盘

**All-in-One 部署**：
```
Pushgateway  : 9091
Prometheus   : 9090
Alertmanager : 9093
Grafana      : 3000
飞书Webhook  : 5000
```

**数据流向**：
```
游戏服 (game_agent.py)
    ↓ push (每60秒)
Pushgateway (:9091)
    ↓ scrape (每60秒)
Prometheus (:9090)
    ↓ alert
Alertmanager (:9093)
    ↓ webhook
飞书Webhook (:5000)
    ↓ HTTP POST
飞书机器人
```

## 扩展路线图

### Phase 1: 测试验证（当前）
- All-in-One 部署
- 覆盖 1-2 个游戏项目
- 验证指标采集、告警、通知链路

### Phase 2: 生产小规模
- Pushgateway 独立部署（抗住 100-200 台游戏服务器）
- Prometheus 保留单实例
- 按项目划分 Dashboard 和告警规则

### Phase 3: 生产大规模
- 多个 Pushgateway 实例（Nginx 负载均衡）
- Prometheus Federation（按机房/项目拆分）
- 考虑 VictoriaMetrics 或 Thanos 长期方案

### Phase 4: 海外扩展
- 海外游戏服单独部署 Pushgateway + Prometheus
- Global Prometheus Federation
- 告警聚合统一到中央 Alertmanager

## 与现有 Zabbix 的关系

| 层面 | 工具 | 说明 |
|------|------|------|
| 主机/OS（CPU/内存/磁盘/网络） | Zabbix | 已有，不重复 |
| JVM 运行时（堆/GC/线程） | Prometheus | **新** |
| MySQL 运行时（Buffer Pool/连接/查询） | Prometheus | **新** |
| 业务指标（在线人数/订单） | 业务自定义 Exporter | 后续扩展 |
| 告警 On-Call | 统一整合 | 未来规划 |

## 未来整合目标

### 告警 On-Call 统一
考虑开源方案：
- **AlertManager**: 现有方案，轻量
- **PagerDuty**: 商业方案，功能全
- **Prometheus AlertManager + WebHook**: 当前方案，够用
- **Zabbix + 告警 API**: 已有方案

### 可视化统一
Grafana 作为统一展示层：
- 数据源 = Prometheus（多个实例）
- 数据源 = Zabbix（通过 Zabbix Datasource Plugin）
- 数据源 = 其他存储（VictoriaMetrics/Mimir）

## 容量估算

| 游戏服规模 | Pushgateway | Prometheus | 预估存储（60d） |
|-----------|-------------|------------|----------------|
| 100 台 | 1 实例 | 1 实例 | ~50GB |
| 500 台 | 2 实例 + LB | 1 实例 + 远程存储 | ~250GB |
| 1000+ 台 | 3+ 实例 + LB | Federation | ~500GB+ |
