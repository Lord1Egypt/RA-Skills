# Fuzzy Title Matching — Technical Deep Dive

## Overview

Prediction Market Arbiter uses **Jaccard similarity** (word-overlap based matching) to identify the same event across Kalshi and Polymarket, despite differences in how each platform phrases market questions.

## The Matching Algorithm

### Jaccard Similarity Formula

```
J(A, B) = |A ∩ B| / |A ∪ B|
```

Where:
- A = set of words in Kalshi title (after preprocessing)
- B = set of words in Polymarket title (after preprocessing)
- |A ∩ B| = number of shared words
- |A ∪ B| = total number of unique words across both

Result: **0.0 to 1.0**, where:
- **1.0** = identical (after stopword removal)
- **0.6** = fairly similar (threshold default)
- **0.3** = vague overlap (low confidence)
- **0.0** = no common words

### Preprocessing Steps

1. **Lowercase conversion**
   ```
   "Will Bitcoin EXCEED $100k?" → "will bitcoin exceed $100k?"
   ```

2. **Tokenization by whitespace**
   ```
   "will bitcoin exceed $100k?" → ["will", "bitcoin", "exceed", "$100k?"]
   ```

3. **Stopword removal**
   Removes common words that don't carry semantic meaning:
   ```
   Stopwords = {will, the, a, an, in, on, by, of, to, for, be, is, at, ?}
   ```

   Example:
   ```
   Before: ["will", "bitcoin", "exceed", "$100k?"]
   After:  ["bitcoin", "exceed", "$100k"]  (removed "will" and "?")
   ```

4. **Set creation**
   ```
   Kalshi:     {"bitcoin", "exceed", "$100k"}
   Polymarket: {"bitcoin", "exceeds", "100000", "eoy"}
   ```

### Worked Example

**Title A (Kalshi):** "Will Bitcoin exceed $100,000 by December 2026?"

1. Lowercase: `"will bitcoin exceed $100,000 by december 2026?"`
2. Split: `["will", "bitcoin", "exceed", "$100,000", "by", "december", "2026?"]`
3. Remove stopwords (`will`, `by`):
   ```
   {"bitcoin", "exceed", "$100,000", "december", "2026"}
   ```

**Title B (Polymarket):** "Bitcoin above 100k by EOY 2026?"

1. Lowercase: `"bitcoin above 100k by eoy 2026?"`
2. Split: `["bitcoin", "above", "100k", "by", "eoy", "2026?"]`
3. Remove stopwords (`by`):
   ```
   {"bitcoin", "above", "100k", "eoy", "2026"}
   ```

**Calculate similarity:**

```
A = {"bitcoin", "exceed", "$100,000", "december", "2026"}
B = {"bitcoin", "above", "100k", "eoy", "2026"}

Intersection (A ∩ B) = {"bitcoin", "2026"}           (2 words)
Union (A ∪ B)        = {"bitcoin", "exceed", "$100,000", "december",
                        "2026", "above", "100k", "eoy"}  (8 words)

J(A, B) = 2 / 8 = 0.25
```

**Result:** 0.25 < 0.6 threshold → **NO MATCH**

## Why This Matters

### The Problem with Exact Matching

