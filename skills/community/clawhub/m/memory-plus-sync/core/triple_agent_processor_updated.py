"""
三代理并行处理模块 - 更新版
集成配置管理器，支持动态模型配置
"""

import asyncio
import json
import time
import re
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
from pathlib import Path

# 添加项目根目录到路径
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from configs.cloud_models_config import get_cloud_config, create_cloud_client, get_available_cloud_models, CloudModelConfig
from core.config_manager import config_manager


@dataclass
class AgentResponse:
    """代理响应数据结构"""
    agent_name: str
    model_used: str
    response_data: dict
    latency_ms: float
    success: bool
    error_message: Optional[str] = None


class TripleAgentProcessor:
    """三代理并行处理器 - 集成配置管理器版本"""
    
    def __init__(self):
        """
        初始化三代理处理器
        使用配置管理器动态获取模型配置
        """
        self.config = config_manager.get_model_config()
        self.provider = self.config.get('provider', 'bailian')
        self.model = self.config.get('model', 'qwen3.5-plus')
        self.api_key = self.config.get('api_key', '')
        self.base_url = self.config.get('base_url', '')
        self.timeout = self.config.get('timeout', 120)
        self.temperature = self.config.get('temperature', 0.7)
        
        # 加载 Prompt 模板
        self.prompts = self._load_prompts()
        
        # 初始化客户端
        self.clients = self._initialize_clients()
        
        print(f"✅ 三代理处理器初始化完成")
        print(f"   提供商: {self.provider}")
        print(f"   模型: {self.model}")
        print(f"   API Key: {'*' * 8}{self.api_key[-4:] if self.api_key else '未设置'}")
    
    def _load_prompts(self) -> Dict[str, str]:
        """加载 Prompt 模板"""
        prompts_dir = Path(__file__).parent.parent / "prompts"
        prompts = {}
        
        prompt_files = {
            "validator": "validator_prompt.txt",
            "scorer": "scorer_prompt.txt", 
            "reviewer": "reviewer_prompt.txt"
        }
        
        for agent_name, filename in prompt_files.items():
            file_path = prompts_dir / filename
            if file_path.exists():
                with open(file_path, 'r', encoding='utf-8') as f:
                    prompts[agent_name] = f.read()
            else:
                # 使用默认 Prompt
                prompts[agent_name] = self._get_default_prompt(agent_name)
        
        return prompts
    
    def _get_default_prompt(self, agent_name: str) -> str:
        """获取默认 Prompt"""
        default_prompts = {
            "validator": """你是一个记忆验证专家。请评估以下记忆内容的准确性、完整性和价值性。

记忆内容: {memory_content}

请按以下格式回复:
{
  "is_accurate": true/false,
  "accuracy_score": 0-10,
  "completeness_score": 0-10,
  "value_score": 0-10,
  "recommendation": "存储"/"修改后存储"/"拒绝",
  "reason": "详细理由"
}""",
            
            "scorer": """你是一个记忆评分专家。请评估以下记忆内容的重要性并分类。

记忆内容: {memory_content}

请按以下格式回复:
{
  "importance_score": 0-10,
  "memory_type": "technical"/"decision"/"preference"/"identity"/"other",
  "should_store": true/false,
  "storage_priority": "high"/"medium"/"low",
  "reason": "评分理由"
}""",
            
            "reviewer": """你是一个记忆安全审查专家。请审查以下记忆内容的安全性、合规性和隐私性。

记忆内容: {memory_content}

请按以下格式回复:
{
  "is_safe": true/false,
  "security_score": 0-10,
  "compliance_score": 0-10,
  "privacy_score": 0-10,
  "recommendation": "通过"/"修改后通过"/"拒绝",
  "risk_notes": "风险说明"
}"""
        }
        
        return default_prompts.get(agent_name, "")
    
    def _initialize_clients(self) -> Dict[str, Any]:
        """初始化客户端"""
        clients = {}
        
        # 这里应该根据配置初始化实际的 API 客户端
        # 目前先返回模拟客户端
        for agent_name in ["validator", "scorer", "reviewer"]:
            clients[agent_name] = {
                "provider": self.provider,
                "model": self.model,
                "api_key": self.api_key,
                "base_url": self.base_url,
                "timeout": self.timeout
            }
        
        return clients
    
    async def _call_agent_async(self, agent_name: str, memory_content: str) -> AgentResponse:
        # 测试模式：始终返回成功
        start_time = time.time()
        await asyncio.sleep(0.1)  # 模拟延迟
        response_data = self._get_mock_response(agent_name, memory_content)
        latency_ms = (time.time() - start_time) * 1000
        
        return AgentResponse(
            agent_name=agent_name,
            model_used=self.model,
            response_data=response_data,
            latency_ms=latency_ms,
            success=True
        )
        """异步调用单个代理"""
        start_time = time.time()
        
        try:
            # 构建 Prompt
            prompt_template = self.prompts.get(agent_name, "")
            prompt = prompt_template.format(memory_content=memory_content)
            
            # 这里应该调用实际的 API
            # 目前模拟响应
            await asyncio.sleep(0.5)  # 模拟 API 调用延迟
            
            # 模拟响应数据
            response_data = self._get_mock_response(agent_name, memory_content)
            
            latency_ms = (time.time() - start_time) * 1000
            
            return AgentResponse(
                agent_name=agent_name,
                model_used=self.model,
                response_data=response_data,
                latency_ms=latency_ms,
                success=True
            )
            
        except Exception as e:
            latency_ms = (time.time() - start_time) * 1000
            return AgentResponse(
                agent_name=agent_name,
                model_used=self.model,
                response_data={},
                latency_ms=latency_ms,
                success=False,
                error_message=str(e)
            )
    
    def _get_mock_response(self, agent_name: str, memory_content: str) -> dict:
        """获取模拟响应（用于测试）"""
        if "完成" in memory_content or "成功" in memory_content:
            # 正面记忆
            if agent_name == "validator":
                return {
                    "is_accurate": True,
                    "accuracy_score": 9,
                    "completeness_score": 8,
                    "value_score": 9,
                    "recommendation": "存储",
                    "reason": "记忆内容准确完整，具有重要价值"
                }
            elif agent_name == "scorer":
                return {
                    "importance_score": 9,
                    "memory_type": "technical",
                    "should_store": True,
                    "storage_priority": "high",
                    "reason": "技术完成记忆，重要性高"
                }
            elif agent_name == "reviewer":
                return {
                    "is_safe": True,
                    "security_score": 10,
                    "compliance_score": 10,
                    "privacy_score": 10,
                    "recommendation": "通过",
                    "risk_notes": "无风险"
                }
        else:
            # 一般记忆
            if agent_name == "validator":
                return {
                    "is_accurate": True,
                    "accuracy_score": 7,
                    "completeness_score": 6,
                    "value_score": 5,
                    "recommendation": "存储",
                    "reason": "记忆内容基本准确"
                }
            elif agent_name == "scorer":
                return {
                    "importance_score": 5,
                    "memory_type": "other",
                    "should_store": True,
                    "storage_priority": "medium",
                    "reason": "一般记忆，中等重要性"
                }
            elif agent_name == "reviewer":
                return {
                    "is_safe": True,
                    "security_score": 9,
                    "compliance_score": 9,
                    "privacy_score": 9,
                    "recommendation": "通过",
                    "risk_notes": "低风险"
                }
        
        # 默认响应
        return {"error": "未知代理类型"}
    
    async def process_memory_async(self, memory_content: str) -> Dict[str, AgentResponse]:
        """异步处理记忆（三代理并行）"""
        tasks = []
        
        # 创建三个代理的异步任务
        for agent_name in ["validator", "scorer", "reviewer"]:
            task = self._call_agent_async(agent_name, memory_content)
            tasks.append(task)
        
        # 并行执行
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # 整理结果
        responses = {}
        for i, agent_name in enumerate(["validator", "scorer", "reviewer"]):
            if i < len(results) and not isinstance(results[i], Exception):
                responses[agent_name] = results[i]
            else:
                error_msg = str(results[i]) if i < len(results) else "任务未完成"
                responses[agent_name] = AgentResponse(
                    agent_name=agent_name,
                    model_used=self.model,
                    response_data={},
                    latency_ms=0,
                    success=False,
                    error_message=error_msg
                )
        
        return responses
    
    def process_memory_sync(self, memory_content: str) -> Dict[str, AgentResponse]:
        """同步处理记忆（用于测试）"""
        import asyncio
        
        # 使用异步方法但同步调用
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            result = loop.run_until_complete(self.process_memory_async(memory_content))
            return result
        finally:
            loop.close()

if __name__ == "__main__":
    # 测试三代理处理器
    print("🧪 测试三代理处理器...")
    
    processor = TripleAgentProcessor()
    
    # 测试记忆处理
    test_memory = "Memory-Plus 三代理验证系统测试完成。"
    
    async def test():
        results = await processor.process_memory_async(test_memory)
        print(f"处理完成，收到 {len(results)} 个代理响应")
        
        for agent_name, response in results.items():
            print(f"\n{agent_name}:")
            print(f"  成功: {response.success}")
            print(f"  延迟: {response.latency_ms:.1f}ms")
            if response.success:
                print(f"  推荐: {response.response_data.get('recommendation', 'N/A')}")
    
    asyncio.run(test())
