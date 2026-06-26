## Description: <br>
PRE Engineering initializes a Plan-Review-Execute multi-agent project workflow by collecting requirements, generating project and role guide documents, and providing startup instructions for Planner, Executor, and Reviewer agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhangzhanluo](https://clawhub.ai/user/zhangzhanluo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to set up a structured multi-agent coding workflow in an existing project. It creates the project goals, collaboration log, and Planner, Executor, and Reviewer guide documents needed to run the workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow launches persistent Planner, Executor, and Reviewer agents that can keep acting on a repository. <br>
Mitigation: Use it only in repositories where you intentionally want autonomous multi-agent coding, record loop job IDs, and stop the loops when work is paused or complete. <br>
Risk: Generated role guides can lead agents to edit code and mutate git state, including stashing or committing changes. <br>
Mitigation: Start from a clean git state, review the generated .pre guides before launch, and disable or revise stash and commit instructions if those actions need human approval. <br>
Risk: Persistent agents may read or act on unrelated repository content if project scope is not clear. <br>
Mitigation: Keep secrets and unrelated work out of scope, define the project code directory carefully, and review the project goals document before starting the agent loops. <br>


## Reference(s): <br>
- [PRE Engineering Skill on ClawHub](https://clawhub.ai/zhangzhanluo/pre-engineering) <br>
- [zhangzhanluo publisher profile](https://clawhub.ai/user/zhangzhanluo) <br>
- [Collaboration Log Format Reference](references/collaboration-log-format-reference.md) <br>
- [Planner Guide Template](references/planner-guide-template.md) <br>
- [Executor Guide Template](references/executor-guide-template.md) <br>
- [Reviewer Guide Template](references/reviewer-guide-template.md) <br>
- [PRE State System Reference](references/state-system-reference.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Files, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown documents and startup instructions with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generates five .pre collaboration documents after user confirmation and includes guidance for launching persistent Planner, Executor, and Reviewer agent loops.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
