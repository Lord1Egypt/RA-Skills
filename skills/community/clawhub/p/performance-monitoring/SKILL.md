# Performance Monitoring Skill

**版本**: v1.0
**创建日期**: 2026-03-26
**作者**: 象腿 (main agent)
**用途**: 监控Agent性能，收集关键指标，优化系统表现

---

## 🎯 核心功能

Performance Monitoring skill负责：
1. **指标收集**: 收集调度、执行、性能等关键指标
2. **数据记录**: 将指标记录到日志和飞书表格
3. **趋势分析**: 分析性能趋势，识别瓶颈
4. **告警机制**: 性能异常时自动告警
5. **优化建议**: 基于数据提供优化建议

---

## 📋 监控指标体系

### 1. Agent调度指标

#### 1.1 调度成功率 (Dispatch Success Rate)

**定义**: 成功调度的任务数 / 总调度任务数

**目标**: >95%

**计算**:
```python
def calculate_dispatch_success_rate(dispatch_logs):
    """
    计算调度成功率

    Args:
        dispatch_logs: 调度日志列表

    Returns:
        float: 成功率 (0.0-1.0)
    """
    total = len(dispatch_logs)
    if total == 0:
        return 1.0

    success = sum(1 for log in dispatch_logs if log['success'])
    return success / total
```

**记录格式**:
```json
{
  "timestamp": "2026-03-26T12:00:00+08:00",
  "metric": "dispatch_success_rate",
  "value": 0.95,
  "total": 100,
  "success": 95,
  "failed": 5
}
```

---

#### 1.2 平均调度耗时 (Avg Dispatch Time)

**定义**: 从收到请求到agent开始执行的平均时间

**目标**: <5秒

**计算**:
```python
def calculate_avg_dispatch_time(dispatch_logs):
    """
    计算平均调度耗时

    Args:
        dispatch_logs: 调度日志列表

    Returns:
        float: 平均耗时（秒）
    """
    times = [log['dispatch_time'] for log in dispatch_logs if 'dispatch_time' in log]

    if not times:
        return 0.0

    return sum(times) / len(times)
```

**记录格式**:
```json
{
  "timestamp": "2026-03-26T12:00:00+08:00",
  "metric": "avg_dispatch_time",
  "value": 3.45,
  "unit": "seconds",
  "min": 1.2,
  "max": 8.5,
  "p50": 3.2,
  "p95": 6.8
}
```

---

#### 1.3 重试率 (Retry Rate)

**定义**: 需要重试的任务数 / 总调度任务数

**目标**: <10%

**计算**:
```python
def calculate_retry_rate(dispatch_logs):
    """
    计算重试率

    Args:
        dispatch_logs: 调度日志列表

    Returns:
        float: 重试率 (0.0-1.0)
    """
    total = len(dispatch_logs)
    if total == 0:
        return 0.0

    retried = sum(1 for log in dispatch_logs if log.get('retry_count', 0) > 0)
    return retried / total
```

**记录格式**:
```json
{
  "timestamp": "2026-03-26T12:00:00+08:00",
  "metric": "retry_rate",
  "value": 0.08,
  "total": 100,
  "retried": 8
}
```

---

#### 1.4 Fallback率 (Fallback Rate)

**定义**: Fallback到main agent的任务数 / 总调度任务数

**目标**: <5%

**计算**:
```python
def calculate_fallback_rate(dispatch_logs):
    """
    计算fallback率

    Args:
        dispatch_logs: 调度日志列表

    Returns:
        float: fallback率 (0.0-1.0)
    """
    total = len(dispatch_logs)
    if total == 0:
        return 0.0

    fallback = sum(1 for log in dispatch_logs if log.get('fallback', False))
    return fallback / total
```

**记录格式**:
```json
{
  "timestamp": "2026-03-26T12:00:00+08:00",
  "metric": "fallback_rate",
  "value": 0.03,
  "total": 100,
  "fallback": 3
}
```

---

### 2. 并行处理指标

#### 2.1 并行加速比 (Parallel Speedup)

**定义**: 串行总时间 / 并行总时间

**目标**: >1.3x

**计算**:
```python
def calculate_parallel_speedup(serial_time, parallel_time):
    """
    计算并行加速比

    Args:
        serial_time: 串行执行时间（秒）
        parallel_time: 并行执行时间（秒）

    Returns:
        float: 加速比
    """
    if parallel_time == 0:
        return 1.0

    return serial_time / parallel_time
```

