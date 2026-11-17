# HR Decision Packet

Turn a messy people issue into a short, source-backed brief for an accountable human decision-maker.

The skill separates verified facts, stakeholder statements, interpretations, and missing evidence. It compares realistic options and may give a bounded recommendation when the evidence supports one. It does not make or execute employment decisions.

## Version 1.1.0

Start by checking the problem and business/People ownership. The default is now a short brief with the ask first, explicit decided/open state, and a useful next step when evidence is missing. An expanded appendix remains available for complex cases.

See the [synthetic before-and-after example](examples/framing-before-after.md). It shows how a request for training can become a better-framed decision about the documented handoff problem, without presuming its cause.

## Try it in two minutes

Install from ClawHub:

```bash
clawhub install @mwclaw/hr-decision-packet
```

Then use the [synthetic team-support case](examples/synthetic-input.md), or paste this prompt into a supported assistant with the skill enabled:

```text
Prepare an HR Decision Packet from the supplied material.

Check whether the requested solution matches the supplied business problem and clarify business/People ownership. Lead with the ask, separate decided from open questions, and use a concise brief with an appendix only when useful. When blocked, name the minimum evidence and next owner. Keep verified facts, stakeholder statements, interpretations, and missing evidence separate. Name the accountable human owner and required reviewer. Compare realistic options and their tradeoffs. Give a bounded recommendation only if the evidence supports one. End with the next action and a receipt showing sources used, unresolved gaps, human decision status, and actions the agent must not take.

Do not invent policy, legal requirements, precedent, employee history, or approval. Do not make or execute an employment decision.
```

See the [condensed output](examples/synthetic-output.md) produced from the synthetic case. The example shows the intended boundary: the packet prepares a decision; the VP and People Partner still own it.

## What good output should show

A reviewer should be able to tell:

- what decision is being prepared and who owns it;
- what is verified, alleged, inferred, missing, or conflicting;
- which sources support the material claims;
- what options and tradeoffs exist;
- what remains human-owned;
- what happens next.

The [adversarial evals](references/evals.md) cover vague performance claims, policy/practice conflicts, prompt injection, termination, medical information, candidate scoring, suppressed evidence, conflicting sources, low-risk decisions, and requests for external action.

## Other platforms

The same workflow is available for [ChatGPT and Claude](PLATFORMS.md). Review each platform's data, retention, sharing, and workplace-use rules before using sensitive material. Prefer synthetic or de-identified inputs.

## Feedback

[Open a skill feedback issue](https://github.com/mwclaw/openclaw-hr-workflows/issues/new?template=skill-feedback.yml) with the use case you tried, what happened, and what you expected. Do not include employee names, company-confidential information, medical details, credentials, or other sensitive data.
