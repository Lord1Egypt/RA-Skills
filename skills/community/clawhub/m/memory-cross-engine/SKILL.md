---
name: memory-cross-engine
version: 1.0.0
description: |
  跨引擎记忆贯通总线：让规划/记忆/验证等四引擎共享同一份结构化记忆，实现跨引擎检索
  与关联，使超级智能体一次长程任务内越跑越连贯。这是「四引擎端到端自主闭环」的关键拼图。
agent_created: true
visibility: public
---

# memory-cross-engine（跨引擎记忆贯通）

> 由 meta-evolver 在「超级智能体实战收口」域构建。解决四引擎（规划↔记忆↔验证↔反思）
> 各自为政、上下文无法贯通的问题——让一次任务内的决策、记忆、校验共享同一份结构化记忆。

## 何时使用
- 组装端到端超级智能体闭环，需要 planner / memory / verify 引擎共享上下文。
- 长程任务中希望「规划产出的目标」能被「验证引擎」直接引用、「记忆引擎」沉淀的偏好能反哺「规划」。
- 调试超级智能体时发现各引擎重复获取、彼此不知道对方已产出的事实。

## 工作流
1. **各引擎写入**：规划引擎写 goal/step、记忆引擎写 fact/preference、验证引擎写 check/criterion，均带 engine 标签。
2. **跨引擎关联**：用 `link` 把相关条目连成图（如 目标↔偏好↔校验标准）。
3. **跨引擎检索**：用 `retrieve` 按查询跨引擎拉取最相关条目（单字+二元组 relevance，规避 CJK 分词缺失）。
4. **按引擎过滤**：`retrieve --engines planner` 只取某引擎视角，支持局部重规划。
5. **全局视图**：`view` 查看各引擎条目数与关联密度，监控贯通度。

## 脚本
`scripts/memory_bus.py`（纯标准库）：
- `MemoryBus` 类：`write(engine, type, payload, links)` / `link(a, b)` / `retrieve(query, topk, engines)` / `cross_engine_view()`
- CLI：`--selftest` 自检；`write` / `link` / `retrieve` / `view` 子命令。
- 记忆落盘 `memory_bus.jsonl`，可持久化跨会话。

## 自验证
```bash
python scripts/memory_bus.py --selftest
```
断言：三引擎条目贯通检索、关联数正确、验证引擎可检索、引擎过滤生效。

## 与四引擎闭环的关系
- 上游：`long-horizon-planner` 产出目标 → 写入 bus(engine=planner)。
- 中游：`continual-memory-engine` 沉淀偏好 → 写入 bus(engine=memory)，并被规划检索引用。
- 下游：`reason-verify` / `reflection-replanner` 产出校验标准与修订 → 写入 bus(engine=verify)，反哺下一轮规划。
- 由此构成「规划→记忆→验证→再规划」真正共享上下文的自主闭环。

## 已知限制
- 当前为轻量 JSONL 存储，未做向量化；大规模记忆建议切换 embedding 检索。
- relevance 用字符级重叠，长文档需先摘要再写入。

---

## 自进化学习系统（越用越好用、越用越高效）

本技能内置通用学习模块 `scripts/learner.py`。每次使用后自动复盘、积累经验，逐步提升输出质量与执行效率，无需人工维护。

### 记忆文件
`learned_patterns.json`（位于本技能目录）记录：操作总数、各能力使用频次、错误模式、用户偏好、改进建议。

### 使用后请调用（Bash）

```bash
# 记录一次成功使用（--capability 填本次主要能力名，如「简历优化」「比价」）
python scripts/learner.py record <本技能目录> --capability 简历优化
# 记录一次失败/异常
python scripts/learner.py record <本技能目录> --capability 简历优化 --fail --error 格式识别失败 --note "用户上传了非标准文件"
# 记录用户偏好（下次直接使用）
python scripts/learner.py prefer <本技能目录> --key 输出语言 --val 中文
# 查看累计洞察（高频能力 / 反复错误）
python scripts/learner.py insight <本技能目录>
# 自动复盘（错误≥3次 或 操作≥10次 时给出改进建议）
python scripts/learner.py reflect <本技能目录>
```

### 迭代规则
- **错误累计 ≥3 次** → 主动增加预检/兜底步骤，并将经验回写本 SKILL.md。
- **操作数 ≥10 次** → 分析高频能力优先打磨示例与质量，低频能力评估精简或合并。
- **重要用户偏好** → 写入 `learned_patterns.json`，下次调用直接采用，减少重复询问。

> 越用越懂你：第一次用是通用能力，第十次用已沉淀为你专属的最佳实践。