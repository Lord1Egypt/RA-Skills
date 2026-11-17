> 版本：v2.18.1（发布版，与 SKILL.md version: 同步）

> 🌐 **语言政策**：产出语言由 Phase 0「目标语言」字段**显式选择**（中文 / English / 中英混 / 其他，**不设默认**），全流程以该字段为准；中文特化按**目标语言客观适用**——含中文时 **G14 中文 AI 痕迹闸必跑**（v2.12.40 起不再是可选项），纯外语时记 `n/a`（客观不适用，非「关闭」）；GB/T 7714-2015 引用规范为可选能力。二者均不构成使用者语种限制。

# status 模板（精简版）

> **精简版**：只保留骨架，详细说明见 [`status-template.md`](status-template.md)

```markdown
# Status

> **位置**: `run/<项目名>/status.md`
> **使用**: 主控独占更新；子代理只读 + 写 `run/<项目名>/.tmp/<两位角色号>-<角色名>-heartbeat.md` 心跳

## 当前状态

- 🔄 In Progress / ✅ Done / ❌ Failed
- 角色: T1 / T2 / **T3** 案例检索/ T4 分析/ T5 写手/ T6 批判/ T7 审计/ T8 终检主控亲完成
- 启动时间: YYYY-MM-DD HH:MM
- 当前模型: deepseek-v4-pro
- **架构**: 多 Agent 九角色（固定）；worker 接管记录见内

## 人在环呈现留痕（四节点）

- `checkpoint_id=<唯一值>` / `checkpoint_presented=true|false` / `checkpoint_presented_at=<时间>`
- `checkpoint_status=<awaiting_owner|reminded|pending_owner|decided>` / `reminder_sent=<true|false>` / `pending_owner_at=<时间|n/a>`
- `owner_response_received=true|false` / `owner_response_at=<时间|n/a>` / `owner_decision_normalized=<合法枚举值|n/a>`

> 仅记录主控呈现与回填动作，不冒充主人已阅读；无应答只允许 `pending_owner`，不得自动接受。

## 执行韧化记录

- 启动心跳: ✅
- 中途 ACK: ✅ / N/A
- 超时硬卡（角色分级）: 未触发 / 已 kill

## 修订回环记录

- v1 → v2: [日期 + 修改内容]
- v2 → v3: [日期 + 修改内容]
- 归档中间态到 archive/
```

---

**精简版结束**

> 完整版见 [`status-template.md`](status-template.md)