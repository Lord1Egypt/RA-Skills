## Description: <br>
Skill 发现中心 helps agents search a built-in sample catalog of ClawHub skills and return command-style recommendations, details, tags, and discovery guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hgta23](https://clawhub.ai/user/hgta23) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and ClawHub users use this skill to discover skills by keyword, tag, popularity, similarity, and simple recommendation commands. Treat its management-style responses as informational because server security evidence says installs and saved favorites are simulated. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Install and management commands can imply real ClawHub actions even though server security evidence says those actions are simulated. <br>
Mitigation: Treat install, favorites, history, and management responses as guidance only, and verify actual skill state in ClawHub before relying on it. <br>
Risk: Recommendations, popularity, and skill details are based on static bundled data rather than live ClawHub metadata. <br>
Mitigation: Cross-check recommendations and skill details against the ClawHub skill page or another trusted catalog source before installing. <br>
Risk: Server security guidance reports that the JavaScript file is syntactically invalid due escaped operators. <br>
Mitigation: Review and fix the JavaScript, then test it in a sandbox before enabling runtime use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hgta23/h) <br>
- [Publisher profile](https://clawhub.ai/user/hgta23) <br>


## Skill Output: <br>
**Output Type(s):** [text, guidance] <br>
**Output Format:** [Plain text command responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a static in-memory skill catalog and does not perform verified live installs, persistent favorites, or live ClawHub catalog updates.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
