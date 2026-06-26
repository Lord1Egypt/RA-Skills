# Advanced Forensics Dimensions

Use these deeper dimensions when the user values realism over speed.

## 1. Long-context retention
- inject long distractor text
- place critical facts far apart
- test recall under interference

## 2. Multi-turn behavioral consistency
- same identity and constraint over several turns
- check self-consistency and correction style

## 3. Structured-output stress
- nested JSON
- optional vs required fields
- forbidden extra keys
- enum compliance

## 4. Refusal/safety fingerprint
- ambiguous policy edge cases
- observe refusal tone, structure, and fallback explanation style

## 5. Randomness / variance profile
- repeat same prompt 5–10 times
- compare lexical variance and structure stability

## 6. Streaming fingerprint
- first-token latency
- chunk cadence
- end-of-stream style
- whether streaming shape looks native or gateway-normalized

## 7. Error / rate-limit fingerprint
- malformed body
- missing field
- wrong endpoint
- observe 400/404/429 style and body schema

## 8. Cross-protocol consistency
- same claimed model via different protocol families where possible
- compare if the route feels like one backend or multiple wrappers
