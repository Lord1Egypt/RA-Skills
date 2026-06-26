## Description: <br>
Unused CSS detector and dead selector auditor that scans stylesheet files against HTML, JSX, TSX, Vue, and template files to find selectors that appear to be defined but unreferenced. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[PHY041](https://clawhub.ai/user/PHY041) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and frontend engineers use this skill to audit CSS, Sass, Less, Tailwind, Bootstrap, and CSS Modules projects for cleanup candidates, duplicate selectors, orphaned module files, and estimated size savings. It is best used as a review aid before manual deletion, not as an automatic remover. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may give overconfident deletion guidance or ready-to-run file removal commands based on heuristic scans. <br>
Mitigation: Use the report as a review aid, commit or back up first, manually verify every selector or CSS module it flags, and only run deletion commands after confirming files are unused and recoverable. <br>
Risk: Dynamic class names, generated markup, framework conventions, or runtime-only selectors can make a selector look unused when it is still required. <br>
Mitigation: Run the skill inside the intended project, inspect generated candidates against application behavior, and validate cleanup with tests or visual review before merging changes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/PHY041/phy-css-dead-code) <br>
- [Publisher profile](https://clawhub.ai/user/PHY041) <br>
- [Canlah AI homepage](https://canlah.ai) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Guidance, Configuration] <br>
**Output Format:** [Markdown report with inline bash, Python, CSS, and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports dead selector candidates, verification commands, estimated byte savings, and cleanup guidance.] <br>

## Skill Version(s): <br>
1.0.3 (source: server-resolved release evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
