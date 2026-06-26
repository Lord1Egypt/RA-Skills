## Description: <br>
Molt Sift validates JSON, text, and data streams against schemas and rules, extracts higher-confidence signals, and returns reliability scores for agent workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[NoizceEra](https://clawhub.ai/user/NoizceEra) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agents use Molt Sift to validate structured or semi-structured data, clean outputs, score reliability, and process validation bounty jobs. It is especially relevant for crypto, trading, sentiment, and custom data-quality workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Bounty and payment features are financial-style workflows and the server security evidence says they are overstated and under-scoped. <br>
Mitigation: Treat bounty and payment behavior as prototype or simulated until independently verified; do not connect real PayAClaw, x402, Solana, wallet, or secret credentials without authentication, approval gates, spend limits, logging, rate limits, and test-vs-production separation. <br>
Risk: The HTTP API can process bounty requests and payment-like actions. <br>
Mitigation: Do not expose the API publicly without access control, request validation, operational monitoring, and clear authorization for any payment-related action. <br>
Risk: Validation scores and extracted signals may be used to support downstream agent decisions. <br>
Mitigation: Review outputs before using them for execution, financial decisions, or automated claims, especially when source data is noisy or untrusted. <br>


## Reference(s): <br>
- [Molt Sift ClawHub listing](https://clawhub.ai/NoizceEra/molt-sift) <br>
- [Validation Rules](artifact/references/rules.md) <br>
- [README](artifact/README.md) <br>
- [Package manifest](artifact/manifest.json) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Text, Shell commands, Code, Configuration] <br>
**Output Format:** [JSON validation results with status, score, cleaned data, issues, and metadata; Markdown guidance with command and Python examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include validation scores, detected issues, cleaned data, payment status fields, and bounty/job metadata.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata and artifact package metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
