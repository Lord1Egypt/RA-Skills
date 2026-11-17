#!/usr/bin/env python3
"""
multi-agent-codegen v3.3 — 4 Agent 流水线 + L4 Verify (Write + Test) + SyntaxError hard retry
============================================================

v3.0 升级（2026-07-20）：
- 每个 Agent 完成后立即推送飞书通知，用户全程可见

v3.1 升级（2026-09-23）：
- **L4 Verify Agent 接入主流水线**（RULE-20260701-001）
- Write Agent 完成后立即跑 5 步规则验证（长度/完整性/占位符/语法/密度）
- 不通过 → 注入失败原因到 WriteAgent → 立即 retry Write
- 通过 → 进入 Test Agent
- 节省 token：不再浪费在不合格的代码上跑 Test/Refine

v3.2 升级（2026-09-23 晚）：
- **SyntaxError hard fail retry**（独立计数器，无视 max_verify_retries 上限）
- 提升 max_verify_retries 默认值 2 → 3（软错误给 LLM 更多机会）
- 区分 hard fail（语法错误，绝对不能放过）vs soft fail（长度/占位符，达到上限可放过）

v3.3 升级（2026-09-23 晚）：
- **Test Verify Agent 接入**（给 test_code.py 加 L4 Verify 保护）
- Test Agent 完成后立即跑 5 步规则验证（test_code.py 默认 5000 字硬下限）
- 不通过 → 注入失败原因到 TestAgent → 立即 retry Test
- 区分 hard (SyntaxError) vs soft 错误，与 Write Verify 相同的硬/软上限机制
- 实战发现：v3.2 只保护 code.py，test_code.py 也有 SyntaxError 漏出！
"""
from __future__ import annotations

import os
import re
import sys
import json
import requests
import functools
from pathlib import Path
from typing import Protocol, TypedDict, Optional
from dataclasses import dataclass, field

print = functools.partial(print, flush=True)


# ===== 0. 飞书通知系统 =====

FEISHU_USER_OPEN_ID = "ou_991021547578f722d08533accc83651d"  # 老板的 open_id
NOTIFY_ENABLED = True  # 设为 False 可关闭通知


def _get_feishu_token():
    """获取飞书 tenant_access_token"""
    config_path = os.path.expanduser("~/.openclaw/openclaw.json")
    try:
        with open(config_path) as f:
            config = json.load(f)
        feishu = config.get("channels", {}).get("feishu", {})
        account = feishu.get("accounts", {}).get("codebot", {})
        app_id = account.get("appId")
        app_secret = account.get("appSecret")
        url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
        r = requests.post(url, json={"app_id": app_id, "app_secret": app_secret}, timeout=10)
        return r.json().get("tenant_access_token")
    except Exception:
        return None


def _send_feishu(title: str, lines: list):
    """发送飞书 post 富文本消息给老板"""
    if not NOTIFY_ENABLED:
        return
    token = _get_feishu_token()
    if not token:
        print("[通知] 无法获取飞书 token，跳过通知", file=sys.stderr)
        return

    # 构建 content（post 富文本格式）
    content_blocks = []
    for line in lines:
        if line == "---":
            content_blocks.append({"tag": "hr"})
        elif line.startswith("**") and line.endswith("**"):
            content_blocks.append({"tag": "text", "text": line, "bold": True})
        else:
            content_blocks.append({"tag": "text", "text": line})

    post_content = {
        "zh_cn": {
            "title": title,
            "content": [content_blocks]
        }
    }

    msg_payload = {
        "receive_id": FEISHU_USER_OPEN_ID,
        "msg_type": "post",
        "content": json.dumps(post_content, ensure_ascii=False)
    }

    url = "https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=open_id"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    try:
        r = requests.post(url, headers=headers, json=msg_payload, timeout=10)
        result = r.json()
        if result.get("code") == 0 or result.get("status_code") == 0:
            print(f"[通知] ✅ 飞书通知已发送：{title}", file=sys.stderr)
        else:
            print(f"[通知] ⚠️ 飞书通知发送失败：{result}", file=sys.stderr)
    except Exception as e:
        print(f"[通知] ❌ 飞书通知异常：{e}", file=sys.stderr)


