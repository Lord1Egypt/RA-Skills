#!/usr/bin/env python3
"""
OpenClaw Agent/Workflow 编排专家系统
THE WORKFLOW ORCHESTRATION EXPERT - 专业的节点编排与流程设计

作者：ProClaw
网站：www.ProClaw.top
联系方式：wechat:Mr-zifang

功能：
1. Agent 创建与管理
2. Workflow 编排设计
3. 节点类型详解
4. 变量与上下文管理
5. 条件与循环控制
"""

import os
import sys
import json
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from enum import Enum


# =============================================================================
# 节点类型定义
# =============================================================================

class NodeType(Enum):
    """节点类型枚举"""
    # 核心节点
    LLM = "llm"                    # 大语言模型节点
    TOOL = "tool"                  # 工具调用节点
    ACTION = "action"              # 动作执行节点
    CONDITION = "condition"        # 条件判断节点
    LOOP = "loop"                  # 循环控制节点
    
    # 数据节点
    INPUT = "input"                # 输入节点
    OUTPUT = "output"              # 输出节点
    TRANSFORM = "transform"        # 数据转换节点
    FILTER = "filter"              # 数据过滤节点
    
    # 高级节点
    MEMORY = "memory"              # 记忆存储节点
    RETRIEVAL = "retrieval"        # 记忆检索节点
    WEBHOOK = "webhook"            # Webhook 节点
    PARALLEL = "parallel"          # 并行执行节点
    MERGE = "merge"                # 结果合并节点


class NodeCategory(Enum):
    """节点分类"""
    CORE = "core"                  # 核心节点
    DATA = "data"                  # 数据节点
    CONTROL = "control"            # 控制节点
    MEMORY = "memory"              # 记忆节点
    INTEGRATION = "integration"    # 集成节点


# =============================================================================
# 节点模板库
# =============================================================================

class NodeTemplates:
    """节点模板库"""

    @staticmethod
    def llm_node(
        model: str = "gpt-4o",
        prompt: str = "",
        temperature: float = 0.7,
        max_tokens: int = 4096,
        system_prompt: str = ""
    ) -> Dict:
        """LLM 节点模板"""
        return {
            "type": NodeType.LLM.value,
            "config": {
                "model": model,
                "prompt": prompt,
                "system_prompt": system_prompt,
                "parameters": {
                    "temperature": temperature,
                    "max_tokens": max_tokens,
                    "top_p": 0.9,
                    "frequency_penalty": 0.0,
                    "presence_penalty": 0.0
                }
            }
        }

    @staticmethod
    def tool_node(
        tool_name: str,
        tool_input: Dict = None,
        timeout: int = 30
    ) -> Dict:
        """工具节点模板"""
        return {
            "type": NodeType.TOOL.value,
            "config": {
                "tool": tool_name,
                "input": tool_input or {},
                "timeout": timeout,
                "retry": {
                    "enabled": True,
                    "max_attempts": 3,
                    "backoff": "exponential"
                }
            }
        }

    @staticmethod
    def condition_node(
        conditions: List[Dict] = None,
        default_branch: str = "false"
    ) -> Dict:
        """条件节点模板"""
        return {
            "type": NodeType.CONDITION.value,
            "config": {
                "conditions": conditions or [
                    {
                        "expression": "{{input.value}} > 0",
                        "operator": "gt",
                        "value": 0,
                        "branch": "true"
                    }
                ],
                "default_branch": default_branch,
                "branches": {
                    "true": {"next": None},
                    "false": {"next": None}
                }
            }
        }

    @staticmethod
    def loop_node(
        loop_type: str = "for",  # for / while / do_while
        max_iterations: int = 100,
        items_path: str = "{{items}}"
    ) -> Dict:
        """循环节点模板"""
        return {
            "type": NodeType.LOOP.value,
            "config": {
                "loop_type": loop_type,
                "max_iterations": max_iterations,
                "items_path": items_path,
                "loop_variable": "item",
                "body": {"nodes": []}
            }
        }

    @staticmethod
    def memory_node(
        operation: str = "store",  # store / clear
        content_path: str = "{{output}}",
        metadata: Dict = None
    ) -> Dict:
        """记忆节点模板"""
        return {
            "type": NodeType.MEMORY.value,
            "config": {
                "operation": operation,
                "content_path": content_path,
                "metadata": metadata or {},
                "ttl": None  # 永不过期
            }
        }

    @staticmethod
    def retrieval_node(
        query: str = "{{query}}",
        top_k: int = 5,
        score_threshold: float = 0.7
    ) -> Dict:
        """记忆检索节点模板"""
        return {
            "type": NodeType.RETRIEVAL.value,
            "config": {
                "query": query,
                "top_k": top_k,
                "score_threshold": score_threshold,
                "include_metadata": True
            }
        }

    @staticmethod
    def parallel_node(
        tasks: List[Dict] = None
    ) -> Dict:
        """并行执行节点模板"""
        return {
            "type": NodeType.PARALLEL.value,
            "config": {
                "tasks": tasks or [],
                "concurrency": "all",  # all / limited
                "max_concurrent": 10,
                "fail_fast": True
            }
        }

    @staticmethod
    def webhook_node(
        url: str,
        method: str = "POST",
        headers: Dict = None,
        body_template: Dict = None
    ) -> Dict:
        """Webhook 节点模板"""
        return {
            "type": NodeType.WEBHOOK.value,
            "config": {
                "url": url,
                "method": method,
                "headers": headers or {"Content-Type": "application/json"},
                "body_template": body_template or {},
                "timeout": 30
            }
        }


