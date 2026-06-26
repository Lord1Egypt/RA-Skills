# Future Improvement Research

> Researched 2026-04-05. Findings for improving meme generation capabilities.

## 1. AI Image Generation for Memes

### APIs Investigated

| Service | Text Rendering | Cost/Image | Verdict |
|---------|---------------|------------|---------|
| **Replicate — Ideogram V3 Turbo** | Best-in-class | ~$0.03 | Top recommendation |
| **Replicate — FLUX.2 Flex** | Strong | ~$0.04 | Good alternative |
| **OpenAI gpt-image-1** | Strong | ~$0.04 | Content-filtered |
| **FLUX.1 Schnell** | Poor (garbled) | ~$0.003 | Backgrounds only |
| **Stability AI (SDXL, SD3)** | Poor | Varies | Skip |

### Recommended Tiered Approach

1. **Default**: memegen.link for classic template memes (free, instant, reliable)
2. **Custom AI memes**: Replicate + Ideogram V3 Turbo ($0.03/image) when no template fits
3. **Budget option**: FLUX.1 Schnell for backgrounds ($0.003) + Pillow text overlay

### Cost Estimate (20 memes/day)

| Approach | Cost/meme | Monthly |
|----------|-----------|---------|
| memegen.link | Free | $0 |
| FLUX.1 Schnell + Pillow text | $0.003 | $1.80 |
| Ideogram V3 Turbo | $0.03 | $18 |
| gpt-image-1 | $0.04 | $24 |

## 2. GIF/Video Meme Generation

### Best Free Approach: Giphy + FFmpeg

1. Search Giphy for a reaction GIF by keyword
2. Download the GIF
3. Use FFmpeg `drawtext` to add Impact-font top/bottom text
4. Output as captioned GIF

```bash
# Text on GIF with palette optimization
ffmpeg -i input.gif -vf "\
  drawtext=text='TOP TEXT':fontfile=Impact.ttf:fontsize=48:fontcolor=white:borderw=3:bordercolor=black:x=(w-tw)/2:y=20,\
  drawtext=text='BOTTOM TEXT':fontfile=Impact.ttf:fontsize=48:fontcolor=white:borderw=3:bordercolor=black:x=(w-tw)/2:y=h-th-20,\
  split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse" \
  -y output.gif
```

### Video to Captioned GIF

```bash
ffmpeg -i input.mp4 -t 5 -vf "\
  fps=15,scale=480:-1:flags=lanczos,\
  drawtext=text='TEXT':fontfile=Impact.ttf:fontsize=36:fontcolor=white:borderw=2:bordercolor=black:x=(w-tw)/2:y=20,\
  split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse" \
  -y output.gif
```

### Video Meme APIs

| Service | API? | Pricing | Notes |
|---------|------|---------|-------|
| Shotstack | Yes | $0.30/min | JSON-based video composition |
| Creatomate | Yes | ~$0.007/image | REST API |
| Kapwing | No | N/A | Web editor only |
| Imgflip Premium | Yes | $9.99/mo | `/caption_gif` endpoint |

## 3. Dead Ends (Don't Pursue)

| Service | Why |
|---------|-----|
| KnowYourMeme | No API, no programmatic access |
| Tenor API | Discontinued January 2026 |
| Kapwing/Clipchamp | No public APIs |
| Stable Diffusion for text | Poor text rendering |
| Embeddings for template matching | Overkill at <50 templates |
| Spanish meme website APIs | None exist |

## 4. Priority-Ranked Improvements

### Tier 1: High Impact, Low Effort

| Improvement | Effort | Cost |
|-------------|--------|------|
| Enrich template descriptions with rhetorical patterns | 1-2 hrs | Free |
| Two-stage selection prompt (pattern → template) | 30 min | Free |
| Curate Latin American template URLs | 1 hr | Free |
| Add Giphy search for reaction GIFs | 30 min | Free |

### Tier 2: Medium Effort, High Value

| Improvement | Effort | Cost |
|-------------|--------|------|
| Reddit OAuth for r/MemeTemplates trending | 2-3 hrs | Free |
| FFmpeg GIF captioning pipeline | 2 hrs | Free |
| Spanish subreddits as template sources | 30 min | Free |

### Tier 3: Higher Cost, Premium Features

| Improvement | Effort | Cost |
|-------------|--------|------|
| Replicate integration (Ideogram V3 Turbo) | 3-4 hrs | $0.03/meme |
| Imgflip Premium for GIF captioning | 1 hr | $9.99/mo |
| FLUX.1 Schnell backgrounds + Pillow | 2 hrs | $0.003/meme |
