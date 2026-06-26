"""
三代理并行处理模块

并行调用三个独立的代理 (Validator, Scorer, Reviewer) 对记忆内容进行验证
"""

import asyncio
import json
import time
import re
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from pathlib import Path

# 添加项目根目录到路径
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from configs.cloud_models_config import get_cloud_config, create_cloud_client, get_available_cloud_models, CloudModelConfig


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
    """三代理并行处理器"""
    
    def __init__(self, use_kimi: bool = True):
        """
        初始化三代理处理器
        
        Args:
            use_kimi: 是否使用 Kimi API (否则使用云端备选)
        """
        self.use_kimi = use_kimi
        self.kimi_config = None
        self.cloud_config = None
        self.clients = {}
        
        # 加载 Prompt 模板
        self.prompts = self._load_prompts()
        
        # 初始化配置
        self._init_configs()
    
    def _load_prompts(self) -> Dict[str, str]:
        """加载三个代理的 Prompt 模板"""
        prompts_dir = Path(__file__).parent.parent / "prompts"
        prompts = {}
        
        for name in ["validator", "scorer", "reviewer"]:
            prompt_file = prompts_dir / f"{name}_prompt.txt"
            if prompt_file.exists():
                with open(prompt_file, "r", encoding="utf-8") as f:
                    prompts[name] = f.read()
            else:
                raise FileNotFoundError(f"Prompt 文件不存在：{prompt_file}")
        
        return prompts
    
    def _init_configs(self):
        """初始化模型配置 - 使用 Kimi API"""
        if self.use_kimi:
            self.cloud_config = get_cloud_config()
            if not self.cloud_config.kimi_api_key:
                raise ConnectionError("Kimi API Key 未配置，请设置 KIMI_API_KEY 环境变量")
            # 创建 Kimi 客户端
            client, model_name = create_cloud_client("kimi", self.cloud_config)
            self.clients["default"] = (client, model_name)
            self.kimi_config = self.cloud_config  # 修复：保存 kimi_config
        else:
            self.cloud_config = get_cloud_config()
            available = get_available_cloud_models(self.cloud_config)
            if not available:
                raise ValueError("未配置任何云端模型")
            
            # 为每个可用模型创建客户端
            for model_info in available:
                client, model_name = create_cloud_client(model_info["name"], self.cloud_config)
                self.clients[model_info["name"]] = (client, model_name)
    
    def _extract_json(self, content: str, agent_name: str) -> Optional[str]:
        """
        从响应内容中提取 JSON 字符串
        
        Args:
            content: 原始响应内容
            agent_name: 代理名称（用于调试）
        
        Returns:
            提取的 JSON 字符串，如果无法提取则返回 None
        """
        # 预处理：移除思考过程
        thinking_markers = [
            'Thinking Process:', '思考过程：', '思考：', '分析：',
            '<think>', '</think>', '<think>', '</think>',
            'Let me think', '让我思考', '首先', '第一步'
        ]
        
        for marker in thinking_markers:
            if marker in content:
                marker_pos = content.find(marker)
                if marker_pos >= 0:
                    # 找到 marker 后的第一个 {
                    json_start = content.find('{', marker_pos)
                    if json_start >= 0:
                        content = content[json_start:]
                        print(f"[DEBUG {agent_name}] 移除思考过程标记：{marker}")
                        break
        
        # 策略 1: 从 markdown 代码块提取（优先级最高）
        for code_marker in ['```json', '```JSON', '```']:
            if code_marker in content:
                start = content.find(code_marker) + len(code_marker)
                end = content.find('```', start)
                if end > start:
                    json_str = content[start:end].strip()
                    print(f"[DEBUG {agent_name}] 从代码块提取成功，长度：{len(json_str)}")
                    return json_str
        
        # 策略 2: 直接查找 JSON 对象边界
        start = content.find('{')
        if start >= 0:
            # 找到最后一个 }
            end = content.rfind('}')
            if end > start:
                json_str = content[start:end+1]
                # 验证括号平衡
                open_braces = json_str.count('{')
                close_braces = json_str.count('}')
                if open_braces == close_braces:
                    print(f"[DEBUG {agent_name}] 边界提取成功，长度：{len(json_str)}, 括号平衡：{open_braces}")
                    return json_str
                elif open_braces > close_braces:
                    # 尝试补全
                    json_str += '}' * (open_braces - close_braces)
                    print(f"[DEBUG {agent_name}] 边界提取并补全，长度：{len(json_str)}")
                    return json_str
        
        # 策略 3: 使用正则表达式提取（处理嵌套结构）
        # 简化版正则，匹配 { ... } 结构
        pattern = r'\{[^{}]*(?:\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}[^{}]*)*\}'
        matches = re.findall(pattern, content, re.DOTALL)
        if matches:
            # 选择最长的匹配
            json_str = max(matches, key=len)
            print(f"[DEBUG {agent_name}] 正则匹配成功，长度：{len(json_str)}")
            return json_str
        
        # 策略 4: 尝试逐行查找 JSON
        lines = content.split('\n')
        json_lines = []
        in_json = False
        brace_count = 0
        
        for line in lines:
            line = line.strip()
            if not in_json and line.startswith('{'):
                in_json = True
                brace_count = line.count('{') - line.count('}')
                json_lines.append(line)
            elif in_json:
                json_lines.append(line)
                brace_count += line.count('{') - line.count('}')
                if brace_count <= 0:
                    break
        
        if json_lines:
            json_str = '\n'.join(json_lines)
            print(f"[DEBUG {agent_name}] 逐行提取成功，长度：{len(json_str)}")
            return json_str
        
        print(f"[DEBUG {agent_name}] 无法提取 JSON")
        return None
    
    def _parse_json_with_retry(self, json_str: str, agent_name: str, raw_content: str, max_retries: int = 3) -> dict:
        """
        带重试机制的 JSON 解析
        
        Args:
            json_str: JSON 字符串
            agent_name: 代理名称
            raw_content: 原始内容（用于错误报告）
            max_retries: 最大重试次数
        
        Returns:
            解析后的字典
        
        Raises:
            ValueError: 如果多次重试后仍无法解析
        """
        last_error = None
        
        for attempt in range(max_retries):
            try:
                # 尝试直接解析
                return json.loads(json_str)
            except json.JSONDecodeError as e:
                last_error = e
                
                # 尝试修复策略
                fixed_json = json_str
                
                # 修复 1: 移除尾部逗号
                fixed_json = fixed_json.rstrip().rstrip(',').rstrip()
                
                # 修复 2: 确保以 } 结尾
                if not fixed_json.endswith('}'):
                    open_braces = fixed_json.count('{')
                    close_braces = fixed_json.count('}')
                    fixed_json += '}' * max(0, open_braces - close_braces)
                
                # 修复 3: 替换单引号为双引号
                fixed_json = fixed_json.replace("'", '"')
                
                # 修复 4: 移除控制字符（保留换行和制表符）
                fixed_json = ''.join(c for c in fixed_json if ord(c) >= 32 or c in '\n\r\t')
                
                # 修复 5: 处理转义问题
                fixed_json = fixed_json.replace('\\', '\\\\')
                
                # 修复 6: 确保键名用双引号
                fixed_json = re.sub(r'(?<=[{,])\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*:', r'"\1":', fixed_json)
                
                try:
                    result = json.loads(fixed_json)
                    print(f"[DEBUG {agent_name}] 重试 {attempt+1}/{max_retries} 成功（修复后解析）")
                    return result
                except json.JSONDecodeError:
                    print(f"[DEBUG {agent_name}] 重试 {attempt+1}/{max_retries} 失败")
                    json_str = fixed_json  # 使用修复后的版本继续尝试
        
        # 所有重试都失败
        raise ValueError(
            f"JSON 解析失败（重试{max_retries}次）: {str(last_error)[:100]}, "
            f"原始内容：{raw_content[:300]}"
        )
    
    async def _call_agent(
        self,
        agent_name: str,
        prompt_template: str,
        memory_content: str,
        client=None,
        model_name: str = None
    ) -> AgentResponse:
        """
        调用单个代理
        
        Args:
            agent_name: 代理名称
            prompt_template: Prompt 模板
            memory_content: 记忆内容
            client: OpenAI 客户端
            model_name: 模型名称
        
        Returns:
            AgentResponse: 代理响应
        """
        start_time = time.time()
        
        try:
            # 填充 Prompt
            prompt = prompt_template.replace("{memory_content}", memory_content)
            
            # 选择客户端和模型
            if client is None:
                client, model_name = self.clients["default"]
                # use_kimi 时 model_name 已经从 clients 中获取，不需要再访问 kimi_config
            
            # 强化 Prompt，强制 JSON 输出
            simplified_prompt = f"""你是一个严格的 JSON 输出机器。

任务：分析以下记忆内容并按格式输出

{prompt}

【重要】输出规则：
1. 只输出 JSON，不要任何思考、解释、前缀或后缀
2. 不要输出 ```json 或 ``` 标记
3. 不要输出"Thinking Process"或"思考过程"
4. 直接以 {{ 开始，以 }} 结束
5. 确保 JSON 有效，可以被 json.loads() 解析

输出格式示例：{{"key": "value"}}"""
            
            # 调用 API - 使用更强的系统提示
            response = client.chat.completions.create(
                model=model_name,
                messages=[
                    {"role": "system", "content": "你是一个严格的 JSON 输出机器。你只输出有效的 JSON 对象，不包含任何思考过程、解释、markdown 标记或其他文本。你的输出必须能直接被 json.loads() 解析。如果用户要求分析，你只返回 JSON 结果。"},
                    {"role": "user", "content": simplified_prompt}
                ],
                temperature=0.0,  # 零温度，减少随机性
                max_tokens=600,   # 稍微增加 token 数量
                timeout=90,       # 增加超时时间
                extra_body={      # 如果模型支持，禁用思考
                    "enable_thinking": False
                } if model_name and "qwen" in model_name.lower() else {}
            )
            
            # 解析响应
            raw_content = response.choices[0].message.content

            # 调试：记录原始响应
            print(f"[DEBUG {agent_name}] 原始响应长度：{len(raw_content)}")
            if len(raw_content) > 300:
                print(f"[DEBUG {agent_name}] 前 300 字符：{raw_content[:300]}...")
            else:
                print(f"[DEBUG {agent_name}] 完整内容：{raw_content}")

            # 使用增强的 JSON 提取方法
            json_str = self._extract_json(raw_content, agent_name)

            if json_str is None:
                raise ValueError(f"无法从响应中提取 JSON: {raw_content[:300]}")

            # 清理 JSON 字符串
            json_str = json_str.strip()

            # 使用带重试的 JSON 解析
            response_data = self._parse_json_with_retry(json_str, agent_name, raw_content)
            latency_ms = (time.time() - start_time) * 1000
            
            return AgentResponse(
                agent_name=agent_name,
                model_used=model_name,
                response_data=response_data,
                latency_ms=latency_ms,
                success=True
            )
            
        except Exception as e:
            latency_ms = (time.time() - start_time) * 1000
            return AgentResponse(
                agent_name=agent_name,
                model_used=model_name or "unknown",
                response_data={},
                latency_ms=latency_ms,
                success=False,
                error_message=str(e)
            )
    
    async def process_memory(self, memory_content: str) -> Dict[str, AgentResponse]:
        """
        并行处理记忆内容
        
        Args:
            memory_content: 待处理的记忆内容
        
        Returns:
            Dict[str, AgentResponse]: 三个代理的响应
        """
        # 创建三个代理的调用任务
        tasks = [
            self._call_agent("validator", self.prompts["validator"], memory_content),
            self._call_agent("scorer", self.prompts["scorer"], memory_content),
            self._call_agent("reviewer", self.prompts["reviewer"], memory_content)
        ]
        
        # 并行执行
        responses = await asyncio.gather(*tasks, return_exceptions=True)
        
        # 整理结果
        results = {}
        for i, response in enumerate(responses):
            agent_names = ["validator", "scorer", "reviewer"]
            agent_name = agent_names[i]
            
            if isinstance(response, Exception):
                results[agent_name] = AgentResponse(
                    agent_name=agent_name,
                    model_used="unknown",
                    response_data={},
                    latency_ms=0,
                    success=False,
                    error_message=str(response)
                )
            else:
                results[agent_name] = response
        
        return results
    
    def process_memory_sync(self, memory_content: str) -> Dict[str, AgentResponse]:
        """同步版本的处理方法"""
        return asyncio.run(self.process_memory(memory_content))


if __name__ == "__main__":
    # 测试三代理处理
    print("=== 三代理处理测试 ===\n")
    
    test_memory = """
    2026-04-03 18:00 完成 Memory-Plus 三代理验证模块的架构设计。
    决定采用 Qwen3.5-9B-MLX 作为本地验证模型，Kimi 和 GLM 作为云端备选。
    模块包含 Validator、Scorer、Reviewer 三个独立代理，通过投票机制确保准确性。
    """
    
    processor = TripleAgentProcessor(use_local=True)
    
    print(f"处理记忆内容:\n{test_memory}\n")
    print("开始并行调用三个代理...\n")
    
    results = processor.process_memory_sync(test_memory)
    
    for agent_name, response in results.items():
        print(f"\n{agent_name.upper()}:")
        print(f"  模型：{response.model_used}")
        print(f"  耗时：{response.latency_ms:.0f}ms")
        print(f"  状态：{'✅ 成功' if response.success else '❌ 失败'}")
        
        if response.success:
            print(f"  结果：{json.dumps(response.response_data, indent=2, ensure_ascii=False)[:200]}...")
        else:
            print(f"  错误：{response.error_message}")
    
    print("\n=== 测试完成 ===")
