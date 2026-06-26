#!/usr/bin/env python3
"""
OpenClaw Agent优化器
智能配置和优化Agent设置
"""

import json
import os
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum

class AgentType(Enum):
    """Agent类型枚举"""
    GENERAL = "general"          # 通用助手
    CODER = "coder"              # 代码专家
    ANALYST = "analyst"          # 数据分析师
    WRITER = "writer"            # 文案写手
    RESEARCHER = "researcher"    # 研究员
    COORDINATOR = "coordinator"  # 协调器
    SPECIALIST = "specialist"    # 领域专家

@dataclass
class AgentTemplate:
    """Agent配置模板"""
    type: AgentType
    name: str
    description: str
    model: str
    tools: Dict[str, Any]
    workspace: Optional[str] = None
    temperature: float = 0.7
    max_tokens: int = 4000
    thinking: bool = False

class AgentOptimizer:
    """Agent配置优化器"""
    
    def __init__(self, config_path: str = None):
        self.config_path = config_path or os.path.expanduser("~/.openclaw/openclaw.json")
        self.config = None
        
        # Agent模板库
        self.agent_templates = {
            AgentType.GENERAL: AgentTemplate(
                type=AgentType.GENERAL,
                name="通用助手",
                description="通用任务处理助手",
                model="qwen/qwen3.5-plus",
                tools={"profile": "general"},
                temperature=0.7
            ),
            AgentType.CODER: AgentTemplate(
                type=AgentType.CODER,
                name="代码专家",
                description="编程和代码分析专家",
                model="qwen/qwen3-coder-plus",
                tools={"profile": "coding"},
                temperature=0.3,
                thinking=False
            ),
            AgentType.ANALYST: AgentTemplate(
                type=AgentType.ANALYST,
                name="数据分析师",
                description="数据分析和报表生成专家",
                model="qwen/qwen3.5-plus",
                tools={"profile": "data"},
                temperature=0.5
            ),
            AgentType.WRITER: AgentTemplate(
                type=AgentType.WRITER,
                name="文案写手",
                description="文案创作和编辑专家",
                model="qwen/qwen3.5-plus",
                tools={"profile": "writing"},
                temperature=0.8
            ),
            AgentType.RESEARCHER: AgentTemplate(
                type=AgentType.RESEARCHER,
                name="研究员",
                description="研究和分析专家",
                model="qwen/qwen3.5-plus",
                tools={"profile": "research"},
                temperature=0.6,
                thinking=True
            ),
            AgentType.COORDINATOR: AgentTemplate(
                type=AgentType.COORDINATOR,
                name="协调器",
                description="任务协调和路由专家",
                model="qwen/qwen3.5-plus",
                tools={"profile": "coordination"},
                temperature=0.5,
                thinking=True
            ),
            AgentType.SPECIALIST: AgentTemplate(
                type=AgentType.SPECIALIST,
                name="领域专家",
                description="特定领域专家",
                model="ollama/qwen3.5:specialist",
                tools={"profile": "specialized"},
                temperature=0.6
            )
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
    
    def analyze_agents(self) -> Dict:
        """分析当前Agent配置"""
        if not self.config or "agents" not in self.config:
            return {"error": "未找到agents配置"}
        
        agents = self.config["agents"]
        agent_list = agents.get("list", [])
        
        analysis = {
            "total_agents": len(agent_list),
            "default_agent": None,
            "agent_types": {},
            "model_distribution": {},
            "issues": []
        }
        
        for agent in agent_list:
            agent_id = agent.get("id", "unknown")
            
            # 检查默认Agent
            if agent.get("default"):
                analysis["default_agent"] = agent_id
            
            # 分析模型使用
            model = agent.get("model", "unknown")
            if isinstance(model, dict):
                model = model.get("primary", "unknown")
            analysis["model_distribution"][model] = analysis["model_distribution"].get(model, 0) + 1
            
            # 检测问题
            if "name" not in agent:
                analysis["issues"].append(f"Agent {agent_id} 缺少name字段")
            if "model" not in agent:
                analysis["issues"].append(f"Agent {agent_id} 缺少model配置")
        
        return analysis
    
    def create_agent(self, agent_id: str, agent_type: AgentType, 
                    custom_name: str = None, custom_model: str = None) -> Dict:
        """创建新的Agent配置"""
        template = self.agent_templates[agent_type]
        
        agent_config = {
            "id": agent_id,
            "name": custom_name or template.name,
            "description": template.description,
            "model": custom_model or template.model
        }
        
        # 添加工具配置
        if template.tools:
            agent_config["tools"] = template.tools
        
        # 添加高级参数
        advanced_config = {}
        if template.temperature != 0.7:
            advanced_config["temperature"] = template.temperature
        if template.max_tokens != 4000:
            advanced_config["maxTokens"] = template.max_tokens
        if template.thinking:
            advanced_config["thinking"] = "stream"
        
        if advanced_config:
            agent_config["advanced"] = advanced_config
        
        return agent_config
    
    def optimize_agent_routing(self) -> List[Dict]:
        """优化Agent路由策略"""
        if not self.config or "agents" not in self.config:
            return []
        
        agents = self.config["agents"]
        agent_list = agents.get("list", [])
        
        # 分析Agent能力
        agent_capabilities = []
        for agent in agent_list:
            agent_id = agent.get("id")
            agent_name = agent.get("name", "")
            model = agent.get("model", "")
            
            # 根据名称和模型推断能力
            capabilities = []
            
            # 检查名称关键词
            name_lower = agent_name.lower()
            if any(keyword in name_lower for keyword in ["代码", "coder", "编程", "开发"]):
                capabilities.append("coding")
            if any(keyword in name_lower for keyword in ["分析", "analyst", "数据", "报表"]):
                capabilities.append("analysis")
            if any(keyword in name_lower for keyword in ["写作", "writer", "文案", "编辑"]):
                capabilities.append("writing")
            if any(keyword in name_lower for keyword in ["研究", "researcher", "调研"]):
                capabilities.append("research")
            if any(keyword in name_lower for keyword in ["协调", "coordinator", "路由"]):
                capabilities.append("coordination")
            
            # 检查模型关键词
            if isinstance(model, str):
                model_lower = model.lower()
                if "coder" in model_lower:
                    capabilities.append("coding")
                if "research" in model_lower:
                    capabilities.append("research")
            
            # 如果没有检测到能力，添加通用能力
            if not capabilities:
                capabilities.append("general")
            
            agent_capabilities.append({
                "agent_id": agent_id,
                "agent_name": agent_name,
                "capabilities": list(set(capabilities))  # 去重
            })
        
        return agent_capabilities
    
    def generate_routing_rules(self) -> List[Dict]:
        """生成智能路由规则"""
        capabilities = self.optimize_agent_routing()
        
        routing_rules = []
        
        # 基于能力的路由规则
        capability_to_agent = {}
        for agent in capabilities:
            for capability in agent["capabilities"]:
                if capability not in capability_to_agent:
                    capability_to_agent[capability] = []
                capability_to_agent[capability].append(agent["agent_id"])
        
        # 创建路由规则
        for capability, agent_ids in capability_to_agent.items():
            if agent_ids:
                routing_rules.append({
                    "match": {
                        "capability": capability
                    },
                    "route_to": agent_ids[0],  # 使用第一个匹配的Agent
                    "fallback": agent_ids[1:] if len(agent_ids) > 1 else []
                })
        
        return routing_rules
    
    def optimize_subagent_permissions(self) -> Dict:
        """优化子Agent权限配置"""
        if not self.config or "agents" not in self.config:
            return {}
        
        agents = self.config["agents"]
        defaults = agents.get("defaults", {})
        agent_list = agents.get("list", [])
        
        # 收集所有Agent ID
        all_agent_ids = [agent.get("id") for agent in agent_list if agent.get("id")]
        
        # 更新默认配置中的allowAgents
        if "subagents" not in defaults:
            defaults["subagents"] = {}
        
        defaults["subagents"]["allowAgents"] = all_agent_ids
        
        # 为每个Agent设置合理的子Agent权限
        for agent in agent_list:
            agent_id = agent.get("id")
            if not agent_id:
                continue
            
            # 确保每个Agent都有subagents配置
            if "subagents" not in agent:
                agent["subagents"] = {}
            
            # 根据Agent类型设置权限
            agent_name = agent.get("name", "").lower()
            
            if any(keyword in agent_name for keyword in ["协调", "coordinator", "主", "main"]):
                # 协调器可以访问所有Agent
                agent["subagents"]["allowAgents"] = all_agent_ids
            elif any(keyword in agent_name for keyword in ["代码", "coder"]):
                # 代码专家可以访问分析相关Agent
                agent["subagents"]["allowAgents"] = [
                    aid for aid in all_agent_ids 
                    if any(keyword in aid.lower() for keyword in ["analyst", "research"])
                ]
            else:
                # 其他Agent只能访问自己
                agent["subagents"]["allowAgents"] = [agent_id]
        
        return {
            "default_allowAgents": all_agent_ids,
            "agent_count": len(all_agent_ids)
        }
    
    def generate_optimization_report(self) -> Dict:
        """生成优化报告"""
        analysis = self.analyze_agents()
        routing_rules = self.generate_routing_rules()
        permissions = self.optimize_subagent_permissions()
        
        return {
            "current_state": analysis,
            "proposed_routing": routing_rules,
            "optimized_permissions": permissions,
            "recommendations": self.generate_recommendations(analysis)
        }
    
    def generate_recommendations(self, analysis: Dict) -> List[str]:
        """生成优化建议"""
        recommendations = []
        
        # 检查默认Agent
        if not analysis.get("default_agent"):
            recommendations.append("设置一个默认Agent")
        
        # 检查模型分布
        model_dist = analysis.get("model_distribution", {})
        if len(model_dist) == 1:
            recommendations.append("考虑使用多个模型以提高多样性和容错性")
        
        # 检查问题
        issues = analysis.get("issues", [])
        if issues:
            recommendations.append(f"修复{len(issues)}个配置问题")
        
        # 检查Agent数量
        total_agents = analysis.get("total_agents", 0)
        if total_agents < 3:
            recommendations.append("考虑添加更多专业Agent以提高效率")
        elif total_agents > 10:
            recommendations.append("考虑合并功能相似的Agent以简化管理")
        
        return recommendations

def main():
    """命令行入口"""
    import argparse
    
    parser = argparse.ArgumentParser(description="OpenClaw Agent优化器")
    parser.add_argument("action", choices=["analyze", "create", "optimize", "report"],
                       help="执行动作: analyze(分析), create(创建), optimize(优化), report(报告)")
    parser.add_argument("--agent-id", help="Agent ID（用于create动作）")
    parser.add_argument("--agent-type", choices=["general", "coder", "analyst", "writer", 
                                                "researcher", "coordinator", "specialist"],
                       help="Agent类型（用于create动作）")
    parser.add_argument("--name", help="Agent名称（用于create动作）")
    parser.add_argument("--model", help="自定义模型（用于create动作）")
    parser.add_argument("--config", default="~/.openclaw/openclaw.json",
                       help="配置文件路径")
    
    args = parser.parse_args()
    config_path = os.path.expanduser(args.config)
    
    optimizer = AgentOptimizer(config_path)
    
    if not optimizer.load_config():
        print("❌ 无法加载配置文件")
        return
    
    if args.action == "analyze":
        analysis = optimizer.analyze_agents()
        print(json.dumps(analysis, indent=2, ensure_ascii=False))
        
    elif args.action == "create":
        if not args.agent_id or not args.agent_type:
            print("❌ 需要提供 --agent-id 和 --agent-type 参数")
            return
        
        try:
            agent_type = AgentType(args.agent_type)
            agent_config = optimizer.create_agent(
                args.agent_id, agent_type, args.name, args.model
            )
            print("✅ 创建的Agent配置:")
            print(json.dumps(agent_config, indent=2, ensure_ascii=False))
        except ValueError:
            print(f"❌ 无效的Agent类型: {args.agent_type}")
            print(f"可用类型: {[t.value for t in AgentType]}")
            
    elif args.action == "optimize":
        permissions = optimizer.optimize_subagent_permissions()
        print("✅ 优化的权限配置:")
        print(json.dumps(permissions, indent=2, ensure_ascii=False))
        
    elif args.action == "report":
        report = optimizer.generate_optimization_report()
        print(json.dumps(report, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()