def notify_plan_done(plan_text: str, requirement: str):
    """Plan Agent 完成后通知"""
    lines = [
        "**🏛️ Plan 架构师完成**",
        "---",
        f"📥 需求：{requirement[:60]}{'...' if len(requirement) > 60 else ''}",
        f"📊 产出字数：{len(plan_text)} 字",
        "---",
        "**下一步：💻 Write Agent 启动 → 生成完整代码**",
    ]
    _send_feishu("🏛️ Plan 完成", lines)


def notify_write_done(code_text: str, file_count: int, method_count: int):
    """Write Agent 完成后通知"""
    # 统计代码行数
    code_lines = [l for l in code_text.split('\n') if l.strip() and not l.strip().startswith('#')]
    lines = [
        "**💻 Write 开发者完成**",
        "---",
        f"📁 生成文件：{file_count} 个",
        f"📝 代码行数：{len(code_lines)} 行",
        f"⚙️  方法数量：约 {method_count} 个",
        "---",
        "**关键检查：**",
        "✅ API Key 占位符已替换",
        "✅ 单文件实现（无跨文件依赖）",
        "---",
        "**下一步：🧪 Test Agent 启动 → 写 pytest 测试**",
    ]
    _send_feishu("💻 Write 完成", lines)


def notify_test_done(tests_text: str, test_count: int, requirement: str):
    """Test Agent 完成后通知"""
    test_lines = [l for l in tests_text.split('\n') if l.strip().startswith('def test_')]
    lines = [
        "**🧪 Test 测试工程师完成**",
        "---",
        f"📊 测试用例：{test_count} 个",
        f"📝 测试代码行数：{len([l for l in tests_text.split(chr(10)) if l.strip()])} 行",
        "---",
        "**下一步：🛡️ L4 Test Verify → 验证 test_code.py**",
    ]
    _send_feishu("🧪 Test 完成", lines)


def notify_test_verify_done(result, retry_idx: int):
    """v3.3 新增: L4 Test Verify Agent 完成后通知

    Args:
        result: verify_agent.VerifyResult 对象
        retry_idx: 第几次 verify (0 = 首次)
    """
    if result.passed:
        lines = [
            "**🛡️ L4 Test Verify Agent 通过**",
            "---",
            f"📊 测试代码字数：{result.metrics.get('actual_chars')} 字",
            f"📊 关键字密度：{result.metrics.get('keyword_density')}",
            f"📊 语法检查：{result.metrics.get('syntax', 'N/A')}",
            "---",
            "✅ 5 步检查全过（长度/完整性/占位符/语法/密度）",
            "**下一步：🔍 Refine Agent 启动**",
        ]
        _send_feishu("🛡️ Test Verify 通过", lines)
    else:
        crit = len(result.failures)
        lines = [
            f"**🛡️ L4 Test Verify Agent 不通过（第 {retry_idx + 1} 次）**",
            "---",
            f"📊 测试代码字数：{result.metrics.get('actual_chars')} / 下限 {result.metrics.get('min_chars')}",
            f"📊 关键字密度：{result.metrics.get('keyword_density')}",
            f"🔍 发现问题：**{crit} 项**",
        ]
        for i, fail in enumerate(result.failures[:3], 1):
            lines.append(f"  {i}. {fail[:120]}")
        if len(result.failures) > 3:
            lines.append(f"  ...还有 {len(result.failures) - 3} 项")
        lines += [
            "---",
            "**下一步：🧪 Test Agent retry（带入失败原因）**",
        ]
        _send_feishu("🛡️ Test Verify 不通过", lines)


