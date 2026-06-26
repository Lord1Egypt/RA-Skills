# 使用示例

## 示例 1：基本使用流程

```python
from scripts import SkillLibrary, TaskPlanner

# 初始化
library = SkillLibrary()
planner = TaskPlanner(library)

# 规划任务
task = "查询今天天气"
plan = planner.plan(task)

print(f"行动计划: {plan.action}")
print(f"理由: {plan.reasoning}")
```

输出：
```
行动计划: use_skill
理由: 找到相似技能 skill_weather（相似度: 0.92）
```

## 示例 2：生成新技能

```python
from scripts import SkillGenerator, SimpleTester, TestCase

# 生成
generator = SkillGenerator(llm_client)
skill = generator.generate("创建一个发送邮件的技能")

print(f"技能名称: {skill.name}")
print(f"代码:\n{skill.code[:200]}...")

# 测试
tester = SimpleTester()
results = tester.test_skill(skill.code, [
    TestCase(
        name="test_send",
        inputs={"to": "test@example.com", "content": "Hello"},
        expected="邮件已发送"
    )
])

for r in results:
    print(f"{r.case_name}: {'✅' if r.success else '❌'}")
```

## 示例 3：评估技能

```python
from scripts import SkillEvaluator, TestResult

evaluator = SkillEvaluator()

# 模拟测试结果
test_results = [
    TestResult("test1", True, {"result": "ok"}, None, 0.1),
    TestResult("test2", True, {"result": "ok"}, None, 0.15),
    TestResult("test3", False, None, "错误", 0.2),
]

times = [0.1, 0.15, 0.2]
code = "..." # 技能代码

result = evaluator.evaluate(test_results, times, code)

print(f"总分: {result.score}")
print(f"通过: {result.passed}")
print(f"详细: {result.breakdown}")
```

输出：
```
总分: 0.725
通过: True
详细: {'SR (Success Rate)': 0.667, 'Sp (Speed)': 0.975, 'R (Robustness)': 0.4, 'Q (Quality)': 0.75}
```

## 示例 4：优化技能

```python
from scripts import SkillOptimizer, SkillEvaluator

optimizer = SkillOptimizer(llm_client)
evaluator = SkillEvaluator()

# 原始代码（有错误）
code = '''
class MySkill:
    def execute(self, name):
        return {"result": "Hello " + name}
'''

error = "TypeError: unsupported operand..."

# 优化
version_a, version_b = optimizer.optimize(code, error)

# 评估两者
from scripts import SimpleTester, TestCase

tester = SimpleTester()
test_cases = [TestCase("test", {"name": "World"}, "Hello World")]

results_a = tester.test_skill(version_a.code, test_cases)
eval_a = evaluator.evaluate(results_a, [r.execution_time for r in results_a], version_a.code)

results_b = tester.test_skill(version_b.code, test_cases)
eval_b = evaluator.evaluate(results_b, [r.execution_time for r in results_b], version_b.code)

# 选择最佳
if eval_a.score >= eval_b.score:
    best = version_a
else:
    best = version_b

print(f"最佳版本: {best.strategy}, 得分: {max(eval_a.score, eval_b.score)}")
```

## 示例 5：组合技能

```python
from scripts import SkillComposer, SkillNode

composer = SkillComposer(library)

# 分解复杂任务
nodes = composer.decompose_task("发送邮件并通知")

# 构建 DAG
dag = composer.build_dag(nodes)

# 可视化
print(composer.visualize_dag(dag))

# 执行
def load_skill(skill_id):
    # 加载技能
    ...

result = composer.execute_pipeline(dag, initial_inputs, load_skill)

print(f"成功: {result.success}")
print(f"执行顺序: {result.execution_order}")
```

## 示例 6：自动重构

```python
from scripts import AutoRefactor

refactor = AutoRefactor()

# 记录使用
refactor.record_execution(["skill_email", "skill_notification"])
refactor.record_execution(["skill_email", "skill_notification"])
refactor.record_execution(["skill_email", "skill_notification"])

# 分析
analysis = refactor.analyze_usage()
print(f"高频组合: {analysis['frequent_pairs']}")

# 生成 meta-skill
suggestions = refactor.run_auto_refactor(llm_client)
print(f"生成了 {len(suggestions)} 个 meta-skills")
```

## 示例 7：完整工作流

```python
from scripts import (
    SkillLibrary, TaskPlanner, SkillGenerator,
    SimpleTester, SkillEvaluator, SkillOptimizer
)

def workflow(task, llm_client):
    # 1. 规划
    library = SkillLibrary()
    planner = TaskPlanner(library)
    plan = planner.plan(task)
    
    if plan.action == "use_skill":
        # 使用现有技能
        skill = library.load_skill(plan.skill_id)
        return skill.execute()
    
    # 2. 生成
    generator = SkillGenerator(llm_client)
    skill = generator.generate(task)
    
    # 3. 测试 + 评估 + 优化（循环）
    tester = SimpleTester()
    evaluator = SkillEvaluator()
    optimizer = SkillOptimizer(llm_client)
    
    for iteration in range(3):
        # 测试
        results = tester.test_skill(skill.code, test_cases)
        
        # 评估
        eval_result = evaluator.evaluate(results, times, skill.code)
        
        if eval_result.passed:
            # 保存
            library.embed_skill(new_skill)
            return eval_result
        
        # 优化
        skill.code = optimizer.optimize(skill.code, error)
    
    return None
```

## CLI 用法

### 注册技能

```bash
python scripts/embed_skill.py embed --path skills/skill_library/weather
```

### 搜索技能

```python
python scripts/embed_skill.py search --query "天气"
```

### 列出所有技能

```python
python scripts/embed_skill.py list
```
