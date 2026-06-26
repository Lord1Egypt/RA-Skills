# principles-agent - 基于第一性原理的迭代式任务拆解框架

**作者：** 🖤 小黑 & 小龙

## 描述

基于 [miltonian/principles](https://github.com/miltonian/principles) 的设计思想，在 OpenClaw 中实现的**第一性原理思维 + 迭代式开发**框架。

**架构职责分离：**
| 模块 | 职责 |
|------|------|
| **principles-agent** | 需求澄清 → 第一性原理推导 → 原子任务拆解 → 迭代精炼 → 依赖排序 → 结果整合 → 分层验证 |
| **OpenClaw 主 Agent** | 实际执行 LLM 调用 → 执行子任务 → 处理外部操作 → 权限管控 |

skill 不直接调用 API、不访问网络、不读取环境变量，所有 IO 由主 Agent 完成。

## 核心能力

1. **第一性原理需求分析** —— 剥离经验假设，回归最基础的事实和公理
2. **原子级任务拆解** —— 将复杂目标拆解为不可再分、可验证的原子子任务
3. **迭代式精炼** —— 自动检查并优化不满足条件的真理/子任务
4. **依赖感知调度** —— 拓扑排序处理依赖，识别可并行批次
5. **分层质量验证** —— 每层都验证，不通过反馈优化
6. **全局整合验收** —— 最终交付前整体验证，保证结果满足目标

## 触发条件

当用户需要：
- 从零设计一个复杂系统/项目
- 对复杂问题进行深度分析
- 构建多步骤多 Agent 协作系统
- 需要按照第一性原理思维解决问题时触发

## 用法

**直接在 OpenClaw 会话中使用：**
```
principles "你的目标或问题描述"
```

**可选输出到文件：**
```
principles "你的目标" --output report.md
```

**配置最大迭代次数：**
```
principles "你的目标" --max-iterations 5
```

## 权限边界

principles-agent 遵循最小权限原则：

- ✅ **LLM 调用**：由 OpenClaw 主 Agent 注入，skill 只接收结果
- ✅ **文件读取**：仅读取 skill 自身目录内的源代码
- ✅ **文件写入**：仅在用户通过 `--output` 指定时写入报告
- ❌ **网络访问**：skill 不发起任何网络请求
- ❌ **环境变量**：skill 不读取任何环境变量
- ❌ **系统访问**：不执行外部命令，不修改系统配置

## 工作流程

```
1. 接收需求 → 澄清目标，提取约束和成功标准
2. 第一性原理解构 → 推导基础事实/公理
3. 原子任务拆解 → 拆解为最小可验证子任务
4. 迭代精炼 → 检查最小性/可行性/对齐性，不满足则优化
5. 依赖排序 → 拓扑排序确定执行顺序，检测循环依赖
6. 分批执行 → 主 Agent 执行子任务，skill 验证每个结果
7. 全局整合 → 合并所有子任务结果生成完整输出
8. 最终验收 → 验证满足原始目标，交付成果
```

## 架构

```
principles-agent/
├── SKILL.md          # 本文件
├── package.json      # Skill 元数据和权限声明
├── cli.py            # OpenClaw CLI 入口
├── openclaw_entry.py # OpenClaw 技能入口点
└── src/
    ├── __init__.py
    ├── types_def.py           # 数据类型定义
    ├── orchestrator.py       # 总控编排
    ├── truth_deriver.py      # 基础事实推导
    ├── task_breaker.py       # 原子任务拆解
    ├── refiner.py            # 迭代精炼决策
    ├── dependency_sorter.py  # 依赖拓扑排序
    ├── validator.py          # 分层质量验证
    ├── executor.py           # 执行调度（调用主 Agent 执行）
    └── integrator.py         # 结果整合
```

## 参考资料

- 原始项目：https://github.com/miltonian/principles
