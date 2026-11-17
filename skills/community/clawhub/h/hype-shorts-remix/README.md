# Hype Shorts Remix

Turn viral references into fresh scripts, captions and short videos you can edit.

See [SKILL.md](SKILL.md) for the complete workflow and [setup](references/setup.md) for requirements. Node.js 22+, FFmpeg and FFprobe are required.

The Skill is free. New image/video generation uses your own [APIsRouter account](https://apisrouter.com) and is billed separately. Local inspection and the included example work without an API key.

## Local example

```sh
node scripts/media.mjs render --project examples/edit.json --output rain-remix.mp4
```

The latest independent video API check was acknowledged but reached a failed terminal state. The local five-second render passed. See the generation guide for supported parameters and availability limits.
