"""
OpenClaw 入口
===== 架构说明 =====
* skill 职责：流程控制、需求分析、任务拆解、迭代精炼、依赖排序、结果整合、质量验证
* LLM 调用：全部由 OpenClaw 主 Agent 执行，skill 只接收结果不直接调用 API
* 权限边界：skill 不读取环境变量，不访问网络，仅在内存中处理逻辑
"""
import sys
import os
import json

# 添加 src 到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from orchestrator import PrinciplesOrchestrator


def run_in_openclaw(prompt: str, llm_call) -> dict:
    """
    在 OpenClaw 会话中运行 principles-agent
    :param prompt: 用户目标
    :param llm_call: OpenClaw 主 Agent 提供的 LLM 调用函数 (prompt: str) -> str
    :return: 结果字典
    """
    orch = PrinciplesOrchestrator(
        llm_call=llm_call,
        max_iterations=5
    )
    result = orch.run(prompt)
    report = orch.generate_report(result)
    
    return {
        "result": result,
        "report": report,
        "success": result.global_validation_passed
    }
