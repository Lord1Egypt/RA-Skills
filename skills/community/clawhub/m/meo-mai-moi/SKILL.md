---
name: meo-mai-moi
description: "Use for Meo Mai Moi pet-owner tasks when an agent needs to help a user manage their pets through the documented API: listing pets, updating pet profiles, adding weights, vaccinations, medical records, or microchips, understanding helper profiles, or navigating placement workflows. Also use when the user asks how to authenticate to Meo Mai Moi, how to install or configure this skill, which prompts to give their agent, or how to safely automate day-to-day pet-management actions without guessing undocumented routes."
---

# Meo Mai Moi

Use this skill for user-facing pet-management help on Meo Mai Moi. Prefer documented `/api/*` endpoints and avoid inventing routes or payload fields.

## Required user setup

Meo Mai Moi is hosted at https://meo-mai-moi.com. Before an agent can use Meo Mai Moi for a user, the user must manually sign in or register there, then create a personal API key/token at https://meo-mai-moi.com/developer.

The user should provide that key to their agent securely, ideally as a local secret or environment variable, not by pasting it into public chats, shared prompts, GitHub issues, logs, or commits.

Without this API key, the agent cannot access the user's pets or account data through the API.

Useful official links:

- App: https://meo-mai-moi.com
- API token page: https://meo-mai-moi.com/developer
- Docs: https://meo-mai-moi.com/docs
- API integration guide: https://meo-mai-moi.com/docs/api-integration.html
- Project page: https://project.meo-mai-moi.com

## Load the right reference

Read only the reference file you need:

- Read `references/api.md` for authentication, response format, documented endpoints, and API usage rules.
- Read `references/domain-model.md` for pet, helper, relationship, and placement concepts.
- Read `references/workflows.md` for task playbooks and safe execution patterns.
- Read `references/examples.md` when the user asks how to install the skill, configure token loading, or phrase requests to their agent.

## Working rules

- Prefer read operations first to discover current state before proposing or making updates.
- Treat personal access tokens as bearer secrets. Load them from a local env file; never paste them into chat, commits, logs, or generated docs.
- Assume the stable external contract is the documented pet-management slice unless the user explicitly says to work with another route and you can verify it.
- Send `Accept: application/json` and `Authorization: Bearer <token>` for PAT-backed requests.
- Expect the standard API envelope. Success is usually `{ success: true, data, message? }`. Errors are usually `{ success: false, data: null, message, error?, errors? }`.
- Respect documented abilities: `read`, `create`, `update`, `delete`.
- Do not assume PATCH support for pets. Use the documented methods.
- For destructive changes like delete, ownership transfer, or status changes with real-world consequences, confirm intent unless the user clearly asked for that exact action.
- When the task needs domain nuance, read the domain reference before acting. The app has relationship-based access and placement-specific lifecycle rules that are easy to mangle if you wing it.

## Output expectations

When helping with Meo Mai Moi tasks:

- Be explicit about which endpoint and method you are using.
- Surface important constraints before risky writes.
- If the contract looks incomplete for the requested task, say so plainly and stop guessing.
- Prefer compact examples over long tutorials.
- Default to the pet owner's perspective unless the user clearly asks for developer or backend-contract analysis.
