# Local ACE-Step Request Template

Copy-pasteable direct submission pattern for the ACE-Step REST API, using the bundled standard-library helper. Use this
when the local server is already running on `http://127.0.0.1:8001` and the
operator wants deterministic control over the request body.

## Why This Exists

ACE-Step accepts a JSON request body at `/release_task`. The critical detail is
that `lyrics` must be a JSON string, so multiline lyrics need to be escaped
before they are inserted into the payload.

## Build The Request Body

Write the body with Python so multiline lyrics are escaped correctly:

```bash
python3 - <<'PY'
import json
from pathlib import Path
body = {
    "prompt": Path("prompt.txt").read_text(encoding="utf-8"),
    "lyrics": Path("cleaned_lyrics.txt").read_text(encoding="utf-8"),
    "audio_duration": 200,
    "bpm": 80,
    "key_scale": "E major",
    "time_signature": "4/4",
    "vocal_language": "en",
    "thinking": True,
    "inference_steps": 8,
    "guidance_scale": 7.0,
}
Path("body.json").write_text(json.dumps(body, ensure_ascii=False), encoding="utf-8")
PY
```

`prompt.txt` should contain the full production-sheet prompt. Example:

```text
Fully arranged indie rock ballad with warm electric guitars, steady drums,
melodic bass, intimate lead vocal, wide chorus harmonies, emotional lift in
the final chorus. Anti-sparse rule: every section has guitar, bass, drums,
and vocal presence; never a cappella, never silent gaps.
```

## Submit And Wait

```bash
TASK_ID=$(python3 scripts/acestep_request.py release_task --print-task-id --json-file body.json)
printf 'TASK_ID=%s\n' "$TASK_ID"
python3 scripts/wait_for_acestep.py "$TASK_ID" --expected-seconds 200
```

`scripts/acestep_request.py` only talks to a loopback server (`127.0.0.1`,
`localhost`, `::1`). Other endpoints work the same way, for example
`python3 scripts/acestep_request.py health` or
`python3 scripts/acestep_request.py v1/init --json '{"dit_model": "acestep-v15-turbo"}'`.

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
