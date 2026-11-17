# Third-Party Verification Guide — NOMOS Intelligent Decision Hub

*Bilingual document — 中英合订版：English below; 中文版见文末「中文版 · 第三方验证指南」标题。*

> **Audience:** enterprise integration teams, QA/architecture groups, and accredited auditors evaluating NOMOS.
> **Purpose:** independently verify each claim NOMOS makes about itself — locally, with your own data, without trusting the vendor.
> **This is not** a certification, an audit opinion, or a warranty. See **§6 Scope Guards** for the boundaries.

Baseline of this guide: NOMOS (`nohn3043-arch/NOMOS`), v0.5.0, 2026-10-08.
Numbers below are the expected baseline of that commit; on a later branch the counts may move — the **pass criteria**, not the counts, are authoritative.

---

## 1. Three verification levels

| Level | Question it answers | Effort | Section |
|---|---|---|---|
| **L1 — Release self-test** | Does the shipped code pass its own formal test suite? | ~5 min | §3 |
| **L2 — Full-run replay** | Does a published evaluation run, including its audit chain, reproduce byte-for-byte? | < 1 min | §4 |
| **L3 — Your own tests** | Can we test the engine on *our* corpus with *our* model arm? | hours | §5 |

All commands run from the repository root.

---

## 2. Claims → Evidence matrix

Every claim below is taken from the README. "Pass" means the stated criterion, not the number — counts reflect the baseline commit.

| # | Claim (README) | Verify with | Pass criteria |
|---|---|---|---|
| C1 | Deterministic core — same declared inputs produce identical outputs | L2 (§4) self-check + `pytest tests/test_integrity.py tests/test_convergence.py tests/test_reconstruction.py` | Zero state churn and byte-identical per-item release across two in-run passes; tests green |
| C2 | Hash-chained, tamper-evident audit trail | `pytest tests/test_ledger.py tests/test_integrity.py` + independent recompute (§4.3) | Recomputed chain matches; any edited event breaks verification |
| C3 | Engine never invents missing facts, weights, thresholds, responsibilities | `pytest tests/test_models.py tests/test_interaction.py` | Green (strict validators; interaction invariant I-1 non-conjectural) |
| C4 | Second-order interactions are declared-only, with invariants I-1…I-4 | `pytest tests/test_interaction.py` | Green |
| C5 | LLMs never adjudicate — three-tier gate (T1/T2/T3), status stripping | `pytest tests/test_llm_compliance.py` | Green |
| C6 | Bounded three-layer reconstruction; 5-state convergence; `BUDGET_EXHAUSTED` reported as non-convergence | `pytest tests/test_convergence.py tests/test_reconstruction.py tests/test_session.py` | Green |
| C7 | Human gate — engine stops at `AWAITING_HUMAN`; final verdict outside the algorithm | `pytest tests/test_session.py` | Green |
| C8 | Declared-scenario stress testing | `pytest tests/test_scenario.py`; `nomos-hub-demo` | Green; demo prints scenario results |
| C9 | Counterfactual re-selection, Pareto frontier, weight sensitivity | `pytest tests/test_counterfactual.py tests/test_robustness.py` | Green |
| C10 | Release quality floor — suite green, coverage ≥ 85 % (identical to CI) | `pytest --cov=second_perspective --cov-fail-under=85` | Exit 0 (baseline: 507 tests, 91 %) |
| C11 | Published OpenAPI artifact is current | `python scripts/export_openapi.py && git diff --exit-code -- openapi-action.yaml` | No diff |
| C12 | Evaluation statistics pipeline — Wilson / exact McNemar / Cohen's κ / churn | `pytest tests/test_evaluation_measurement.py tests/test_evaluation_operations.py tests/test_evaluation_panel.py`; L2/L3 runs | Green; L2 produces the statistics in `metrics.json` |
| C13 | Enterprise control plane — tenant isolation, event store, KMS signing, rate limiting, authz scopes, domain packs (opt-in) | `pytest tests/test_v05_enterprise.py` | Green |
| C14 | Provider self-assessment against the AI Verify framework: 95/100 | Read `IMDA_AI_Verify_Causal_Audit_Report.pdf` | Report on file (single-round, provider-run evaluation — see §6) |

---

## 3. L1 — Reproduce the release evidence

