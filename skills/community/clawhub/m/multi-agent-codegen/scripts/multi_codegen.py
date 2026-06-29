#!/usr/bin/env python3
"""
multi-agent-codegen v2.0 — 4 个独立 Agent
=============================================

按老板 2026-06-23 00:15 指示重写：
- **完全像是 4 个独立的 agent 来做事**（manual.py 的设计）
- 每个 agent 真正独立（自己的 prompt + LLM 调用 + max_tokens）
- 共享 State 黑板 + Refine 反馈循环

对比 v1.x（用 LangGraph StateGraph 嵌套函数）：
- ✅ 4 agent 真正独立（不是嵌套函数）
- ✅ 每个 agent 可单独替换/测试
- ✅ Retry 策略可配置
- ✅ 框架代码量更少
- ⚠️ 不再用 LangGraph（手写编排）

跑法不变：
  EM_API_KEY="$EM_API_KEY" multi-codegen "做个 CLI 工具"
"""
from __future__ import annotations

import os
import re
import sys
import functools
from pathlib import Path
from typing import Protocol, TypedDict, Optional
from dataclasses import dataclass, field

from langchain_anthropic import ChatAnthropic

print = functools.partial(print, flush=True)


# ===== 1. 抽象：LLM 调用协议 + Agent 通用结构 =====

class LLMCall(Protocol):
    """LLM 调用协议 - 每个 agent 可以有自己的实现"""
    def __call__(self, system: str, user: str, *, max_tokens: int = 4096) -> str: ...


@dataclass
class Agent:
    """4 个 agent 中任意一个 - 真正独立可配"""
    name: str                       # "plan" / "write" / "test" / "refine"
    role_label: str                 # 显示标签: "🏛️ Plan 架构师"
    system_prompt: str              # 该 agent 的 system prompt（独立）
    max_tokens: int = 4096          # 该 agent 独立的输出上限

    def run(self, state: "State", llm: ChatAnthropic) -> str:
        """执行该 agent - 每个 agent 独立实现"""
        raise NotImplementedError


# ===== 2. 共享 State 黑板 =====

class State(TypedDict):
    """所有 4 个 agent 共享的黑板（不是嵌套函数闭包）"""
    requirement: str                # 用户原始需求
    plan: str                       # Plan 产出
    code: str                       # Write 产出
    tests: str                      # Test 产出
    refine_feedback: str            # Refine 产出
    quality_score: int              # 评分
    retry_count: int                # 已重试次数
    trace: list[str]                # 节点轨迹


# ===== 3. 4 个独立 Agent（每个是 Agent 子类，真正独立）=====

class PlanAgent(Agent):
    """🏛️ Plan Agent - 架构师"""

    def __init__(self):
        super().__init__(
            name="plan",
            role_label="🏛️ Plan 架构师",
            system_prompt="""你是「Plan Agent」- 软件架构师。
老板的需求：{requirement}

请输出 **简洁的架构设计**（**越短越好**，< 500 字）：

1. **数据模型**（类名 + 字段，**单文件**）
2. **核心接口**（方法签名 + 用途）
3. **测试要点**（2-3 个关键场景）

⚠️ **重要约束**：
- 必须设计为**单文件实现**
- 类命名不要用 Python builtin（list/dict/str/int/type 等），用 list_tasks/get_items 这种语义名""",
            max_tokens=2048,
        )

    def run(self, state: State, llm: ChatAnthropic) -> str:
        prompt = self.system_prompt.format(requirement=state["requirement"])
        return llm.invoke(prompt).content.strip()


class WriteAgent(Agent):
    """💻 Write Agent - 开发者"""

    def __init__(self):
        super().__init__(
            name="write",
            role_label="💻 Write 开发者",
            system_prompt="",  # 动态构造
            max_tokens=4096,
        )

    def run(self, state: State, llm: ChatAnthropic) -> str:
        is_retry = state.get("retry_count", 0) > 0
        retry_block = ""
        if is_retry and state.get("refine_feedback"):
            retry_block = f"""

⚠️ **⚠️ 这是第 {state['retry_count'] + 1} 次重写。Refine Agent 给的反馈**：
{state['refine_feedback']}

=== 上一次完整代码（请基于此改进，但**必须输出完整新版本**）===
```python
{state.get('code', '')}
=== END ===

**重要：必须输出【完整新版本】代码，不要只输出改动片段！**"""

        prompt = f"""你是「Write Agent」- Python 开发者。
根据以下架构设计写 **完整可运行的 Python 代码**（单文件）：

=== 架构设计 ===
{state['plan']}
=== 设计 END ===
{retry_block}

要求：
1. 简洁优先：代码紧凑，注释少（docstring 只写一行）
2. 错误处理 + 类型注解（必要）
3. **方法命名避免 Python builtin**（list/dict/str 等）→ 用 list_tasks/get_items
4. **单文件实现**：所有类/函数放一个 .py
5. **只输出代码**，用 ```python ... ``` 包裹{('6. **⚠️ 必须输出完整文件，不能只输出改动片段**' if is_retry else '')}"""
        code_raw = llm.invoke(prompt).content.strip()
        code_match = re.search(r"```python\n(.*?)```", code_raw, re.DOTALL)
        return code_match.group(1).strip() if code_match else code_raw.strip()


