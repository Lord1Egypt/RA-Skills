---
name: model-distill-langgraph
description: |
  使用 LangGraph 重构的模型蒸馏 Skill。
  支持状态管理、条件分支、人机在循环中、自动重试。
  触发词：「用 LangGraph 蒸馏」「智能蒸馏流程」「交互式模型蒸馏」。
---

# 模型蒸馏大师 (LangGraph 版本)

> 基于 LangGraph 的状态驱动蒸馏工作流

## 为什么用 LangGraph？

| 传统实现 | LangGraph 实现 |
|---------|---------------|
| Phase 线性执行 | 图结构，支持循环和分支 |
| 检查点靠人工确认 | 状态自动保存，随时恢复 |
| 失败需重新开始 | 从失败节点重试 |
| 人机交互靠打印输出 | 专门的 Human-in-the-loop 节点 |

## 架构图

```
                    ┌─────────────────┐
                    │    用户输入     │
                    └────────┬────────┘
                             ▼
┌──────────────┐      ┌─────────────────┐      ┌──────────────┐
│ 需求诊断节点 │◄─────│   ParseInput    │─────►│  检查目标    │
└──────┬───────┘      └─────────────────┘      └──────┬───────┘
       │                                             │
       ▼                                             ▼
┌──────────────┐      ┌─────────────────┐      ┌──────────────┐
│  可行性评估  │─────►│  Human Confirm  │◄─────│  调整目标    │
└──────┬───────┘      └────────┬────────┘      └──────────────┘
       │                       │
       ▼                       ▼
┌──────────────┐      ┌─────────────────┐
│  环境准备    │      │  用户取消       │
└──────┬───────┘      └─────────────────┘
       │
       ▼
┌──────────────────────────────────────────┐
│         Parallel Teachers Analysis       │
│  ┌─────────┐ ┌─────────┐ ┌─────────┐    │
│  │Agent A  │ │Agent B  │ │Agent C  │    │
│  │能力测绘  │ │推理提取  │ │知识分离  │    │
│  └────┬────┘ └────┬────┘ └────┬────┘    │
│       └────────────┼────────────┘        │
│                    ▼                     │
│            ┌─────────────┐               │
│            │  结果汇总   │               │
│            └──────┬──────┘               │
└───────────────────┼──────────────────────┘
                    ▼
           ┌─────────────────┐
           │  Human Review   │◄────── 用户可要求重新分析
           └────────┬────────┘
                    ▼
           ┌─────────────────┐
           │  数据合成并行   │
           └────────┬────────┘
                    ▼
           ┌─────────────────┐
           │  质量检查       │──失败──┐
           └────────┬────────┘        │
                    ▼                 │
           ┌─────────────────┐        │
           │  训练执行       │        │
           └────────┬────────┘        │
                    ▼                 │
           ┌─────────────────┐        │
           │  效果验证       │        │
           └────────┬────────┘        │
                    ▼                 │
           ┌─────────────────┐        │
           │  是否达标？     │──否────┘
           └────────┬────────┘
                    │是
                    ▼
           ┌─────────────────┐
           │  交付模型       │
           └─────────────────┘
```

## 核心组件

### 1. 状态定义 (State)

```python
from typing import TypedDict, Annotated, List, Optional
from langgraph.graph import StateGraph
from langgraph.checkpoint.memory import MemorySaver

class DistillState(TypedDict):
    # 用户输入
    teacher_model: str
    target_task: str
    student_model: str  # 默认 gemma-4-E4B-it
    
    # 可行性评估结果
    feasibility_score: float
    feasibility_reason: str
    user_approved: Optional[bool]
    
    # 教师分析结果
    teacher_analysis: dict
    analysis_reviewed: Optional[bool]
    
    # 数据合成
    train_data_path: Optional[str]
    eval_data_path: Optional[str]
    data_quality_score: float
    
    # 训练状态
    training_config: Optional[dict]
    checkpoint_path: Optional[str]
    
    # 评估结果
    baseline_metrics: Optional[dict]
    distilled_metrics: Optional[dict]
    performance_improved: Optional[bool]
    
    # 流程控制
    current_step: str
    error_message: Optional[str]
    retry_count: int
```

### 2. 节点定义 (Nodes)

