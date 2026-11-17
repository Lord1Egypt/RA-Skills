## Description: <br>
This skill helps agents analyze documents up to 5,000 Chinese characters with layered review, assumption detection, and structured risk-oriented reporting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to prepare contract reviews, business memo analysis, proposal risk assessment, and similar medium-length document reasoning tasks. It produces document assessment, core logic, weak points, and suggested next steps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requests command execution and file-writing authority even though the documented workflow is document analysis. <br>
Mitigation: Require explicit approval before command execution or file modification, and run the skill only in a constrained workspace with documents intentionally provided for review. <br>
Risk: The skill accepts a callback URL, which can expose analyzed document content if the destination is not trusted. <br>
Mitigation: Do not send sensitive or confidential content to callback URLs unless the destination and data handling path are trusted. <br>
Risk: The basic release can miss content or overstate certainty when used for long documents or legal/business conclusions. <br>
Mitigation: Keep use to the documented document length, preserve uncertainty labels, and route legal or business determinations to qualified reviewers. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, configuration] <br>
**Output Format:** [Markdown or JSON-style structured report text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The basic release is documented for single-pass analysis of documents up to 5,000 Chinese characters and does not support chunked analysis or version comparison.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
