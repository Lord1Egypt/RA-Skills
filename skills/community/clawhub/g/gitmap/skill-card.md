## Description: <br>
Provides Git-like version control tools for ArcGIS web maps, enabling branch management, commits, diffs, and sync with ArcGIS Portal using the gitmap CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[14-TR](https://clawhub.ai/user/14-TR) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and GIS engineers use this skill to inspect, version, branch, commit, compare, push, and pull ArcGIS web map state through GitMap workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: ArcGIS web maps can be changed through push, pull, commit, and branch operations. <br>
Mitigation: Review requested map operations before allowing them, especially push, pull, branch deletion, clone, init, or raw CLI-style requests. <br>
Risk: Portal credentials may be supplied to tool calls or inherited from environment variables. <br>
Mitigation: Use scoped ArcGIS tokens or a limited account, prefer environment variables over per-call passwords, and avoid storing plaintext credentials in prompts or logs. <br>
Risk: The local HTTP server exposes tool endpoints while it is running. <br>
Mitigation: Run the server only when actively using the skill and stop it after the workflow is complete. <br>


## Reference(s): <br>
- [ClawHub Git-Map skill page](https://clawhub.ai/14-TR/gitmap) <br>
- [GitMap project](https://github.com/14-TR/gitmap) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, shell commands, configuration, guidance] <br>
**Output Format:** [Structured JSON tool responses with stdout, stderr, return codes, parsed map or commit data where available, and Markdown documentation examples.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires gitmap-core and ArcGIS Portal credentials; most operations require a local GitMap repository working directory.] <br>

## Skill Version(s): <br>
0.1.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
