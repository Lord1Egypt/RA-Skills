## Description: <br>
Kuvera portfolio and market data CLI for querying mutual fund data, gold prices, USD/INR rates, fund category returns, and Kuvera portfolio information. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ankitsul](https://clawhub.ai/user/ankitsul) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External Kuvera users and agents use this skill to retrieve read-only market data, mutual fund details, and authenticated portfolio summaries from Kuvera. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles Kuvera financial account credentials and authenticated portfolio data. <br>
Mitigation: Use it only in trusted agent sessions, avoid entering passwords in shared or logged terminals, and confirm you are running the reviewed kuvera-cli executable. <br>
Risk: A reusable Kuvera login token is stored locally at ~/.openclaw/credentials/kuvera/token.json. <br>
Mitigation: Protect that file with local access controls and remove it when authenticated Kuvera access is no longer needed. <br>
Risk: Portfolio, transaction, SIP, and profile commands expose sensitive financial and personal information. <br>
Mitigation: Limit outputs to trusted contexts and avoid sharing command results unless the user has approved disclosure. <br>


## Reference(s): <br>
- [Kuvera Portfolio & Market Data on ClawHub](https://clawhub.ai/ankitsul/kuvera) <br>
- [Kuvera](https://kuvera.in) <br>
- [OpenClaw](https://openclaw.org) <br>
- [Kuvera CLI API Guide](references/api-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Terminal text output and Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Authenticated portfolio, transaction, and SIP commands require Kuvera login; unauthenticated commands return market data such as gold prices, USD/INR, fund categories, and fund details.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
