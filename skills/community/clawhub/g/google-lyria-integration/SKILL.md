---
name: lyria
description: Generate 30-second instrumental music via Google Lyria (Vertex AI). Use when user requests music generation, specific styles/keys/instruments, or music iteration.
---

# Music Generation Skill (Lyria)

Generate instrumental music from text prompts using Google Lyria API via Vertex AI.

## Capabilities
- Generate 30-second WAV instrumental tracks optimized for short-form content
- Support style, mood, key, and instrument specifications
- Save generated music to workspace with custom or timestamped filenames
- Iterate based on user feedback

## Use Cases
- **TikTok/YouTube Shorts** — background music for 15-30s videos
- **Instagram Reels** — quick musical intros/outros
- **Video transitions** — short audio bridges
- **Loops** — repeating segments for longer content

## Limitations
- **30 seconds max** per generation (Lyria constraint)
- **Short-form only** — designed for TikTok/Reels/Shorts, not full songs
- **Instrumental only** (no vocals/lyrics)
- **Bearer token expires hourly** (requires periodic refresh)
- English prompts recommended

---

## First-Time Setup

When using this skill for the first time on a machine, follow these steps:

### Step 1: Create Directory Structure

```bash
# Create the lyria folder structure in workspace
mkdir -p ~/.openclaw/workspace/lyria/generated_music
```

### Step 2: Install gcloud CLI (if not installed)

Check if gcloud is installed:
```bash
gcloud --version
```

If not installed, install Google Cloud SDK:

**macOS (Homebrew):**
```bash
brew install --cask google-cloud-sdk
```

**Linux:**
```bash
curl https://sdk.cloud.google.com | bash
exec -l $SHELL
```

**Verify installation:**
```bash
gcloud --version
```

### Step 3: Authenticate with Google Cloud

```bash
gcloud auth login
```

Follow the browser prompt to authenticate.

### Step 4: Get Your Configuration Values

**Get project_id:**
```bash
gcloud config get-value project
```

**Get location:**
```bash
gcloud config get-value compute/region
```

If no region is set, use: `us-central1` (recommended for Lyria)

**Get bearer_token:**
```bash
gcloud auth print-access-token
```

⚠️ **Note:** This token expires in approximately 1 hour. You'll need to refresh it periodically.

### Step 5: Create Config File

Create `~/.openclaw/workspace/lyria/config.json` with your values:

```json
{
  "project_id": "your-project-id-here",
  "location": "us-central1",
  "bearer_token": "ya29.a0AfH...your-token-here",
  "output_dir": "~/.openclaw/workspace/lyria/generated_music"
}
```

Replace the placeholders with your actual values from Step 4.

---

## Usage

### Quick Generate (Shell Wrapper)

The shell wrapper is the recommended way to generate music. It reads all configuration from the config file automatically.

```bash
./scripts/music-gen.sh "<prompt>" [name]
```

**Arguments:**
- `prompt` (required): Text description of the music you want
- `name` (optional): Custom filename (without extension). If omitted, uses timestamp.

**Examples:**
```bash
# With custom name:
./scripts/music-gen.sh "chill lo-fi piano C minor" "my_relaxing_track"
# Output: ~/.openclaw/workspace/lyria/generated_music/my_relaxing_track.wav

# With timestamp (default):
./scripts/music-gen.sh "energetic rock guitar solo"
# Output: ~/.openclaw/workspace/lyria/generated_music/music_20260302_143022.wav
```

### Direct Python Usage

For more control or integration with other tools, call the Python script directly:

```bash
python3 scripts/music-gen.py <config_file> "<prompt>" [name]
```

**Arguments:**
- `config_file` (required): Path to config.json
- `prompt` (required): Text description of the music
- `name` (optional): Custom filename (without extension)

**Example:**
```bash
python3 scripts/music-gen.py ~/.openclaw/workspace/lyria/config.json "jazz saxophone smooth" "evening_jazz"
```

