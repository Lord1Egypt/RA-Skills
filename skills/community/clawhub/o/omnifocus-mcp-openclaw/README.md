# OmniFocus for OpenClaw

Use this skill to review what is due, capture tasks quickly, organize projects, and work with OmniFocus in natural language from OpenClaw.

This guide explains how to install and use the `omnifocus-mcp` skill, which uses the upstream OmniFocus MCP server as the technical connection layer:

- Upstream server: [themotionmachine/OmniFocus-MCP](https://github.com/themotionmachine/OmniFocus-MCP)
- Local skill folder: [omnifocus-mcp-skill](/Users/minhdoan/Documents/Codex/2026-04-18-can-you-refactor-this-into-a/omnifocus-mcp-skill)

## Attribution

Credit for the actual OmniFocus MCP server belongs to [themotionmachine](https://github.com/themotionmachine), the creator of [OmniFocus-MCP](https://github.com/themotionmachine/OmniFocus-MCP).

This package is an OpenClaw skill wrapper around that upstream project. It does not replace or supersede the original server.

Additional credit:

- Original OmniFocus MCP server and tool implementation: [themotionmachine](https://github.com/themotionmachine)
- OpenClaw compatibility refactor and skill-packaging assistance: OpenAI
- Final testing, ownership, and ClawHub publishing: the publisher of this skill

If you publish this to ClawHub, keep the attribution above and link back to the original project homepage:

- GitHub: [themotionmachine/OmniFocus-MCP](https://github.com/themotionmachine/OmniFocus-MCP)
- npm: [omnifocus-mcp](https://www.npmjs.com/package/omnifocus-mcp)

## What this gives you

After setup, OpenClaw can use OmniFocus through MCP to:

- query tasks, projects, folders, tags, and perspectives
- add tasks and projects
- edit and remove items
- perform batch operations from notes, transcripts, or plans

## Requirements

You need:

- macOS
- OmniFocus Pro for Mac installed
- Node.js with `npm` available
- OpenClaw installed

Minimum OmniFocus guidance:

- OmniFocus Pro is required because OmniGroup documents AppleScript support as a Pro feature on Mac
- OmniFocus 3 or later is the safest minimum assumption for this skill
- OmniFocus 4.7 or later is not required for the current skill; that version only matters for future planned-date support mentioned in the upstream roadmap

Sources:

- [OmniFocus MCP README](https://github.com/themotionmachine/OmniFocus-MCP)
- [OmniFocus scripting docs](https://support.omnigroup.com/documentation/omnifocus/mac/3.12/en/print/)

## Do you need to do anything inside the OmniFocus app?

Usually, not much.

You do **not** need to:

- install an Omni Automation plug-in
- add scripts into OmniFocus manually
- change perspectives or database settings for the skill

You **should** do these things:

1. Make sure OmniFocus is installed and launches normally.
2. Open OmniFocus once before first use.
3. If macOS asks whether Terminal, OpenClaw, or another host process may control OmniFocus, allow it.
4. If you use a version of OmniFocus without scripting support, upgrade to a version that supports AppleScript.

Why: the MCP server uses AppleScript to talk to OmniFocus. That means the important setup is mainly macOS automation permission, not an in-app plug-in.

## Do you need to download a separate binary?

No separate OmniFocus-specific binary.

The recommended install path is to install the MCP server from npm:

```bash
npm install -g omnifocus-mcp
```

That gives you the `omnifocus-mcp` command on your `PATH`, which this skill now treats as the default and recommended setup.

## Install options

There are two practical ways to install this.

### Option 1: Use the skill folder directly

If you already have this skill folder locally, copy or move it into one of OpenClaw's skill locations:

- workspace skill: `<workspace>/skills/omnifocus-mcp`
- personal skill: `~/.openclaw/skills/omnifocus-mcp`

For example, if you want it available globally:

```bash
mkdir -p ~/.openclaw/skills
cp -R /Users/minhdoan/Documents/Codex/2026-04-18-can-you-refactor-this-into-a/omnifocus-mcp-skill ~/.openclaw/skills/omnifocus-mcp
```

Then start a new OpenClaw session so it reloads available skills.

### Option 2: Package/publish it later

If you want a cleaner reusable install flow, the next step is to publish this skill to ClawHub or keep it in a shared skills repo. I have not published it yet in this thread.

## Publish to ClawHub

Recommended package identity:

- slug: `omnifocus-mcp-openclaw`
- display name: `OmniFocus MCP for OpenClaw`
- initial version: `1.0.0`

Why this naming:

- it avoids confusion with the upstream MCP server package itself
- it makes the OpenClaw wrapper role explicit
- it preserves clear credit to the original creator

Install the publishing CLI:

```bash
npm install -g clawhub
```

Optional dry run:

```bash
clawhub publish /Users/minhdoan/Documents/Codex/2026-04-18-can-you-refactor-this-into-a/omnifocus-mcp-skill --slug omnifocus-mcp-openclaw --name "OmniFocus MCP for OpenClaw" --version 1.0.0 --tags latest,omnifocus,mcp,openclaw,productivity
```

Publish:

```bash
clawhub publish /Users/minhdoan/Documents/Codex/2026-04-18-can-you-refactor-this-into-a/omnifocus-mcp-skill --slug omnifocus-mcp-openclaw --name "OmniFocus MCP for OpenClaw" --version 1.0.0 --tags latest,omnifocus,mcp,openclaw,productivity --changelog "Initial OpenClaw skill wrapper for the upstream OmniFocus-MCP server by themotionmachine. Includes OpenClaw compatibility refactor assistance from OpenAI, plus install guidance, MCP registration helpers, and query usage references."
```

Suggested changelog for the first release:

`Initial OpenClaw skill wrapper for the upstream OmniFocus-MCP server by themotionmachine. Includes OpenClaw compatibility refactor assistance from OpenAI, plus install guidance, MCP registration helpers, and query usage references.`

Before publishing:

1. Make sure the attribution section remains in this README.
2. Keep the upstream GitHub URL in `SKILL.md` frontmatter `homepage`.
3. Verify the skill locally one last time after a fresh OpenClaw restart.

## Install the OmniFocus MCP package

Install the package globally:

```bash
npm install -g omnifocus-mcp
```

Then verify it is available:

```bash
omnifocus-mcp --help
```

This is the recommended method for this skill because it avoids repeated `npx` resolution and gives OpenClaw a stable executable name to invoke.

## Register the MCP server with OpenClaw

Run the helper script:

```bash
/Users/minhdoan/Documents/Codex/2026-04-18-can-you-refactor-this-into-a/omnifocus-mcp-skill/scripts/register_mcp.sh
```

That writes this OpenClaw MCP definition:

```json
{
  "command": "omnifocus-mcp",
  "args": []
}
```

You can verify the registration with:

```bash
openclaw mcp show omnifocus --json
```

## Check prerequisites

Run:

```bash
/Users/minhdoan/Documents/Codex/2026-04-18-can-you-refactor-this-into-a/omnifocus-mcp-skill/scripts/check_setup.sh
```

This checks for:

- macOS
- `osascript`
- `npm`
- `node`
- `omnifocus-mcp`
- `openclaw`
- OmniFocus.app in the standard Applications locations

## First test

After the skill is installed and the MCP server is registered:

1. Start a fresh OpenClaw session.
2. Ask for a simple read-only task first.
3. Keep OmniFocus open during the first test.

Example prompts:

- `Use $omnifocus-mcp to show me tasks due today.`
- `Use $omnifocus-mcp to list my flagged tasks for this week.`
- `Use $omnifocus-mcp to show my Inbox items.`

If that works, try a simple write:

- `Use $omnifocus-mcp to add a task called Renew passport to my Personal admin project.`

## Troubleshooting

### The skill does not appear in OpenClaw

Check:

- the folder name and `SKILL.md` are in a valid OpenClaw skill location
- you started a new OpenClaw session after copying it
- you are on macOS
- `npm` and `omnifocus-mcp` exist on your `PATH`

### OpenClaw sees the skill, but the OmniFocus tools do not work

Check:

- `openclaw mcp show omnifocus --json`
- `omnifocus-mcp --help`
- OmniFocus is installed and can open normally
- macOS has not blocked automation permission

### macOS asks for permission to control OmniFocus

That is expected. Allow it.

If you denied it earlier, review:

- System Settings > Privacy & Security > Automation

The exact app name shown there may be Terminal, iTerm, OpenClaw, or another host process depending on how you launched it.

### OmniFocus opens, but scripting fails

The most likely causes are:

- OmniFocus edition does not include scripting support
- macOS automation permission was denied
- the local Node/npm environment cannot launch the installed MCP package

### Do I need Omni Automation plug-ins?

No. This setup is based on AppleScript communication with OmniFocus, not custom Omni Automation plug-ins.

## Recommended setup summary

If you want the shortest path:

1. Make sure OmniFocus and OpenClaw are installed.
2. Make sure `node`, `npm`, and `openclaw` work in Terminal.
3. Run `npm install -g omnifocus-mcp`.
4. Copy this skill into `~/.openclaw/skills/omnifocus-mcp`.
5. Run `scripts/register_mcp.sh`.
6. Run `scripts/check_setup.sh`.
7. Open OmniFocus once.
8. Start a new OpenClaw session and try a read-only query.

## Files in this skill

- [SKILL.md](/Users/minhdoan/Documents/Codex/2026-04-18-can-you-refactor-this-into-a/omnifocus-mcp-skill/SKILL.md)
- [agents/openai.yaml](/Users/minhdoan/Documents/Codex/2026-04-18-can-you-refactor-this-into-a/omnifocus-mcp-skill/agents/openai.yaml)
- [scripts/register_mcp.sh](/Users/minhdoan/Documents/Codex/2026-04-18-can-you-refactor-this-into-a/omnifocus-mcp-skill/scripts/register_mcp.sh)
- [scripts/check_setup.sh](/Users/minhdoan/Documents/Codex/2026-04-18-can-you-refactor-this-into-a/omnifocus-mcp-skill/scripts/check_setup.sh)
- [references/query_omnifocus.md](/Users/minhdoan/Documents/Codex/2026-04-18-can-you-refactor-this-into-a/omnifocus-mcp-skill/references/query_omnifocus.md)