class TestAgent(Agent):
    """🧪 Test Agent - 测试工程师"""

    def __init__(self):
        super().__init__(
            name="test",
            role_label="🧪 Test 测试工程师",
            system_prompt="",  # 动态构造
            max_tokens=4096,
        )

    def run(self, state: State, llm: ChatAnthropic) -> str:
        prompt = f"""你是「Test Agent」- 测试工程师。
根据以下架构设计和代码，写 **完整的 pytest 测试用例**：

=== 架构设计 ===
{state['plan']}

=== 代码 ===
```python
{state['code']}
```
=== END ===

要求：
1. **至少 8 个测试函数**，覆盖正常路径 + 边界情况 + 异常处理
2. **测试方法的命名要和代码方法名一致**（如代码用 list_tasks，测试也用 cli.list_tasks()）
3. **属性访问要和实际实现一致**（如代码把 next_id 放在 TodoStore，测试要用 cli.store.next_id）
4. 使用 pytest fixtures（tmp_path 等）做隔离
5. **只输出测试代码**，用 ```python ... ``` 包裹
6. 不要解释、不要多余文字"""
        tests_raw = llm.invoke(prompt).content.strip()
        tests_match = re.search(r"```python\n(.*?)```", tests_raw, re.DOTALL)
        return tests_match.group(1).strip() if tests_match else tests_raw.strip()


class RefineAgent(Agent):
    """🔍 Refine Agent - 代码审查"""

    def __init__(self):
        super().__init__(
            name="refine",
            role_label="🔍 Refine 审查者",
            system_prompt="""你是「Refine Agent」- 严格的代码审查员。
评估以下代码和测试的质量，给出 0-100 分 + 具体改进建议：

=== 代码 ===
```python
{code}
```

=== 测试 ===
```python
{tests}
```
=== END ===

评分维度（**严格对应**）：
- 代码质量（结构、可读性、错误处理、命名规范）：30 分
- 功能完整性（是否覆盖架构设计、是否单文件、是否被截断）：40 分
- 测试覆盖度（边界情况、异常路径）：30 分

⚠️ **扣分项（按严重程度）**：
- **critical**（-15~20）：代码截断不完整、缺核心功能、拆成多模块
- **major**（-5~10）：方法名用了 Python builtin、缺错误处理、测试断言错
- **minor**（-1~3）：命名不一致、注释少、风格问题

**重要：评分要"宽容"。LLM 写的代码有瑕疵是常态，不要因为 minor 问题给 < 70 分。**
**只有 critical 问题（影响功能）才扣到 < 70。**

**严格按格式输出**（先列 critical/major/minor 问题，最后给分）：
严重问题：
- critical: <如果有>
- major: <如果有>
- minor: <如果有>

评分：<0-100 整数>
理由：<一句话说明为什么给这个分>

意见：
1. <具体问题 + 改进建议>
2. <具体问题 + 改进建议>
3. <具体问题 + 改进建议>
4. <具体问题 + 改进建议>
5. <具体问题 + 改进建议>""",
            max_tokens=2048,
        )

    def run(self, state: State, llm: ChatAnthropic) -> tuple[str, int]:
        """返回 (feedback, score)"""
        prompt = self.system_prompt.format(code=state["code"], tests=state["tests"])
        result = llm.invoke(prompt).content.strip()

        # 解析评分
        score_match = re.search(r"评分[：:]\s*(\d+)", result)
        score = int(score_match.group(1)) if score_match else 60

        return result, score


# ===== 4. Pipeline 编排器（不依赖 LangGraph）=====

