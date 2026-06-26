# OpenClaw Evolution v3（Coordinator 升级蓝图）

这是一个基于源码分析与实战验证的升级蓝图，用来把 OpenClaw Agent 从“指令执行器”升级为“协调者（Coordinator）”模式：更强合成、更稳执行、更硬验证。

## 适用人群

- 维护自定义 Agent 策略的 OpenClaw 用户
- 希望复杂任务成功率更高的运维/开发者
- 需要可复用升级 SOP 的部署者

## 快速入口

- 🇬🇧 英文指南：[`EVOLUTION_GUIDE_EN.md`](./EVOLUTION_GUIDE_EN.md)
- 🇨🇳 中文指南：[`EVOLUTION_GUIDE_CN.md`](./EVOLUTION_GUIDE_CN.md)
- 🧬 基因锁定 SOP：[`SOP_GENE_LOCKING.md`](./SOP_GENE_LOCKING.md)
- 🛡 兼容性与安全护栏：[`COMPATIBILITY.md`](./COMPATIBILITY.md)

## 四大核心升级

1. **强制结果合成（Mandatory Synthesis）**
   - 把碎片研究结果合成为“可直接执行”的自包含计划。
2. **原子化任务调度（Atomic Scheduling）**
   - 只读并行、变更串行，避免竞态。
3. **动态上下文注入（Dynamic Context Injection）**
   - 变更前先拿真实系统快照，拒绝记忆漂移。
4. **证明级验证（Verification as Proof）**
   - 用测试/检查证明有效，而非只看文件“改到了”。

## 仓库结构

- `EVOLUTION_GUIDE_EN.md`：英文完整实践指南
- `EVOLUTION_GUIDE_CN.md`：中文完整实践指南
- `SOP_GENE_LOCKING.md`：写入 `IDENTITY.md` / `AGENTS.md` 的持久化模板
- `COMPATIBILITY.md`：版本适配、分阶段上线与回滚规范
- `src/`：用于分析与复现的源码参考快照

## 5 分钟落地路径

1. 先读 `COMPATIBILITY.md`，确认环境匹配。
2. 阅读你偏好的指南（`EN` 或 `CN`）。
3. 在独立分支应用 `SOP_GENE_LOCKING.md`。
4. 执行本地验证（测试/类型检查/冒烟）。
5. 稳定后再合并到主分支。

## 重要声明

本仓库是**升级蓝图**，不是官方“一键安装包”。
必须结合你的 OpenClaw 版本做适配，并始终准备回滚点。

## 推荐实施方式

- 高影响改动必须加 feature flag。
- 不要粗暴替换现有权限系统。
- 采用小步提交，每步都验证。

## 常见问题

### 别人只要照抄就能 100% 成功吗？
不能这么保证。大部分人可以按此路线升级，但仍需做兼容性检查和分阶段验证。

### 只看 `SOP_GENE_LOCKING.md` 就够吗？
它是核心模板，但要安全上线，还需要 `COMPATIBILITY.md` 的前置检查与回滚预案。

### 能不能固化成 skill？
可以。可将触发条件、实施步骤、验证与回滚规则封装成 AgentSkill，实现标准化执行。

## 致谢

基于 OpenClaw 源码实测分析与多轮编排实践总结。
