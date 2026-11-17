## Description:

Retrieves public Xiaohongshu content, note details, comments, and creator post lists through Guaikei-powered Node.js CLI commands for structured analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT

## Use Case:

External users, content teams, marketers, and analysts use this skill to collect public Xiaohongshu search results, note details, comment data, and creator post lists for trend research, competitor analysis, KOL screening, and reporting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends Xiaohongshu keywords, URLs, and the GUAIKEI_API_TOKEN to guaikei.com.

Mitigation: Use only when this data transfer is acceptable for the task, keep the API token protected, and rotate the token if logs or infrastructure records may have exposed it.

Risk: Retrieved results and access-bearing Xiaohongshu URLs are saved locally by default.

Mitigation: Run in an appropriate workspace, avoid sensitive research targets in shared environments, and protect or delete the logs directory after use.

Risk: The security verdict is suspicious even though no specific risk findings were listed.

Mitigation: Review the skill before installation and confirm the Guaikei dependency, token handling, and local result retention match organizational policy.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/engheng-art/skills/guaikei-xhs-get-comments)
- [Guaikei service](https://www.guaikei.com)
- [Options reference](references/options.md)
- [Changelog](references/changelog.md)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Files, Guidance]

**Output Format:** [Markdown guidance with inline bash commands; CLI commands return structured JSON and save result files locally.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js 16.14.0+ and GUAIKEI_API_TOKEN; retrieved results are saved under logs/ by default.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter, package.json, and changelog report 1.1.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
