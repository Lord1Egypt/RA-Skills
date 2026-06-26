# Podcast Cover Generator

Generate professional podcast cover art and show artwork from plain text descriptions. Describe your show — the mood, subject, color palette, central visual — and get back a broadcast-quality square cover ready for Spotify, Apple Podcasts, YouTube Music, Amazon Music, and Overcast. Built for indie podcasters, podcast networks, audio creators, and show hosts who need directory-ready artwork that stands out in search results across true crime, comedy, business, interview, educational, storytelling, news, tech, and entertainment categories.

Powered by the Neta AI image generation API (api.talesofai.com) — the same service as neta.art/open.

## Install

Via the skills CLI:

```bash
npx skills add blammectrappora/podcast-cover-generator
```

Via ClawHub:

```bash
clawhub install podcast-cover-generator
```

## Usage

```bash
node podcastcovergenerator.js "your description here" --token YOUR_TOKEN
```

The first positional argument is your prompt. A cinematic podcast-cover style suffix is appended automatically, so you can focus on describing the subject.

### Examples

Generate a true-crime show cover:

```bash
node podcastcovergenerator.js "shadowy detective silhouette against a neon-lit rainy alley, moody noir atmosphere" --token YOUR_TOKEN
```

Generate a business interview podcast cover:

```bash
node podcastcovergenerator.js "confident founder portrait, clean geometric background, gold and navy palette" --token YOUR_TOKEN
```

Generate a comedy show cover in portrait orientation:

```bash
node podcastcovergenerator.js "two cartoon microphones laughing, playful pastel background" --size portrait --token YOUR_TOKEN
```

Reuse the style of an existing reference image:

```bash
node podcastcovergenerator.js "tech startup podcast, minimal circuit motif" --ref <picture_uuid> --token YOUR_TOKEN
```

### Output

Returns a direct image URL printed to stdout on success. Progress messages go to stderr, so you can pipe the URL cleanly:

```bash
URL=$(node podcastcovergenerator.js "astronomy podcast, deep space nebula" --token YOUR_TOKEN)
echo "$URL"
```

## Options

| Flag | Description | Default |
| --- | --- | --- |
| `<prompt>` | First positional argument — what you want generated | required |
| `--token` | Neta API token | required |
| `--size` | `square`, `portrait`, `landscape`, or `tall` | `square` |
| `--ref` | Reference image `picture_uuid` for style inheritance | none |
| `-h`, `--help` | Show help | — |

Size presets:

| Preset | Dimensions |
| --- | --- |
| `square` | 1024 × 1024 |
| `portrait` | 832 × 1216 |
| `landscape` | 1216 × 832 |
| `tall` | 704 × 1408 |

## Token setup

The script reads your Neta API token **only** from the `--token` command-line flag. There is no config file, no hidden lookup — whatever you pass to `--token` is what the script uses.

Pass it directly:

```bash
node podcastcovergenerator.js "a cozy storytelling podcast cover" --token sk-xxxxxxxxxxxx
```

Or expand a shell variable you set yourself:

```bash
node podcastcovergenerator.js "a cozy storytelling podcast cover" --token "$NETA_TOKEN"
```

If `--token` is missing the script exits with an error.

---

This skill requires a Neta API token (free trial available at https://www.neta.art/open/).
