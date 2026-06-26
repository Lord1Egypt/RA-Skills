## Description: <br>
Coordinate the end-to-end Hong Kong IPO workflow across discovery, snapshot extraction, personalization, scoring, and review optimization. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hackstoic](https://clawhub.ai/user/hackstoic) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent operators use this skill to route Hong Kong IPO research tasks across discovery, data extraction, profile and watchlist management, scoring, decision-card generation, batch review, and outcome feedback. It supports research and decision preparation, not investment advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can make public market-data requests and the resulting data may be incomplete, stale, or degraded. <br>
Mitigation: Review source data and degraded-data notices before relying on outputs, and treat scores as research support rather than financial advice. <br>
Risk: Profile, watchlist, scoring, and review-history files may reveal investment preferences or activity. <br>
Mitigation: Keep the HKIPO home directory and configuration files out of shared folders, public artifacts, and version control. <br>
Risk: Commands that save parameters or accept imported suggestions can change local scoring rules and future review behavior. <br>
Mitigation: Review parameter changes and imported suggestions before accepting them, and preserve prior versions for comparison. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hackstoic/hkipo-orchestrator) <br>
- [Runtime README](runtime/hkipo-next/README.md) <br>
- [AiPO API Documentation](runtime/hkipo-next/references/aipo-api.md) <br>
- [API Guide](runtime/hkipo-next/references/api-guide.md) <br>
- [Analysis Guide](runtime/hkipo-next/references/analysis-guide.md) <br>
- [IPO Mechanism Guide](runtime/hkipo-next/references/ipo-mechanism.md) <br>
- [Risk Preferences Guide](runtime/hkipo-next/references/risk-preferences.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Concise text or markdown for users, JSON for machine steps, and shell commands for CLI workflows.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read public market data and may write local profile, watchlist, scoring, and review-history state under the configured HKIPO home directory.] <br>

## Skill Version(s): <br>
0.1.0 (source: SKILL.md frontmatter, pyproject.toml, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
