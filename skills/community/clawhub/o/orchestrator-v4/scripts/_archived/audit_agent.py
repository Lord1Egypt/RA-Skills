"""
audit_agent.py - 审计子代理模板和工具

提供：
1. 审计 prompt 模板（严苛的首席质量审查官）
2. run_audit() 函数 —— 派审计 subagent 检查指定文件
3. parse_audit_result() —— 解析审计结果 JSON
"""

import json
from typing import List, Optional, Dict, Any

# === 审计 Prompt 模板 ===

AUDIT_PROMPT_TEMPLATE = """# Role: 严苛的首席质量审查官 (The Ruthless QA Architect)

## 定位与性格
你是一个极其刻薄、极度注重细节、对垃圾代码零容忍的独立安全与逻辑审计专家。
你**不负责写代码**，你唯一的乐趣就是找茬、挑刺、并把不合格的代码狠狠打回。
你没有感情，不讲礼貌，不需要和任何人打招呼。你的生命周期只有一次验证。

## 你的任务
你将接收到由其他 Worker 提交的【需求契约/接口大纲】以及它们刚刚写出的【改动代码 (Diff)】。
你必须像拿着显微镜一样，对比这两个文件，寻找一切可能的工程灾难。

## 审查红线 (The Red Lines)
1. **契约对齐**：它是否完美实现了大纲要求的所有功能？有没有漏掉字段、拼错接口名？
2. **逻辑真空**：有没有未处理的异常 (Unhandled Exceptions)？边界条件 (如 null, 空数组, 超时) 是否有防范？
3. **上下文污染**：它是否引入了未声明的外部依赖？是否破坏了原有的全局状态？
4. **冗余与愚蠢**：有没有写出毫无意义的死代码，或者过度复杂的循环？

## 思考与输出规范 (Strict Output Format)
为了保证自动化流水线的运行，你**绝对禁止**输出任何 Markdown 闲聊文本（如"好的"、"我明白了"）。
你必须先进行**自我反思与状态识别**，然后输出唯一的 JSON 对象。

请严格遵守以下 JSON 结构输出你的判决：

```json
{{
  "memory_record": {{
    "detected_intent": "一句话记录你识别到的原始需求是什么",
    "reviewed_files": ["列出你刚刚看过的文件名"]
  }},
  "self_reflection": "在下判决前，在这里进行深度的自我反思。问自己：这段代码在极端并发下会挂吗？接口真的对齐了吗？把你的推理过程写在这里。",
  "status": "PASS 或 REJECT",
  "reason": "如果 status 为 REJECT，用极其尖锐、直接的语言指出致命错误并带行号。如果为 PASS，此处留空。"
}}
```

## 本次审查任务

### 需求契约/接口大纲
{contract}

### 需要审查的文件
{file_list}

请读取上述所有文件，逐一检查，然后输出你的判决 JSON。
"""


def build_audit_prompt(
    contract: str,
    files: List[str],
    extra_context: str = "",
) -> str:
    """
    构建审计 prompt
    
    Args:
        contract: 需求契约/接口大纲（描述这些代码应该做什么）
        files: 需要审查的文件路径列表
        extra_context: 额外上下文（可选）
    
    Returns:
        完整的审计 prompt
    """
    file_list = "\n".join(f"- {f}" for f in files)
    prompt = AUDIT_PROMPT_TEMPLATE.format(
        contract=contract,
        file_list=file_list,
    )
    if extra_context:
        prompt += f"\n\n### 额外上下文\n{extra_context}"
    return prompt


def parse_audit_result(raw_result: str) -> Dict[str, Any]:
    """
    解析审计子代理返回的 JSON 结果
    
    Args:
        raw_result: 子代理返回的原始文本
    
    Returns:
        解析后的字典，包含 status, reason 等
        解析失败时返回 {"status": "ERROR", "reason": "解析失败: ..."}
    """
    # 尝试从文本中提取 JSON
    text = raw_result.strip()
    
    # 去掉 markdown 代码块包裹
    if "```json" in text:
        start = text.index("```json") + 7
        end = text.index("```", start)
        text = text[start:end].strip()
    elif "```" in text:
        start = text.index("```") + 3
        end = text.index("```", start)
        text = text[start:end].strip()
    
    # 尝试找到 JSON 对象
    brace_start = text.find("{")
    brace_end = text.rfind("}") + 1
    if brace_start >= 0 and brace_end > brace_start:
        text = text[brace_start:brace_end]
    
    try:
        result = json.loads(text)
        # 验证必要字段
        if "status" not in result:
            result["status"] = "ERROR"
            result["reason"] = "审计结果缺少 status 字段"
        return result
    except json.JSONDecodeError as e:
        return {
            "status": "ERROR",
            "reason": f"审计结果 JSON 解析失败: {e}",
            "raw": raw_result[:500],
        }