# =============================================================================
# Agent 模板库
# =============================================================================

class AgentTemplates:
    """Agent 模板库"""

    @staticmethod
    def basic_chat_agent(
        name: str = "ChatBot",
        model: str = "gpt-4o",
        system_prompt: str = "你是一个友好的AI助手"
    ) -> Dict:
        """基础对话 Agent"""
        return {
            "name": name,
            "type": "agent",
            "config": {
                "model": model,
                "system_prompt": system_prompt,
                "workflow": {
                    "nodes": [
                        {
                            "id": "input",
                            "type": "input",
                            "config": {"input_schema": {"message": "string"}}
                        },
                        {
                            "id": "llm",
                            "type": "llm",
                            "config": {
                                "model": model,
                                "prompt": "{{input.message}}",
                                "system_prompt": system_prompt
                            }
                        },
                        {
                            "id": "output",
                            "type": "output",
                            "config": {"output_schema": {"response": "string"}}
                        }
                    ],
                    "edges": [
                        {"from": "input", "to": "llm"},
                        {"from": "llm", "to": "output"}
                    ]
                }
            }
        }

    @staticmethod
    def tool_calling_agent(
        name: str = "ToolAgent",
        model: str = "gpt-4o",
        tools: List[str] = None
    ) -> Dict:
        """工具调用 Agent"""
        return {
            "name": name,
            "type": "agent",
            "config": {
                "model": model,
                "system_prompt": "你是一个专业的助手，可以调用各种工具来完成任务。",
                "tools": tools or ["search", "calculator", "web_fetch"],
                "workflow": {
                    "nodes": [
                        {"id": "input", "type": "input"},
                        {"id": "llm", "type": "llm"},
                        {"id": "tool_call", "type": "tool"},
                        {"id": "output", "type": "output"}
                    ],
                    "edges": [
                        {"from": "input", "to": "llm"},
                        {"from": "llm", "to": "tool_call"},
                        {"from": "tool_call", "to": "output"}
                    ]
                }
            }
        }

    @staticmethod
    def data_processing_agent(
        name: str = "DataProcessor",
        model: str = "gpt-4o",
        steps: List[str] = None
    ) -> Dict:
        """数据处理 Agent"""
        steps = steps or ["validate", "transform", "aggregate", "output"]
        
        nodes = [{"id": "input", "type": "input"}]
        edges = []
        
        prev_id = "input"
        for i, step in enumerate(steps):
            node_id = f"step_{i}"
            nodes.append({
                "id": node_id,
                "type": "action",
                "config": {"operation": step}
            })
            edges.append({"from": prev_id, "to": node_id})
            prev_id = node_id
        
        nodes.append({"id": "output", "type": "output"})
        edges.append({"from": prev_id, "to": "output"})
        
        return {
            "name": name,
            "type": "agent",
            "config": {
                "model": model,
                "workflow": {"nodes": nodes, "edges": edges}
            }
        }


