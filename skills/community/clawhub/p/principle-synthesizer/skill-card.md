## Description: <br>
Synthesize invariant principles from 3+ sources - find the core that survives across all expressions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[leegitw](https://clawhub.ai/user/leegitw) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, writers, and knowledge-management users apply this skill to synthesize three or more related sources into invariant principle candidates with supporting evidence. It is useful for creating Golden Master candidates while preserving the need for human judgment before treating any candidate as canonical. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The documentation is inconsistent about whether the skill writes a local requires_review.md file containing derived review notes. <br>
Mitigation: Treat use on highly sensitive source text as potentially persistent unless the author clarifies output-only behavior, and review any local files the agent proposes to create or update. <br>
Risk: Golden Master candidates can be mistaken for verified truth even though they are pattern-analysis outputs. <br>
Mitigation: Review the source evidence and apply human judgment before using any synthesized principle as a canonical reference. <br>


## Reference(s): <br>
- [Skill homepage](https://github.com/live-neon/skills/tree/main/pbd/principle-synthesizer) <br>
- [ClawHub skill page](https://clawhub.ai/leegitw/principle-synthesizer) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, guidance] <br>
**Output Format:** [Markdown guidance with JSON schema examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces invariant principles, Golden Master candidates, source evidence, synthesis metrics, and next steps when supported by the input.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata; artifact frontmatter lists 1.0.2) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
