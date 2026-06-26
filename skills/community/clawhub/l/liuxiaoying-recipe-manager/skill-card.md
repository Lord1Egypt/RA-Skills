## Description: <br>
Recipe Manager helps agents manage commercial ingredient recipes, track multiple recipe versions, calculate ingredient costs, retrieve standard ratios, and export recipe data as CSV or Excel files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[luzewen](https://clawhub.ai/user/luzewen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to store beverage and ingredient recipes, retrieve standard preparation ratios, calculate per-recipe costs, and export recipe tables for operational use. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Recipe formulas and cost data are stored in local home-directory files. <br>
Mitigation: Use the skill only where local file storage, backups, sharing behavior, and filesystem permissions are acceptable for the sensitivity of the recipes. <br>
Risk: CSV or XLSX exports may write recipe and cost data to default or user-selected paths. <br>
Mitigation: Check the export destination before sharing or backing up exported files, especially for confidential commercial recipes. <br>
Risk: Delete and export actions may not provide clear confirmation prompts. <br>
Mitigation: Review requested actions before execution and keep a backup of important recipe data. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/luzewen/liuxiaoying-recipe-manager) <br>
- [Source repository](https://github.com/luzewen/openclaw-recipe-manager) <br>
- [Publisher profile](https://clawhub.ai/user/luzewen) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, files, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON command results; CSV or XLSX export files when requested] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores recipe and cost data in local home-directory files and may export recipe tables to user-selected or default home-directory paths.] <br>

## Skill Version(s): <br>
0.1.0 (source: release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