**记录格式**:
```json
{
  "timestamp": "2026-03-26T12:00:00+08:00",
  "metric": "parallel_speedup",
  "value": 1.5,
  "serial_time": 30.0,
  "parallel_time": 20.0
}
```

---

#### 2.2 任务完成率 (Task Completion Rate)

**定义**: 成功完成的任务数 / 总任务数

**目标**: >95%

**计算**:
```python
def calculate_task_completion_rate(task_logs):
    """
    计算任务完成率

    Args:
        task_logs: 任务日志列表

    Returns:
        float: 完成率 (0.0-1.0)
    """
    total = len(task_logs)
    if total == 0:
        return 1.0

    completed = sum(1 for log in task_logs if log['success'])
    return completed / total
```

**记录格式**:
```json
{
  "timestamp": "2026-03-26T12:00:00+08:00",
  "metric": "task_completion_rate",
  "value": 0.97,
  "total": 100,
  "completed": 97,
  "failed": 3
}
```

---

### 3. Memory指标

#### 3.1 Memory数量 (Memory Count)

**定义**: 当前memory总数量

**目标**: <=200

**计算**:
```python
def calculate_memory_count(memories):
    """
    计算memory数量

    Args:
        memories: 记忆列表

    Returns:
        int: memory数量
    """
    return len(memories)
```

**记录格式**:
```json
{
  "timestamp": "2026-03-26T12:00:00+08:00",
  "metric": "memory_count",
  "value": 180,
  "window": 200,
  "utilization": 0.9
}
```

---

#### 3.2 平均相关度 (Avg Relevance Score)

**定义**: 所有memory的平均相关度分数

**目标**: >0.7

**计算**:
```python
def calculate_avg_relevance_score(memories):
    """
    计算平均相关度分数

    Args:
        memories: 记忆列表

    Returns:
        float: 平均相关度分数
    """
    if not memories:
        return 0.0

    scores = [m.get('relevance_score', 0.5) for m in memories]
    return sum(scores) / len(scores)
```

**记录格式**:
```json
{
  "timestamp": "2026-03-26T12:00:00+08:00",
  "metric": "avg_relevance_score",
  "value": 0.75,
  "min": 0.3,
  "max": 0.98,
  "distribution": {
    "high": 120,
    "medium": 50,
    "low": 10
  }
}
```

---

#### 3.3 检索准确率 (Retrieval Accuracy)

**定义**: 相关结果数 / 总返回结果数

**目标**: >80%

**计算**:
```python
def calculate_retrieval_accuracy(retrieval_logs):
    """
    计算检索准确率

    Args:
        retrieval_logs: 检索日志列表

    Returns:
        float: 准确率 (0.0-1.0)
    """
    total_results = sum(log['total_results'] for log in retrieval_logs)
    if total_results == 0:
        return 1.0

    relevant_results = sum(log['relevant_results'] for log in retrieval_logs)
    return relevant_results / total_results
```

**记录格式**:
```json
{
  "timestamp": "2026-03-26T12:00:00+08:00",
  "metric": "retrieval_accuracy",
  "value": 0.85,
  "total_results": 100,
  "relevant_results": 85
}
```

---

#### 3.4 Token效率 (Token Efficiency)

**定义**: 保留价值 / 总token数

**目标**: >95%

**计算**:
```python
def calculate_token_efficiency(original_tokens, current_tokens):
    """
    计算Token效率

    Args:
        original_tokens: 原始token数
        current_tokens: 当前token数

    Returns:
        float: 效率 (0.0-1.0)
    """
    if original_tokens == 0:
        return 1.0

    return 1.0 - (current_tokens / original_tokens)
```

**记录格式**:
```json
{
  "timestamp": "2026-03-26T12:00:00+08:00",
  "metric": "token_efficiency",
  "value": 0.96,
  "original_tokens": 100000,
  "current_tokens": 4000,
  "saved_tokens": 96000
}
```

---

## 🛠️ PowerShell实现

### 指标收集器

