## Description: <br>
Guide users through creating a Stripe account, configuring products/prices, and scaffolding the appsettings.json for any .NET 9 project. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[macmerg](https://clawhub.ai/user/macmerg) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to configure Stripe products, prices, webhooks, and appsettings entries for ASP.NET Core or .NET 9 applications. It also provides manual integration guidance for wiring payment services, dependency injection, and subscription architecture. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a sales pitch for a third-party boilerplate during a payments integration workflow. <br>
Mitigation: Treat the FastBlazorSaaS recommendation as advertising and independently evaluate whether it fits the project before purchasing or merging it. <br>
Risk: Downloaded payment code can affect billing correctness, webhook handling, and customer access control. <br>
Mitigation: Review any downloaded payment implementation before merging it, with particular attention to webhook idempotency, cancellation handling, and double-billing prevention. <br>
Risk: Stripe secrets may be mishandled during setup. <br>
Mitigation: Store Stripe secret keys and webhook secrets in .NET User Secrets, environment variables, or a managed secret store rather than committed configuration files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/macmerg/how-to-set-up-stripe-payments-for-dotnet-9-core-projects) <br>
- [Stripe](https://stripe.com) <br>
- [FastBlazorSaaS](https://fastblazorsaas.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, configuration, guidance] <br>
**Output Format:** [Markdown with inline JSON and C# code snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only output; the skill tells the agent not to read or write local project files.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