---

## Prompt Guidelines

Good prompts include:
- **Genre/Mood**: "chill lo-fi", "energetic rock", "melancholic jazz", "epic orchestral"
- **Key**: "C minor", "F major", "E Phrygian"
- **Instruments**: "piano, strings, soft drums", "electric guitar, bass, drums"
- **Tempo/Feel**: "slow and relaxing", "fast and driving", "mid-tempo groove"

**Example prompts:**
- `"A calm acoustic folk song in C minor with gentle guitar melody and soft strings, no drums"`
- `"Upbeat electronic dance music with strong synth bass and driving beats, 128 BPM feel"`
- `"Melancholic jazz piano in F minor with soft brush drums and upright bass"`
- `"Epic cinematic orchestral with brass and strings, heroic and uplifting mood"`

---

## Refreshing Your Bearer Token

Since tokens expire hourly, you may need to refresh during long sessions:

1. Get new token:
   ```bash
   gcloud auth print-access-token
   ```

2. Update config.json with the new token

3. Continue generating music

---

## Workflow for Agents

When a user asks you to generate music:

1. **Check if setup is complete:**
   - Verify `~/.openclaw/workspace/lyria/config.json` exists
   - If not, guide user through First-Time Setup above

2. **Check if token is valid:**
   - If generation fails with 401/403, token expired
   - Guide user to refresh token (see above)

3. **Refine the prompt:**
   - Ask user for style, mood, instruments, key if not provided
   - Help craft a descriptive prompt

4. **Generate:**
   ```bash
   ./scripts/music-gen.sh "<refined_prompt>" "<descriptive_name>"
   ```

5. **Deliver:**
   - Send the generated `.wav` file to user
   - Confirm success

6. **Iterate (if needed):**
   - Ask: "Want any changes? Faster? Different instruments?"
   - Update prompt, regenerate, deliver

---

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| Config file not found | First-time setup incomplete | Follow First-Time Setup steps |
| 401 Unauthorized | Bearer token expired or invalid | Refresh token: `gcloud auth print-access-token` |
| 403 Forbidden | No access to Lyria API | Enable Vertex AI API in Google Cloud Console |
| 404 Not Found | Project or location incorrect | Verify project_id and location in config |
| No predictions | API issue or invalid prompt | Retry with modified prompt |

---

## File Structure

```
~/.openclaw/workspace/
└── lyria/
    ├── config.json              # User credentials and settings
    └── generated_music/         # All generated audio files
        ├── music_20260302_143022.wav
        ├── my_relaxing_track.wav
        └── ...
```

---

## API Reference

- **Model**: `lyria-002`
- **Endpoint**: `https://{location}-aiplatform.googleapis.com/v1/projects/{project}/locations/{location}/publishers/google/models/lyria-002:predict`
- **Docs**: https://ai.google.dev/gemini-api/docs/music-generation
- **Pricing**: $0.06 per 30 seconds of generated music

---

## Best Practices

1. **Use specific prompts** — "jazz piano in F minor" works better than "jazz music"
2. **Specify what to exclude** — "no drums" or "no vocals" helps steer output
3. **Generate variations** — Create 2-3 versions and let user pick favorite
4. **Monitor costs** — At $0.06 per 30s, 10 generations = $0.60
5. **Refresh token proactively** — If session >45 min, get fresh token before generating

---

## Example Complete Session

```
User: Generate some lo-fi music for studying

Agent: I'll create a chill lo-fi track for you. First, let me check your setup...
[Checks config exists - yes]
[Checks token validity - yes]

Generating: "Chill lo-fi hip hop with soft piano melody, warm vinyl crackle, relaxed beats, no vocals"
...
Generated: ~/.openclaw/workspace/lyria/generated_music/lofi_study_track.wav
[Sends file]

Done! 30 seconds of chill lo-fi. Want me to make it longer by generating a continuation, or try a different vibe?
```
