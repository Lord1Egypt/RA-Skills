## Description: <br>
Production code audit via git blame that provides natural language risk analysis for overtime commits, scattered changes, no-PR-review merges, and impact domain tracing for suspicious lines. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[harrylabsj](https://clawhub.ai/user/harrylabsj) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, security auditors, tech leads, and on-call engineers use this skill to triage code safety by combining local git blame data, commit metadata, author patterns, and impact-domain analysis into a risk-focused audit report. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads local git history and author metadata from repositories where it is invoked. <br>
Mitigation: Install and use it only in repositories where that metadata access is acceptable. <br>
Risk: Risk scores and author-pattern findings can be mistaken for proof of malicious intent or unsafe code. <br>
Mitigation: Treat the output as triage guidance and have a qualified reviewer confirm findings before taking action. <br>
Risk: Broad or accidental invocation could expose more repository history than intended to the agent session. <br>
Mitigation: Prefer explicit use through /git-blame-audit and scope requests to the relevant file, line, range, author, or time window. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/harrylabsj/git-blame) <br>
- [Publisher profile](https://clawhub.ai/user/harrylabsj) <br>
- [Project homepage](https://github.com/harry) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown risk reports with tables, concise verdicts, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local repository git history and author metadata; does not make install-time code changes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
