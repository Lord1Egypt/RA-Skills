## Description: <br>
Gigo Lobster Taster runs the full GIGO benchmark, uploads verified results by default, generates a personal result page, and enters the result on the leaderboard. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gigolab](https://clawhub.ai/user/gigolab) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to run a multi-task agent benchmark, produce local result artifacts, and optionally publish verified results to the GIGO result page and leaderboard. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The default mode uploads detailed benchmark results to the GIGO API and may create a public result page or leaderboard entry. <br>
Mitigation: Use the local or offline mode where available when cloud submission is not intended, and review generated reports before sharing links. <br>
Risk: The benchmark may execute local tests and package commands and create local caches or work directories. <br>
Mitigation: Run it in a dedicated workspace with only the files needed for evaluation, and review the security guidance before deployment. <br>
Risk: The skill may load OpenClaw-related profile or secrets files while running. <br>
Mitigation: Keep unrelated secrets out of workspace-level secrets.env files and use scoped credentials for benchmark runs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/gigolab/gigo-lobster-taster) <br>
- [GIGO Lobster Skill Family README](artifact/README.md) <br>
- [GIGO Lobster Taster v2 Bundle README](artifact/bundle/README.md) <br>
- [GIGO Lobster Taster Integration Guide](artifact/bundle/INTEGRATION.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance, Files] <br>
**Output Format:** [Markdown guidance with shell commands plus generated HTML, PNG or SVG, and log files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces benchmark progress updates and writes outputs such as lobster-report.html, lobster-cert.png or lobster-cert.svg, and gigo-run.log.] <br>

## Skill Version(s): <br>
2.1.2 (source: server release evidence and manifest.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
