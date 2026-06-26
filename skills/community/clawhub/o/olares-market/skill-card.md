## Description: <br>
Olares Market (olares-cli market) helps agents browse Olares Market catalogs and manage Olares app lifecycle, status, local chart upload, and chart deletion through authenticated olares-cli commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[olares](https://clawhub.ai/user/olares) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and Olares operators use this skill to inspect Olares Market inventory and run app lifecycle workflows such as install, upgrade, uninstall, clone, stop, resume, cancel, status checks, and local chart management. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Destructive lifecycle commands can interrupt or remove Olares app services. <br>
Mitigation: Require the agent to show the exact app names, operation, source or cascade choice when relevant, and receive explicit confirmation before running uninstall, stop, cancel, upgrade, or bulk-stop workflows. <br>
Risk: Chart deletion removes local chart versions from the upload bucket. <br>
Mitigation: Confirm the chart name and version first, check whether the app is still running, and use uninstall before delete when the goal is to remove both the deployment and its local chart source. <br>
Risk: Authenticated olares-cli commands act through the user's active Olares profile. <br>
Mitigation: Verify the intended Olares ID/profile before mutating commands and follow the shared authentication guidance for login, token refresh, and auth-error recovery. <br>


## Reference(s): <br>
- [Olares Market release page](https://clawhub.ai/olares/olares-market) <br>
- [market list / categories / get / status](references/olares-market-list.md) <br>
- [market lifecycle](references/olares-market-lifecycle.md) <br>
- [market upload / delete](references/olares-market-charts.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and optional JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May recommend olares-cli commands that mutate Olares app state or local chart storage.] <br>

## Skill Version(s): <br>
4.0.1 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
