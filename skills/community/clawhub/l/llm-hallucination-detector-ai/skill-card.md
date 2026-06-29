## Description: <br>
Detects hallucinations in large language model outputs through fact checking, consistency checks, source tracing, and confidence assessment. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ai-gaoqian](https://clawhub.ai/user/ai-gaoqian) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, evaluators, and AI safety reviewers use this skill to review LLM-generated text, conversations, or technical documents for fabricated, incorrect, unsupported, or inconsistent claims. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can produce incorrect or incomplete hallucination judgments when source coverage is insufficient or the checked domain requires expert interpretation. <br>
Mitigation: Use the report as review guidance and confirm high-impact medical, legal, financial, or code findings against authoritative sources and qualified experts. <br>
Risk: The release evidence security guidance notes that high-impact actions should keep confirmation gates in place. <br>
Mitigation: Review findings before acting on them and preserve any workflow confirmation gates around production data, users, packages, emails, or reviewer tooling. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ai-gaoqian/llm-hallucination-detector-ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown hallucination detection report with sentence-level findings, confidence scores, risk levels, reasons, and corrective suggestions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include an overall trust score and summary for the reviewed LLM output.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
