#!/usr/bin/env python3
"""
OpenClaw 模型路由器
智能模型选择和路由策略
"""

import json
import os
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum


class TaskType(Enum):
    """任务类型枚举"""
    CODING = "coding"
    ANALYSIS = "analysis"
    WRITING = "writing"
    RESEARCH = "research"
    GENERAL = "general"
    MATH = "math"
    TRANSLATION = "translation"


@dataclass
class ModelCapability:
    """模型能力描述"""
    model_id: str
    strengths: List[str]
    max_context: int
    cost_per_1k: float
    speed_score: int  # 1-10
    reasoning_score: int  # 1-10
    coding_score: int  # 1-10


class ModelRouter:
    """智能模型路由器"""
    
    def __init__(self, config_path: str = None):
        self.config_path = config_path or os.path.expanduser("~/.openclaw/openclaw.json")
        self.config = None
        
        # 模型能力数据库
        self.model_capabilities = {
            "qwen/qwen3.5-plus": ModelCapability(
                model_id="qwen/qwen3.5-plus",
                strengths=["general", "analysis", "writing"],
                max_context=256000,
                cost_per_1k=0.004,
                speed_score=7,
                reasoning_score=8,
                coding_score=7
            ),
            "qwen/qwen3-coder-plus": ModelCapability(
                model_id="qwen/qwen3-coder-plus",
                strengths=["coding", "debugging"],
                max_context=256000,
                cost_per_1k=0.008,
                speed_score=6,
                reasoning_score=7,
                coding_score=10
            ),
            "deepseek/deepseek-chat": ModelCapability(
                model_id="deepseek/deepseek-chat",
                strengths=["general", "coding", "math"],
                max_context=128000,
                cost_per_1k=0.001,
                speed_score=8,
                reasoning_score=7,
                coding_score=8
            ),
            "qwen/qwen-turbo": ModelCapability(
                model_id="qwen/qwen-turbo",
                strengths=["general", "fast"],
                max_context=128000,
                cost_per_1k=0.0004,
                speed_score=10,
                reasoning_score=5,
                coding_score=5
            ),
            "ollama/qwen3.5": ModelCapability(
                model_id="ollama/qwen3.5",
                strengths=["local", "privacy"],
                max_context=32000,
                cost_per_1k=0.0,
                speed_score=9,
                reasoning_score=6,
                coding_score=6
            )
        }
        
        # 任务类型到模型能力的映射权重
        self.task_weights = {
            TaskType.CODING: {"coding_score": 0.5, "reasoning_score": 0.3, "speed_score": 0.2},
            TaskType.ANALYSIS: {"reasoning_score": 0.5, "coding_score": 0.2, "speed_score": 0.3},
            TaskType.WRITING: {"speed_score": 0.4, "reasoning_score": 0.3, "coding_score": 0.3},
            TaskType.RESEARCH: {"reasoning_score": 0.6, "coding_score": 0.2, "speed_score": 0.2},
            TaskType.GENERAL: {"speed_score": 0.4, "reasoning_score": 0.3, "coding_score": 0.3},
            TaskType.MATH: {"reasoning_score": 0.6, "coding_score": 0.3, "speed_score": 0.1},
            TaskType.TRANSLATION: {"speed_score": 0.6, "reasoning_score": 0.2, "coding_score": 0.2}
        }
    
    def load_config(self) -> bool:
        """加载配置文件"""
        try:
            if not os.path.exists(self.config_path):
                return False
            
            with open(self.config_path, 'r', encoding='utf-8') as f:
                self.config = json.load(f)
            return True
        except Exception:
            return False
    
    def select_best_model(self, task: Dict) -> Tuple[str, Optional[str]]:
        """
        根据任务需求选择最佳模型
        
        Args:
            task: 任务描述字典，包含:
                - task_type: 任务类型
                - context_length: 上下文长度需求
                - budget_constraint: 预算限制 (low/medium/high)
                - speed_priority: 速度优先级 (1-10)
                - requires_reasoning: 是否需要推理
                - requires_coding: 是否需要编程
        
        Returns:
            (model_id, thinking_mode) 元组
        """
        task_type = TaskType(task.get("task_type", "general"))
        context_length = task.get("context_length", 4000)
        budget = task.get("budget_constraint", "medium")
        speed_priority = task.get("speed_priority", 5)
        requires_reasoning = task.get("requires_reasoning", False)
        requires_coding = task.get("requires_coding", False)
        
        weights = self.task_weights.get(task_type, self.task_weights[TaskType.GENERAL])
        
        best_model = None
        best_score = -1
        best_thinking = None
        
        for model_id, capability in self.model_capabilities.items():
            # 检查上下文长度
            if capability.max_context < context_length:
                continue
            
            # 计算综合得分
            score = 0
            score += capability.coding_score * weights.get("coding_score", 0.3)
            score += capability.reasoning_score * weights.get("reasoning_score", 0.3)
            score += capability.speed_score * weights.get("speed_score", 0.3)
            
            # 预算调整
            if budget == "low":
                score *= (1.0 - capability.cost_per_1k * 10)
            elif budget == "high":
                score *= (1.0 + capability.cost_per_1k * 5)
            
            # 速度优先级调整
            if speed_priority >= 8:
                score *= (capability.speed_score / 10.0)
            
            # 特殊需求调整
            if requires_reasoning and capability.reasoning_score < 6:
                score *= 0.5
            if requires_coding and capability.coding_score < 6:
                score *= 0.5
            
            if score > best_score:
                best_score = score
                best_model = model_id
                best_thinking = "stream" if requires_reasoning and capability.reasoning_score >= 7 else None
        
        # 默认 fallback
        if best_model is None:
            best_model = "deepseek/deepseek-chat"
        
        return best_model, best_thinking
    
    def analyze_model_usage(self) -> Dict:
        """分析当前模型使用情况"""
        if not self.config:
            return {"error": "配置未加载"}
        
        agents = self.config.get("agents", {}).get("list", [])
        defaults = self.config.get("agents", {}).get("defaults", {})
        
        usage = {
            "total_agents": len(agents),
            "model_distribution": {},
            "cost_estimate": 0.0,
            "recommendations": []
        }
        
        # 统计模型使用
        for agent in agents:
            model = agent.get("model", {})
            if isinstance(model, str):
                model = {"primary": model}
            
            primary = model.get("primary", "unknown")
            usage["model_distribution"][primary] = usage["model_distribution"].get(primary, 0) + 1
            
            # 成本估算
            if primary in self.model_capabilities:
                usage["cost_estimate"] += self.model_capabilities[primary].cost_per_1k * 100  # 假设每 agent 100k tokens
        
        # 生成建议
        for model_id, count in usage["model_distribution"].items():
            if model_id in self.model_capabilities:
                cap = self.model_capabilities[model_id]
                if cap.cost_per_1k > 0.005 and count > 1:
                    usage["recommendations"].append({
                        "type": "cost_optimization",
                        "message": f"考虑将 {count} 个使用 {model_id} 的 Agent 切换到更经济的模型",
                        "potential_saving": f"{(cap.cost_per_1k - 0.001) * 100 * count:.2f} 元/月"
                    })
        
        return usage
    
    def generate_routing_config(self) -> Dict:
        """生成推荐的路由配置"""
        routing = {
            "rules": [],
            "fallback_chain": []
        }
        
        # 基于任务类型的路由规则
        routing["rules"].append({
            "condition": {"task_type": "coding"},
            "model": "qwen/qwen3-coder-plus",
            "thinking": "stream"
        })
        
        routing["rules"].append({
            "condition": {"task_type": "research", "requires_reasoning": True},
            "model": "qwen/qwen3.5-plus",
            "thinking": "stream"
        })
        
        routing["rules"].append({
            "condition": {"budget_constraint": "low"},
            "model": "deepseek/deepseek-chat",
            "thinking": None
        })
        
        routing["rules"].append({
            "condition": {"speed_priority": 8},
            "model": "qwen/qwen-turbo",
            "thinking": None
        })
        
        # Fallback 链
        routing["fallback_chain"] = [
            "qwen/qwen3.5-plus",
            "deepseek/deepseek-chat",
            "qwen/qwen-turbo",
            "ollama/qwen3.5"
        ]
        
        return routing
    
    def optimize_provider_config(self) -> Dict:
        """优化 Provider 配置"""
        if not self.config:
            return {"error": "配置未加载"}
        
        providers = self.config.get("models", {}).get("providers", {})
        optimizations = {"added_retry_config": [], "added_timeout": [], "suggestions": []}
        
        for provider_name, provider_config in providers.items():
            # 添加重试配置
            if "retry" not in provider_config:
                provider_config["retry"] = {
                    "maxAttempts": 3,
                    "backoffMs": 1000
                }
                optimizations["added_retry_config"].append(provider_name)
            
            # 添加超时配置
            if "timeout" not in provider_config:
                provider_config["timeout"] = 60000  # 60 秒
                optimizations["added_timeout"].append(provider_name)
            
            # 网络问题建议
            if provider_name in ["feishu", "qwen"] and "baseUrl" in provider_config:
                optimizations["suggestions"].append(
                    f"提供商 {provider_name} 需要网络连接，请确保 DNS 解析正常"
                )
        
        return {
            "optimized_providers": providers,
            "changes": optimizations
        }
    
    def generate_optimization_report(self) -> Dict:
        """生成模型路由优化报告"""
        usage_analysis = self.analyze_model_usage()
        routing_config = self.generate_routing_config()
        provider_optimizations = self.optimize_provider_config()
        
        # 生成模型选择建议
        sample_tasks = [
            {"task_type": "coding", "context_length": 8000, "budget_constraint": "low"},
            {"task_type": "research", "context_length": 50000, "requires_reasoning": True},
            {"task_type": "writing", "context_length": 4000, "speed_priority": 8},
            {"task_type": "analysis", "context_length": 12000, "requires_reasoning": True}
        ]
        
        model_selections = {}
        for i, task in enumerate(sample_tasks):
            model_id, thinking = self.select_best_model(task)
            model_selections[f"task_{i+1}"] = {
                "requirements": task,
                "recommended_model": model_id,
                "thinking_mode": thinking
            }
        
        return {
            "current_usage": usage_analysis,
            "recommended_routing": routing_config,
            "provider_optimizations": provider_optimizations,
            "sample_selections": model_selections,
            "total_recommendations": len(usage_analysis.get("recommendations", []))
        }


