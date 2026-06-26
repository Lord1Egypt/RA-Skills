---
name: microsoft-learn
description: >
  Query official Microsoft documentation for concepts, tutorials, best practices,
  working code samples, API signatures, and SDK troubleshooting. Use whenever the
  user asks about any Microsoft technology (Azure, .NET, M365, Windows, Power Platform,
  Teams, Dynamics 365, etc.)—whether understanding a concept, finding a code sample,
  or debugging Microsoft-related code. Triggers: "how does X work in Azure",
  "show me code for Y in .NET", "Microsoft docs for Z", or any MS technology question.
---

# Microsoft Learn

Search official Microsoft documentation via the `mslearn` CLI (`@microsoft/learn-cli`).

## Setup

```bash
npm install -g @microsoft/learn-cli
```

If not installed, prefix commands with `npx @microsoft/learn-cli` instead of `mslearn`.

## Commands

### search — Find documentation

```bash
mslearn search "Azure Functions Python v2 programming model"
```

Returns up to 10 results with title, URL, and content excerpt.

### code-search — Find working code samples

```bash
mslearn code-search "upload file to blob storage" --language csharp
```

Supported languages: `csharp`, `javascript`, `typescript`, `python`, `powershell`, `java`, `go`, `rust`, `ruby`, `php`

### fetch — Get full page content

```bash
mslearn fetch "https://learn.microsoft.com/..." [--section "heading"] [--max-chars 5000]
```

## When to use which

1. **User asks a concept/how-to question** → `search`
2. **User needs code examples or is debugging** → `code-search` with `--language`
3. **You already have a docs URL and need details** → `fetch`
4. **Search results are too brief** → `fetch` the URL from search results

## Tips

- Add `--json` for machine-readable output when chaining with other tools.
- If no results, rephrase with more specific Microsoft product names.
- Prefer `code-search` over `search` when the user is actively writing code.
