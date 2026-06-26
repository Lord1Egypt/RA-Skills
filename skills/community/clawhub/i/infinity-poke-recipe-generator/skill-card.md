## Description: <br>
Generate a small, specific, daily-life Poke recipe MVP from idea to Kitchen-ready draft (name, onboarding, integrations, automations, sandbox tests), with a lightweight uniqueness check against poke.com/recipes, publish-readiness verdict, and a repeatable improvement loop. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[skylinehk](https://clawhub.ai/user/skylinehk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and recipe authors use this skill to scaffold narrow Poke recipe MVPs, map recipe specs into Kitchen fields, generate sandbox checks, and prepare publish-readiness review materials. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated recipe and integration drafts may contain TODO placeholders or unverified endpoint values. <br>
Mitigation: Review generated files before publishing and replace placeholders with tested Poke Kitchen and MCP configuration. <br>
Risk: Setup commands can affect Poke accounts or connect to MCP endpoints selected by the user. <br>
Mitigation: Run generated npx poke login and mcp add commands only for accounts and endpoints the user trusts. <br>
Risk: The recipe uniqueness check depends on visible poke.com listings and may miss unavailable or recently changed recipes. <br>
Mitigation: Confirm the generated recipe remains unique enough before publication. <br>


## Reference(s): <br>
- [Recipe Template](artifact/references/recipe-template.json) <br>
- [Integration Template](artifact/references/integration-template.json) <br>
- [Verdict Checklist](artifact/references/verdict-checklist.md) <br>
- [Poke Recipes Listing](https://poke.com/recipes) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, JSON, Code, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Generated files containing JSON recipe and integration drafts, Markdown sandbox and review documents, and inline shell commands for Poke setup] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes scaffolded recipe assets under recipes/poke/<slug>/ when the helper script is used.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
