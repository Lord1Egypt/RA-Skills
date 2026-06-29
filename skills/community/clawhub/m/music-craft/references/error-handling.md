# Error Handling

Music generation can fail in many ways. This is a reference for the common ones, what causes them, and how to recover.

## Generation Errors

| Error | Cause | Fix |
|---|---|---|
| 401 Unauthorized | Bad or expired API key | The runtime should handle this; if not, tell the user to check the provider config |
| 429 Too Many Requests | Rate limit hit | Wait 60s, retry once, then reduce concurrency |
| 500 / 502 / 503 | Provider outage | Wait 30s, retry once; if persistent, try a different model if available |
| Timeout | Provider is slow, or audio is very long | Increase timeout; consider shorter lyrics |
| Empty file returned | API error not surfaced, or model returned silence | Check provider logs, retry with adjusted prompt |
| Sparse / a cappella output | Prompt missing anti-sparse guards | See Anti-Sparse Rules in SKILL.md |
| Wrong language | Prompt did not specify language | Add explicit language to the prompt |
| Clipped / distorted | Prompt used "raw" or "gritty" with high BPM | Remove harsh adjectives, add "clean mix" |
| Wrong genre | Provider does not support the genre | Switch to a closer supported style, or move to Skill 2 for finer control |
| Repeated chorus where it should not be | Lyrics missing or wrong section tags | Add or correct `[Verse]`, `[Chorus]`, etc. tags in the lyrics body |
| Too short | Lyrics body too short | Add more sections to the lyrics |
| Too long | Lyrics body too long | Trim sections, drop a `[Verse]` + `[Chorus]` repetition |
| No vocals despite requesting them | `instrumental: true` was set by mistake, or the provider does not support the requested language | Check the call parameters, specify the language explicitly in the prompt |

## User-Facing Errors

| Situation | What to say |
|---|---|
| No music backend found | Branch on detected hardware (see SKILL.md → User & Hardware Setup → no backend found message). Apple Silicon: clone ACE-Step with `git clone https://github.com/ace-step/ACE-Step-1.5.git "${ACE_STEP_PATH}" && cd "${ACE_STEP_PATH}" && uv sync && uv run acestep-api`. Intel Mac / Windows: recommend cloud backends or MusicGen. Linux+NVIDIA: same Apple Silicon install but with CUDA. |
| ACE-Step: API not responding on :8001 | "ACE-Step API server not running. Start it: `cd ACE-Step-1.5 && uv run acestep-api`" |
| ACE-Step: generation timeout (>10 min) | "ACE-Step generation taking too long. The first run loads models (~3 min). Subsequent runs should take ~2 min for 60s of audio on M3." |
| ACE-Step: OOM on any hardware | "Memory pressure. Try shorter duration (30s instead of 60s), downgrade to a lower tier (fast instead of xl-mixed), or restart the API server to clear cached models. On Apple Silicon M3 24GB, xl-mixed is viable with `ACESTEP_GENERATION_TIMEOUT=3600` (~52 min for 60s audio). Best (4B LM) requires 32GB+." |
| MusicGen: `import audiocraft` fails | "MusicGen not installed. Run: `pip install audiocraft torch`" |
| MusicGen: CUDA out of memory | "GPU memory full. Try model `small` instead of `medium`/`large`, or reduce duration to 60 seconds." |
| MusicGen: output is only ~30 seconds | "MusicGen's default chunk is ~30s. For longer tracks, accept shorter output or use a cloud backend (Stable Audio API) or install ACE-Step locally." |
| MiniMax quota exhausted | "MiniMax quota hit. Switching to next available backend." Then re-run detection, skip MiniMax, try MusicGen or Stable Audio. |
| The user asks for a fast cover or mashup | "That needs fast cloud cover / style transfer. Switch to `music-craft-minimax` and I will run the pre-flight with the extended checks." |
| The user asks for a local cover/repaint experiment | "I can try this locally with ACE-Step, but it is slower, queue-bound, and source-length sensitive. I will use the ACE-Step cover/repaint workflow and wait helper." |
| The user asks for emotion analysis | Same redirect to Skill 2 |
| The user provides audio without a clear goal | Ask: cover? Sample? Style reference? |
| The user wants 10 variations of the same song | Generate 3 max with different (genre, mood, OR structure — not all three at once). More is wasteful. |
| The user wants deterministic output (same input = same output every time) | Tell them: AI generation is non-deterministic by default. Some providers support a seed; check provider docs. |
| The user wants a specific real artist's voice (e.g., "sound like Rosalía") | Tell them: AI generation can imitate style, not specific copyrighted voices. Use the artist's typical style (genre, instruments, vocal register) in the prompt instead. |
| The user wants the song to mention a real person, brand, or event | Allowed, but flag the ethical / legal implications. The user is responsible for the content. |
| The user wants the song to include copyrighted lyrics | Tell them: do not paste copyrighted lyrics into the prompt. Rewrite or summarize instead. |
| The user wants vocals in a language the provider does not support | Skill 2's `lyrics_generation` endpoint handles many languages via MiniMax. For other providers, fall back to English and note the limitation. |

