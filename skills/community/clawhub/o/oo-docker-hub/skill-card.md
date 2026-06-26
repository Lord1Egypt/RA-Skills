## Description: <br>
Operate Docker Hub through an OOMOL-connected account for repository, image, organization, team, and access-token workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and platform operators use this skill to inspect Docker Hub repositories and tags, manage organization members and teams, and create repositories through a connected Docker Hub account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a connected Docker Hub account and can administer Docker Hub resources. <br>
Mitigation: Use a least-privileged Docker Hub connection and install only when agent access to that account is intended. <br>
Risk: The skill can list organization access tokens and perform high-impact organization changes. <br>
Mitigation: Review the requested scope and confirm exact write or destructive targets before running those actions. <br>
Risk: First-time setup may require running the oo CLI installer. <br>
Mitigation: Review the oo CLI installer before using the one-line installation command. <br>


## Reference(s): <br>
- [Docker Hub homepage](https://hub.docker.com) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [ClawHub skill page](https://clawhub.ai/oomol/oo-docker-hub) <br>
- [Publisher profile](https://clawhub.ai/user/oomol) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May return Docker Hub data as JSON from oo CLI connector actions.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
