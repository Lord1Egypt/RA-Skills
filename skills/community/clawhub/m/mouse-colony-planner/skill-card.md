## Description: <br>
Calculate breeding timelines and cage requirements for transgenic mouse colonies. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aipoch-ai](https://clawhub.ai/user/aipoch-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External researchers, lab staff, and developers use this skill to estimate transgenic mouse breeding timelines, cage requirements, costs, and breeding flowcharts from command-line parameters. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Wet-lab assumptions or input parameters may produce inaccurate colony timelines, cage counts, or cost estimates. <br>
Mitigation: Have qualified lab staff verify breeding assumptions and parameter values before relying on the generated plan. <br>
Risk: Unnecessary or unpinned dependencies can add avoidable installation risk. <br>
Mitigation: Install and run the skill in a virtual environment, and remove or pin the dataclasses and enum dependencies before operational use. <br>


## Reference(s): <br>
- [Mouse Colony Planner on ClawHub](https://clawhub.ai/aipoch-ai/mouse-colony-planner) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Command-line text output with timelines, cage counts, cost estimates, and a breeding flowchart.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs depend on user-supplied breeding scheme, colony size, timing, cage capacity, and cost parameters.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