## Recovery Patterns

| Pattern | When to use | How |
|---|---|---|
| Retry with same payload | Rate limit, transient network | Once, after waiting 60s |
| Retry with adjusted prompt | Wrong genre, sparse output, wrong language | Adjust one or two slots, see [`references/prompt-formula.md`](prompt-formula.md) |
| Retry with a different model | Provider model failure or quality issue | Try a different model if the runtime exposes one |
| Switch to Skill 2 | User wants cover, mashup, emotion analysis | Redirect cleanly |
| Ask the user to clarify | After 2 failed retries | "I've tried twice. Can you give me more direction?" |
| Accept the result with caveats | 1–2 of 8 quality checks failed, retry unlikely to fix | Deliver with a note about which checks failed |

### Common prompt adjustments

- **Sparse output** -> restate every instrument, add the always-playing rule again, and add a quiet-section floor such as "quiet sections: reduced to piano and bass only, still fully played."
- **Wrong language** -> restate the target language in the prompt and lyrics body, and simplify the style wording so the vocal language does not get drowned out.
- **Bad vocals** -> specify voice type, register, and delivery more tightly; if the issue is clipping or warping, remove harsh descriptors and add "clean mix, no distortion."
- **Wrong structure** -> align the prompt's structure line with the actual lyric tags, then add or remove `[Bridge]`, `[Break]`, or `[Build Up]` so the shape is unambiguous.
- **Clipped ending** -> add a dedicated `[Outro]`, request a full ending with the final line held, and avoid abrupt cut-off language.

## Retry Recipes

When a generation fails a specific way, the recovery is a small recipe. Pick the recipe that matches the failure mode and apply it as a **single** targeted change. Never combine more than two recipes per retry — chained changes make it impossible to know what actually fixed the problem.

For each recipe, the failure is described, the fix is a tight checklist, and the prompt mutation shows what to add (or remove) at the end of the original prompt. For the matching `REVISION:` pattern that keeps the rest of the prompt intact, see `SKILL.md` → Revision Prompts.

### Wrong language

The vocals are not in the language the user asked for, or mixed languages appear unexpectedly.

1. Restate the target language in the prompt: `vocal in Spanish only, no English words`.
2. Confirm the lyrics body is in the target language (the auto-lyrics optimizer can drift).
3. Move the language descriptor to the front of the voice line so it is not lost among other descriptors.
4. Drop adjectives that might pull the model toward the wrong accent: `British`, `American`, `regional`.

Prompt mutation:

```
REVISION:
- Vocals in [target language] only, no [other language] words
- Lyric body is already in [target language] — keep as is
- Keep: genre, mood, instruments
```

### Weak chorus

The chorus does not feel like a hook. Verses and chorus blend together; the song has no payoff.

1. Add a `[Pre Chorus]` between every verse and chorus for a build.
2. In the prompt, ask for: `Chorus: melody-driven, hook-forward, with sustained vowels`.
3. In the lyrics, give the chorus longer held notes (stretch vowels: `riiiiiise`, `hoooold`).
4. Request wider chorus instrumentation: `chorus: full band plus backing vocals and stacked harmony`.

Prompt mutation:

```
REVISION:
- Chorus: melody-driven, hook-forward, with sustained vowels and stacked backing vocals
- Add a [Pre Chorus] section before each [Chorus] for build
- Keep: verse style, language, instruments
```

### Sparse arrangement

The output goes a cappella or silent mid-track. This is the most common failure. See the **Anti-Sparse Failures** table below for the dedicated fix path; the recipe is the same idea expressed as a tight checklist.

