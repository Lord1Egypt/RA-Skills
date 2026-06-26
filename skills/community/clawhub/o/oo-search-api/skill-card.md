## Description: <br>
SearchApi (searchapi.io). Use this skill for ANY SearchApi request -- searching and reading data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to run SearchApi searches, retrieve cached search results, inspect account usage, and look up canonical locations through an OOMOL-connected SearchApi account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses an OOMOL-connected SearchApi account and may trigger account-authenticated network requests. <br>
Mitigation: Run only SearchApi actions expected by the user, inspect action schemas before payload construction, and confirm any write or destructive action before execution. <br>
Risk: First-time setup and connection recovery can involve authentication, credential scope, or billing state. <br>
Mitigation: Use setup steps only after a matching command failure and rely on OOMOL server-side credential injection rather than handling raw API keys. <br>


## Reference(s): <br>
- [SearchApi homepage](https://www.searchapi.io) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [ClawHub skill page](https://clawhub.ai/oomol/oo-search-api) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON payload examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May return SearchApi JSON or HTML data through the oo CLI response envelope.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
