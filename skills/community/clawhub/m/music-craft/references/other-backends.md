# Other Backends

Backend guides for everything that is not ACE-Step: MusicGen (local,
non-commercial weights),
Stable Audio (Stability AI REST API), and generic
CLI backends. Load this when the selected backend is one of these.

## MusicGen (local — non-commercial weights, no API key, no quota)

**License gate:** AudioCraft code is MIT, but MusicGen model weights are
CC-BY-NC 4.0. Use this backend only for personal, research, or other
non-commercial work permitted by that license. Do not use its output for
commercial releases, monetized channels, client work, paid products, or
advertising. For commercial local generation, use a backend whose exact model
checkpoint terms permit it, such as the currently documented ACE-Step 1.5
route, after verifying the current license.

**Best for:** fully offline non-commercial generation, no API dependency, and
no quota. **Trade-off:** quality is lower than MiniMax/ACE-Step, especially
for vocals. Use it for sketches or non-commercial instrumentals.

MusicGen takes a single text description. It does NOT have a separate lyrics parameter — the text description IS the entire input. MusicGen was trained on short natural-language descriptions, NOT structured production sheets like MiniMax. The skill must reformat the prompt before passing it.

**Device selection (MPS / CUDA / CPU):**

```python
import torch
if torch.backends.mps.is_available():      # Apple Silicon (M1/M2/M3)
    device = "mps"
elif torch.cuda.is_available():            # NVIDIA GPU
    device = "cuda"
else:
    device = "cpu"
```

Use `model.to(device)` after loading. MPS gives 2-5x speedup over CPU on Apple Silicon.

**Generation command (run via bash heredoc):**

```bash
python3 << 'MUSICGEN_EOF'
from audiocraft.models import MusicGen
from audiocraft.data.audio import audio_write
import torch

# Device selection
if torch.backends.mps.is_available():
    device = "mps"
elif torch.cuda.is_available():
    device = "cuda"
else:
    device = "cpu"

model = MusicGen.get_pretrained("<model_name>")
model.to(device)

# Generation parameters tuned for quality
model.set_generation_params(
    duration=30,          # MusicGen's effective max per call
    top_k=250,            # Token sampling diversity
    top_p=0.0,            # Nucleus sampling (0 = disabled)
    temperature=1.0,      # Creativity (0.5 = conservative, 1.0 = default, 1.5 = wild)
    cfg_coef=3.0,         # How strictly to follow the prompt (higher = more faithful)
)

# MUSICGEN-SPECIFIC PROMPT FORMAT (see below)
desc = """<short genre/mood/instrument description, 1-2 sentences>

<short lyric snippet, if any>"""

wav = model.generate([desc])
audio_write("<output_path_no_ext>", wav[0].cpu(), model.sample_rate, strategy="loudness", loudness_compressor=True)
print(f"Done: <output_path_no_ext>.wav")
MUSICGEN_EOF
```

**Model selection:**

| Model | Parameters | Vocal quality | Lyrics following | Best for |
|---|---|---|---|---|
| `small` | 300M | ❌ Instrumental only | ❌ Ignores lyrics | Quick tests, instrumentals |
| `medium` | 1.5B | ⚠️ Vague vocal-like sounds | ⚠️ Occasionally | Best CPU-vs-quality trade-off |
| `large` | 3.3B | ✅ Best vocals MusicGen offers | ✅ Better | When you have GPU or patience |
| `melody` | 1.5B | ✅ Melody-conditioned | ⚠️ Humming, not lyrics | Vocal-melody tracks |

**Selection logic:**
- Apple Silicon without GPU + need quick result → `medium`
- Apple Silicon with MPS + can wait → `large`
- NVIDIA GPU available → `large` (10-20x faster than CPU)
- Want vocal melody emphasis → `melody`

**MusicGen-specific prompt format:**

MusicGen was trained on short descriptions like `"upbeat indie rock with jangly guitars and energetic drums"`. Long structured production sheets like MiniMax prompts are NOT what it expects and produce worse results.