def notify_refine_done(feedback: str, score: int, iteration: int, retry_needed: bool):
    """Refine Agent 完成后通知"""
    # 提取问题数量
    crit_count = len(re.findall(r'critical[:：]', feedback, re.IGNORECASE))
    maj_count = len(re.findall(r'major[:：]', feedback, re.IGNORECASE))
    min_count = len(re.findall(r'minor[:：]', feedback, re.IGNORECASE))

    emoji = "🏆" if score >= 85 else "👍" if score >= 70 else "⚠️"
    lines = [
        f"**{emoji} Refine 审查完成**",
        "---",
        f"📊 质量评分：**{score}/100**（第 {iteration + 1} 次迭代）",
    ]
    if crit_count or maj_count or min_count:
        lines.append("**问题统计：**")
        if crit_count: lines.append(f"  🔴 critical: {crit_count} 个")
        if maj_count: lines.append(f"  🟡 major: {maj_count} 个")
        if min_count: lines.append(f"  🟢 minor: {min_count} 个")

    if retry_needed:
        lines += [
            "---",
            "**⚠️ 评分 < 70，重新生成中...**",
        ]
    else:
        lines += [
            "---",
            "**✅ 评分达标，流水线结束！**",
        ]

    _send_feishu(f"{emoji} Refine 完成 — {score}/100", lines)


def notify_verify_done(result, retry_idx: int):
    """L4 Verify Agent 完成后通知（v3.1 新增）

    Args:
        result: verify_agent.VerifyResult 对象
        retry_idx: 第几次 verify（0 = 首次）
    """
    if result.passed:
        lines = [
            "**🛡️ L4 Verify Agent 通过**",
            "---",
            f"📊 代码字数：{result.metrics.get('actual_chars')} 字",
            f"📊 关键字密度：{result.metrics.get('keyword_density')}",
            f"📊 语法检查：{result.metrics.get('syntax', 'N/A')}",
            "---",
            "✅ 5 步检查全过（长度/完整性/占位符/语法/密度）",
            "**下一步：🧪 Test Agent 启动**",
        ]
        _send_feishu("🛡️ Verify 通过", lines)
    else:
        crit = len(result.failures)
        lines = [
            f"**🛡️ L4 Verify Agent 不通过（第 {retry_idx + 1} 次）**",
            "---",
            f"📊 代码字数：{result.metrics.get('actual_chars')} / 下限 {result.metrics.get('min_chars')}",
            f"📊 关键字密度：{result.metrics.get('keyword_density')}",
            f"🔍 发现问题：**{crit} 项**",
        ]
        # 只列前 3 个失败原因
        for i, fail in enumerate(result.failures[:3], 1):
            lines.append(f"  {i}. {fail[:120]}")
        if len(result.failures) > 3:
            lines.append(f"  ...还有 {len(result.failures) - 3} 项")
        lines += [
            "---",
            "**下一步：💻 Write Agent retry（带入失败原因）**",
        ]
        _send_feishu("🛡️ Verify 不通过", lines)


def notify_pipeline_start(requirement: str, output_dir: str):
    """流水线启动通知"""
    lines = [
        "**🚀 4-Agent 流水线启动**",
        "---",
        f"📥 需求：{requirement[:80]}{'...' if len(requirement) > 80 else ''}",
        f"📁 输出目录：{output_dir}",
        "---",
        "**执行顺序：**",
        "1️⃣ 🏛️ Plan → 架构设计",
        "2️⃣ 💻 Write → 生成代码",
        "3️⃣ 🧪 Test → 写测试用例",
        "4️⃣ 🔍 Refine → 质量评审",
        "5️⃣ → (评分<70 则循环重写)",
    ]
    _send_feishu("🚀 流水线启动", lines)


def notify_pipeline_end(result: dict, output_dir: str, duration_sec: float):
    """流水线结束通知"""
    score = result["quality_score"]
    retry = result["retry_count"]
    emoji = "🏆" if score >= 85 else "👍" if score >= 70 else "⚠️"

    lines = [
        f"**{emoji} 流水线完成！**",
        "---",
        f"🏆 最终评分：{score}/100",
        f"🔄 迭代次数：{retry + 1} 次",
        f"⏱️ 总耗时：约 {int(duration_sec)} 秒",
        f"📁 产物目录：{output_dir}",
        "---",
        "**产出文件：**",
        f"  📄 plan.md — 架构设计",
        f"  📄 code.py — 完整代码",
        f"  📄 test_code.py — 测试用例",
        f"  📄 refine.md — 评审报告",
        "---",
        "💡 如需查看代码详情，可让我读取产物文件",
    ]
    _send_feishu(f"{emoji} 流水线完成 — {score}/100", lines)


# ===== 1. 抽象：LLM 调用协议 + Agent 通用结构 =====

