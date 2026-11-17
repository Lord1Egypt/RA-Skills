# 跨 Agent / 多平台可移植性契约（Portability Contract）

> 适用场景：本 Skill 将提交联想 **天禧 AI Skill 比赛**。天禧平台尚未发布、用法格式未知，
> 因此「可在任意 Agent 主机上运行」是必须证明的硬指标。本文档定义第三方主机（含天禧）
> 接入本 Skill 的**最小契约**，以及平台方无需等待我们适配即可即插即用的路径。

---

## 1. 核心结论（一句话）

**office-token-booster 的内核（diagnose / report / qa）完全不依赖任何宿主平台。**
它与具体 Agent 主机的唯一耦合点，是一个名为 `HostCostProvider` 的极简契约：

```python
class HostCostProvider(Protocol):
    def fetch_recent(self, days: int) -> list[CostRecord]: ...
```

只要主机能产出 `CostRecord` 列表，内核一行都不用改。WorkBuddy 只是当前**默认实现之一**。
这由 `tests/test_portability_cross_agent.py::test_port_core_independent_of_host_cost` 强证明：
即便在运行时把 `host_cost` 模块彻底拦截（模拟「没有任何适配层的主机」），内核仍能独立跑通。

---

## 2. 主机的两种接入方式

### 方式 A：零代码（推荐给未知/未发布平台）

主机只需把每次会话的 token / 耗时以 **JSON 或 JSONL** 形式导出到一个文件，
本 Skill 自带的 `GenericJsonProvider` 即可读取，**无需我们为它写任何专属代码**。

导出文件形态（任一即可，字段名容忍）：

```json
[
  {
    "usage": { "prompt_tokens": 1000, "completion_tokens": 500, "total_tokens": 1500 },
    "model": "tianxi-gpt-x",
    "startedAt": "2026-08-15T10:00:00Z"
  },
  { "totalTokens": 2000, "model": "tianxi-gpt-x", "startedAt": "2026-08-16T10:00:00Z" }
]
```

调用（当前版本，编排层直接构造 provider）：

```python
from host_cost import GenericJsonProvider, draft_entries_from_host
# 主机导出的用法文件（JSON / JSONL，字段名容忍）
entries = draft_entries_from_host(GenericJsonProvider("<用法文件>.json"), days=7,
                                  baseline_ratio=3.0)
```

或通过 `ledger_agent.import_host_usage(ledger_path, days=7,
provider=GenericJsonProvider("<用法文件>.json"), apply=True)` 直接写回。

或通过 **CLI 零代码接入**（天禧/OpenClaw 只需把用法导出成文件）：

```bash
python scripts/ledger_agent.py <账本>.json \n    --import-host --provider generic --provider-arg <用法文件>.json \n    --days 7 --baseline-ratio 3 --apply
```

- `--provider generic`：使用宿主无关的 `GenericJsonProvider` 读取任意主机的用法 JSON/JSONL。
- `--provider-arg <路径>`：指向第三方导出的用法文件（缺省报错退出，提示补 `--provider-arg`）。
- `--provider workbuddy`（默认，可省略）：本机 WorkBuddy traces 读取器。
- 重复导入自动去重（有 session_id 用 session_id；第三方缺 session_id 按内容签名去重），不膨胀账本。
- 无需改 skill 内核：CLI 仅构造 provider 后交给既有的 `import_host_usage`。

识别的字段名（均容忍，解析不到即跳过该条，**绝不抛异常**）：

| 维度 | 支持的键（任一） |
|---|---|
| Token | `effective_tokens` / `effectiveTokens` / `total_tokens` / `totalTokens` / `skill_tokens` / `tokens` / `usage.total_tokens` / `usage.prompt_tokens + usage.completion_tokens` |
| 耗时(分钟) | `effective_minutes` / `skill_minutes` / `minutes` / `duration_min` / `duration`(毫秒折算) |
| 日期 | `date` / `day` / `startedAt` / `endedAt` / `timestamp` / `created_at` / `time` |
| 模型 | `model` / `modelInfo.models[0]` |
| 任务类型 | `type` / `task_type`（缺省归为「AI办公任务」） |

### 方式 B：写一个 Provider（主机有私有 API / 流式事件时）

主机方实现 `HostCostProvider` 契约，返回 `CostRecord` 列表，传给 `import_host_usage(..., provider=...)`。
完整示例见 `tests/test_portability_cross_agent.py::_TianxiLikeProvider`（仅一个方法）。

```python
from host_cost import CostRecord, HostCostProvider, draft_entries_from_host

class MyHostProvider:
    def fetch_recent(self, days=7) -> list[CostRecord]:
        # 调你的私有 API / 读你的私有格式，映射成 CostRecord
        return [CostRecord(date="2026-08-15", skill_tokens=2830000,
                           model="my-model", source="my-host")]

# 一键转成账本草稿（skill 取实测，baseline 用 --baseline-ratio 假设）
entries = draft_entries_from_host(MyHostProvider(), days=7, baseline_ratio=3.0)
```

---

## 3. CostRecord 字段说明（主机要填什么）

| 字段 | 必填 | 含义 |
|---|---|---|
| `date` | 是 | `YYYY-MM-DD`，会话日期 |
| `skill_tokens` | 是 | 该次任务的实测 token 消耗（内核只认这个） |
| `skill_minutes` | 否 | 实测耗时（分钟），缺省 0 |
| `model` | 否 | 模型名（仅展示用） |
| `task_type` | 否 | 任务归类；缺省归「AI办公任务」 |
| `session_id` | 否 | 会话标识（去重用） |
| `source` | 否 | 来源标识，默认 `"host"` |

> 注意：`baseline_tokens`（笨办法手搓成本）主机**无从获得**，默认 0；
> 可用 `--baseline-ratio`（主观假设，如 3.0=手搓约为 AI 的 3 倍）先看提效报告。
> 纯消耗视角（skill_tokens 合计）是实打实的，不依赖 baseline。

---

## 4. 降级保证（未知主机的底线行为）

- 主机未导出用法文件 / provider 返回 `[]` → `import_host_usage` 返回 `count=0` + 友好提示，**不崩、不写盘、不破坏已有账本**。
- 单条脏数据 / 字段缺失 → 容忍抽取器跳过该条，整体继续。
- 内核从不 import `host_cost` → 即使适配层完全缺失，Skill 仍按「用户自报成本」模式正常出报告。

---

## 5. 可移植性测试清单（CI 门禁）

| 测试 | 证明点 |
|---|---|
| `test_port_contract_minimal_provider_satisfies_protocol` | 最小 duck-typed provider 即满足契约 |
| `test_port_contract_all_real_providers_satisfy` | 现有 3 个 provider 均实现同一契约 |
| `test_port_cross_agent_closed_loop` | 非 WorkBuddy provider 完整跑通 import→diagnose→report |
| `test_port_schema_tolerance_openai_usage` | 识别 OpenAI/Claude 的 `usage.*` |
| `test_port_schema_tolerance_alternate_keys` | 多键兜底 + duration 折算 |
| `test_port_generic_json_provider` | 第三方导出 JSON 被 GenericJsonProvider 读 |
| `test_port_graceful_degradation_unknown_host` | 未知主机返回空、不崩 |
| `test_port_core_independent_of_host_cost` | host_cost 不可导入时 core 仍跑通 |

运行：

```bash
cd office-token-booster
python -m pytest tests/test_portability_cross_agent.py -v --alluredir=allure-results
```
