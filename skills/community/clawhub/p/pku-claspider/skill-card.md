## Description: <br>
PKU Claspider helps agents guide use of a PKU course-catalog scraping CLI that gathers and merges read-only course data from dean.pku.edu.cn, elective.pku.edu.cn, and onlineroomse.pku.edu.cn. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wjsoj](https://clawhub.ai/user/wjsoj) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External PKU developers and course-data users use this skill when they need agent guidance for scraping full-semester course catalogs, filtering by department, teacher, keyword, or category, and merging dean, elective, and Zhiyun course data into JSON for offline lookup or analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Zhiyun browser tokens are sensitive credentials and may be exposed through shared terminals, shell history, or logs. <br>
Mitigation: Use authenticated modes only on trusted machines, avoid pasting real JWTs into shared contexts, and prefer safer local secret handling where the CLI supports it. <br>
Risk: The skill guides execution of local claspider and elective CLI code. <br>
Mitigation: Install and run the CLI only when the local code and package source are trusted. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wjsoj/pku-claspider) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline bash commands and JSON-oriented workflow guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include instructions for handling local CLI credentials and exporting course data as JSON.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
