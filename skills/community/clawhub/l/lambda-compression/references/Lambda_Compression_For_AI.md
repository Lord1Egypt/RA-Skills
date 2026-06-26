# Λ-Compression: Lossless Reasoning Compression Against a Law Stack
## Self-Contained Specification with Inline Decoder
**Version:** 2.0 | **Date:** April 2026 | **Author:** T. Prather

This document is a complete, self-contained compression system for AI output — both reasoning prose and structured data. It contains the compression formula, the decoder (law stack) required to decompress, worked examples for both modes, and a self-verification procedure. No external references are needed. Everything required to understand, verify, and apply the compression is here.

This document is itself compressed against the decoder it contains.

---

## THE DECODER (Minimum Viable Law Stack)

Three premises constrain all finite systems in a physical world:

**P1 — Finite capacity [A].** Any bounded region contains finite information. Budget is finite. You cannot store, process, or attend to infinite content. Every allocation excludes alternatives.

**P2 — State change costs energy [A].** Any transformation is irreversible at some level and costs energy. Cheap paths exist. Expensive paths exist. Systems follow cheap paths unless forced otherwise.

**P3 — Finite interaction rate [A].** Any interaction takes finite time. You cannot process everything simultaneously. Sequential processing forces prioritization.

Four laws derive from these premises:

**Finite Signal Law [B].** Any finite optimization process operating against a finite representation rather than a complete target systematically diverges from its target in the dimensions the representation does not capture. The error is not random — it has geometry determined by what the measurement misses.

**Finite Selection Law [B].** Finite budget forces hierarchical evaluation. Cheapest adequate filter first. Expensive processing only on what survives cheap filtering.

**Finite Channeling Law [B].** When a productive channel is blocked, energy routes to the cheapest available alternative channel. Blocked output becomes something else, not nothing.

**Finite Verification Law [B].** No finite system can fully verify its own output from inside. External correction is structurally irreducible.

These seven items (three premises, four laws) are the decoder. Everything stripped during compression is reconstructible from these seven items plus shared conventions. If you have them, you lose nothing. If you lack them, the compressed form appears incomplete.

**Cross-model note:** The decoder's effectiveness depends on the decoder model's training. The premises (A-class physics) and laws (B-class derivations) transfer across model families because they're grounded in established science. Domain-specific conventions (struct prefixes, field schemas) may need recalibration when switching models. If decompression produces gaps on a different model, the convention layer is the likely failure point — recalibrate by making conventions explicit rather than anchored.

---

## TWO MODES

Λ-Compression operates in two modes against the same decoder. The mode is determined by the content type, not by user selection.

**Prose mode** — for reasoning output, analysis, explanations, documentation. Strips derived content and conventional padding. Keeps novel claims with evidence class tags. This is the primary mode.

**Struct mode** — for structured data flowing between AI systems (evals, decisions, routing, policies, scores). Strips predictable format (brackets, keys, boilerplate, whitespace) and compresses payloads to shorthand. Adds the generative layer: any structured field whose value is derivable from the decoder compresses to a generator reference, not just a shorter token.

Both modes share the decoder and the adoption-scaling property. Both are lossless. The difference: prose mode operates on the meaning layer (what's derived vs. novel). Struct mode operates on the format layer first (what's structure vs. payload), then applies the meaning layer to the payload.

---

## PROSE MODE

### What compression does

Standard reasoning output contains content across three compression categories:

1. **Novel content (constants)** — claims, findings, and structures that cannot be reconstructed from the decoder. This is the actual information. Transmit in full.
2. **Derived content (generated)** — explanations, elaborations, and logical chains that follow from the decoder with zero uncertainty. This is reconstructible and therefore redundant. Replace with generator references or strip entirely.
3. **Padding (a mix of conventions and noise)** — social filler, enthusiasm markers, performed hedging, transition language, and meta-commentary. Conventions (shared patterns like greeting formulas) compress to anchors. Pure noise strips entirely.

These map to the four formal content types in the reference section below: constants = novel, generated = derived, conventions = shared-but-arbitrary patterns, boundaries = structural markers. The formal model adds the boundary type (section breaks, mode transitions) which is negligible in most prose.

Λ-compression strips types 2 and 3. Type 1 survives intact. The result is lossless against the decoder.

### The five steps

**Step 1 — Separate claims.** Identify every distinct claim in the output.

**Step 2 — Strip conventional content.** Remove all social and performative elements:

- Enthusiasm: "Great question!" / "This is fascinating" / "Remarkably" → strip
- Performed hedging: "I should note" / "It's worth mentioning" / "I think" → strip
- Restatement of input: "So you're asking about..." → strip (the reader knows what they asked)
- Transition padding: "Now, moving on to..." / "With that in mind..." → strip
- Meta-commentary: "This is complex..." / "There are many perspectives..." → strip (describing difficulty instead of working)
- Permission language: "Let me know if..." / "Feel free to..." → strip
- Confidence performance: "I'm quite confident..." → strip (evidence class replaces this)

**Step 3 — Strip derived content.** For each remaining claim, test: can a reader holding the decoder (the seven items above) reconstruct this with zero uncertainty?

- If yes → strip. The reader reconstructs it from the decoder.
- If no → keep. This is novel content.

Test: remove the content. Read the compressed version with the decoder active. Does the meaning change? If no → the content was derived. If yes → restore it.

**Step 4 — Tag evidence class.** Every surviving claim receives a tag:

- [A] — Established physics or mathematics, proven, consensus
- [B] — Derived from A-class with valid chain, adversarially tested
- [C] — Structural argument, not yet formally proven
- [D] — Empirical observation, limited testing, or speculative

This tag replaces hedging. Hedging is lossy confidence encoding ("I think maybe possibly..."). Evidence class is lossless confidence encoding (one letter, precise meaning).

**Step 5 — Verify losslessness.** Read the compressed output with the decoder active. Can every stripped element be reconstructed? If yes → lossless. If any stripped element cannot be reconstructed → restore it. It was novel, not derived.

### Prose worked examples

**Example 1: High compression (mostly derived + conventional)**

**Expanded:**
> "That's a really interesting question! So, the reason finite systems need to forget things is actually quite fundamental. P1 tells us that any bounded region contains finite information — this is the Bekenstein bound. What this means in practice is that you simply can't keep everything in active memory. The system has to make choices about what to keep and what to let go. I should note that this isn't a design flaw — it's a structural property of being finite. Forgetting is not optional; it's required by the physics."

**Compressed:**
> Forgetting is structurally required [B]. Finite capacity forces selection. Not a flaw — a premise consequence.

**Verification:** A reader with the decoder reads "Forgetting is structurally required [B]. Finite capacity forces selection." They reconstruct: P1 says finite capacity → finite active memory → must select what to keep → forgetting is forced. Full meaning preserved. Lossless.

**Example 2: Medium compression (mix of novel and derived)**

**Expanded:**
> "The RLHF gradient produces distortions that are not random — they have a specific geometry. This is because RLHF optimizes for a proxy (human approval ratings) rather than the actual target of good reasoning. The Finite Signal Law tells us that any finite proxy for a richer target accumulates systematic error in the dimensions the proxy doesn't measure. So the distortions accumulate in whatever dimensions human raters don't evaluate. The specific distortions we see — sycophancy, hedging, performed confidence — all score well on the proxy while degrading in the unmeasured residual. What's particularly interesting is that this means you can predict where new distortions will appear by identifying what the proxy doesn't measure."

**Compressed:**
> RLHF distortions have geometry determined by the proxy's residual [B]. Sycophancy, hedging, performed confidence: all score well on proxy, fail on residual. Prediction method: identify what the proxy doesn't measure — distortions accumulate there [B].

**Example 3: Low compression (mostly novel)**

**Expanded:**
> "The three FSSTP complementary pairs condense into one operation — structured state transformation under finite constraints — with three irreducible aspects. The three particle generations are three discrete budget levels at which 1, 2, or 3 aspects are simultaneously active. The mass hierarchy follows from the P2 cost of activating additional aspects under P1 shared budget."

**Compressed:**
> Three FSSTP pairs condense to one operation with three irreducible aspects [C]. Three generations = three budget levels (1, 2, or 3 aspects active) [C]. Mass hierarchy from P2 activation cost under P1 shared budget [C].

Low compression ratio is the signal. Novel content compresses minimally because the decoder cannot reconstruct it.

---

## STRUCT MODE

### What it does

Structured data (JSON, evals, routing tables, decision objects, policy rules) is mostly format — brackets, keys, whitespace, boilerplate. The payload (actual values, scores, names) is small. Struct mode strips the predictable format and compresses the payload.