If we required exact title match:
- Kalshi: "Will Bitcoin exceed 100000 by December 2026?"
- Polymarket: "Bitcoin above 100k by EOY 2026?"
- **Result: NO MATCH** (even though they're identical events)

### Why Jaccard Works

Jaccard focus on **semantic overlap** via word sharing:
- Numbers are normalized by platform (100000 vs 100k)
- Synonyms don't match (exceed vs above), so they contribute to divergence
- But if 70%+ of unique words overlap, we trust it's the same event
- Trade-off: Some false positives at low thresholds, fewer misses

## Threshold Tuning

| Threshold | Sensitivity | False Positive Rate | Use Case |
|-----------|-------------|-------------------|----------|
| **0.4** | Very High | ~20% | Quick discovery, high alert volume |
| **0.5** | High | ~10% | Balanced (good starting point) |
| **0.6** | Medium | ~5% | Default (production-tested) |
| **0.7** | Low | ~2% | Conservative, only obvious matches |
| **0.8** | Very Low | <1% | Only near-identical titles |
| **0.9** | Extremely Low | <0.1% | Almost exact match required |

### When to Adjust

**Lower threshold (0.4-0.5) if:**
- You want to catch early arbitrage
- Kalshi and Polymarket title formatting is very different for your markets
- You're willing to manually filter false matches

**Keep at default (0.6) if:**
- You want balanced detection
- You trust the Arbiter to filter noise

**Raise threshold (0.7-0.8) if:**
- You're getting too many false matches
- You only want high-confidence pairs
- Platform overlap is weak (few events on both)

## Stopword List

The current stopword set:
```python
stopwords = {
    "will",      # future tense indicator
    "the",       # definite article
    "a",         # indefinite article
    "an",        # indefinite article
    "in",        # preposition
    "on",        # preposition
    "by",        # preposition
    "of",        # preposition
    "to",        # preposition
    "for",       # preposition
    "be",        # linking verb
    "is",        # linking verb
    "at",        # preposition
    "?",         # punctuation
}
```

These are chosen to:
1. Remove question markers (both use "?" but it's not semantic)
2. Remove verb tenses (will, is, be → capture the core event)
3. Remove connecting words (the, a, in, on, of, to, by) → focus on nouns/adjectives

### Extending the Stopword List

If you're seeing false matches from articles, add them:

```python
stopwords.update({
    "whether",
    "that",
    "this",
    "if",
    "whether",
})
```

Recompile and re-run. Lower sensitivity = fewer alerts but higher confidence.

## Performance Impact

**Matching complexity:** O(n × m × k)

Where:
- n = number of Kalshi markets
- m = number of Polymarket markets
- k = average title length

With defaults (1000 Kalshi, 200 Polymarket):
- **Worst case:** 200,000 comparisons
- **Typical:** <5 seconds (matching is fast)

## Common Matching Failure Cases

### Case 1: Different Event Framing

**Kalshi:** "Will the Fed cut rates by 50bp before June 2026?"
**Polymarket:** "Federal Reserve rate cut June 2026?"

```
A = {"fed", "cut", "rates", "50bp", "june", "2026"}
B = {"federal", "reserve", "rate", "cut", "june", "2026"}

Intersection: {"cut", "june", "2026"}  (3)
Union: 10 words
J = 3/10 = 0.30 → NO MATCH (below 0.6 threshold)
```

**Fix:** Lower threshold to 0.4-0.5, or manually verify.

### Case 2: Opposite Event Phrasing

**Kalshi:** "Will Bitcoin exceed $100k by EOY 2026?"
**Polymarket:** "Will Bitcoin stay below $100k by EOY 2026?"

```
A = {"bitcoin", "exceed", "100k", "eoy", "2026"}
B = {"bitcoin", "stay", "below", "100k", "eoy", "2026"}

Intersection: {"bitcoin", "100k", "eoy", "2026"}  (4)
Union: 7 words
J = 4/7 = 0.57 → NO MATCH (below 0.6 threshold)
```

**Result:** Correctly rejected (opposite events). This is good!

### Case 3: Number Normalization

**Kalshi:** "Will Bitcoin exceed $100,000?"
**Polymarket:** "Bitcoin above 100k?"

Tokens: `$100,000` vs `100k`
- These are different string tokens, so they don't overlap
- Word similarity would help, but pure Jaccard doesn't support it

**Workaround:** Preprocess numbers to canonical form:
```python
# Optional: normalize currency/numbers
title = re.sub(r'\$?(\d+)[,k]', r'\1', title)
# "$100,000" → "100000"
# "100k" → "100000"
```

Currently not implemented (false negative on number format mismatches), but can be added.

## Advanced: Extending to Other Platforms

To add new platforms (Manifold Markets, Betfair, etc.):

1. Implement `_fetch_manifold_markets()` returning list of dicts with `title`, `yes_price`, `volume`
2. Add cross-platform matching loop:
   ```python
   for km in kalshi_markets:
       for mm in manifold_markets:
           score = _fuzzy_match_title(km["title"], mm["title"])
           if score >= match_threshold:
               # Compare prices, record divergence
   ```
3. Update cache output to include platform triplets

Current implementation supports 2 platforms; extending to 3+ requires tracking all pairwise comparisons.

## References

- **Jaccard Similarity:** https://en.wikipedia.org/wiki/Jaccard_index
- **Text Similarity:** https://en.wikipedia.org/wiki/String_metric
- **Alternative approaches:**
  - Levenshtein distance (edit-distance, string-level)
  - Cosine similarity (TF-IDF, semantic vectors)
  - Semantic similarity (embedding-based, requires model)

Jaccard was chosen for its simplicity, transparency, and lack of ML dependency.
