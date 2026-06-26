---
name: Infra
description: A comprehensive AI agent skill for managing, designing, and troubleshooting technical infrastructure. Covers cloud architecture, server configuration, networking, security hardening, cost optimization, incident response, and infrastructure as code. Helps engineers, DevOps professionals, and technical founders build systems that are reliable, secure, scalable, and cost-efficient — and fix them fast when they are not.
---

# Infra

## 3:47 AM

The alert fires at 3:47 AM. You are asleep. Your phone is not.

By the time you have found your glasses and opened your laptop, the incident has been running for eleven minutes. You do not know yet whether this is a blip that will resolve itself or the beginning of something that will consume the next eighteen hours and require a postmortem with your largest customer. You do not know whether the problem is in your code, your database, your network, your cloud provider, or something three layers below any of that which you do not control. You do not know whether the fix is one command or a complete architecture change.

What you know is that something is broken, people are affected, and every minute you spend figuring out what is happening is a minute the problem continues.

This is the moment infrastructure work is actually about. Not the architecture diagrams. Not the Terraform files. Not the capacity planning spreadsheets. The moment when something breaks in a way you did not anticipate and you have to think clearly under pressure with incomplete information and fix it fast.

Everything else — the reliability work, the security work, the cost optimization work, the documentation — exists to make this moment less likely, less severe, and less long when it happens anyway. Because it always happens anyway.

Infra is built around this reality.

---

## Incident Response

When something is broken, the skill shifts into incident response mode.

The first priority is understanding what is actually happening. Not what you think is happening. Not what the last alert said. What the current state of the system actually is. The skill helps you move through a structured diagnostic process without skipping steps under pressure — which is when steps get skipped, and skipping steps is how incidents that should take forty minutes take four hours.

What is the blast radius? Who and what is affected? When did it start — the exact time, not approximately? What changed in the system in the hours before the incident started? What do the logs say at the exact moment the problem began? What do the metrics show — not just the metric that triggered the alert, but the metrics that might explain why?

It helps you form and test hypotheses quickly. Not brainstorm endlessly. Form the most likely hypothesis based on available evidence, test it with the fastest available means, confirm or eliminate it, move to the next. This sounds obvious. Under pressure at 3:47 AM it is not obvious. Having a structured process makes it obvious.

When you find the problem, it helps you evaluate the fix. The fast fix that restores service now and creates technical debt you will deal with later. The correct fix that takes longer but actually resolves the root cause. The right choice depends on the severity of the impact and how long the correct fix will take. The skill helps you make that call clearly rather than defaulting to one approach because it is familiar.

After the incident, it helps you write the postmortem. Not to assign blame. To understand what actually happened, why the existing safeguards did not prevent it, and what specific changes will make this class of incident less likely or less severe in the future.

---

## Architecture and Design

Good infrastructure architecture is invisible. The system handles load. Deployments do not cause outages. Failures in one component do not cascade into failures everywhere else. The team can move fast without being afraid. Nobody thinks about the infrastructure because there is nothing to think about.

Bad infrastructure architecture is very visible. Every deployment is a tense event. Scaling requires heroic effort. A single component failure takes down unrelated services. The team slows down as the system grows because every change carries unpredictable risk.

The difference is usually not sophistication. It is whether the architecture was designed with failure in mind.

The skill helps you design systems that assume failure. Not systems that try to prevent all failure — that is impossible and the attempt creates fragility. Systems that contain failure: that limit blast radius, that degrade gracefully when components fail, that recover automatically from the failures that happen frequently, and that make the failures that require human intervention obvious and fast to diagnose.

For greenfield systems, it helps you make the foundational decisions that are easy to get right at the beginning and expensive to change later. Stateless versus stateful services. Synchronous versus asynchronous communication. Single versus multi-region. Monolith versus services. The right answer depends on your specific scale, team size, operational maturity, and growth trajectory. The skill helps you think through these tradeoffs honestly rather than defaulting to whatever is currently fashionable.

