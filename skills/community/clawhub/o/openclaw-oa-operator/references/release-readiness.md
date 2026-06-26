# Release Readiness

## Best Public Shape

Treat this capability as a `skill` first when the main value is:

- installing or initializing OA
- operating `oa collect` and `oa serve`
- interpreting dashboard health
- guiding safe self-heal work
- helping package OA for a user's own workspace

Promote it to a `plugin` when the public value depends on:

- background services
- persistent HTTP routes
- productized dashboard hosting
- commands that should exist independently of an agent conversation

## Scrub Before Publish

Remove or template all machine-specific defaults:

- absolute `openclaw_home` paths
- fixed ports
- `launchd` labels
- local usernames
- private agent rosters
- workspace-local artifact paths
- screenshots that expose private data

Review all remediation commands before publish:

- keep commands explicit and narrow
- avoid arbitrary shell injection points
- document fallback behavior
- prefer safe file creation or tagging over destructive edits

## Minimum Validation Checklist

- Confirm the skill explains when to use OA and when not to.
- Confirm the skill does not assume one exact directory layout unless it first verifies it.
- Confirm a fresh workspace can follow the instructions without your local patches.
- Confirm the publish copy describes workflow value, not just a dashboard skin.
- Confirm any bundled references are generic enough for public use.

## Suggested Listing Copy

Display name:
`OpenClaw OA Operator`

Short description:
`Operate OA monitoring for OpenClaw workspaces.`

Positioning sentence:
`Install, operate, interpret, and package OA monitoring and self-heal workflows for OpenClaw teams.`

## Example Trigger Prompts

- `Use $openclaw-oa-operator to set up OA for this OpenClaw workspace and verify the dashboard.`
- `Use $openclaw-oa-operator to explain why Team Health dropped this week.`
- `Use $openclaw-oa-operator to review whether this OA setup should ship as a skill or a plugin.`
