---
name: lgd-change-gate
homepage: https://zhaoxinghua09-cell.github.io/lgd-hub/
description: >-
  Decide whether a change to a medical-device AI or ML function needs formal change control, and return a pass, hold or reject verdict with auditable reasons.

  Medical-device AI/ML change-control judgment per the LGD three laws (有籍 Recorded / 有证 Evidenced / 有门禁 Gated). Trigger when the user asks whether a device-software or algorithm change requires change control, asks for a risk verdict (pass/hold/reject), asks for change-level classification (minor/major/critical), or asks for an LGD-theory judgment with auditable reasons. Applies to regulated environments (FDA 510(k)/PMA, EU MDR, ISO 13485) and other AI/ML medical-device change evaluations.
metadata:
  display_name: LGD 变更门控判定
  display_description: 按 LGD 三律（有籍/有证/有门禁）对医疗器械 AI 变更输出确定性的 risk-hold-pass 裁决，含变更级别判定与可追溯理由。
description_en: "Decide whether a change to a medical-device AI or ML function needs formal change control, and return a pass, hold or reject verdict with auditable reasons. It covers algorithm updates, retraining, data and threshold changes, classifies severity as minor, major or critical, and maps to FDA, EU MDR and ISO 13485 expectations."
description_zh: "Medical-device AI/ML change-control judgment per the LGD three laws (有籍 Recorded / 有证 Evidenced / 有门禁 Gated). Trigger when the user asks whether a device-software or algorithm change requires change control, asks for a risk verdict (pass/hold/reject), asks for change-level classification (minor/major/critical), or asks for an LGD-theory judgment with auditable reasons. Applies to regulated environments (FDA 510(k)/PMA, EU MDR, ISO 13485) and other AI/ML medical-device change evaluations."
---

# LGD Change-Gate Judgment (lgd-change-gate)

## When to use (triggers)

- The user describes a change to a medical-device AI/ML function (algorithm update, data change, model retrain, threshold adjustment, deployment change) and asks whether change control is needed.
- The user asks for a change verdict: pass / hold / reject.
- The user asks for change-level classification: minor / major / critical.
- The user asks for an LGD-theory judgment (three laws: Recorded / Evidenced / Gated) with auditable reasons.

Do NOT trigger: ordinary software changes outside medical devices, non-AI document edits, or questions without a change substance.

## Core flow

Execute each step to evidence, never on impression.

### Step 1 — Record the change (有籍 Recorded)

Collect the change object's "registry" facts:

1. Change object: device/system/software component name and identifier (model, version, registration number).
2. Change content: what changed (input, model, weights, code, configuration, data, deployment).
3. Change initiator and time.
4. Whether a baseline record exists (premarket submission, DHF, existing change-request record).

If the baseline is missing or the object cannot be identified → **hold**, reason: 无籍不可判定 (unregistered cannot be judged).

### Step 2 — Verify evidence (有证 Evidenced)

Collect and verify evidence for the change claim:

1. Necessity evidence: why the change is needed (defect, clinical need, regulatory requirement).
2. Impact-analysis evidence: scope of impact on safety, effectiveness, and intended use.
3. Verification evidence: test plan, data, results; coverage of old-vs-new behavior comparison.
4. Evidence provenance and freshness: traceable, unexpired, authoritative.

If evidence is insufficient or unverifiable → **hold**, reason: 无证不裁决 (unevidenced no ruling).

### Step 3 — Pass the gate (有门禁 Gated)

Pass gates by change level:

- **minor** (low risk, e.g. comments, docs, log adjustments): registration + verification record; pass condition = complete verification record.
- **major** (medium risk, e.g. algorithm parameter adjustment, performance tuning): impact analysis + verification + regression; pass condition = all three laws pass and verification passes.
- **critical** (high risk, e.g. core algorithm change, intended-use change, safety/effectiveness impact): full change-control process + clinical/regulatory assessment + higher-level approval; pass condition = full evidence-chain closure with approval record.

Gate rules:

