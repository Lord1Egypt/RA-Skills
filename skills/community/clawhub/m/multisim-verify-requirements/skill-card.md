## Description:

Turns Multisim circuit design requirements into measurable criteria and uses experiment data to report PASS, FAIL, or unverified outcomes with evidence.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yxy050208](https://clawhub.ai/user/yxy050208)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to convert Multisim experiment requirements into measurable criteria, run the Multisim verification tool, and produce evidence-backed acceptance results and minimal rerun plans when data is insufficient.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: English-only users may miss operational detail because most detailed instructions are in Chinese.

Mitigation: Review the English summary and obtain a fuller English translation before relying on the workflow in an English-only review process.

Risk: Existing Multisim analysis may lack the measurements needed to prove a requirement.

Mitigation: Keep unsupported items unverified and propose the smallest rerun needed to collect the missing evidence.

Risk: Qualitative safety, reliability, thermal, or manufacturability claims could be overstated as simulation passes.

Mitigation: Report only claims supported by experiment data and keep unsupported claims outside the pass/fail verification result.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yxy050208/skills/multisim-verify-requirements)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown with requirement status counts, measured values, targets, tolerances, and evidence notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Preserves unverified outcomes and proposes a minimal rerun plan when the existing analysis cannot provide the required evidence.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
