## Description: <br>
Contribute to the OpenClaw core repository using the repo's own CONTRIBUTING.md rules. Use when working in `openclaw/openclaw` or a fork to triage issues, plan a focused fix, choose the right validation commands, prepare AI-assisted PRs, route changes to the right subsystem maintainers, or avoid breaking OpenClaw contribution norms. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[manjaroblack](https://clawhub.ai/user/manjaroblack) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill when contributing to `openclaw/openclaw` or a fork to plan focused fixes, choose validation commands, prepare AI-assisted PRs, and route changes to maintainers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Recommended build or test commands may not fit a dirty, unusual, or outdated OpenClaw checkout. <br>
Mitigation: Review the repository state and generated recommendations before running commands. <br>
Risk: The optional PR-body generator writes Markdown to the path supplied with `--output`. <br>
Mitigation: Use `--output` only with an intended destination and review the generated PR body before submission. <br>
Risk: OpenClaw contribution norms can change after this skill release. <br>
Mitigation: Start with the target repo's root `CONTRIBUTING.md` and treat it as the source of truth. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/manjaroblack/openclaw-contributor) <br>
- [OpenClaw Contributor Repository](https://github.com/manjaroblack/openclaw-contributor-skill) <br>
- [OpenClaw Contribution Checklist](references/contributing-checklist.md) <br>
- [OpenClaw PR Template Guide](references/pr-template.md) <br>
- [Example Perplexity Check Plan](references/example-perplexity-check-plan.txt) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Code, JSON] <br>
**Output Format:** [Markdown guidance with optional generated PR-body Markdown and JSON validation plans] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May run bundled Python scripts against a local OpenClaw git checkout to recommend checks or draft PR text.] <br>

## Skill Version(s): <br>
0.1.1 (source: release evidence and changelog) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
