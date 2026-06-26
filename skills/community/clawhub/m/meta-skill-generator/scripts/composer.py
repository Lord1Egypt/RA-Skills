"""
技能组合器 - DAG 任务解析与技能编排
"""

import json
import os
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from collections import defaultdict
import networkx as nx


@dataclass
class SkillNode:
    """技能节点"""
    skill_id: str
    inputs: Dict[str, Any] = field(default_factory=dict)
    depends_on: List[str] = field(default_factory=list)


@dataclass
class ExecutionResult:
    """执行结果"""
    success: bool
    outputs: Dict[str, Any]
    errors: List[str]
    execution_order: List[str]


class SkillComposer:
    """技能组合器 - 将复杂任务分解为技能执行流"""
    
    DECOMPOSE_PROMPT = """将复杂任务分解为技能调用序列。

任务：{task}

已安装的技能：
{available_skills}

请分析任务，输出技能调用计划。

输出格式（JSON）：
{{
    "execution_plan": [
        {{
            "skill_id": "skill_xxx",
            "inputs": {{"param": "value"}},
            "depends_on": ["skill_yyy"]  // 依赖的技能 ID 列表
        }}
    ],
    "reasoning": "为什么这样分解"
}}
"""
    
    def __init__(self, library, llm_client=None):
        """
        初始化组合器
        
        Args:
            library: SkillLibrary 实例
            llm_client: LLM 客户端
        """
        self.library = library
        self.llm_client = llm_client
        self.usage_graph = defaultdict(list)
        self.execution_history: List[List[str]] = []
    
    def decompose_task(self, task: str) -> List[SkillNode]:
        """
        将复杂任务分解为技能执行流
        
        Args:
            task: 复杂任务描述
            
        Returns:
            技能节点列表
        """
        if not self.llm_client:
            return self._decompose_local(task)
        
        try:
            # 获取可用技能
            skills = self.library.list_skills()
            available = "\n".join([
                f"- {s['id']}: {s['metadata'].get('name', 'N/A')}"
                for s in skills
            ])
            
            # 构建 prompt
            prompt = self.DECOMPOSE_PROMPT.format(
                task=task,
                available_skills=available or "无"
            )
            
            # 调用 LLM
            response = self.llm_client.chat.completions.create(
                model="deepseek-chat",
                messages=[
                    {"role": "system", "content": "你是一个任务规划专家。"},
                    {"role": "user", "content": prompt}
                ],
                response_format={"type": "json_object"}
            )
            
            result = json.loads(response.choices[0].message.content)
            
            # 解析执行计划
            plan = result.get("execution_plan", [])
            return [
                SkillNode(
                    skill_id=step.get("skill_id", ""),
                    inputs=step.get("inputs", {}),
                    depends_on=step.get("depends_on", [])
                )
                for step in plan
            ]
            
        except Exception as e:
            print(f"⚠️ LLM 分解失败: {e}")
            return self._decompose_local(task)
    
    def _decompose_local(self, task: str) -> List[SkillNode]:
        """
        本地分解（简单规则匹配）
        
        找到任务中提到的关键词匹配的技能
        """
        # 简单实现：搜索相关技能
        results = self.library.search(task, top_k=3)
        
        if not results['ids'] or not results['ids'][0]:
            return []
        
        nodes = []
        for skill_id in results['ids'][0]:
            nodes.append(SkillNode(
                skill_id=skill_id,
                inputs={},
                depends_on=[nodes[-1].skill_id] if nodes else []
            ))
        
        return nodes
    
    def build_dag(self, nodes: List[SkillNode]) -> nx.DiGraph:
        """
        构建有向无环图
        
        Args:
            nodes: 技能节点列表
            
        Returns:
            NetworkX 有向图
        """
        G = nx.DiGraph()
        
        # 添加节点
        for node in nodes:
            G.add_node(
                node.skill_id,
                inputs=node.inputs,
                depends_on=node.depends_on
            )
        
        # 添加边（依赖关系）
        for node in nodes:
            for dep in node.depends_on:
                G.add_edge(dep, node.skill_id)
        
        # 检查是否有环
        if not nx.is_directed_acyclic_graph(G):
            raise ValueError("技能依赖存在环，无法执行")
        
        return G
    
    def execute_pipeline(
        self,
        dag: nx.DiGraph,
        initial_inputs: Dict[str, Any],
        skill_loader
    ) -> ExecutionResult:
        """
        按依赖顺序执行技能
        
        Args:
            dag: 技能依赖图
            initial_inputs: 初始输入
            skill_loader: 技能加载器函数
            
        Returns:
            执行结果
        """
        # 拓扑排序获取执行顺序
        try:
            execution_order = list(nx.topological_sort(dag))
        except nx.NetworkXError as e:
            return ExecutionResult(
                success=False,
                outputs={},
                errors=[f"依赖图存在环: {e}"],
                execution_order=[]
            )
        
        results = {**initial_inputs}
        errors = []
        
        for skill_id in execution_order:
            node_data = dag.nodes[skill_id]
            inputs = node_data.get('inputs', {})
            
            # 解析输入（从之前的输出中获取）
            resolved_inputs = self._resolve_inputs(inputs, results)
            
            # 加载并执行技能
            try:
                skill = skill_loader(skill_id)
                output = skill.execute(**resolved_inputs)
                
                results[skill_id] = output
                
                if not output.get('success', False):
                    errors.append(f"{skill_id}: {output.get('error', 'Unknown error')}")
                
            except Exception as e:
                errors.append(f"{skill_id}: {str(e)}")
                results[skill_id] = {"success": False, "error": str(e)}
        
        # 记录执行历史
        self.execution_history.append(execution_order)
        self._update_usage_graph(execution_order)
        
        return ExecutionResult(
            success=len(errors) == 0,
            outputs=results,
            errors=errors,
            execution_order=execution_order
        )
    
    def _resolve_inputs(
        self,
        inputs: Dict[str, Any],
        previous_outputs: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        解析输入变量
        
        将 {{skill_id.output}} 格式替换为实际输出
        """
        resolved = {}
        
        for key, value in inputs.items():
            if isinstance(value, str) and '{{' in value:
                # 替换变量引用
                for skill_id, output in previous_outputs.items():
                    placeholder = f"{{{{{skill_id}.output}}}}"
                    if placeholder in value:
                        value = value.replace(
                            placeholder,
                            str(output.get('result', ''))
                        )
            
            resolved[key] = value
        
        return resolved
    
    def _update_usage_graph(self, execution_order: List[str]):
        """更新使用图"""
        for i in range(len(execution_order) - 1):
            self.usage_graph[execution_order[i]].append(execution_order[i+1])
    
    def visualize_dag(self, dag: nx.DiGraph) -> str:
        """
        生成 DAG 可视化（文本形式）
        
        Args:
            dag: 技能依赖图
            
        Returns:
            ASCII 形式的有向图
        """
        lines = ["digraph skills {"]
        
        for edge in dag.edges():
            lines.append(f'    "{edge[0]}" -> "{edge[1]}";')
        
        lines.append("}")
        
        return "\n".join(lines)
    
    def suggest_compositions(self, min_usage: int = 3) -> List[Dict]:
        """
        建议可组合的技能
        
        查找经常连续使用的技能组合
        
        Args:
            min_usage: 最小使用次数
            
        Returns:
            技能组合建议
        """
        # 统计共现
        cooccurrence = defaultdict(int)
        
        for sequence in self.execution_history:
            for i in range(len(sequence) - 1):
                pair = tuple(sorted([sequence[i], sequence[i+1]]))
                cooccurrence[pair] += 1
        
        # 找出高频组合
        suggestions = []
        for (skill_a, skill_b), count in cooccurrence.items():
            if count >= min_usage:
                suggestions.append({
                    "skills": [skill_a, skill_b],
                    "usage_count": count,
                    "suggestion": f"建议创建 meta-skill 封装 {skill_a} + {skill_b}"
                })
        
        return sorted(suggestions, key=lambda x: x['usage_count'], reverse=True)


def create_composer(library, llm_client=None) -> SkillComposer:
    """创建组合器实例"""
    return SkillComposer(library, llm_client)


if __name__ == "__main__":
    # 测试
    from embed_skill import SkillLibrary
    
    library = SkillLibrary()
    composer = SkillComposer(library)
    
    # 模拟分解
    nodes = [
        SkillNode("skill_email", {"to": "user@example.com"}, []),
        SkillNode("skill_notification", {"message": "task done"}, ["skill_email"])
    ]
    
    dag = composer.build_dag(nodes)
    
    print("📊 DAG 可视化:")
    print(composer.visualize_dag(dag))