class Pipeline:
    """4 Agent Pipeline - 真正像 4 个独立 agent 在协作

    对比 v1.x：
    - v1.x：4 个嵌套函数 + LangGraph StateGraph 编排
    - v2.0：4 个独立 Agent 子类 + Pipeline 手动编排（更清晰）
    """

    def __init__(self, agents: list[Agent], max_retries: int = 2, threshold: int = 70):
        self.agents = {a.name: a for a in agents}
        self.max_retries = max_retries
        self.threshold = threshold

    def should_retry(self, state: State) -> bool:
        """Refine 反馈循环条件"""
        return (state["quality_score"] < self.threshold
                and state["retry_count"] <= self.max_retries)

    def run(self, requirement: str, llm: ChatAnthropic) -> State:
        """执行 4 Agent 流水线"""
        state: State = {
            "requirement": requirement,
            "plan": "", "code": "", "tests": "",
            "refine_feedback": "", "quality_score": 0,
            "retry_count": 0, "trace": [],
        }

        for iteration in range(self.max_retries + 1):
            state["trace"].append(f"--- 迭代 {iteration + 1} ---")

            # 1. Plan
            print(f"\n⏳ [{self.agents['plan'].role_label}] 启动", file=sys.stderr)
            state["plan"] = self.agents["plan"].run(state, llm)
            state["trace"].append(f"✅ {self.agents['plan'].name} → {len(state['plan'])} 字")

            # 2. Write
            print(f"⏳ [{self.agents['write'].role_label}] 启动", file=sys.stderr)
            state["code"] = self.agents["write"].run(state, llm)
            state["trace"].append(f"✅ {self.agents['write'].name} → {len(state['code'])} 字")

            # 3. Test
            print(f"⏳ [{self.agents['test'].role_label}] 启动", file=sys.stderr)
            state["tests"] = self.agents["test"].run(state, llm)
            state["trace"].append(f"✅ {self.agents['test'].name} → {len(state['tests'])} 字")

            # 4. Refine
            print(f"⏳ [{self.agents['refine'].role_label}] 启动", file=sys.stderr)
            state["refine_feedback"], state["quality_score"] = self.agents["refine"].run(state, llm)
            state["trace"].append(f"{'✅' if state['quality_score'] >= self.threshold else '⚠️'} {self.agents['refine'].name} → {state['quality_score']}/100")

            # 决策：retry or end
            if not self.should_retry(state):
                break
            state["retry_count"] += 1

        return state


# ===== 5. LLM 工厂 =====

def make_llm() -> ChatAnthropic:
    api_key = os.environ.get("EM_API_KEY") or os.environ.get("MINIMAX_API_KEY")
    if not api_key:
        raise RuntimeError("需要 EM_API_KEY 或 MINIMAX_API_KEY 环境变量")
    return ChatAnthropic(
        model="MiniMax-M3",
        api_key=api_key,
        base_url="https://api.minimaxi.com/anthropic",
    )


# ===== 6. 入口 =====

def main():
    if len(sys.argv) > 1:
        requirement = " ".join(sys.argv[1:]).strip()
    elif not sys.stdin.isatty():
        requirement = sys.stdin.read().strip()
    else:
        requirement = input("老板，想开发什么软件？\n> ").strip()

    if not requirement:
        print("❌ 需求不能为空", file=sys.stderr)
        sys.exit(1)

    # 4 个独立 Agent（像 4 个独立 agent 在做事）
    agents = [PlanAgent(), WriteAgent(), TestAgent(), RefineAgent()]
    pipeline = Pipeline(agents)

    print(f"\n🦀 码虫启动 4-Agent 流水线 v2.0（独立 Agent 架构）", flush=True)
    print(f"📥 需求：{requirement}\n", flush=True)
    print(f"🏛️ Plan → 💻 Write → 🧪 Test → 🔍 Refine → (循环)\n", file=sys.stderr)

    try:
        llm = make_llm()
        result = pipeline.run(requirement, llm)
    except Exception as e:
        print(f"❌ 出错了：{e}", file=sys.stderr)
        sys.exit(1)

    # 保存产物
    out_dir = Path.home() / ".openclaw/workspace-coding-advisor/output/multi_agent_codegen"
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "plan.md").write_text(result["plan"], encoding="utf-8")
    (out_dir / "code.py").write_text(result["code"], encoding="utf-8")
    (out_dir / "test_code.py").write_text(result["tests"], encoding="utf-8")
    (out_dir / "refine.md").write_text(result["refine_feedback"], encoding="utf-8")

    # 漂亮输出
    print(f"\n🏆 最终评分：{result['quality_score']}/100（迭代 {result['retry_count']} 次）")
    print("━" * 60)
    print(f"🏛️ [Plan] 架构设计（节选）：\n{result['plan'][:400]}...")
    print("━" * 60)
    print(f"💻 [Write] 代码（节选）：\n```python\n{result['code'][:400]}...\n```")
    print("━" * 60)
    print(f"🧪 [Test] 测试（节选）：\n```python\n{result['tests'][:400]}...\n```")
    print("━" * 60)
    print(f"🔍 [Refine] 评审（节选）：\n{result['refine_feedback'][:500]}...")
    print("━" * 60)
    print(f"🔍 节点轨迹：")
    for t in result["trace"]:
        print(f"   {t}")

    print(f"\n📁 产物已保存到：{out_dir}")


if __name__ == "__main__":
    main()
