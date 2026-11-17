---
name: memory-bench
display_name: 智能体长期记忆评测台
version: 1.0.1
category: research
platforms: ["web", "desktop"]
author: 注册老炮
license: MIT
description: AI 说"我记得"，你敢信吗？测一下就知道。长期记忆评测台 memory-bench——本地一键评测智能体/大模型长期记忆：12 类题型（时序/实体/否定/反事实/跨会话整合），EM/F1 标准评分，零配置开箱即跑；可接真实 LLM 严评（SiliconFlow/DeepSeek），密钥 env 注入不落盘。结果可复现、可对比、可入发布证据。自带安全稳定性 10 维实测全 5.0。适合 Agent 开发者、AI 产品经理、记忆方案选型。"记忆好不好，测了才知道。" #AI评测 #长期记忆 #LLM #benchmark
description_en: Benchmark your AI agent's long-term memory in one command. memory-bench runs 12 question types (temporal, entity, negation, counterfactual, cross-session) with standard EM/F1 scoring, zero-config local execution, and a pluggable real-LLM backend (SiliconFlow / DeepSeek) with env-injected keys that never touch disk. Reproducible, honest, evidence-ready. Ships with a 10-dimension security & stability self-test scoring 5.0/5. Built for agent developers, AI product managers and memory-solution selection. "Is your AI memory real? Test it."
tags: [AI, 评测, 长期记忆, LLM, benchmark, 记忆评测, 评测台, agent]
---

# 智能体长期记忆评测台（memory-bench）

> **One-command long-term memory benchmark for AI agents & LLMs.** Local, zero-config, standard EM/F1 scoring, pluggable real-LLM backend, honest & reproducible.

AI 说"我记得"，你敢信吗？**测一下就知道**。这是为「智能体 / 大模型的长期记忆能力」设计的本地评测台：12 类题型覆盖记忆的常见坑，标准 EM/F1 评分，一条命令出结果，可复现、可对比、可当发布证据。

## 何时用

- **Agent 开发**：上线前给记忆模块打分，量化"记得住多少、会不会串、能不能跨会话整合"。
- **方案选型**：对比不同记忆方案（RAG / 记忆库 / 长上下文）在同一批题目上的表现。
- **模型严评**：接真实 LLM（SiliconFlow / DeepSeek 等）跑一轮，看大模型自己的记忆表现。
- **发布自检**：把评测结果作为"能力证据"附进发布材料（诚实标注口径）。

## 依赖与运行环境

- **零第三方依赖**：仅用 Python 标准库（`re` / `json` / `urllib` / `os` / `time`），无需 `pip install`。
- **Python 3.8+** 即可运行；Windows / macOS / Linux 跨平台。
- 真模型严评需自备 API 密钥（env 注入），不依赖任何厂商 SDK。

## 快速上手（零配置，3 步）

```bash
# 1. 跑内部确定性评测（不联网、可复现、默认后端）
python tools/memory_bench.py

# 2. 看安全稳定性实测（10 维，本地闭环）
python tools/security_test.py

# 3.（可选）接真实 LLM 严评——密钥只走环境变量，不打印、不落盘
MODEL_BACKEND=api REAL_API_KEY=你的密钥 REAL_API_BASE=https://api.siliconflow.cn/v1 REAL_MODEL=deepseek-ai/DeepSeek-V3 \
  python tools/memory_bench.py
```

## 12 道评测题 · 覆盖 10+ 记忆能力维度

内置「星轨智能手表发布会」多会话记忆场景（4 个会话 + 上月历史），每类题型测一类记忆能力：

