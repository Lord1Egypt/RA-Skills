# Publish-All Checklist

Use this checklist to push One Person Company OS `1.0.3` across the mainstream agent markets without overstating publication status.

## Before Any Publish

- Run `python3 scripts/validate_release.py`.
- Run `python3 scripts/validate_platforms.py`.
- Confirm `git status --short` is clean or only contains intended release changes.
- Confirm `README.md`, `README.zh-CN.md`, `SKILL.md`, and `platforms/PUBLISHING-STATUS.md` match the target version.
- Confirm the platform package says files are written only inside the founder-approved workspace.

## OpenClaw / ClawHub

- Publish from the repository root with `clawhub publish`.
- Verify the ClawHub version API shows `1.0.3`.
- Download the remote package and check `README.zh-CN.md`, `agents/openai.yaml`, `platforms/PUBLISHING-STATUS.md`, and `platforms/mcp-server/server.py`.
- Record static and LLM scan verdicts before keeping the status as `published`.

## Claude Skills

- Use `platforms/claude-skill/SKILL.md` as the Claude-facing skill.
- Include the repository root package when local scripts are supported.
- If scripts are not supported, submit the prompt skill and link the GitHub/OpenClaw package as the downloadable workspace generator.
- Mark `published` only after Claude shows the skill as installed, uploaded, or shareable in the target account.

## OpenAI GPT Store

- Create the GPT using `platforms/openai-gpt/instructions.md`.
- Add knowledge from `platforms/openai-gpt/knowledge-files.txt`.
- For a prompt-only launch, do not claim file-writing actions.
- For an Actions launch, host an HTTPS API that implements `platforms/openai-gpt/actions-openapi.yaml`.
- Add a valid privacy policy URL before making a GPT with Actions public.
- Mark `published` only after the GPT Store page or builder share page is visible.

## MCP Registry / Smithery / Glama / PulseMCP

- Use `platforms/mcp-server/server.py` and `platforms/mcp-server/server.json` as the common execution package.
- Use `platforms/mcp-registries/submission-matrix.md` for per-registry metadata.
- Submit to each registry separately because namespace, indexing, and hosting requirements differ.
- Mark a registry `published` only after its listing URL or API record is visible.

## Hermes Agent / agentskills.io

- Use `platforms/hermes-agent/SKILL.md`, `SOUL.md`, `mcp-config.json`, and `install.md`.
- Use `platforms/agentskills-io/listing.md` for agentskills.io marketplace copy.
- Confirm the Hermes instance can call the MCP adapter before claiming execution support.
- Mark `published` only after the Hermes install or agentskills.io listing is visible.

## Dify Marketplace

- Package `platforms/dify-plugin/` with Dify's marketplace tooling.
- Confirm `manifest.yaml`, provider YAML, provider Python, and all tool YAML files are included.
- Keep the plugin scoped to the same approved-workspace boundary as the canonical package.
- Mark `published` only after the Dify marketplace review or listing page is available.

## GitHub Copilot Extensions

- Treat `platforms/github-copilot-extension/` as a planning package until a currently supported Copilot extension surface exists.
- Do not use the retired GitHub App Copilot Extension route as the primary submission path.
- Rebuild this adapter as a VS Code Copilot Extension or another currently supported GitHub Copilot integration before marketplace submission.
- Reuse the same action schema as the OpenAI GPT Actions bridge where possible.
- Keep status as `backend-needed` until the supported Copilot surface can run the operating cockpit workflow.

## Microsoft Copilot Studio / Commercial Marketplace

- Create the Copilot Studio agent from `platforms/microsoft-copilot-studio/agent-instructions.md`.
- Use `teams-app-manifest.template.json` only after the tenant-backed agent exists.
- Use `commercial-marketplace-notes.md` for marketplace positioning and compliance notes.
- For Commercial Marketplace, package through the supported Microsoft 365 Agents Toolkit / Partner Center route rather than treating the Copilot Studio prompt alone as a marketplace app.
- Keep status as `tenant-needed` until tenant, admin approval, and marketplace publisher account are in place.

## Poe Bots

- Create the Poe bot using `platforms/poe-bot/profile.md` and `platforms/poe-bot/prompt.md`.
- Treat it as a guided assistant, not the full local file-writing runtime.
- Mark `published` only after a public or shareable Poe bot URL exists.

## Gemini Gems

- Create the Gem using `platforms/gemini-gem/instructions.md`.
- Treat it as a guided assistant unless connected to the hosted API/MCP bridge.
- Mark `published` only after a shareable Gem URL or account-visible Gem record exists.

## Evidence To Capture

- public listing URL
- version number or publication date
- package hash or download URL
- key file check
- security scan result
- approval, rejection, or review note
