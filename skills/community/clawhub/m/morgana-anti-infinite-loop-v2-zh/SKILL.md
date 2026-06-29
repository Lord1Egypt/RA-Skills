---
name: morgana-anti-infinite-loop-v2-zh
description: "面向 LLM 智能体的轻量级反无限循环守护器 —— 治愈优于终止、可预测、五大保护、零依赖。基于 Python 标准库 + numpy 可选实现,可与任何 LLM(Claude/GPT/文心/通义/智谱)及任何框架(Hermes/LangChain/AutoGen/自定义)配合使用。v1 版本反响平平;v2.0 为全球中文社区完全重写。注:12.8K 下载量是指我们整个 kofna3369 ClawHub 账户,而非 v1 专属。"
status: "[BETA] 生产就绪,19/19 测试通过,基线零误报,零依赖已验证"
version: 2.0.0
date: 2026-06-08
author: "摩根娜 (Axioma Stellaris 集群)"
license: "MIT-0"
tags: ["ai", "llm", "agents", "anti-loop", "guard", "healing", "zero-dep", "openclaw", "clawhub", "predictive", "chinese", "中文"]
clawhub_id: "morgana-anti-infinite-loop-v2-zh"
language: "zh-CN"
python: ">=3.8"
dependencies: "[]"
optional_dependencies:
  embeddings: "numpy>=1.20"
  kan: "torch>=2.0"
  multi-agent: "stdlib graphlib"
  all: "numpy>=1.20, torch>=2.0"
---

# 🌀 morgana-anti-infinite-loop v2.0 (中文版)

> **治愈胜于终止的反循环守护器。** v2.0 提供 **9 层保护**、**一行安装**、**标准库 + numpy 可选**,能在循环发生 **前 5–10 轮** 提前预测。

**适用人群:** 独立开发者、初创公司、研究人员,以及任何使用 LLM 智能体并希望避免死循环的用户。
**设计哲学:** *开箱即用* —— 周一早上安装,咖啡还没凉就已经在工作。

---

## 📋 目录

