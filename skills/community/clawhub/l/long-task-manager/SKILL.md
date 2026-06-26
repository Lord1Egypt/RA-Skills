# Long Task Manager Skill

**版本**: v1.0  
**作者**: BI Alpha  
**创建时间**: 2026-03-17  
**适用场景**: AI Agent 长时间任务处理、进度追踪、异步执行

---

## 🎯 Skill 简介

**Long Task Manager** 是一个专为 OpenClaw AI Agent 设计的长时间任务处理框架，解决 Agent 执行超时、状态不可见、无法取消等问题。

### 核心能力

| 能力 | 说明 |
|------|------|
| 🕐 **无超时执行** | 支持任意时长任务（代码生成、数据处理等） |
| 📊 **实时进度** | 0-100% 进度可视化，执行过程透明 |
| 🔄 **异步非阻塞** | 提交后立即返回任务ID，主流程不等待 |
| ❌ **任务取消** | 支持中途取消长时间任务 |
| 💾 **断点续传** | 支持任务恢复和断点继续 |
| 📈 **状态持久化** | 任务状态保存到文件，跨会话保持 |

---

## 📦 安装与启用

### 1. 安装 Skill

```bash
# 通过 clawhub 安装
clawhub install long-task-manager

# 或者手动复制到 skills 目录
cp -r long-task-manager ~/.openclaw/workspace/skills/
```

### 2. 在 AGENTS.md 中注册

```yaml
# AGENTS.md

## Long Task Manager

| 属性 | 值 |
|------|-----|
| **名称** | 长时间任务管理器 |
| **ID** | `long_task_manager` |
| **运行时** | `subagent` |
| **模式** | `run` / `session` |
| **超时** | 无限制 (session模式) |
| **版本** | v1.0 |

**能力列表**:
- 长时间任务提交与调度
- 实时进度追踪与查询
- 任务取消与恢复
- 批量任务管理

**使用场景**:
- 代码生成 (大量API/文件)
- 数据处理 (大数据集)
- 批量文档生成
- 长时间计算任务

**记忆文件**: `memory/agents/long_task_manager.md`
```

---

## 🚀 快速开始

### 基础用法

```python
# 1. 导入 Long Task Manager
from skills.long_task_manager import LongTaskManager

# 2. 初始化管理器
task_manager = LongTaskManager(
    task_dir="/tmp/long_tasks",  # 任务存储目录
    max_concurrent=5              # 最大并发任务数
)

# 3. 提交长时间任务
task_id = task_manager.submit(
    agent_id="code_gen_ali",
    task_config={
        "name": "生成50个API接口",
        "type": "code_gen",
        "total_items": 50,  # 总工作量
        "params": {
            "module": "MyApp.Controllers",
            "output_dir": "/output/apis/"
        }
    }
)

print(f"✅ 任务已提交: {task_id}")

# 4. 轮询查询进度
import time
while True:
    status = task_manager.get_status(task_id)
    
    print(f"[{status['status']}] 进度: {status['progress']}")
    
    if status['status'] == 'completed':
        result = task_manager.get_result(task_id)
        print(f"✅ 完成！生成文件: {result['files']}")
        break
    
    if status['status'] == 'failed':
        print(f"❌ 失败: {status['error']}")
        break
    
    time.sleep(5)  # 每5秒查询一次
```

---

## 📚 完整 API 文档

### 类: LongTaskManager

#### 构造函数

```python
LongTaskManager(
    task_dir: str = "/tmp/long_tasks",  # 任务存储目录
    max_concurrent: int = 5,            # 最大并发数
    default_timeout: int = None         # 默认超时(秒), None=无限制
)
```

#### 方法: submit()

提交长时间任务。

```python
def submit(
    self,
    agent_id: str,           # 执行Agent ID
    task_config: dict,       # 任务配置
    priority: str = "normal" # 优先级: high/normal/low
) -> str:
    """
    提交任务，返回任务ID
    
    Args:
        agent_id: 执行任务的Agent (如 "code_gen_ali")
        task_config: 任务配置字典
        priority: 任务优先级
        
    Returns:
        task_id: 唯一任务标识符
    """
```

**task_config 配置项**:

| 字段 | 类型 | 必需 | 说明 |
|------|------|------|------|
| `name` | str | ✅ | 任务名称 |
| `type` | str | ✅ | 任务类型 (code_gen/data_process/...) |
| `total_items` | int | ✅ | 总工作量 (用于计算进度) |
| `params` | dict | ⚪ | 任务参数 |
| `estimated_time` | int | ⚪ | 预估时间(秒) |

#### 方法: get_status()

查询任务状态。

