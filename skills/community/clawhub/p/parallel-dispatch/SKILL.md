# Parallel Dispatch Skill

**版本**: v1.0
**创建日期**: 2026-03-26
**作者**: 象腿 (main agent)
**用途**: 并行调度多个独立任务，提升执行效率

---

## 🎯 核心功能

Parallel Dispatch skill负责：
1. **任务识别**: 识别哪些任务可以并行执行
2. **依赖分析**: 分析任务之间的依赖关系
3. **并行调度**: 使用多线程/多进程并行执行任务
4. **结果聚合**: 合并并行任务的执行结果
5. **错误处理**: 处理并行执行中的异常情况

---

## 📋 并行任务类型

### 类型1: 独立任务 (Independent Tasks)

多个完全独立的任务，可以同时执行。

**示例**:
```
任务1: 查询AI新闻
任务2: 检查Gateway状态
任务3: 查询今日日程
```

**并行度**: 最多2个任务（config.max_parallel_tasks）

---

### 类型2: 批量任务 (Batch Tasks)

同一类型的多个任务，可以批量处理。

**示例**:
```
批量查询3个飞书表格
批量搜索5个关键词
批量创建10个文档
```

**并行度**: 动态调整（基于任务数量和复杂度）

---

### 类型3: 流水线任务 (Pipeline Tasks)

前后有依赖关系的任务，可以流水线并行。

**示例**:
```
阶段1: 数据收集
阶段2: 数据处理（在阶段1部分完成后即可开始）
阶段3: 数据分析（在阶段2部分完成后即可开始）
```

**并行度**: 每个阶段内部并行

---

## 🔄 并行调度算法

### 算法1: 简单并行 (Simple Parallel)

```python
def simple_parallel_dispatch(tasks, max_parallel=2):
    """
    简单并行调度

    Args:
        tasks: 任务列表
        max_parallel: 最大并行数（默认2）

    Returns:
        list: 执行结果列表
    """
    from concurrent.futures import ThreadPoolExecutor, as_completed

    # 限制并行数量
    tasks_to_run = tasks[:max_parallel]

    results = []
    with ThreadPoolExecutor(max_workers=max_parallel) as executor:
        # 提交所有任务
        futures = {
            executor.submit(execute_task, task): task
            for task in tasks_to_run
        }

        # 等待任务完成
        for future in as_completed(futures):
            task = futures[future]
            try:
                result = future.result()
                results.append({
                    'task': task,
                    'result': result,
                    'success': True
                })
            except Exception as e:
                results.append({
                    'task': task,
                    'error': str(e),
                    'success': False
                })

    return results
```

---

### 算法2: 智能分批 (Smart Batching)

```python
def smart_batch_dispatch(tasks, max_parallel=2, timeout_per_task=60):
    """
    智能分批调度 - 自动处理大量任务

    Args:
        tasks: 任务列表（可能很多）
        max_parallel: 每批最大并行数
        timeout_per_task: 每个任务超时时间（秒）

    Returns:
        list: 所有任务的执行结果
    """
    from concurrent.futures import ThreadPoolExecutor, as_completed
    import time

    all_results = []
    batch_size = max_parallel

    # 分批处理
    for i in range(0, len(tasks), batch_size):
        batch = tasks[i:i + batch_size]
        batch_start_time = time.time()

        with ThreadPoolExecutor(max_workers=batch_size) as executor:
            futures = {
                executor.submit(execute_task_with_timeout, task, timeout_per_task): task
                for task in batch
            }

            for future in as_completed(futures):
                task = futures[future]
                try:
                    result = future.result()
                    all_results.append({
                        'task': task,
                        'result': result,
                        'success': True,
                        'batch': i // batch_size
                    })
                except Exception as e:
                    all_results.append({
                        'task': task,
                        'error': str(e),
                        'success': False,
                        'batch': i // batch_size
                    })

        batch_time = time.time() - batch_start_time
        log(f"Batch {i // batch_size} completed in {batch_time:.2f}s")

    return all_results
```

---

### 算法3: 依赖感知 (Dependency-Aware)

