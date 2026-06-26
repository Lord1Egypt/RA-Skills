# Voice Fingerprint Reference

Read the JSON output from `scripts/analyze_voice.py` and translate each metric into concrete writing constraints. This file tells you how to interpret the numbers.

## Sentence stats

| Metric | What it means | How to imitate |
|--------|---------------|----------------|
| `mean_words` | Average sentence length | Hit within ±10% over a 200-word draft |
| `burstiness` | sd/mean of sentence lengths. >0.6 = very human, <0.3 = AI metronome | Mix 2-word fragments with 30-word runs |
| `fragment_share` | Share of sentences ≤5 words | Use that many one-punchers. They land. Like this. |
| `long_sentence_share` | Share ≥25 words | Match it -- a long sentence is permission to chain three clauses with dashes, riff a bit, and only then land the period |
| `stdev_words` | Variation around the mean | If stdev > mean × 0.6, the author swings hard between short and long. Imitate the swing |

If the author's burstiness is >0.6, never write three sentences in a row of similar length. Vary deliberately.

## Vocab

| Metric | Imitation rule |
|--------|----------------|
| `type_token_ratio` | 0.4-0.5 is normal humans. <0.4 = repetitive (match it -- repeat key nouns instead of synonym-cycling). >0.6 = wide vocabulary (vary more) |
| `top_content_words` | These are the author's anchor words. Reuse them. Do NOT replace with synonyms |
| `profanity_per_1k_words` | If >2, profanity is part of the voice -- omitting it sounds fake. Match the rate, don't dilute or inflate |
| `ai_filler_hits` | Should be near zero in human text. If you're tempted to write "leverage" or "delve," stop |
| `hedge_hits` | Low = confident voice. Don't pad with "perhaps/arguably" |

## Punctuation

| Metric | Imitation rule |
|--------|----------------|
| `em_dash_per_1k` | If >2, the author uses dashes as a structural device -- mid-sentence asides, not just lists |
| `exclaim_per_1k` | Match it. Authors who don't use `!` sound flat if you sprinkle them in |
| `question_per_1k` | If high, the author uses rhetorical questions. Mirror that move |
| `semicolon_per_1k` | If 0, never use one. Semicolons are the #1 tell of a "writer" voice the author doesn't have |
| `caps_words` | All-caps for emphasis is a strong stylistic choice -- count and match |

## Contractions

`contractions_per_1k_words` over ~30 = casual voice. Use "it's, don't, you're, can't" freely. Under ~10 = formal voice; expand them.

## Signature phrases

`signature_bigrams` and `signature_trigrams` are the author's verbal tics. Examples from real fingerprints:

- "ask for" / "the money" → tactical noun phrases the author leans on
- "you can't" / "i've seen" → recurring stance markers
- Drop 2-3 of the top signature phrases into any mimic draft so it sounds like the same author

Do NOT paraphrase signature phrases. They're load-bearing.

## Sentence openers

`top_sentence_openers` reveals rhythm. If "you" or "I've" or "that's" lead the list, the author opens with stance/observation, not subject+verb academic style. Start your sentences the same way.

## Quirks

The `quirks` array is plain-English flags. Treat every entry as a hard constraint:

- "uses 'fuck' as intensifier" → include it; don't sub "really" or "very"
- "rhetorical questions answered by self" → write a Q. Then answer it.
- "ALL-CAPS for emphasis" → use it on the SAME kind of words the author does
- "dash-driven asides" → favor `--` over `(parens)` and over commas for asides
- "spoken contractions: gonna/wanna/gotta" → write the way they talk

## Sanity check after drafting

After your mimic draft, mentally re-run the fingerprint:

1. Did you match the burstiness? Read aloud -- does the rhythm shift?
2. Did you reuse 2+ signature phrases?
3. Did you hit the profanity rate (±50%)?
4. Did you avoid every word in the AI filler set?
5. Did you preserve the author's quirks?

If any answer is "no," revise that pass before delivering.
