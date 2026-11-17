## Description:

Search and read Wangdian ERP goods, inventory, orders, refunds, stockouts, shops, and warehouses through the oo CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Wangdian ERP users, operations teams, and analysts use this skill to retrieve product, inventory, sales, refund, shop, and warehouse records.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup can execute downloaded software without a clear user checkpoint; the installer and live service behavior were not inspected.

Mitigation: Review and verify the oo CLI installer before setup, and limit the ERP connection to the data needed.

## Reference(s):

- [Wangdian ERP](https://www.wangdian.cn)
- [Wangdian API documentation](https://open.wangdian.cn/open/guide?path=guide_kfzn)
- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [oo CLI command reference](https://raw.githubusercontent.com/oomol-lab/oo-cli/main/docs/commands.md)

## Skill Output:

**Output Type(s):** [JSON data, Text summaries, Guidance]

**Output Format:** [Wangdian ERP records returned as JSON, with agent-readable text summaries and setup guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses the user's OOMOL-connected account. The documented ERP actions retrieve records; live service behavior was not inspected.]

## Skill Version(s):

1.0.4 (source: server release evidence and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
