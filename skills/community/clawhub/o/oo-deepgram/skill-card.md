## Description: <br>
Deepgram (deepgram.com). Use this skill for Deepgram search and read requests through an OOMOL-connected account instead of calling the API directly. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to inspect Deepgram projects, models, balances, and API key listings through the oo CLI with an OOMOL-connected Deepgram account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read sensitive Deepgram account details, including project balances and API key listings. <br>
Mitigation: Install only if the user trusts OOMOL and intends the agent to access the connected Deepgram account; avoid requesting balances or key listings unless needed. <br>
Risk: The skill depends on an authenticated OOMOL connection and may fail when the oo CLI is missing, the user is not signed in, or the Deepgram connection is expired. <br>
Mitigation: Run setup or reconnection steps only after a matching command failure, then retry with the live connector schema. <br>


## Reference(s): <br>
- [ClawHub Deepgram skill page](https://clawhub.ai/oomol/oo-deepgram) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [Deepgram homepage](https://deepgram.com/) <br>
- [oo CLI install guide](https://cli.oomol.com/install-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON payload examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses oo CLI commands and returns connector responses as JSON data with execution metadata.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
