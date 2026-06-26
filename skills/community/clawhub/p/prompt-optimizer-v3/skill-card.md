## Description: <br>
Optimizes vague Chinese-language user requests into structured, executable AI prompts with task type, format, audience, style, and constraint detection. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ntaffffff](https://clawhub.ai/user/ntaffffff) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and other AI users use this skill to rewrite brief or ambiguous Chinese prompts into clearer instructions before sending them to an AI system. It is useful for code, debugging, testing, documentation, research, analysis, translation, and structured content-generation requests. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompt contents can be displayed, cached, or written to output files during local optimization. <br>
Mitigation: Avoid secrets and sensitive internal text, use explicit invocation, and disable caching when prompt retention is not acceptable. <br>
Risk: Broad prompt rewriting can change user intent or add unsuitable task framing. <br>
Mitigation: Review optimized prompts before sending them to another AI system, especially for security, legal, or production engineering work. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ntaffffff/prompt-optimizer-v3) <br>
- [Publisher Profile](https://clawhub.ai/user/ntaffffff) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, YAML, guidance] <br>
**Output Format:** [Optimized prompt text, optionally serialized as JSON or YAML] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can include detected task type, missing information, enhancements, output format, style, audience, constraints, timestamp, and cache status.] <br>

## Skill Version(s): <br>
3.2.0 (source: server release evidence, artifact metadata, and config_data.py) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
