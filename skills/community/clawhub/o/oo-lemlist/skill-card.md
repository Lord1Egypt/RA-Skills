## Description: <br>
Operate lemlist through an OOMOL-connected account for read-only campaign, campaign lead, and team information lookup. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to inspect lemlist campaigns, campaign leads, and team information through an OOMOL-connected account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The lemlist trigger wording may be broader than necessary for incidental mentions. <br>
Mitigation: Confirm the user intends lemlist-related work before invoking the skill, and avoid using it for incidental references. <br>
Risk: The skill operates through connected lemlist account permissions. <br>
Mitigation: Use least-privilege lemlist credentials and review account/API permissions before installation or use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/oomol/skills/oo-lemlist) <br>
- [lemlist homepage](https://www.lemlist.com) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [oo CLI install guide](https://cli.oomol.com/install-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON connector payloads or responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the oo CLI, an authenticated OOMOL account, and a connected lemlist account.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
