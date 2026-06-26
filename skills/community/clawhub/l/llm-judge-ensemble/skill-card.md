## Description: <br>
Build a cost-efficient LLM evaluation ensemble with sampling, tiebreakers, and deterministic validators. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nissan](https://clawhub.ai/user/nissan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and ML engineers use this skill to design repeatable, cost-controlled LLM-as-judge evaluations for comparing generative model outputs, shadow-testing models, and setting promotion gates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sampled evaluation data may be sent to selected LLM providers during judge calls. <br>
Mitigation: Use the skill only with provider accounts and data-handling terms that are acceptable for the evaluated content; avoid confidential data unless those terms and logging practices are approved. <br>
Risk: Judge calls can incur provider API costs, especially when sampling is increased or promotion gates force full coverage. <br>
Mitigation: Use scoped or budget-limited API keys and configure sampling and promotion-gate behavior deliberately before running evaluations. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nissan/llm-judge-ensemble) <br>
- [Project homepage](https://github.com/reddinft/skill-llm-as-judge) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, configuration] <br>
**Output Format:** [Markdown guidance with Python examples and configuration patterns] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces evaluation architecture guidance, rubric design patterns, sampling advice, and example judge-ensemble code.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
