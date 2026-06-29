## Description: <br>
Audits a Next.js App Router codebase for React Server Component boundary mistakes, request waterfalls, client/server anti-patterns, and Core Web Vitals risks, then proposes concrete fixes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sioncoolwijk](https://clawhub.ai/user/sioncoolwijk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to audit Next.js App Router applications for correctness, performance, streaming, SEO, and client/server boundary issues. It combines a local static scanner with a manual review checklist and produces prioritized findings with concrete fixes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The scanner reads local Next.js source files and reports heuristic findings that may not capture project-specific intent. <br>
Mitigation: Review the cited files and manual checklist before treating findings as confirmed defects. <br>
Risk: Agent-proposed code changes could alter application behavior if applied without review. <br>
Mitigation: Only allow edits when explicitly requested, then rerun the scanner and project tests before accepting fixes. <br>


## Reference(s): <br>
- [App Router review checklist](reference/checklist.md) <br>
- [Sample audit report](examples/sample-report.md) <br>
- [ClawHub skill page](https://clawhub.ai/sioncoolwijk/nextjs-app-router-audit) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown report with file-level findings, severity, impact, concrete fixes, scanner commands, and optional JSON scanner output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Findings should be manually verified before reporting fixes as complete.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
