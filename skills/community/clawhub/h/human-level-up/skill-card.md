## Description: <br>
Extracts core principles from user-provided material, explains them in plain language, tests understanding with multiple-choice challenges, and tracks learning progress with evolution points. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ai-acheng](https://clawhub.ai/user/ai-acheng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Learners, students, engineers, and professionals use this skill to turn documents, code, papers, or conversations into plain-language concepts, comprehension checks, feedback, and progress tracking. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: User-provided documents may contain private or sensitive information that becomes available to the agent session during extraction and quiz generation. <br>
Mitigation: Only use the extraction workflow on documents the user intends the agent session to process. <br>
Risk: The optional browser bookmarklet pattern can send selected webpage text to an API endpoint. <br>
Mitigation: Use that pattern only with endpoints the user trusts and controls, especially for private or internal webpages. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ai-acheng/human-level-up) <br>
- [README](README.md) <br>
- [Prompt](prompt.md) <br>
- [Examples](examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance] <br>
**Output Format:** [Markdown learning modules with quiz choices and feedback; optional JSON from helper scripts.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May process user-provided documents and, when helper scripts are run, may write local progress data to evolution_data.json.] <br>

## Skill Version(s): <br>
3.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