```python
def dependency_aware_dispatch(tasks_with_deps):
    """
    依赖感知的并行调度

    Args:
        tasks_with_deps: 带依赖关系的任务列表
            [{
                'id': 'task1',
                'action': '...',
                'dependencies': []  # 空数组表示无依赖
            }, {
                'id': 'task2',
                'action': '...',
                'dependencies': ['task1']  # 依赖task1
            }]

    Returns:
        list: 所有任务的执行结果
    """
    # 构建依赖图
    dependency_graph = build_dependency_graph(tasks_with_deps)

    # 拓扑排序
    execution_order = topological_sort(dependency_graph)

    # 按层级执行
    all_results = {}
    for level in execution_order:
        # 同一层的任务可以并行执行
        level_tasks = [t for t in tasks_with_deps if t['id'] in level]

        # 并行执行当前层的所有任务
        level_results = simple_parallel_dispatch(level_tasks)

        # 记录结果
        for result in level_results:
            all_results[result['task']['id']] = result

    return all_results
```

---

## 🛠️ PowerShell实现

### PowerShell并行执行（使用ForEach-Object）

```powershell
function Invoke-ParallelDispatch {
    param(
        [array]$Tasks,
        [int]$MaxParallel = 2
    )

    # 使用PowerShell 7+的ForEach-Object -Parallel
    $results = $Tasks | ForEach-Object -Parallel {
        $task = $_

        try {
            # 执行任务
            $result = Invoke-Task -Task $task

            @{
                Task = $task
                Result = $result
                Success = $true
            }
        } catch {
            @{
                Task = $task
                Error = $_.Exception.Message
                Success = $false
            }
        }
    } -ThrottleLimit $MaxParallel

    return $results
}
```

### PowerShell并行执行（使用Runspaces）

```powershell
function Invoke-ParallelDispatchRunspaces {
    param(
        [array]$Tasks,
        [int]$MaxParallel = 2
    )

    # 创建Runspace池
    $runspacePool = [runspacefactory]::CreateRunspacePool(1, $MaxParallel)
    $runspacePool.Open()

    # 创建任务列表
    $powershells = New-Object System.Collections.ArrayList
    $results = New-Object System.Collections.ArrayList

    foreach ($task in $Tasks) {
        # 创建PowerShell实例
        $powershell = [powershell]::Create()
        $powershell.RunspacePool = $runspacePool

        # 添加脚本
        $powershell.AddScript({
            param($task)
            Invoke-Task -Task $task
        }).AddArgument($task) | Out-Null

        # 开始异步执行
        $handle = $powershell.BeginInvoke()

        # 保存引用
        [void]$powershells.Add(@{
            PowerShell = $powershell
            Handle = $handle
            Task = $task
        })
    }

    # 等待所有任务完成
    foreach ($item in $powershells) {
        $item.Handle.WaitOne()

        $result = $item.PowerShell.EndInvoke($item.Handle)
        [void]$results.Add(@{
            Task = $item.Task
            Result = $result
            Success = $true
        })

        # 清理
        $item.PowerShell.Dispose()
    }

    # 清理Runspace池
    $runspacePool.Close()
    $runspacePool.Dispose()

    return $results
}
```

---

## 📊 性能优化

### 优化1: 任务预判

```python
def can_parallelize(tasks):
    """
    判断任务是否可以并行执行

    Args:
        tasks: 任务列表

    Returns:
        bool: 是否可以并行
    """
    # 检查任务数量
    if len(tasks) < 2:
        return False

    # 检查任务独立性
    task_ids = [task.get('id') for task in tasks]
    dependencies = []
    for task in tasks:
        dependencies.extend(task.get('dependencies', []))

    # 如果有依赖关系，不能简单并行
    if set(task_ids) & set(dependencies):
        return False

    return True
```

### 优化2: 动态并行度

```python
def calculate_optimal_parallelism(tasks):
    """
    根据任务特征计算最优并行度

    Args:
        tasks: 任务列表

    Returns:
        int: 最优并行度
    """
    # 基础并行度
    base_parallelism = 2

    # 根据任务数量调整
    if len(tasks) > 10:
        base_parallelism = 4
    elif len(tasks) > 5:
        base_parallelism = 3

    # 根据任务复杂度调整
    avg_complexity = sum(t.get('complexity', 1) for t in tasks) / len(tasks)
    if avg_complexity < 0.5:
        # 简单任务，可以增加并行度
        base_parallelism = min(base_parallelism + 1, 5)

    # 根据系统资源调整
    cpu_count = os.cpu_count()
    base_parallelism = min(base_parallelism, cpu_count)

    return base_parallelism
```

### 优化3: 超时控制

