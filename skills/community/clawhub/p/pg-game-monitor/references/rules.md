# Prometheus 告警规则说明

## 规则文件位置

- 监控服务器规则：`/opt/monitor/prometheus/rules.yml`
- 参考文件：`/root/rules.yml`

## JVM 告警规则

### JVMHeapUsageHigh
```yaml
- alert: JVMHeapUsageHigh
  expr: (heap_used_bytes / clamp_min(heap_committed_bytes, 1)) > 0.85
    and (time() - jvm_start_time_seconds > 3600)
  for: 5m
  labels:
    severity: warning
  annotations:
    summary: "堆内存高"
    description: "{{ $labels.hostname }} {{ $labels.game_dir }} 堆内存使用率过高"
    value: "{{ $value }}"
```
**说明**：`jvm_start_time > 3600` 用于过滤刚启动的 JVM（预热期堆内存本身就会高）。超过 85% 持续 5 分钟触发 warning。

### JVMGcPressureWarning
```yaml
- alert: JVMGcPressureWarning
  expr: gc_time_seconds / 60 > 0.3
  for: 3m
  labels:
    severity: warning
```
**说明**：GC 时间占采集周期（60秒）的比例，超过 30% 持续 3 分钟。

### JVMGcPressureCritical
```yaml
- alert: JVMGcPressureCritical
  expr: gc_time_seconds / 60 > 0.6
  for: 2m
  labels:
    severity: critical
```
**说明**：GC 时间超过 60 秒周期的 60%，即 36 秒。

## MySQL 告警规则

### MySQLDown
```yaml
- alert: MySQLDown
  expr: mysql_up == 0
  for: 2m
  labels:
    severity: critical
```
**说明**：MySQL 连接失败持续 2 分钟。

### MySQLBufferPoolHigh
```yaml
- alert: MySQLBufferPoolHigh
  expr: (innodb_buffer_pool_bytes_data / clamp_min(innodb_buffer_pool_bytes_total, 1)) > 0.85
  for: 5m
  labels:
    severity: warning
```
**说明**：InnoDB Buffer Pool 使用率超过 85%。

### MySQLMemoryHigh
```yaml
- alert: MySQLMemoryHigh
  expr: mysql_process_resident_memory_bytes > 8589934592
  for: 5m
  labels:
    severity: warning
```
**说明**：MySQL 进程 RSS 超过 8GB。

## 注释掉的规则

以下规则在当前 `rules.yml` 中被注释，原因是预热期误报或需求不明确：

- `JVMOldGenHigh`：老年代使用率 > 80%（JVM 预热期正常）
- `JVMProcessDown`：JVM 掉线（游戏服重启较频繁，暂时关闭）

如需启用，取消注释即可。

## 告警级别

| severity | 说明 | 接收的 Webhook |
|----------|------|---------------|
| critical | 严重故障（服务下线） | `http://<webhook>:5000/webhook?level=critical` |
| warning | 性能告警（资源紧张） | `http://<webhook>:5000/webhook?level=warning` |
| （默认） | 普通通知 | `http://<webhook>:5000/webhook` |

## 自定义阈值

修改 `/opt/monitor/prometheus/rules.yml` 后重载：
```bash
curl -X POST http://<prometheus-host>:9090/-/reload
```
