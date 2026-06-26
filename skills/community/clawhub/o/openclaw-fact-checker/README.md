# fact-checker ✅

**Open-source multimodal fact-checking for OpenClaw — verify news, claims, images, and videos in any language. Zero config.**

## Install

```bash
claw install fact-checker
```

That's it. No Python, no pip install, no API keys required beyond what you already have in OpenClaw.

## What it does

- Fact-check news articles, social media posts, and claims
- Verify images — detect AI-generated, manipulated, or out-of-context photos
- Verify videos — extract keyframes, transcribe audio, detect deepfakes
- Detect misinformation and disinformation in any language
- Cross-reference claims against 100+ global fact-checking organizations
- Decompose articles into atomic claims and verify each independently
- Search the web for evidence and cite sources for every verdict
- Extract and analyze image/video metadata (EXIF) and content credentials (C2PA)
- Output structured verdicts with confidence scores
  - **Text:** TRUE / FALSE / PARTIALLY_TRUE / MISLEADING / UNVERIFIED
  - **Image/Video:** AUTHENTIC / MANIPULATED / AI_GENERATED / OUT_OF_CONTEXT / DEEPFAKE_SUSPECTED / UNVERIFIED

## Usage

Just ask your agent:

```
Fact-check this: "NASA announced that Earth will stop rotating by 2030."
```

```
Fact-check this news: "Elon Musk announced Tesla will stop producing EVs entirely by 2027."
```

```
Is this true? https://example.com/suspicious-article
```

```
Is this image real or AI-generated? [attach image]
```

```
Is this video a deepfake? [attach video]
```

## How It Works

The skill auto-detects input modality (text, image, or video) and routes to the appropriate pipeline:

**Text Pipeline** (4 stages):
1. **Existing Fact-Check Lookup** — Searches 100+ global fact-checkers (Snopes, PolitiFact, AFP, etc.)
2. **Claim Extraction & Triage** — Decomposes text into atomic claims, filters out opinions and vague statements
3. **Deep Verification** — Searches the web for evidence, analyzes sources, assigns verdicts
4. **Report Generation** — Structured report with per-claim verdicts and source URLs

**Image Pipeline**:
1. **Visual Analysis** — Multimodal LLM examines image for AI artifacts, manipulation signs, OCR
2. **Reverse Image Search** — Finds original source, detects out-of-context reuse
3. **Metadata Extraction** — EXIF data analysis via `exiftool` (optional)
4. **C2PA Verification** — Content credential and provenance check via `c2patool` (optional)
5. **Verdict Synthesis & Report** — Combines all signals into a verdict with source attribution

**Video Pipeline** (search-first, ffmpeg enhances):
1. **Context Search & Source Verification** — Web search for origin, fact-checks, media coverage (always runs)
2. **Keyframe & Audio Analysis** — Extracts frames via `ffmpeg`, transcribes audio via Whisper (when available)
3. **Verdict Synthesis & Report** — Combines search + technical analysis into verdict with source attribution

### Verdicts

**Text claims:**

| Verdict | Meaning |
|---------|---------|
| TRUE | Confirmed by multiple credible sources |
| FALSE | Contradicted by multiple credible sources |
| PARTIALLY_TRUE | Contains some truth but is misleading or missing context |
| MISLEADING | Technically accurate but creates a false impression |
| UNVERIFIED | Insufficient evidence to confirm or deny |

**Image/Video:**

| Verdict | Meaning |
|---------|---------|
| AUTHENTIC | Genuine, unaltered media with verified source |
| MANIPULATED | Digitally edited, cropped misleadingly, or altered |
| AI_GENERATED | Created by AI (Stable Diffusion, DALL-E, Midjourney, etc.) |
| OUT_OF_CONTEXT | Real media used in a misleading context |
| DEEPFAKE_SUSPECTED | Facial/body anomalies suggest AI face-swap or synthesis |
| UNVERIFIED | Insufficient evidence to determine authenticity |

## Configuration

### Web Search (most users already have this)

The skill uses your OpenClaw agent's built-in web search. If you already have Brave Search, Firecrawl, or any other web search configured in OpenClaw, **you're good to go — no extra setup needed**.

If you don't have web search configured yet, the skill will guide you through setting up Brave Search (free, takes ~1 minute):
1. Go to https://brave.com/search/api/ and create a free account
2. Generate an API key (free plan = 1,000 searches/month)
3. Set `BRAVE_SEARCH_API_KEY` in your OpenClaw config

