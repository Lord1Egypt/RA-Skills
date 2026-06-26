## Description: <br>
Perform comprehensive website health checks covering performance, broken links, security headers, accessibility, and SEO issues. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mattvalenta](https://clawhub.ai/user/mattvalenta) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, site owners, and technical reviewers use this skill to audit a website for performance, broken links, accessibility, security headers, SSL details, and SEO issues, then summarize findings in a Markdown report. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Website audit commands and crawler scripts make network requests to target sites. <br>
Mitigation: Run checks only against authorized targets and keep crawl depth reasonable. <br>
Risk: Optional npx and pip tools may execute third-party code. <br>
Mitigation: Review or pin tool packages before allowing them to run. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown with inline bash and Python code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces audit findings, recommended checks, and a website audit report template; network checks should be run only against authorized targets.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
