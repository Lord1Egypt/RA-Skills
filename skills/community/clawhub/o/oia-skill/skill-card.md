## Description:

Initializes Deno + Fresh web projects with the oia framework via @oia-ai/oia-fresh, including environment checks, scaffolding, local dev server startup, and verification.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pankitgg](https://clawhub.ai/user/pankitgg)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill in Claude Code to create oia/oia-fresh web projects, check required Deno and npx tooling, run the scaffold command, start the development server, and verify the generated app returns HTTP 200.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks agents to run mutable remote installers and npm scaffolding commands with user-level filesystem access.

Mitigation: Review carefully before installing, pin exact versions of @oia-ai/oia-skill and @oia-ai/oia-fresh, and avoid pipe-to-shell installation.

Risk: Scaffolding can create or overwrite generated project files in the selected target directory.

Mitigation: Initialize only in a new or version-controlled directory so generated files can be reviewed or reverted.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/pankitgg/skills/oia-skill)
- [README](artifact/README.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration guidance]

**Output Format:** [Markdown guidance with inline shell commands and verification summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May initialize project files in a user-selected directory; the skill asks for confirmation before using a non-empty target directory.]

## Skill Version(s):

1.1.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
