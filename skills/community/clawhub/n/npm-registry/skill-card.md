## Description: <br>
Search npm packages, inspect metadata and versions, review download stats, and check security advisories via the npm API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hith3sh](https://clawhub.ai/user/hith3sh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to explore npm registry data, verify package integrity, monitor package health, and inspect advisories through ClawLink-backed npm tools. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires connecting npm through ClawLink and may access private package data within the connected npm account. <br>
Mitigation: Use the least-privileged npm account or token practical, review the live tool list after setup, and only install if ClawLink credential handling is acceptable for the environment. <br>
Risk: Some npm write operations, such as token deletion or scope changes, can modify account state. <br>
Mitigation: Preview and explicitly confirm write actions only when the requested change matches the user's intent; prefer read, list, search, and describe operations first. <br>
Risk: The live ClawLink tool catalog may change over time. <br>
Mitigation: Treat `clawlink_list_tools --integration npm` and `clawlink_describe_tool` as the source of truth before calling unfamiliar or ambiguous tools. <br>


## Reference(s): <br>
- [ClawHub npm Registry Skill](https://clawhub.ai/hith3sh/npm-registry) <br>
- [npm Documentation](https://docs.npmjs.com/) <br>
- [npm Registry API](https://github.com/npm/registry) <br>
- [npm Security Advisories](https://www.npmjs.com/advisories) <br>
- [ClawLink OpenClaw Docs](https://docs.claw-link.dev/openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, text] <br>
**Output Format:** [Markdown with inline bash code blocks and tool-call examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include npm package metadata, version details, download statistics, security advisory summaries, setup steps, and connection troubleshooting guidance.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
