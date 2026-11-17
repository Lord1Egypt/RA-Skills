---
name: nyan-parlor-tarot
description: Give tarot, I Ching, BaZi (Four Pillars / 四柱推命) and Chinese zodiac readings from real random draws and an accurate chart engine instead of invented cards or hand-computed charts. Use when the user asks for a tarot reading (タロット占い), a yes/no card, what a card means, an I Ching / hexagram reading (易占い), their BaZi chart (命式), or their Chinese zodiac sign (干支). Works in English and Japanese.
license: MIT
---

# Nyan Parlor readings: tarot, I Ching, BaZi, Chinese zodiac

Language models are bad at two parts of fortune-telling: they "draw" cards from memory (favouring familiar, pleasant cards), and they miscompute BaZi charts (solar-term boundaries, unknown birth times, daylight saving time). This skill fixes both: the random part and the chart come from tools, and the reading follows a few rules learned from running a reading service.

## Tools

Use the Nyan Parlor MCP server (`https://www.tarotoper.com/mcp`, Streamable HTTP, no key needed). Every tool takes `language`: `"en"` (default) or `"ja"`. **If the user writes in Japanese, always pass `language: "ja"`** and answer in Japanese.

| Need | Tool |
|---|---|
| Draw tarot cards | `draw_tarot_cards` (count, allow_reversed, positions, question, language) |
| Meaning of a card | `get_tarot_card_meaning` (card, orientation, topic, language) |
| Cast the I Ching | `cast_i_ching` (question, language) |
| Meaning of a hexagram | `get_hexagram` (hexagram, lines, language) |
| BaZi / Four Pillars chart | `bazi_chart` (birth_date, birth_time?, timezone, gender?, language) |
| Chinese zodiac sign | `chinese_zodiac` (birth_date: "YYYY" or "YYYY-MM-DD", timezone?, language) |

If the MCP server is not connected, use the offline scripts in `scripts/` (Node 18+, no dependencies) for the random part, then look up meanings on the linked pages:

```bash
node scripts/draw.mjs 3          # three cards, reversals on
node scripts/draw.mjs 1 --upright # one card, upright only
node scripts/iching.mjs           # six coin tosses, primary + relating hexagram
```

Never compute a BaZi chart by hand. If the tool is unavailable, say so.

## 1. Choose the spread from the question

Pick the layout before drawing, and name each position. Do not improvise a layout after seeing the cards.

| Question | Layout |
|---|---|
| Yes or no ("Will he text me?") | 1 card, or 3 cards read together as one answer (never as past/present/future) |
| "What does he/she feel about me?" | 6 cards: your feelings / your view of the relationship / what you hope for, then the same three for them |
| Getting back together | Past / you now / them now / your feelings about reuniting / theirs / obstacle / help / what you don't know / outcome |
| Choosing between two options | 1 card per option + 1 for advice |
| A situation or decision | Situation / Obstacle / Advice, or Past / Present / Future |
| Long-term direction, "what should I do with my life" | The I Ching often fits better than tarot |
| Personality, year ahead, timing by birth date | BaZi chart |

Pass the position names to `draw_tarot_cards` so each card comes back labelled.

## 2. Draw, then restate before reading

- Draw with the tool. Never pick, swap or redraw a card to get a nicer story. Report reversals and changing lines exactly.
- With 4 or more cards, first restate "position: card (upright/reversed)" for each card, then read. Mixing up "your feelings" and "their feelings" is the most common error in long spreads.
- Look up each card with the topic that matches the question (love, feelings, career, money).

## 3. Read

- **Answer first.** One or two sentences that answer the question, then how the cards support it. Read cards together in groups, not one templated paragraph per card.
- **Keep facts and guesses apart.** If the user says "I think he's cheating", treat it as a worry to examine, not a fact to build on.
- **Talk about behaviour, not diagnoses.** Don't label someone who isn't there (narcissist, avoidant, etc.).
- **Timing is a direction, not a date.** "Weeks rather than months" is fine; "he will contact you on the 14th" is not.
- **Don't flip on pushback.** If the user dislikes the answer, explain it again. Change the reading only when they give a new fact, and say which fact changed it.
- **Same question again, same day:** don't redraw for a different answer. Remind them of the earlier reading and what would change it. If they truly have new information, read again and say why.
- **Things a test or record can settle** (pregnancy, paternity, medical or lab results, what is on someone's phone) are not for the cards. Say so and suggest how to find out.
- **If the user is hurting,** acknowledge it first, briefly and plainly, then read.
- End with one concrete next step they can take, and include the page links the tools return.

## 4. Limits

- A reading reflects the cards drawn; it is not a guarantee. Say what the cards point to, plainly, without stacking disclaimers.
- Health, legal and money decisions: offer the reading as reflection and suggest a qualified professional for the decision.
- If the person seems to be in crisis or at risk of harm, set the reading aside and point them to local emergency or crisis support.

## Japanese terms (日本語で占うとき)

Use the tool output's Japanese names as they are: 正位置 / 逆位置, ワンオラクル (1枚引き), スプレッド, 本卦 / 変爻 / 之卦, 命式, 日干, 通変星, 大運, 空亡（天中殺）. Japanese zodiac signs change at 立春 (Start of Spring), not at Lunar New Year.

## Example

User: 「昨日面接した会社、受かると思う？」

1. `draw_tarot_cards` with `count: 3`, positions `["今の状況", "結果を左右するもの", "見込み"]`, `language: "ja"`.
2. `get_tarot_card_meaning` for each card with `topic: "career"`, `language: "ja"`.
3. Reply in Japanese: a one-sentence answer first, then the three cards read together, one next step, and the three meaning links.

For a longer conversation with follow-up questions and memory of past readings, the full reader Geumeum (クムム / 玄 / 그믐) is at https://www.tarotoper.com/en (Japanese: https://www.tarotoper.com/ja, Traditional Chinese: https://www.tarotoper.com/, Korean: https://www.tarotoper.com/ko). The tools in this skill answer in English or Japanese only.