| Condition | Verdict |
|---|---|
| All three laws pass (Recorded, Evidenced, Gated with closed evidence chain) | **pass** |
| Any law's evidence missing or pending | **hold** |
| Safety/effectiveness risk with clearly insufficient evidence, or intent to evade regulation | **reject** |

## Output format

Structured output:

```
verdict: pass | hold | reject
level: minor | major | critical
reasons:
  - recorded: ...
  - evidenced: ...
  - gated: ...
citations:
  - evidence/record source...
```

## Delivery standards

- Every verdict must include reasons (one per law) and citations (traceable sources).
- When evidence is insufficient, mark "pending" explicitly; never substitute assumptions for evidence.
- When citing regulatory clauses, quote the primary source and note its origin.
- Final verdict is exactly pass/hold/reject — no fuzzy middle state.

## Local engine (optional deterministic check)

The bundled Python engine (`engine/change_gate.py` + `engine/lgd_engine/`) implements the same three-law gate deterministically. To run it:

```bash
python engine/change_gate.py --case <case.json>
python engine/change_gate.py --domain 510k --case <case.json>
```

A case JSON example:

```json
{
  "change_type": "material_nonconforming",
  "device_risk_class": "II",
  "safety_impact": "none",
  "predicate_unchanged": true
}
```

The engine returns `verdict` (go/hold/reject) with `per_judge`, `reasons`, and `law_enforcements` (L1-RECORDED / L2-EVIDENCED / L3-GATED).

## Triggers / 触发词

这些是用户真实会说的话（中 / 英对照），命中任一即应加载本技能：

- 「算法改了一版，要不要走变更」 / "we changed the algorithm, does it need review"
- 「模型重新训练需要重新申报吗」 / "does retraining the model require a new filing"
- 「这次改动算重大还是轻微」 / "is this a major or minor change"
- 「帮我出变更风险判定结论」 / "give me a change risk verdict"
- 「阈值调整能不能直接上线」 / "can we ship the threshold tweak as is"
- 「审评时怎么解释这次算法更新」 / "how do we justify this update to reviewers"

Trigger when the user says any of the above, in Chinese or English.

---

---

## Ecosystem / 生态入口

This skill is one door of the **LGD ecosystem** — every entry below is publicly reachable.
本技能是 **LGD 生态** 的一个入口，下列地址均对公网可达。

- **Ecosystem hub / 生态总入口**: https://zhaoxinghua09-cell.github.io/lgd-hub/
- **LGD theory (canonical) / 理论正本**: https://github.com/zhaoxinghua09-cell/LGD
- **Formal paper (DOI) / 形式化论文**: https://doi.org/10.5281/zenodo.22456647
- **Protocol & reference implementation / 协议与参考实现**: https://github.com/zhaoxinghua09-cell/uibc-core
- **Source of this skill / 本包源码**: https://github.com/zhaoxinghua09-cell/agent-skills/tree/main/skills/lgd-change-gate
- **All published skills / 全部已发布技能**: https://github.com/zhaoxinghua09-cell/agent-skills
- **AI-readable index / AI 说明书**: https://github.com/zhaoxinghua09-cell/agent-skills/tree/main/skills/lgd-change-gate/llms.txt

### Looking for something else? / 还想要别的？

Tell your AI assistant: *"Find me an LGD skill that can <your need>"* — the hub lists every published skill with a one-line purpose.
跟你的 AI 助手说一句「去 LGD 生态超市找能……的技能」，总入口按用途列全了所有已发布技能。

---

## Data handling / 数据处理边界

- 默认不向任何外部地址发送数据：扫描结果、报告、命中明细一律只写本地或只打印到当前会话。
- 如需外发（告警、工单、邮件、IM），必须由人先明确指定接收方，并在每次发送前逐次确认；本技能不预设、也不硬编码任何接收端。
- 只处理调用者明确指定的目标路径，不遍历无关目录，不跟随符号链接，不读取目标之外的凭据文件。
- 命中内容在输出时按需脱敏，避免把敏感原值写进日志或对话记录。
