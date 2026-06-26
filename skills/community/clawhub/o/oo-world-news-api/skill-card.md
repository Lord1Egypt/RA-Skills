## Description: <br>
World News API (worldnewsapi.com). Use this skill for World News API requests that search, retrieve, or read news data through the OOMOL connector. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to query World News API through OOMOL for top news, article search, article retrieval, source search, and location coordinate lookup. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The package is flagged suspicious by the authoritative ClawHub security evidence. <br>
Mitigation: Install only after reviewing the ClawHub security summary and confirming the local tools and credentials this package may use are acceptable. <br>
Risk: The skill depends on the local oo CLI and OOMOL-managed World News API credentials. <br>
Mitigation: Use normal connector actions only after the user has installed and signed in to the oo CLI; run setup or connection commands only after an auth or connection failure. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/oomol/oo-world-news-api) <br>
- [World News API Homepage](https://worldnewsapi.com) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses OOMOL-managed credentials through the oo CLI and returns connector JSON responses when actions are run.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
