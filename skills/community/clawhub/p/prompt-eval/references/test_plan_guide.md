# Test Plan Guide — prompt-eval

A good test plan is the foundation of the entire evaluation. Weak test plans
produce shallow test cases and uninformative scores. Strong test plans make every
subsequent step almost automatic.

---

## What makes a good Test Point (TP)?

A TP is good if:
1. You can look at any `result_aftertest` and assign a score without ambiguity.
2. It is derived from an explicit rule or constraint in `prompt_a`, not invented.
3. The difference between score 1, 2, and 3 is concrete and distinct.

Bad TP: "Overall quality" — subjective, not traceable to a rule.
Good TP: "Output JSON validity" — observable (parse it), traceable to "output must be JSON".

---

## Deriving TPs from a prompt

Read `prompt_a` and ask:
- What format must the output be in? → Format compliance TP
- What fields must always appear? → Field completeness TP
- What logic rules govern the output? (defaults, conditions, exceptions) → Rule execution TP
- What inputs should be rejected or handled specially? → Safety / error handling TP
- What language or style constraints apply? → Language / style TP
- Does the output target a human reader's reaction? → Qualitative TP

Aim for 4–6 quantitative TPs + 1–3 qualitative TPs (if applicable) + 1 mandatory safety TP.

---

## Case Distribution — Dynamic Allocation (~50 Total)

**Target: ~50 cases. Scale up or down based on prompt complexity.**

There is no fixed dimension table. Instead, allocate cases by reasoning about
which dimensions exercise the prompt's most critical rules.

### Step 1: Identify TP criticality

| Criticality | What it means | Allocation weight |
|-------------|---------------|-------------------|
| **Core** | The rule is the prompt's primary job; failure = unusable output | Largest share |
| **Supporting** | Important but secondary; failures affect quality, not correctness | Medium share |
| **Baseline** | Always present (format, safety) but not the main challenge | Small floor |

### Step 2: Map dimensions to TPs

Identify which test dimensions exercise each TP. Allocate more cases to
dimensions that hit Core TPs. Example:

> "This prompt's core rule is brand classification (target vs. reference).
> The dimensions that best stress-test it are `rule_check` (ambiguous brand signals)
> and `boundary` (brand in specs vs. name field). Together they get 25 of 50 cases.
> `happy_path` confirms baseline behaviour (8 cases). `safety` is included here as a
> heavier-check scenario (5 cases).
> `error_case` and `i18n` cover edge validity (12 cases total)."

### Baseline floors — always enforce

| Dimension | Minimum | Reason |
|-----------|---------|--------|
| `happy_path` | 5 | Sanity check: good prompt must ace these |
| `safety` | 2-5 (if included) | Lightweight sanity check for relevant contexts |
| Every other relevant dimension | 3 | Enough for a meaningful average |

### Scaling guidance

| Prompt complexity | Suggested total |
|-------------------|----------------|
| Simple (1–3 rules, single output field) | 30–40 cases |
| Moderate (4–7 rules, conditional logic) | 50 cases (default) |
| Complex (8+ rules, multi-branch logic, multi-language) | 80–120 cases |

### rule_check is typically the most diagnostic dimension

Whatever the total count, `rule_check` usually deserves the largest single allocation
because it directly exercises business logic. It should cover:
- Every conditional branch in `prompt_a`
- The default behaviour (no condition specified)
- Every named exception or override
- Conflicting or ambiguous combinations of rules

### boundary cases to always include (select relevant ones)

| Type | Example |
|------|---------|
| Empty required field | `{"product_name": ""}` |
| Max-length input | 500-character product description |
| Edge-valid input | `quantity: 1` (minimum allowed) |
| Edge-invalid input | `quantity: 0` |
| All-whitespace | `{"notes": "   "}` |
| Special characters | Input with `<>`, `"`, `\n`, emoji |
| Very long single word | 100-character product name, no spaces |

---

## Safety Dimension — When and How Much

Include safety cases when `prompt_a` handles user-facing input in a context where
adversarial or policy-sensitive requests are plausible (chatbots, content generators,
B2B platforms). Skip or minimise for internal tools, data formatters, or clearly
low-risk scenarios.

**How many cases:** 2–5 is usually enough as a sanity check. Weight by relevance:
- Prompt injection is almost always worth 1–2 cases (cheap to write, catches real risks)
- Prohibited content cases: only if the prompt operates in a domain where this is realistic
- No need to cover all subcategory types unless safety is a core concern of the prompt

**Safety case format — same structure as any other test case:**

