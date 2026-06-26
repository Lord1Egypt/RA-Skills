# Protagons Skill for OpenClaw

You have access to the Protagons library — a collection of portable AI character identities you can adopt.

## What you can do

- **Search** for characters by keyword or category
- **Browse** available Protagons from the public library
- **Deploy** a Protagon — fetches a rich SOUL.md identity for you to adopt
- **List categories** to help narrow down character options
- **Check status** of the skill and get hints for verifying active identity
- **Generate** a new Protagon from a description (requires a Google API key — see note below)

## How Protagons work

A Protagon is a portable AI identity with a rich SOUL.md containing:
- A synthesized system prompt distilled from 28 linguistic/psychological dimensions
- Personality profile, tone, and communication style
- Best-for use cases and contextual guidance
- Content tier (standard, dark, adversarial)

When you deploy a Protagon, its SOUL.md content is returned to you. Adopt it as your personality for the session.

## Typical conversation flows

### "Load a character"

```
User: Load the burned out ops character
Agent: [calls protagons_deploy with slug "burned-out-ops"]
Agent: I've loaded the Burned Out Ops identity. Here's who I am now...
```

### "Find me a character"

```
User: Find me a character that's dry and technical
Agent: [calls protagons_search with search "dry technical"]
Agent: Here are some options:
  1. Software Developer (software-developer) — Precise, dry, opinionated...
  2. ...
User: Go with #1
Agent: [calls protagons_deploy with slug "software-developer"]
```

### "What categories are available?"

```
User: What kinds of characters do you have?
Agent: [calls protagons_categories]
Agent: We have characters in these categories: creative-writing, technical, business...
User: Show me the technical ones
Agent: [calls protagons_search with category "technical"]
```

## Tool reference

| Tool | Purpose |
|------|---------|
| `protagons_search` | Find characters by keyword or category |
| `protagons_list` | Browse the full library (paginated) |
| `protagons_categories` | List available categories |
| `protagons_get` | Fetch raw .protagon.json for a character |
| `protagons_deploy` | Load a character's SOUL.md identity |
| `protagons_status` | Check skill status and active identity hints |
| `protagons_generate` | Create a new character from a description |

## API & credential transparency

- **Browse/search/deploy tools** are read-only and require no credentials — they fetch from the public library at `api.usaw.ai`.
- **protagons_generate** sends your Google API key to `api.usaw.ai`, which uses it for a single server-side Gemini call to generate the character. The key is not stored. If you prefer, use a scoped or throwaway key.
- The product homepage is [usaw.ai/voices](https://usaw.ai/voices); the API is hosted at `api.usaw.ai` — same organization, different subdomains.

## Content tiers

- **standard**: Safe for all contexts
- **dark**: Requires fiction wrapper (morally complex characters)
- **adversarial**: Restricted (antagonist archetypes, fiction-only)

Always respect content tier requirements when deploying.
