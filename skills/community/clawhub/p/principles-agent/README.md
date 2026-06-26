# principles-agent

基于第一性原理的迭代式 Agent 框架，OpenClaw 实现。

灵感来自 [miltonian/principles](https://github.com/miltonian/principles)。

**作者：** 🖤 小黑 & 小龙

## 核心能力

- **第一性原理需求分析** —— 剥离经验假设，回归最基础的事实和公理
- **原子级任务拆解** —— 将复杂目标拆解为不可再分、可验证的原子子任务
- **迭代式精炼** —— 自动检查并优化不满足条件的真理/子任务
- **依赖感知调度** —— 拓扑排序处理依赖，支持无依赖并行执行
- **分层质量验证** —— 每层都验证，不通过自动调试重试
- **全局整合验收** —— 最终交付前整体验证，保证结果质量

## 安装

```bash
# 已经作为 OpenClaw 技能安装
# 需要 Python 3.8+
# 无需额外依赖，直接使用
```

## 使用

```python
from principles_agent import PrinciplesOrchestrator

def llm_call(prompt):
    # 你的 LLM 调用
    return response

orch = PrinciplesOrchestrator(llm_call=llm_call)
result = orch.run("你的目标描述")
report = orch.generate_report(result)
print(report)
```

### CLI 使用

```bash
python ~/.openclaw/skills/principles-agent/cli.py "我要设计一个基于第一性原理的多Agent系统" -o report.md
```

## 工作流程

```
1. 接收需求 → 提取清晰目标
2. 第一性原理解构 → 识别基础事实/公理
3. 原子任务拆解 → 拆解为最小可执行子任务
4. 迭代精炼 → 检查最小性/可行性/对齐性，不满足则优化
5. 依赖排序 → 拓扑排序确定执行顺序，检测循环依赖
6. 执行验证 → 按序/并行执行子任务，每个都验证
7. 全局整合 → 合并所有子任务结果
8. 最终验收 → 验证满足原始目标，交付成果
```

## 架构

```
principles-agent/
├── SKILL.md
├── README.md  (本文件)
├── cli.py      # 命令行入口
└── src/
    ├── __init__.py
    ├── types.py            # 类型定义
    ├── orchestrator.py    # 总控 Orchestrator
    ├── truth_deriver.py   # 基础公理推导
    ├── task_breaker.py    # 原子任务拆解
    ├── refiner.py         # 迭代精炼决策
    ├── dependency_sorter.py # 拓扑排序
    ├── validator.py       # 验证器
    ├── executor.py        # 子任务执行器
    └── integrator.py      # 结果整合
```

## 许可证

MIT (继承自原始项目)
