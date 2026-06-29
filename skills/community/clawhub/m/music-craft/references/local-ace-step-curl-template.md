# Local ACE-Step Curl Template

Copy-pasteable direct submission pattern for the ACE-Step REST API. Use this
when the local server is already running on `http://127.0.0.1:8001` and the
operator wants deterministic control over the request body.

## Why This Exists

ACE-Step accepts a JSON request body at `/release_task`. The critical detail is
that `lyrics` must be a JSON string, so multiline lyrics need to be escaped
before they are inserted into the payload.

## Prepare Prompt And Lyrics JSON

```bash
PROMPT_JSON=$(python3 -c 'import json,sys; print(json.dumps(sys.stdin.read()))' < prompt.txt)
LYRICS_JSON=$(python3 -c 'import json,sys; print(json.dumps(sys.stdin.read()))' < cleaned_lyrics.txt)
```

## Submit A Job

`prompt.txt` should contain the full production-sheet prompt. Example:

```text
Fully arranged indie rock ballad with warm electric guitars, steady drums,
melodic bass, intimate lead vocal, wide chorus harmonies, emotional lift in
the final chorus. Anti-sparse rule: every section has guitar, bass, drums,
and vocal presence; never a cappella, never silent gaps.
```

```bash

TASK_ID=$(curl -s -m 30 -X POST http://127.0.0.1:8001/release_task \
  -H "Content-Type: application/json" \
  -d "{
    \"prompt\": $PROMPT_JSON,
    \"lyrics\": $LYRICS_JSON,
    \"audio_duration\": 200,
    \"bpm\": 80,
    \"key_scale\": \"E major\",
    \"time_signature\": \"4/4\",
    \"vocal_language\": \"en\",
    \"thinking\": true,
    \"inference_steps\": 8,
    \"guidance_scale\": 7.0
  }" | python3 -c 'import json,sys; print(json.load(sys.stdin).get("data",{}).get("task_id",""))')

printf 'TASK_ID=%s\n' "$TASK_ID"
```

## Field Notes

- `audio_duration` is the main reason to use the local route when exact length
  matters. In the 2026-06-12 field run, 18/18 local outputs matched the
  requested duration exactly.
- `thinking: true` is the quality default and can produce two saved cache files
  for one request. Collect both when present and label the second as a variant.
- Fill in BPM, key, time signature, vocal language, and duration explicitly
  even when `thinking: true` is enabled. These metas anchor the LM.
- Keep the anti-sparse guard in every prompt: list instruments, require them to
  keep playing, and forbid a cappella or silent gaps unless explicitly wanted.

## Next Step

After submission, use [`wait-and-collect.md`](wait-and-collect.md) to watch the
server log, collect cache files, and verify duration before submitting the next
version.
