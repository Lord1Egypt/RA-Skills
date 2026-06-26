## Description: <br>
Use when publishing a SKILL.md-style agent skill across uGig, sh1pt, GitHub/gists, and follow-on skill marketplaces such as ClawHub, Goose, LobeHub, Kilo, Skillstore, FreeMyGent, ClawMart, Manus, VS Code Agent Skills, and Moltbook. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ralyodio](https://clawhub.ai/user/ralyodio) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to prepare a public-safe SKILL.md, create a source URL, publish to ClawHub and related marketplaces, and track follow-on promotion steps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Publishing workflows can expose credentials, cookies, private environment values, or personal secrets if a skill file is uploaded without review. <br>
Mitigation: Run a secret scan from the intended skill directory, manually inspect any hits, and keep real secrets out of SKILL.md and marketplace listings. <br>
Risk: Marketplace commands, wallet access, and credentialed submissions may affect public listings or paid releases if run against the wrong account or artifact. <br>
Mitigation: Review every generated command, confirm authentication and target account state, use dry-run flows where available, and provide marketplace credentials or wallet access only to trusted services. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ralyodio/promote-skill) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and marketplace checklists] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces reviewable publication steps and command examples; users should inspect commands before execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
