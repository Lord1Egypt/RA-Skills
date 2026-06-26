## Description: <br>
Analyzes and visualizes Git commit time distribution for repositories by day, hour, weekday, and weekday-hour heatmap. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangyendt](https://clawhub.ai/user/wangyendt) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to run gitstats against a Git repository, filter by branch or date range, and generate commit activity charts for review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Analyzing private repositories can process commit metadata across the selected branch scope. <br>
Mitigation: Run it only on repositories intended for analysis, and use --all on private repositories only when all branch history is in scope. <br>
Risk: Saved chart output can overwrite an existing file at the selected path. <br>
Mitigation: Choose --save paths deliberately and review existing files before writing output. <br>
Risk: The skill depends on a local gitstats command and Python plotting dependencies. <br>
Mitigation: Install gitstats, pandas, and matplotlib from trusted sources before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wangyendt/gitstats) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, guidance, files] <br>
**Output Format:** [Markdown with inline bash command examples and command option guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May save chart image files or display a plot when the underlying gitstats command is run.] <br>

## Skill Version(s): <br>
0.1.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
