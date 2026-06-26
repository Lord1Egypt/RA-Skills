# API Reference

## SkillLibrary

技能记忆库管理

### 初始化

```python
from scripts.embed_skill import SkillLibrary

library = SkillLibrary(persist_dir="skills/vector_store")
```

### 方法

#### `embed_skill(skill_path: str) -> bool`

将技能向量化存入 ChromaDB

**参数：**
- `skill_path`: 技能目录路径

**返回：** `bool` - 是否成功

---

#### `search(query: str, top_k: int = 5) -> Dict`

语义检索技能

**参数：**
- `query`: 查询文本
- `top_k`: 返回数量

**返回：** `Dict` - 检索结果

---

#### `list_skills() -> List[Dict]`

列出所有技能

**返回：** `List[Dict]` - 技能列表

---

## TaskPlanner

任务路由器

### 初始化

```python
from scripts.planner import TaskPlanner

planner = TaskPlanner(library, llm_client)
```

### 方法

#### `plan(task: str) -> PlanResult`

规划任务执行

**参数：**
- `task`: 用户任务描述

**返回：** `PlanResult` - 执行计划

---

## SkillGenerator

技能生成器

### 初始化

```python
from scripts.generator import SkillGenerator

generator = SkillGenerator(llm_client, model="deepseek/deepseek-coder")
```

### 方法

#### `generate(requirement: str) -> Optional[GeneratedSkill]`

生成技能

**参数：**
- `requirement`: 用户需求

**返回：** `GeneratedSkill` 或 `None`

---

## SkillTester

技能测试器

### SimpleTester（本地测试）

```python
from scripts.tester import SimpleTester, TestCase

tester = SimpleTester(timeout=10)

results = tester.test_skill(code, [
    TestCase("test1", {"name": "Alice"}, "expected"),
])
```

### DockerTester（容器测试）

```python
from scripts.tester import DockerTester

tester = DockerTester(
    image="python:3.11-slim",
    timeout=10,
    memory_limit="256m"
)
```

---

## SkillEvaluator

技能评估器

### 初始化

```python
from scripts.evaluator import SkillEvaluator

evaluator = SkillEvaluator(
    weights={
        "success_rate": 0.4,
        "speed": 0.2,
        "robustness": 0.2,
        "quality": 0.2
    },
    pass_threshold=0.7
)
```

### 方法

#### `evaluate(test_results, execution_times, code, timeout=10) -> EvaluationResult`

评估技能

**参数：**
- `test_results`: 测试结果列表
- `execution_times`: 执行时间列表
- `code`: 技能代码
- `timeout`: 超时时间

**返回：** `EvaluationResult`

---

## SkillOptimizer

技能优化器

### 初始化

```python
from scripts.optimizer import SkillOptimizer

optimizer = SkillOptimizer(llm_client)
```

### 方法

#### `optimize(original_code, error, expected_output=None) -> Tuple[Result, Result]`

优化技能代码

**参数：**
- `original_code`: 原始代码
- `error`: 错误信息
- `expected_output`: 期望输出

**返回：** `(版本A结果, 版本B结果)`

---

## SkillComposer

技能组合器

### 初始化

```python
from scripts.composer import SkillComposer

composer = SkillComposer(library, llm_client)
```

### 方法

#### `decompose_task(task: str) -> List[SkillNode]`

分解复杂任务

**返回：** 技能节点列表

---

#### `execute_pipeline(dag, initial_inputs, skill_loader) -> ExecutionResult`

执行技能管道

**参数：**
- `dag`: NetworkX 有向图
- `initial_inputs`: 初始输入
- `skill_loader`: 技能加载函数

**返回：** `ExecutionResult`

---

## AutoRefactor

自动重构器

### 初始化

```python
from scripts.auto_refactor import AutoRefactor

refactor = AutoRefactor(
    history_file="logs/skill_usage.json",
    output_dir="skills/generated",
    min_usage_count=5
)
```

### 方法

#### `record_execution(skill_sequence: List[str])`

记录技能执行

#### `run_auto_refactor(llm_client=None) -> List[RefactorSuggestion]`

运行自动重构

#### `schedule_weekly(llm_client=None)`

每周定时运行

---

## 使用示例

### 完整流程

```python
from scripts import (
    SkillLibrary, TaskPlanner, SkillGenerator,
    SimpleTester, SkillEvaluator, SkillOptimizer
)

# 1. 初始化
library = SkillLibrary()
planner = TaskPlanner(library)
generator = SkillGenerator(llm_client)
tester = SimpleTester()
evaluator = SkillEvaluator()

# 2. 规划
task = "发送邮件给老板"
plan = planner.plan(task)

if plan.action == "use_skill":
    # 使用现有技能
    skill = library.load_skill(plan.skill_id)
    result = skill.execute(...)
    
elif plan.action == "generate_skill":
    # 生成新技能
    skill = generator.generate(plan.task_description)
    
    # 测试
    results = tester.test_skill(skill.code, test_cases)
    
    # 评估
    eval_result = evaluator.evaluate(results, times, skill.code)
    
    if eval_result.passed:
        # 保存
        library.embed_skill(new_skill_path)
    else:
        # 优化
        optimizer = SkillOptimizer(llm_client)
        # ... 优化循环
```
