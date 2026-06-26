# Mascot Generator

Generate custom brand mascots and cartoon characters from text descriptions using AI. Perfect for small businesses, startups, sports teams, schools, gaming clans, esports crews, and YouTube channels that need a unique company mascot, brand character, cute logo mascot, team figure, or memorable brand identity illustration — all created from a simple written prompt.

Powered by the Neta AI image generation API (api.talesofai.com) — the same service as neta.art/open.

## Install

Using the ClawHub skills CLI:

```bash
npx skills add blammectrappora/mascot-generator
```

Or using clawhub directly:

```bash
clawhub install mascot-generator
```

## Usage

```bash
node mascotgenerator.js "your description here" --token YOUR_TOKEN
```

### Examples

Generate a coffee shop mascot:

```bash
node mascotgenerator.js "a smiling coffee bean character wearing a barista apron, holding a tiny cup" --token YOUR_TOKEN
```

Generate an esports team mascot in landscape:

```bash
node mascotgenerator.js "fierce wolf mascot for an esports team, wearing headphones, neon accents" \
  --token YOUR_TOKEN \
  --size landscape
```

Use a reference image UUID for style inheritance:

```bash
node mascotgenerator.js "friendly robot mascot for a tech startup" \
  --token YOUR_TOKEN \
  --ref 123e4567-e89b-12d3-a456-426614174000
```

## Options

| Flag       | Description                                                       | Default  |
| ---------- | ----------------------------------------------------------------- | -------- |
| `--token`  | Neta API token (required)                                         | —        |
| `--size`   | Output aspect: `square`, `portrait`, `landscape`, `tall`          | `square` |
| `--ref`    | Reference image UUID for style inheritance                        | —        |
| `-h`, `--help` | Show help                                                     | —        |

### Sizes

| Name        | Dimensions   |
| ----------- | ------------ |
| `square`    | 1024 × 1024  |
| `portrait`  | 832 × 1216   |
| `landscape` | 1216 × 832   |
| `tall`      | 704 × 1408   |

## Token setup

This skill requires a Neta API token (free trial available at <https://www.neta.art/open/>).

Pass it via the `--token` flag:

```bash
node <script> "your prompt" --token YOUR_TOKEN
```

## Output

Returns a direct image URL.

