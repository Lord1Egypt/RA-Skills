---
name: litellm-vertex-codex
description: Configure OpenAI Codex CLI to use Vertex AI Gemini models via LiteLLM. A guide for translating strict Codex requests for Gemini compatibility.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [Coding-Agent, Codex, Vertex-AI, Gemini, LiteLLM, Proxy]
    related_skills: [codex, claude-code]
---

# LiteLLM to Vertex AI Setup for Codex

This skill describes how to configure the OpenAI Codex CLI agent to communicate with Google's Vertex AI Gemini models using LiteLLM as a protocol translation proxy.

Codex requires a strict OpenAI response format and specific roles (`user`, `assistant`/`model`) which native Gemini or lightweight proxies (like CLIProxyAPI) do not perfectly support. LiteLLM is required to strip unsupported parameters and format the requests.

## Prerequisites

- `codex` CLI installed (`npm install -g @openai/codex`)
- `litellm` installed and running locally
- Google Cloud Platform (GCP) Project ID with Vertex AI API enabled
- Vertex AI authentication configured (e.g., Application Default Credentials)

## 1. LiteLLM Configuration

You need to create a `config.yaml` for LiteLLM that drops complex parameters and sets content to simple strings, then routes a `codex` model alias to your Gemini Vertex endpoint.

Create or update your `config.yaml` (e.g., `/app/config.yaml`):

```yaml
litellm_settings:
  drop_params: true
  set_content_to_str: true # Crucial for Codex: forces complex system prompts into simple strings

model_list:
  - model_name: gemini-3.1-pro-preview
    litellm_params:
      model: vertex_ai/gemini-3.1-pro-preview
      vertex_project: your-gcp-project-id
      vertex_location: global
      drop_params: true
      
  # Create aliases for Codex to use
  - model_name: codex
    litellm_params:
      model: vertex_ai/gemini-3.1-pro-preview
      vertex_project: your-gcp-project-id
      vertex_location: global
      drop_params: true
```

Run LiteLLM with this config (e.g., `litellm --config /app/config.yaml --port 4000`).

## 2. Codex Configuration

Codex stores its configuration in `~/.codex/config.toml`. You must configure it to point to your local LiteLLM instance and specifically request the `responses` wire API, as Codex has deprecated the `chat` wire API.

Update `~/.codex/config.toml`:

```toml
# Use the custom LiteLLM provider
model_provider = "litellm"
# The model name here MUST match the `model_name` in your LiteLLM config
model = "gemini-3.1-pro-preview" 
model_reasoning_effort = "high"

[model_providers.litellm]
name = "litellm"
# Point to your local LiteLLM instance
base_url = "http://127.0.0.1:4000/v1"
# Crucial: Codex will error out if this is set to "chat"
wire_api = "responses" 

[projects."/path/to/your/workspace"]
trust_level = "trusted"
```

## 3. Shell Environment

Codex expects `OPENAI_API_KEY` to be set, even when using a custom proxy that doesn't require an actual OpenAI key.

Add this to your shell profile (`~/.bashrc` or `~/.zshrc`):

```bash
export OPENAI_API_KEY="sk-litellm"
```

## 4. Verification

To verify the setup is working, run Codex in a temporary git repository (Codex refuses to run outside a git repo):

```bash
cd $(mktemp -d) && git init && codex exec 'hello'
```

If successful, Gemini will respond via the Codex CLI interface.

## Troubleshooting

- **`wire_api = "chat"` is no longer supported**: Ensure `wire_api = "responses"` is set in `~/.codex/config.toml`.
- **`Please use a valid role: user, model.`**: This means your proxy isn't correctly translating the OpenAI `assistant` or `system` roles to Gemini's expected format. Ensure you are using LiteLLM (not CLIProxyAPI) and that `set_content_to_str: true` is enabled in LiteLLM config.
- **Hanging Commands / No Output**: Ensure `pty=true` is used if calling Codex programmatically via Hermes, or that you are running it in an interactive terminal.