#### Node 0: Parse Input
```python
def parse_input(state: DistillState) -> DistillState:
    """解析用户输入，提取关键信息"""
    # 提取教师模型、目标任务等
    return {
        **state,
        "teacher_model": extract_teacher(state["raw_input"]),
        "target_task": extract_task(state["raw_input"]),
        "student_model": "google/gemma-4-E4B-it",
        "current_step": "parsed"
    }
```

#### Node 1: Feasibility Check
```python
def check_feasibility(state: DistillState) -> DistillState:
    """评估蒸馏目标是否可行"""
    task = state["target_task"]
    
    # 评估逻辑
    if "知识" in task or "事实" in task:
        score = 0.4  # 4B模型不适合知识密集型
        reason = "4B模型容量有限，不适合知识密集型任务"
    elif "推理" in task or "代码" in task or "数学" in task:
        score = 0.9
        reason = "推理密集型任务适合蒸馏到4B模型"
    else:
        score = 0.7
        reason = "通用任务可以尝试"
    
    return {
        **state,
        "feasibility_score": score,
        "feasibility_reason": reason,
        "current_step": "feasibility_checked"
    }
```

#### Node 2: Human Confirm (人机交互)
```python
def human_confirm_feasibility(state: DistillState) -> DistillState:
    """
    等待用户确认可行性评估
    
    LangGraph 会自动保存状态并暂停，
    等待用户输入后继续
    """
    print(f"\n可行性评估: {state['feasibility_score']:.0%}")
    print(f"原因: {state['feasibility_reason']}")
    
    # LangGraph 的 interrupt 机制
    response = interrupt({
        "question": "是否继续蒸馏？",
        "options": ["继续", "调整目标", "取消"]
    })
    
    if response == "继续":
        return {**state, "user_approved": True}
    elif response == "调整目标":
        return {**state, "user_approved": False, "current_step": "need_refine"}
    else:
        raise ValueError("用户取消")
```

#### Node 3: Parallel Teacher Analysis
```python
from langgraph.constants import Send

def start_teacher_analysis(state: DistillState) -> List[Send]:
    """启动并行的教师分析"""
    return [
        Send("analyze_capability", state),
        Send("analyze_reasoning", state),
        Send("analyze_knowledge", state),
    ]

def analyze_capability(state: DistillState) -> DistillState:
    """Agent A: 能力边界测绘"""
    # 分析教师模型在目标领域的能力
    analysis = {
        "accuracy": 0.95,
        "coverage": ["task1", "task2", "task3"],
        "weaknesses": ["edge_case1"]
    }
    return {
        **state,
        "teacher_analysis": {
            **state.get("teacher_analysis", {}),
            "capability": analysis
        }
    }

def analyze_reasoning(state: DistillState) -> DistillState:
    """Agent B: 推理模式提取"""
    analysis = {
        "patterns": ["step_by_step", "verification"],
        "cot_style": "detailed"
    }
    return {
        **state,
        "teacher_analysis": {
            **state.get("teacher_analysis", {}),
            "reasoning": analysis
        }
    }

def analyze_knowledge(state: DistillState) -> DistillState:
    """Agent C: 知识vs能力分离"""
    analysis = {
        "transferable": 0.7,
        "memorization": 0.3
    }
    return {
        **state,
        "teacher_analysis": {
            **state.get("teacher_analysis", {}),
            "knowledge_skill_split": analysis
        }
    }

def aggregate_analysis(state: DistillState) -> DistillState:
    """汇总所有分析结果"""
    print("\n=== 教师分析结果 ===")
    print(json.dumps(state["teacher_analysis"], indent=2, ensure_ascii=False))
    return {**state, "current_step": "analysis_complete"}
```

#### Node 4: Human Review Analysis
```python
def human_review_analysis(state: DistillState) -> DistillState:
    """用户审查分析结果，可要求重新分析"""
    response = interrupt({
        "question": "分析结果是否满意？",
        "analysis": state["teacher_analysis"],
        "options": ["满意，继续", "重新分析", "调整目标"]
    })
    
    if response == "满意，继续":
        return {**state, "analysis_reviewed": True}
    elif response == "重新分析":
        return {**state, "analysis_reviewed": False, "current_step": "reanalyze"}
    else:
        return {**state, "current_step": "need_refine"}
```

