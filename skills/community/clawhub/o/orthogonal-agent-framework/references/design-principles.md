# 正交性设计原则

## 核心原则

### 1. 模块独立（Module Independence）

每个模块应该能够独立工作，不依赖其他模块的内部实现。

```python
# ✅ 好的设计
class PlanningModule:
    def plan(self, task):
        return decompose(task)

class ExecutionModule:
    def execute(self, step):
        return run(step)

# 两个模块独立，可以单独测试和替换
```

### 2. 清晰接口（Clear Interfaces）

模块之间通过明确定义的接口通信。

```python
# 接口定义
interface PlanningInterface:
    def plan(task: str) -> List[Step]
    def update_plan(progress: Progress)

interface ExecutionInterface:
    def execute(step: Step) -> Result
    def rollback(step: Step)

interface MemoryInterface:
    def store(key: str, value: Any)
    def retrieve(key: str) -> Any
    def forget(key: str)

interface EvaluationInterface:
    def evaluate(result: Result) -> Score
    def feedback(issues: List[Issue]) -> List[Improvement]
```

### 3. 单一职责（Single Responsibility）

每个模块只负责一个功能域。

| 模块 | 职责 |
|------|------|
| Planning | 任务拆解、目标设定 |
| Execution | 工具调用、操作执行 |
| Memory | 存储、检索、遗忘 |
| Evaluation | 评估、反馈、验证 |

### 4. 可替换性（Replaceability）

任何模块都可以被替换而不影响系统。

```python
# 替换记忆模块
class FileMemory:
    """基于文件的记忆"""
    pass

class VectorMemory:
    """基于向量数据库的记忆"""
    pass

# 使用时选择
agent = Agent(memory=VectorMemory())  # 轻松替换
```

### 5. 可测试性（Testability）

每个模块可以单独测试。

```python
# 单独测试规划模块
def test_planning_module():
    module = PlanningModule()
    result = module.plan("写一篇论文")
    assert len(result.steps) > 0
    assert result.steps[0].title == "确定主题"
```

## 设计模式

### 模块注册模式

```python
class AgentFramework:
    modules = {}
    
    @classmethod
    def register(cls, name, module_class):
        cls.modules[name] = module_class
    
    @classmethod
    def create_agent(cls, config):
        return Agent(
            planning=cls.modules['planning'](config.planning),
            execution=cls.modules['execution'](config.execution),
            memory=cls.modules['memory'](config.memory),
            evaluation=cls.modules['evaluation'](config.evaluation),
        )
```

### 插件模式

```python
# 动态加载模块
class Agent:
    def __init__(self, modules):
        self.modules = {}
        for name, module in modules.items():
            self.modules[name] = module
    
    def add_module(self, name, module):
        self.modules[name] = module  # 热插拔
```

## 反模式（避免）

### 1. 紧耦合

```python
# ❌ 避免：模块之间直接调用内部方法
class Planning:
    def plan(self, task):
        # 直接调用execution模块
        self.execution.validate(task)  # 紧耦合
```

### 2. 共享状态

```python
# ❌ 避免：共享全局状态
global_state = {}

class ModuleA:
    def work(self):
        global_state['data'] = calculate()

class ModuleB:
    def work(self):
        data = global_state['data']  # 依赖共享状态
```

### 3. 循环依赖

```python
# ❌ 避免：模块之间循环依赖
class Planning:
    def __init__(self):
        self.execution = Execution()  # 依赖Execution
    
class Execution:
    def __init__(self):
        self.planning = Planning()  # 依赖Planning - 循环!
```