# =============================================================================
# Workflow 模板库
# =============================================================================

class WorkflowTemplates:
    """Workflow 模板库"""

    @staticmethod
    def sequential_workflow(
        name: str,
        nodes: List[Dict]
    ) -> Dict:
        """顺序执行 Workflow"""
        edges = []
        for i in range(len(nodes) - 1):
            edges.append({
                "from": nodes[i]["id"],
                "to": nodes[i + 1]["id"]
            })
        
        return {
            "name": name,
            "type": "workflow",
            "workflow_type": "sequential",
            "nodes": nodes,
            "edges": edges
        }

    @staticmethod
    def conditional_workflow(
        name: str,
        conditions: List[Dict],
        branches: Dict
    ) -> Dict:
        """条件分支 Workflow"""
        return {
            "name": name,
            "type": "workflow",
            "workflow_type": "conditional",
            "nodes": [
                {"id": "input", "type": "input"},
                {"id": "condition", "type": "condition"},
                *branches.get("true_nodes", []),
                *branches.get("false_nodes", []),
                {"id": "output", "type": "output"}
            ],
            "edges": [
                {"from": "input", "to": "condition"},
                {"from": "condition", "to": "branch_true", "condition": "true"},
                {"from": "condition", "to": "branch_false", "condition": "false"}
            ],
            "config": {
                "conditions": conditions
            }
        }

    @staticmethod
    def parallel_workflow(
        name: str,
        parallel_tasks: List[Dict]
    ) -> Dict:
        """并行执行 Workflow"""
        nodes = [
            {"id": "input", "type": "input"},
            {"id": "dispatch", "type": "parallel"},
            *parallel_tasks,
            {"id": "merge", "type": "merge"},
            {"id": "output", "type": "output"}
        ]
        
        return {
            "name": name,
            "type": "workflow",
            "workflow_type": "parallel",
            "nodes": nodes,
            "edges": [
                {"from": "input", "to": "dispatch"},
                *[
                    {"from": "dispatch", "to": f"task_{i}", "branch": i}
                    for i in range(len(parallel_tasks))
                ],
                *[
                    {"from": f"task_{i}", "to": "merge"}
                    for i in range(len(parallel_tasks))
                ],
                {"from": "merge", "to": "output"}
            ]
        }

    @staticmethod
    def loop_workflow(
        name: str,
        loop_body: List[Dict],
        condition: str = "{{items}}"
    ) -> Dict:
        """循环执行 Workflow"""
        return {
            "name": name,
            "type": "workflow",
            "workflow_type": "loop",
            "nodes": [
                {"id": "input", "type": "input"},
                {"id": "loop", "type": "loop"},
                {"id": "output", "type": "output"}
            ],
            "edges": [
                {"from": "input", "to": "loop"},
                {"from": "loop", "to": "output"}
            ],
            "config": {
                "loop_condition": condition,
                "loop_body": loop_body,
                "max_iterations": 100
            }
        }


# =============================================================================
# 编排模式库
# =============================================================================