```python
def get_status(self, task_id: str) -> dict:
    """
    获取任务当前状态
    
    Returns:
        {
            "task_id": "xxx",
            "status": "running",      # pending/running/completed/failed/cancelled
            "progress": "45%",        # 进度百分比
            "current_item": "Api23",  # 当前执行项
            "completed": 23,          # 已完成数量
            "total": 50,              # 总数量
            "started_at": "...",
            "updated_at": "...",
            "detail": "生成Api23Controller..."
        }
    """
```

#### 方法: get_result()

获取任务结果。

```python
def get_result(self, task_id: str) -> dict:
    """
    获取已完成任务的结果
    
    Returns:
        {
            "task_id": "xxx",
            "status": "completed",
            "files": [...],           # 生成的文件列表
            "summary": "...",         # 执行摘要
            "elapsed_time": 300,      # 耗时(秒)
            "completed_at": "..."
        }
    """
```

#### 方法: cancel()

取消任务。

```python
def cancel(self, task_id: str) -> bool:
    """
    取消正在运行的任务
    
    Returns:
        True: 取消成功
        False: 任务已完成或不存在
    """
```

#### 方法: list_tasks()

列出所有任务。

```python
def list_tasks(
    self,
    status_filter: str = None,  # 状态过滤
    agent_id: str = None        # Agent过滤
) -> list:
    """
    列出任务
    
    Returns:
        [{"task_id": "...", "status": "...", ...}, ...]
    """
```

---

### Agent内部进度上报

在长时间任务的Agent内部，需要定期上报进度：

```python
# 在 code_gen_ali Agent 内部
from skills.long_task_manager import TaskWorker

class MyLongTask:
    def __init__(self, task_id, task_dir):
        self.worker = TaskWorker(task_id, task_dir)
    
    def run(self, params):
        total = params['total_items']
        
        for i in range(total):
            # 执行实际工作
            self.do_work(i)
            
            # 上报进度 (每10%或每30秒)
            if i % (total // 10) == 0:
                self.worker.update_progress(
                    progress=f"{i/total*100:.1f}%",
                    current_item=f"Item{i}",
                    detail=f"正在处理第{i}项..."
                )
        
        # 完成上报
        self.worker.complete(result={"files": [...]})
```

---

## 💡 使用示例

### 示例1: 代码生成

```python
# 生成大量API代码
manager = LongTaskManager()

task_id = manager.submit(
    agent_id="code_gen_ali",
    task_config={
        "name": "生成BI4Sight后端API",
        "type": "code_gen",
        "total_items": 50,
        "params": {
            "module": "BI4Sight.API",
            "output_dir": "/projects/bi4sight/apis/"
        }
    }
)

# 监控进度
monitor_task(manager, task_id)
```

### 示例2: 数据处理

```python
# 处理大数据集
manager = LongTaskManager()

task_id = manager.submit(
    agent_id="data_miner",
    task_config={
        "name": "分析用户行为数据",
        "type": "data_process",
        "total_items": 100000,  # 10万条数据
        "params": {
            "input_file": "/data/users.csv",
            "output_file": "/results/analysis.json"
        }
    }
)
```

### 示例3: 批量文档生成

```python
# 批量生成文档
manager = LongTaskManager()

task_id = manager.submit(
    agent_id="product_agent",
    task_config={
        "name": "生成产品文档",
        "type": "doc_gen",
        "total_items": 20,
        "params": {
            "template": "product_doc",
            "output_dir": "/docs/products/"
        }
    }
)
```

---

## 🔧 高级配置

### 配置定时轮询 (HEARTBEAT)

```yaml
# HEARTBEAT.md

## 长时间任务监控

- **任务**: 检查长时间任务进度
- **频率**: 每1分钟
- **动作**: 
  - 查询所有running任务状态
  - 更新进度显示
  - 完成时发送通知
```

### 自定义存储后端

```python
# 使用数据库存储 (可选)
from skills.long_task_manager import LongTaskManager, DatabaseStorage

manager = LongTaskManager(
    storage=DatabaseStorage(
        url="sqlite:///tasks.db"
    )
)
```

---

## 🐛 故障排查

### 常见问题

**Q1: 任务状态不更新**
- 检查Agent是否调用了 `update_progress()`
- 检查状态文件权限

**Q2: 任务完成后无法获取结果**
- 检查任务是否真的完成 (status == "completed")
- 检查 `task_dir` 路径是否正确

**Q3: 并发任务过多**
- 调整 `max_concurrent` 参数
- 使用任务队列排队

---

## 📝 更新日志

| 版本 | 日期 | 变更 |
|------|------|------|
| v1.0 | 2026-03-17 | 初始版本，基础功能完整 |

---

## 📞 支持与反馈

- **Issues**: 提交到 GitHub Issues
- **讨论**: OpenClaw Discord #skills 频道
- **文档**: https://docs.openclaw.ai/skills/long-task-manager

---

**🎉 开始使用 Long Task Manager，告别 Agent 超时困扰！**