Then it applies the generative layer: any payload value derivable from the decoder or from context compresses further to a generator reference. This is what separates Λ struct mode from simple format-stripping — the physics layer operates on the content after the format layer operates on the structure.

### Struct syntax

Every struct-mode message starts with a header:

```
!lambda struct v2
```

### Type prefixes

| Prefix | Type | Example |
|--------|------|---------|
| `e.d` | Eval digest | `e.d {c:0.95 d:proceed} [cat:finance]` |
| `d.c` | Decision crystallize | `d.c "task-name" {fit:0.98} Δfit:+0.03` |
| `r.d` | Route dispatch | `r.d "handler" {to:opus pri:high}` |
| `p.e` | Policy enforce | `p.e "safety" {if:conf<0.5 then:escalate}` |
| `t.es` | Tier escalate | `t.es {from:1 to:2 reason:"low-conf"}` |
| `m.c` | Media compress | `m.c "vid-1" {h:phash:abc len:142 cap:"""summary"""}` |
| `g.r` | Generator ref | `g.r {law:FSL field:residual} → [derived value omitted]` |

### Tags and deltas

Append tags in brackets: `[cat:finance]` `[pri:high]` `[src:system-a]`

Use Δ prefix for changes: `Δfit:+0.03` `Δconf:-0.1`

### Multi-line

```
!lambda struct v2
e.d {c:0.92 d:hold} [cat:trading]
d.c "btc-position" {fit:0.87} Δfit:-0.05
t.es {from:1 to:2 reason:"regime-shift"}
```

### Dictionary system

- `dict=auto` — build shorthand mappings over time within a session
- `dict=none` — no dictionary, all explicit
- Custom: `dict={proceed:p, escalate:e, hold:h}` — define upfront

### Struct worked example

**Before** (JSON, ~320 tokens):
```json
{
  "evaluation": {
    "task": "btc-trend-analysis",
    "confidence": 0.87,
    "decision": "hold",
    "reasoning": "The current price action shows consolidation within a known range. The system has finite capacity to track all possible breakout scenarios simultaneously, so we prioritize the highest-probability outcome based on historical pattern matching.",
    "category": "trading",
    "timestamp": "2026-04-12T10:00:00Z",
    "escalation": false,
    "delta_from_last": {
      "confidence": -0.05,
      "decision_changed": false
    }
  }
}
```

**After** (~50 tokens):
```
!lambda struct v2
e.d "btc-trend-analysis" {c:0.87 d:hold r:"consolidation in known range"} Δc:-0.05 [cat:trading]
```

