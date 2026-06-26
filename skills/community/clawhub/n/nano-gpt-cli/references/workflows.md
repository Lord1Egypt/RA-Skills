# NanoGPT Workflows

## One-shot answer

```bash
./scripts/prompt.sh "Write a concise release note for these changes."
```

## Multimodal prompt

```bash
./scripts/prompt.sh "Extract the visible error message from this screenshot." --image ./output/screenshot.png
```

## Machine-readable result

```bash
./scripts/prompt.sh "Return a JSON object with summary and risks." --json
```

## Interactive session

```bash
./scripts/chat.sh "You are helping with a TypeScript CLI."
```

Useful chat commands:

- `/clear`
- `/model MODEL_NAME`
- `/exit`

## Image generation

```bash
./scripts/image.sh "A flat lay of developer tools on a walnut desk" --output output/devtools.png
```

## Video generation

```bash
./scripts/video.sh "A cinematic drone flyover of a neon coastal city at dusk" --duration 5 --output output/neon-city.mp4
```

For long renders, return the async id first and check later:

```bash
./scripts/video.sh "Animate this storyboard into a teaser shot" --image ./storyboard.png --no-wait
nano-gpt video-status REQUEST_ID --output output/teaser.mp4
```
