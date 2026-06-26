## Description: <br>
Scans recent GitHub issues labeled as bounties, filters and tracks new opportunities, and can export results for agent review. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dagangtj](https://clawhub.ai/user/dagangtj) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, security researchers, and agents use this skill to run a local bounty scan, review newly found GitHub bounty-labeled issues, and optionally save results as JSON. It is useful for recurring discovery workflows where local configuration controls filters such as technology stack and minimum reward. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The artifact claims broad multi-platform scanning and Telegram notifications, but the authoritative security summary notes that the current behavior is a local GitHub bounty-label scanner. <br>
Mitigation: Treat GitHub scanning as the implemented capability, verify any advertised platform or notification support before relying on it, and avoid presenting empty platform stubs as completed coverage. <br>
Risk: The scanner runs the GitHub CLI under the user's local GitHub profile and can be scheduled as a recurring cron task. <br>
Mitigation: Run it only in an account and workspace intended for bounty discovery, review any cron entry before enabling recurring scans, and remove scheduled runs when no longer needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dagangtj/multi-bounty-scanner) <br>
- [Publisher profile](https://clawhub.ai/user/dagangtj) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Console text or JSON file output, with Markdown documentation containing shell commands and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js 18+ and the GitHub CLI for implemented scanning; stores seen bounty IDs under the user's home directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
