## Description: <br>
Query version-specific GitHub bug reports with quality assessment markers so an agent can combine the results with user configuration for contextual OpenClaw upgrade evaluation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[suidge](https://clawhub.ai/user/suidge) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw operators use this skill before upgrades to retrieve version-specific issue summaries, severity groupings, quality markers, and merged-fix status. Agents use that output with local deployment context to recommend whether an upgrade is suitable. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The script uses the local GitHub CLI session and sends version search terms to GitHub. <br>
Mitigation: Confirm gh authentication status and intended GitHub account before running the skill. <br>
Risk: Upgrade guidance can be misleading if the agent ignores the user's actual OpenClaw channels, plugins, runtime, Node version, or deployment model. <br>
Mitigation: Ask the agent to compare reported issues against the user's local configuration before acting on upgrade recommendations. <br>
Risk: The skill may require access to sensitive local OpenClaw configuration to make contextual recommendations. <br>
Mitigation: Approve any local configuration inspection explicitly and limit it to the fields needed for the upgrade assessment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/suidge/openclaw-version-bug-hunter) <br>
- [Severity rules](references/severity-rules.md) <br>
- [OpenClaw GitHub issues target](https://github.com/openclaw/openclaw) <br>
- [GitHub CLI](https://cli.github.com/) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, guidance] <br>
**Output Format:** [Markdown-style terminal report with categorized issue lists, quality markers, counts, and upgrade-evaluation guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a version string and depends on local gh and jq availability.] <br>

## Skill Version(s): <br>
2.1.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