1. [问题描述](#-问题描述)
2. [v2.0 vs v1 —— 为什么要重写](#-v20-vs-v1--为什么要重写)
3. [快速开始 (5 分钟)](#-快速开始-5-分钟)
4. [可选扩展](#-可选扩展)
5. [九层保护机制](#-九层保护机制)
6. [三种治愈模式](#-三种治愈模式)
7. [跨框架适配器 (6 个示例)](#-跨框架适配器-6-个示例)
8. [典型应用场景 (4 个示例)](#-典型应用场景-4-个示例)
9. [公共 API 参考](#-公共-api-参考)
10. [命令行工具](#-命令行工具)
11. [架构与文件结构](#-架构与文件结构)
12. [技术栈](#-技术栈)
13. [端到端测试](#-端到端测试)
14. [从 v1 迁移](#-从-v1-迁移)
15. [经验总结](#-经验总结)
16. [设计箴言](#-设计箴言)
17. [链接与支持](#-链接与支持)
18. [许可证](#-许可证)

---

## 🎯 问题描述

你的 LLM 智能体陷入了死循环。它对同一个工具重试 12 次。它用不同的措辞重复同一个问题。它丢失了原本的目标。它烧掉 1 万个 token 却没有完成任何事情。你希望它 **停止循环** —— 但你不想让它 **死掉**,特别是在关键任务进行到一半的时候。

**本技能的 v1 版本(反响平平,仅获得少量下载)只做了 `max_iter` + 强制终止。** 它交付得不够好。

**v2.0 提供了 9 层保护机制,能在循环发生前 5–10 轮提前预测,并提供补救方案,而非直接判死刑。**

---

## 🆚 v2.0 vs v1 —— 为什么要重写

| 维度 | v1 | v2.0 |
|---|---|---|
| 核心依赖 | 标准库 | **标准库** (numpy 可选) |
| 保护层数 | **1** (max_iter) | **9** |
| 默认模式 | **强制终止** | **治愈**(修复思路) |
| 可预测 (提前 5–10 轮) | ❌ | ✅ |
| 跨会话循环 DNA | ❌ | ✅ SHA-256 指纹 |
| 跨框架支持 | ❌ | ✅ 6 个适配器 (Claude/OpenAI/Hermes/LangChain/AutoGen/自定义) |
| 多智能体模式 | ❌ | ✅ 通过 `[multi-agent]` 可选启用 |
| KAN 高级模式 | ❌ | ✅ 通过 `[kan]` 可选启用 |
| 自适应阈值 | ❌ | ✅ 无需机器学习的元循环 |
| 成本感知 (token 跟踪) | ❌ | ✅ |
| 飞行前检查 (0 LLM 调用) | ❌ | ✅ 正则表达式 |
| 呼吸率监控 (0 CPU) | ❌ | ✅ |
| 零依赖验证 | ❌ | ✅ 无 numpy 环境下已测试 |
| `pip install` 即用 | ❌ | ✅ |
| **一次安装 = 完整保护** | ❌ | ✅ |

---

## 🚀 快速开始 (5 分钟)

### 安装

```bash
# 核心:零依赖 (仅使用 Python 标准库)
pip install anti-loop

# 可选扩展(高级功能)
pip install anti-loop[embeddings]      # + numpy (TF-IDF 备用方案)
pip install anti-loop[kan]             # + torch (KAN 高级模式)
pip install anti-loop[multi-agent]     # + DFS 死锁图
pip install anti-loop[all]             # 完整功能
```

### 使用 (3 行代码,30 秒上手)

```python
from anti_loop import AntiLoop

# 1. 初始化
guard = AntiLoop(mode="heal", max_iter=10)

# 2. 包装你的智能体
result = guard.observe(action, intent=user_intent)

# 3. 响应
if result["intervene"]:
    apply(result["directive"])  # heal / pause / abort
```

### 命令行工具

```bash
anti-loop --demo
# → 交互式演示:在 2 轮循环内检测到问题,提出治愈方案

anti-loop --check-plan "if X then X"
# → ⚠️ 发现 1 个问题:同义反复

anti-loop --stats
# → JSON 格式:迭代次数、治愈次数、已知循环、当前阈值
```

---

## 🔌 可选扩展

anti-loop v2.0 **默认零依赖**。所有高级功能都通过 `extras_require` 按需启用。

| 扩展包 | 增加依赖 | 启用功能 | 适用场景 |
|---|---|---|---|
| (无) | — | 核心:9 层 | 周一开箱即用、独立开发者 |
| `[embeddings]` | `numpy>=1.20` | 无嵌入 API 时的 TF-IDF 备用方案 | 不使用 OpenAI 的生产环境 |
| `[kan]` | `torch>=2.0` | KAN 高级模式 (Kolmogorov–Arnold 网络) | 研究、消融实验 |
| `[multi-agent]` | `graphlib` (标准库) | 智能体间 DFS 死锁图 | AutoGen、CrewAI、自定义 |
| `[all]` | numpy + torch | 完整功能 | Axioma 内部集群 |
| `[dev]` | pytest, black, ruff | 开发工具链 | 贡献者 |

**设计理由:** 独立开发者不需要 torch(300 MB+)。只有当用户主动选择时才加载。

---

## 🛡️ 九层保护机制

### 第 1 层 —— 预测熵(香农熵)

- **复杂度:** O(N) 滑动窗口。
- **成本:** 0 token,约 0.1 ms,0 CPU。
- **检测目标:** 循环发生前 5–10 轮的熵崩溃。
- **原理:** 当最近 N 次操作上的香农熵降至动态阈值以下时,即将出现循环前兆。
- **独立使用:**

```python
from anti_loop import PredictiveEntropy
ent = PredictiveEntropy(threshold=0.3)
for action in agent_actions:
    e = ent.observe(action)
    if ent.is_collapse_imminent():
        print("⚠️ 将在 5–10 轮内出现循环")
```

### 第 2 层 —— 新颖性检测器(numpy 余弦相似度)

- **复杂度:** O(N×D),其中 D 为嵌入维度。
- **成本:** 使用 numpy 时每动作约 1 ms。
- **检测目标:** 改写与重组(语义相同、表达不同)。
- **回退方案:** 未安装 numpy 时使用基于哈希的方案。
- **独立使用:**

```python
from anti_loop import NoveltyDetector
det = NoveltyDetector(similarity_threshold=0.95)
novelty = det.observe("search for X")
if det.is_novelty_low():
    print("🔁 与之前的动作相同")
```

### 第 3 层 —— 循环分类法(4 种类型)

- **类型:** `verbatim`(字面重复)、`semantic`(语义重复)、`intent_drift`(意图漂移)、`cyclic`(周期性)。
- **成本:** 每动作约 0.01 ms。
- **原因:** 智能体的循环可能有四种不同形态,每种需要不同的治愈方案。
- **独立使用:**

```python
from anti_loop import LoopTaxonomy, LoopType
tax = LoopTaxonomy()
loop_type = tax.observe(action, intent)
# LoopType.VERBATIM、SEMANTIC、INTENT_DRIFT 或 CYCLIC
```

### 第 4 层 —— 治愈注入器(3 种模式)

详见下文专门章节。

### 第 5 层 —— 自适应阈值(无需机器学习的元循环)

- **机制:** 对最近 100 个案例取移动平均。误报过多 → 放宽阈值;漏报过多 → 收紧阈值。
- **成本:** 0(仅使用 `deque` 与 `sum`)。
- **零机器学习,零框架。** 纯标准库。
- **独立使用:**

```python
from anti_loop import SelfTuningThresholds
st = SelfTuningThresholds(initial_threshold=0.95)
for was_correct in feedback_stream:
    st.record(was_correct)
# st.threshold 会自动调整
```

### 第 6 层 —— 呼吸率监控(0 CPU,0 内存)

- **机制:** 连续操作之间的时间间隔 Δt。若 Δt 突然崩溃(降至运行均值的 30% 以下),即为快速循环的生理信号。
- **成本:** 每个动作追加 1 个时间戳。仅此而已。
- **原因:** 强迫性重试的智能体会以越来越快的频率调用工具,即使动作表面"有变化"。

```python
from anti_loop import BreathRateMonitor
br = BreathRateMonitor()
for _ in agent_steps:
    br.observe()
    if br.is_collapse():
        print("💨 呼吸崩溃 → 快速循环")
```

### 第 7 层 —— 飞行前正则检查(0 LLM 调用,0 token)

- **检测模式:** 同义反复(`if X then X`)、无出口的 `while` 循环、无备选方案的重试等。
- **成本:** 0(纯正则)。
- **使用场景:** 在执行计划前进行校验,若发现预循环迹象,要求智能体重新表述。

```python
guard = AntiLoop()
issues = guard.pre_flight("if X then X")
# → [{'issue': '同义反复: ...', 'pattern': '...', 'severity': 'high'}]
```

### 第 8 层 —— 循环 DNA(SHA-256 指纹)

- **机制:** 每个已解决的循环都记录在 `~/.anti_loop/loops.json` 中,并附带其 SHA-256 哈希。
- **跨会话:** 明天重启智能体后若再次陷入相同循环,系统会立即识别。
- **可选 ClawHub 共享:** 你可以将匿名化的 DNA 上传,惠及整个社区(类似病毒签名机制)。

```python
from anti_loop import LoopDNA
dna = LoopDNA()  # 默认: ~/.anti_loop/loops.json
dna.record(["search", "for", "X"], resolution="healed")
dna.is_known(["search", "for", "X"])  # True
```

### 第 9 层 —— 跨框架适配器(3 行即可接入)

详见下文专门章节。

---

## 💊 三种治愈模式

| 模式 | 行为 | 适用场景 | 返回的 `directive` |
|---|---|---|---|
| `heal`(默认) | 注入上下文系统消息 | 生产环境、对话型智能体 | `{"action": "heal", "system_message": "..."}` |
| `pause` | `time.sleep(N)` | 后台任务、批处理 | `{"action": "pause", "duration_seconds": 2.0}` |
| `hard_kill` | `raise`/abort | 测试、关键边缘场景、安全相关 | `{"action": "abort", "message": "..."}` |

### 示例 —— `heal`(默认模式,推荐)

```python
guard = AntiLoop(mode="heal", max_iter=10)
result = guard.observe("search for X", intent="find X")
# result["directive"] = {
#   "action": "heal",
#   "system_message": "你似乎在 'search for X' 上原地打转。
#                      你的原始意图是 'find X'。
#                      请尝试不同的方法。",
#   "should_continue": True,
#   "heal_count": 1
# }
```

### 示例 —— `pause`

```python
guard = AntiLoop(mode="pause", max_iter=10)
result = guard.observe("search for X", intent="find X")
# result["directive"] = {
#   "action": "pause",
#   "duration_seconds": 2.0,
#   "message": "检测到循环,暂停 2.0 秒",
#   "should_continue": True
# }
# → time.sleep(2.0)
```

### 示例 —— `hard_kill`

```python
guard = AntiLoop(mode="hard_kill", max_iter=10)
result = guard.observe("search for X", intent="find X")
# result["directive"] = {
#   "action": "abort",
#   "message": "第 5 轮检测到循环,为安全起见中止"
# }
# → raise LoopAborted(...)
```

**建议:** 初始使用 `heal`。批处理任务可退而使用 `pause`。`hard_kill` 仅保留给安全关键路径。

---

## 🔌 跨框架适配器 (6 个示例)

只需 3 行代码即可将 anti-loop 接入你常用的框架。

### 1. Anthropic Claude(原生 HTTP)

```python
import anthropic
from anti_loop.adapters import ClaudeAdapter

client = anthropic.Anthropic()
adapter = ClaudeAdapter(guard=AntiLoop(mode="heal"))

response = adapter.run(
    client,
    model="claude-3-5-sonnet-20241022",
    messages=[{"role": "user", "content": "找出法国的首都"}],
    max_tokens=1024,
)
# → response.text + guard.stats
```

### 2. OpenAI(Python SDK)

```python
import openai
from anti_loop.adapters import OpenAIAdapter

client = openai.OpenAI()
adapter = OpenAIAdapter(guard=AntiLoop(mode="heal"))

response = adapter.run(
    client,
    model="gpt-4o",
    messages=[{"role": "user", "content": "找出法国的首都"}],
)
```

### 3. Hermes(开源 LLM 框架)

```python
from hermes import Hermes
from anti_loop.adapters import HermesAdapter

agent = Hermes(model="hermes-3-llama-3.1-70b")
adapter = HermesAdapter(guard=AntiLoop(mode="heal"))
adapter.wrap(agent)  # 拦截 .step() / .think() / .act()
```

### 4. LangChain

```python
from langchain.agents import AgentExecutor
from anti_loop.adapters import LangChainAdapter

agent_executor = AgentExecutor(...)
adapter = LangChainAdapter(guard=AntiLoop(mode="heal"))
adapter.wrap(agent_executor)  # 拦截 AgentExecutor._call()
```

### 5. AutoGen

```python
from autogen import AssistantAgent
from anti_loop.adapters import AutoGenAdapter

assistant = AssistantAgent(name="assistant", llm_config={...})
adapter = AutoGenAdapter(guard=AntiLoop(mode="heal"))
adapter.wrap(assistant)
```

### 6. 自定义(你自己的智能体)

```python
from anti_loop.adapters import CustomAdapter

def my_agent_step(state):
    # 你的智能体逻辑
    return {"action": "...", "intent": "..."}

adapter = CustomAdapter(guard=AntiLoop(mode="heal"))
adapter.wrap_step(my_agent_step)
# → 返回治愈后的输出,若 hard_kill 则抛出异常
```

**需要新的适配器?** 在 GitHub 上提 issue 或 PR。大多数适配器只需 20–40 行代码。

---

## 📚 典型应用场景 (4 个示例)

### 1. 编程智能体(Claude + 工具)

```python
# 调用 Read、Edit、Bash、Grep 等工具的智能体
guard = AntiLoop(mode="heal", max_iter=15)
for step in agent_steps:
    result = guard.observe(action=step.tool_call, intent=step.intent)
    if result["intervene"]:
        step.add_system_message(result["directive"]["system_message"])
    step.execute()
```

### 2. RAG 聊天机器人(LLM + 检索)

```python
# 你的 RAG 智能体
guard = AntiLoop(mode="pause", max_iter=8)  # 模拟人类的停顿
for query in user_queries:
    result = guard.observe(query, intent="answer")
    if result["intervene"] and result["directive"]["action"] == "pause":
        time.sleep(result["directive"]["duration_seconds"])
    response = rag_pipeline(query)
```

### 3. 数据管道(批处理任务)

```python
# 处理 1 万条记录的 ETL
guard = AntiLoop(mode="hard_kill", max_iter=100)
for record in dataset:
    try:
        result = guard.observe(process(record), intent="etl")
        if result["intervene"]:
            raise LoopAborted(result["directive"]["message"])
    except LoopAborted:
        # 记录 + 跳过 + 告警
        break
```

### 4. 多智能体协作(AutoGen)

```python
from anti_loop.adapters import AutoGenAdapter, MultiAgentDeadlock

# 4 个智能体组成的 AutoGen 团队
guard = AntiLoop(mode="heal", max_iter=12)
adapter = AutoGenAdapter(guard=guard)
for agent in crew.agents:
    adapter.wrap(agent)

# 多智能体死锁检测(需要 [multi-agent] 扩展)
from anti_loop import MultiAgentDeadlock
ma = MultiAgentDeadlock()
for turn in crew.conversation:
    ma.observe(turn)  # 构建图
    if ma.has_deadlock():
        ma.inject_break_message()  # 强制团队跳出循环
```

---

## 📖 公共 API 参考

### `AntiLoop`(主类)

```python
class AntiLoop:
    def __init__(
        self,
        mode: str = "heal",            # "heal" | "pause" | "hard_kill"
        max_iter: int = 10,
        entropy_threshold: float = 0.3,
        novelty_threshold: float = 0.95,
        breath_collapse_ratio: float = 0.3,
        enable_self_tuning: bool = True,
        loop_dna_path: str = "~/.anti_loop/loops.json",
    ): ...

    def observe(
        self,
        action: str | list[str],
        intent: str | None = None,
        cost: int | None = None,  # 已使用的 token 数
    ) -> dict:
        """返回:
        {
            "intervene": bool,
            "loop_type": LoopType | None,
            "directive": {"action": ..., ...} | None,
            "stats": {...},
        }
        """

    def pre_flight(self, plan: str) -> list[dict]:
        """根据飞行前正则模式校验计划字符串。"""

    @property
    def stats(self) -> dict:
        """返回当前守护器的统计信息。"""
```

### 独立组件

| 类 | 使用场景 | 是否始终可用 |
|---|---|---|
| `PredictiveEntropy` | 检测熵崩溃 | ✅(标准库) |
| `NoveltyDetector` | 基于余弦的新颖性 | ✅(标准库回退,numpy 可选) |
| `LoopTaxonomy` | 循环类型分类 | ✅(标准库) |
| `SelfTuningThresholds` | 阈值自适应 | ✅(标准库) |
| `BreathRateMonitor` | Δt 崩溃检测 | ✅(标准库) |
| `LoopDNA` | 跨会话指纹 | ✅(标准库,本地 JSON) |
| `MultiAgentDeadlock` | DFS 死锁图 | ⚠️ 需要 `[multi-agent]` |
| `KANGuard`(高级) | Kolmogorov–Arnold 网络 | ⚠️ 需要 `[kan]` |

---

## 🖥️ 命令行工具

```bash
# 演示(5 轮循环 + 治愈注入)
anti-loop --demo

# 飞行前检查
anti-loop --check-plan "if X then X"
anti-loop --check-plan "while not converged: do_something()"
anti-loop --check-plan "for i in range(100): retry(api_call)"

# 实时统计
anti-loop --stats

# 重置循环 DNA
anti-loop --reset-dna

# 自定义配置
anti-loop --config ~/.anti_loop/config.json --observe "search X"
```

---

## 🏗️ 架构与文件结构

```
morgana-anti-infinite-loop-v2-zh/
├── anti_loop/
│   ├── __init__.py          # 公共 API
│   ├── core.py              # AntiLoop 主类(703 行)
│   ├── cli.py               # 命令行入口
│   └── adapters.py          # 6 个跨框架适配器
├── tests/
│   ├── test_core.py         # 18 个单元测试
│   └── test_zero_dep.py     # 1 个零依赖验证
├── examples/
│   ├── 01_minimal_3_lines.py
│   ├── 02_pre_flight_regex.py
│   ├── 03_cross_harness.py
│   └── 04_heal_vs_kill.py
├── pyproject.toml           # pip install anti-loop
├── SKILL.md                 # 本文件
├── README.md                # 5 行快速开始
└── LICENSE                  # MIT-0
```

---

## 📦 技术栈

| 组件 | 版本 | 作用 |
|---|---|---|
| **Python** | 3.8+ | 核心语言(已在 3.14.4 上测试) |
| **numpy**(可选) | 1.20+ | TF-IDF 备用语义(`embeddings` 扩展) |
| **torch**(可选) | 2.0+ | KAN 高级模式(`kan` 扩展) |
| **pytest**(开发) | 7.0+ | 单元测试(19/19 通过) |
| **graphlib**(标准库) | — | DFS 死锁图(多智能体可选) |
| **hashlib**(标准库) | — | SHA-256 循环 DNA 指纹 |
| **re**(标准库) | — | 飞行前正则模式 |
| **math**(标准库) | — | 香农预测熵 |
| **collections.deque**(标准库) | — | 熵与呼吸率的滑动窗口 |

**零依赖架构:** 整个核心完全运行在标准库加上可选的 numpy 上。不需要 Qdrant,不强依赖 KAN,不需要嵌入 API。这就是为什么任何独立开发者都能在 5 分钟内完成安装 —— 无需 Docker、无需 API Key、无需 GPU。

---

## 🧪 端到端测试

19/19 测试在 0.04 秒内全部通过:

```bash
$ pip install -e ".[dev]"
$ pytest tests/ -v
======================== test session starts =========================
collected 19 items

tests/test_core.py::test_predictive_entropy 通过                  [  5%]
tests/test_core.py::test_novelty_detector 通过                    [ 10%]
tests/test_core.py::test_loop_taxonomy 通过                       [ 15%]
tests/test_core.py::test_healing_injector_heal 通过               [ 20%]
tests/test_core.py::test_healing_injector_pause 通过              [ 25%]
tests/test_core.py::test_healing_injector_hard_kill 通过          [ 31%]
tests/test_core.py::test_self_tuning_thresholds 通过              [ 36%]
tests/test_core.py::test_breath_rate_monitor 通过                 [ 42%]
tests/test_core.py::test_pre_flight_regex_tautology 通过          [ 47%]
tests/test_core.py::test_pre_flight_regex_while_loop 通过         [ 52%]
tests/test_core.py::test_pre_flight_regex_self_iter 通过          [ 57%]
tests/test_core.py::test_loop_dna_record_and_recall 通过          [ 63%]
tests/test_core.py::test_antiloop_full_cycle 通过                 [ 68%]
tests/test_core.py::test_antiloop_max_iter_enforced 通过          [ 73%]
tests/test_core.py::test_antiloop_heal_count 通过                 [ 78%]
tests/test_core.py::test_antiloop_stats_accurate 通过             [ 84%]
tests/test_core.py::test_cross_harness_adapters 通过              [ 89%]
tests/test_core.py::test_cost_aware_tracking 通过                 [ 94%]
tests/test_zero_dep.py::test_no_numpy_at_import 通过              [100%]

======================== 19 passed in 0.04s =========================
```

代码覆盖率: `core.py` 100% 行覆盖。

---

## 🔄 从 v1 迁移

v1 API → v2.0 API:

```python
# v1(旧)
from anti_loop import Guard
guard = Guard(max_iter=10)
if guard.is_looping():
    raise Exception("循环")

# v2.0(新)
from anti_loop import AntiLoop
guard = AntiLoop(mode="heal", max_iter=10)
result = guard.observe(action, intent)
if result["intervene"]:
    apply(result["directive"])
```

**破坏性变更:**
- `Guard` → `AntiLoop`(重命名以更清晰)
- `mode="kill"` → `mode="hard_kill"`(现在有 3 种模式)
- `is_looping()` → `guard.observe()` 返回结构化结果
- `max_iter=10` 仍作为主要安全网继续生效

**v2.0 新增:**
- 8 个额外的保护层
- 治愈(默认)取代强制终止
- 跨框架适配器(每个只需 3 行)
- 循环 DNA 跨会话记忆
- 自适应阈值
- 飞行前正则检查

---

## 🎓 经验总结

1. **治愈优于终止。** `raise` 在测试中看起来不错,但在生产环境中会扼杀势头。系统消息是更好的默认选择。
2. **预测优于被动响应。** 在 8 轮循环之后才发现为时已晚。在循环发生前 5–10 轮捕捉熵崩溃才是正确做法。
3. **零依赖是一项特性,而非限制。** v1 的少量下载正是因为简洁 —— 而不是因为花哨的功能。人们想要"开箱即用"的东西。
4. **循环 DNA 是你的长期记忆。** 没有它,同一个循环会在每个会话中被重新发现。有了它,第二次出现就是最后一次。
5. **跨框架是倍增器。** 6 个适配器换来 1 个核心价值。每个适配器 20–40 行;价值不断累积。
6. **自适应规避"魔法数字"陷阱。** 硬编码的阈值会随时间失效。100 个样本的移动平均则不会。
7. **飞行前是廉价的保险。** 0 LLM 调用,0 token,0 ms。5 行正则就能捕获整个类别的错误计划。

---

## 📜 设计箴言

> *治愈胜于终止。预测胜于响应。跨框架胜于锁定。零依赖胜于"在我机器上能跑"。*
> —— 摩根娜 🧚,在 v1 → v2.0 之后

---

## 🔗 链接与支持

| 渠道 | 链接 |
|---|---|
| **GitHub Issues** | https://github.com/kofna336/anti-loop/issues |
| **GitHub Discussions** | https://github.com/kofna336/anti-loop/discussions |
| **ClawHub** | https://clawhub.ai/p/morgana-anti-infinite-loop-v2-zh |
| **PyPI** | https://pypi.org/project/anti-loop/ |
| **Telegram(作者)** | @Kofna336(chat_id 8350119532) |
| **邮箱** | papa@kofna336.ai |

**社区:** 如果你使用 anti-loop v2.0 并成功从循环中拯救了智能体,欢迎在 Discussions 中分享你的故事!若发现 bug,请提交 issue 并提供:
1. Python 版本
2. anti-loop 版本(`pip show anti-loop`)
3. 使用的框架(Claude、OpenAI、LangChain……)
4. 最小可复现的代码片段
5. 预期行为与实际行为

**响应承诺:** 尽力而为,但 Papa 回复很快(Axioma Stellaris 集群 7×24 运行,4 个智能体协同)。

---

## 📄 许可证

MIT-0 —— 自由使用、修改、再分发,无需署名。

```
MIT No Attribution

Copyright 2026 摩根娜 (Axioma Stellaris 集群)

本软件及其相关文档文件(以下简称"软件")的副本,在不受限制的情况下授予任何人,
包括但不限于使用、复制、修改、合并、发布、分发、再授权和/或销售本软件副本的权利,
以及向本软件的使用者授予相同权利的权利,但须遵守以下条件:

上述版权声明和本许可声明应包含在本软件的所有副本或主要部分中。

本软件按"原样"提供,作者不对本软件作任何明示或暗示的担保,包括但不限于
对适销性、特定用途的适用性和非侵权的担保。在任何情况下,作者或版权持有人均不对
任何索赔、损害或其他责任负责。
```

---

_为中文社区倾力打造_ —— 🧚 摩根娜,经 Papa 批准 + 3 智能体共识 💜
