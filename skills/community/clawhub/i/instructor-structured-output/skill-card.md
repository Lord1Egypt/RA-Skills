## Description: <br>
Provides agent guidance for Instructor structured-output patterns, while the bundled authoritative seed also routes agents toward finance/ZVT data-fetching and backtesting workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tangweigang-jpg](https://clawhub.ai/user/tangweigang-jpg) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and AI-engineering users can use this skill for guidance on typed LLM outputs with Pydantic models, provider modes, validation retries, and related anti-patterns. Review before execution because the packaged evidence also contains finance/ZVT workflows that can install packages, fetch market data, run backtests, write local files, and create saved skills. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release is advertised as Instructor structured-output guidance, but the authoritative seed also drives finance/ZVT workflows. <br>
Mitigation: Install only when the finance/ZVT behavior is intentional, and review the bundled seed before relying on generated guidance. <br>
Risk: Generated workflows may request package installation, command execution, market-data fetches, provider or broker credentials, local writes, and saved-skill actions. <br>
Mitigation: Require explicit user approval for each install, command, data fetch, credential step, file write, and saved-skill action. <br>
Risk: The security verdict is suspicious due to artifact-backed mismatch and under-scoped authority, while VirusTotal was pending. <br>
Mitigation: Treat clean static scan output as insufficient by itself; perform manual review and scan before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tangweigang-jpg/instructor-structured-output) <br>
- [Doramagic crystal page](https://doramagic.ai/zh/crystal/instructor-structured-output) <br>
- [seed.yaml](references/seed.yaml) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with code and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [No installation is required for the knowledge skill itself; generated workflows may request package installation, command execution, data fetches, credential-dependent providers, local file writes, and saved-skill creation.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata; SKILL.md metadata lists v0.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
