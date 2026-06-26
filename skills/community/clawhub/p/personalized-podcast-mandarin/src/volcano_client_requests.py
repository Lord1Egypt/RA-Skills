"""
Volcano Engine Ark API Client (使用requests)
替代官方SDK，解决Windows代理问题
"""

import os
import json
import time
from typing import Type, TypeVar, Optional, Dict, Any
from pydantic import BaseModel
import requests

# 尝试导入 json-repair，如果不存在则使用内置修复
try:
    from json_repair import repair_json
    HAS_JSON_REPAIR = True
except ImportError:
    HAS_JSON_REPAIR = False
    repair_json = None

T = TypeVar('T', bound=BaseModel)


class VolcanoArkClientRequests:
    """火山引擎 Ark API 客户端 (requests实现)"""

    # Doubao-Seed-2.0-lite 模型端点
    DEFAULT_MODEL = "ep-20260330183110-h92rj"
    API_BASE = "https://ark.cn-beijing.volces.com/api/v3"

    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        """
        初始化 Ark 客户端

        Args:
            api_key: 火山引擎 API Key
            model: 模型端点
        """
        self.api_key = api_key or os.getenv("DOUBAO_API_KEY")
        self.model = model or self.DEFAULT_MODEL

        if not self.api_key:
            raise ValueError("API key is required. Set DOUBAO_API_KEY environment variable.")

        # 创建session，完全禁用代理
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        })
        # 彻底禁用代理 - 清空系统代理环境变量并设置空代理
        for proxy_var in ['HTTP_PROXY', 'HTTPS_PROXY', 'http_proxy', 'https_proxy', 'ALL_PROXY']:
            os.environ.pop(proxy_var, None)
            os.environ[proxy_var] = ''
        self.session.proxies = {}
        # 禁用urllib3的代理检测
        self.session.trust_env = False

    def chat_completion(
        self,
        system_prompt: str,
        user_message: str,
        output_schema: Type[T],
        temperature: float = 0.7,
        max_tokens: int = 8192,
        timeout: int = 180,
        max_retries: int = 3,
    ) -> tuple[T, Dict[str, int]]:
        """
        调用模型并解析输出为 Pydantic Schema
        支持指数退避重试

        Args:
            system_prompt: 系统提示词
            user_message: 用户输入消息
            output_schema: 输出数据的 Pydantic 模型类
            temperature: 温度参数
            max_tokens: 最大输出 token 数
            max_retries: 最大重试次数

        Returns:
            (解析后的对象, token使用情况)
        """
        last_error = None

        for attempt in range(max_retries):
            try:
                return self._chat_completion_once(
                    system_prompt, user_message, output_schema,
                    temperature, max_tokens, timeout
                )
            except (requests.exceptions.RequestException, ValueError) as e:
                last_error = e
                is_retryable = isinstance(e, requests.exceptions.RequestException) or \
                              ("Failed to parse JSON" in str(e) and attempt < max_retries - 1)

                if not is_retryable:
                    raise

                # 指数退避
                delay = 2 ** attempt
                print(f"  [Retry {attempt + 1}/{max_retries}] 请求失败，{delay}s后重试...")
                time.sleep(delay)

        raise last_error

    def _chat_completion_once(
        self,
        system_prompt: str,
        user_message: str,
        output_schema: Type[T],
        temperature: float = 0.7,
        max_tokens: int = 8192,
        timeout: int = 180,
    ) -> tuple[T, Dict[str, int]]:
        """单次调用（内部方法）"""
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message},
        ]

        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
        }

        try:
            response = self.session.post(
                f"{self.API_BASE}/chat/completions",
                json=payload,
                timeout=180
            )
            response.raise_for_status()
            data = response.json()

            # 检查是否因为长度被截断
            finish_reason = data["choices"][0].get("finish_reason", "")
            if finish_reason == "length":
                print(f"  [Warning] Output truncated due to length limit")

            # 提取输出内容
            content = data["choices"][0]["message"]["content"]

            # 清理可能的 Markdown 代码块
            content = self._clean_json_content(content)

            # 处理可能的多个JSON对象或额外文本，只取第一个完整JSON
            content = self._extract_first_json(content)

            # 尝试修复截断的JSON
            content = self._fix_truncated_json(content)

            # 解析 JSON
            try:
                result_data = json.loads(content)
            except json.JSONDecodeError as e:
                # 尝试更激进的修复
                content = self._aggressive_json_fix(content)
                try:
                    result_data = json.loads(content)
                except json.JSONDecodeError as e2:
                    raise ValueError(f"Failed to parse JSON response: {e2}\nContent: {content[:500]}")

            # 验证 Schema
            try:
                result = output_schema.model_validate(result_data)
            except Exception as e:
                raise ValueError(f"Schema validation failed: {e}\nData: {result_data}")

            # 提取 token 使用情况
            usage = data.get("usage", {})
            token_usage = {
                "input": usage.get("prompt_tokens", 0),
                "output": usage.get("completion_tokens", 0),
                "total": usage.get("total_tokens", 0),
            }

            return result, token_usage

        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"API request failed: {e}")

    def _clean_json_content(self, content: str) -> str:
        """清理可能的 Markdown 代码块包装"""
        content = content.strip()

        # 移除 ```json 和 ``` 包装
        if content.startswith("```json"):
            content = content[7:]
        elif content.startswith("```"):
            content = content[3:]

        if content.endswith("```"):
            content = content[:-3]

        # 处理可能的中文字符编码问题
        content = content.strip()

        # 查找JSON开始和结束位置
        start_idx = content.find('{')
        end_idx = content.rfind('}')

        if start_idx != -1 and end_idx != -1 and end_idx > start_idx:
            content = content[start_idx:end_idx+1]

        return content

    def _extract_first_json(self, content: str) -> str:
        """提取第一个完整的JSON对象"""
        # 查找第一个 { 和最后一个匹配的 }
        start = content.find('{')
        if start == -1:
            return content

        # 使用括号计数找到匹配的结束括号
        count = 0
        end = start
        for i in range(start, len(content)):
            if content[i] == '{':
                count += 1
            elif content[i] == '}':
                count -= 1
                if count == 0:
                    end = i
                    break

        return content[start:end+1]

    def _fix_truncated_json(self, content: str) -> str:
        """尝试修复截断的JSON"""
        # 检查是否在字符串中间截断
        in_string = False
        escape = False
        last_quote = -1

        for i, char in enumerate(content):
            if escape:
                escape = False
                continue
            if char == '\\':
                escape = True
                continue
            if char == '"' and not escape:
                in_string = not in_string
                if in_string:
                    last_quote = i

        # 如果在字符串中间截断，补全
        if in_string:
            content = content + '"'

        # 检查括号平衡
        brace_count = content.count('{') - content.count('}')
        bracket_count = content.count('[') - content.count(']')

        # 补全缺失的括号
        content = content + ('}' * brace_count) + (']' * bracket_count)

        return content

    def _aggressive_json_fix(self, content: str) -> str:
        """激进的JSON修复，处理严重截断的情况"""
        # 首先尝试使用 json-repair 库（如果可用）
        if HAS_JSON_REPAIR and repair_json:
            try:
                repaired = repair_json(content)
                if repaired:
                    return repaired
            except Exception:
                pass

        # 找到最后一个完整的字段
        lines = content.split('\n')
        fixed_lines = []

        for line in lines:
            # 如果行以逗号或冒号结尾，可能是不完整的
            if line.rstrip().endswith((':', ',')):
                continue
            fixed_lines.append(line)

        content = '\n'.join(fixed_lines)

        # 确保JSON结构完整
        if not content.strip().endswith('}'):
            # 找到最后一个完整的字段后关闭
            last_brace = content.rfind('}')
            if last_brace > 0:
                content = content[:last_brace+1]
            else:
                content = content + '}'

        return content


    def chat_completion_stream(
        self,
        system_prompt: str,
        user_message: str,
        output_schema: Type[T],
        temperature: float = 0.7,
        max_tokens: int = 8192,
        timeout: int = 300,
        verbose: bool = False,
    ) -> tuple[T, Dict[str, int]]:
        """
        流式调用模型并解析输出为 Pydantic Schema
        解决长文本生成超时问题

        Args:
            system_prompt: 系统提示词
            user_message: 用户输入消息
            output_schema: 输出数据的 Pydantic 模型类
            temperature: 温度参数
            max_tokens: 最大输出 token 数
            timeout: 总超时时间（秒），流式生成可能需要较长时间
            verbose: 是否打印进度

        Returns:
            (解析后的对象, token使用情况)
        """
        from .streaming_json_assembler import StreamingJSONAssembler

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message},
        ]

        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "stream": True,
            "stream_options": {
                "include_usage": True
            }
        }

        token_usage = {"input": 0, "output": 0, "total": 0}
        assembler = StreamingJSONAssembler()
        total_chars = 0
        last_update = time.time()

        try:
            # 使用官方SDK进行流式调用
            import volcenginesdkarkruntime as ark
            client = ark.Ark(
                api_key=self.api_key,
                base_url=self.API_BASE,
                timeout=timeout
            )

            stream = client.chat.completions.create(**payload)

            if verbose:
                print("  [Stream] 开始接收...")

            for chunk in stream:
                # 检查是否有usage信息（最后一个chunk）
                if chunk.usage:
                    token_usage = {
                        "input": chunk.usage.prompt_tokens or 0,
                        "output": chunk.usage.completion_tokens or 0,
                        "total": chunk.usage.total_tokens or 0,
                    }
                    continue

                # 提取内容
                delta = chunk.choices[0].delta.content or ''
                if delta:
                    total_chars += len(delta)
                    result = assembler.feed(delta)

                    if verbose and time.time() - last_update > 10:
                        print(f"  [Stream] 已接收 {total_chars} 字符...")
                        last_update = time.time()

                    if result:
                        # 提取到完整JSON
                        if verbose:
                            print(f"  [Stream] 完成，共 {total_chars} 字符")

                        # 验证 Schema
                        try:
                            parsed = output_schema.model_validate(result)
                            return parsed, token_usage
                        except Exception as e:
                            # 验证失败，返回原始数据便于调试
                            raise ValueError(f"Schema validation failed: {e}\nData keys: {list(result.keys())}")

            # 流结束但没有提取到完整JSON
            # 尝试从剩余buffer中强制提取
            remaining = assembler.get_remaining()
            if remaining:
                try:
                    result = json.loads(remaining)
                    parsed = output_schema.model_validate(result)
                    return parsed, token_usage
                except:
                    pass

            raise ValueError(f"Stream ended without complete JSON. Received {total_chars} chars.")

        except Exception as e:
            raise RuntimeError(f"Stream API request failed: {e}")


def create_ark_client_requests(api_key: Optional[str] = None, model: Optional[str] = None):
    """创建 Ark 客户端的工厂函数"""
    return VolcanoArkClientRequests(api_key=api_key, model=model)
