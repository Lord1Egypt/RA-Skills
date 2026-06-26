#!/usr/bin/env python3
"""
Model Router - 并行调用多模型，结果智能合并
Parallel multi-LLM invocation with result merging
"""
import asyncio, json, time
from typing import List, Dict, Optional, Any
from dataclasses import dataclass
from enum import Enum

# ==================== 配置 ====================
class LLM(Enum):
    GPT4 = "gpt4"
    CLAUDE = "claude"
    KIMI = "kimi"
    DEEPSEEK = "deepseek"
    QWEN = "qwen"
    ERNIE = "ernie"
    GEMINI = "gemini"
    MOE = "moe"

# 模型端点映射
LLM_ENDPOINTS = {
    "gpt4": {"url": "https://api.openai.com/v1/chat/completions", "model": "gpt-4"},
    "claude": {"url": "https://api.anthropic.com/v1/messages", "model": "claude-3-opus"},
    "kimi": {"url": "https://api.moonshot.cn/v1/chat/completions", "model": "kimi-k2"},
    "deepseek": {"url": "https://api.deepseek.com/v1/chat/completions", "model": "deepseek-chat"},
    "qwen": {"url": "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions", "model": "qwen-plus"},
    "ernie": {"url": "https://qianfan.baidubce.com/v3/chat/ernie-4.0-8k", "model": "ernie-4.0-8k"},
    "gemini": {"url": "https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent", "model": "gemini-pro"},
}

# ==================== 数据结构 ====================
@dataclass
class ModelResult:
    model: str
    result: str
    latency: float
    status: str  # success/error
    error: Optional[str] = None

@dataclass
class MergeResult:
    final: str
    sources: List[ModelResult]
    merge_model: str
    total_time: float

# ==================== 核心类 ====================
class ModelRouter:
    """模型路由器 - 并行调用+结果合并"""
    
    def __init__(self, api_keys: Dict[str, str] = None):
        self.api_keys = api_keys or {}
    
    async def invoke(self, model: str, prompt: str, **kwargs) -> ModelResult:
        """调用单个模型"""
        start = time.time()
        try:
            # 模拟调用 (实际需要接入真实API)
            result = await self._call_api(model, prompt, **kwargs)
            return ModelResult(
                model=model,
                result=result,
                latency=time.time() - start,
                status="success"
            )
        except Exception as e:
            return ModelResult(
                model=model,
                result="",
                latency=time.time() - start,
                status="error",
                error=str(e)
            )
    
    async def _call_api(self, model: str, prompt: str, **kwargs) -> str:
        """实际API调用 (模拟)"""
        # 实际实现需要根据不同模型接入API
        await asyncio.sleep(0.1)  # 模拟延迟
        return f"[{model}] 处理: {prompt[:50]}..."
    
    async def parallel_call(self, models: List[str], prompt: str) -> List[ModelResult]:
        """并行调用多个模型"""
        tasks = [self.invoke(m, prompt) for m in models]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # 处理异常结果
        processed = []
        for i, r in enumerate(results):
            if isinstance(r, Exception):
                processed.append(ModelResult(
                    model=models[i],
                    result="",
                    latency=0,
                    status="error",
                    error=str(r)
                ))
            else:
                processed.append(r)
        return processed
    
    async def merge_results(self, results: List[ModelResult], 
                          merge_model: str,
                          task: str,
                          prompt_template: str = None) -> str:
        """合并结果"""
        # 构建合并提示
        merge_prompt = prompt_template or f"""任务: {task}

以下是各模型的回答:
{self._format_results(results)}

请综合以上回答，给出最佳答案。"""
        
        # 调用目标模型合并 (模拟)
        merged = await self.invoke(merge_model, merge_prompt)
        return merged.result if merged.status == "success" else self._fallback_merge(results)
    
    def _format_results(self, results: List[ModelResult]) -> str:
        """格式化结果"""
        lines = []
        for r in results:
            if r.status == "success":
                lines.append(f"### {r.model}\n{r.result}\n")
            else:
                lines.append(f"### {r.model} (失败: {r.error})\n")
        return "\n".join(lines)
    
    def _fallback_merge(self, results: List[ModelResult]) -> str:
        """降级合并: 简单拼接"""
        success = [r for r in results if r.status == "success"]
        if not success:
            return "所有模型调用失败"
        return "\n\n".join([f"## {r.model}\n{r.result}" for r in success])
    
    async def run(self, task: str, 
                 models: List[str],
                 merge_model: str = None,
                 prompt_template: str = None,
                 timeout: int = 60) -> MergeResult:
        """
        主流程: 并行调用 + 结果合并
        
        Args:
            task: 用户任务
            models: 要调用的模型列表
            merge_model: 合并用模型 (默认取第一个)
            prompt_template: 自定义合并提示词
            timeout: 超时时间
            
        Returns:
            MergeResult: 包含最终结果和所有模型结果
        """
        start = time.time()
        
        # 默认合并模型
        if not merge_model:
            merge_model = models[0]
        
        # 并行调用
        results = await asyncio.wait_for(
            self.parallel_call(models, task),
            timeout=timeout
        )
        
        # 合并结果
        final = await self.merge_results(
            results, merge_model, task, prompt_template
        )
        
        return MergeResult(
            final=final,
            sources=results,
            merge_model=merge_model,
            total_time=time.time() - start
        )

# ==================== 便捷函数 ====================
async def route(task: str, models: List[str], **kwargs) -> MergeResult:
    """快捷路由"""
    router = ModelRouter()
    return await router.run(task, models, **kwargs)

# ==================== CLI ====================
if __name__ == "__main__":
    import sys
    
    async def demo():
        print("🔀 Model Router Demo / 模型路由器演示")
        print("=" * 40)
        
        router = ModelRouter()
        
        # 测试并行调用
        print("\n【1】并行调用测试")
        results = await router.parallel_call(
            ["gpt4", "claude", "kimi"],
            "解释什么是人工智能"
        )
        for r in results:
            print(f"  {r.model}: {r.status} ({r.latency:.2f}s)")
        
        # 测试完整流程
        print("\n【2】完整流程测试")
        result = await router.run(
            task="写一首关于春天的诗",
            models=["gpt4", "claude", "kimi"],
            merge_model="claude"
        )
        print(f"  合并模型: {result.merge_model}")
        print(f"  总耗时: {result.total_time:.2f}s")
        print(f"  最终结果: {result.final[:100]}...")
        
        print("\n" + "=" * 40)
        print("✅ Demo完成")
    
    asyncio.run(demo())

__all__ = ["ModelRouter", "route", "LLM", "ModelResult", "MergeResult"]
