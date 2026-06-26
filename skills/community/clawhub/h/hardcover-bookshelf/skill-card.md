## Description: <br>
Talk to a user's Hardcover bookshelf via the Hardcover GraphQL API to manage reading activity in natural language. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[diwakergupta](https://clawhub.ai/user/diwakergupta) <br>

### License/Terms of Use: <br>
MIT No Attribution <br>


## Use Case: <br>
External users and developers use this skill to let an agent view and update their Hardcover bookshelf, including listing Want to Read books, marking books as started or finished, and counting books read in the previous year. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses HARDCOVER_TOKEN to view and update the user's Hardcover bookshelf. <br>
Mitigation: Install it only for intended Hardcover account use, keep the token scoped to the user, and revoke or rotate the token when the skill is no longer needed. <br>
Risk: Start and finish actions can change reading status in the user's Hardcover account. <br>
Mitigation: Treat those prompts as account-changing actions; the skill asks for disambiguation before mutating ambiguous title matches and echoes the final title and state after successful writes. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/diwakergupta/hardcover-bookshelf) <br>
- [Hardcover API Settings](https://hardcover.app/account/api) <br>
- [Hardcover GraphQL Endpoint](https://api.hardcover.app/v1/graphql) <br>
- [Hardcover GraphQL Patterns](references/graphql-patterns.md) <br>
- [Hardcover Schema Quirks](references/schema-quirks.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, JSON] <br>
**Output Format:** [Markdown responses with shell command execution and optional JSON CLI output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires HARDCOVER_TOKEN with the full Bearer value before API calls.] <br>

## Skill Version(s): <br>
0.1.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
