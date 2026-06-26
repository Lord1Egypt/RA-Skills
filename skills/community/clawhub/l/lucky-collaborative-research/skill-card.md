## Description: <br>
Lucky gathers raw web data for research tasks while Jinx analyzes local files and structures findings for market research, competitive analysis, API documentation review, trend analysis, pricing research, and marketplace intelligence. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rmbell09-lang](https://clawhub.ai/user/rmbell09-lang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and research teams use this skill to split multi-source research into web collection, local analysis, and final synthesis. It is intended for structured market, competitor, pricing, trend, documentation, and content analysis workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow encourages broad webpage capture and transfer, which can collect private, sensitive, or out-of-scope data. <br>
Mitigation: Use only approved sources, scope collection before browsing, review captured files before transfer, and redact secrets or personal data. <br>
Risk: The artifact includes environment-specific localhost, SSH key, destination host, and storage path examples that may not match the user's system. <br>
Mitigation: Install and run only after replacing those values with systems and paths the user owns or is authorized to use. <br>
Risk: Delegated analysis may include requests for Jinx to execute scripts against collected files. <br>
Mitigation: Require explicit approval before requesting script execution and inspect analysis code or commands before running them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/rmbell09-lang/lucky-collaborative-research) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples, HTTP API examples, structured data templates, and report outlines] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce structured JSON analysis requests, competitor profiles, pricing analysis, market gap summaries, and final research reports.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
