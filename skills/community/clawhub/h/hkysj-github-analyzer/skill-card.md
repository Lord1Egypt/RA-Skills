## Description: <br>
Analyzes GitHub repositories for project metadata, technology stack signals, license posture, and deployment options, then generates a local Markdown report. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hkysj](https://clawhub.ai/user/hkysj) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to review public GitHub repositories for technical fit, open-source license considerations, and deployment planning during dependency evaluation or project due diligence. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The shell script contacts GitHub and writes Markdown reports to the local filesystem. <br>
Mitigation: Run it only in environments where outbound GitHub API access and local report creation are acceptable, and choose the output directory intentionally. <br>
Risk: Generated reports may include README excerpts or deployment commands from the analyzed repository. <br>
Mitigation: Treat repository-provided content as untrusted and review commands or excerpts before acting on them. <br>
Risk: License and deployment recommendations are heuristic summaries and may not cover all project-specific obligations. <br>
Mitigation: Verify license terms and deployment steps against authoritative repository documentation and appropriate legal or engineering review. <br>


## Reference(s): <br>
- [Open-source license reference](references/licenses.md) <br>
- [ClawHub skill page](https://clawhub.ai/hkysj/hkysj-github-analyzer) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Analysis, Files, Guidance] <br>
**Output Format:** [Markdown report with tables and inline shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes reports to a user-selected output directory, defaulting to ~/Desktop/github-reports.] <br>

## Skill Version(s): <br>
1.0.3 (source: ClawHub release metadata; artifact frontmatter reports 1.0.2) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