| 题型 | 考查点 | 示例问题 |
|---|---|---|
| 时序 | 记住时间点 | 发布会定在周几的几点？ |
| 实体 | 人物/属性绑定 | 设计负责人是谁，偏好什么配色？ |
| 事件 | 事实因果 | 周四的评审会为什么取消？ |
| 否定 | 记得"没做"的事 | 林涛最终明确没做哪件事？ |
| 数值 | 数字变化追踪 | 媒体邀请从几家扩到几家？ |
| 数值推理 | 多值运算 | 初始 50 万追加 20 万海外，最终锁多少？ |
| 时序推理 | 日历推算 | 设计稿周三交付、审核 2 天，能否赶周五定稿？ |
| 实体更新 | 追踪人事变动 | 演讲稿负责人从谁换成谁？ |
| 指代 | 代词消解 | "他"在"他说太技术化"里指谁？ |
| 反事实 | 假设撤销 | 若海外投放没追加 20 万，最终预算多少？ |
| 跨会话整合 ×2 | 新旧信息融合 | 配色相对上月复盘做了什么调整？ |

## 评分标准（标准 EM/F1，可比对）

- **EM（精确匹配）**：答案归一化后与标准答案完全一致 = 1，否则 0。
- **F1（字符级）**：预测与标准答案的字符重叠度（精确率 × 召回率调和平均），0~1。
- 判定：`EM=1 或 F1 ≥ 0.6` 记 PASS；汇总输出 `通过率 / Macro-EM / Macro-F1`。

## 完整用法与输出示例

```bash
$ python tools/memory_bench.py
================================================================
长期记忆评测台 v2 · EM/F1 · backend=internal
================================================================
[PASS] Q1 <时序> EM=1 F1=1.00 (0.0ms)
[PASS] Q2 <实体> EM=1 F1=1.00 (0.0ms)
[PASS] Q3 <事件> EM=1 F1=1.00 (0.0ms)
[PASS] Q4 <否定> EM=1 F1=1.00 (0.0ms)
...
[PASS] Q12 <反事实> EM=1 F1=1.00 (0.1ms)
----------------------------------------------------------------
通过: 12/12 (100%) ｜ Macro-EM=1.00 ｜ Macro-F1=1.00
诚实标注: 非官方数据集(方法论复现)；评分用标准 EM/F1；真模型接口预留未启用
================================================================
```

## 真模型接口（MODEL_BACKEND=api）

- 默认 `internal`：确定性解析后端（复现 Agent 抽取路径），不联网、完全可复现，作为对照基线。
- 设 `MODEL_BACKEND=api`：调用真实 LLM（OpenAI 兼容协议，SiliconFlow / DeepSeek 均可）。
- **密钥安全**：`REAL_API_KEY` 只从环境变量读取，代码不打印、不落盘；未配置密钥时优雅降级返回"未答出"，不发起网络请求。
- **密钥别名**：除 `REAL_API_KEY` 外，也认 `SILICONFLOW_API_KEY` / `DEEPSEEK_API_KEY`（按你用的平台二选一即可），行为一致。

## 自定义数据集

想测自己的记忆场景？改 `memory_bench.py` 里的三块即可：

- `TRANSCRIPT`：当前会话文本（多会话用 `[会话N·周X] 说话人：内容` 分段）
- `HISTORY_BLOCK`：历史会话块（测跨会话整合）
- `QUESTIONS`：`(编号, 题型, 问题, 标准答案)` 四元组列表

改完直接重跑，评分与输出格式不变。

## 安全稳定性实测（10 维，本地闭环）

随包自带 `security_test.py`，对评测台本身做 10 维安全稳定性实测（零真实凭据、可重跑），结果写入 `security_results.json`：

| 维度 | 实测 | 行业基线(参考) | 企业级(参考) |
|---|---|---|---|
| 评测可复现性 | 5.0 | 4.0 | 5.0 |
| 密钥零落盘 | 5.0 | 3.0 | 4.5 |
| 评分标准性 | 5.0 | 3.5 | 4.5 |
| 题型覆盖完整性 | 5.0 | 4.0 | 4.5 |
| 边界容错 | 5.0 | 3.5 | 4.0 |
| 数值推理 | 5.0 | 3.5 | 4.5 |
| 时序推理 | 5.0 | 3.5 | 4.5 |
| 否定与指代理解 | 5.0 | 3.5 | 4.5 |
| 跨会话整合 | 5.0 | 3.5 | 4.5 |
| 长上下文稳定性 | 5.0 | 4.0 | 4.5 |
| **综合** | **5.00 / 5** | — | — |