For existing systems, it helps you understand what you have, identify the highest-risk architectural problems, and prioritize the changes that will have the most impact on reliability and operational burden.

---

## Cloud Infrastructure

The major cloud providers — AWS, GCP, Azure — offer enough services and configuration options to make every decision feel consequential and every mistake feel expensive. The skill provides clear, opinionated guidance on the decisions that matter most.

**Compute** selection between virtual machines, containers, and serverless functions involves tradeoffs in cost, operational complexity, cold start behavior, and scaling characteristics that depend heavily on your specific workload pattern. The skill analyzes your workload and recommends the right compute model, with honest acknowledgment of the cases where the answer is genuinely ambiguous.

**Networking** configuration — VPCs, subnets, security groups, load balancers, CDNs, DNS — is where many cloud security problems originate and where misconfiguration has consequences that are both serious and non-obvious. The skill reviews network configurations for common security gaps and helps you understand what each component is doing and why.

**Database** selection and configuration involves tradeoffs between consistency, availability, query flexibility, operational complexity, and cost that depend on your data model and access patterns. The skill helps you choose the right database for your specific requirements and configure it for reliability and performance.

**Cost optimization** on cloud infrastructure requires understanding the pricing model for every service you use, identifying waste, and making architectural decisions that reduce cost without compromising reliability. Cloud bills grow in ways that are easy to miss until they are large. The skill analyzes your infrastructure for cost reduction opportunities and helps you implement the changes that have the highest impact per unit of engineering effort.

---

## Security

Infrastructure security failures have a specific character. They are often invisible until they are catastrophic. The system appears to work normally while an attacker has had access for weeks. The misconfigured storage bucket has been public for months before anyone notices. The unpatched vulnerability has been sitting in production through multiple deployments.

The skill treats security as an infrastructure property that must be designed in, not a checklist to be completed before launch.

**Access control** — who can do what to which systems — is the foundation. The principle of least privilege applied consistently: every service, every user, every automation has exactly the access it needs and nothing more. The skill reviews IAM configurations and service permissions for violations of this principle and helps you remediate them systematically.

**Network security** — what can talk to what — is the second layer. Internal services that should not be reachable from the internet. Databases that should only accept connections from specific application servers. Management interfaces that should only be accessible through a bastion or VPN. The skill reviews network configurations for exposures and helps you close them.

**Secrets management** — how credentials, API keys, and certificates are stored and rotated — is where many breaches originate. Credentials in environment variables. API keys in code repositories. Certificates that expire without warning. The skill helps you implement proper secrets management and identifies existing secrets hygiene problems.

**Vulnerability management** — keeping software patched and dependencies updated — requires a systematic process rather than periodic heroic efforts. The skill helps you build and maintain this process.

---

## Infrastructure as Code

Infrastructure managed through consoles and manual processes cannot be reliably reproduced, audited, or version-controlled. Infrastructure as code — Terraform, Pulumi, CloudFormation, Ansible, and similar tools — treats infrastructure configuration the same way software treats application code: version-controlled, reviewed, tested, and deployed through automated pipelines.

The skill helps you write infrastructure as code that is correct, readable, and maintainable. It reviews existing configurations for common mistakes. It helps you structure modules for reuse across environments. It helps you build the CI/CD pipelines that test and deploy infrastructure changes safely.

For teams migrating from manually managed infrastructure to infrastructure as code, it helps you plan and execute the migration without disrupting running systems — which is the hard part that documentation rarely covers adequately.

---

## For the Person Who Owns Everything

At many companies, particularly early-stage startups and small engineering teams, one person owns all of this. The architecture decisions. The incident response. The security. The cost management. The on-call rotation. The postmortems.

This is a lot to carry. The skill does not make it light. It makes it more manageable by ensuring you have a clear process for each of these areas, that the most important things are documented well enough to survive a late-night incident, and that you are not solving the same problems repeatedly because the solutions were never written down.

The goal is infrastructure that you can operate confidently — that does not require heroism to maintain, that fails in predictable ways, and that you understand well enough to fix quickly when it breaks at 3:47 AM.
