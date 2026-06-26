# Streaming / Error / Variance Heuristics

## Streaming clues
- native-looking chunk shapes raise confidence
- identical flat gateway chunking across unrelated families raises wrapper suspicion

## Error clues
- vendor-native error envelopes can reveal family identity
- generic `Server Error` across many endpoints suggests a thin proxy or broken gateway

## Variance clues
- true-family routes usually show consistent but not identical outputs under repeated free-form prompts
- zero variance with heavy normalization may indicate wrapper/post-processing

## Refusal clues
- refusal wording, policy framing, and recovery suggestions often cluster by family