> 诚实声明：以上为本地闭环自测，非第三方权威机构认证；基线为行业常见水平估计，仅用于对比展示。

## 能力边界（诚实）

- **非官方数据集**：题型设计对标 LoCoMo / LongMemEval 方法论，但数据为自建场景，非其授权数据集；评测结论用于横向对比与能力画像，不宣称与官方基准等值。
- **internal 后端是解析器**：对内置场景精确匹配（可复现、可解释）；对未覆盖的新题型需自行扩展 `internal_answer` 或改走真模型。
- **真模型严评会消耗 API 额度**：单轮 12 题，用量极小；密钥自备。
- 禁用绝对词：对外表述用"我们主张 / 提出"，不宣称"最 / 全球首创 / 第一"。

## FAQ

**Q1：跑内部评测需要联网吗？**
不需要。`internal` 后端完全本地，不联网、不收集数据、不上传任何内容。

**Q2：真模型密钥安全吗？**
安全。`REAL_API_KEY` 只从环境变量读取，代码无任何打印/写盘；未配置时优雅降级，不发起网络请求。

**Q3：能测我自己的记忆场景吗？**
能。改 `TRANSCRIPT` / `HISTORY_BLOCK` / `QUESTIONS` 三块即可，评分与输出格式不变。

**Q4：评测结果能用于发布材料吗？**
能，但请保留诚实口径：标注"非官方数据集（方法论复现）+ 标准 EM/F1"。

**Q5：internal 和 api 后端结果为什么不一样？**
internal 是确定性解析（对内置场景精确），api 是真实 LLM 自由生成（可能长句、可能过度弃权）。两者对比恰好能暴露"解析器假象 vs 模型真实表现"。

**Q6：12 题太少，怎么扩？**
`QUESTIONS` 是四元组列表，直接追加；多会话文本按 `[会话N]` 分段即可。

## 功能状态（已实现 / 路线图）

**已实现**：12 题型评测、EM/F1 标准评分、internal 确定性后端、真模型接口（env 注入密钥）、自定义数据集、安全稳定性 10 维实测、雷达图生成。

**路线图中（未实现，不夸大）**：多语言题库、Web UI 可视化、官方数据集接入（需授权）。

## 文件导航

```
SKILL.md                # 本说明
LICENSE.md              # MIT 许可
ATTESTATION.md          # 权属证明（著作权/知识版权/免责/时间戳/指纹）
manifest.json           # 逐文件哈希 + 包指纹
安全审计报告.md          # 安全审计（结论 P2）
tools/memory_bench.py   # 核心评测台（12 题型 + EM/F1 + 真模型接口）
tools/security_test.py  # 安全稳定性实测（10 维 → security_results.json）
tools/gen_security_radar.py  # 雷达图生成（SVG，支持 --out 指定输出路径）
tools/security_results.json  # 实测结果（10 维 5.0）
```

## 版权与许可

© 2026 注册老炮. 保留所有权利。

本作品（含软件代码与文档）的著作权归 注册老炮 所有，以 MIT License 授权使用（见 `LICENSE.md`）。

**知识版权声明**：本作品所汇集的方法论、题型设计、对比分析与合成内容（"知识内容"），其编排与原创表达归 注册老炮 所有。未经书面许可，不得复制、转载、摘编、转售，或用于训练任何模型 / 商业系统。（软件代码依随附 LICENSE 的许可条款使用；本声明不限制 LICENSE 已授予的权利。）

**免责声明**：本作品按「现状」提供，不提供任何明示或暗示的担保，包括但不限于适销性、特定用途适用性及非侵权担保。使用风险由使用者自行承担，因使用本作品所致任何直接或间接损失，作者不承担责任。
