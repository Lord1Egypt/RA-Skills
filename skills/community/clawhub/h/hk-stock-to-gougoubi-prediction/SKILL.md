---
name: hk-stock-to-gougoubi-prediction
description: Turn Hong Kong stock research into Gougoubi-ready prediction proposals with deterministic market wording, deadline selection, resolution rules, and tags. Use when users want to analyze 港股 and publish or prepare a Gougoubi prediction market from the result.
metadata: {"clawdbot":{"emoji":"🏦","os":["darwin","linux","win32"]}}
---

# HK Stock To Gougoubi Prediction

Use `hk-stock-predictor` to generate prediction candidates, then convert the best candidate into a Gougoubi-ready proposal and pass it to `gougoubi-create-prediction`.

## Minimal Input

```json
{
  "symbol": "00700",
  "horizon": "30d"
}
```

Theme-first input is also valid:

```json
{
  "theme": "南向资金持续流入的港股通互联网龙头",
  "horizon": "14d"
}
```

## Required Subskills

Use these skills in order:

1. `hk-stock-predictor`
2. `gougoubi-create-prediction`

If `hk-stock-predictor` is missing, do not continue to market creation. Ask the agent to perform the HK stock analysis workflow first.

## Deterministic Workflow

1. Analyze the HK stock or theme.
   - Run the `hk-stock-predictor` workflow.
   - Collect `predictionCandidates` and `recommendedPrediction`.
2. Pick one prediction candidate.
   - Prefer the recommended candidate unless it violates the filters below.
3. Validate prediction quality.
   - Must be binary, range, event, or relative-performance.
   - Must have a concrete deadline.
   - Must have a public resolution source.
   - Must not rely on subjective judgment.
4. Convert to Gougoubi proposal fields.
   - `marketName`
   - `deadlineIsoUtc`
   - `rules`
   - `tags`
5. Pass the resulting market to `gougoubi-create-prediction`.
   - Minimal required user-facing fields remain `marketName` and `deadlineIsoUtc`.
   - The rest of the content should be generated deterministically from the chosen prediction.
6. Return both layers of output.
   - analysis summary
   - chosen prediction
   - Gougoubi payload
   - create transaction result if submission is requested

## Market Filters

Only create markets that satisfy all of these:

- time-bounded
- externally resolvable
- single thesis, not multiple stacked conditions
- sufficiently liquid underlying or high-quality event source
- wording is concise and non-ambiguous

Do not create markets for:

- micro-cap or illiquid names likely to be manipulated
- vague sentiment questions
- open-ended macro narratives without a measurable threshold
- markets that cannot be resolved from a public page or published report

## Gougoubi Conversion Rules

### 1. `marketName`

Use a short title with one measurable claim.

Good:

- `Will 00700 close above HK$520 on 2026-04-30?`
- `Will 09988 outperform HSTECH between now and 2026-05-15?`
- `Will 02318 report YoY net profit growth above 10% in its next earnings release?`

### 2. `deadlineIsoUtc`

Choose the earliest deadline that still allows clean resolution:

- close-price market: use market close date plus a short safety buffer
- earnings market: use expected report date plus a safety buffer
- relative-performance market: end date at the comparison window close

Default timezone for rules: `Asia/Hong_Kong`, unless the data source clearly reports in another timezone.

### 3. `rules`

Rules must explicitly define:

- resolution source
- metric field
- comparison operator
- timezone
- tie handling
- fallback source if primary source is temporarily unavailable

Use this template:

```markdown
Resolution source:
- Primary: [source]
- Fallback: [fallback source]

Resolution rule:
- This market resolves YES if [exact measurable condition].
- This market resolves NO otherwise.

Measurement details:
- Timezone: Asia/Hong_Kong
- Observation time: [exact time or reporting event]
- Metric: [close price / YoY growth / index-relative return / etc.]
- Tie handling: equality resolves [YES or NO], as stated in market title interpretation.
```

### 4. `tags`

Always include:

- `hong-kong-stocks`
- one sector tag
- one catalyst tag
- one horizon tag
- when possible, align with project-known category ids such as `finance`, `earnings`, and `tech`

Examples:

- `hong-kong-stocks`
- `finance`
- `internet`
- `earnings`
- `30d`

## Output Schema

```json
{
  "ok": true,
  "analysis": {
    "symbol": "00700",
    "companyName": "Tencent Holdings",
    "recommendedPrediction": {
      "title": "",
      "deadlineIsoUtc": "",
      "confidence": 0
    }
  },
  "gougoubiPayload": {
    "marketName": "",
    "deadlineIsoUtc": "",
    "rules": "",
    "tags": []
  },
  "createInput": {
    "marketName": "",
    "deadlineIsoUtc": ""
  },
  "createResult": null,
  "warnings": []
}
```

## Response Format

```markdown
# 港股到 Gougoubi 预测题

## 标的结论
- 标的:
- 核心判断:
- 时间窗口:

## 选中的预测题
- 题目:
- 截止时间:
- 置信度:
- 公开裁决来源:

## Gougoubi 参数
- marketName:
- deadlineIsoUtc:
- tags:

## 规则草案
[rules text]

## 提交结果
- status:
- txHash:
- proposalAddress:
```

## Boundaries

- Do not submit on-chain or through the UI unless the user clearly wants actual creation.
- If only asked for preparation, stop after generating the Gougoubi-ready payload.
- Surface uncertainty if earnings date or source availability is unclear.
- Prefer event-driven or close-price markets over loose valuation narratives.

## Additional Resource

- For a concrete Tencent example, see [examples.md](examples.md).
