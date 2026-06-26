#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OpenClaw 子会话 LLM 客户端
通过 sessions_spawn 调用真实 LLM
"""

import json
import time
import hashlib
import logging
import os
import sys
from typing import Dict, List, Optional, Any
from dataclasses import dataclass

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class LLMResponse:
    """LLM 响应结构"""
    content: str
    success: bool
    error: Optional[str] = None
    tokens_used: int = 0
    latency: float = 0.0


class SmartCache:
    """智能缓存管理"""
    
    def __init__(self, ttl: int = 3600, max_size: int = 1000):
        self.cache: Dict[str, Dict] = {}
        self.ttl = ttl
        self.max_size = max_size
        self.hit_count = 0
        self.miss_count = 0
    
    def _hash_key(self, prompt: str) -> str:
        """生成缓存键"""
        return hashlib.md5(prompt.encode('utf-8')).hexdigest()
    
    def get(self, prompt: str) -> Optional[str]:
        """获取缓存"""
        key = self._hash_key(prompt)
        if key in self.cache:
            entry = self.cache[key]
            if time.time() < entry['expire_at']:
                self.hit_count += 1
                return entry['value']
            else:
                del self.cache[key]
        self.miss_count += 1
        return None
    
    def set(self, prompt: str, response: str) -> None:
        """设置缓存"""
        if len(self.cache) >= self.max_size:
            self._cleanup()
        
        key = self._hash_key(prompt)
        self.cache[key] = {
            'value': response,
            'expire_at': time.time() + self.ttl
        }
    
    def _cleanup(self) -> None:
        """清理过期缓存"""
        now = time.time()
        expired = [k for k, v in self.cache.items() if v['expire_at'] < now]
        for key in expired:
            del self.cache[key]
    
    def stats(self) -> Dict:
        """获取缓存统计"""
        total = self.hit_count + self.miss_count
        hit_rate = self.hit_count / total if total > 0 else 0
        return {
            'hit_count': self.hit_count,
            'miss_count': self.miss_count,
            'hit_rate': f"{hit_rate:.2%}",
            'size': len(self.cache)
        }


class OpenClawSubagentClient:
    """通过 OpenClaw 子会话调用 LLM"""
    
    def __init__(self, config: Dict):
        self.config = config
        self.cache = SmartCache(
            ttl=config.get('cache', {}).get('ttl', 3600),
            max_size=config.get('cache', {}).get('max_size', 1000)
        )
        self.llm_config = config.get('llm', {})
        self.model = self.llm_config.get('model', 'myprovider/LLM_GLM5')
        self.timeout = self.llm_config.get('timeout', 120)
        self.max_retries = self.llm_config.get('max_retries', 3)
        self.temperature = self.llm_config.get('temperature', 0.1)
        
        # 统计信息
        self.call_count = 0
        self.total_tokens = 0
        self.total_latency = 0.0
        
        # 会话管理
        self._session_id = None
        self._session_created = False
    
    def call(self, prompt: str, use_cache: bool = True) -> LLMResponse:
        """调用 LLM"""
        start_time = time.time()
        
        # 检查缓存
        if use_cache:
            cached = self.cache.get(prompt)
            if cached:
                logger.info("使用缓存响应")
                return LLMResponse(
                    content=cached,
                    success=True,
                    latency=0.0
                )
        
        # 通过子会话调用 LLM
        for attempt in range(self.max_retries):
            try:
                response = self._call_via_subagent(prompt)
                if response.success:
                    # 更新统计
                    self.call_count += 1
                    self.total_tokens += response.tokens_used
                    self.total_latency += response.latency
                    
                    # 设置缓存
                    if use_cache:
                        self.cache.set(prompt, response.content)
                    
                    return response
                else:
                    logger.warning(f"子会话调用失败 (尝试 {attempt + 1}/{self.max_retries}): {response.error}")
                    if attempt < self.max_retries - 1:
                        time.sleep(2)
            except Exception as e:
                logger.warning(f"子会话调用异常 (尝试 {attempt + 1}/{self.max_retries}): {e}")
                if attempt < self.max_retries - 1:
                    time.sleep(2)
        
        return LLMResponse(
            content="",
            success=False,
            error="子会话调用失败，已达到最大重试次数"
        )
    
    def _call_via_subagent(self, prompt: str) -> LLMResponse:
        """通过 OpenClaw agent 本地调用 LLM"""
        start_time = time.time()
        
        try:
            import subprocess
            
            # 使用 openclaw agent --local 命令
            # 这会在本地运行 agent 并调用 LLM
            result = subprocess.run(
                [
                    'openclaw', 'agent',
                    '--local',
                    '--agent', 'main',
                    '--message', prompt,
                    '--json'
                ],
                capture_output=True,
                text=True,
                timeout=self.timeout + 30  # 额外30秒用于进程开销
            )
            
            latency = time.time() - start_time
            
            if result.returncode == 0:
                content = self._parse_agent_response(result.stdout)
                
                if content:
                    return LLMResponse(
                        content=content,
                        success=True,
                        tokens_used=len(prompt) + len(content),
                        latency=latency
                    )
                else:
                    return LLMResponse(
                        content="",
                        success=False,
                        error="无法解析 agent 响应",
                        latency=latency
                    )
            else:
                error_msg = result.stderr[:500] if result.stderr else "未知错误"
                logger.warning(f"openclaw agent 调用失败: {error_msg}")
                return LLMResponse(
                    content="",
                    success=False,
                    error=f"CLI 错误: {error_msg}",
                    latency=latency
                )
                    
        except subprocess.TimeoutExpired:
            logger.warning("agent 调用超时")
            return LLMResponse(
                content="",
                success=False,
                error="agent 调用超时",
                latency=time.time() - start_time
            )
        except Exception as e:
            logger.warning(f"agent 调用失败: {e}")
            return LLMResponse(
                content="",
                success=False,
                error=str(e),
                latency=time.time() - start_time
            )
    
    def _parse_agent_response(self, output: str) -> Optional[str]:
        """解析 agent 响应"""
        lines = output.strip().split('\n')
        
        # 查找 JSON 内容
        json_content = None
        brace_count = 0
        json_start = -1
        
        for i, line in enumerate(lines):
            # 跳过日志行
            if line.startswith('[') and ':' in line[:30]:
                continue
            if any(skip in line for skip in ['Config', 'Plugins', 'Registered', '---', 'Runtime', 'Session']):
                continue
            
            # 检测 JSON 开始
            if line.strip().startswith('{') or line.strip().startswith('['):
                if json_start == -1:
                    json_start = i
                brace_count += line.count('{') + line.count('[')
                brace_count -= line.count('}') + line.count(']')
                
                if brace_count == 0:
                    # JSON 结束
                    json_content = '\n'.join(lines[json_start:i+1])
                    break
        
        if json_content:
            try:
                response_data = json.loads(json_content)
                
                # 处理 OpenClaw agent 响应格式
                if isinstance(response_data, dict):
                    # 尝试从 payloads 中提取文本
                    if 'payloads' in response_data:
                        payloads = response_data.get('payloads', [])
                        if payloads and isinstance(payloads, list):
                            for payload in payloads:
                                if isinstance(payload, dict) and 'text' in payload:
                                    text = payload['text']
                                    # 移除引用块（如 > "..."）
                                    if '\n\n>' in text:
                                        text = text.split('\n\n>')[0].strip()
                                    return text
                    
                    # 尝试其他常见格式
                    if 'content' in response_data:
                        return response_data['content']
                    elif 'response' in response_data:
                        return response_data['response']
                    elif 'result' in response_data:
                        return response_data['result']
                    elif 'message' in response_data:
                        return response_data['message']
                    else:
                        # 返回整个 JSON
                        return json.dumps(response_data, ensure_ascii=False)
                elif isinstance(response_data, list) and response_data:
                    return json.dumps(response_data, ensure_ascii=False)
                    
            except json.JSONDecodeError as e:
                logger.warning(f"JSON 解析失败: {e}")
        
        # 如果没有找到 JSON，尝试提取纯文本响应
        content_lines = []
        for line in lines:
            # 跳过日志行
            if line.startswith('[') and ':' in line[:30]:
                continue
            if any(skip in line for skip in ['Config', 'Plugins', 'Registered', '---', 'Runtime', 'Session']):
                continue
            if line.strip():
                content_lines.append(line)
        
        content = '\n'.join(content_lines).strip()
        return content if content else None
    
    def batch_call(self, prompts: List[str], use_cache: bool = True) -> List[LLMResponse]:
        """批量调用"""
        return [self.call(p, use_cache) for p in prompts]
    
    def stats(self) -> Dict:
        """获取统计信息"""
        avg_latency = self.total_latency / self.call_count if self.call_count > 0 else 0
        return {
            'call_count': self.call_count,
            'total_tokens': self.total_tokens,
            'avg_latency': f"{avg_latency:.2f}s",
            'cache_stats': self.cache.stats()
        }


# 为了兼容性，创建别名
LLMClient = OpenClawSubagentClient

# 单例客户端
_client_instance: Optional[OpenClawSubagentClient] = None


def get_client(config: Optional[Dict] = None) -> OpenClawSubagentClient:
    """获取 LLM 客户端单例"""
    global _client_instance
    if _client_instance is None and config is not None:
        _client_instance = OpenClawSubagentClient(config)
    return _client_instance


def init_client(config: Dict) -> OpenClawSubagentClient:
    """初始化 LLM 客户端"""
    global _client_instance
    _client_instance = OpenClawSubagentClient(config)
    return _client_instance
