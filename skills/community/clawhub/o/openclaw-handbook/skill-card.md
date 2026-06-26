## Description: <br>
Fetches live from docs.openclaw.ai on every question, with a whole-docs index, working scripts, CI-style selftests for decision-tree drift, worked routing examples, and coverage for SOUL, multi-agent, sessions, platforms, nodes, and ClawHub topics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[igornumeriano](https://clawhub.ai/user/igornumeriano) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and OpenClaw users use this skill to answer OpenClaw setup, configuration, integration, troubleshooting, and marketplace questions from live docs.openclaw.ai pages with source citations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill fetches public OpenClaw documentation over the network and depends on docs.openclaw.ai being available and current. <br>
Mitigation: Run the verification script when freshness matters, cite fetched source URLs, and use the documented not-found fallback when the docs do not contain an answer. <br>
Risk: Routing misses can append the user's question text to a local misses.md file. <br>
Mitigation: Avoid including secrets, private incident details, or sensitive internal URLs in OpenClaw questions that may be logged, and clear the local misses log when needed. <br>


## Reference(s): <br>
- [OpenClaw documentation](https://docs.openclaw.ai) <br>
- [ClawHub skill page](https://clawhub.ai/igornumeriano/openclaw-handbook) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown answers with cited source URLs and optional shell command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Fetches public OpenClaw documentation live; search output is capped at 200 lines and llms-full.txt is cached locally for 1 hour.] <br>

## Skill Version(s): <br>
1.6.2 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
