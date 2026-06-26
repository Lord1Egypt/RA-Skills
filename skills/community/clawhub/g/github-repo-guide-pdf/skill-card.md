## Description: <br>
Analyzes a GitHub repository URL or OWNER/REPO and produces a Chinese, usage-first user guide with Markdown and PDF outputs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[smile618](https://clawhub.ai/user/smile618) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and operators use this skill when they provide a GitHub repository and need a Chinese guide that explains how to install, configure, run, and troubleshoot the project. It is intended for usage documentation rather than implementation analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill clones and summarizes user-provided repositories, which may expose private or sensitive repository content in generated Markdown, PDF, or intermediate build files. <br>
Mitigation: Use it only with repositories the user is comfortable processing locally, and review or remove generated files when handling sensitive content. <br>
Risk: The PDF build converts repository-derived Markdown through local pandoc and TeX/PDF tooling. <br>
Mitigation: Use trusted local gh, pandoc, and TeX/PDF installations, especially when processing untrusted repository Markdown. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/smile618/github-repo-guide-pdf) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Files, Guidance] <br>
**Output Format:** [Chinese Markdown guide, PDF file, and MEDIA lines] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generates output files under the workspace media directory and creates an intermediate combined Markdown file during PDF conversion.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