1. Restate every instrument by name (do not just refer to "the band").
2. Restate the always-playing rule explicitly.
3. Add a quiet-section floor: `quiet sections: reduced to [2 instruments] only, still fully played`.
4. Add an explicit anti-a-cappella line: `NEVER a cappella, NEVER silent at any point`.

Prompt mutation:

```
REVISION:
- Strengthen anti-sparse: "ALL instruments ALWAYS playing, NEVER a cappella, NEVER silent"
- Re-list every instrument: [instrument 1], [instrument 2], [instrument 3]
- Quiet sections: reduce to [instrument 1] and [instrument 2] only, still fully played
- Keep: language, vocal type, structure
```

### Vocals present in instrumental

The user asked for an instrumental but the output has vocals (or humming, or whispered words).

1. Confirm `Instrumental only, no vocals, no lyrics` is at the top of the prompt.
2. Check the `instrumental` flag is set (provider-specific).
3. If the model keeps adding vocals, add a redundant AVOID line: `AVOID vocals, AVOID singing, AVOID human voice, AVOID humming`.
4. As a last resort, switch to a provider with a true instrumental mode (Volcengine BGM, ElevenLabs instrumental model).

Prompt mutation:

```
REVISION:
- Reinforce: "Instrumental only, no vocals, no lyrics, no humming"
- AVOID vocals, AVOID singing, AVOID human voice
- Keep: genre, mood, structure
```

### Missing genre identity

The output sounds generic — could be any genre. The genre descriptor was not strong enough to commit the model to a specific style.

1. Replace the broad genre (`pop`, `rock`) with a subgenre and era: `80s synth-pop`, `modern Latin pop with reggaeton influence`, `British indie rock with Britpop-era production`.
2. List 3–4 genre-specific instruments: `synth-pop → analog synth, drum machine, slap bass, gated reverb`.
3. Reference a specific production: `Phil Collins era gated drum sound`, `1980s LinnDrum`, `MTV-era pop production`.
4. AVOID the opposite: `AVOID modern trap drums, AVOID acoustic guitar, AVOID lo-fi bedroom mix`.

Prompt mutation:

```
REVISION:
- Genre: [specific subgenre] with [era] production
- Instruments: [3–4 genre-specific instruments]
- AVOID [opposite-of-genre]
- Keep: language, vocal type, structure
```

### Too generic output

The result is technically correct but unmemorable. The prompt had nothing distinctive for the model to commit to.

1. Add a specific production or artist reference (style only, never copyrighted voice): `style of Daft Punk, NOT the actual voices`.
2. Add a distinctive arrangement detail: `four-on-the-floor kick, syncopated hats, call-and-response synth`, `galloping bass line`, `tritone substitution in the bridge`.
3. Add a memorable melodic or lyrical device: `recurring synth motif in the intro that returns in the outro`, `call-and-response between lead vocal and backing vocal in the chorus`.
4. Trim generic adjectives (`emotional`, `cinematic`, `beautiful`, `moody`, `vibe`) — they are model defaults that get ignored. Either ground them with production details or drop them.

Prompt mutation:

```
REVISION:
- Add distinctive arrangement: [specific production detail]
- Add memorable device: [motif, hook, or production signature]
- Remove ungrounded words: emotional, cinematic, beautiful
- Keep: language, structure, base genre
```

## Iteration Loop

When the output fails verification, follow this loop before escalating to the user:

1. Identify the failure mode (sparse, clipped, wrong genre, no vocals, and so on).
2. Adjust the prompt or lyrics to target the failure.
3. Try once with a different seed or model if available.
4. After 2 failed retries, ask the user to clarify or accept the best attempt.

Never retry the same prompt plus lyrics combination twice in a row.

## When NOT to Retry

- Do not retry the same exact prompt + lyrics combination more than twice in a row.
- Do not retry if the user has already changed direction mid-iteration.
- Do not retry if the provider returned a 4xx (client error) — fix the request first.
- Do not retry if the output was good but the user is just undecided — ask for confirmation instead.

## Anti-Sparse Failures (Special Case)

The most common generation failure is sparse / a cappella output. It has a dedicated fix path:

