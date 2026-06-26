## Description: <br>
Control Meta/Facebook/Instagram ads through Meta's official `meta ads ...` CLI for read-only audits, reporting, safe planning, and approved one-step mutations of campaigns, ad sets, ads, creatives, catalog/product assets, datasets/pixels, and insights. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tristanmanchester](https://clawhub.ai/user/tristanmanchester) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to let shell-capable agents inspect, report on, plan, and carefully operate Meta advertising accounts through the official Meta Ads CLI. It is intended for workflows where reads are routine but mutations, spend changes, activation, deletion, catalog or dataset changes, and media uploads require explicit review and approval. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can operate Meta ad accounts and may affect budgets, delivery status, campaign assets, catalogs, datasets, or media. <br>
Mitigation: Use a token scoped to the intended account, prefer read-only credentials for reporting, and approve only commands that clearly name the account, object ID, action, and values. <br>
Risk: Budget changes, activation, deletion, and other write actions can create spend or business impact if approved without review. <br>
Mitigation: Review each proposed write command before execution, require specific approval text, and execute one guarded mutation at a time followed by verification. <br>
Risk: Sensitive credentials may be exposed if passed through chat, command arguments, files, or logs. <br>
Mitigation: Keep tokens in environment variables or official auth storage, do not pass secret flags on commands, and leave persistent logging disabled unless a protected audit path is explicitly configured. <br>


## Reference(s): <br>
- [Meta Ads CLI overview](https://developers.facebook.com/documentation/ads-commerce/ads-ai-connectors/ads-cli/ads-cli-overview) <br>
- [Meta Ads 1.0.1 PyPI package](https://pypi.org/project/meta-ads/1.0.1/) <br>
- [Meta Ads 1.0.1 PyPI JSON](https://pypi.org/pypi/meta-ads/1.0.1/json) <br>
- [ClawHub skill page](https://clawhub.ai/tristanmanchester/meta-ads-cli) <br>
- [Artifact provenance metadata](resources/provenance.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands, JSON-oriented command plans, and concise reporting summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read results should be summarized with date ranges, account or object IDs, metrics, caveats, and recommendations separated from any approved changes.] <br>

## Skill Version(s): <br>
2.1.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