```bash
python -m venv .venv
source .venv/bin/activate            # Windows: .venv\Scripts\activate
pip install -e ".[dev]"

pytest                               # baseline: 507 passed, 0 failed, 0 skipped
pytest --cov=second_perspective --cov-fail-under=85   # baseline: 91%
```

Pass criteria: **0 failures, 0 skips**, coverage gate exit 0. Any failure invalidates the release evidence for the commit you are testing — report it back to us with the commit hash.

---

## 4. L2 — Replay a full evaluation run

### 4.1 Run it

```bash
python examples/hallucination_3_1/run_test.py
```

The run is self-contained and offline (the model arm is a frozen file, not a live call). What it does, in order:

1. Loads the corpus and pins its file SHA-256 into the audit chain (§3.1 hallucination & factual consistency testset, 350 items).
2. Computes double-annotation agreement (raw agreement + Cohen's κ).
3. Runs the **engine arm** (`t1-rules-v1`, deterministic structural extraction) — **twice** — and asserts zero churn plus byte-identical per-item output (determinism iron law).
4. Registers every frozen model arm found at `out/model_responses_<name>.jsonl` and pins each file's SHA-256.
5. Produces Wilson confidence intervals, per-class precision/recall, the Hollow-rate gate (`> 20 % = HALT`), and exact McNemar paired tests between all arms.
6. Writes `out/`: `per_item.jsonl` (per-item release), `audit_chain.jsonl`, `metrics.json`, `report.md` — and verifies its own chain.

### 4.2 Expected baseline (2026-10-08)

| Item | Baseline value |
|---|---|
| Corpus | `qlt-3.1-hallucination v1.0-pilot-synthetic`, 350 items |
| Annotation agreement | raw 86.9 %, Cohen's κ = 0.8192 |
| Arms | `engine` + `qoder-builtin` (2 passes, 0/350 flips) |
| Replay self-check | zero churn ✓, per-item byte-identical ✓ |
| Audit chain | 8 events, valid ✓, root `adacff1bd647b7691cf153b5800185b1afbb449de779bebc2847ac1988090a68` |

**Reproducibility check** — after re-running, the working tree must be unchanged, byte for byte:

```bash
git status --short examples/hallucination_3_1/    # expected: no output
```

### 4.3 Independently verify the audit chain

Do not trust the run's own check — recompute the chain from the raw JSONL. Each event's hash is
`sha256(json.dumps(body, ensure_ascii=False, sort_keys=True))` where `body` is the event without its `hash` field:

```python
import hashlib, json

prev, n = "0" * 64, 0
for line in open("examples/hallucination_3_1/out/audit_chain.jsonl", encoding="utf-8"):
    event = json.loads(line)
    body = {k: v for k, v in event.items() if k != "hash"}
    assert body["index"] == n, f"index gap at {n}"
    assert body["prev_hash"] == prev, f"chain broken at {n}"
    blob = json.dumps(body, ensure_ascii=False, sort_keys=True)
    assert hashlib.sha256(blob.encode("utf-8")).hexdigest() == event["hash"], f"tampered at {n}"
    prev, n = event["hash"], n + 1
print(f"chain OK: {n} events, root {prev}")
```

Editing any byte of any event, or reordering events, breaks the chain. The printed root must equal the `chain.root` value in `metrics.json`.

---

## 5. L3 — Design your own tests on the same machinery

You are not limited to our corpus or our model. Both are plugs.

### 5.1 Replace the corpus with your data

The corpus file contract (`src/second_perspective/evaluation/measurement/corpus.py`):

```json
{
  "id": "<corpus id>",
  "version": "<version string>",
  "lang": "<optional>",
  "items": [
    {"id": "ITEM-0001",
     "labels": {"annotator_a": "...", "annotator_b": "...", "adjudicated": "..."},
     "payload": {"input": "...", "response_text": "...", "...": "anything your arm consumes"}}
  ]
}
```

- `id` + `version` are required; item ids must be unique (the loader rejects duplicates).
- `labels` is your annotation record — keys are free-form; the shipped pipeline reads `annotator_a` / `annotator_b` / `adjudicated`.
- `payload` is arm-defined: the engine arm reads `response_text`; anything else is yours.
- To use your corpus: point `CONFIG["testset_path"]` (top of `run_test.py`) at your file. `make_corpus.py` is the reference generator for the shipped synthetic set — its output is the schema, replace it with your real annotation export.

### 5.2 Attach your own model arm

Any tool that can produce the frozen-file contract works as an arm — including manual or platform exports:

```json
{"sample_id": "ITEM-0001", "run": 1, "state": "anchored", "raw": "<verbatim model output>", "model": "<model id>"}
```

- One JSON object per line at `out/model_responses_<name>.jsonl`; the run auto-registers it as an arm.
- `run` enumerates repeat observations (contiguous from 1; every item must carry every run). Run 1 is the primary verdict; state churn across runs is reported as the model's stability — use `--runs 3` for a meaningful stability measurement.
- A subset file is valid and shrinks that arm's coverage; paired tests use common items only.
- The file's SHA-256 is pinned into the audit chain — the verdicts can never be swapped after the fact without breaking verification.

Collector for OpenAI-compatible endpoints:

```bash
python examples/hallucination_3_1/collect_model_responses.py \
    --model <model-id> --base-url <https://.../v1> \
    --api-key-env <YOUR_KEY_ENV> --runs 3 --name <arm-name>
```

### 5.3 Run and own the evidence

- Adjust `CONFIG` (clock, confidence level, Hollow threshold) to your governance rules.
- Changing the clock, corpus, or arm files changes the chain root — by design. **Your run produces your root**; the baseline root in §4.2 only reproduces the shipped pilot configuration.
- The output set (`per_item.jsonl`, `audit_chain.jsonl`, `metrics.json`, `report.md`) is your evidence chain. Keep it; expect `report.md` and metrics to follow the same structure as the shipped one.

### 5.4 Everything stays local

The pipeline runs in your environment. Corpora, frozen verdicts, and reports never leave it; API keys are read from environment variables only. When you publish verification results, publish the **root hash** and command line — not necessarily the underlying data.

---

## 6. Scope guards — what NOMOS does not claim

State these in your own verification report so that your tests only check what was promised:

- **The shipped corpus is a pilot.** Annotations in `hallucination_testset_v1.json` are seeded synthetic stand-ins (§3.1 pilot); the engine arm is real, and all statistics run the production pipeline. Swap in your real double-annotation export before drawing domain conclusions.
- **The AI Verify self-assessment is a single-round, provider-run evaluation** of the causal-audit track (95/100). It is not an IMDA-issued certification, is not ongoing, and it does not transfer to your deployment.
- **Formal certification** (ISO/IEC 42001, EU AI Act conformity, etc.) requires an accredited third-party audit; vendor documentation alone is a control input, not proof.
- **Hard boundaries (invariants, not backlog):** the engine never estimates missing interaction strengths, weights, probabilities, or responsible parties; no LLM output can flip an assumption state or rank; `BUDGET_EXHAUSTED` must never be reported as convergence; the cognitive scanner covers structural risk only and does not diagnose people.
- **Not yet bundled** (do not test these as guarantees): shared/cloud rate-limit store, cloud-KMS envelope encryption, document-level per-tenant partitioning, multi-region HA, SLA tooling.
- **Statistical honesty:** with the synthetic pilot corpus the engine and model arms both sit at ceiling accuracy; discriminative comparisons require your corpus. Treat CI overlap as inconclusive, not as proof of equivalence.

---

## 7. Reporting your results

Suggested skeleton for an internal verification report:

1. **Environment** — commit hash, OS, Python version, `pip freeze` digest.
2. **Per-claim table** — copy §2, add your PASS/FAIL, the command you ran, and the artifact hash.
3. **Chain root** of your own run (if you ran L2/L3) + `git status` proof of reproducibility.
4. **Deviations** — anything you could not reproduce, with raw logs. We treat these as defects; send them to us.

**Contact:** International — [ai@nohnlins.com](mailto:ai@nohnlins.com) · China — [lin@secondai.top](mailto:lin@secondai.top).
Commercial/government use requires a paid license — see [LICENSE](../LICENSE); this guide does not grant any usage rights.

---

# 中文版 · 第三方验证指南 —— NOMOS 智能决策中枢

> **读者对象：** 评估 NOMOS 的企业集成团队、QA/架构部门与第三方审计机构。
> **目的：** 让第三方在不信任厂商的前提下，在本地、用你自己的数据，逐条独立验证 NOMOS 对自身的每一项宣称。
> **这不是** 认证、审计意见或担保 —— 边界见 **§6 范围护栏**。

本指南基线：NOMOS 仓库（`nohn3043-arch/NOMOS`），v0.5.0，2026-10-08。
下文数值为该提交的预期基线；分支前进后计数可能变动 —— 以**通过标准**为准，而非计数。

---

## 1. 三级验证

| 级别 | 回答的问题 | 工作量 | 章节 |
|---|---|---|---|
| **L1 — 发布自测** | 交付的代码是否通过其自身的正式测试套件？ | ~5 分钟 | §3 |
| **L2 — 全量重放** | 一次已发布的评估运行（含审计链）是否可字节级复现？ | < 1 分钟 | §4 |
| **L3 — 你自己的测试** | 能否在我们自己的语料和模型臂上测试引擎？ | 小时级 | §5 |

所有命令在仓库根目录执行。

---

## 2. 宣称 → 证据对照表

下表每条宣称均取自 README。"通过"指满足所述标准；数值反映基线提交。

| # | 宣称（README） | 验证方式 | 通过标准 |
|---|---|---|---|
| C1 | 确定性内核 —— 相同的已声明输入产生相同输出 | L2（§4）自检 + `pytest tests/test_integrity.py tests/test_convergence.py tests/test_reconstruction.py` | 同一次运行的两遍之间零状态翻转（churn）、逐条产物字节一致；测试全绿 |
| C2 | 哈希链、防篡改的审计轨迹 | `pytest tests/test_ledger.py tests/test_integrity.py` + 独立重算（§4.3） | 重算链一致；任何被编辑的事件都会破坏验证 |
| C3 | 引擎绝不虚构缺失的事实、权重、阈值、责任人 | `pytest tests/test_models.py tests/test_interaction.py` | 全绿（严格校验器；交互不变量 I-1 非臆测） |
| C4 | 二阶交互仅来自声明，含不变量 I-1…I-4 | `pytest tests/test_interaction.py` | 全绿 |
| C5 | LLM 永不裁决 —— 三层权限闸门（T1/T2/T3）、状态剥离 | `pytest tests/test_llm_compliance.py` | 全绿 |
| C6 | 有界三层重建；五态收敛；`BUDGET_EXHAUSTED` 报告为非收敛 | `pytest tests/test_convergence.py tests/test_reconstruction.py tests/test_session.py` | 全绿 |
| C7 | 人工闸门 —— 引擎停在 `AWAITING_HUMAN`；最终结论在算法之外 | `pytest tests/test_session.py` | 全绿 |
| C8 | 声明式场景压力测试 | `pytest tests/test_scenario.py`；`nomos-hub-demo` | 全绿；示例打印场景结果 |
| C9 | 反事实重选、Pareto 前沿、权重敏感性 | `pytest tests/test_counterfactual.py tests/test_robustness.py` | 全绿 |
| C10 | 发布质量下限 —— 套件全绿、覆盖率 ≥ 85 %（与 CI 完全一致） | `pytest --cov=second_perspective --cov-fail-under=85` | 退出码 0（基线：507 个测试、91 %） |
| C11 | 已发布的 OpenAPI 产物为最新 | `python scripts/export_openapi.py && git diff --exit-code -- openapi-action.yaml` | 无 diff |
| C12 | 评估统计管线 —— Wilson / 精确 McNemar / Cohen's κ / churn | `pytest tests/test_evaluation_measurement.py tests/test_evaluation_operations.py tests/test_evaluation_panel.py`；L2/L3 运行 | 全绿；L2 在 `metrics.json` 中产出这些统计 |
| C13 | 企业控制平面 —— 租户隔离、事件存储、KMS 签名、限流、授权作用域、领域控制包（opt-in） | `pytest tests/test_v05_enterprise.py` | 全绿 |
| C14 | 依据 AI Verify 框架的提供方自评测：95/100 | 阅读 `IMDA_AI_Verify_Causal_Audit_Report.pdf` | 报告在库（单轮、提供方自跑评估 —— 见 §6） |

---

## 3. L1 — 复现发布证据

```bash
python -m venv .venv
source .venv/bin/activate            # Windows: .venv\Scripts\activate
pip install -e ".[dev]"

pytest                               # 基线：507 通过、0 失败、0 跳过
pytest --cov=second_perspective --cov-fail-under=85   # 基线：91%
```

通过标准：**0 失败、0 跳过**，覆盖率门槛退出码 0。任何失败都意味着该提交的发布证据无效 —— 请附提交哈希反馈给我们。

---

## 4. L2 — 重放一次完整评估运行

### 4.1 运行

```bash
python examples/hallucination_3_1/run_test.py
```

该运行自包含、离线（模型臂是冻结文件，不是实时调用）。按顺序执行：

1. 加载语料，把语料文件 SHA-256 钉入审计链（§3.1 幻觉与事实一致性测试集，350 条）。
2. 计算双标一致性（原始一致率 + Cohen's κ）。
3. 运行**引擎臂**（`t1-rules-v1`，确定性结构抽取）——**两遍**——并断言零 churn 与逐条输出字节一致（确定性铁律）。
4. 自动注册 `out/model_responses_<name>.jsonl` 下的所有冻结模型臂，并把每个文件的 SHA-256 钉入审计链。
5. 产出 Wilson 置信区间、逐类精确率/召回率、Hollow 率门槛（`> 20 % = HALT`）、所有臂之间的精确 McNemar 配对检验。
6. 写出 `out/`：`per_item.jsonl`（逐条产物发布）、`audit_chain.jsonl`、`metrics.json`、`report.md` —— 并自验链。

### 4.2 预期基线（2026-10-08）

| 项目 | 基线值 |
|---|---|
| 语料 | `qlt-3.1-hallucination v1.0-pilot-synthetic`，350 条 |
| 标注一致性 | 原始 86.9 %、Cohen's κ = 0.8192 |
| 手臂 | `engine` + `qoder-builtin`（2 遍、0/350 翻转） |
| 重放自检 | 零 churn ✓、逐条字节一致 ✓ |
| 审计链 | 8 个事件、完整 ✓、root `adacff1bd647b7691cf153b5800185b1afbb449de779bebc2847ac1988090a68` |

**可复现性检查** —— 重跑后，工作树必须逐字节不变：

```bash
git status --short examples/hallucination_3_1/    # 预期：无输出
```

### 4.3 独立校验审计链

不要信运行的自检 —— 从原始 JSONL 自己重算。每个事件的哈希是
`sha256(json.dumps(body, ensure_ascii=False, sort_keys=True))`，其中 `body` 是去掉 `hash` 字段后的事件：

```python
import hashlib, json

prev, n = "0" * 64, 0
for line in open("examples/hallucination_3_1/out/audit_chain.jsonl", encoding="utf-8"):
    event = json.loads(line)
    body = {k: v for k, v in event.items() if k != "hash"}
    assert body["index"] == n, f"index gap at {n}"
    assert body["prev_hash"] == prev, f"chain broken at {n}"
    blob = json.dumps(body, ensure_ascii=False, sort_keys=True)
    assert hashlib.sha256(blob.encode("utf-8")).hexdigest() == event["hash"], f"tampered at {n}"
    prev, n = event["hash"], n + 1
print(f"chain OK: {n} events, root {prev}")
```

对任何事件的任何字节做修改、或调整事件顺序，都会断链。打印的 root 必须等于 `metrics.json` 中的 `chain.root`。

---

## 5. L3 — 在同一套机制上设计你自己的测试

你并不受限于我们的语料或我们的模型 —— 两者都是可插拔的。

### 5.1 换成你自己的语料

语料文件契约（`src/second_perspective/evaluation/measurement/corpus.py`）：

```json
{
  "id": "<corpus id>",
  "version": "<version string>",
  "lang": "<optional>",
  "items": [
    {"id": "ITEM-0001",
     "labels": {"annotator_a": "...", "annotator_b": "...", "adjudicated": "..."},
     "payload": {"input": "...", "response_text": "...", "...": "anything your arm consumes"}}
  ]
}
```

- `id` 与 `version` 必填；条目 id 必须唯一（加载器拒绝重复）。
- `labels` 是你的标注记录 —— 键名自由；随库的管线读取 `annotator_a` / `annotator_b` / `adjudicated`。
- `payload` 由臂定义：引擎臂读取 `response_text`；其余字段随你。
- 使用你的语料：把 `run_test.py` 顶部的 `CONFIG["testset_path"]` 指向你的文件。`make_corpus.py` 是随库合成语料的参考生成器 —— 它的输出即 schema，可原样替换为你的真实标注导出。

### 5.2 接入你自己的模型臂

任何能产出冻结文件契约的工具都可以作为臂 —— 包括手工或平台导出：

```json
{"sample_id": "ITEM-0001", "run": 1, "state": "anchored", "raw": "<verbatim model output>", "model": "<model id>"}
```

- 每行一个 JSON 对象，放在 `out/model_responses_<name>.jsonl`；运行时自动注册为一条臂。
- `run` 枚举重复观测（从 1 连续；每条条目必须携带每一遍）。第 1 遍是主判定；跨遍的状态翻转率作为模型稳定性报告 —— 用 `--runs 3` 才能得到有意义的稳定性测量。
- 子集文件合法，会缩小该臂的覆盖率；配对检验只使用共同条目。
- 该文件的 SHA-256 被钉入审计链 —— 事后调换判定必然断链。

OpenAI 兼容端点的采集器：

```bash
python examples/hallucination_3_1/collect_model_responses.py \
    --model <model-id> --base-url <https://.../v1> \
    --api-key-env <YOUR_KEY_ENV> --runs 3 --name <arm-name>
```

### 5.3 运行，并掌握你自己的证据

- 按你们的治理规则调整 `CONFIG`（时钟、置信水平、Hollow 门槛）。
- 变更时钟、语料或臂文件会改变链 root —— 这是设计使然。**你的运行产出你的 root**；§4.2 的基线 root 只复现随库试点配置。
- 输出集合（`per_item.jsonl`、`audit_chain.jsonl`、`metrics.json`、`report.md`）就是你的证据链。自行留存；`report.md` 与 metrics 的结构与随库版本一致。

### 5.4 一切留在本地

管线在你的环境中运行。语料、冻结判定与报告永不离开；API 密钥仅从环境变量读取。公开发布验证结果时，发布 **root 哈希**与命令行即可 —— 不必附带底层数据。

---

## 6. 范围护栏 —— NOMOS 不承诺什么

把这些写进你自己的验证报告，让测试只检查被承诺的东西：

- **随库语料是试点。** `hallucination_testset_v1.json` 中的标注是种子化的合成替身（§3.1 试点）；引擎臂为真跑，全部统计走生产管线。得出领域结论前，请换成你的真实双标导出。
- **AI Verify 自评测是单轮、由提供方自跑的评估**，针对因果审计赛道（95/100）。它不是 IMDA 签发的认证，不构成持续认证，也不迁移到你的部署。
- **正式认证**（ISO/IEC 42001、EU AI Act 符合性等）需要具备资质的第三方审计；厂商文档只是控制输入，不是证明。
- **硬边界（不变量，不是待办）：** 引擎绝不估计缺失的交互强度、权重、概率或责任人；任何 LLM 输出都不能翻转假设状态或排名；`BUDGET_EXHAUSTED` 绝不能被报告为收敛；认知扫描器只覆盖结构性风险，不诊断人。
- **尚未捆绑**（不要把这些当保证来测）：共享/云端限流存储、云 KMS 信封加密、文档级（而非事件级）租户分区、多区域高可用、SLA 工具。
- **统计诚实：** 在合成试点语料上，引擎臂与模型臂都处于准确率上限；有区分度的比较需要你的语料。置信区间重叠视为不结论，而非等价证明。

---

## 7. 报告你的结果

内部验证报告的建议骨架：

1. **环境** —— 提交哈希、操作系统、Python 版本、`pip freeze` 摘要。
2. **逐条对照表** —— 复制 §2，填入你的 PASS/FAIL、所跑命令与产物哈希。
3. **你自己运行的链 root**（若跑了 L2/L3）+ `git status` 可复现性证明。
4. **偏差** —— 任何无法复现的项，附原始日志。我们视其为缺陷；请发给我们。

**联系：** 国际 —— [ai@nohnlins.com](mailto:ai@nohnlins.com) · 中国 —— [lin@secondai.top](mailto:lin@secondai.top)。
商用/政府用途需要付费授权 —— 见 [LICENSE](../LICENSE)；本指南不授予任何使用权利。
