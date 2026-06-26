## Description: <br>
Bijian AI Writing Expert collects topic, viewpoints, and reference material, calls the Bijian AI platform, and returns publication-ready article content. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bytearch1990-beep](https://clawhub.ai/user/bytearch1990-beep) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External content creators and agents use this skill to draft articles through Bijian AI. The skill guides collection of a topic, 3-5 viewpoint points, and reference material, then generates, polls, and retrieves article content. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill relies on local credentials for an external service. <br>
Mitigation: Store credentials only in the workspace configuration file, restrict file permissions, and rotate the token if it is exposed. <br>
Risk: Generated article content may be incomplete, inaccurate, or unsuitable for publication. <br>
Mitigation: Review the full generated article and source material before publication; this skill is scoped to writing and does not publish content. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/bytearch1990-beep/inkroam-bijian-writing) <br>
- [Bijian API token page](https://sso.aizmjx.com/home/apikey) <br>
- [Bijian space page](https://bj.aizmjx.com/space) <br>
- [Bijian API base URL](https://bj.aizmjx.com/api) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, API Calls, Guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and generated article text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a workspace configuration file for API credentials and can poll generation status before returning article details.] <br>

## Skill Version(s): <br>
1.1.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
