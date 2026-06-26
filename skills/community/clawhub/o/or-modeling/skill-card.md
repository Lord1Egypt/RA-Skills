## Description: <br>
Helps users turn real-world operations research problems into mathematical optimization models, including objective functions, constraints, assumptions, complexity estimates, literature context, and LaTeX model output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Go-own-way](https://clawhub.ai/user/Go-own-way) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, researchers, and students use this skill to formulate operations research problems as optimization models, validate assumptions, search relevant academic literature when needed, and produce clear mathematical model documentation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Academic paper searches may send user-provided keywords to OpenAlex or Semantic Scholar. <br>
Mitigation: Keep confidential business data, client names, private datasets, and sensitive operational details out of search keywords. <br>
Risk: Quick confirmation mode can let modeling assumptions proceed with limited review. <br>
Mitigation: Review and confirm assumptions before relying on the generated optimization model or allowing the workflow to continue. <br>


## Reference(s): <br>
- [Operations Research Modeling ClawHub listing](https://clawhub.ai/Go-own-way/or-modeling) <br>
- [Operations Research Problem Reference](artifact/references/or-problems.md) <br>
- [OpenAlex Works API](https://api.openalex.org/works) <br>
- [Semantic Scholar Graph API](https://api.semanticscholar.org/graph/v1/paper/search) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, latex, shell commands, guidance] <br>
**Output Format:** [Markdown with LaTeX model blocks, structured analysis tables, self-check reports, and optional shell commands for literature search.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May use scripts/paper_search.py to query OpenAlex and Semantic Scholar when literature review is needed.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
