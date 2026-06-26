## Description: <br>
Monitor GitHub repositories and npm packages for new releases and version updates, summarize changelogs, and highlight breaking changes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[newageinvestments25-byte](https://clawhub.ai/user/newageinvestments25-byte) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to monitor a configured watchlist of GitHub repositories and npm packages, detect new releases, and generate markdown changelog reports with breaking-change highlights. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill performs network lookups against public GitHub and npm sources and may encounter rate limits, missing packages, or transient network errors. <br>
Mitigation: Review the watchlist before use, start with a dry run, and follow the setup guide's rate-limit and error-handling guidance. <br>
Risk: Using --update-state changes the local baseline, which can suppress future reporting for versions already recorded. <br>
Mitigation: Use --update-state only after confirming the report is correct; omit it for dry runs. <br>


## Reference(s): <br>
- [Setup Guide](references/setup-guide.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/newageinvestments25-byte/nai-changelog-watcher) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports and JSON release data, with shell commands and configuration guidance for setup and scheduling.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a local watchlist and local state file; --update-state records current versions as the future baseline.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