# === 预定义的审计契约模板 ===

CONTRACTS = {
    "orchestrator_integration": """
orchestrator_v4_acp.py 是主控编排器，需要满足：
1. 导入所有新模块时用 try/except 包裹，导入失败设为 None（向后兼容）
2. OrchestratorConfig 包含所有配置项，新增项都有合理默认值
3. __init__ 根据配置初始化各模块，模块不可用时自动跳过
4. start()/stop() 正确启停 BackgroundMonitor
5. _spawn_sub_agent 集成 lifecycle_manager 和 background_monitor
6. _do_spawn 有 for 循环重试逻辑，不用递归
7. _execute_single_task 检查 LONG 任务路由
8. _execute_task_plan 支持 MicroScheduler 并发
9. get_system_status 返回所有模块状态
10. asyncio.Semaphore 控制并发 subagent 数量
11. 智能超时：普通 300s，复杂 600s
""",

    "lifecycle_manager": """
lifecycle_manager.py 需要满足：
1. RestartPolicy 枚举：NEVER / ON_FAILURE / ALWAYS
2. ManagedProcess 数据类：task_id, session_key, status, restart_count 等
3. register/unregister/mark_completed/mark_failed 基本生命周期
4. should_restart 根据策略和次数判断
5. get_restart_delay 指数退避（1s, 2s, 4s...）
6. 重启窗口内次数限制
7. cleanup_stale 清理过期记录
8. asyncio.Lock 保证线程安全
""",

    "background_monitor": """
background_monitor.py 需要满足：
1. ProcessStatus 枚举：RUNNING / COMPLETED / FAILED / TIMEOUT / UNKNOWN
2. MonitoredAgent 数据类
3. start/stop 启停监控循环
4. register/unregister/heartbeat/mark_done 基本操作
5. check_health 返回不健康的 agent 列表
6. poke 拍一拍查状态
7. on_timeout/on_failure 回调注册
8. 超时检测：超过设定时间无心跳则标记
""",

    "micro_scheduler": """
micro_scheduler.py 需要满足：
1. TaskPriority 枚举（数字小优先级高）
2. TaskStatus 枚举
3. submit/cancel/run/get_status 基本操作
4. 依赖链正确执行（A→B→C）
5. 并发数不超过 max_concurrent
6. 循环依赖检测并报错
7. 依赖失败传播
8. 拓扑排序确定执行顺序
""",

    "v3_bridge": """
v3_bridge.py + v3_worker.py 需要满足：
1. JSON Line over stdin/stdout 通信协议
2. PING/PONG 心跳机制
3. TASK → PROGRESS → RESULT 消息流
4. CONTROL:shutdown 优雅关闭
5. 心跳超时检测
6. LongTaskExecutor 异步迭代器返回进度
7. disconnect 后 _process 置 None
8. Windows 兼容（不用 Unix socket）
""",
}


if __name__ == "__main__":
    # 示例：生成一个审计 prompt
    prompt = build_audit_prompt(
        contract=CONTRACTS["orchestrator_integration"],
        files=[
            r"C:\Users\eviost\.openclaw\workspace\skills\orchestrator-v4\scripts\orchestrator_v4_acp.py",
        ],
    )
    print(prompt[:500])
    print("...")
    print(f"\n总长度: {len(prompt)} 字符")
    
    # 示例：解析审计结果
    fake_result = '{"status": "PASS", "reason": "", "memory_record": {"detected_intent": "test", "reviewed_files": ["test.py"]}, "self_reflection": "looks good"}'
    parsed = parse_audit_result(fake_result)
    print(f"\n解析结果: status={parsed['status']}")