**Translation rule:** when adapting a MiniMax-style production-sheet prompt for MusicGen:

| MiniMax prompt element | MusicGen equivalent |
|---|---|
| 13-line production sheet with anti-sparse guards | **Condense to 1-2 sentences** with the core genre + mood + 2-3 key instruments |
| `[Verse]`, `[Chorus]` section tags in lyrics | **Replace with a short lyric snippet** (4-8 lines) |
| BPM/key/structure flags | **Fold into natural language** ("slow 80 BPM", "minor key") |
| Anti-sparse instructions ("always playing") | **Drop entirely** — MusicGen doesn't have that failure mode |
| `AVOID` lists | **Drop entirely** — MusicGen doesn't interpret them well |

**Example translation:**

```text
# MiniMax-style (13 lines, structured)
sludge doom metal, Melvins meets Eyehategod, crushingly heavy slow-motion,
oppressive dark cathartic, weight of a system collapsing,
male lead vocal, deep guttural growls, raw throat-shredding delivery,
FULL ARRANGEMENT: massively downtuned sludge guitar, sub-bass shakes floor,
tempo 82 BPM in E minor, doom reimagining, "the system will stand" becomes mantra,
extreme dynamic range whispered verses to screaming chaos,
sludge metal production thick muddy analog saturation,
vocal character: whispered verses, growling pre-chorus, full scream,
emotional arc: oppressive whisper opening, gradual crushing weight buildup,
dramatic pauses at 12s 55s 95s 130s, repeated "oh my god" lines,
avoid fast upbeat avoid clean singing avoid polished production

# MusicGen-style (2-3 sentences, natural language)
Slow crushing sludge doom metal at 82 BPM in E minor. 
Downtuned detuned guitars, sub-bass, slow half-time drums, 
oppressive dark mood. Melodic humming: "I don't know why, 
I don't know why, what I know is how to get along."
```

The MusicGen version is shorter, uses natural phrasing, and inlines a short lyric fragment at the end.

**MusicGen limitations (documented):**

- Default max ~30 seconds per call. Generate in chunks for longer tracks, or accept the limit.
- No separate lyrics parameter — lyrics are only useful as a short prompt hint, not a full song.
- No BPM/key flags — fold into natural-language text.
- CPU is very slow; MPS (Apple Silicon GPU) gives 2-5x speedup, CUDA gives 10-20x.
- Vocal quality is fundamentally lower than MiniMax/ACE-Step — this is a model design difference, not a configuration issue.
- Output is WAV by default. Convert with `ffmpeg -i in.wav -codec:a libmp3lame -qscale:a 2 out.mp3` if ffmpeg is available.

**Generation parameters (tuning guide):**

| Parameter | Default | Range | Effect |
|---|---|---|---|
| `top_k` | 250 | 50-500 | Lower = more focused, higher = more diverse |
| `top_p` | 0.0 | 0.0-1.0 | 0 = disabled. 0.9 = nucleus sampling, often better quality |
| `temperature` | 1.0 | 0.5-1.5 | Lower = more predictable, higher = more creative |
| `cfg_coef` | 3.0 | 1.0-10.0 | Higher = follows prompt more strictly but can sound artificial |

**Recommended starting values per intent:**

| Intent | top_k | top_p | temperature | cfg_coef |
|---|---|---|---|---|
| Faithful to prompt (style match) | 150 | 0.0 | 0.8 | 5.0 |
| Creative/experimental | 350 | 0.9 | 1.2 | 2.0 |
| Best vocals (singing attempt) | 200 | 0.0 | 1.0 | 4.0 |
| Instrumental only | 250 | 0.0 | 1.0 | 3.0 |

**Chunked generation for longer tracks:**

```python
# Generate 30s segments and concatenate
import torch
from audiocraft.models import MusicGen

model = MusicGen.get_pretrained("large")
model.to("mps")  # or "cuda" / "cpu"

all_audio = []
for i in range(total_segments):
    segment = model.generate([desc], progress=True)
    all_audio.append(segment)

# Concatenate and save
combined = torch.cat(all_audio, dim=-1)
audio_write("output_long", combined[0].cpu(), model.sample_rate, strategy="loudness", loudness_compressor=True)
```