| Symptom | Likely cause | Fix |
|---|---|---|
| Output is silent for entire chorus | Prompt did not list instruments for that section | Add explicit instruments and "ALL instruments ALWAYS playing" |
| Output goes a cappella mid-track | The model interpreted "build" or "decrescendo" as "remove all instruments" | Add explicit "NEVER a cappella, NEVER silent" with the always-playing rule |
| Quiet sections have only one instrument | Prompt did not specify minimum instrument count for quiet sections | Add "quiet sections: reduced to [X] and [Y] only, still fully played" |
| Output is instrumental when user wanted vocals | Provider may not support the requested language or voice | Specify language explicitly; consider a different model |
| Output has no drums / percussion | Prompt listed melodic instruments only | Add "with [drums/percussion type] throughout" |
| Output has vocals but no melody / harmony | Prompt did not specify harmony | Add "with [chord instrument] playing chord progression" |

For the full anti-sparse rules, see `SKILL.md` → Anti-Sparse Rules (Critical).

## Provider-Specific Failure Modes

Different providers fail in different ways. Here are the patterns to recognize:

### MiniMax Music 2.6

- **Most common failure:** sparse output when the prompt is vague. Anti-sparse rules solve it.
- **Vocal speed:** No native "vocal speed" parameter. Achieve through lyrics formatting (fewer syllables, repeated vowels).
- **Sparse interpretation:** "sparse" or "minimal" → removes all instruments. Always pair with explicit instruments.
- **Lyrics optimizer:** if no lyrics, auto-generates. Quality is good but unprompted.

### ACE-Step 1.5

- **Most common failure:** under-specified or conflicting caption. ACE-Step works best with a detailed, coherent caption plus explicit metas; short tags can work when `thinking=true`, but do not rely on the LM to rescue a vague brief.
- **First-run latency:** model loading takes ~90s on first generation. Subsequent generations are ~2 min for 60s of audio.
- **Audio location:** generated files are saved to `<ACE-Step-repo>/.cache/acestep/tmp/api_audio/` with UUID filenames. Copy files directly from cache — the `v1/audio` endpoint may not work reliably.
- **query_result quirk:** the task result may return empty even when audio is ready. Check the server logs or the cache directory directly.
- **Apple Silicon:** MPS tier6a (17.8 GB unified memory) uses MLX backend with no compile/quantization. DiT diffusion ~7.8s/step, VAE decode ~28s.
- **Batch of 2:** ACE-Step generates 2 variants per request. Both are saved to cache. Use the better one.

#### ACE-Step Tier / RAM Errors

