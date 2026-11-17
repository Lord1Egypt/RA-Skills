## Description:

Bilingual meme token risk radar for Binance Web3 data that scans newly launched or fast-rising meme tokens from Meme Rush, enriches them with token audit and token info, and produces normalized risk reports in Chinese or English.

This skill is ready for commercial/non-commercial use.

## Publisher:

[2663629531](https://clawhub.ai/user/2663629531)

### License/Terms of Use:


## Use Case:

External traders, researchers, alpha communities, and content operators use this skill to turn Binance Web3 meme token discovery data into an explainable risk-ranked shortlist for further review. It supports scan, audit, and health-check workflows without placing trades.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Payment handling could leak a billing key or charge more than once during failures.

Mitigation: Review billing behavior before paid installation, use noop billing for local testing, avoid custom billing endpoints unless fully trusted, and require idempotency fixes before production paid use.

Risk: Billing configuration documentation and implementation use inconsistent environment variable names.

Mitigation: Confirm the required billing variables in a controlled test environment before enabling SkillPay mode.

Risk: PaxHeader metadata files are included in the package.

Mitigation: Remove archive metadata files from the release package before redistribution.

Risk: Risk scores are point-in-time screening signals and can be mistaken for safety or investment advice.

Mitigation: Treat reports as research inputs only, preserve the no-investment-advice disclaimer, and require independent review before any trading decision.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/2663629531/skills/meme-risk-radar-skill)
- [ClawHub listing copy](references/clawhub_listing.md)
- [Binance Web3 endpoint](https://web3.binance.com)
- [SkillPay service](https://skillpay.me)

## Skill Output:

**Output Type(s):** [text, json, shell commands, guidance]

**Output Format:** [JSON risk report with bilingual text fields]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Scan results include chain, stage, language, timestamp, billing status, sorted token entries, risk scores, visible signals, metrics, audit data, links, and a risk-filtering disclaimer.]

## Skill Version(s):

1.0.0 (source: server release, VERSION.txt, README, CHANGELOG released 2026-03-06)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
