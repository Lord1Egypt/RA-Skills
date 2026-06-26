## Description: <br>
Track Meta (Facebook/Instagram) ad creative performance and hit rates across multiple accounts with benchmark metrics and currency conversion. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fortytwode](https://clawhub.ai/user/fortytwode) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Performance marketing teams and agents use this skill to fetch Meta Ads data, calculate creative hit rates, compare accounts and months, and identify ads meeting configured CPT, CPI, IPM, or ROAS benchmarks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Meta Ads credentials and reporting data could be exposed if tokens are over-scoped or placed in chat or config files. <br>
Mitigation: Use a Meta token scoped to only the required ad accounts and permissions, and store secrets in environment variables or a secret manager. <br>
Risk: Cached performance analytics can retain ad account and creative performance data locally. <br>
Mitigation: Restrict access to the workspace and local SQLite data directory, and clear cached data according to internal retention policies. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/fortytwode/meta-ad-creatives) <br>
- [Meta Graph API endpoint](https://graph.facebook.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python examples, shell commands, and JSON-like performance data.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May call the Meta Graph API with user-provided credentials and cache performance snapshots in Firestore or local SQLite.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
