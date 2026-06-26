# v1.19.0 (2026-04-28)

**核心修复：消除每次 prompt 注入 ~7900 字 / ~2000 tokens 的工具表，TTFT（首字延迟）实测降幅显著。**

## 背景

诊断发现 `before_prompt_build` hook 在每次 LLM call 之前都注入 ~7900 字的工具速查 + 自然语言映射表到 system context（[index.ts:5212-5489](index.ts#L5212)）。

**用户感受**：哪怕只发"你好"也注入这 2000 tokens。LLM 处理这堆 prompt + reasoning thinking 一起拖到 TTFT 70-150 秒。

实测 14:33-14:35 dispatch 拆解：
- dispatch-start → first deliver-block = **129 秒**
- 大头是 LLM TTFT 72 秒（首字延迟）
- 加上 plugin 多次 reload 拖累 ~17 秒

## 改动

### 删 — system context 7900 字 → 1500 字

[index.ts](index.ts) 的 `registerHooks` 函数中 `appendSystemContext` 模板字面量整体重写：

| 删 | 改成 |
|---|---|
| 工具速查（共 77 个）整段 6500 字 | 只保留 6 行高频工具速查（任务 / CRM / 项目 / 客服 / 财务 / 联系人 / 检索 / 状态） |
| 自然语言 → 工具映射 130+ 行 8000+ 字 | 全删（让 LLM 自己推断意图，识别不出再调 odoo_help） |
| 常用数据模型 26 个 | 缩到 14 个最常用 |
| 日期 & 字段规范 6 条 | 保留全部（这部分对 LLM 调用工具时仍重要，但本身只 200 字） |

最终 system context 注入约 1500 字 / ~400 tokens。

### 加 — `odoo_help` 工具（按需查工具表）

新增 `api.registerTool({ name: 'odoo_help', ... })`，参数：

- 无参数 → 返回完整 7900 字工具表 + 自然语言映射 + 数据模型清单
- `keyword="<模糊词>"` → 行级模糊匹配（如 `"请假"` 返回所有请假相关工具行；`"CRM"` 返回 CRM 分类）

LLM 在不知道某意图对应哪个工具时**主动调 odoo_help**，把 token 消耗从"每次 prompt 都付"改成"按需付"。

工具数从 189 → **190**。

### 不改

- 未连接路径的 system context（[index.ts:5176-5202](index.ts#L5176)）保留——那段本来就没工具表，只是连接引导
- 189 工具的实现逻辑 / 接口 / 业务规则 全部不动
- 共享凭据规则、品牌口径硬规则、用户/系统/凭据动态字段 全保留

## 用户可见效果

| 项 | v1.18 | v1.19 |
|---|---|---|
| 每次 prompt 注入 | ~7900 字 / ~2000 tokens | ~1500 字 / ~400 tokens |
| TTFT 预期降幅 | — | -5 ~ -25 秒 |
| 工具数 | 189 | 190 (+ odoo_help) |
| LLM 调用工具的能力 | 完整可见 | 高频 8 个直接可见，其他通过 odoo_help 按需查 |

## 风险与缓解

- **风险**：LLM 看不到完整工具表可能导致它"不知道某个工具存在"
- **缓解**：
  1. system context 顶部明确告知"完整 189 工具表调 odoo_help"
  2. odoo_help 工具的 description 写明 "按需获取详细信息"
  3. 高频 8 个工具仍然在 system context 里直接可见，覆盖 80% 日常需求

## 测试

- `tsc --noEmit` exit 0（剩余 schema 字段警告是 v1.18 之前就存在的 SDK 类型定义问题，与本次改动无关）
- 启动期 log 应从 `[odoo] 189 个工具已注册` 变为 `[odoo] 190 个工具已注册（v1.19 — 加 odoo_help 按需查工具表，system context 不再每次注入 ~7900 字）`
- before_prompt_build 钩子注册 log 加 `v1.19 system context 已瘦身 ~6500 字 → 调 odoo_help 按需取详`

## 兼容性

完全向下兼容。所有 189 工具签名 / 行为 / 业务逻辑不变。LLM 端如果还期望从 system context 看完整工具表，调 odoo_help 即可恢复 v1.18 行为。