def main():
    """命令行入口"""
    import argparse
    
    parser = argparse.ArgumentParser(description="OpenClaw 模型路由器")
    parser.add_argument("action", choices=["analyze", "route", "optimize", "report"],
                       help="执行动作：analyze(分析), route(路由), optimize(优化), report(报告)")
    parser.add_argument("--task-type", choices=["coding", "analysis", "writing", "research", "general"],
                       help="任务类型（用于 route 动作）")
    parser.add_argument("--context-length", type=int, default=4000,
                       help="上下文长度需求（用于 route 动作）")
    parser.add_argument("--requires-images", action="store_true",
                       help="是否需要图像理解（用于 route 动作）")
    parser.add_argument("--config", default=None,
                       help="配置文件路径")
    parser.add_argument("--json", action="store_true",
                       help="输出 JSON 格式")
    
    args = parser.parse_args()
    
    router = ModelRouter(config_path=args.config)
    
    if args.action == "analyze":
        if router.load_config():
            result = router.analyze_model_usage()
        else:
            result = {"error": "无法加载配置"}
    
    elif args.action == "route":
        task = {
            "task_type": args.task_type or "general",
            "context_length": args.context_length,
            "requires_images": args.requires_images
        }
        model, thinking = router.select_best_model(task)
        result = {
            "recommended_model": model,
            "thinking_mode": thinking,
            "task": task
        }
    
    elif args.action == "optimize":
        if router.load_config():
            result = router.generate_optimization_report()
        else:
            result = {"error": "无法加载配置"}
    
    elif args.action == "report":
        if router.load_config():
            result = router.generate_optimization_report()
        else:
            result = {"error": "无法加载配置"}
    
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
