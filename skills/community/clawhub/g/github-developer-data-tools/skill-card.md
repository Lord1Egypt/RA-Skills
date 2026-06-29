## Description: <br>
GitHub and developer data for AI agents, including repository metadata, audit and risk scoring, user profiles, releases, and gist content through paid HTTPS GET calls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[colinhughes2121](https://clawhub.ai/user/colinhughes2121) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, engineers, and dev-tool agents use this skill to look up live GitHub repository, release, user, and gist data and to support dependency due diligence or open source research. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Queries may send GitHub repository, user, release, or gist identifiers to GoCreative. <br>
Mitigation: Review the identifiers before use and avoid submitting private or sensitive repository details unless that sharing is acceptable. <br>
Risk: Using the skill may trigger small USDC payments through x402. <br>
Mitigation: Configure wallet spending limits or approval prompts before allowing an agent to make calls. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/colinhughes2121/github-developer-data-tools) <br>
- [GoCreative API](https://api.gocreativeai.com) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Analysis, API Calls] <br>
**Output Format:** [JSON responses from HTTPS GET endpoints] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [No API key or signup is described. Calls are paid per request in USDC through x402.] <br>

## Skill Version(s): <br>
1.0.0 (source: server evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
