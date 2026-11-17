# Sealed Report Specification（技能层信封 · 对应 NOMOS 0.7.0）

Hub 的每次决策可输出为**密封报告**（sealed report）——防篡改、可验证、机器可读。
这是审计方消费的产物。

> **定位说明**：本文件定义**技能层的报告信封与验证流程**。引擎原生产物是
> `HubReport`（含基线记录、场景结果、认知发现、信息优先级、算法账本验证状态、
> 策略快照与报告哈希）；其每个审计事件带 `sealed_hash`，链根哈希可独立复核。
> 本信封是它在技能层的可交付封装。

## Report structure (JSON)

```json
{
  "report_id": "rep-<uuid>",
  "schema_version": 1,
  "engine": "NOMOS Decision Engine",
  "engine_version": "0.7.0",
  "generated_at": "2026-10-19T12:00:00Z",
  "lang": "zh",
  "decision": {
    "question": "approve vendor X?",
    "verdict": "reject",
    "confidence": "high",
    "chain": [
      {"op": "ORI",   "input_hash": "sha256:...", "output": "..."},
      {"op": "NS",    "input_hash": "sha256:...", "output": "..."},
      {"op": "IAP",   "input_hash": "sha256:...", "output": "..."},
      {"op": "LCH",   "input_hash": "sha256:...", "output": "..."},
      {"op": "TPG",   "input_hash": "sha256:...", "output": "..."},
      {"op": "BFC",   "input_hash": "sha256:...", "output": "..."},
      {"op": "CCS",   "input_hash": "sha256:...", "output": "..."},
      {"op": "GRF",   "input_hash": "sha256:...", "output": "..."},
      {"op": "META",  "input_hash": "sha256:...", "output": "..."},
      {"op": "STATE", "input_hash": "sha256:...", "output": "..."}
    ]
  },
  "evidence": {
    "scenarios": ["stress-case-01", "adversarial-02"],
    "sources": ["policy-v3.md", "vendor-contract.pdf"]
  }
}
```

`ORI` 仅在声明原点时注册，`GRF` 仅在声明灰度阶梯时注册。二者未声明时，链中不出现
对应条目——这是**条件注册**，不是缺失步骤，不得因此判报告不完整。

## Sealing mechanism

1. Hash each operator's output → `input_hash` chain（每一步引用前一步哈希，形成
   Merkle 式因果链）。
2. Canonicalize the full report（确定性 JSON 序列化）。
3. Seal：`seal = sha256(canonical_report + sealed_at + nonce)`。
4. 可选签名（v0.5 起）：对密封产物哈希做分离式 HMAC-SHA256，响应头
   `X-Nomos-Kms-Signature`；未配置 `SP_KMS_SECRET` / `SP_KMS_KEY_FILE` 时为透明 no-op。

## Verification (for auditors)

```bash
# 从已发布报告重算封条
python verify_seal.py report.json --expect <seal>
```

输出 `SEAL VALID` 或 `TAMPERED`，并指出不匹配的片段。

引擎原生复核路径：校验 `sealed_hash` 链（`decision/integrity.py`、
`audit/execution.py`），任何对 payload / event_type / timestamp / nonce 的改动都会
使哈希失配而被检出。

## Rules

- Every P0/P1 decision MUST produce a sealed report; P2 optional.
- `confidence` ∈ {low, medium, high}，由场景覆盖度推导，不凭主观。
- Audit trail is append-only；修正确立新报告并以 `supersedes` 链接旧 `report_id`。
- `BUDGET_EXHAUSTED` 不得写成「收敛」；`META` 的低分不得当作缺输入阻断推导。
- `lang` ∈ {zh, en}：同一因果链无需重跑引擎即可渲染为目标语言。
