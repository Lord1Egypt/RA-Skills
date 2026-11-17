# Infoseek ↔ QCM 跨 skill 协同契约（v1.0.1 · A3）

> 版本：v1.0.1 ｜ 状态：✅ 已提供 ｜ 对齐全：`scripts/mcp_tools_qcm.py`（Infoseek 侧）/ `QCM/scripts/infoseek_bridge.py` + `tools_pack.py::qcm_attribution`（QCM 侧）

## 1. 双向闭环架构

```
Infoseek ──qcm_query──▶ QCM（反向调用 · 查询路由）
   ▲                        │
   │      qcm_attribution   ▼
   └────────◀───（5 维触发 ≥2 时调研）───┘
```

| 方向 | 工具 | 调用方 → 被调方 | 用途 |
|---|---|---|---|
| Infoseek → QCM | `qcm_query`（Infoseek TOOLS #16） | Infoseek MCP → QCM `mcp_server.py`（stdio） | 用户问题 → QCM 4 形态输出（quick_response / full_analysis / …） |
| QCM → Infoseek | `qcm_attribution`（QCM Tool 7） | QCM → Infoseek `research_v3`（stdio） | 5 维失败触发 → Infoseek 深度调研（L0 优先） |

## 2. qcm_query 工具契约（Infoseek 侧）

- **入参**：`query`（必填，string）、`form`（可选，string）
- **出参**：`status` = `ok` / `degraded` / `failed`
  - `ok` → `qcm_result.{intent, form, confidence, degradation_path, anchors[:5], version}`
  - `degraded` → `reason` + `degradation`（`qcm_not_installed` / 调用异常）
  - `failed` → `degradation=invalid_input`（空 query 拒绝）
- **QCM 探测**：`QCM_ROOT` env 优先 → `~/.workbuddy/skills/QCM` 兜底
- **调用方式**：stdio 子进程（`sys.executable` 启动 QCM `scripts/mcp_server.py`，30s 超时）

## 3. qcm_attribution 触发语义（QCM 侧 · §8 协议）

**触发条件：5 维触发信号中"失败维 ≥ 2"**（`failed = [d for d in dims if d and d != "ok"]`）

- `""` 空串**不计失败**（仅 `ok` 与显式失败描述计入判定）
- `["", "ok", "", "", ""]` → failed=0 → **not_triggered**（仅 L0 探测，不触发调研）
- `["半导体行业", "ok", "工具缺失", "标准缺失", "ok"]` → failed=2 → **触发调研**（L0_infoseek）

**语义要点**：`qcm_query` 默认传 5 维占位（0 失败）→ **查询优先语义**（路由 4 形态，不强制深度调研）；深度调研由 QCM 侧在真实失败场景（≥2 维）触发。`infoseek_status`：`available`（调研成功）/ `not_triggered`（未达阈值）/ `not_installed` / `partial`（调用异常降级 L1/L3）。

**降级链**：L0_infoseek → L1_local（corpus 检索）→ L3_protocol（协议输出）。

## 4. 测试与维护要点

- **Infoseek 侧**：`tests/test_qcm_bridge_v101.py`（10 用例：注册/空查询/未装降级/4 形态/失败降级/env 探测/schema/分发/async 不生成/真实端到端）→ 已纳入 `run_tests.py` 标准回归
- **QCM 侧**：`tests/basic/qcm_mcp_v044_test.py`（8 用例双向集成）
- **维护**：`mcp_tools_qcm.py` 属 G11 mcp_tools 家族 → 新增模块必须通过 `scripts/mcp_tools_check.py` 符号自检（防 `import sys/os` 缺失类回归）
- **变更同步**：工具面变化须同步 `tests/test_tools_surface.py` / `test_mcp_snapshot_v101.py` 的 CANONICAL 断言与 `dist/dify`、`dist/coze` 生态产物
