## Description: <br>
Osori is a local project registry and context loader that helps agents find, inspect, switch between, and manage projects through Telegram slash commands or shell scripts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oozoofrog](https://clawhub.ai/user/oozoofrog) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and engineers use Osori to maintain a local project registry, discover projects, inspect git status and repository fingerprints, and load project context before working in an agent session. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Osori reads local project metadata and writes registry and cache files. <br>
Mitigation: Review configured discovery roots, OSORI_SEARCH_PATHS, OSORI_REGISTRY, and OSORI_CACHE_FILE before enabling broad scans or fixes. <br>
Risk: GitHub PR and issue counts may reveal repository identifiers and request timing to GitHub when gh is used. <br>
Mitigation: Use GitHub-backed commands only for repositories where that disclosure is acceptable, and rely on the TTL cache to reduce repeated queries. <br>
Risk: Registry repair commands can change or reinitialize local registry data when fix flags are used. <br>
Mitigation: Run doctor in its default preview mode first, review the risk plan, and use generated backups for recovery if a fix is applied. <br>
Risk: Fuzzy project switching can select the wrong project when names are similar. <br>
Mitigation: Use root filters and explicit --index selection when multiple candidates are shown. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/oozoofrog/osori) <br>
- [README](README.md) <br>
- [Multi-root Design](docs/multi-root-design.md) <br>
- [v1.5 Roadmap](docs/roadmap-v1.5.md) <br>
- [Entire CLI](https://entire.io) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown or plain text with inline shell commands; selected health checks can return JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include local project paths, git status summaries, repository fingerprints, and registry health findings.] <br>

## Skill Version(s): <br>
1.6.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