```python
def execute_task_with_timeout(task, timeout=60):
    """
    带超时控制的任务执行

    Args:
        task: 任务对象
        timeout: 超时时间（秒）

    Returns:
        任务执行结果
    """
    from concurrent.futures import ThreadPoolExecutor
    import signal

    def timeout_handler(signum, frame):
        raise TimeoutError(f"Task timeout after {timeout}s")

    # 设置超时
    signal.signal(signal.SIGALRM, timeout_handler)
    signal.alarm(timeout)

    try:
        result = execute_task(task)
        signal.alarm(0)  # 取消超时
        return result
    except TimeoutError as e:
        signal.alarm(0)
        return {'error': str(e), 'timeout': True}
```

---

## 🎓 使用示例

### 示例1: 简单并行

```python
# 用户输入
user_input = "查询AI新闻、检查Gateway状态、查看今日日程"

# 任务分解
tasks = [
    {'type': 'search', 'query': 'AI新闻'},
    {'type': 'check', 'target': 'Gateway'},
    {'type': 'query', 'target': '今日日程'}
]

# 并行执行
results = simple_parallel_dispatch(tasks, max_parallel=2)

# 结果整合
for result in results:
    print(f"Task: {result['task']}")
    print(f"Success: {result['success']}")
    if result['success']:
        print(f"Result: {result['result']}")
```

### 示例2: 批量查询

```python
# 批量查询飞书表格
table_ids = ['tbl1', 'tbl2', 'tbl3', 'tbl4', 'tbl5']

tasks = [
    {'type': 'query_bitable', 'table_id': tid}
    for tid in table_ids
]

# 智能分批执行
results = smart_batch_dispatch(tasks, max_parallel=2)

# 统计结果
success_count = sum(1 for r in results if r['success'])
print(f"成功: {success_count}/{len(results)}")
```

### 示例3: 依赖感知

```python
# 有依赖关系的任务
tasks = [
    {
        'id': 'collect_data',
        'action': '收集数据',
        'dependencies': []
    },
    {
        'id': 'process_data',
        'action': '处理数据',
        'dependencies': ['collect_data']
    },
    {
        'id': 'analyze_data',
        'action': '分析数据',
        'dependencies': ['process_data']
    }
]

# 依赖感知调度
results = dependency_aware_dispatch(tasks)

# 按顺序输出
for task_id in ['collect_data', 'process_data', 'analyze_data']:
    print(f"{task_id}: {results[task_id]}")
```

---

## ⚙️ 配置文件

### parallel-dispatch-config.json

```json
{
  "version": "1.0",
  "config": {
    "max_parallel_tasks": 2,
    "timeout_per_task": 60,
    "enable_smart_batching": true,
    "enable_dependency_aware": true,
    "log_performance": true
  },
  "algorithms": {
    "simple_parallel": {
      "enabled": true,
      "max_workers": 2
    },
    "smart_batching": {
      "enabled": true,
      "batch_size": 2,
      "batch_timeout": 120
    },
    "dependency_aware": {
      "enabled": false,
      "max_workers": 2
    }
  },
  "optimization": {
    "auto_adjust_parallelism": true,
    "predict_optimal_parallelism": true,
    "enable_timeout_control": true
  }
}
```

---

## 📈 性能指标

### 关键指标

```yaml
metrics:
  - name: "parallel_speedup"
    description: "并行加速比"
    formula: "串行总时间 / 并行总时间"
    target: "> 1.3x"

  - name: "task_completion_rate"
    description: "任务完成率"
    formula: "成功任务数 / 总任务数"
    target: "> 95%"

  - name: "avg_execution_time"
    description: "平均执行时间"
    formula: "总时间 / 任务数"
    target: "< 串行时间的70%"

  - name: "resource_utilization"
    description: "资源利用率"
    formula: "CPU使用率 / CPU核心数"
    target: "60-80%"
```

---

## 🚀 未来优化

### 短期 (1-2周)
- [ ] 添加任务优先级支持
- [ ] 实现任务取消机制
- [ ] 添加进度回调

### 中期 (1个月)
- [ ] 实现分布式任务调度
- [ ] 添加任务持久化
- [ ] 实现任务重试策略

### 长期 (3个月)
- [ ] 引入机器学习优化并行度
- [ ] 实现自适应调度算法
- [ ] 构建任务性能预测模型

---

*Skill版本: v1.0*
*最后更新: 2026-03-26*
*维护者: 象腿 (main agent)*