#### Node 5: Data Generation (带重试)
```python
def generate_training_data(state: DistillState) -> DistillState:
    """生成训练数据，支持失败重试"""
    max_retries = 3
    
    for attempt in range(max_retries):
        try:
            # 调用数据生成逻辑
            train_path, eval_path = synthesize_data(
                teacher=state["teacher_model"],
                task=state["target_task"],
                analysis=state["teacher_analysis"]
            )
            
            return {
                **state,
                "train_data_path": train_path,
                "eval_data_path": eval_path,
                "data_quality_score": 0.85,
                "current_step": "data_generated"
            }
        except Exception as e:
            if attempt == max_retries - 1:
                raise
            print(f"数据生成失败，重试 {attempt + 1}/{max_retries}")
            time.sleep(2 ** attempt)  # 指数退避

def check_data_quality(state: DistillState) -> DistillState:
    """检查数据质量"""
    score = state.get("data_quality_score", 0)
    
    if score < 0.6:
        return {
            **state,
            "current_step": "data_quality_failed",
            "error_message": "数据质量不足，需要重新生成"
        }
    
    return {**state, "current_step": "data_quality_ok"}
```

#### Node 6: Training
```python
def train_model(state: DistillState) -> DistillState:
    """执行模型训练"""
    config = generate_training_config(state)
    
    print(f"\n开始训练...")
    print(f"训练数据: {state['train_data_path']}")
    print(f"学生模型: {state['student_model']}")
    
    # 实际训练调用
    checkpoint = run_distillation_training(config)
    
    return {
        **state,
        "training_config": config,
        "checkpoint_path": checkpoint,
        "current_step": "training_complete"
    }
```

#### Node 7: Evaluation
```python
def evaluate_model(state: DistillState) -> DistillState:
    """评估蒸馏效果"""
    baseline = evaluate_baseline(state["student_model"])
    distilled = evaluate_distilled(state["checkpoint_path"])
    
    improved = distilled["accuracy"] > baseline["accuracy"]
    
    return {
        **state,
        "baseline_metrics": baseline,
        "distilled_metrics": distilled,
        "performance_improved": improved,
        "current_step": "evaluation_complete"
    }
```

#### Node 8: Human Final Review
```python
def human_final_review(state: DistillState) -> DistillState:
    """最终审查，可决定是否继续优化"""
    print("\n=== 蒸馏结果 ===")
    print(f"基线准确率: {state['baseline_metrics']['accuracy']:.2%}")
    print(f"蒸馏后准确率: {state['distilled_metrics']['accuracy']:.2%}")
    
    if not state["performance_improved"]:
        print("⚠️ 性能未提升")
    
    response = interrupt({
        "question": "蒸馏结果是否满意？",
        "metrics": {
            "baseline": state["baseline_metrics"],
            "distilled": state["distilled_metrics"]
        },
        "options": ["满意，交付", "重新训练", "调整数据再试"]
    })
    
    if response == "满意，交付":
        return {**state, "current_step": "deliver"}
    elif response == "重新训练":
        return {**state, "current_step": "retrain", "retry_count": state.get("retry_count", 0) + 1}
    else:
        return {**state, "current_step": "regenerate_data"}
```

### 3. 条件边 (Conditional Edges)

```python
def should_continue_after_feasibility(state: DistillState) -> str:
    """根据可行性评估决定下一步"""
    if state.get("user_approved") is True:
        return "continue"
    elif state.get("user_approved") is False:
        return "refine"
    else:
        return "cancel"

def should_reanalyze(state: DistillState) -> str:
    """根据用户反馈决定是否重新分析"""
    if state.get("analysis_reviewed") is True:
        return "continue"
    elif state.get("current_step") == "reanalyze":
        return "reanalyze"
    else:
        return "refine_goal"

def check_data_quality_edge(state: DistillState) -> str:
    """检查数据质量分支"""
    if state.get("data_quality_score", 0) >= 0.6:
        return "proceed"
    else:
        return "retry"

def check_training_result(state: DistillState) -> str:
    """检查训练结果"""
    if state.get("performance_improved"):
        return "deliver"
    elif state.get("retry_count", 0) < 2:
        return "retry"
    else:
        return "deliver_anyway"  # 达到重试上限，交付当前最佳
```

### 4. 构建图