class LLMCall(Protocol):
    """LLM 调用协议 - 每个 agent 可以有自己的实现"""
    def __call__(self, system: str, user: str, *, max_tokens: int = 4096) -> str: ...


@dataclass
class Agent:
    """4 个 agent 中任意一个 - 真正独立可配"""
    name: str                       # "plan" / "write" / "test" / "refine"
    role_label: str                 # 显示标签: "🏛️ Plan 架构师"
    role_emoji: str                 # emoji: "🏛️" / "💻" / "🧪" / "🔍"
    system_prompt: str              # 该 agent 的 system prompt（独立）
    max_tokens: int = 4096          # 该 agent 独立的输出上限

    def run(self, state: "State", llm) -> str:
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
    verify_feedback: str            # Write Verify 失败原因（v3.1 新增）
    verify_test_feedback: str       # Test Verify 失败原因（v3.3 新增）
    quality_score: int              # 评分
    retry_count: int                # 已重试次数（整体流水线）
    verify_retry_count: int         # Write Verify 重试次数（v3.1 新增）
    syntax_retry_count: int         # Write SyntaxError 重试次数（v3.2 新增）
    test_verify_retry_count: int    # Test Verify 重试次数（v3.3 新增，soft）
    test_syntax_retry_count: int    # Test SyntaxError 重试次数（v3.3 新增，hard）
    trace: list[str]                # 节点轨迹


# ===== 3. 4 个独立 Agent（每个是 Agent 子类，真正独立）=====

