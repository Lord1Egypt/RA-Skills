#!/usr/bin/env python3
"""
模型蒸馏的 LangGraph 实现
展示状态管理、并行执行、人机交互、条件分支
"""

import json
import time
from typing import TypedDict, Annotated, List, Optional, Literal
from dataclasses import dataclass, field

# LangGraph 导入
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
from langgraph.constants import Send
from langchain_core.runnables import RunnableConfig


# ============ 1. 状态定义 ============

class DistillState(TypedDict):
    """蒸馏工作流的完整状态"""
    # 输入
    raw_input: str
    teacher_model: str = "gpt-4"
    target_task: str = "general"
    student_model: str = "google/gemma-4-E4B-it"

    # 可行性评估
    feasibility_score: float = 0.0
    feasibility_reason: str = ""
    user_approved: Optional[bool] = None

    # 教师分析（并行收集）
    teacher_analysis: dict = field(default_factory=dict)
    analysis_reviewed: Optional[bool] = None

    # 数据合成
    train_data_path: Optional[str] = None
    eval_data_path: Optional[str] = None
    data_quality_score: float = 0.0

    # 训练
    training_config: Optional[dict] = None
    checkpoint_path: Optional[str] = None

    # 评估
    baseline_metrics: Optional[dict] = None
    distilled_metrics: Optional[dict] = None
    performance_improved: Optional[bool] = None

    # 流程控制
    current_step: str = "init"
    error_message: Optional[str] = None
    retry_count: int = 0

    # 输出
    final_model_path: Optional[str] = None
    deliverables: dict = field(default_factory=dict)


# ============ 2. 节点实现 ============

def parse_input(state: DistillState) -> DistillState:
    """解析用户输入"""
    print("\n" + "="*50)
    print("📋 Step 1: 解析输入")
    print("="*50)

    user_input = state["raw_input"]

    # 简单的意图识别
    if "数学" in user_input or "math" in user_input.lower():
        task = "math"
    elif "代码" in user_input or "code" in user_input.lower():
        task = "code"
    elif "推理" in user_input:
        task = "reasoning"
    else:
        task = "general"

    # 识别教师模型
    if "gpt-4" in user_input.lower():
        teacher = "gpt-4"
    elif "claude" in user_input.lower():
        teacher = "claude-3-opus"
    else:
        teacher = "gpt-4"

    print(f"🎯 目标任务: {task}")
    print(f"👨‍🏫 教师模型: {teacher}")
    print(f"👨‍🎓 学生模型: gemma-4-E4B-it")

    return {
        **state,
        "teacher_model": teacher,
        "target_task": task,
        "student_model": "google/gemma-4-E4B-it",
        "current_step": "parsed"
    }


def check_feasibility(state: DistillState) -> DistillState:
    """评估蒸馏可行性"""
    print("\n" + "="*50)
    print("🔍 Step 2: 可行性评估")
    print("="*50)

    task = state["target_task"]

    # 评估逻辑
    evaluations = {
        "math": (0.9, "数学推理适合4B模型蒸馏"),
        "code": (0.85, "代码能力可以迁移到4B模型"),
        "reasoning": (0.88, "逻辑推理任务蒸馏效果好"),
        "general": (0.6, "通用能力蒸馏挑战较大，建议聚焦特定领域")
    }

    score, reason = evaluations.get(task, (0.5, "未知任务类型"))

    print(f"📊 可行性评分: {score:.0%}")
    print(f"💡 评估建议: {reason}")

    if score < 0.7:
        print("⚠️  建议: 考虑缩小任务范围或选择更大模型")

    return {
        **state,
        "feasibility_score": score,
        "feasibility_reason": reason,
        "current_step": "feasibility_checked"
    }


