# Text Pipeline: Stages 1-4

This file is loaded when `modality = text`. Execute stages in order.

---

## Stage 1: Existing Fact-Check Lookup (Optional)

Check if this claim has already been fact-checked by established organizations.

1. Check if the Google Fact Check API key is available:
   ```bash
   echo "${GOOGLE_FACTCHECK_API_KEY:-}"
   ```

2. **If the key is set (non-empty)**, query the API:
   ```bash
   curl -s -G "https://factchecktools.googleapis.com/v1alpha1/claims:search" \
     --data-urlencode "query=<FIRST 200 CHARACTERS OF INPUT TEXT>" \
     -d "languageCode=<LANGUAGE>" \
     -d "pageSize=10" \
     -d "key=$GOOGLE_FACTCHECK_API_KEY"
   ```

3. Parse the JSON response. For each entry in `claims[].claimReview[]`, record:
   - `text`: the claim
   - `existing_verdict`: the `textualRating`
   - `source`: the `publisher.name`
   - `url`: the review URL

4. **If the key is not set**, skip this stage silently.

---

## Stage 2: Claim Extraction

Decompose the input text into atomic, independently verifiable factual claims.

### Rules
- Each claim MUST be a **complete sentence** containing specific names, numbers, dates, or events.
- **Ignore**: opinions, subjective evaluations, predictions, vague statements, and hedged language.
- Output claims as a numbered list in the same language as the input.
- Claim limit by input length:
  - Short text (< 200 words): max **3** claims
  - Medium text (200-1000 words): max **5** claims
  - Long text (> 1000 words): max **10** claims
- Prioritize by:
  1. Claims with specific numbers, dates, or statistics (most verifiable)
  2. Claims about named individuals or organizations
  3. Claims about events with definite outcomes
  4. Drop generic, widely-known, or low-stakes claims first

### If no verifiable claims are found:
Skip to Report Generation and output the "No verifiable claims" template from the main SKILL.md.

---

## Stage 3: Claim Triage

For each claim from Stage 2, determine if it is **check-worthy**.

### Decision criteria:
- **Proceed**: The claim makes a specific, falsifiable assertion about a real event, person, organization, or statistic.
- **Skip**: The claim is a general truism, common knowledge, an opinion disguised as fact, or too vague to verify.

### Default: when in doubt, **proceed**.

Mark each claim as `proceed` or `skip` with a brief reason.

---

## Stage 4: Deep Verification

For each claim marked `proceed`:

### Step 1: Search for evidence

**搜索策略（严格按此顺序执行）：**

1. **第一次搜索**：用用户的原始语言构建查询词，搜索一次。
2. **第二次搜索（必做）**：将核心关键词翻译成英文，用英文再搜索一次。即使第一次搜索已经找到结果，仍然必须做英文 cross-check，因为英文新闻覆盖面最广，且包含 Reuters、AP、BBC、Al Jazeera 等国际权威消息源。如果用户本身就是英文输入，则第二次搜索换一组英文关键词。
3. **综合两次搜索结果**判定 verdict。如果两次搜索均无有效结果，标记为 UNVERIFIED。

示例：
- 用户输入："伊朗今天说要打击美以的银行"
- 第一次搜索（中文）：`伊朗 打击 美国 以色列 银行 2026`
- 第二次搜索（英文，必做）：`Iran target US Israel banks economic interests March 2026`

⚠️ 英文 cross-check 不可跳过。即使中文搜索已找到来源，英文搜索往往能补充国际视角和更权威的消息源，显著提升 verdict 的置信度。

- If WebSearch fails entirely (tool not available), tell the user:
  > Fact-checking requires web search. Please set up Brave Search (free, ~1 minute):
  > 1. Go to https://brave.com/search/api/ and create a free account
  > 2. Generate an API key (free plan = 1,000 searches/month)
  > 3. Set `BRAVE_SEARCH_API_KEY` in your OpenClaw config, then retry.
  >
  > 中文：事实核查需要网络搜索。请访问 https://brave.com/search/api/ 注册免费账号，获取 API Key，配置到 OpenClaw 后重试。

  Do NOT proceed without web search — there is no fallback for text verification.

### Step 2: Analyze evidence
- Review search result titles, snippets, and URLs.
- If a result looks highly relevant but the snippet is insufficient, use **WebFetch** to read the full page.
- Consider source credibility: official government sites, major news outlets, academic sources, and established fact-checkers are more reliable than blogs or social media.
- **必须记录每条证据的来源 URL。** 在报告中，每条论据必须附上对应的来源链接。格式为 `[来源名称](URL)`。如果 WebSearch 结果中有 URL，必须记录下来并在报告中使用。不要只写来源名称（如 "Reuters 报道"）而省略链接。这是强制要求，不是可选项。

### Step 3: Determine verdict

| Verdict | When to use |
|---------|-------------|
| **TRUE** | Multiple credible sources confirm the claim |
| **FALSE** | Multiple credible sources directly contradict the claim |
| **PARTIALLY_TRUE** | Contains some truth but is misleading, exaggerated, or missing context |
| **MISLEADING** | Technically accurate but creates a false impression |
| **UNVERIFIED** | Insufficient evidence to confirm or deny |

### Step 4: Assign confidence
Use the Confidence Framework from the main SKILL.md.

### Step 5: Record for each claim
- `id`: claim_001, claim_002, etc.
- `text`: the claim text
- `verdict`: one of the five verdicts
- `confidence`: 0-100
- `explanation`: 1-2 sentence summary of evidence and reasoning
- `sources`: list of URLs used as evidence

---

## Report Template (English)

```
# Fact-Check Report

### claim_001: [VERDICT] (Confidence: [SCORE]%)
> [claim text]

**Evidence:**
1. [evidence point 1] — [Source Name](url1)
2. [evidence point 2] — [Source Name](url2)
```

## Report Template (中文)

**当用户使用中文时，必须使用此模板。标题、标签、verdict 全部使用中文，不得混用英文。**

```
# 事实核查报告

### 声明一：[判定]（置信度：[分数]%）
> [声明内容]

**证据：**
1. [论据 1] — [来源名称](url1)
2. [论据 2] — [来源名称](url2)
```