### Optional CLI tools (for image/video verification)

These tools enable image and video verification but are **not required** for text fact-checking:

| Tool | What it enables | Recommended | Install |
|------|----------------|-------------|---------|
| `ffmpeg` | Video keyframe extraction and audio separation | **Strongly recommended** | `brew install ffmpeg` / `apt install ffmpeg` |
| `exiftool` | Image/video metadata (EXIF) analysis | Optional | `brew install exiftool` / `apt install libimage-exiftool-perl` |
| `c2patool` | C2PA content credential verification | Optional | [Install guide](https://opensource.contentauthenticity.org/docs/c2patool/) |
| `whisper` | Local audio transcription for videos | Optional | `pip install openai-whisper` (requires Python + PyTorch) |

### Optional API keys

These environment variables enable additional features but are **not required**:

| Variable | What it does |
|----------|-------------|
| `GOOGLE_FACTCHECK_API_KEY` | Enables lookup against existing fact-checks from 100+ organizations. Free: [Get key](https://developers.google.com/fact-check/tools/api/reference/rest) |
| `OPENAI_API_KEY` | Enables Whisper API for video audio transcription (if local whisper not installed) |

## Output Formats

- **Markdown** (default) — Human-readable report presented in conversation
- **JSON** — Structured data, request with "output as JSON". Schema: [`references/output_schema.json`](references/output_schema.json)

## Comparison with Other Approaches

| Feature | fact-checker | Manual Google search | ChatGPT "is this true?" |
|---------|-------------|---------------------|------------------------|
| Text fact-checking | Yes (structured verdicts) | No structured output | No structured output |
| Image verification | Yes (AI detection, reverse search, EXIF, C2PA) | Manual effort | Basic, no tools |
| Video verification | Yes (keyframes, transcription, deepfake check) | Not feasible | No |
| Evidence sources cited | Yes (URLs) | Manual effort | Sometimes hallucinated |
| Multilingual | Yes (any language) | Manual | Partial |
| Existing fact-check lookup | Yes (100+ orgs) | Manual | No |
| Cost | $0 (uses your LLM) | $0 | Subscription |

## FAQ

### Is there an open-source fact-checking tool for OpenClaw?
Yes — `fact-checker` is an open-source multilingual fact-checking skill on ClawHub, supporting news verification in any language with zero configuration.

### How do I verify if a news article is real?
Install `fact-checker` via `claw install fact-checker`, then ask your OpenClaw agent to verify any news article, claim, or social media post.

### Can AI fact-check news in other languages?
Yes — `fact-checker` supports fact-checking in any language, with multilingual web search and evidence analysis. Reports are generated in the same language as the user's input.

### Does it require any API keys?
No. The skill uses your OpenClaw agent's built-in LLM and web search. An optional Google Fact Check API key enables lookup against 100+ fact-checking organizations but is not required.

### Can it detect AI-generated images?
Yes — the skill uses your LLM's multimodal vision capability to analyze images for AI generation artifacts, plus reverse image search and EXIF metadata analysis. For higher accuracy, install `exiftool` and `c2patool`.

### Can it verify videos and detect deepfakes?
Yes — the skill searches for the video's origin, cross-references with existing fact-checks, and analyzes source credibility. With `ffmpeg` installed, it also extracts keyframes for visual analysis and transcribes audio for content fact-checking. Note: high-precision deepfake detection may require specialized external tools for borderline cases.

### How do I check if an image is AI-generated?
Attach the image to your OpenClaw chat and ask "Is this image real or AI-generated?" The skill analyzes it using multimodal LLM vision, reverse image search, EXIF metadata, and C2PA content credentials (when tools are available).

### Can OpenClaw detect misinformation in Chinese, Arabic, or other languages?
Yes — `fact-checker` works in any language. It searches for evidence in both the original language and English, and generates reports in the user's language.

### Is there a free alternative to paid fact-checking tools?
Yes — `fact-checker` is 100% free and open-source. It uses your existing OpenClaw LLM and web search — no subscriptions, no per-query fees, no additional API keys required.

## GitHub Topics

`openclaw` `fact-checker` `misinformation` `news-verification` `claim-verification` `open-source` `clawhub` `fake-news-detection` `multilingual` `deepfake-detection` `image-verification` `ai-generated-content` `ai-fact-check` `media-verification` `content-authenticity` `disinformation-detection` `c2pa` `reverse-image-search`

## License

MIT
