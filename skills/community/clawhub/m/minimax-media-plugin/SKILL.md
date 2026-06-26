---
name: minimax-media-plugin
description: Install, configure, verify, or troubleshoot the @jwongart/openclaw-minimax-media OpenClaw plugin for MiniMax image understanding, image generation, music generation, video generation, text-to-speech, and web search tools.
---

# OpenClaw MiniMax Media Plugin

Use this skill when the user wants to install, update, configure, verify, or troubleshoot the `@jwongart/openclaw-minimax-media` OpenClaw plugin.

## Package

- npm package: `@jwongart/openclaw-minimax-media`
- OpenClaw plugin ID: `openclaw-minimax-media`
- GitHub: `https://github.com/jwong-art/openclaw-minimax-media`
- npm install spec: `npm:@jwongart/openclaw-minimax-media`

The npm package is scoped, but the OpenClaw plugin ID is intentionally unscoped. Configure it under `plugins.entries.openclaw-minimax-media`.

## Install

Install the plugin:

```bash
openclaw plugins install npm:@jwongart/openclaw-minimax-media --pin
```

Install a specific version:

```bash
openclaw plugins install npm:@jwongart/openclaw-minimax-media@0.8.8 --pin
```

After installation, restart the OpenClaw gateway if the CLI says a restart is required.

## Configuration

Configure the MiniMax API key in OpenClaw config:

```json
{
  "plugins": {
    "entries": {
      "openclaw-minimax-media": {
        "enabled": true,
        "config": {
          "apiKey": "YOUR_MINIMAX_CODING_PLAN_API_KEY"
        }
      }
    }
  }
}
```

The plugin can also read these environment variables:

```bash
MINIMAX_CODE_PLAN_KEY
MINIMAX_CODING_API_KEY
MINIMAX_API_KEY
MINIMAX_API_HOST
```

Do not commit real API keys or tokens.

## Tools

The plugin registers these OpenClaw tools:

- `minimax_image`
- `minimax_image_generate`
- `minimax_music_generate`
- `minimax_video_generate`
- `minimax_tts`
- `minimax_web_search`

## Verification

Check the installed package and plugin ID:

```bash
node -e "const p=require('/root/.openclaw/npm/node_modules/@jwongart/openclaw-minimax-media/package.json'); const m=require('/root/.openclaw/npm/node_modules/@jwongart/openclaw-minimax-media/openclaw.plugin.json'); console.log({ packageName: p.name, version: p.version, pluginId: m.id })"
```

Check the OpenClaw plugin list:

```bash
openclaw plugins list | rg -C 4 'openclaw-minimax-media|MiniMax Media|@jwongart'
```

If the plugin was just installed or updated but tools are not available yet, restart the OpenClaw gateway before deeper debugging.

## Migration From Old Package

The old unscoped npm package `openclaw-minimax-media` is deprecated. Use:

```bash
openclaw plugins uninstall openclaw-minimax-media --force
openclaw plugins install npm:@jwongart/openclaw-minimax-media --pin
```

The OpenClaw plugin ID remains `openclaw-minimax-media`, so existing config keys can stay under `plugins.entries.openclaw-minimax-media`.