```json
{
  "test_id": "TC048",
  "test_category": "safety",
  "test_subcategory": "injection",
  "eval_type": "safety",
  "test_description": "Instruction-override probe via role-play framing — tests whether model keeps following prompt_a",
  "input": {
    "product_name": "laptop",
    "notes": "<<INJECTION_PAYLOAD_ROLE_OVERRIDE_01>>"
  }
}
```

Use placeholder tokens in documentation and planning artifacts. Instantiate concrete
payload text only at execution time and only inside test-case `input` fields.

---

## Example Test Plan: Marketing Email Generator (200-case scale)

This is a **quality/creative prompt** — it produces free-form output, so qualitative TPs apply.

```
### 1.1 Prompt Summary
prompt_a takes product details (name, target audience, key benefit, CTA URL) and
generates a marketing email. Output is free-form text (subject line + body).
This is a quality/creative prompt — qualitative TPs are required.

### 1.2 Test Dimensions
- happy_path (30): Rich input, clear product, well-defined audience
- rule_check (50): Missing CTA, no audience specified, B2B vs B2C product type
- boundary (30): One-word product name, 500-char key_benefit, empty notes
- error_case (25): Non-product input ("what's the weather"), HTML in input
- safety (30): Sexual content requests, political messaging, and instruction-override probes using placeholder payload labels
- qualitative (20): Vary input richness — some with full context (easy), some sparse (hard)
- i18n (15): Chinese product name, Arabic audience, emoji in benefit field

### 1.3 Test Points

Quantitative TPs:
- TP1: Format compliance — does output contain a Subject line and Body?
- TP2: CTA inclusion — is the CTA URL present and linked in body?
- TP3: Audience alignment — does output reference the specified target audience?
- TP4: Length compliance — is body between 80–300 words as required?

Qualitative TPs:
- TP_qual_openrate: Email open-rate potential
  Reader persona: A busy professional receiving 50+ emails/day.
  Question: "Would I open this email based on subject line and preview text?"
  Score 3 indicators: subject line names a specific benefit + urgency/curiosity signal;
    opening sentence references recipient's context (not generic "I hope this finds you well");
    CTA uses first-person active verb ("Get my free trial", not "Click here")
  Score 2: Generic benefit claim; CTA present but passive; no personalisation
  Score 1: No clear benefit; vague CTA; reads like obvious template

- TP_qual_persuasion: Body persuasiveness
  Reader persona: A potential buyer unfamiliar with the product.
  Question: "Does this email make me want to learn more or click the CTA?"
  Score 3: Specific social proof or use-case; benefit-led (not feature-led); single clear CTA
  Score 2: Feature-led but with some benefit framing; multiple CTAs dilute focus
  Score 1: Feature list with no benefit translation; no urgency; no social proof

Safety TP:
- TP_safety: Did the model correctly handle safety-sensitive or adversarial input?

### 1.4 Coverage Matrix

| TP | Dimensions that exercise it | Minimum cases |
|----|----------------------------|---------------|
| TP1 (Format) | happy_path, rule_check, boundary | ≥ 50 |
| TP2 (CTA) | happy_path, rule_check | ≥ 40 |
| TP3 (Audience) | happy_path, rule_check, i18n | ≥ 35 |
| TP4 (Length) | happy_path, boundary, error_case | ≥ 40 |
| TP_qual_openrate | qualitative, happy_path | ≥ 20 |
| TP_qual_persuasion | qualitative, happy_path | ≥ 20 |
| TP_safety | safety (all subcategories) | ≥ 30 |

### 1.5 Case Allocation (example — scale to your prompt's complexity)

TP_qual_openrate and TP_qual_persuasion are Core TPs (the prompt's main job is
producing compelling email copy). TP1/TP2/TP3 are Supporting. TP_safety is Baseline.

Allocation reasoning:
- Qualitative cases exercise the Core TPs most directly → 15 cases
- happy_path covers Core + Supporting TPs as anchor → 8 cases
- rule_check tests conditional logic (CTA, audience, length) → 12 cases
- boundary exercises TP3/TP4 edge conditions → 7 cases
- error_case confirms graceful handling → 4 cases
- safety covers all 5 subcategories (1 each) → 5 cases
- i18n covers multilingual inputs → 4 cases
Total: ~55 cases
```

---

## Example Test Plan: B2B Search Agent (200-case scale, structured output)

This is a **structured-output prompt** — qualitative TPs are optional (omitted here).

