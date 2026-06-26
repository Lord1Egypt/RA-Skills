## Description: <br>
Compare two sources to find shared and divergent principles - discover what survives independent observation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[leegitw](https://clawhub.ai/user/leegitw) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and analysts use this skill to compare two extractions or text sources and identify shared principles, source-specific principles, and divergences without deciding which source is correct. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Shared principles may be mistaken for proof that an idea is true or correct. <br>
Mitigation: Use the output as structural comparison only, and apply independent judgment before treating any principle as correct. <br>
Risk: Semantic alignment requires judgment and may produce incorrect matches or missed divergences. <br>
Mitigation: Review alignment confidence, evidence notes, and divergent items before using the comparison for decisions. <br>
Risk: Input text is processed by the configured agent model, which may be cloud-hosted. <br>
Mitigation: Only provide source text that is appropriate for the configured agent trust boundary. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/leegitw/principle-comparator) <br>
- [Skill Homepage](https://github.com/live-neon/skills/tree/main/pbd/principle-comparator) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, analysis] <br>
**Output Format:** [Markdown or JSON-style structured comparison with shared principles, source-specific principles, divergence analysis, confidence notes, and next steps.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include N-count validation, normalized principle forms, alignment confidence, and share text when a high-confidence N=2 invariant is identified.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata; artifact frontmatter says 1.0.2) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
