## Description: <br>
Searches GitHub for existing implementations, libraries, or patterns. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to search GitHub for existing implementations, libraries, examples, and prior art during research or code discovery. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may require broad GitHub API authority through a GitHub token. <br>
Mitigation: Use the narrowest token scopes and repository access possible. <br>
Risk: Broad activation triggers may invoke the skill during ordinary GitHub, code, or search requests. <br>
Mitigation: Require explicit confirmation before creating branches, opening or modifying pull requests or issues, touching CI/CD resources, or using privileged GitHub operations. <br>
Risk: Search results and ranked findings may be incomplete or contextually wrong. <br>
Mitigation: Review findings against the target repository and validate any reused implementation before applying it. <br>


## Reference(s): <br>
- [OpenClaw homepage](https://github.com/athola/claude-night-market/tree/master/plugins/tome) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown or structured text findings] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include ranked GitHub search findings for agent review.] <br>

## Skill Version(s): <br>
1.9.12 (source: server release metadata; artifact frontmatter lists 1.9.8) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
