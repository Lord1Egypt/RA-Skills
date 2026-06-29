# 钩子系统

## 流程门禁系统

门禁状态查看：`python novel_pipeline_gate.py status <state_path>`

| 钩子 | 触发时机 | 类型 | 行为 | 脚本 |
|------|---------|------|------|------|
| 大纲确认 | 阶段1完成时 | 阻断式 | 未确认则禁止进入阶段2 | — |
| **大纲因果链验证** | 用户确认大纲前 | **阻断式** | novel_causality_check.py outline — 验证每章概述因果递进 | `scripts/novel_causality_check.py` |
| 子结构先行规划 | 每章写作前 | **代码级硬约束** | novel_workflow_engine.py plan-chapter 批量注册子结构 | `scripts/novel_workflow_engine.py` |
| **子结构因果链验证** | plan-chapter 后 | **阻断式** | novel_causality_check.py sub-structure — 验证子结构因果递进 | `scripts/novel_causality_check.py` |
| 子结构存在性验证 | 每段写作前 | **代码级硬约束** | novel_context_loader.py 读 sub_structures，未注册则报错退出 | `scripts/novel_context_loader.py` |
| **串行阻断** | **每段写作前（context_loader）** | **阻断式** | 检测上一子结构 state 是否为 completed，pending 则 HOOK-BLOCK 并输出 write-sub 修复命令 | `scripts/novel_context_loader.py` |
| 字数约束注入 | 每段写作前（context_loader） | 信息式（硬性提示） | 根据 meta.length 输出篇幅对应的字数范围 + 校验上浮值，禁止 LLM 自行配置 | `scripts/novel_context_loader.py` |
| 写作前加载上下文 | 写作前 | 阻断式+阶段约束 | novel_context_loader.py 输出命题指令框（含字数约束/情绪/人格/文风） | `scripts/novel_context_loader.py` |
| 写后即存 | 每段写作完成后 | 阻断式+原子写入 | novel_atomic_writer.py 格式校验 + fsync + 编号标记 + 字数校验（子结构目标） | `scripts/novel_atomic_writer.py` |
| **更新/扩写提醒** | **已 completed 的子结构再次写入** | **软性（不阻断）** | write-sub 检测子结构状态为 completed，输出提醒要求更新后运行 finalize-chapter | `scripts/novel_workflow_engine.py` |
| 署名检测 | 每段写入时 | **代码级硬阻断** | atomic_writer 检测"由...撰写"等8种署名模式；signature=off 时阻断 | `scripts/novel_atomic_writer.py` |
| 更新进度 | 每个子结构完成后 | 阻断式 | novel_state_manager.py update-sub | `scripts/novel_state_manager.py` |
| 角色登记 | 新角色出场时 | 阻断式 | novel_state_manager.py add-char | `scripts/novel_state_manager.py` |
| 时间线记录 | 每章完成后 | 阻断式 | novel_timeline.py add | `scripts/novel_timeline.py` |
| 章内连通性检查 | finalize-chapter 时 | **软性（不阻断）** | novel_continuity.py check — 子结构间时间/角色断链检测 | `scripts/novel_continuity.py` |
| 跨章承诺链检查 | finalize-chapter 时 | **软性（不阻断）** | novel_continuity.py cross-chapter — 关键词续接检测 | `scripts/novel_continuity.py` |
| 风格校验 | finalize-chapter 时 | **HARD（阻断）** | novel_style_check.py — 禁用词/末行编号/超200行阻断 | `scripts/novel_style_check.py` |
| 逻辑检查 | finalize-chapter 时 | **HARD（阻断）** | novel_logic_check.py — 人物/时间线/概述匹配度，命中<30%阻断 | `scripts/novel_logic_check.py` |
| **语义检查(BERT)** | **finalize-chapter 时（第5步）** | **HARD（可选，有模型时）** | novel_semantic_check.py — overview-vs-content 语义对齐<0.4 阻断；子结构间语义跳跃<0.4 阻断；情绪偏离/同义冗余/跨章主题延续 SOFT 提示 | `scripts/novel_semantic_check.py` |
| **推理审核(DeepSeek-R1)** | **finalize-chapter 时（第6步）** | **HARD+SOFT（可选，有模型时，CPU 可跑）** | novel_reasoning_check.py — 5 项推理审核（因果合理性/人物行为一致/情绪弧自然度/对话匹配度/论证可靠性），按结果输出 HARD 或 SOFT | `scripts/novel_reasoning_check.py` |
| **别名声明拦截/自动补** | **write-sub 写入时** | **代码级自动补（旧版为阻断）** | novel_atomic_writer.py — 检测到正文末尾缺少【别名】声明行时系统自动补 `【别名】无`；存在时剥离并调用 register-alias 注册到 characters[].aliases | `scripts/novel_atomic_writer.py` + `scripts/novel_state_manager.py` |
| **一键完结章节（阻断循环）** | 子结构全部完成后 | **编排式+HARD 阻断** | finalize-chapter：聚合上述检查→有 HARD 问题写入`_fixes.json`并阻断，不标记门禁；全部通过才 pass `chapter_finalized:L##` | `scripts/novel_workflow_engine.py` |
| 大纲忠实度报告 | 全文完成后 | 自动式+阶段门禁 | novel_fidelity.py generate-report（需≥stage3_ready）→ pass fidelity 门禁 | `scripts/novel_fidelity.py` |
| 结尾收束验证 | 全文完成后 | **阻断式+门禁** | novel_fidelity.py verify-ending — 封闭/开放/悬停类型专项检查 | `scripts/novel_fidelity.py` |

## 门禁点列表（有序、不可逆）

| 门禁 | 在读什么 | 由谁 pass | 被谁 require | 阻断后果 |
|------|---------|-----------|-------------|---------|
| `outline_causality` | 章概述因果链 | novel_causality_check.py outline（自动） | set-phase → writing | LLM 无法开始写作 |
| `sub_causality` | 子结构因果链 | novel_causality_check.py sub-structure（自动） | set-phase → writing | LLM 无法开始写作 |
| `chapter_finalized:L##` | 章完结检查 | finalize-chapter（HARD 全过时） | — | 不阻断 phase，只标记完成 |
| `fidelity` | 大纲忠实度 | novel_fidelity.py generate-report | set-phase → stage3_ready | LLM 无法推进到完结阶段 |
| `ending_verify` | 结尾收束验证 | novel_fidelity.py verify-ending | set-phase → stage3_ready | LLM 无法推进到完结阶段 |

## 查看门禁状态

```bash
python novel_pipeline_gate.py status <state_path>
```

输出示例：
```
[门禁状态] 当前阶段: writing
  outline_causality    ⬜ PENDING
  sub_causality:L01    ⬜ PENDING
  chapter_finalized:L01 ⬜ PENDING
  fidelity             ⬜ PENDING
  ending_verify        ⬜ PENDING
```