| Error | Cause | User Message | Fix |
|---|---|---|---|
| Insufficient disk space for XL | User wants xl-mixed but <20 GB free (or <10 GB for base models) | "The XL model needs ~20 GB extra disk space (you have X GB free). Standard tier needs ~10 GB total. Options: (1) free up space and retry, (2) use standard tier (no extra download, still sounds great), or (3) use a cloud backend like MiniMax or Stable Audio." | Suggest standard tier or cloud alternative |
| Insufficient ML budget for requested tier | Tier needs more ML budget than available | "This quality tier needs ~X GB of ML budget (free RAM minus OS overhead, or smaller of free RAM/VRAM on dedicated GPU). Your system has Y GB ML budget. Try: fast (~8 GB), standard (~11 GB), or xl-mixed if you have 15 GB+." | Run memory check, suggest appropriate tier |
| OOM when loading XL model | Not enough RAM for 4B DiT + LM simultaneously | "ACE-Step ran out of memory. The xl-mixed tier needs ~25-30 GB peak (with MPS pool pressure on unified memory). On a unified-memory Mac, your 24 GB total is actually ~18-20 GB ML budget after macOS + apps. Solutions: (1) restart the server with `PYTORCH_MPS_HIGH_WATERMARK_RATIO=0.0` env var; (2) close other apps (browser tabs, IDE, Docker); (3) use a shorter audio length (60s instead of 210s); (4) downgrade to standard tier." | Restart with env var, close apps, shorten audio, or downgrade |
| System extremely slow during generation | Using xl-mixed with other apps open on limited unified memory | "Your laptop is slow because ACE-Step's xl-mixed tier uses ~25-30 GB RAM during generation (MPS pool pressure on unified memory), but only ~18-20 GB is actually available on a 24 GB Mac after macOS + apps. On a dedicated GPU system this would be a different issue — the bottleneck would be VRAM, not system RAM. Close browser tabs, IDE, or heavy apps and it should speed up significantly. If it doesn't, switch to standard tier." | Close apps, don't multitask during gen |
| **Generation stalled (step time > 60s)** | Memory pressure causing swap-thrashing (unified) or VRAM exhaustion (dedicated) | "Generation is going very slow (each diffusion step taking 60+ seconds) — this means either (a) unified-memory swap-thrashing: system is using disk as RAM, or (b) dedicated-GPU VRAM exhaustion: GPU is paging. Solutions: (1) set `ACESTEP_GENERATION_TIMEOUT=3600` and wait; (2) close all other apps; (3) restart the API server; (4) downgrade to standard tier. Verified: 60s audio at 50 steps on 24GB M3 unified memory takes ~52 min wall-clock (~50-100s/step) but completes successfully." | Set extended timeout, close apps, OR downgrade |
| `Music generation timed out after 600 seconds` | Default timeout too short for xl-mixed | "ACE-Step's default 600s (10 min) server timeout fired mid-generation. This is normal for xl-mixed (4B DiT + 1.7B LM) on 24GB M3 unified memory — full generation takes 50+ min. Solution: restart the server with `ACESTEP_GENERATION_TIMEOUT=3600` env var (1 hour). If still timing out, reduce audio duration to 60s or downgrade to standard tier." | Set `ACESTEP_GENERATION_TIMEOUT=3600` |
| **Audio sounds like "many songs at once"** | XL model with `inference_steps: 8` — too few steps for sft model | "The XL sft model needs 50 diffusion steps to produce clean output. With only 8 steps, the diffusion can't separate vocals from instruments, foreground from background — all elements compete at the same level. Verified: LRA drops from 4.0+ LU (50 steps) to 1.8-4.8 LU (8 steps). Solution: use `inference_steps: 50` for XL, even though it takes longer." | Use `inference_steps: 50` for XL, not 8 |
| **Audio sounds like noise / no sense samples (xl-mixed 50 steps)** | XL sft on 24GB M3 produces poor audio even with 50 steps — likely LM-generated codes are low quality, or shift/CFG defaults are suboptimal for sft model. | "This is a known issue with xl-mixed on 24GB M3. Generation completes in ~52 min for 60s but output is not production-ready. Use the standard tier for now (10 min, known good output). If you want to keep trying xl-mixed, the most likely fixes are: (1) provide a detailed prompt with all 6 metas (BPM, key, time sig, vocal lang, duration, genre), (2) try `shift: 1.0` or `shift: 5.0`, (3) try `guidance_scale: 4.0`, (4) try `infer_method: 'sde'`, (5) try `thinking: false` to skip LM." | Use standard tier (recommended); or try the fix list in the SKILL.md "XL 50-step fixes to try" section |
| Model not found: acestep-v15-xl-* | XL model not downloaded | "XL model not found. To upgrade quality: tell me 'use best quality' or 'use xl-mixed' and I'll guide you through the ~20 GB download." | Download model on user request |
| Model not found: acestep-5Hz-lm-4B | 4B LM not downloaded AND user is on unified memory (Mac, integrated graphics) | "The 4B LM model is NOT recommended on unified-memory hardware (Apple Silicon, integrated graphics) — it peaks at ~22 GB and the model + MPS pool + macOS overhead would OOM or swap heavily. The xl-mixed tier (4B DiT + 1.7B LM) is the max-quality tier your hardware can safely run. Want to upgrade to xl-mixed instead? (Yes / No)" | Suggest xl-mixed tier instead of 4B LM |
| Model not found: acestep-5Hz-lm-4B on dedicated GPU (32GB+ VRAM) | 4B LM not downloaded but dedicated VRAM is sufficient | "The 4B LM needs ~10 GB extra download and ~22 GB peak VRAM. Your GPU has enough VRAM to handle it. Download? (Yes / No)" | Download on consent, generate |
| Model not found: acestep-5Hz-lm-4B on dedicated GPU (16-24GB VRAM) | 4B LM needs ~22 GB but VRAM is only 16-24 GB | "The 4B LM needs ~22 GB peak VRAM but your GPU has {X} GB. The xl-mixed tier (4B DiT + 1.7B LM) is the best tier that fits your VRAM. Want to upgrade to xl-mixed instead? (Yes / No)" | Suggest xl-mixed tier instead of 4B LM |
| `Slot init failed` | Tried invalid model combination via `/v1/init` | "That model combination isn't supported. Valid combinations for {RAM}GB: {list of available tiers}. Pick one." | Use a valid tier combo from the SKILL.md table |
| Generation extremely slow (>30 min) | Using xl-mixed on weak hardware or too many apps open | "Generation taking longer than expected — xl-mixed tier is ~15 min/track AND other apps are competing for RAM. Close everything except ACE-Step, or switch to standard (~10 min/track)." | Close apps or downgrade tier |

