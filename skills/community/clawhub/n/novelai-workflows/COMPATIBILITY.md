# Compatibility notes

This is a sanitized summary of the API-level validation performed on 2026-09-05. It contains no credentials, account identifiers, or generated test files.

## Verified

- NovelAI account authentication and subscription queries;
- text model discovery;
- Xialong completion;
- GLM-4.6 streaming chat;
- tag suggestions;
- V5 text-to-image;
- V4.5 multi-character generation;
- img2img;
- V4.5 inpainting;
- Vibe encoding and transfer;
- ControlNet annotation;
- Director tools: line art, sketch, background removal, declutter, colorize, and emotion.

## Limitations

- Prefer streaming for GLM-4.6. A non-streaming request may return HTTP 200 with an empty text field.
- The dedicated `/ai/upscale` route returned HTTP 404 on both tested NovelAI image hosts. Treat `upscale_image` as unavailable unless the active server returns an image; larger-resolution img2img or a local upscaler is a different fallback.
- The reference deployment pins `novelai-image-mcp==0.4.0`. Re-check the upstream package and rerun the live suite before changing this pin.
- API-level validation does not replace an MCP handshake and tool-discovery check on the target OpenClaw host.