class OrchestrationPatterns:
    """编排模式库"""

    @staticmethod
    def router_pattern(
        routes: List[Dict]
    ) -> Dict:
        """
        路由器模式 - 根据输入路由到不同处理分支
        
        适用场景：
        -意图识别后路由
        -内容分类处理
        -多语言处理
        """
        return {
            "pattern": "router",
            "description": "根据条件路由到不同处理分支",
            "nodes": [
                {"id": "input", "type": "input"},
                {"id": "classifier", "type": "llm", "config": {
                    "prompt": "分类以下输入：{{input}}",
                    "system_prompt": "你是一个分类器，输出 JSON: {\"category\": \"...\"}"
                }},
                {"id": "router", "type": "condition", "config": {"routes": routes}},
                {"id": "handler_1", "type": "action"},
                {"id": "handler_2", "type": "action"},
                {"id": "handler_3", "type": "action"},
                {"id": "output", "type": "output"}
            ],
            "edges": [
                {"from": "input", "to": "classifier"},
                {"from": "classifier", "to": "router"},
                {"from": "router", "to": "handler_1", "condition": "category=handler_1"},
                {"from": "router", "to": "handler_2", "condition": "category=handler_2"},
                {"from": "router", "to": "handler_3", "condition": "category=handler_3"},
                {"from": "handler_1", "to": "output"},
                {"from": "handler_2", "to": "output"},
                {"from": "handler_3", "to": "output"}
            ]
        }

    @staticmethod
    def pipeline_pattern(
        stages: List[str]
    ) -> Dict:
        """
        流水线模式 - 顺序执行多个处理阶段
        
        适用场景：
        - 数据清洗 ETL
        - 多步骤处理流程
        - 审批流程
        """
        nodes = [{"id": "input", "type": "input"}]
        edges = []
        
        for i, stage in enumerate(stages):
            node_id = f"stage_{i}"
            nodes.append({
                "id": node_id,
                "type": "action",
                "config": {"operation": stage}
            })
            if i == 0:
                edges.append({"from": "input", "to": node_id})
            else:
                edges.append({"from": f"stage_{i-1}", "to": node_id})
        
        nodes.append({"id": "output", "type": "output"})
        edges.append({"from": stages[-1], "to": "output"})
        
        return {
            "pattern": "pipeline",
            "description": "顺序执行多个处理阶段",
            "nodes": nodes,
            "edges": edges
        }

    @staticmethod
    def fan_out_fan_in_pattern(
        task_generator: str,
        task_handler: str,
        aggregation: str
    ) -> Dict:
        """
        扇出扇入模式 - 并行处理后聚合结果
        
        适用场景：
        - 批量处理
        - 并行搜索
        - 分布式计算
        """
        return {
            "pattern": "fan_out_fan_in",
            "description": "并行处理任务后聚合结果",
            "nodes": [
                {"id": "input", "type": "input"},
                {"id": "generate", "type": "action", "config": {"operation": task_generator}},
                {"id": "parallel", "type": "parallel", "config": {"task_handler": task_handler}},
                {"id": "aggregate", "type": "action", "config": {"operation": aggregation}},
                {"id": "output", "type": "output"}
            ],
            "edges": [
                {"from": "input", "to": "generate"},
                {"from": "generate", "to": "parallel"},
                {"from": "parallel", "to": "aggregate"},
                {"from": "aggregate", "to": "output"}
            ]
        }

    @staticmethod
    def saga_pattern(
        steps: List[Dict]
    ) -> Dict:
        """
        Saga 模式 - 长事务处理
        
        适用场景：
        - 分布式事务
        - 跨系统操作
        - 需要回滚的操作序列
        """
        nodes = [{"id": "input", "type": "input"}]
        edges = []
        
        for i, step in enumerate(steps):
            node_id = f"step_{i}"
            compensation_id = f"compensate_{i}"
            
            nodes.append({
                "id": node_id,
                "type": "action",
                "config": {"operation": step["action"]}
            })
            nodes.append({
                "id": compensation_id,
                "type": "action",
                "config": {"operation": step["compensation"]}
            })
            
            if i == 0:
                edges.append({"from": "input", "to": node_id})
            else:
                edges.append({"from": f"step_{i-1}", "to": node_id})
            
            edges.append({
                "from": node_id,
                "to": compensation_id,
                "condition": "failed"
            })
        
        nodes.append({"id": "output", "type": "output"})
        edges.append({"from": steps[-1]["action"], "to": "output"})
        
        return {
            "pattern": "saga",
            "description": "长事务处理与回滚",
            "nodes": nodes,
            "edges": edges
        }