### ElevenLabs Music

- **Most common failure:** errors when no lyrics are provided. ElevenLabs requires explicit lyrics.
- **Vocal quality:** very strong, multiple voice options.
- **Length limit:** shorter than competitors (typically 30s–2min).

### Volcengine / DouBao

- **Most common failure:** BGM mode is great, vocal mode is weaker.
- **Vocal quality:** best in Mandarin Chinese.
- **Use case:** ideal for background music, jingles, intros.

### Other / unknown providers

- Default to the standard anti-sparse rules.
- If the result is poor after 2 attempts, recommend the user switch to a known provider or install `music-craft-minimax` (which uses MiniMax and has a more controlled output).

## When to Give Up and Ask the User

If after 2 retries the result is still unacceptable:

1. Show the user the best attempt so far.
2. Explain what was tried and why it failed.
3. Ask the user for:
   - A clearer direction (specific style, reference artist, sample audio)
   - Permission to try a different model
   - Permission to switch to Skill 2 for finer control
   - Acceptance of the best result with a note about the limitation

Never loop forever. Always give the user an off-ramp.

## Smoke Tests for Base Prompts

Before submitting a prompt to `music_generate`, run a quick smoke test. The full smoke-test suite is provider-agnostic — no API calls, no audio libraries, no provider-specific assumptions. A future agent or test can run it as a pre-flight check on any prompt the skill produces.

### Representative checks

The list below is the **minimum** a prompt must pass. If any check fails, fix the prompt before calling the tool. For the matching prompt-slot rules, see [`prompt-formula.md`](prompt-formula.md) → Prompt Lint.

1. **All required slots are present.** Genre/subgenre, mood, voice or instrumental mode, instruments, anti-sparse instruction, BPM/key, structure, dynamics, production quality, avoid list. A missing slot is a hard fail.
2. **The anti-sparse guard is in the prompt body.** The string contains a phrase equivalent to `ALL instruments ALWAYS playing` and a phrase equivalent to `NEVER a cappella or silent`. Implied guards do not count.
3. **Instruments are listed by name.** The instruments slot has at least 3 named instruments separated by commas. A single instrument ("piano") is a hard fail.
4. **The avoid list is explicit.** The prompt ends with `AVOID ...` and contains at least one anti-sparse term (`sparse`, `a cappella`, `minimal`).
5. **Language is consistent.** The voice language in the prompt matches the dominant language in the lyrics body. Mismatched languages are a hard fail.
6. **Tags are in English.** The lyrics body uses `[Verse]`, `[Chorus]`, etc., not `[Verso]`, `[Coro]`, etc. Non-English tags are a hard fail.
7. **User-provided lyrics are intact.** If the request was user-lyrics, the lyrics body is a superset of the user's input. The set difference between user text and lyrics body should be empty (only section tags may be added).
8. **Instrumental requests omit voice details.** If the request was instrumental, the prompt contains `Instrumental only` or equivalent, and the voice line does not describe a specific singer.
9. **Mood words are grounded.** Every mood adjective in the prompt is paired with at least one production detail in the same prompt (instrument, rhythm, vocal delivery, arrangement, or mix). A bare `emotional` or `cinematic` is a hard fail.
10. **The structure line matches the tags.** The structure slot lists the same sections in the same order as the lyric tags. A structure line of `verse-chorus-verse-chorus` with a lyric body that has `[Bridge]` is a hard fail.

### Optional: integrate with the MiniMax linter

If the helper script `music-craft-minimax/scripts/lint_music_request.py` is available in the workspace, run it for the routing, missing-field, prompt-slot, and `mmx` flag checks. The MiniMax linter is the closest thing to an automated smoke test for this skill, but it is **not** a substitute for the ten checks above. The linter does not enforce mood grounding, language consistency between prompt and lyrics, or the user-lyrics-intact rule.

### Optional: keep a regression set

If the workspace has a `tests/prompts/` directory (provider-agnostic, just plain text), save one prompt per worked example from [`examples.md`](examples.md) as a regression fixture. Future changes to the prompt formula or the lint rules can be checked against this set. The five examples (Spanish pop, English instrumental jingle, user-provided lyrics, image-inspired track, text-only style reference) cover the main shapes a base prompt can take.
