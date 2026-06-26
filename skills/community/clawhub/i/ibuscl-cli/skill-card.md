## Description: <br>
iBus.CL CLI helps agents use a terminal command to query real-time arrivals for Chilean public transport stops, with service filtering and raw JSON output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[iiroak](https://clawhub.ai/user/iiroak) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to install and run the iBus.CL CLI for checking Chilean public transport stop arrivals, filtering by bus service, and producing human-readable or raw JSON output for pipelines. <br>

### Deployment Geography for Use: <br>
Chile <br>

## Known Risks and Mitigations: <br>
Risk: The documented quick install path runs an unpinned remote shell script from GitHub. <br>
Mitigation: Prefer cloning the repository, reviewing install.sh, and installing manually or from a pinned release when available. <br>
Risk: Real-time stop lookups can fail because of invalid stop codes, connectivity problems, or timeouts. <br>
Mitigation: Handle the documented nonzero exit code and validate raw JSON output before using it in automation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/iiroak/ibuscl-cli) <br>
- [iBus.CL-API repository](https://github.com/iiroak/iBus.CL-API) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance, Configuration] <br>
**Output Format:** [Markdown with bash and JSON code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes CLI examples, readable output, JSON response shape, and exit-code behavior.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
