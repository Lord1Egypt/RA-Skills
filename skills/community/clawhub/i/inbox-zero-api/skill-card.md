## Description: <br>
Use the Inbox Zero API CLI to inspect the live API schema, list and manage automation rules, and read inbox analytics through the public API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[elie222](https://clawhub.ai/user/elie222) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to inspect Inbox Zero API schemas, manage automation rules, and read inbox analytics through the Inbox Zero CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent to use an Inbox Zero API key for authenticated access. <br>
Mitigation: Keep credentials in INBOX_ZERO_API_KEY or approved skill configuration, avoid passing keys as CLI flags, and use a revocable or least-privilege key where available. <br>
Risk: Rule create, update, and delete commands can change Inbox Zero automation behavior. <br>
Mitigation: Ask for explicit approval before mutations, inspect the live schema first, and read the existing rule before applying a full replacement. <br>
Risk: The skill depends on the third-party @inbox-zero/api npm package. <br>
Mitigation: Install only when the package source is trusted and verify the intended package before use. <br>


## Reference(s): <br>
- [Inbox Zero API CLI documentation](https://www.getinboxzero.com/api-reference/cli) <br>
- [CLI reference](references/cli-reference.md) <br>
- [npm package: @inbox-zero/api](https://www.npmjs.com/package/@inbox-zero%2Fapi) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON-oriented CLI guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires INBOX_ZERO_API_KEY for authenticated rules and stats commands; prefers --json for stable output.] <br>

## Skill Version(s): <br>
2.29.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
