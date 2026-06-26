## Description: <br>
Pearl Calc evaluates math expressions through a Pearl-backed paid calculator that charges $0.01 per expression. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[misteeka](https://clawhub.ai/user/misteeka) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and users can submit simple math expressions and receive calculated results after Pearl payment setup and user approval. The skill is suited to paid calculator calls where the user understands that expressions are sent to a third-party service. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Using the skill may incur charges through Pearl. <br>
Mitigation: Review the Pearl skill and payment setup before approval, and set spending limits or approved-skill controls. <br>
Risk: Math expressions are transmitted to pearlcash.ai. <br>
Mitigation: Avoid entering confidential financial, business, or personal values. <br>
Risk: The skill installs a Node.js dependency before use. <br>
Mitigation: Install only after reviewing the skill, package dependency, and payment behavior. <br>


## Reference(s): <br>
- [Pearl Calc on ClawHub](https://clawhub.ai/misteeka/pearl-calc) <br>
- [Pearl payment service](https://pearlcash.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration guidance] <br>
**Output Format:** [Plain text result with Markdown setup and usage guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js, the @pearl-cash/client dependency, Pearl setup, network access to pearlcash.ai, and user-approved paid requests.] <br>

## Skill Version(s): <br>
0.9.20 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
