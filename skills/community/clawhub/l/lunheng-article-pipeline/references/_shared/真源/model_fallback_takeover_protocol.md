> 版本：v2.18.1（发布版，与 SKILL.md version: 同步）

> 🌐 **语言政策**：产出语言由 Phase 0「目标语言」字段**显式选择**（中文 / English / 中英混 / 其他，**不设默认**），全流程以该字段为准；中文特化按**目标语言客观适用**——含中文时 **G14 中文 AI 痕迹闸必跑**（v2.12.40 起不再是可选项），纯外语时记 `n/a`（客观不适用，非「关闭」）；GB/T 7714-2015 引用规范为可选能力。二者均不构成使用者语种限制。

# 模型 fallback 接管协议（model_fallback_takeover_protocol）

> **真源性质**：本文件是「论衡主控进程被 fallback 模型接管」场景的**唯一真源**。
> **作用域**：仅适用于 in-process 主控进程失联（custody disconnect）场景；常规降级（provider_silence_escalation）走 phase-order.yaml 顶层 `provider_silence_escalation`，不在本协议范围。

---

## 一、触发条件（必须三项同时命中）

1. **in-process 失联**：主控 session 在平台层仍可见，但 `session_status` 返回 `running` 而实际心跳已停止 ≥ 5 分钟（固定阈值 5 分钟，skill 自包含；运行时不读取任何宿主配置）。
2. **fallback 模型可调用**：当前会话可见模型面（`session_status` 只读元数据，非读取宿主配置）中存在至少 1 个可调用模型（Phase 0 已跑过 `top_tier_liveness_gate`，可直接复用结论）。
3. **未触发主人拍板**：同一项目未进入「主人已显式叫停」状态（`status.md` 不含 `pending_owner_halt`）。

三项任一不命中 ⇒ **禁触发接管**，按既有路径等待 / 降级 / 报错。

---

## 二、接管动作（顺序执行，不可跳步）

| 步骤 | 动作 | 工具 | 必填产物 |
|------|------|------|----------|
| 1 | 读 `run/<项目名>/status.md` 当前快照 | `read` | — |
| 2 | 写 `run/<项目名>/status.md` 「§8 模型接管声明」段 | `edit` | `## §8 模型接管声明` 段 |
| 3 | 列**接管时正在运行的 worker 节点**（从 status 节点表读）| `read` | 接管清单 = `[node_id, run_id?, last_heartbeat?]` |
| 4 | 对**每个正在运行的 worker** 写接管记录：`run/<项目名>/audits/takeover-log-v{N}.md` | `write` | takeover-log-v{N}.md |
| 5 | 重读 phase-order.yaml，按 seq 顺序从失联点**继续向下游推进**；禁止**回放**已完成的节点 | `read` | 新一轮 status 节点表 |
| 6 | 在 `run/<项目名>/status.md` 头部加显眼提示：「⚠️ 本轮由 fallback 模型接管」 | `edit` | status.md 头部 banner |

**禁**：尝试唤醒原 session / 给原 session 发 session.send / 任何 sessions_history 反查；这些操作在失联场景下要么超时要么反馈错位，徒增延迟。

---

## 三、§8 接管声明字段规范（status.md 必填段）

每次触发本协议，**必须**在 `run/<项目名>/status.md` 写入（或更新）以下字段：

    ## §8 模型接管声明

    - **触发时间**（ISO 8601）：<YYYY-MM-DDTHH:MM:SS+08:00>
    - **原主控 session_key**：<原 sessions_history 可见到的 key；若已不可见记 `unknown`>
    - **fallback 模型**（provider/model）：<如 kkaiapi/gpt-5.6-terra>
    - **接管时 seq 序号**：<数字>
    - **接管时 node_id**：<如 t4_analysis>
    - **正在运行的 worker 数**：<数字>
    - **takeover-log 路径**：<相对路径，如 audits/takeover-log-v1.md>
    - **原主控恢复状态**：<recovered | not_recovered | unknown>
    - **主人是否已告知**：<yes | no | pending>

字段任一为空 ⇒ 记 `takeover_incomplete`，下游 T8 终检按 M-Exist 项判「路径或参数错误」档（不当作 P1 内容问题）。

---

## 四、与既有机制的分界

| 场景 | 真源 | 与本协议关系 |
|------|------|------------|
| 同一 provider 连续 ≥3 次静默 | phase-order.yaml `provider_silence_escalation` | **不触发**接管；走主人三选一 |
| 单次 provider 失败 | `glossary-core.md` §降级规则 | **不触发**接管；走换族重派 |
| 顶配档 2 次失败 | `phase-order.yaml` `top_tier_liveness_gate` | **不触发**接管；断路器暂停 |
| 主控心跳停止 ≥ 5 分钟 | **本协议** | ✅ 唯一接管路径 |
| 主人显式叫停 | `owner_timeout_policy` | **抢先于本协议**；不接管 |

---

## 五、版本与变更记录

- v2.15.7（2026-10-02 初版）：基于 ECS 实战反馈（fallback 模型启动后不知如何续跑）建立。
- 变更记录：字段命名 / 步骤顺序如需调整，须同步 `00-主控-扩展职责.md`「模型接管」段与 SKILL.md frontmatter `coordinator_fallback_protocol_ref` 字段（**单一真源 = 本文件**）。