# 鲁班.Skill（luban-skill）

工业级 AI Agent Skill 优化器。对 skill 进行 10 维度结构评分 + 效果验证，通过棘轮机制保留改进、回滚退步，输出可量化的优化日志。

- **10 维 Rubric**覆盖 frontmatter / 工作流 / 失败模式 / 检查点 / 具体性 / 资源 / 架构 / 实测 / 反例 / 门控
- **棘轮机制**：只保留改进，自动回滚退步，`results.tsv` 全量记录
- **独立评分**：效果维度用子 agent 独立打分，消除"自己改自己评"的偏差
- **人在回路**：每个 skill 优化完暂停，用户确认再继续

## 安装

将本目录放入 Agent 的 skills 加载路径即可。

## 使用方式

```
优化所有skills        → Phase 0-6 完整流程
优化 <skill名>        → 对指定 skill 执行 Phase 1-4
评估所有skills        → 只执行 Phase 1-2，不进入优化循环
看看 skill 优化历史   → 读取并展示 results.tsv
```

## 已知限制

1. **Quick/Full 模式选定后不会自动切换**：双轨反馈（Quick→Full、Full→Quick）依赖跨会话状态追踪，当前无法实现。运行时 agent 按前置网关选一次模式，执行到底。
2. **Full 模式依赖 git**：git 不可用时降级为 `.bak` 文件备份。多评委评分依赖 `dispatch_task` 可用。
3. **确定性维度（dim1/4/7/9）由 agent 按 Rubric 逐条自检**，非系统内置工具。评分一致性依赖 agent 对 rubric 的理解准确度。
4. **dim10 多角色审查仅在 Full 模式 + dispatch_task 可用时触发**，降级模式下默认 100 分。

## 目录结构

```
luban-skill/
├── SKILL.md                     # 主文件（本 skill 的定义和指令）
├── README.md
├── QUICKSTART.md
└── references/
    ├── SA-DM.md                 # 方法论骨架（静态参考）
    └── baseline-skill.md        # 消费者基线测试用 skill
```
