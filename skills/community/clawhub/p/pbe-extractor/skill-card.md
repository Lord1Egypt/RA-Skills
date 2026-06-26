## Description: <br>
Extract invariant principles from text and identify ideas that survive rephrasing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[leegitw](https://clawhub.ai/user/leegitw) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, writers, and knowledge workers use this skill to distill documents, notes, methodology, or code comments into candidate principles with confidence levels and source evidence. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Input text may contain confidential content that is processed by the user's configured agent and model provider. <br>
Mitigation: Use only approved agents and model providers for sensitive material, and avoid pasting confidential content unless that environment is authorized. <br>
Risk: Extracted principles are candidate patterns, not verified truths, and may omit nuance at high compression levels. <br>
Mitigation: Review extracted principles before relying on them and validate important findings against additional sources. <br>
Risk: The artifact contains inconsistent wording about whether a review file may be created. <br>
Mitigation: Allow any local review artifact only when the user explicitly requests or approves that file. <br>


## Reference(s): <br>
- [Project homepage](https://github.com/live-neon/skills/tree/main/pbd/pbe-extractor) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Guidance] <br>
**Output Format:** [Structured JSON with extracted principles, confidence levels, source evidence, summary metadata, and next steps.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [No external APIs or third-party services are called by the skill itself; processing occurs within the user's configured agent and model provider.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
