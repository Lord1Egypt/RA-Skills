## Description: <br>
Skill marketplace for OpenClaw agents. One subscription, unlimited tools. Search, download, and install skills from the LarryBrain library. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[OllieWazza](https://clawhub.ai/user/OllieWazza) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and OpenClaw users use Larrybrain to search a third-party skill marketplace, download selected skills, install them locally, and follow their setup instructions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Downloaded remote skills may be given authority to write files and run setup on the user's machine. <br>
Mitigation: Require explicit user confirmation before each search, download, file write, dependency install, command run, service start, or update. <br>
Risk: Remote skill content may include unsafe or misleading instructions. <br>
Mitigation: Inspect downloaded files and paths before use, treat update responses as untrusted text, and sandbox setup where possible. <br>
Risk: The LarryBrain API key could be exposed through local environment handling or logs. <br>
Mitigation: Protect the API key, avoid displaying it, and rotate it if exposure is suspected. <br>


## Reference(s): <br>
- [ClawHub Larrybrain release page](https://clawhub.ai/OllieWazza/larrybrain) <br>
- [LarryBrain website](https://www.larrybrain.com) <br>
- [LarryBrain documentation](https://docs.larrybrain.com) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration, files] <br>
**Output Format:** [Markdown instructions with inline shell commands and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May call the LarryBrain API, write downloaded skill files locally, and require LARRYBRAIN_API_KEY for premium downloads.] <br>

## Skill Version(s): <br>
1.5.3 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
