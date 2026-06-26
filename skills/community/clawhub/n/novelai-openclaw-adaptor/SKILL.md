---
name: novelai-openclaw-adaptor
description: Explain how to connect NovelAI to OpenClaw through a local OpenAI-compatible shim. Use when the user wants configuration guidance for a local NovelAI adaptor, model selection, or OpenClaw `base_url` setup.
metadata: {"openclaw":{"os":["win32","linux","darwin"]}}
---

# NovelAI OpenClaw Adaptor

Use this skill to explain how a local adaptor can bridge OpenClaw's OpenAI-style API calls to NovelAI, and how to configure OpenClaw to talk to that local endpoint.

## Scope

This skill is for explanation and local configuration guidance:

- Explain that the adaptor is a local proxy/shim, not a hosted service.
- Explain how `base_url` and model names should be configured in OpenClaw.
- Help the user choose a supported text model or image model.
- Describe the local commands a user may run after they have verified the package source.

Do not use this skill to:

- Auto-install software.
- ask the user to paste secrets into chat.
- present unverified third-party packages as implicitly trusted.

## Safety rules

Follow these rules whenever this skill is used:

1. Treat installation as optional and approval-based.
2. Before suggesting installation, tell the user to verify the package source, maintainer, and repository or project page.
3. Prefer local source checkout or an already-verified package source when available.
4. Never ask the user to paste a NovelAI API key into chat.
5. Never include secrets inline in command examples.
6. If the package source cannot be verified, stop at configuration guidance and ask the user how they want to proceed.

## Verification-first workflow

If the user wants to enable runtime use, follow this order:

1. Check whether the adaptor is already present locally or already installed.
2. If it is not present, explain that the package source should be verified before any installation.
3. Ask for approval before running any install command.
4. After the user has verified the source and approved installation, use the package's documented install method.
5. Prefer interactive or local-only credential entry during configuration.

Safe examples:

```bash
pip install novelai-openclaw-adaptor
```

```bash
novelai-config init
```

Do not use examples like:

```bash
novelai-config init --api-key "YOUR_NOVELAI_API_KEY"
```

If the user needs help deciding whether the package is trustworthy, suggest reviewing its repository, release history, and maintainers before installation.

## Supported models

Text models:

- `glm-4-6`
- `erato`
- `kayra`
- `clio`
- `krake`
- `euterpe`
- `sigurd`
- `genji`
- `snek`

Image models:

- `nai-diffusion-4-5-full`
- `nai-diffusion-4-5-curated`
- `nai-diffusion-4-full`
- `nai-diffusion-4-curated`
- `nai-diffusion-3`
- `nai-diffusion-3-furry`

When helping with setup, ask the user which model they want instead of assuming silently. If they do not care, recommend:

- Text: `glm-4-6`
- Image: `nai-diffusion-4-5-full`

## OpenClaw configuration

When explaining how to connect OpenClaw to the adaptor:

1. Set `base_url` to the local adaptor endpoint, such as `http://127.0.0.1:xxxx/v1` or `http://localhost:xxxx/v1`.
2. Set the OpenClaw model name to the adaptor-exposed model the user selected.
3. Clarify that credential handling belongs to the local adaptor configuration, not the chat.
4. If OpenClaw insists on an API key field, explain that some clients accept a placeholder value such as `sk-local`, but the real NovelAI credential should stay in the local adaptor config only.

## Helpful local commands

If the user has already verified the package source and approved local usage, these commands are relevant:

```bash
novelai-config --help
novelai-shim --help
novelai-image --help
```

Use `novelai-config init` as the normal guided setup entry point. It should collect local configuration such as:

- UI language
- NovelAI credential through local input
- Default shim model
- Default image output directory
- Default image model

## Image generation usage

Once the local adaptor is configured and running, image generation can use the normal OpenClaw or OpenAI-style prompt flow.

Example prompt:

`1girl, solo, masterpiece, best quality, highly detailed`

The adaptor is responsible for translating that prompt into the format expected by NovelAI.
