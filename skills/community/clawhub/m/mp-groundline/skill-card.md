## Description: <br>
Migrates a WeChat Mini Program from the Skyline renderer to WebView, keeps page visuals and behavior consistent, and produces a MIGRATION-MAP document for review. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vincentjiang06](https://clawhub.ai/user/vincentjiang06) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to move WeChat Mini Programs off Skyline and onto WebView with minimal, reviewable changes. It scans for Skyline-specific patterns, generates a MIGRATION-MAP, flips renderer configuration, and guides verification before targeted fixes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill modifies renderer configuration and may touch page JSON files in a target Mini Program. <br>
Mitigation: Run it in a git-backed project, review the generated MIGRATION-MAP before edits, and use the documented rollback path for app.json and touched page JSON files. <br>
Risk: Verification may capture screenshots and pageData through vince-mp. <br>
Mitigation: Capture only the pages needed for migration review and handle screenshots and pageData according to the target project's data handling rules. <br>
Risk: Skyline-only features such as worklets, custom routes, or exclusive components have no direct WebView equivalent. <br>
Mitigation: Treat rewrite findings as manual-review gates and do not silently drop or auto-rewrite those features. <br>
Risk: Modernizing existing Skyline-era workarounds can create avoidable visual or behavioral drift. <br>
Mitigation: Keep compatible workarounds by default and only apply the smallest fix for deltas confirmed by before-and-after verification. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/vincentjiang06/skills/mp-groundline) <br>
- [Skyline to WebView mapping](references/skyline-to-webview.md) <br>
- [Scanner contract](references/scanner-contract.md) <br>
- [Scan protocol](rules/scan-protocol.md) <br>
- [Verify with vince-mp](rules/verify-with-vince-mp.md) <br>
- [Minimal-fix protocol](rules/minimal-fix-protocol.md) <br>
- [Metric plan](assets/metric-plan.json) <br>
- [Release manifest](assets/release-manifest.json) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance, deterministic JSON scan output, and targeted code or configuration edits] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes a MIGRATION-MAP.md, scan findings, manual rewrite gates, and minimal renderer edits.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
