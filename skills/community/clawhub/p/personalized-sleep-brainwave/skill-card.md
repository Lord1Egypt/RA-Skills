## Description:

A Chinese-language workflow that helps sleep-service practitioners assess sleep complaints and generate personalized brainwave audio recommendations with a four-week use plan.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pvli508](https://clawhub.ai/user/pvli508)

### License/Terms of Use:

MIT-0

## Use Case:

External sleep clinics, health management centers, counselors, rehabilitation organizations, elder-care teams, and wellness practitioners use this skill to structure a brief sleep intake and produce a sleep-audio recommendation, listening guidance, and four-week follow-up plan for clients.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad sleep-related triggers may route casual sleep comments into a structured assessment.

Mitigation: Confirm the user wants sleep-support assistance before collecting details or generating a plan.

Risk: Users may treat the audio plan as medical care for insomnia, medication changes, breathing issues, depression signals, or pain-related sleep problems.

Mitigation: Present the output as non-medical sleep-support guidance and recommend qualified clinical care for medication changes, severe or persistent symptoms, suspected sleep apnea, low mood, or physical pain.

Risk: The bundled audio library uses unsecured HTTP links for health-related audio resources.

Mitigation: Open audio links only after user consent and source trust are established; prefer verified HTTPS delivery before operational use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/pvli508/skills/personalized-sleep-brainwave)
- [Audio library](artifact/references/audio-library.md)
- [Symptom classification and severity assessment](artifact/references/symptom-classification.md)
- [Medication guidance](artifact/references/medication-guidance.md)
- [Matching rules](artifact/references/matching-rules.md)
- [Age and gender profiles](artifact/references/age-gender-profiles.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown with structured intake questions, an audio URL recommendation, usage instructions, health cautions, and a four-week plan]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-language output; recommendations may include HTTP audio links from the bundled audio library.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
