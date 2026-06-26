"""
core/llm_client.py
==================
统一 LLM 客户端，支持 OpenAI 和 Claude，自动 fallback
为 Neuro-Agent 四区提供真实智能基础
"""

import os
import json
from pathlib import Path
from typing import Optional, Dict, Any, List
from dataclasses import dataclass
from enum import Enum


class LLMProvider(Enum):
    OPENAI = "openai"
    CLAUDE = "claude"


@dataclass
class LLMResponse:
    """LLM 响应包装"""
    content: str
    provider: LLMProvider
    model: str
    usage: Optional[Dict[str, int]] = None
    raw_response: Optional[Any] = None


class LLMClient:
    """
    Neuro-Agent 统一 LLM 客户端
    
    优先级：
    1. 尝试 OpenAI (gpt-4o-mini / gpt-4o)
    2. 失败则 fallback 到 Claude (claude-3-haiku / claude-3-sonnet)
    3. 都失败则返回 None，调用方需处理降级
    """
    
    DEFAULT_MODELS = {
        LLMProvider.OPENAI: "gpt-4o-mini",  # 快且便宜，适合高频调用
        LLMProvider.CLAUDE: "claude-3-haiku-20240307"  # 快且便宜
    }
    
    FALLBACK_MODELS = {
        LLMProvider.OPENAI: "gpt-4o",  # 质量更高
        LLMProvider.CLAUDE: "claude-3-sonnet-20240229"  # 质量更高
    }
    
    def __init__(
        self,
        openai_api_key: Optional[str] = None,
        claude_api_key: Optional[str] = None,
        default_provider: LLMProvider = LLMProvider.OPENAI,
        enable_fallback: bool = True,
        use_openclaw: bool = True
    ):
        # 自动检测 API Key（优先级：参数 > 环境变量 > 配置文件）
        self.openai_key = openai_api_key or self._detect_openai_key()
        self.claude_key = claude_api_key or self._detect_claude_key()
        self.default_provider = default_provider
        self.enable_fallback = enable_fallback
        self.use_openclaw = use_openclaw
        
        self._openai_client = None
        self._claude_client = None
    
    def _detect_openai_key(self) -> Optional[str]:
        """自动检测 OpenAI API Key"""
        # 1. 环境变量
        key = os.getenv("OPENAI_API_KEY")
        if key:
            return key
        
        # 2. 配置文件 ~/.neuro_agent/.env
        env_file = Path.home() / ".neuro_agent" / ".env"
        if env_file.exists():
            for line in env_file.read_text().split("\n"):
                if line.startswith("OPENAI_API_KEY="):
                    return line.split("=", 1)[1].strip().strip('"\'')
        
        # 3. OpenClaw 配置
        openclaw_config = Path.home() / ".openclaw" / "openclaw.json"
        if openclaw_config.exists():
            try:
                import json
                config = json.loads(openclaw_config.read_text())
                # 检查是否有模型配置
                if "models" in config and "openai" in config["models"]:
                    return config["models"]["openai"].get("apiKey")
            except Exception:
                pass
        
        return None
    
    def _detect_claude_key(self) -> Optional[str]:
        """自动检测 Claude API Key"""
        # 1. 环境变量
        key = os.getenv("ANTHROPIC_API_KEY") or os.getenv("CLAUDE_API_KEY")
        if key:
            return key
        
        # 2. 配置文件
        env_file = Path.home() / ".neuro_agent" / ".env"
        if env_file.exists():
            for line in env_file.read_text().split("\n"):
                if line.startswith("ANTHROPIC_API_KEY=") or line.startswith("CLAUDE_API_KEY="):
                    return line.split("=", 1)[1].strip().strip('"\'')
        
        return None
    
    @classmethod
    def setup_api_key(cls, provider: str, api_key: str):
        """
        设置 API Key 并保存到配置文件
        供用户一次性设置，后续自动读取
        """
        config_dir = Path.home() / ".neuro_agent"
        config_dir.mkdir(parents=True, exist_ok=True)
        
        env_file = config_dir / ".env"
        
        # 读取现有内容
        lines = []
        if env_file.exists():
            lines = env_file.read_text().split("\n")
        
        # 更新或添加
        key_name = "OPENAI_API_KEY" if provider == "openai" else "ANTHROPIC_API_KEY"
        new_line = f"{key_name}={api_key}"
        
        updated = False
        for i, line in enumerate(lines):
            if line.startswith(f"{key_name}="):
                lines[i] = new_line
                updated = True
                break
        
        if not updated:
            lines.append(new_line)
        
        env_file.write_text("\n".join(lines))
        print(f"[LLMClient] {provider} API Key 已保存到 {env_file}")
        
    def _get_openai_client(self):
        """延迟初始化 OpenAI 客户端"""
        if self._openai_client is None and self.openai_key:
            try:
                from openai import OpenAI
                self._openai_client = OpenAI(api_key=self.openai_key)
            except ImportError:
                raise ImportError("OpenAI SDK not installed. Run: pip install openai")
        return self._openai_client
    
    def _get_claude_client(self):
        """延迟初始化 Claude 客户端"""
        if self._claude_client is None and self.claude_key:
            try:
                import anthropic
                self._claude_client = anthropic.Anthropic(api_key=self.claude_key)
            except ImportError:
                raise ImportError("Anthropic SDK not installed. Run: pip install anthropic")
        return self._claude_client
    
    def _call_openai(
        self,
        messages: List[Dict[str, str]],
        model: str,
        temperature: float = 0.7,
        max_tokens: int = 500
    ) -> Optional[LLMResponse]:
        """调用 OpenAI API"""
        client = self._get_openai_client()
        if not client:
            return None
            
        try:
            response = client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens
            )
            return LLMResponse(
                content=response.choices[0].message.content,
                provider=LLMProvider.OPENAI,
                model=model,
                usage={
                    "prompt_tokens": response.usage.prompt_tokens,
                    "completion_tokens": response.usage.completion_tokens
                },
                raw_response=response
            )
        except Exception as e:
            print(f"[LLMClient] OpenAI call failed: {e}")
            return None

    def _call_openclaw(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: int = 500
    ) -> Optional[LLMResponse]:
        """
        使用 OpenClaw 内置模型路由（无需 API Key）
        通过 sessions_spawn 调用子 agent 完成
        """
        try:
            # 构建 prompt
            system_msg = ""
            user_msgs = []
            for msg in messages:
                if msg["role"] == "system":
                    system_msg = msg["content"]
                elif msg["role"] == "user":
                    user_msgs.append(msg["content"])
                elif msg["role"] == "assistant":
                    user_msgs.append(f"[Assistant]: {msg['content']}")
            
            full_prompt = f"{system_msg}\n\n" + "\n".join(user_msgs) if system_msg else "\n".join(user_msgs)
            
            # 使用 OpenClaw 模型路由
            # 注意：这里使用简单的直接调用方式
            # 实际环境中可以通过 subprocess 调用 openclaw 命令
            import subprocess
            
            # 构建 openclaw 命令
            cmd = [
                "openclaw", "sessions", "spawn",
                "--task", full_prompt[:2000],  # 截断避免过长
                "--mode", "run",
                "--runtime", "subagent",
                "--timeout-seconds", "60"
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=65)
            
            if result.returncode == 0:
                # 解析输出（取最后一行非空内容）
                lines = [l.strip() for l in result.stdout.split('\n') if l.strip()]
                content = lines[-1] if lines else "（无响应）"
                
                return LLMResponse(
                    content=content,
                    provider=LLMProvider.OPENAI,
                    model="openclaw/modelroute",
                    usage=None,
                    raw_response=None
                )
            else:
                return None
                
        except Exception as e:
            return None
    
    def _call_claude(
        self,
        messages: List[Dict[str, str]],
        model: str,
        temperature: float = 0.7,
        max_tokens: int = 500
    ) -> Optional[LLMResponse]:
        """调用 Claude API"""
        client = self._get_claude_client()
        if not client:
            return None
            
        try:
            # Claude 的 messages 格式转换
            system_msg = None
            user_messages = []
            
            for msg in messages:
                if msg["role"] == "system":
                    system_msg = msg["content"]
                else:
                    user_messages.append(msg)
            
            # Claude API 调用
            response = client.messages.create(
                model=model,
                max_tokens=max_tokens,
                temperature=temperature,
                system=system_msg,
                messages=user_messages
            )
            return LLMResponse(
                content=response.content[0].text,
                provider=LLMProvider.CLAUDE,
                model=model,
                usage={
                    "prompt_tokens": response.usage.input_tokens,
                    "completion_tokens": response.usage.output_tokens
                },
                raw_response=response
            )
        except Exception as e:
            print(f"[LLMClient] Claude call failed: {e}")
            return None
    
    def chat(
        self,
        messages: List[Dict[str, str]],
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 500,
        prefer_provider: Optional[LLMProvider] = None
    ) -> Optional[LLMResponse]:
        """
        统一聊天接口，自动 fallback
        
        优先级：
        1. OpenClaw 模型路由（如果可用）
        2. OpenAI API
        3. Claude API
        4. 返回 None，调用方 fallback 到规则
        """
        # 第一优先：OpenClaw 模型路由（无需 API Key）
        if self.use_openclaw:
            result = self._call_openclaw(messages, temperature, max_tokens)
            if result:
                return result
        
        # 第二优先：OpenAI / Claude API
        provider = prefer_provider or self.default_provider
        default_model = model or self.DEFAULT_MODELS[provider]
        
        if provider == LLMProvider.OPENAI:
            result = self._call_openai(messages, default_model, temperature, max_tokens)
        else:
            result = self._call_claude(messages, default_model, temperature, max_tokens)
        
        if result:
            return result
        
        # Fallback 提供商
        if not self.enable_fallback:
            return None
            
        fallback_provider = (
            LLMProvider.CLAUDE if provider == LLMProvider.OPENAI 
            else LLMProvider.OPENAI
        )
        
        if fallback_provider == LLMProvider.OPENAI and not self.openai_key:
            return None
        if fallback_provider == LLMProvider.CLAUDE and not self.claude_key:
            return None
        
        fallback_model = self.DEFAULT_MODELS[fallback_provider]
        print(f"[LLMClient] Fallback to {fallback_provider.value}")
        
        if fallback_provider == LLMProvider.OPENAI:
            return self._call_openai(messages, fallback_model, temperature, max_tokens)
        else:
            return self._call_claude(messages, fallback_model, temperature, max_tokens)
    
    def quick_chat(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        **kwargs
    ) -> Optional[str]:
        """
        快捷聊天接口，直接返回字符串内容
        
        Args:
            prompt: 用户输入
            system_prompt: 系统提示词
            **kwargs: 传给 chat() 的其他参数
        
        Returns:
            回复字符串，失败返回 None
        """
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        
        response = self.chat(messages, **kwargs)
        return response.content if response else None
    
    def generate(
        self,
        messages: List[Dict[str, str]],
        context: Optional[Dict[str, Any]] = None,
        temperature: float = 0.7,
        max_tokens: int = 500
    ) -> Optional[str]:
        """
        生成回复（兼容旧版 API）
        
        Args:
            messages: 消息列表
            context: 上下文信息（可选）
            temperature: 温度
            max_tokens: 最大 token 数
        
        Returns:
            生成的回复字符串
        """
        response = self.chat(messages, temperature=temperature, max_tokens=max_tokens)
        return response.content if response else None


# ============ 便捷函数 ============

def get_llm_client() -> LLMClient:
    """获取默认 LLM 客户端实例"""
    return LLMClient()


# 测试代码
if __name__ == "__main__":
    client = get_llm_client()
    
    # 测试简单对话
    response = client.quick_chat(
        prompt="你好，请用一句话介绍自己",
        system_prompt="你是一个有帮助的 AI 助手"
    )
    
    if response:
        print(f"回复: {response}")
    else:
        print("调用失败，请检查 API Key")