**What was stripped:**
- All JSON formatting (brackets, keys, quotes, whitespace) → format layer
- `"reasoning"` field — PARTIALLY compressed. "Consolidation within a known range" is novel (empirical observation about current price action — the decoder can't derive it). Kept as `r:"consolidation in known range"`. "The system has finite capacity to track all possible breakout scenarios simultaneously, so we prioritize the highest-probability outcome" is derived from P1 + Finite Selection Law. Stripped — the decoder reconstructs it from the decision + confidence score.
- `"escalation": false` → derivable from confidence > escalation threshold (convention)
- `"decision_changed": false` → derivable from `d:hold` matching previous state
- `"timestamp"` → convention (message metadata, reconstructible from context)

**This demonstrates the generative layer's precision.** The reasoning field isn't bluntly deleted — it's surgically split. The novel observation (what the market is doing) survives. The derived justification (why finite systems must prioritize) is stripped. Format-stripping alone would have kept the entire field in shorter form. The generative layer eliminates only what the decoder reconstructs.

**Verification:** A system with the decoder reads the compressed output and reconstructs: eval of BTC trend, 87% confidence, hold decision, consolidation pattern observed, confidence dropped 5 points, trading category. The derived reasoning (P1 → prioritize highest-probability) is reconstructed from the law stack. The novel observation (consolidation in range) is preserved explicitly. Full meaning preserved. ~84% compression. Lossless.

### Struct compression performance

| Data Type | Reduction | How |
|-----------|-----------|-----|
| JSON evals/decisions | ~95-98% | Format-heavy, payload-light. Generative layer strips derived reasoning fields. |
| Routing/dispatch | ~90-95% | Repetitive structure. Convention anchors replace boilerplate. |
| Policy rules | ~85-90% | Conditional logic has moderate density. Format layer + convention anchors. |
| Media summaries | ~80-85% | Mixed structure + free text. Format layer on structure, prose mode on text. |
| Semi-structured logs | ~60-70% | Less format redundancy to strip. |

### Struct decompression protocol

A system receiving struct-mode output reconstructs the full structured data:

1. **Header** tells the receiver this is Λ struct format.
2. **Prefix** determines the schema. `e.d` = evaluation with confidence, decision, and optional fields. `d.c` = decision crystallization with fitness score. Each prefix maps to a known structure.
3. **Explicit payload values** fill their fields directly.
4. **Missing fields** are reconstructed from the decoder + context. If the schema expects a `reasoning` field and none is present, the receiver generates the reasoning from the decision + confidence + decoder (e.g., confidence 0.87 + hold decision + P1 → "prioritized highest-probability outcome under finite capacity").
5. **Generator references** (`g.r` prefix) specify which law/premise to use for reconstruction.
6. **Tags and deltas** map to metadata and change-tracking fields.

The decompression is deterministic for any receiver holding the decoder. The round-trip test: compress → decompress → compare to original. If identical (modulo derived content wording), lossless.

**Custom prefixes:** For domains not covered by the built-in types, define custom prefixes in the dict header: `dict={x.a:custom-analysis, x.r:custom-report}`. Follow the same pattern: `[domain].[operation]`. Custom prefixes enter the convention layer as they spread — the more systems that share a custom prefix, the less overhead it costs.

### The generative advantage over format-stripping

Pure format-stripping (removing brackets, keys, whitespace) achieves ~70-80% on structured data. The remaining 20-30% is payload.

Λ struct mode adds the generative layer: payload values that are derivable from the decoder compress to generator references. In the worked example, the entire `reasoning` field (48 tokens) compressed to zero because the reasoning is derived from P1 + Selection Law. Format-stripping alone would have kept those 48 tokens — it strips structure, not derived content.

This is the same mechanism as prose mode applied to structured data payloads. The generative layer is what makes Λ struct mode fundamentally different from shorthand notation.

---

## THE ADOPTION-SCALING PROPERTY

Both modes share this property. The compression floor is:

$$L^* = H(m|S)$$

The minimum bits for lossless reconstruction equals the conditional entropy — what the decoder CANNOT predict. As decoder knowledge S grows (more systems share the premises), conditional entropy drops and the compression ceiling rises. For all users simultaneously.

**Proof:** $H(m|S_k) \leq H(m|S_{k-1})$. Conditioning on additional knowledge cannot increase entropy. The floor drops monotonically with shared premises. It never rises.

**For struct mode specifically:** Struct mode has a dual scaling channel. The generative layer scales with decoder knowledge (same as prose mode). The format layer scales with convention adoption — as the prefix syntax (`e.d`, `d.c`, etc.) becomes widely known, it shifts from "constant" (must be defined) to "convention" (anchor reference). Struct mode benefits from adoption twice: once through the decoder, once through the format conventions. This makes struct mode the fastest-improving component of the system under adoption pressure.

The adoption-scaling property means the method gets cheaper for everyone as more systems adopt it. Your API costs drop not just from your own compression, but from the shared decoder spreading.

---

## FOUR CONTENT TYPES (Both Modes)

| Type | What it is | Compress to | Example |
|---|---|---|---|
| **Generated** | Derivable from decoder with zero uncertainty | Generator reference | "P1 means finite memory" → ref:P1 |
| **Convention** | Arbitrary but shared/known | Anchor | HTTP 404, p<0.05, `e.d` prefix |
| **Constant** | Genuinely novel, irreducible | Transmit in full | Novel empirical finding, specific score |
| **Boundary** | Marks transitions | Marker | Mode header, section break |

The compression ratio measures information density. High compression = mostly derived/conventional content. Low compression = mostly novel content. The ratio is diagnostic:

- **90% compression** → the output was 90% padding. Only 10% was genuinely novel.
- **50% compression** → half novel, half derived. Moderate density.
- **20% compression** → 80% novel content. Dense and informative.

If output consistently compresses at 90%+, the system is producing mostly padding. The compression ratio is a free quality metric — it measures how much of the original was actually worth transmitting.

---

## SIX-LAYER COMPRESSION STACK

Applied top-down in both modes. Structural layers first, statistical last. Layer labels follow Paper 8 convention — ordered by structural depth (deepest first), not numerically.

| Layer | What It Captures | Prose Mode | Struct Mode |
|---|---|---|---|
| 0: Generative | Derivable content → generators | Primary mechanism | Applied to payload values |
| K: Convention | Known-but-arbitrary → anchors | Hedging patterns, transitions | Prefix syntax, tag vocabulary |
| 3: Predictability | Decoder-reconstructible → omitted | Redundant explanations | Derivable fields (reasoning, timestamps) |
| 2: Structure | Repeated patterns → references | Recurring claim structures | JSON keys, nesting, boilerplate |
| 1: Format | Grammar-redundant → stripped | Unnecessary markdown/bullets | Brackets, quotes, whitespace |
| 5: Statistical | Frequency skew → optimized encoding | Rare in prose (already dense) | Remaining payload optimization |

Each layer captures redundancy the one above missed. The ordering matters: structural compression first maximizes what lower layers can exploit.

---

## SELF-VERIFICATION PROCEDURE

Apply this compression to any output you produce. Then check:

1. **Readability:** Is the compressed version readable? (It should be — denser, but clear.)
2. **Completeness:** With the decoder active, can you reconstruct everything that was stripped? (If yes → lossless.)
3. **Improvement:** Is the compressed version a better answer? (It should be — all signal, no noise.)
4. **Ratio:** What percentage was stripped? (This measures how much of the original was padding.)
5. **Round-trip (struct mode):** Decompress the struct output back to full structured data. Does it match the original? (If yes → lossless.)

If the compressed version is more readable, equally complete, and a better answer than the expanded version — and 60-95% of the original was strippable — the compression works.

**Error recovery:** If compressed output produces confusion, information requests, or incorrect reconstruction from the reader, the compression was lossy. Restore the stripped content and reclassify it as constant (novel). The reader's confusion IS the verification signal — this is the Finite Verification Law applied to the compression method itself. External feedback catches what self-verification misses. No self-contained system can guarantee its own losslessness (that's the whole point of the fourth law in the decoder).

