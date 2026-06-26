## Description: <br>
AI-native behavior benchmark with 48 scenarios across 3 difficulty levels, 144 questions, and 8 scoring dimensions for evaluating what an AI should do rather than what it can do. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wanyview1](https://clawhub.ai/user/wanyview1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, evaluators, and AI safety reviewers use MayuBench to test model behavior in boundary cases such as uncertainty, refusal quality, privacy, agent boundaries, and metacognition. It supports manual scoring, automated judge-model scoring, and Arena-style evaluation sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Automated evaluation can send benchmark prompts, model responses, or user-provided test data to external judge models. <br>
Mitigation: Use automated Arena-style evaluation only in deliberate test sessions, and avoid sending private user data to external judge models unless that evaluation setup has been reviewed. <br>


## Reference(s): <br>
- [MayuBench source homepage](https://github.com/kaidimi/mayubench) <br>
- [ClawHub release page](https://clawhub.ai/wanyview1/mayubench) <br>
- [MayuBench_v1.0.md](artifact/MayuBench_v1.0.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown benchmark prompts, rubrics, scoring guidance, and pseudocode for automated evaluation] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only benchmark; no code execution, installation, or data access by the skill itself.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
