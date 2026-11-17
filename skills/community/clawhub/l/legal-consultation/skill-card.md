## Description:

General legal consultation entry point to help users identify their legal issues and guide them to appropriate resources.

This skill is ready for commercial/non-commercial use.

## Publisher:

[harrylabsj](https://clawhub.ai/user/harrylabsj)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to triage general legal questions, identify the likely legal area, assess urgency, and suggest appropriate next steps or resources. It is intended for general legal guidance only and not as a substitute for qualified legal advice in the relevant jurisdiction.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may mistake general legal triage for jurisdiction-specific legal advice.

Mitigation: Keep responses framed as general information and direct users to a qualified attorney for specific legal matters.

Risk: The routing behavior is broad and appears optimized for Chinese-language inputs.

Mitigation: Confirm the user intentionally invoked the skill for a legal issue and ask clarifying questions when the jurisdiction, language, or legal area is unclear.

Risk: Legal deadlines and evidence requirements may be time-sensitive.

Mitigation: Encourage users to preserve relevant documents and communications and to promptly consult counsel for urgent or deadline-bound matters.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/harrylabsj/skills/legal-consultation)

## Skill Output:

**Output Type(s):** [guidance, text]

**Output Format:** [JSON-like structured response with classification, suggestions, and disclaimer]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Optimized for Chinese-language legal triage inputs; output must remain general guidance.]

## Skill Version(s):

1.0.0 (source: evidence release metadata, package.json, clawhub.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