```python
# 初始化图
workflow = StateGraph(DistillState)

# 添加节点
workflow.add_node("parse_input", parse_input)
workflow.add_node("check_feasibility", check_feasibility)
workflow.add_node("human_confirm", human_confirm_feasibility)
workflow.add_node("analyze_capability", analyze_capability)
workflow.add_node("analyze_reasoning", analyze_reasoning)
workflow.add_node("analyze_knowledge", analyze_knowledge)
workflow.add_node("aggregate_analysis", aggregate_analysis)
workflow.add_node("human_review_analysis", human_review_analysis)
workflow.add_node("generate_data", generate_training_data)
workflow.add_node("check_quality", check_data_quality)
workflow.add_node("train", train_model)
workflow.add_node("evaluate", evaluate_model)
workflow.add_node("human_final", human_final_review)
workflow.add_node("deliver", deliver_model)

# 添加边
workflow.set_entry_point("parse_input")
workflow.add_edge("parse_input", "check_feasibility")
workflow.add_edge("check_feasibility", "human_confirm")

# 条件边
workflow.add_conditional_edges(
    "human_confirm",
    should_continue_after_feasibility,
    {
        "continue": "analyze_capability",  # 进入并行分析
        "refine": "parse_input",  # 回到开始重新解析
        "cancel": END
    }
)

# 并行分析
workflow.add_conditional_edges(
    "analyze_capability",
    start_teacher_analysis,
    ["analyze_capability", "analyze_reasoning", "analyze_knowledge"]
)
workflow.add_edge("analyze_capability", "aggregate_analysis")
workflow.add_edge("analyze_reasoning", "aggregate_analysis")
workflow.add_edge("analyze_knowledge", "aggregate_analysis")

workflow.add_edge("aggregate_analysis", "human_review_analysis")

# 条件边：是否重新分析
workflow.add_conditional_edges(
    "human_review_analysis",
    should_reanalyze,
    {
        "continue": "generate_data",
        "reanalyze": "analyze_capability",
        "refine_goal": "parse_input"
    }
)

# 数据生成和训练
workflow.add_edge("generate_data", "check_quality")
workflow.add_conditional_edges(
    "check_quality",
    check_data_quality_edge,
    {
        "proceed": "train",
        "retry": "generate_data"
    }
)

workflow.add_edge("train", "evaluate")
workflow.add_edge("evaluate", "human_final")

# 最终结果分支
workflow.add_conditional_edges(
    "human_final",
    check_training_result,
    {
        "deliver": "deliver",
        "retry": "train",
        "deliver_anyway": "deliver"
    }
)

workflow.add_edge("deliver", END)

# 添加记忆（支持断点续传）
checkpointer = MemorySaver()
app = workflow.compile(checkpointer=checkpointer)
```

### 5. 运行

```python
# 初始输入
initial_state = {
    "raw_input": "把GPT-4的数学推理能力蒸馏到gemma-4-E4B-it",
    "retry_count": 0
}

# 运行（自动处理人机交互）
config = {"configurable": {"thread_id": "distill_001"}}

for event in app.stream(initial_state, config, stream_mode="updates"):
    print(event)

# 如果需要从断点恢复
# app.invoke(None, config)  # 从上次中断处继续
```

## 优势对比

| 功能 | 传统实现 | LangGraph |
|-----|---------|-----------|
| 状态管理 | 全局变量或文件 | TypedDict，类型安全 |
| 人机交互 | `input()` 阻塞 | `interrupt()` 优雅暂停 |
| 断点续传 | 手动实现 | `MemorySaver` 自动保存 |
| 并行执行 | `multiprocessing` | 内置并行节点支持 |
| 可视化 | 无 | 可导出 Mermaid 图 |
| 重试逻辑 | 手动实现 | 条件边 + 循环 |

## 可视化

```python
# 生成架构图
from IPython.display import Image, display

display(Image(app.get_graph().draw_mermaid_png()))
```

## 运行示例

```
用户: 蒸馏模型

→ Parse Input: 提取 teacher=GPT-4, task=math, student=gemma-4-E4B-it
→ Check Feasibility: score=0.9, reason="推理任务适合4B模型"
→ Human Confirm: [等待用户] 用户选择"继续"
→ Parallel Analysis: Agent A/B/C 同时运行
→ Aggregate: 汇总分析结果
→ Human Review: [等待用户] 用户选择"满意，继续"
→ Generate Data: 合成50K数据
→ Check Quality: score=0.85 (>0.6, proceed)
→ Train: 执行QLoRA训练
→ Evaluate: baseline=65%, distilled=82%
→ Human Final: [等待用户] 用户选择"满意，交付"
→ Deliver: 输出模型和报告
```

---

## 安装依赖

```bash
pip install langgraph langchain langchain-openai
```

## 完整代码

见 `langgraph_version/distill_graph.py`