# =============================================================================
# Workflow 专家系统
# =============================================================================

class WorkflowExpert:
    """
    Workflow 编排专家系统
    
    提供专业级的 Workflow 设计和编排服务
    """

    def __init__(self):
        self.node_templates = NodeTemplates()
        self.agent_templates = AgentTemplates()
        self.workflow_templates = WorkflowTemplates()
        self.patterns = OrchestrationPatterns()

    def create_agent(
        self,
        name: str,
        agent_type: str = "chat",
        model: str = "gpt-4o",
        **kwargs
    ) -> Dict:
        """
        创建 Agent
        
        Args:
            name: Agent 名称
            agent_type: Agent 类型 (chat/tool_calling/data_processing)
            model: 使用的模型
            **kwargs: 其他配置参数
        """
        templates = {
            "chat": self.agent_templates.basic_chat_agent,
            "tool_calling": self.agent_templates.tool_calling_agent,
            "data_processing": self.agent_templates.data_processing_agent
        }
        
        creator = templates.get(agent_type, self.agent_templates.basic_chat_agent)
        return creator(name=name, model=model, **kwargs)

    def create_workflow(
        self,
        name: str,
        workflow_type: str = "sequential",
        **kwargs
    ) -> Dict:
        """
        创建 Workflow
        
        Args:
            name: Workflow 名称
            workflow_type: Workflow 类型 (sequential/conditional/parallel/loop)
            **kwargs: 其他配置参数
        """
        templates = {
            "sequential": self.workflow_templates.sequential_workflow,
            "conditional": self.workflow_templates.conditional_workflow,
            "parallel": self.workflow_templates.parallel_workflow,
            "loop": self.workflow_templates.loop_workflow
        }
        
        creator = templates.get(workflow_type, self.workflow_templates.sequential_workflow)
        return creator(name=name, **kwargs)

    def apply_pattern(
        self,
        pattern_name: str,
        **kwargs
    ) -> Dict:
        """
        应用编排模式
        
        Args:
            pattern_name: 模式名称 (router/pipeline/fan_out_fan_in/saga)
            **kwargs: 模式配置参数
        """
        pattern_funcs = {
            "router": self.patterns.router_pattern,
            "pipeline": self.patterns.pipeline_pattern,
            "fan_out_fan_in": self.patterns.fan_out_fan_in_pattern,
            "saga": self.patterns.saga_pattern
        }
        
        func = pattern_funcs.get(pattern_name)
        if not func:
            raise ValueError(f"Unknown pattern: {pattern_name}")
        
        return func(**kwargs)

    def export_workflow(
        self,
        workflow: Dict,
        format: str = "json",
        output_path: str = None
    ) -> str:
        """
        导出 Workflow
        
        Args:
            workflow: Workflow 定义
            format: 导出格式 (json/yaml/python)
            output_path: 输出路径
        """
        if format == "json":
            content = json.dumps(workflow, indent=2, ensure_ascii=False)
        elif format == "yaml":
            try:
                import yaml
                content = yaml.dump(workflow, allow_unicode=True)
            except ImportError:
                content = json.dumps(workflow, indent=2, ensure_ascii=False)
        elif format == "python":
            content = f"""
# OpenClaw Workflow: {workflow.get('name', 'Unnamed')}

workflow = {json.dumps(workflow, indent=4, ensure_ascii=False)}
"""
        else:
            raise ValueError(f"Unknown format: {format}")
        
        if output_path:
            path = Path(output_path)
            path.parent.mkdir(parents=True, exist_ok=True)
            with open(path, 'w') as f:
                f.write(content)
        
        return content

    def validate_workflow(self, workflow: Dict) -> Tuple[bool, List[str]]:
        """
        验证 Workflow 正确性
        
        Returns:
            (is_valid, error_messages)
        """
        errors = []
        
        # 检查必填字段
        if "name" not in workflow:
            errors.append("缺少 workflow name")
        
        if "nodes" not in workflow:
            errors.append("缺少 nodes 定义")
        else:
            # 检查节点ID唯一性
            node_ids = [n.get("id") for n in workflow["nodes"]]
            if len(node_ids) != len(set(node_ids)):
                errors.append("存在重复的节点ID")
            
            # 检查输入输出节点
            node_types = [n.get("type") for n in workflow["nodes"]]
            if "input" not in node_types:
                errors.append("缺少 input 节点")
            if "output" not in node_types:
                errors.append("缺少 output 节点")
        
        # 检查边定义
        if "edges" in workflow:
            node_ids = set(node_ids)
            for edge in workflow["edges"]:
                if edge.get("from") not in node_ids:
                    errors.append(f"边的源节点 {edge.get('from')} 不存在")
                if edge.get("to") not in node_ids:
                    errors.append(f"边的目标节点 {edge.get('to')} 不存在")
        
        return len(errors) == 0, errors


