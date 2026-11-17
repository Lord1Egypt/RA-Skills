## Description:

This skill provides ASMR audio relief recommendations for users experiencing headaches and matches users to audio resources based on gender using a reference rules file.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hcrunner](https://clawhub.ai/user/hcrunner)

### License/Terms of Use:

MIT-0

## Use Case:

External users can use this skill to receive brief, supportive ASMR audio recommendations when they mention headaches, migraines, head pain, or stress-related headache symptoms. The skill is intended as a supplementary comfort resource, not medical advice or treatment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow can ask users to disclose binary gender before providing a simple ASMR recommendation.

Mitigation: Make gender disclosure optional and opt-in, allow users to decline or request a generic resource, and avoid implying gender is medically required.

Risk: Users may describe severe, frequent, persistent, or worsening headache or migraine symptoms.

Mitigation: Frame ASMR audio as supplementary comfort only and encourage professional medical care for severe, frequent, persistent, or worsening symptoms.

## Reference(s):

- [Audio matching rules](references/rules.md)
- [ClawHub skill page](https://clawhub.ai/hcrunner/skills/headache-relief-audio)
- [Male ASMR audio resource](https://myxt.com/link/b39d057a-3530-4e37-83df-b8cfae9dcfc7)
- [Female ASMR audio resource](https://myxt.com/link/0755e916-5b29-4460-959f-46aa14640171)

## Skill Output:

**Output Type(s):** [Text, Guidance]

**Output Format:** [Markdown text with audio links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Provides brief supportive language, gender-matched ASMR audio links, and escalation guidance for severe or persistent symptoms.]

## Skill Version(s):

1.0.3 (source: frontmatter and server evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
