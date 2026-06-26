# 使用说明

## 这不是“完整克隆包”

这个 skill 的定位不是把某个 live assistant 原样封存，而是提供 **最大可迁移、可复现、可审查的能力层**。

它分为三层：

1. **Assistant operating layer**  
   公开可迁移的工作风格与质量标准，例如 `SOUL.md`、通用 `USER.md` / `TOOLS.md` 模板、heartbeat 模板。
2. **热层 continuity**  
   给 OpenClaw 增加长任务不断线所需的 `memory / plans / status / handoff` 工作流。
3. **运行时补丁层**  
   给 OpenClaw 增加“前台同一对话、后台自动续接”的 thread continuity / successor rollover / hidden handoff / **silent continuity preparation** 能力。

---

## 何时只用 workspace 层

适用于：
- 你想让另一个 assistant 更接近这套工作方式
- 你想复制质量标准、任务纪律、heartbeat 入口
- 你暂时不准备改 OpenClaw 源码

这时优先使用：
- `../scripts/bootstrap_workspace.py`
- `../assets/workspace/SOUL.md`
- `../assets/workspace/HEARTBEAT.md`
- `../assets/workspace/AGENTS.md`
- `../assets/workspace/SESSION_CONTINUITY.md`
- `../assets/workspace/USER.template.md`
- `../assets/workspace/TOOLS.template.md`

---

## 何时只用 continuity 模板层

适用于：
- 你只想先把长任务 continuity 工作流跑起来
- 你不准备改 OpenClaw 源码
- 你只需要可恢复的 handoff / status 闭环

这时重点使用：
- `../assets/workspace/SESSION_CONTINUITY.md`
- `../assets/workspace/plans/TEMPLATE.md`
- `../assets/workspace/status/TEMPLATE.md`
- `../assets/workspace/handoff/TEMPLATE.md`
- `../assets/workspace/memory/README.md`
- `../assets/workspace/temp/README.md`

---

## 何时启用完整 continuity 层

适用于：
- 你明确要“visible thread 不变”
- 你明确要后台 successor rollover
- 你明确要 hidden handoff 不泄露到用户可见历史
- 你希望高 context 时采用静默准备，而不是给用户弹 continuity/context 提示
- 你持有匹配的 OpenClaw 源码树并能自行构建与部署

这时必须再使用：
- `../assets/patch/thread-continuity.patch`
- `../scripts/apply_runtime_patch.py`
- `./files-to-replace.md`
- `./deploy-notes.md`
- `./verify.md`
- `./rollback.md`

---

## 完整 continuity 的当前运行语义

当前补丁面向的 live 行为是：
- **80%+**：静默 durability refresh
- **85%+**：进入 `compact_prepare` / successor preparation
- **88%+**：如果预测下一轮会冲到 90%+，则提前准备切换
- **90%+**：进入 `rollover_required`
- 普通聊天页不显示 continuity/context 两类提示
- 回答质量不靠“先缩短、先敷衍、先收敛”来换上下文余量

---

## 重要边界

- 这个 skill **不能** 单独复制 base model、本机工具权限、插件安装、provider 鉴权、live channel 配置、真实用户记忆、隐藏系统提示词。
- workspace 层可以复制“公开可迁移的工作风格与流程纪律”，但**不能**单独复制整个 live assistant。
- 模板层 **不会** 单独创造 successor session、hidden handoff 或 silent same-thread rollover。
- 完整 continuity 体验依赖运行时补丁层 + `pnpm build` + `pnpm ui:build`。
- 这个 skill 交付的是**最大可迁移的能力层**，不是某台机器的完整现场快照。