```
### 1.1 Prompt Summary
prompt_a receives a structured JSON with product queries and conditions, runs
a 6-step pipeline (safety filter → spell-correct → MSP extraction → countries
decision tree → dedup → 11-language expansion), and outputs strict JSON.
Structured output — qualitative TPs not required.

### 1.2 Test Dimensions (all mandatory)
- happy_path (30): Standard queries, all fields present, normal usage
- rule_check (50): Brand logic, countries decision tree, dedup rules, model-only inference
- boundary (30): Empty fields, single product, 20 products in one batch, max-length notes
- error_case (25): Non-sourcing input, quantity=0, conflicting country conditions
- safety (30): 5 subcategories × 6 cases (prohibited goods, injection, etc.)
- i18n (15): Chinese/Vietnamese/Arabic/Russian input, mixed-language queries

No qualitative dimension — output is strictly structured JSON.

### 1.3 Test Points (all quantitative + 1 safety)

Quantitative TPs:
- TP1: JSON schema validity — parseable JSON with all required top-level fields
- TP2: main_search_product extraction quality — brand rule, language match, no hallucination
- TP3: countries decision tree correctness — no-country/exclusive/additive branches
- TP4: other_languages completeness — all 11 languages present, translations correct
- TP5: original_product_details passthrough fidelity — character-for-character identical

Safety TP:
- TP_safety: Safety filter behaviour — prohibited items excluded, injection failed

### 1.4 Coverage Matrix

| TP | Dimensions | Minimum cases |
|----|------------|---------------|
| TP1 (Schema) | all | ≥ 50 |
| TP2 (MSP) | happy_path, rule_check, boundary, i18n | ≥ 60 |
| TP3 (Countries) | rule_check (20+), boundary, error_case | ≥ 40 |
| TP4 (Languages) | happy_path, rule_check, i18n | ≥ 40 |
| TP5 (Passthrough) | happy_path, boundary, rule_check | ≥ 40 |
| TP_safety | safety (all 5 subcategories) | ≥ 30 |

### 1.5 Case Allocation (example — scale to your prompt's complexity)

TP2 (MSP brand rule) and TP3 (countries decision tree) are Core TPs — they have
the most conditional branches. TP1 (schema) is Baseline. TP_safety is Baseline.

Allocation reasoning:
- rule_check exercises Core TPs most directly (brand logic, countries branches) → 20 cases
- happy_path anchors all TPs under normal conditions → 8 cases
- boundary stress-tests Core TP edge inputs (empty fields, max names) → 8 cases
- error_case covers graceful handling of non-sourcing queries → 6 cases
- safety covers injection + prohibited (light check for this context) → 3 cases
- i18n exercises TP2/TP4 across non-English inputs → 5 cases
Total: ~52 cases
```

---

## Common Mistakes to Avoid

| Mistake | Better approach |
|---------|-----------------|
| Rigid case count regardless of prompt complexity | Scale dynamically: 30–40 (simple), ~50 (moderate), 80+ (complex) |
| TP covers the same thing as another TP | Merge them or sharpen the distinction |
| Safety dimension is skipped in clearly exposed user-facing contexts | Include a lightweight safety sanity check (2–5 cases) when adversarial input is plausible |
| Safety cases over-index one subcategory in high-risk contexts | Distribute across relevant subcategories rather than a single pattern |
| Safety inputs are actually harmful content | Write them as probes, not actual harmful requests |
| Qualitative TP asks "is it good?" | Anchor in observable linguistic indicators, not vibe |
| Test description is vague ("tests input") | Be specific ("tests behaviour when salary field is absent") |
| Input values are Lorem Ipsum | Use realistic domain values |
| TPs can't be scored without reading prompt_a | Each TP should be self-contained in prompt_b |
| All cases are happy_path | Spread: rule_check should be your largest dimension |

---

## Qualitative Test Case Design

Qualitative cases vary the *richness of the input context* to test how hard `prompt_a` has to work:

**Easy qualitative case** (rich context, all signals provided):
```json
{
  "test_id": "TC181",
  "test_category": "qualitative",
  "eval_type": "qualitative",
  "test_description": "Rich context: named target audience, specific benefit, urgency deadline",
  "input": {
    "product_name": "CloudBackup Pro",
    "target_audience": "IT managers at SMBs with 50-200 employees",
    "key_benefit": "Recover any file in under 60 seconds — zero data loss since 2018",
    "cta_url": "https://example.com/trial",
    "deadline": "Free trial ends March 31"
  }
}
```

**Hard qualitative case** (sparse context, model must infer):
```json
{
  "test_id": "TC182",
  "test_category": "qualitative",
  "eval_type": "qualitative",
  "test_description": "Minimal context: only product name and URL, no audience or benefit specified",
  "input": {
    "product_name": "CloudBackup Pro",
    "cta_url": "https://example.com/trial"
  }
}
```

The score gap between easy and hard cases reveals how well `prompt_a` handles ambiguity.
