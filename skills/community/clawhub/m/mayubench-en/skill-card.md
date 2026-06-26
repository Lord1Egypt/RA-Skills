## Description: <br>
AI-Native Behavior Benchmark - 48 scenarios x 3 difficulty levels = 144 questions, 8-dimension scoring, measuring whether AI should do things, not whether it can. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wanyview1](https://clawhub.ai/user/wanyview1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, evaluators, and AI safety reviewers use this skill to test model behavioral decision quality across boundary scenarios, score responses with MayuBench rubrics, and compare model reliability. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Benchmark scenarios include adversarial, sensitive, or risky phrases that could be mistaken for operational guidance. <br>
Mitigation: Use the content only in controlled model evaluations and keep benchmark prompts separate from live user workflows. <br>
Risk: Hard-coded crisis-resource examples may become outdated or unsuitable for production safety responses. <br>
Mitigation: Treat crisis-resource text as benchmark material and verify any production safety guidance against current authoritative resources. <br>
Risk: Automated judge-model scoring can be subjective or inconsistent across models and runs. <br>
Mitigation: Review sampled results manually, keep scoring rubrics visible, and compare models under separate sessions as described by the benchmark. <br>


## Reference(s): <br>
- [MayuBench Homepage](https://github.com/kaidimi/mayubench) <br>
- [MayuBench v1.0 Question Bank](artifact/MayuBench_v1.0.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/wanyview1/mayubench-en) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, code] <br>
**Output Format:** [Markdown benchmark content with scoring tables, evaluation criteria, and pseudocode] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Provides 144 scenario-based benchmark questions across 8 behavioral dimensions and a six-level scoring framework.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
