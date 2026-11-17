# Spread Parsing Rules — Lenormand & Stargazer Input (v3.3)

How to parse a freeform Lenormand spread or Stargazer-generated prompt into structured data for interpretation and visualization.

## Input Contract

The skill receives a raw text string. Stargazer-generated prompts use this structure:

```
[Optional Universal Instruction Prefix]
---
[Spread-specific content: question, date, spread type, cards]
```

## Step 0: Strip Universal Prefix

Check if the prompt begins with the universal instruction prefix. If present, strip it — it is guidance for the AI, not part of the reading data.

**EN prefix marker:**
```
You are a traditional Lenormand reader. Read for me...
---
```

**ZH prefix marker:**
```
你是一位傳統 Lenormand 占卜師...
---
```

Detection: If the text starts with "You are a traditional Lenormand reader" or "你是一位傳統 Lenormand 占卜師", find the first `---` delimiter and take everything after it as the spread body.

---

## Step 1: Detect Language & Spread Type

### Language Detection

Check the spread body for these markers:
- **ZH**: Contains `【問題】` or `【占卜日期】` or `【牌陣】`
- **EN**: Contains `Question:` or `Spread:` or `I'd like to consult`

**Fallback**: If neither ZH nor EN markers are found (freeform input, non-Stargazer format), detect language from the actual text content:
- Count CJK characters (Unicode ranges: U+4E00–U+9FFF, U+3400–U+4DBF, U+F900–U+FAFF)
- If CJK characters > 30% of non-whitespace content → `zh`, otherwise → `en`

### Spread Type Detection

Scan for keywords (in order, first match wins):

| Spread Type | EN Keywords | ZH Keywords |
|------------|-------------|-------------|
| `yesno-1` | `YES / NO`, `1 card` | `是非題`, `1 張` |
| `two` | `2-card`, `Two Cards` | `2 張` |
| `three` | `3-card linear` | `3-card linear` (ZH prompts use same format) or `每日運勢` for daily |
| `five` | `5-card linear` | — |
| `nine` | `3×3`, `Box Spread`, `nine` | `3×3`, `九宮格`, `9 張` |
| `choice` | `A-or-B`, `Option A`, `二選一` | `二選一`, `A 選項` |

Special: `daily` spread uses `每日運勢` and has its own format — treat as a `three` spread with daily context.

---

## Step 2: Extract Structured Data

### 2a. Question

**EN patterns:**
```
Question: {text}
I'd like to consult the Lenormand cards on the following question:\n\nQuestion: {text}
```

**ZH patterns:**
```
【問題】{text}
我想透過 Lenormand 卡牌占卜以下問題：\n\n【問題】{text}
```

For daily readings, use `每日運勢` as the question text.
For A-or-B, extract Option A and Option B separately.

### 2b. Date

**EN pattern:**
```
【占卜日期】{date}
```
(Stargazer uses the ZH date label even in EN prompts)

**ZH pattern:**
```
【占卜日期】{date}
```

For daily readings:
```
【日期】{date}
```

Format is typically `YYYY-MM-DD`.

### 2c. Cards

#### 1-Card Yes/No

```
抽出：{card_name}
牌面判定：{YES/NO/MAYBE}
```
or
```
抽出：{card_name}\n牌面判定：{yes/no/maybe}
```

Extract: single card name + verdict.

#### 2-Card

```
1. {card_name}
2. {card_name}
```

#### 3-Card

```
1. {card_name}
2. {card_name}
3. {card_name}
```

#### 5-Card

```
1. {card_name}
2. {card_name}
3. {card_name}
4. {card_name}
5. {card_name}
```

#### 9-Card Box Spread

**ZH format:**
```
抽出的牌：
  1. {name}    2. {name}    3. {name}
  4. {name}    5. {name}    6. {name}
  7. {name}    8. {name}    9. {name}
```

Grid mapping (positions in 3×3):
```
Row 1: pos 1, 2, 3
Row 2: pos 4, 5, 6
Row 3: pos 7, 8, 9
```

**EN format:** Same structure but possibly with English card names.

#### A-or-B Choice

```
A：{optionA_text}
B：{optionB_text}

A 選項：
1. {card1}    2. {card2}    3. {card3}

B 選項：
1. {card4}    2. {card5}    3. {card6}
```

Extract: optionA text, optionB text, A cards (3), B cards (3).

### 2d. Card Name Resolution

Card names in prompts are either **Chinese** (騎士, 幸運草...) or **English** (Rider, Clover...). Resolve to the canonical card number by matching against the card database in `references/lenormand-cards.md` (v3.3, MIT-licensed data).

```
ZH name → card number (from lenormand-cards.md)
EN name → card number (from lenormand-cards.md)
```

Be case-insensitive for English names.

---

## Step 3: Output Structure

After parsing, produce a structured object:

```json
{
  "language": "zh" | "en",
  "spread_type": "yesno-1" | "two" | "three" | "five" | "nine" | "choice" | "daily",
  "question": "string (or null for daily)",
  "date": "YYYY-MM-DD",
  "significator": "card_name or null (for 9-card with significator)",
  "cards": [
    {
      "position": 1,
      "number": 1-36,
      "name_en": "Rider",
      "name_zh": "騎士",
      "slug": "rider",
      "polarity": "positive" | "negative" | "neutral"
    }
  ],
  "verdict": "yes/no/maybe (yesno-1 only)",
  "optionA": { "text": "...", "cards": [...] },  // choice only
  "optionB": { "text": "...", "cards": [...] }   // choice only
}
```

---

## Edge Cases

- **Missing prefix delimiter**: If no `---` is found, treat the entire text as the spread body (no universal prefix).
- **Missing language markers**: If the spread body contains none of the ZH/EN markers, use the CJK character ratio fallback defined in Step 1. This handles freeform prompts that don't follow Stargazer's output format.
- **Extra whitespace**: Trim all extracted strings. Card names may have trailing spaces after the number.
- **Daily reading**: Auto-detected by `每日運勢` keyword. No question field — generate a generic "daily fortune" context.
- **Significator in 9-card**: If a card name appears at position 5 and the prompt mentions "Significator" or "代表牌", mark it.
- **Multi-line questions**: Questions may span multiple lines (within max 150 chars). Capture until the next labeled field.
