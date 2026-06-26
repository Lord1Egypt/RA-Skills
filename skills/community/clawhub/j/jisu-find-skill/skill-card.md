## Description: <br>
用 find_skills.py 在 ClawHub 搜索或列举已装技能，支持 JSON 输出。当用户说：ClawHub 上有没有天气技能、我本地装了哪些 skill，或类似技能发现问题时，使用本技能。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jisuapi](https://clawhub.ai/user/jisuapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and developers use this skill to search ClawHub for relevant skills, list installed skills, inspect candidates, view stats, and prepare installs with a dry-run default. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search input can include stdin or @file content and may be sent to ClawHub search or API lookups. <br>
Mitigation: Use normal search terms where possible and avoid passing sensitive files or stdin as search input. <br>
Risk: Running install with --execute may add a new skill with its own code and behavior to the agent environment. <br>
Mitigation: Use the dry-run default first, and only run install --execute after reviewing and trusting the target skill. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/jisuapi/jisu-find-skill) <br>
- [Publisher Profile](https://clawhub.ai/user/jisuapi) <br>
- [JisuAPI](https://www.jisuapi.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, guidance] <br>
**Output Format:** [Human-readable terminal text or structured JSON, with command examples in Markdown documentation.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Search and list commands can include ranked results, install hints, detail lines, and optional JSON output.] <br>

## Skill Version(s): <br>
1.0.2 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
