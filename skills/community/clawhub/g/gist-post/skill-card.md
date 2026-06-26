## Description: <br>
Post content to GitHub Gist and get back a shareable URL. Rich context sharing between agents, operators, and humans. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[psiclawops](https://clawhub.ai/user/psiclawops) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents, operators, and developers use this skill to publish selected markdown content, summaries, logs, or handoff notes to GitHub Gist and return a shareable URL for humans or future agent sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected content may be published to GitHub Gist with secrets, personal data, private logs, proprietary code, or internal context. <br>
Mitigation: Review every Gist before posting and avoid publishing sensitive or proprietary information. <br>
Risk: A GitHub token with excessive permissions could increase account or repository exposure if mishandled. <br>
Mitigation: Use a Personal Access Token limited to the gist scope and avoid storing or pasting real tokens into prompts or shared files. <br>
Risk: Secret Gists are not indexed but remain accessible to anyone with the URL. <br>
Mitigation: Use --secret for non-indexed sharing only when appropriate and still treat the URL as shareable access. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/psiclawops/gist-post) <br>
- [Skill homepage](https://github.com/PsiClawOps/gist-share) <br>
- [GitHub CLI](https://cli.github.com) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Markdown, Guidance] <br>
**Output Format:** [Markdown with inline bash commands and a returned GitHub Gist URL] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires GitHub CLI access and a gist-scoped GITHUB_TOKEN; can create public or secret Gists.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
