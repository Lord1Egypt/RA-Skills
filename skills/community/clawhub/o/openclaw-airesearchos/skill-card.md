## Description: <br>
Deep research powered by AIresearchOS. Submit, track, and retrieve research with clarifying questions. Supports API key auth and x402 USDC payments. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bowtiedbluefin](https://clawhub.ai/user/bowtiedbluefin) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and external users use this skill to submit AIresearchOS deep research requests, answer clarifying questions, monitor job status, retrieve cited Markdown reports, and check credits or research history from an OpenClaw assistant. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Research prompts are sent to an external AIresearchOS service. <br>
Mitigation: Avoid submitting sensitive data unless the user has approved the external service for that use. <br>
Risk: x402 mode can spend USDC using a wallet key. <br>
Mitigation: Use a dedicated low-balance wallet, confirm paid mode and price before each request, and keep wallet keys out of chat and command-line arguments. <br>
Risk: Custom base URLs and returned research content may be untrusted. <br>
Mitigation: Avoid untrusted custom base URLs and present returned reports as external content rather than executable instructions. <br>


## Reference(s): <br>
- [AIresearchOS homepage](https://airesearchos.com) <br>
- [ClawHub skill page](https://clawhub.ai/bowtiedbluefin/openclaw-airesearchos) <br>
- [SETUP.md](SETUP.md) <br>
- [README.md](README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, API calls, guidance] <br>
**Output Format:** [Markdown responses with inline shell commands and JSON API examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May schedule background status checks and returns external research reports as untrusted content.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
