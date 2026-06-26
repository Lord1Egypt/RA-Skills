## Description: <br>
GitHub Reader generates structured analysis reports for public GitHub repositories using the GitHub REST API without third-party analysis services. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[krislu1221](https://clawhub.ai/user/krislu1221) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and engineers use this skill to inspect explicitly named public GitHub repositories and produce a concise report with project metadata, README summary, links, and quick-start commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Repository names requested for analysis are sent to GitHub's API and resulting reports may be cached locally. <br>
Mitigation: Use the skill only for repository identifiers that can be disclosed to GitHub API logs and local cache storage; clear or relocate the cache when needed. <br>
Risk: Reports are based on GitHub API metadata and README content, so they may not represent private repository state or full code-level behavior. <br>
Mitigation: Review the generated report before relying on it for decisions and use a GitHub token only where authorized. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/krislu1221/github-reader) <br>
- [README](artifact/README.md) <br>
- [Security notes](artifact/SECURITY.md) <br>
- [Release notes](artifact/RELEASE_NOTES.md) <br>
- [License](artifact/LICENSE) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Text, Shell commands, Guidance] <br>
**Output Format:** [Markdown report with tables and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses GitHub REST API data and a local cache; report content depends on public repository metadata and README availability.] <br>

## Skill Version(s): <br>
3.2.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