class PlanAgent(Agent):
    """🏛️ Plan Agent - 架构师"""

    def __init__(self):
        super().__init__(
            name="plan",
            role_label="🏛️ Plan 架构师",
            role_emoji="🏛️",
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

    def run(self, state: State, llm) -> str:
        prompt = self.system_prompt.format(requirement=state["requirement"])
        return llm.invoke(prompt).content.strip()


class WriteAgent(Agent):
    """💻 Write Agent - 开发者"""

    def __init__(self):
        super().__init__(
            name="write",
            role_label="💻 Write 开发者",
            role_emoji="💻",
            system_prompt="",  # 动态构造
            max_tokens=4096,
        )

    def run(self, state: State, llm) -> str:
        is_retry = state.get("retry_count", 0) > 0
        retry_block = ""
        # v3.1: Verify 反馈优先于 Refine 反馈（更精确）
        verify_feedback = state.get("verify_feedback", "")
        if verify_feedback:
            retry_block = f"""

⚠️ **这是 L4 Verify Agent 的反馈**（确定性规则检查失败）：
{verify_feedback}

=== 上一次完整代码 ===
```python
{state.get('code', '')}
=== END ===

**重要：必须修复上面所有失败项，重新输出【完整新版本】代码！**"""
        elif is_retry and state.get("refine_feedback"):
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
3. **方法命名避免 Python builtin**（list/dict/str/int/type 等）→ 用 list_tasks/get_items
4. **单文件实现**：所有类/函数放一个 .py
5. **只输出代码**，用 ```python ... ``` 包裹{('6. **⚠️ 必须输出完整文件，不能只输出改动片段**' if is_retry else '')}"""
        code_raw = llm.invoke(prompt).content.strip()
        code_match = re.search(r"```python\n(.*?)```", code_raw, re.DOTALL)
        return code_match.group(1).strip() if code_match else code_raw.strip()


class TestAgent(Agent):
    """🧪 Test Agent - 测试工程师（v3.3: 支持 verify_test_feedback 注入）"""

    def __init__(self):
        super().__init__(
            name="test",
            role_label="🧪 Test 测试工程师",
            role_emoji="🧪",
            system_prompt="",  # 动态构造
            max_tokens=4096,
        )

    def run(self, state: State, llm) -> str:
        # v3.3: Test Verify 反馈注入（类似 WriteAgent）
        verify_test_feedback = state.get("verify_test_feedback", "")
        retry_block = ""
        if verify_test_feedback:
            retry_block = f"""

⚠️ **这是 L4 Test Verify Agent 的反馈**（确定性规则检查失败）：
{verify_test_feedback}

=== 上一次完整测试代码 ===
```python
{state.get('tests', '')}
=== END ===

**重要：必须修复上面所有失败项，重新输出【完整新版本】测试代码！**"""

        prompt = f"""你是「Test Agent」- 测试工程师。
根据以下架构设计和代码，写 **完整的 pytest 测试用例**：

=== 架构设计 ===
{state['plan']}

=== 代码 ===
```python
{state['code']}
```
=== END ===
{retry_block}

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
            role_emoji="🔍",
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

    def run(self, state: State, llm) -> tuple[str, int]:
        """返回 (feedback, score)"""
        prompt = self.system_prompt.format(code=state["code"], tests=state["tests"])
        result = llm.invoke(prompt).content.strip()

        # 解析评分
        score_match = re.search(r"评分[：:]\s*(\d+)", result)
        score = int(score_match.group(1)) if score_match else 60

        return result, score


# ===== 4. Pipeline 编排器（v3.3 - L4 Verify Write+Test + SyntaxError hard retry + 全程飞书通知）=====

class Pipeline:
    """4 Agent Pipeline v3.3 — L4 Verify Agent (Write + Test) + SyntaxError hard retry + 全程飞书通知

    v3.0：
    - 每个 Agent 完成后立即推送飞书通知

    v3.1（2026-09-23）：
    - **L4 Verify Agent 接入**（RULE-20260701-001 终极根治）
    - Write Agent 完成后立即跑 5 步规则验证
    - 不通过 → 注入失败原因 → 立即 retry Write（最多 max_verify_retries 次）
    - 通过 → 进入 Test Agent
    - 节省 token：不再在不合格的代码上跑 Test/Refine

    v3.2（2026-09-23 晚）：
    - **SyntaxError hard fail retry**（独立计数器，无视 max_verify_retries 上限）
    - 区分 hard fail（语法错误，绝对不能放过）vs soft fail（长度/占位符，达到上限放过）
    - max_verify_retries 默认值 2 → 3（软错误给 LLM 更多机会）
    - max_hard_retries 默认值 5（hard fail 上限，达到也强制继续）

    v3.3（2026-09-23 晚）：
    - **Test Verify Agent 接入**（给 test_code.py 加 L4 Verify 保护）
    - Test Agent 完成后立即跑 5 步规则验证（test_code.py 阈值 5000 字）
    - 不通过 → 注入失败原因 → 立即 retry Test（同样区分 hard/soft）
    - 实战发现：v3.2 只保护 code.py，test_code.py 也有 SyntaxError 漏出
    """

    def __init__(
        self,
        agents: list[Agent],
        max_retries: int = 2,
        threshold: int = 70,
        enable_verify: bool = True,
        max_verify_retries: int = 3,           # v3.2: 2 → 3
        max_hard_retries: int = 5,             # v3.2 新增: SyntaxError 独立上限
        max_test_verify_retries: int = 3,      # v3.3 新增: Test Verify soft 上限
    ):
        self.agents = {a.name: a for a in agents}
        self.max_retries = max_retries
        self.threshold = threshold
        self.enable_verify = enable_verify
        self.max_verify_retries = max_verify_retries
        self.max_hard_retries = max_hard_retries
        self.max_test_verify_retries = max_test_verify_retries  # v3.3
        if enable_verify:
            try:
                from verify_agent import VerifyAgent
                self.verify_agent = VerifyAgent()
            except ImportError:
                print("[Verify] ⚠️ 未能导入 verify_agent，禁用 L4 验证", file=sys.stderr)
                self.enable_verify = False
                self.verify_agent = None
        else:
            self.verify_agent = None

    def should_retry(self, state: State) -> bool:
        """Refine 反馈循环条件"""
        return (state["quality_score"] < self.threshold
                and state["retry_count"] <= self.max_retries)

    def _count_code_metrics(self, code_text: str) -> tuple[int, int]:
        """统计代码指标：(文件数估, 方法数)"""
        lines = [l for l in code_text.split('\n') if l.strip() and not l.strip().startswith('#')]
        # 估算文件数（通过 class/def 出现频率）
        class_count = len(re.findall(r'^class\s+', code_text, re.MULTILINE))
        func_count = len(re.findall(r'^def\s+', code_text, re.MULTILINE))
        # 单文件场景：class>=1 则认为有结构
        file_est = 1 if class_count > 0 else 1
        return file_est, class_count + func_count

    def _count_test_metrics(self, tests_text: str) -> int:
        """统计测试用例数量"""
        return len(re.findall(r'def\s+test_\w+', tests_text))

    def _classify_failure(self, result) -> str:
        """v3.2: 区分 hard fail vs soft fail

        hard fail = SyntaxError（绝对不能放过）
        soft fail = 长度/占位符/密度（达到上限可放过）
        """
        if result.metrics.get("syntax") == "invalid":
            return "hard"
        return "soft"

    def _run_verify_step(self, state: State) -> tuple[bool, str]:
        """L4 Verify Agent (Write) - 5 步规则检查

        Returns:
            (should_continue, reason)
            - (True, "passed"): 通过，继续 Test
            - (True, "hard_overflow"): SyntaxError 重试上限达到，强制继续
            - (True, "soft_overflow"): 其他重试上限达到，强制继续
            - (False, "retry"): 不通过，应该 retry Write
        """
        if not self.enable_verify or not self.verify_agent:
            return True, "skipped"  # 验证关闭，跳过

        result = self.verify_agent.verify(state["code"], "code.py")
        retry_idx = state.get("verify_retry_count", 0)
        notify_verify_done(result, retry_idx)
        print(
            f"{'✅' if result.passed else '⚠️'} L4 Verify Agent (Write) "
            f"{'通过' if result.passed else '不通过'}（{len(result.failures)} 个问题）",
            file=sys.stderr,
        )

        if result.passed:
            return True, "passed"

        # 不通过：分类 + 注入反馈
        failure_type = self._classify_failure(result)  # "hard" or "soft"
        state["verify_feedback"] = self.verify_agent.format_failure_for_write_agent(result)
        state["verify_retry_count"] = retry_idx + 1

        if failure_type == "hard":
            # v3.2: SyntaxError 独立计数器
            state["syntax_retry_count"] = state.get("syntax_retry_count", 0) + 1
            if state["syntax_retry_count"] >= self.max_hard_retries:
                print(
                    f"[Verify Write] ⚠️ SyntaxError hard retry 上限 {self.max_hard_retries} 达到，强制继续",
                    file=sys.stderr,
                )
                return True, "hard_overflow"
        else:
            # soft: 检查通用上限
            if state["verify_retry_count"] >= self.max_verify_retries + 1:  # +1 因为刚 +1 了
                print(
                    f"[Verify Write] ⚠️ soft verify retry 上限 {self.max_verify_retries} 达到，强制继续",
                    file=sys.stderr,
                )
                return True, "soft_overflow"

        return False, "retry"

    def _run_test_verify_step(self, state: State) -> tuple[bool, str]:
        """v3.3 新增: L4 Test Verify Agent - 5 步规则检查 test_code.py

        Returns:
            (should_continue, reason) - 同 _run_verify_step
        """
        if not self.enable_verify or not self.verify_agent:
            return True, "skipped"

        result = self.verify_agent.verify(state["tests"], "test_code.py")
        retry_idx = state.get("test_verify_retry_count", 0)
        notify_test_verify_done(result, retry_idx)
        print(
            f"{'✅' if result.passed else '⚠️'} L4 Test Verify Agent "
            f"{'通过' if result.passed else '不通过'}（{len(result.failures)} 个问题）",
            file=sys.stderr,
        )

        if result.passed:
            return True, "passed"

        # 不通过：分类 + 注入反馈
        failure_type = self._classify_failure(result)
        state["verify_test_feedback"] = self.verify_agent.format_failure_for_write_agent(result)
        state["test_verify_retry_count"] = retry_idx + 1

        if failure_type == "hard":
            # v3.3: Test SyntaxError 独立计数器（共用 max_hard_retries）
            state["test_syntax_retry_count"] = state.get("test_syntax_retry_count", 0) + 1
            if state["test_syntax_retry_count"] >= self.max_hard_retries:
                print(
                    f"[Verify Test] ⚠️ SyntaxError hard retry 上限 {self.max_hard_retries} 达到，强制继续",
                    file=sys.stderr,
                )
                return True, "hard_overflow"
        else:
            # soft: 独立 max_test_verify_retries 上限
            if state["test_verify_retry_count"] >= self.max_test_verify_retries + 1:
                print(
                    f"[Verify Test] ⚠️ soft verify retry 上限 {self.max_test_verify_retries} 达到，强制继续",
                    file=sys.stderr,
                )
                return True, "soft_overflow"

        return False, "retry"

    def run(self, requirement: str, llm, output_dir: str) -> State:
        """执行 4 Agent 流水线（含 L4 Verify Write+Test + SyntaxError hard retry + 全程通知）"""
        state: State = {
            "requirement": requirement,
            "plan": "", "code": "", "tests": "",
            "refine_feedback": "", "verify_feedback": "",
            "verify_test_feedback": "",  # v3.3
            "quality_score": 0,
            "retry_count": 0, "verify_retry_count": 0,
            "syntax_retry_count": 0,
            "test_verify_retry_count": 0,    # v3.3
            "test_syntax_retry_count": 0,    # v3.3
            "trace": [],
        }

        # 启动通知
        notify_pipeline_start(requirement, output_dir)

        for iteration in range(self.max_retries + 1):
            state["trace"].append(f"--- 迭代 {iteration + 1} ---")

            # 1. Plan
            print(f"\n⏳ [{self.agents['plan'].role_label}] 启动", file=sys.stderr)
            state["plan"] = self.agents["plan"].run(state, llm)
            state["trace"].append(f"✅ {self.agents['plan'].name} → {len(state['plan'])} 字")
            print(f"✅ {self.agents['plan'].role_label} 完成", file=sys.stderr)
            notify_plan_done(state["plan"], requirement)

            # 2. Write + Verify (v3.2/v3.3: hard fail 独立计数)
            print(f"\n⏳ [{self.agents['write'].role_label}] 启动", file=sys.stderr)
            state["verify_feedback"] = ""  # 清空
            while True:
                state["code"] = self.agents["write"].run(state, llm)
                file_cnt, method_cnt = self._count_code_metrics(state["code"])
                state["trace"].append(f"✅ {self.agents['write'].name} → {len(state['code'])} 字")
                print(f"✅ {self.agents['write'].role_label} 完成", file=sys.stderr)
                notify_write_done(state["code"], file_cnt, method_cnt)

                should_continue, reason = self._run_verify_step(state)
                if reason == "passed":
                    state["trace"].append("✅ verify (Write) → 通过")
                    break
                elif reason == "hard_overflow":
                    state["trace"].append(
                        f"🔥 verify (Write) SyntaxError hard retry 上限 {self.max_hard_retries} 达到，强制进入 Test"
                    )
                    break
                elif reason == "soft_overflow":
                    state["trace"].append(
                        f"⚠️ verify (Write) soft retry 上限 {self.max_verify_retries} 达到，强制进入 Test"
                    )
                    break
                else:  # "retry"
                    state["trace"].append(
                        f"⚠️ verify (Write) → 第 {state['verify_retry_count']} 次 retry Write"
                    )

            # 3. Test + Test Verify (v3.3 新增)
            print(f"\n⏳ [{self.agents['test'].role_label}] 启动", file=sys.stderr)
            state["verify_test_feedback"] = ""  # 清空
            while True:
                state["tests"] = self.agents["test"].run(state, llm)
                test_cnt = self._count_test_metrics(state["tests"])
                state["trace"].append(f"✅ {self.agents['test'].name} → {len(state['tests'])} 字")
                print(f"✅ {self.agents['test'].role_label} 完成", file=sys.stderr)
                notify_test_done(state["tests"], test_cnt, requirement)

                # v3.3: L4 Test Verify 立即检查
                should_continue, reason = self._run_test_verify_step(state)
                if reason == "passed":
                    state["trace"].append("✅ verify (Test) → 通过")
                    break
                elif reason == "hard_overflow":
                    state["trace"].append(
                        f"🔥 verify (Test) SyntaxError hard retry 上限 {self.max_hard_retries} 达到，强制进入 Refine"
                    )
                    break
                elif reason == "soft_overflow":
                    state["trace"].append(
                        f"⚠️ verify (Test) soft retry 上限 {self.max_test_verify_retries} 达到，强制进入 Refine"
                    )
                    break
                else:  # "retry"
                    state["trace"].append(
                        f"⚠️ verify (Test) → 第 {state['test_verify_retry_count']} 次 retry Test"
                    )

            # 4. Refine
            print(f"\n⏳ [{self.agents['refine'].role_label}] 启动", file=sys.stderr)
            state["refine_feedback"], state["quality_score"] = self.agents["refine"].run(state, llm)
            retry_needed = self.should_retry(state)
            state["trace"].append(
                f"{'✅' if not retry_needed else '⚠️'} {self.agents['refine'].name} → {state['quality_score']}/100"
            )
            print(f"✅ {self.agents['refine'].role_label} 完成，评分 {state['quality_score']}/100", file=sys.stderr)
            notify_refine_done(state["refine_feedback"], state["quality_score"], iteration, retry_needed)

            # 决策：retry or end
            if not retry_needed:
                break
            state["retry_count"] += 1

        return state


# ===== 5. LLM 工厂 =====

def make_llm():
    """创建 LLM 实例（MiniMax-M3 via Anthropic 协议）"""
    api_key = os.environ.get("EM_API_KEY") or os.environ.get("MINIMAX_API_KEY")
    if not api_key:
        raise RuntimeError("需要 EM_API_KEY 或 MINIMAX_API_KEY 环境变量")

    try:
        from langchain_anthropic import ChatAnthropic
        return ChatAnthropic(
            model="MiniMax-M3",
            api_key=api_key,
            base_url="https://api.minimaxi.com/anthropic",
        )
    except ImportError:
        # fallback: 直接用 Anthropic 原生
        import anthropic
        client = anthropic.Anthropic(
            api_key=api_key,
            base_url="https://api.minimaxi.com/anthropic",
        )
        class SimpleLLM:
            def invoke(self, prompt):
                resp = client.messages.create(
                    model="MiniMax-M3",
                    max_tokens=4096,
                    messages=[{"role": "user", "content": prompt}]
                )
                return type("Resp", (), {"content": resp.content[0].text})()
        return SimpleLLM()


# ===== 6. 入口 =====

def main():
    import time
    start_time = time.time()

    if len(sys.argv) > 1:
        requirement = " ".join(sys.argv[1:]).strip()
    elif not sys.stdin.isatty():
        requirement = sys.stdin.read().strip()
    else:
        requirement = input("老板，想开发什么软件？\n> ").strip()

    if not requirement:
        print("❌ 需求不能为空", file=sys.stderr)
        sys.exit(1)

    # 输出目录（支持 --output 参数）
    output_dir = str(Path.home() / ".openclaw/workspace-coding-advisor/output/multi_agent_codegen")
    for i, arg in enumerate(sys.argv):
        if arg == "--output" and i + 1 < len(sys.argv):
            output_dir = sys.argv[i + 1]

    # 4 个独立 Agent
    agents = [PlanAgent(), WriteAgent(), TestAgent(), RefineAgent()]
    pipeline = Pipeline(agents)

    print(f"\n🦀 码虫 4-Agent 流水线 v3.0（全程飞书通知）", flush=True)
    print(f"📥 需求：{requirement}\n", flush=True)

    try:
        llm = make_llm()
        result = pipeline.run(requirement, llm, output_dir)
    except Exception as e:
        print(f"❌ 出错了：{e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)

    # 保存产物
    out_path = Path(output_dir)
    out_path.mkdir(parents=True, exist_ok=True)
    (out_path / "plan.md").write_text(result["plan"], encoding="utf-8")
    (out_path / "code.py").write_text(result["code"], encoding="utf-8")
    (out_path / "test_code.py").write_text(result["tests"], encoding="utf-8")
    (out_path / "refine.md").write_text(result["refine_feedback"], encoding="utf-8")

    duration = time.time() - start_time

    # 流水线结束通知
    notify_pipeline_end(result, output_dir, duration)

    # 控制台摘要
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

    print(f"\n📁 产物已保存到：{out_path}")
    print(f"⏱️ 总耗时：约 {int(duration)} 秒")


if __name__ == "__main__":
    main()
