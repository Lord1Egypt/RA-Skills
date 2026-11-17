---
name: makemidas
description: Generate AI images and short videos with the MakeMidas CLI (Nano Banana, GPT Image, Seedream, Flux, Seedance, Kling, Veo, Wan…), from a prompt, reference images or a first and last frame, and save them to disk. Use when the user asks to generate, draw or render an image, illustration, photo, product shot, cover or mockup, to animate a picture, or to make a short video clip, and wants files on their computer; also for "生成图片", "画一张", "做个视频", "图生视频". Spends the user's MakeMidas credits.
license: MIT
metadata:
  openclaw:
    requires:
      bins:
        - node
    homepage: https://makemidas.com/developers
---

# Generate images and videos with MakeMidas

The `makemidas` CLI sends a prompt to the user's MakeMidas account, waits for
the result and saves the files where you run it. Results (file paths) go to
stdout, progress to stderr. Every command takes `--json`.

## 1. Make sure the CLI runs

```bash
makemidas --version
```

If it isn't installed, use `npx -y @makemidas/cli` in place of `makemidas`
everywhere below (Node.js 20+). Ask the user before running
`npm i -g @makemidas/cli`.

## 2. Make sure the user is signed in

```bash
makemidas auth status --json
```

Exit code 3 means not signed in. Either:

- run `makemidas auth login`: it opens the browser, where the user signs in
  and allows "MakeMidas CLI", and waits up to 5 minutes. Tell the user to
  approve it in the browser; if your shell times out sooner, run it in the
  background and check `auth status` after; or
- ask the user for an API key (Settings → API keys on makemidas.com) and run
  with `MAKEMIDAS_API_KEY` set in the environment. Never write the key into
  files or the conversation.

## 3. Check credits and pick a model

```bash
makemidas credits --json
makemidas models --json            # or --kind image / --kind video
```

Every generation costs credits. Unless the user asks for something else:
one output, the default (cheapest usable) model, `1:1` for images. Tell the
user what a run will cost when it is more than a few credits (videos,
4K, several outputs). Free accounts get 10 credits a day, the free models
only and watermarked images; videos need a plan or credit pack.

## 4. Generate

```bash
makemidas image "a red fox in fresh snow, golden hour, 35mm film" --aspect 3:2 --json
makemidas image "same fox as a watercolor" --ref fox.png --model <id> --json
makemidas video "the fox looks up and the snow starts falling" --ref fox.png --duration 5 --json
```

- `--model <id>` from `makemidas models`; `--aspect`, `--resolution`
  (`1K|2K|4K` for images, `480p|720p|1080p` for videos), `--count 1-4`.
- `--ref <file|url>` adds a reference image (repeat for more). For videos one
  image is the first frame, two are the first and last frame; `--frame-mode
  reference` uses them as references instead (Seedance).
- `--duration <s>` and `--audio` for videos; `--style <id>` (photo,
  cinematic, film, anime, …); `--enhance` lets MakeMidas expand a short
  prompt.
- `--out <dir>` picks the folder (default: current directory). Files are
  named `makemidas-<id>-<n>.<ext>`; existing files are kept unless `--force`.
- `--no-download` prints signed links (valid one hour) instead of saving.

Images come back in under a minute. Videos take one to several minutes; the
CLI waits (up to `--timeout` minutes, default 15). To avoid blocking your
shell:

```bash
makemidas video "…" --no-wait --json        # prints the id, exit code 7
makemidas get <id> --wait --json            # run in the background
```

With `--json`, `image`, `video` and `get` print the generation
(`{ id, kind, model, status, credits, watermarked, outputs, files }`), where
`files` are the saved paths.

## 5. Use the result

Show the user the saved files (open or embed them if your environment can).
`makemidas list --json` lists recent generations and ids; `makemidas get <id>`
downloads one again.

## Exit codes

| Code | Meaning | What to do |
|---|---|---|
| 0 | done | |
| 2 | bad input (unknown model, unsupported ratio or size, bad file) | fix the command; check `makemidas models` |
| 3 | not signed in or sign-in expired | `makemidas auth login`, or `MAKEMIDAS_API_KEY` |
| 4 | not enough credits, paid model on a free plan, or too many running | show `makemidas credits`; plans at https://makemidas.com/pricing |
| 5 | the model could not make it (credits refunded) | show the error; change the prompt or model before retrying |
| 6 | network or server error | retry once, then report |
| 7 | video still rendering | `makemidas get <id> --wait` |

## Rules

- Generations spend the user's credits. Don't run batches, 4K or videos the
  user didn't ask for; ask first when the cost is unclear.
- Don't generate images of real people without their consent, or content the
  user would not want stored in their MakeMidas account.
- Never print, log or copy tokens, `MAKEMIDAS_API_KEY` or the credentials
  file (`~/.config/makemidas/credentials.json`).
- In ChatGPT, Claude or another MCP client, the MakeMidas MCP server
  (`https://makemidas.com/api/mcp`) does the same without the CLI.
