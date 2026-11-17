## Description:

Integrates with Lingxing ERP to query today's orders, product inventory, and product lists through OpenClaw.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wengjianmin19850412](https://clawhub.ai/user/wengjianmin19850412)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can use this skill to connect an agent to Lingxing ERP for order lookup and product inventory or product list queries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Configurable BASE_URL can send ERP authentication data to an arbitrary host if misconfigured or tampered with.

Mitigation: Keep BASE_URL fixed to the legitimate Lingxing API host, restrict configuration changes, and use trusted least-privilege Lingxing API keys stored as protected secrets.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/wengjianmin19850412/skills/lingxing-erp)

## Skill Output:

**Output Type(s):** [API Calls, JSON]

**Output Format:** [JSON API response data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires ACCESS_KEY, SECRET_KEY, and BASE_URL configuration; the order lookup supports page and page_size parameters.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact/skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