```powershell
# 指标收集器
function Collect-PerformanceMetrics {
    param(
        [string]$LogDir = "C:\Users\Administrator\.openclaw\workspace-main\logs",
        [string]$MetricsFile = "performance-metrics.json"
    )

    $metrics = @{}

    # 1. 收集调度指标
    $dispatchLogs = Get-DispatchLogs -LogDir $LogDir
    $metrics['dispatch_success_rate'] = Calculate-DispatchSuccessRate -Logs $dispatchLogs
    $metrics['avg_dispatch_time'] = Calculate-AvgDispatchTime -Logs $dispatchLogs
    $metrics['retry_rate'] = Calculate-RetryRate -Logs $dispatchLogs
    $metrics['fallback_rate'] = Calculate-FallbackRate -Logs $dispatchLogs

    # 2. 收集并行指标
    $parallelLogs = Get-ParallelLogs -LogDir $LogDir
    $metrics['parallel_speedup'] = Calculate-ParallelSpeedup -Logs $parallelLogs
    $metrics['task_completion_rate'] = Calculate-TaskCompletionRate -Logs $parallelLogs

    # 3. 收集memory指标
    $memories = Load-Memories
    $metrics['memory_count'] = Calculate-MemoryCount -Memories $memories
    $metrics['avg_relevance_score'] = Calculate-AvgRelevanceScore -Memories $memories
    $metrics['retrieval_accuracy'] = Calculate-RetrievalAccuracy -Logs (Get-RetrievalLogs -LogDir $LogDir)
    $metrics['token_efficiency'] = Calculate-TokenEfficiency -Memories $memories

    # 4. 添加时间戳
    $metrics['timestamp'] = (Get-Date).ToString("yyyy-MM-ddTHH:mm:ssK")

    # 5. 保存到文件
    $metricsJson = $metrics | ConvertTo-Json -Depth 10
    $metricsPath = Join-Path $LogDir $MetricsFile
    $metricsJson | Out-File -FilePath $metricsPath -Encoding UTF8

    return $metrics
}

# 获取调度日志
function Get-DispatchLogs {
    param([string]$LogDir)

    $logFile = Join-Path $LogDir "dispatch-*.log"
    if (Test-Path $logFile) {
        $logs = Get-Content $logFile | ConvertFrom-Json
        return $logs
    }

    return @()
}

# 计算调度成功率
function Calculate-DispatchSuccessRate {
    param([array]$Logs)

    $total = $Logs.Count
    if ($total -eq 0) {
        return @{value = 1.0; total = 0; success = 0; failed = 0}
    }

    $success = ($Logs | Where-Object { $_.success -eq $true }).Count

    return @{
        value = [math]::Round($success / $total, 2)
        total = $total
        success = $success
        failed = $total - $success
    }
}

# 计算平均调度耗时
function Calculate-AvgDispatchTime {
    param([array]$Logs)

    $times = $Logs | Where-Object { $_.dispatch_time } | ForEach-Object { $_.dispatch_time }

    if ($times.Count -eq 0) {
        return @{value = 0; unit = "seconds"}
    }

    $avg = ($times | Measure-Object -Average).Average

    return @{
        value = [math]::Round($avg, 2)
        unit = "seconds"
        min = [math]::Round(($times | Measure-Object -Minimum).Minimum, 2)
        max = [math]::Round(($times | Measure-Object -Maximum).Maximum, 2)
    }
}

# 计算重试率
function Calculate-RetryRate {
    param([array]$Logs)

    $total = $Logs.Count
    if ($total -eq 0) {
        return @{value = 0; total = 0; retried = 0}
    }

    $retried = ($Logs | Where-Object { $_.retry_count -gt 0 }).Count

    return @{
        value = [math]::Round($retried / $total, 2)
        total = $total
        retried = $retried
    }
}

# 计算fallback率
function Calculate-FallbackRate {
    param([array]$Logs)

    $total = $Logs.Count
    if ($total -eq 0) {
        return @{value = 0; total = 0; fallback = 0}
    }

    $fallback = ($Logs | Where-Object { $_.fallback -eq $true }).Count

    return @{
        value = [math]::Round($fallback / $total, 2)
        total = $total
        fallback = $fallback
    }
}
```

---

## 📊 数据记录

### 日志格式

所有指标记录到统一格式的日志文件：

```
logs/performance-metrics-YYYY-MM-DD.json
```

**格式**:
```json
{
  "date": "2026-03-26",
  "metrics": {
    "dispatch_success_rate": 0.95,
    "avg_dispatch_time": 3.45,
    "retry_rate": 0.08,
    "fallback_rate": 0.03,
    "parallel_speedup": 1.5,
    "task_completion_rate": 0.97,
    "memory_count": 180,
    "avg_relevance_score": 0.75,
    "retrieval_accuracy": 0.85,
    "token_efficiency": 0.96
  },
  "alerts": [
    {
      "metric": "dispatch_success_rate",
      "threshold": 0.95,
      "actual": 0.92,
      "severity": "warning"
    }
  ]
}
```

