## Description: <br>
Designs academic poster layouts with section placement, visual hierarchy, size recommendations, and content flow guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aipoch-ai](https://clawhub.ai/user/aipoch-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to plan academic poster layouts from poster dimensions and content sections. It helps structure a bounded poster layout workflow and return explicit assumptions, section placement, and design recommendations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release security guidance notes that the skill's broad description can exceed its poster-specific capability. <br>
Mitigation: Treat the skill as an academic poster layout helper and confirm poster dimensions, sections, and scope before use. <br>
Risk: The artifact includes local Python execution and may read or write workspace files if adapted for user inputs. <br>
Mitigation: Review commands before execution, run in a sandboxed workspace, and keep output paths restricted to the intended project directory. <br>


## Reference(s): <br>
- [Poster Layout Planner References](references/guidelines.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/aipoch-ai/poster-layout-planner) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, JSON] <br>
**Output Format:** [Markdown response with optional shell commands and JSON layout output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires poster dimensions and a list of content sections; packaged script uses fixed demonstration inputs unless adapted.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