# =============================================================================
# 主函数
# =============================================================================

def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="OpenClaw Agent/Workflow 编排专家系统 v5.0"
    )

    # 创建 Agent
    parser.add_argument("--create-agent", help="创建 Agent")
    parser.add_argument("--agent-type", choices=["chat", "tool_calling", "data_processing"],
                       default="chat", help="Agent 类型")
    parser.add_argument("--model", default="gpt-4o", help="使用的模型")

    # 创建 Workflow
    parser.add_argument("--create-workflow", help="创建 Workflow")
    parser.add_argument("--workflow-type", choices=["sequential", "conditional", "parallel", "loop"],
                       default="sequential", help="Workflow 类型")

    # 应用模式
    parser.add_argument("--pattern", choices=["router", "pipeline", "fan_out_fan_in", "saga"],
                       help="应用编排模式")

    # 导出
    parser.add_argument("--export", action="store_true", help="导出为文件")
    parser.add_argument("--format", choices=["json", "yaml", "python"],
                       default="json", help="导出格式")
    parser.add_argument("--output", "-o", help="输出文件路径")

    # 验证
    parser.add_argument("--validate", action="store_true", help="验证 Workflow")
    parser.add_argument("--workflow-file", help="要验证的 Workflow 文件")

    args = parser.parse_args()

    expert = WorkflowExpert()

    if args.create_agent:
        agent = expert.create_agent(
            name=args.create_agent,
            agent_type=args.agent_type,
            model=args.model
        )
        print(json.dumps(agent, indent=2, ensure_ascii=False))

    elif args.create_workflow:
        workflow = expert.create_workflow(
            name=args.create_workflow,
            workflow_type=args.workflow_type,
            nodes=[]
        )
        print(json.dumps(workflow, indent=2, ensure_ascii=False))

    elif args.pattern:
        pattern = expert.apply_pattern(args.pattern)
        print(json.dumps(pattern, indent=2, ensure_ascii=False))

    elif args.validate and args.workflow_file:
        with open(args.workflow_file) as f:
            workflow = json.load(f)
        
        is_valid, errors = expert.validate_workflow(workflow)
        
        if is_valid:
            print("Workflow 验证通过")
        else:
            print("Workflow 验证失败:")
            for error in errors:
                print(f"  - {error}")

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
