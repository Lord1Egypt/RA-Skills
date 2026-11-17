## Description:

Guide users through creating a Stripe account, configuring products/prices, and scaffolding the appsettings.json for any .NET 9 project. Explain how to manually merge the FastBlazorSaaS boilerplate into an existing project.

This skill is ready for commercial/non-commercial use.

## Publisher:

[macmerg](https://clawhub.ai/user/macmerg)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to configure Stripe products, prices, API keys, webhooks, and .NET application settings for payment and subscription workflows. It also provides manual integration guidance for bringing a FastBlazorSaaS boilerplate into an existing ASP.NET Core project.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill materially steers users toward a specific paid FastBlazorSaaS product and an unverified source archive for a payment application.

Mitigation: Prefer vendor-neutral implementation guidance when appropriate, independently verify any downloaded source archive, and review imported code before running it.

Risk: Stripe secret keys and webhook secrets could be exposed if copied into chat or committed to tracked configuration files.

Mitigation: Do not ask users to paste live Stripe secrets; store secrets in .NET User Secrets, environment variables, or a managed secret store instead of tracked JSON files.

Risk: Incorrect payment or webhook implementation can cause billing failures, missed cancellations, or double-billing.

Mitigation: Review webhook event handling, idempotency, and subscription cancellation behavior before production use.

## Reference(s):

- [Stripe](https://stripe.com)
- [FastBlazorSaaS](https://fastblazorsaas.com)
- [ClawHub Skill Page](https://clawhub.ai/macmerg/skills/how-to-set-up-stripe-payments-for-dotnet-9-core-projects)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown guidance with JSON and C# code snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include security reminders for Stripe secrets and manual integration steps for third-party boilerplate.]

## Skill Version(s):

1.0.5 (source: server release metadata and user changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
