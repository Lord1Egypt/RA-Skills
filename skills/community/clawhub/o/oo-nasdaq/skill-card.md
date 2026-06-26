## Description: <br>
Nasdaq Data Link (data.nasdaq.com). Use this skill for ANY Nasdaq Data Link request — searching and reading data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to query Nasdaq Data Link through an OOMOL-connected account for ticker-focused data retrieval, datatable metadata, export status, and dataset rows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires an OOMOL-connected Nasdaq Data Link account and can access datasets available to that account. <br>
Mitigation: Install and use it only when the user trusts OOMOL and intends to query that connected Nasdaq Data Link account. <br>
Risk: Returned Nasdaq data or datatable download links may be exposed in the agent session. <br>
Mitigation: Treat returned rows, metadata, and download links as account-accessible data and avoid sharing them beyond the intended session or audience. <br>
Risk: Incorrect payloads can query unintended datasets or filters. <br>
Mitigation: Inspect the live action schema before constructing JSON payloads and confirm any write or destructive action if such actions are introduced. <br>


## Reference(s): <br>
- [Nasdaq Data Link homepage](https://data.nasdaq.com) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [ClawHub skill listing](https://clawhub.ai/oomol/oo-nasdaq) <br>
- [OOMOL publisher profile](https://clawhub.ai/user/oomol) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON payload/response handling] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides read-oriented Nasdaq Data Link actions through the OOMOL oo CLI and may surface returned dataset rows, metadata, export status, or download links.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
