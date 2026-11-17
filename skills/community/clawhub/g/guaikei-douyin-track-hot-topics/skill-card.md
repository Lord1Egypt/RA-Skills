## Description:

This skill helps agents search Douyin public content, retrieve real-time hot topics, collect video comments, and fetch creator posts through CLI commands that return structured JSON.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT

## Use Case:

External users, developers, and analysts use this skill for Douyin content research, trend tracking, competitive analysis, and public-comment review. It is intended for authorized analysis of public Douyin content and not for publishing, watermark removal, private account data, or other platforms.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad activation may run the skill for short-video research requests that do not explicitly mention Douyin.

Mitigation: Confirm the target platform is Douyin before running commands for ambiguous requests.

Risk: Submitted keywords, profile URLs, video URLs, and targets go to the GUAIKEI service.

Mitigation: Use the skill only for public-data analysis the user is authorized to perform and avoid submitting sensitive targets.

Risk: Command results may be saved automatically in local logs.

Mitigation: Review log contents and clear local logs when they are no longer needed.

Risk: API token handling and runtime messages were flagged for review in the security evidence.

Mitigation: Protect and rotate tokens as needed; prefer a revised release that sends credentials in headers and removes promotional runtime messages.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/engheng-art/skills/guaikei-douyin-track-hot-topics)
- [Skill README](artifact/readme.md)
- [CLI options reference](artifact/references/options.md)
- [Changelog](artifact/references/changelog.md)
- [Input and output JSON schemas](artifact/assets/)
- [GUAIKEI token and help site](https://www.guaikei.com)
- [Declared repository metadata, not provenance](https://github.com/um-why/douyin-search-openclaw)

## Skill Output:

**Output Type(s):** [shell commands, JSON, guidance, configuration]

**Output Format:** [Markdown guidance with inline shell commands; CLI stdout is structured JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js >= 16.14.0 and GUAIKEI_API_TOKEN; command results may also be written to local logs.]

## Skill Version(s):

1.0.0 (source: evidence release, package.json, SKILL.md metadata, changelog, constants.js)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