def human_confirm(state: DistillState) -> DistillState:
    """
    人机交互节点 - 等待用户确认
    在真实环境中，这会暂停等待用户输入
    """
    print("\n" + "="*50)
    print("👤 人机交互: 确认继续")
    print("="*50)
    print(f"\n可行性: {state['feasibility_score']:.0%}")
    print(f"原因: {state['feasibility_reason']}")
    print("\n选项: [继续/调整/取消]")

    # 模拟用户输入（实际使用 interrupt）
    # response = interrupt({"question": "是否继续？", "options": ["继续", "调整", "取消"]})

    # 这里模拟自动继续
    print("✅ 用户选择: 继续")

    return {
        **state,
        "user_approved": True,
        "current_step": "user_confirmed"
    }


# ============ 3. 并行分析节点 ============

def analyze_capability(state: DistillState) -> DistillState:
    """Agent A: 能力边界测绘"""
    print("\n🤖 Agent A: 分析教师能力边界...")
    time.sleep(0.5)  # 模拟工作

    analysis = {
        "overall_accuracy": 0.94,
        "task_coverage": ["algebra", "geometry", "word_problems"],
        "weak_areas": ["complex_proofs", "advanced_calculus"],
        "confidence": "high"
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
    print("\n🤖 Agent B: 提取推理模式...")
    time.sleep(0.5)

    analysis = {
        "reasoning_style": "step_by_step",
        "verification_behavior": True,
        "uncertainty_expression": "explicit",
        "common_patterns": [
            "identify_knowns_and_unknowns",
            "apply_formulas",
            "verify_intermediate_steps"
        ]
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
    print("\n🤖 Agent C: 分离知识与能力...")
    time.sleep(0.5)

    analysis = {
        "transferable_skills": 0.75,
        "pure_knowledge": 0.25,
        "recommendation": "Focus on problem-solving patterns, not memorized formulas"
    }

    return {
        **state,
        "teacher_analysis": {
            **state.get("teacher_analysis", {}),
            "knowledge_split": analysis
        }
    }


def aggregate_analysis(state: DistillState) -> DistillState:
    """汇总并行分析结果"""
    print("\n" + "="*50)
    print("📊 Step 3: 分析结果汇总")
    print("="*50)

    analysis = state["teacher_analysis"]

    print("\n教师模型分析:")
    print(f"  - 能力覆盖: {', '.join(analysis['capability']['task_coverage'])}")
    print(f"  - 推理风格: {analysis['reasoning']['reasoning_style']}")
    print(f"  - 可迁移能力: {analysis['knowledge_split']['transferable_skills']:.0%}")

    return {
        **state,
        "current_step": "analysis_complete"
    }


def start_parallel_analysis(state: DistillState) -> List[Send]:
    """启动并行的教师分析"""
    print("\n🚀 启动并行分析...")
    return [
        Send("analyze_capability", state),
        Send("analyze_reasoning", state),
        Send("analyze_knowledge", state),
    ]


# ============ 4. 数据合成与训练 ============

def generate_training_data(state: DistillState) -> DistillState:
    """生成训练数据"""
    print("\n" + "="*50)
    print("📝 Step 4: 数据合成")
    print("="*50)

    task = state["target_task"]

    # 模拟数据生成
    data_sizes = {"math": 50000, "code": 30000, "reasoning": 40000, "general": 100000}
    size = data_sizes.get(task, 50000)

    print(f"生成 {size} 条训练数据...")
    for i in range(5):
        time.sleep(0.2)
        print(f"  进度: {(i+1)*20}%")

    # 模拟质量评估
    quality = 0.85

    print(f"✅ 数据质量评分: {quality:.0%}")

    return {
        **state,
        "train_data_path": f"./data/{task}_train_{size}.jsonl",
        "eval_data_path": f"./data/{task}_eval_{size//10}.jsonl",
        "data_quality_score": quality,
        "current_step": "data_generated"
    }


def check_data_quality(state: DistillState) -> DistillState:
    """检查数据质量"""
    score = state["data_quality_score"]

    print(f"\n📊 数据质量检查: {score:.0%}")

    if score < 0.6:
        print("❌ 数据质量不足，需要重新生成")
        return {
            **state,
            "current_step": "data_quality_failed",
            "error_message": "Data quality too low"
        }

    print("✅ 数据质量通过")
    return {**state, "current_step": "data_quality_ok"}


def train_model(state: DistillState) -> DistillState:
    """执行模型训练"""
    print("\n" + "="*50)
    print("🚀 Step 5: 模型训练")
    print("="*50)

    config = {
        "method": "qlora",
        "epochs": 3,
        "batch_size": 8,
        "learning_rate": 2e-5,
        "student": state["student_model"],
        "teacher": state["teacher_model"]
    }

    print(f"训练配置:")
    print(f"  - 方法: {config['method']}")
    print(f"  - 轮数: {config['epochs']}")
    print(f"  - 学习率: {config['learning_rate']}")

    # 模拟训练过程
    print("\n训练进度:")
    for epoch in range(1, config["epochs"] + 1):
        time.sleep(0.5)
        loss = 2.5 / epoch
        print(f"  Epoch {epoch}/{config['epochs']}: loss={loss:.4f}")

    checkpoint = "./outputs/checkpoints/final_model"
    print(f"\n✅ 训练完成，模型保存至: {checkpoint}")

    return {
        **state,
        "training_config": config,
        "checkpoint_path": checkpoint,
        "current_step": "training_complete"
    }


def evaluate_model(state: DistillState) -> DistillState:
    """评估模型效果"""
    print("\n" + "="*50)
    print("📊 Step 6: 效果评估")
    print("="*50)

    # 模拟基线评估
    baseline = {"accuracy": 0.65, "f1": 0.63}

    # 模拟蒸馏后评估（根据任务类型）
    task = state["target_task"]
    improvements = {"math": 0.18, "code": 0.15, "reasoning": 0.16, "general": 0.10}
    improvement = improvements.get(task, 0.12)

    distilled = {
        "accuracy": baseline["accuracy"] + improvement,
        "f1": baseline["f1"] + improvement * 0.9
    }

    improved = distilled["accuracy"] > baseline["accuracy"]

    print(f"\n性能对比:")
    print(f"  基线模型:    {baseline['accuracy']:.1%}")
    print(f"  蒸馏后模型:  {distilled['accuracy']:.1%} (+{improvement:.1%})")
    print(f"  性能提升:    {'✅' if improved else '❌'}")

    return {
        **state,
        "baseline_metrics": baseline,
        "distilled_metrics": distilled,
        "performance_improved": improved,
        "current_step": "evaluation_complete"
    }


# ============ 5. 条件边函数 ============

def should_continue(state: DistillState) -> str:
    """根据可行性决定是否继续"""
    if state.get("user_approved") is True:
        return "continue"
    elif state.get("retry_count", 0) > 2:
        return "give_up"
    else:
        return "refine"


def check_quality(state: DistillState) -> str:
    """检查数据质量分支"""
    if state["data_quality_score"] >= 0.6:
        return "proceed"
    else:
        return "retry"


def check_result(state: DistillState) -> str:
    """检查训练结果"""
    if state.get("performance_improved"):
        return "deliver"
    elif state.get("retry_count", 0) < 2:
        return "retry"
    else:
        return "deliver_anyway"


def route_after_confirm(state: DistillState) -> Literal["analyze_capability", "parse_input", END]:
    """用户确认后的路由"""
    if state.get("user_approved") is True:
        return "analyze_capability"
    elif state.get("retry_count", 0) > 3:
        return END
    else:
        return "parse_input"


# ============ 6. 最终交付 ============

def deliver_model(state: DistillState) -> DistillState:
    """交付最终模型"""
    print("\n" + "="*50)
    print("🎉 蒸馏完成！")
    print("="*50)

    deliverables = {
        "model_path": state["checkpoint_path"],
        "config": state["training_config"],
        "baseline": state["baseline_metrics"],
        "final": state["distilled_metrics"],
        "analysis": state["teacher_analysis"]
    }

    print("\n交付物:")
    print(f"  📦 模型: {deliverables['model_path']}")
    print(f"  📊 基线性能: {deliverables['baseline']['accuracy']:.1%}")
    print(f"  🚀 最终性能: {deliverables['final']['accuracy']:.1%}")
    print(f"  📈 提升: {deliverables['final']['accuracy'] - deliverables['baseline']['accuracy']:.1%}")

    return {
        **state,
        "final_model_path": state["checkpoint_path"],
        "deliverables": deliverables,
        "current_step": "delivered"
    }


# ============ 7. 构建图 ============

def create_distill_graph():
    """创建并编译蒸馏工作流图"""

    # 初始化
    workflow = StateGraph(DistillState)

    # 添加节点
    workflow.add_node("parse_input", parse_input)
    workflow.add_node("check_feasibility", check_feasibility)
    workflow.add_node("human_confirm", human_confirm)
    workflow.add_node("analyze_capability", analyze_capability)
    workflow.add_node("analyze_reasoning", analyze_reasoning)
    workflow.add_node("analyze_knowledge", analyze_knowledge)
    workflow.add_node("aggregate_analysis", aggregate_analysis)
    workflow.add_node("generate_data", generate_training_data)
    workflow.add_node("check_quality", check_data_quality)
    workflow.add_node("train", train_model)
    workflow.add_node("evaluate", evaluate_model)
    workflow.add_node("deliver", deliver_model)

    # 设置入口
    workflow.set_entry_point("parse_input")

    # 添加边
    workflow.add_edge("parse_input", "check_feasibility")
    workflow.add_edge("check_feasibility", "human_confirm")

    # 条件边：用户确认后
    workflow.add_conditional_edges(
        "human_confirm",
        route_after_confirm,
        {
            "analyze_capability": "analyze_capability",
            "parse_input": "parse_input",
            END: END
        }
    )

    # 并行分析（使用Send）
    workflow.add_conditional_edges(
        "analyze_capability",
        start_parallel_analysis,
        ["analyze_capability", "analyze_reasoning", "analyze_knowledge"]
    )

    # 汇总
    workflow.add_edge("analyze_capability", "aggregate_analysis")
    workflow.add_edge("analyze_reasoning", "aggregate_analysis")
    workflow.add_edge("analyze_knowledge", "aggregate_analysis")

    # 继续流程
    workflow.add_edge("aggregate_analysis", "generate_data")
    workflow.add_edge("generate_data", "check_quality")

    # 质量检查分支
    workflow.add_conditional_edges(
        "check_quality",
        check_quality,
        {
            "proceed": "train",
            "retry": "generate_data"
        }
    )

    workflow.add_edge("train", "evaluate")

    # 评估结果分支
    workflow.add_conditional_edges(
        "evaluate",
        check_result,
        {
            "deliver": "deliver",
            "retry": "train",
            "deliver_anyway": "deliver"
        }
    )

    workflow.add_edge("deliver", END)

    # 添加记忆（支持断点续传）
    checkpointer = MemorySaver()

    return workflow.compile(checkpointer=checkpointer)


# ============ 8. 运行示例 ============

def main():
    """运行示例"""
    print("\n" + "="*60)
    print("🚀 模型蒸馏 - LangGraph 版本")
    print("="*60)

    # 创建图
    app = create_distill_graph()

    # 初始状态
    initial_state = DistillState(
        raw_input="把GPT-4的数学推理能力蒸馏到gemma-4-E4B-it"
    )

    # 配置（用于断点续传）
    config = {"configurable": {"thread_id": "distill_demo_001"}}

    # 运行
    print("\n开始执行蒸馏工作流...")
    print("-" * 60)

    for event in app.stream(initial_state, config, stream_mode="updates"):
        # 打印每个节点的更新
        for node_name, state_update in event.items():
            if node_name != "__end__":
                print(f"\n[Node: {node_name}] 完成")

    # 获取最终结果
    final_state = app.get_state(config)

    print("\n" + "="*60)
    print("✅ 工作流执行完成！")
    print("="*60)

    if final_state and final_state.values.get("deliverables"):
        print("\n最终交付物:")
        print(json.dumps(final_state.values["deliverables"], indent=2, ensure_ascii=False))

    return final_state


if __name__ == "__main__":
    main()
