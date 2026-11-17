# OpenClaw NovelAI

An unofficial OpenClaw Skill for NovelAI fiction and image workflows.

The project adds a workflow layer around NovelAI text generation and the upstream [NovelAI-Image-MCP](https://github.com/xinvxueyuan/NovelAI-Image-MCP). It helps an OpenClaw agent maintain story context, plan chapter illustrations, choose image operations, request cost confirmation, and record reproducible assets.

The Skill name is `openclaw-novelai`; the ClawHub slug is `novelai-workflows`.

- GitHub: [techotaku39/openclaw-novelai](https://github.com/techotaku39/openclaw-novelai)
- ClawHub: [@techotaku39/novelai-workflows](https://clawhub.ai/techotaku39/skills/novelai-workflows)
- Install from ClawHub: `openclaw skills install @techotaku39/novelai-workflows`

> This project is not affiliated with or endorsed by OpenClaw or NovelAI.

## What it does

- Maintains bounded fiction context from `canon.md`, `memory.md`, `lorebook.md`, and `style.md`.
- Supports outline, continuation, rewrite, review, and summary workflows.
- Orchestrates NovelAI text models through an OpenAI-compatible provider.
- Delegates image operations to the upstream NovelAI Image MCP server.
- Covers text-to-image, multi-character prompting, img2img, inpainting, Vibe, Director tools, ControlNet annotation, tag suggestions, and account/cost checks when the active server exposes them.
- Records model, prompt, seed, dimensions, tool, and output paths without storing credentials.
- Includes a redacted live API capability suite and offline contract tests.

This Skill is an orchestration guide, not a replacement image API implementation. The MCP server remains the runtime that calls NovelAI's image endpoints.

## Documentation

- [简体中文 README](README.zh-CN.md)
- [English full user manual](docs/FULL-USER-MANUAL.md)
- [English quick-start guide](docs/QUICK-START.md)
- [Chinese full user manual](docs/完整使用手册.md)
- [Chinese quick-start guide](docs/快速入门用法.md)
- [Costs and quotas](docs/COSTS-AND-QUOTAS.md) — NovelAI Anlas, Opus free images, and V5 usage limits.
- [费用与额度说明](docs/费用与额度说明.md)
- [Zero-Anlas variant](variants/openclaw-novelai-free/README.md) — restricted mode that never falls back to paid image operations.
- [零 Anlas 中文变体](variants/openclaw-novelai-free/README.zh-CN.md)
- [Opus free enhancement variant](variants/openclaw-novelai-opus-free/README.md) — Opus-only zero-Anlas img2img, inpainting, annotation, pre-encoded Vibe, and tested-free Director subset.
- [Opus 免费增强中文变体](variants/openclaw-novelai-opus-free/README.zh-CN.md)
- [Compatibility notes](COMPATIBILITY.md) — sanitized capability and limitation summary.

## Repository layout

```text
SKILL.md
README.md
README.zh-CN.md
LICENSE
NOTICE.md
SECURITY.md
CONTRIBUTING.md
CHANGELOG.md
.clawhubignore
docs/
  COSTS-AND-QUOTAS.md
  FULL-USER-MANUAL.md
  QUICK-START.md
  费用与额度说明.md
  完整使用手册.md
  快速入门用法.md
variants/
  openclaw-novelai-free/
    SKILL.md
  openclaw-novelai-opus-free/
    SKILL.md
    README.md
    README.zh-CN.md
examples/
  openclaw.config.example.json5
scripts/
  project_state.py
  live_api_test.py
tests/
  test_project_state.py
  test_live_api_test.py
  test_skill_contract.py
```

`SKILL.md` stays at the repository root so it can be installed as a local or Git-backed OpenClaw Skill.

## Runtime model

The reference configuration uses:

- NovelAI text provider: `https://text.novelai.net/oa`;
- text models: `xialong-v1` and `glm-4-6`;
- upstream image MCP: `novelai-image-mcp==0.4.0`;
- credential source: a host-managed `NOVELAI_TOKEN` environment variable or an equivalent SecretRef.

Keep credentials outside the repository, prompts, logs, generated metadata, and command arguments. Do not replace `${NOVELAI_TOKEN}` in the example configuration with a real value.

See [examples/openclaw.config.example.json5](examples/openclaw.config.example.json5) for the configuration relationship. Merge it into an existing OpenClaw configuration instead of overwriting unrelated settings.

## Example requests

```text
Read the current project's canon, memory, lorebook, and style. Propose three directions for chapter three and wait for confirmation before drafting.
```

```text
Find the key scenes in chapter three, draft image prompts, estimate the total cost, and wait for confirmation before generating anything.
```

```text
Use this image for img2img. Keep the face and composition, change the background to a rainy street, preserve the original, and save the result as a new asset.
```

```text
Use this image and mask to inpaint only the right hand. Keep all unmasked areas unchanged and record the generation parameters.
```

## Safety behavior

The Skill instructs the agent to:

- never ask for or repeat a NovelAI token in chat;
- inspect available MCP tools before model-specific operations;
- show model, resolution, steps, sample count, and estimated cost before ambiguous or batch image work;
- preserve source images and write edited results separately;
- record safe metadata without credentials;
- report a failed operation as failed instead of inventing an output.

Third-party Skills and MCP servers should be reviewed before enabling. The upstream MCP server is an independent dependency; see its own license and security policy.

## Current compatibility notes

The included API suite was run on 2026-09-05. It verified account access, Xialong completion, GLM-4.6 streaming chat, V5/V4.5 image generation, multi-character prompts, img2img, inpainting, Vibe, tag suggestions, ControlNet annotation, and Director tools.

- Prefer streaming for GLM-4.6; a non-streaming request may return HTTP 200 with empty text.
- The dedicated NovelAI `/ai/upscale` route returned 404 on both tested image hosts. Treat `upscale_image` as unavailable unless the active server returns an image; use larger-resolution img2img or a local upscaler as a different operation.
- The target OpenClaw host still needs its own MCP handshake and tool-discovery check.

NovelAI and OpenClaw may change independently. Re-run the live smoke suite and update `COMPATIBILITY.md` before changing the upstream version pin.

## Development checks

The offline test suite must not require a Token:

```powershell
python -m unittest discover -s tests -v
python -m py_compile scripts\project_state.py scripts\live_api_test.py tests\test_project_state.py tests\test_skill_contract.py tests\test_live_api_test.py
```

The live suite is opt-in and reads `NOVELAI_TOKEN` only from the process environment. Never paste a credential into a command or commit live output artifacts.

## Publishing

Recommended distribution:

1. Use GitHub as the canonical source repository.
2. Tag releases and keep the `SKILL.md` frontmatter name stable.
3. Publish or sync the Skill to [ClawHub](https://clawhub.ai/) as `novelai-workflows`.
4. Keep generated images, account-specific reports, `.env` files, caches, and archives out of the public repository.

See [CONTRIBUTING.md](CONTRIBUTING.md), [SECURITY.md](SECURITY.md), and [NOTICE.md](NOTICE.md) before publishing.

## References

- [OpenClaw Skills](https://docs.openclaw.ai/skills)
- [OpenClaw ClawHub quickstart](https://docs.openclaw.ai/clawhub/quickstart)
- [NovelAI Image MCP](https://github.com/xinvxueyuan/NovelAI-Image-MCP)
- [NovelAI image models](https://docs.novelai.net/en/image/models/)
- [NovelAI text models](https://docs.novelai.net/en/text/models/)
- [NovelAI persistent API token](https://docs.novelai.net/en/text/usersettings/account/)
