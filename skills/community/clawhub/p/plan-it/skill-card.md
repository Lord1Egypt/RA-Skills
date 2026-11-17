## Description:

plan-it helps agents create and maintain a self-contained interactive plan.html planning artifact with phase tracking, embedded JSON state, session catchup, attestation, templates, and Markdown export.

This skill is ready for commercial/non-commercial use.

## Publisher:

[othmanadi](https://clawhub.ai/user/othmanadi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use plan-it during multi-step work to produce a navigable HTML planning file, track phases and decisions, preserve state across context resets, and export the plan to Markdown or JSON.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads local agent session stores to detect prior planning context.

Mitigation: Use it only in trusted projects and set PLANIT_NO_HISTORY=1 or pass --no-history when session history inspection is not acceptable.

Risk: Browser-opened plan files and unsafe HTML handling can affect users who open plans built from untrusted content.

Mitigation: Avoid opening plans built from untrusted content and review generated plan.html before browser use.

Risk: Untrusted template or slug values passed to init scripts can affect path handling.

Mitigation: Use known template names and trusted plan slugs; do not pass untrusted values to init scripts.

## Reference(s):

- [Server-resolved GitHub source](https://github.com/OthmanAdi/plan-it/tree/main/skills/plan-it)
- [ClawHub skill page](https://clawhub.ai/othmanadi/skills/plan-it)
- [Markdown predecessor](https://github.com/OthmanAdi/planning-with-files)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, Files]

**Output Format:** [Markdown guidance with shell commands and generated self-contained HTML and JSON plan artifacts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a local plan.html with embedded JSON state and can export Markdown or JSON.]

## Skill Version(s):

0.1.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