Each segment takes 2-5 min on MPS, so a 3-minute song = 6-15 min total. Acceptable trade-off for free + local.

**Quality expectation (honest):**

| Output aspect | MusicGen best case | MiniMax baseline |
|---|---|---|
| Instrumental fidelity | ✅ Good | ✅ Excellent |
| Vocal presence | ⚠️ Vague humming | ✅ Clear singing |
| Lyrics accuracy | ❌ Ignores most | ✅ Word-level match |
| Song structure (verse/chorus) | ❌ Single texture | ✅ Follows tags |
| Audio polish | ⚠️ Lo-fi by default | ✅ Production-quality |
| Speed (CPU, 30s) | ~7 min | ~30s (cloud) |

Use MusicGen for instrumentals, sketches, or when cloud is unavailable. Use ACE-Step when you need actual sung lyrics.

Install details: see **MusicGen Installation Details** in [`setup-and-preflight.md`](setup-and-preflight.md).

## MiniMax (cloud) — no longer available

MiniMax closed its paid music and lyrics APIs to new users on 2026-08-20, is
discontinuing the free music models, and a paying account received HTTP 410 in
September 2026. `mmx` 1.0.28 no longer has a `music` command. Do not offer
MiniMax as a backend.

## MiniMax Music 3 (local open weights) — researched, not verified

MiniMax's suggested replacement is its open-weights
[`MiniMaxAI/MiniMax-Music3`](https://huggingface.co/MiniMaxAI/MiniMax-Music3).
This skill has not run it. Research notes, checked 2026-10-18:

- **Strength:** full songs with vocals, lyrics and section structure.
- **Apple Silicon:** the official weights need CUDA. The local route is
  `mlx-audio` with the `mlx-community/MiniMax-Music3-*` conversions: 4-bit
  9.2 GB, 6-bit 11.7 GB (the sensible choice for 24 GB of memory), 8-bit
  14.2 GB, BF16 28.5 GB (does not fit 24 GB).
- **Behavior:** the requested duration is an upper bound (the model may stop
  early), so it is not an exact-duration backend; trim or crossfade to length.
  Lyrics are required: pass `[instrumental]` for an instrumental. Output is
  44.1 kHz stereo WAV on the MLX route, up to about 5 minutes.
- **License (MiniMax-Music3 Community License):** commercial use is allowed
  while yearly revenue from products using it stays at or under USD 20M;
  above that, written authorization is needed. A commercial product must show
  "MiniMax-Music3" in its UI, and publishing generated content without clear
  disclosure that it is AI-generated is a restricted use. Name the license and
  get the user's acceptance before any download, like the other local models.

Before relying on it: install into its own virtual environment, pin the
`mlx-audio` revision, run a 30 s probe, and compare by ear with ACE-Step.

## Stable Audio (Stability AI REST API)

**Best for:** short instrumentals, sound design, text-to-audio.

**Data sharing:** this is a cloud API. The prompt (and any lyrics you fold into
it) is sent to Stability AI and billed to the user's account. Before the first
call, tell the user what will be sent and get their OK; offer local ACE-Step or
MusicGen if they prefer to keep the content on their machine. Never include
credentials or personal details in the prompt.

Use Stability AI's current audio-generation endpoint from their official API
documentation with the user's `STABILITY_API_KEY` (read from the environment,
never pasted into chat or files). Typical request fields: the text `prompt`, a
`duration` in seconds, and an `output_format` such as `mp3`. Save the response
body to the output file the user chose, then run the normal verification.

Stable Audio may not support separate lyrics input. For vocal tracks, combine
lyrics into the prompt text only after the user agrees to send them.

## Generic CLI (any other)

If a music generation CLI is detected that is not listed above, use it with the production-sheet prompt as the text input and the lyrics file if the CLI supports it. Adapt the command to the CLI's expected arguments.
