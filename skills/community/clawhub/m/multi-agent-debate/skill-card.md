## Description: <br>
Verify facts, reduce hallucinations, and explore multiple viewpoints through structured multi-agent debate. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[simoncatbot](https://clawhub.ai/user/simoncatbot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and other agent users apply this skill when they need a structured second-opinion workflow for fact-checking, complex reasoning, trade-off analysis, or hallucination detection. The skill guides multiple agents through independent answers, critique, optional revision, and a consensus or verdict phase. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Higher model cost and latency can occur because the workflow requests multiple independent answers and critique rounds. <br>
Mitigation: Use the debate workflow for complex, high-stakes, or accuracy-sensitive questions, and limit the number of agents or rounds when speed matters. <br>
Risk: Sensitive prompt content may be processed across multiple internal reasoning passes. <br>
Mitigation: Avoid placing secrets or highly sensitive information into debate prompts unless the agent environment is approved for that data. <br>


## Reference(s): <br>
- [Detailed Examples](references/examples.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/simoncatbot/multi-agent-debate) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown debate transcript with independent answers, critique rounds, optional revisions, and a final consensus or verdict] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May increase token use and latency because the workflow asks for multiple independent answers and critique rounds.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
