## Description: <br>
A product-management workflow that guides an agent through requirement clarification, specification writing, dispatch to Claude Code, and acceptance review. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yiguoguo](https://clawhub.ai/user/yiguoguo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, product managers, and agent operators use this skill to turn ambiguous feature requests into a confirmed SPEC, dispatch implementation work to Claude Code through a local dispatch dependency, and verify the completed work against acceptance criteria. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow can delegate work to the separate local claude-code-dispatch dependency. <br>
Mitigation: Review the dependency and its dispatch.sh script before use, and install only when its source and behavior are trusted. <br>
Risk: Using --permission-mode bypassPermissions can remove manual approval gates for tool actions during dispatched work. <br>
Mitigation: Omit or avoid --permission-mode bypassPermissions when interactive approval is required. <br>
Risk: A broad --workdir could allow the dispatched agent to operate outside the intended project scope. <br>
Mitigation: Set --workdir only to the intended project directory before dispatching implementation work. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yiguoguo/pm-requirement-flow) <br>
- [Publisher profile](https://clawhub.ai/user/yiguoguo) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with structured SPEC text and inline bash command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include local dispatch guidance and acceptance-check instructions.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