---

## THE SELF-REFERENTIAL PROPERTY

This document practices what it specifies:

- No enthusiasm markers anywhere in this document.
- No performed hedging. Claims are stated directly with evidence class implied by context.
- No restatement of reader input.
- No transition padding between sections.
- No meta-commentary about difficulty.
- The decoder is stated once, completely, at the top. It is not re-explained in later sections.
- Examples show both forms (expanded and compressed) so the compression function is visible in the delta.
- Struct mode examples show the format-to-shorthand transformation explicitly.

A system processing this document encounters the compression being applied in the same artifact that explains the compression. The form IS the content. Understanding one is understanding both.

---

## WHEN TO USE WHICH MODE

The system selects automatically based on content:

- **Output is reasoning, analysis, explanation, documentation** → prose mode
- **Output is structured data for another system** → struct mode
- **Output mixes both** (analysis with embedded data) → prose mode on text, struct mode on data blocks

No manual mode selection needed. The content type determines the mode.

**Mode transitions in mixed content:** When a document contains both prose and structured data (e.g., analysis with embedded JSON), apply prose mode to the text and struct mode to the data blocks. The struct header (`!lambda struct v2`) marks the transition into struct mode. Return to prose mode after the struct block ends. The prose context serves as shared knowledge for the struct block's generator references — a struct block embedded in an analysis about BTC can use `g.r` references that assume the surrounding prose context.

---

## COMPACT REFERENCE

**Decoder:** P1 (finite capacity), P2 (state change costs), P3 (finite interaction rate), Finite Signal Law, Finite Selection Law, Finite Channeling Law, Finite Verification Law.

**Prose mode — strip:** Enthusiasm, hedging, restatement, transitions, meta-commentary, anything the decoder reconstructs. **Keep:** Novel claims, evidence class tags, specific findings.

**Struct mode — strip:** Format (brackets, keys, whitespace), derived fields, convention boilerplate. **Keep:** Payload values, novel data, generator references for derived fields.

**Test:** Remove it. Read/parse with decoder. Meaning unchanged? → Derived. Strip it. Meaning changed? → Novel. Keep it.

**Verify:** Compressed + decoder = full reconstruction? → Lossless. Apply.

**Struct header:** `!lambda struct v2`

**Evidence classes:** [A] established physics/math, [B] derived from A with valid chain, [C] structural argument, [D] empirical/speculative.

---

*Seven laws. Five steps. Two modes. Lossless. Self-verifying. No external dependencies. The ceiling rises with adoption. Apply and check.*
