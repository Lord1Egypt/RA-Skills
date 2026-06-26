## Description: <br>
Apollo. Use this skill for ANY Apollo request - searching and reading data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to run Apollo prospecting and enrichment workflows through the OOMOL-connected oo CLI, including people search, organization search, entity enrichment, and API usage checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Apollo actions use an OOMOL-connected account and may access account or team data through server-side credentials. <br>
Mitigation: Use only the intended signed-in OOMOL account, inspect the live connector schema before building payloads, and run setup steps only after matching authentication or connection failures. <br>
Risk: Connector actions tagged as write or destructive could change or remove Apollo data if such actions are added or used. <br>
Mitigation: Confirm the exact payload and effect with the user before write actions, and require explicit approval for destructive actions. <br>


## Reference(s): <br>
- [ClawHub Apollo Skill Page](https://clawhub.ai/oomol/oo-apollo) <br>
- [OOMOL Publisher Profile](https://clawhub.ai/user/oomol) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [oo CLI Install Guide](https://cli.oomol.com/install-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API Calls, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline bash commands and JSON payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Connector responses are JSON objects containing data and meta.executionId when actions run successfully.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
