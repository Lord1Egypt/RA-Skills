## Description: <br>
Find natural hot springs and thermal baths - outdoor pools, private onsen, medicinal springs, and spa complexes - plus related travel services powered by Fliggy. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiejinsong](https://clawhub.ai/user/xiejinsong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External travelers and travel-planning agents use this skill to find hot springs, thermal baths, and related booking options from FlyAI/Fliggy CLI results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks the agent to install and run an unpinned global third-party CLI. <br>
Mitigation: Approve the FlyAI/Fliggy CLI source and installation before use; prefer a reviewed, pinned installation path where the host environment supports it. <br>
Risk: The skill may store raw travel queries in a local execution log. <br>
Mitigation: Disable, redact, or delete the local execution log when travel queries should not be retained on disk. <br>
Risk: Travel results depend on live CLI output and may be unavailable or incomplete if the CLI, network, or upstream service fails. <br>
Mitigation: Run the documented environment check and fallback steps, and report retrieval failures instead of answering from model memory. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xiejinsong/hot-springs) <br>
- [templates.md](references/templates.md) <br>
- [playbooks.md](references/playbooks.md) <br>
- [fallbacks.md](references/fallbacks.md) <br>
- [runbook.md](references/runbook.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with booking links and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs should be based on flyai CLI results, include booking links when results are shown, and avoid raw JSON.] <br>

## Skill Version(s): <br>
3.2.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
