## Description: <br>
Automatically scans GitHub bounty issues, filters them by configured skills and reward criteria, and can submit application comments through the GitHub CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[SASAMITTRRR](https://clawhub.ai/user/SASAMITTRRR) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent users can use this skill to discover open bounty issues, match them against configured expertise and reward thresholds, and prepare or submit bounty applications from an authenticated GitHub account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can post public bounty application comments from the user's authenticated GitHub account. <br>
Mitigation: Verify the active GitHub account, use a least-privilege token, restrict allowed repositories, and require dry-run or manual approval before posting. <br>
Risk: Automated polling and application behavior can repeatedly interact with public repositories without strong scoping controls. <br>
Mitigation: Set conservative action limits, keep rate limits enabled, and review matched bounties before allowing automated submission. <br>
Risk: The bundled configuration includes a wallet address value. <br>
Mitigation: Replace or remove the wallet address before use and verify payment settings against the intended account. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/SASAMITTRRR/github-bounty-hunter) <br>
- [README.md](artifact/README.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance, JSON configuration, console status text, and GitHub CLI commands or comments] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local configuration for skills, reward thresholds, competition limits, polling interval, platform selection, and wallet address.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
