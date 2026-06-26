# GitHub Copilot Extension Planning Package

This adapter is a marketplace planning package for a future supported GitHub Copilot integration.

Current publication boundary:

- GitHub App-based Copilot Extensions are no longer the primary route.
- VS Code Copilot Extensions remain a supported distribution surface.
- Marketplace submission still requires publisher approval and a complete, runnable package.
- Any hosted bridge must convert Copilot chat requests into approved workspace actions.

Recommended implementation:

- build a VS Code Copilot Extension wrapper or another currently supported Copilot surface
- expose the same operations as `platforms/openai-gpt/actions-openapi.yaml`
- enforce workspace approval and path boundaries
- return generated cockpit summaries as Markdown

Do not submit this adapter as a complete extension until the supported Copilot surface exists and has been tested.
