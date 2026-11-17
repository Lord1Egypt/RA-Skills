# Prompts, the model chain, and notes

## Never call a provider SDK

`from services import llm`. That module resolves an ordered chain of providers,
so one outage is not the terminal's outage, and it centralises the things every
call site would otherwise get wrong: quota cooldowns, retry with `retry_after`,
and stripping `<think>…</think>` blocks from reasoning models.

```python
async def generate(prompt: str, *, system: str = "", temperature: float = 0.7,
                   max_tokens: int = 1000, top_p=None, stop=None,
                   timeout: float = 60.0, reasoning: Optional[bool] = None,
                   json_mode: bool = False, extra: Optional[dict] = None,
                   prefer: Optional[LLMProvider] = None) -> Optional[str]
```

Everything after `prompt` is keyword-only. It returns `None` when every
provider failed — that is the normal degraded path and callers must handle it.
The one exception it raises is `LLMRequestError` (HTTP 400), which means the
request itself was malformed; that is our bug and must not be swallowed.

`prefer=` puts a user-supplied provider at the head of the chain, for work
billed to that user's own key. **Pass `prefer=None` for anything cached and
served to everyone** — otherwise one reader's key pays for every other reader's
copy.

Other exports worth knowing: `llm_health()`, `active_provider_info()`,
`PRESETS` / `preset_names()`, `cooldown_remaining()`, `clear_cooldowns()`, and
the error hierarchy `LLMError` → `LLMTransientError` / `LLMRateLimitError` /
`LLMUnavailableError` / `LLMRequestError`.

Adding a provider is a `PRESETS` entry in `presets.py` plus an adapter in
`providers.py` registered in `ADAPTERS`. Adapters subclass `LLMProvider(ABC)`:
`async generate(req) -> str`, `async health() -> bool`, optional `list_models()`.

## Prompts are files

`backend/prompts/<domain>/<name>.md`. Domains today: `analysis`, `chat`,
`ownership`, `notes`, `macro`, `news`, `generic`, `chains`, `detection`.

```python
from services.prompts import load_prompt, render_prompt

system = load_prompt("generic/system_default")          # .md implied, cached
body = render_prompt("chains/anomaly", chain="Solana", fee_delta="+240%")
```

Substitution is `{{placeholder}}` by plain `str.replace` — deliberately not
`str.format` or `string.Template`, because market text is full of `$` and `{}`
that those would choke on. An unsubstituted `{{` only logs a warning, so it
will not crash a turn; it will just ship a broken prompt.

Format is plain Markdown: no frontmatter, no Jinja. The house shape is a
`TASK:` line first, `═══`-fenced sections, then numbered bold instructions.

**The template name must be a string literal.** `backend/tests/test_prompts.py`
walks the AST of the whole backend collecting literal arguments to
`load_prompt`, `render_prompt` and `prompt=` on `NoteSpec`, then fails on dead
templates, placeholders that are never supplied, and keys supplied but never
used — in both directions. A computed name passes review and defeats all of it.

## The note pattern

Most services do not call `llm.generate` directly. They declare a note and let
`backend/services/ai_notes.py` run it:

```python
NOTE_SPEC = NoteSpec(kind="chain_anomaly", prompt="chains/anomaly",
                     max_tokens=260, temperature=0.2, max_age_seconds=3600)

facts = note_facts(detection)        # quantized — this is the cache fingerprint
return await get_note(NOTE_SPEC, facts, note_values(facts))
```

`get_note` returns `{"status": "ready" | "generating" | "unavailable", "note",
"generated_at", "reason"}` and **never raises and never blocks**. Generation is
single-flight through `analysis_jobs.start(...)`; the HTTP request that
triggered it returns `generating` and the page renders without the note. Every
consumer must handle all three states — the label is always there, the note may
not be.

Two constraints that are easy to violate:

- **`note_values()` must be derived from `facts` alone.** `facts` is what gets
  fingerprinted, so a value that comes from somewhere else changes the prompt
  without changing the cache key, and stale notes survive forever.
- **Quantize the facts.** They are the cache key; unrounded floats mean a fresh
  generation on every poll.

`fingerprint()` hashes `NOTE_REVISION`, the kind, the model, the *content* of
the prompt file, the content of `notes/rules`, and the canonical facts — so
editing a prompt file retires every note derived from it automatically.

To add a note surface: a prompt in `prompts/<domain>/<x>.md` ending in
`{{rules}}`, a `NoteSpec`, `note_facts()` / `note_values()` in the service, and
one router line — `{**payload, "note": await x_note(payload)}`.

## Evals

`backend/evals/` — standalone CLI scripts. **Not pytest, not in CI**, because
they need a live Ollama and populated feeds. Run them from `backend/` with the
venv active when you change retrieval, the planner, or an answer mode.

| Script | Measures | Gate |
|---|---|---|
| `eval_planner.py` | tool-selection recall/precision, heuristic-fallback rate | thresholds gate `CHAT_PLANNER_ENABLED` |
| `eval_groundedness.py` | every number in an answer appears in the captured context | slow; real turns |
| `eval_refusal.py` | refusal rate, fabrication rate, drift in `conceptual` mode | `--style concise\|detailed` |
| `eval_retrieval.py` | recall@5 and MRR over `golden_set.jsonl` | `--no-rerank`, `--no-hybrid`, `--compare` isolate each stage |

`golden_set.jsonl` is 31 objects of the form
`{"id", "query", "asset_type", "symbol"?, "expect_events": [...], "note": "why this case exists"}`.
The `note` field is not decoration — a case nobody can explain is a case nobody
can fix when it regresses.

Each script exits 0 for PASS and 1 for FAIL and takes `--limit` and `-v`. Match
that shape if you add one.