---

## 🚨 告警机制

### 告警规则

```python
def check_alerts(metrics):
    """
    检查指标是否触发告警

    Args:
        metrics: 指标字典

    Returns:
        list: 告警列表
    """
    alerts = []

    # 1. 调度成功率告警
    if metrics['dispatch_success_rate']['value'] < 0.95:
        alerts.append({
            'metric': 'dispatch_success_rate',
            'threshold': 0.95,
            'actual': metrics['dispatch_success_rate']['value'],
            'severity': 'warning' if metrics['dispatch_success_rate']['value'] > 0.9 else 'critical'
        })

    # 2. 平均调度耗时告警
    if metrics['avg_dispatch_time']['value'] > 5.0:
        alerts.append({
            'metric': 'avg_dispatch_time',
            'threshold': 5.0,
            'actual': metrics['avg_dispatch_time']['value'],
            'severity': 'warning' if metrics['avg_dispatch_time']['value'] < 10.0 else 'critical'
        })

    # 3. 重试率告警
    if metrics['retry_rate']['value'] > 0.10:
        alerts.append({
            'metric': 'retry_rate',
            'threshold': 0.10,
            'actual': metrics['retry_rate']['value'],
            'severity': 'warning'
        })

    # 4. Memory数量告警
    if metrics['memory_count']['value'] > 200:
        alerts.append({
            'metric': 'memory_count',
            'threshold': 200,
            'actual': metrics['memory_count']['value'],
            'severity': 'warning'
        })

    return alerts
```

---

## 📈 趋势分析

### 7天趋势

```python
def analyze_7day_trend():
    """
    分析过去7天的性能趋势

    Returns:
        dict: 趋势分析结果
    """
    # 获取过去7天的指标
    metrics_history = load_metrics_history(days=7)

    trend = {}
    for metric_name in ['dispatch_success_rate', 'avg_dispatch_time', 'retry_rate']:
        values = [m[metric_name] for m in metrics_history]

        # 计算趋势
        if len(values) >= 2:
            if values[-1] > values[-2]:
                direction = 'up'
            elif values[-1] < values[-2]:
                direction = 'down'
            else:
                direction = 'stable'

            # 计算变化率
            change_rate = (values[-1] - values[0]) / values[0] if values[0] != 0 else 0

            trend[metric_name] = {
                'direction': direction,
                'change_rate': change_rate,
                'current': values[-1],
                'previous': values[-2]
            }

    return trend
```

---

## ⚙️ 配置文件

### performance-monitoring-config.json

```json
{
  "version": "1.0",
  "config": {
    "collection_interval": 3600,
    "retention_days": 30,
    "enable_alerts": true,
    "alert_channel": "feishu"
  },
  "thresholds": {
    "dispatch_success_rate": {
      "warning": 0.90,
      "critical": 0.85
    },
    "avg_dispatch_time": {
      "warning": 5.0,
      "critical": 10.0
    },
    "retry_rate": {
      "warning": 0.10,
      "critical": 0.20
    },
    "fallback_rate": {
      "warning": 0.05,
      "critical": 0.10
    },
    "memory_count": {
      "warning": 180,
      "critical": 200
    }
  },
  "targets": {
    "dispatch_success_rate": 0.95,
    "avg_dispatch_time": 5.0,
    "retry_rate": 0.10,
    "fallback_rate": 0.05,
    "parallel_speedup": 1.3,
    "task_completion_rate": 0.95,
    "memory_count": 200,
    "avg_relevance_score": 0.7,
    "retrieval_accuracy": 0.8,
    "token_efficiency": 0.95
  }
}
```

---

## 🚀 未来优化

### 短期 (1-2周)
- [ ] 实现自动化性能报告
- [ ] 添加性能基线对比
- [ ] 实现异常检测算法

### 中期 (1个月)
- [ ] 实现性能预测模型
- [ ] 添加根因分析
- [ ] 实现自动优化建议

### 长期 (3个月)
- [ ] 引入AI驱动的性能优化
- [ ] 实现自适应阈值调整
- [ ] 构建性能知识库

---

*Skill版本: v1.0*
*最后更新: 2026-03-26*
*维护者: 象腿 (main agent)*
