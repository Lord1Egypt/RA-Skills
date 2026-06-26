## Description: <br>
Name Generator helps create Chinese baby names, English names, pen names, usernames, and brand names with meaning notes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ckchzh](https://clawhub.ai/user/ckchzh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to generate and refine name recommendations for babies, companies, pen names, usernames, and English names. The script output is a starting point that can be adjusted for user preferences. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Name recommendations can be culturally inappropriate, misleading, or conflict with existing people, brands, domains, or trademarks. <br>
Mitigation: Treat generated names as suggestions and review meaning, pronunciation, social context, domain availability, and trademark conflicts before use. <br>
Risk: The auxiliary script can store user-provided entries and command history in a local name-generator data directory. <br>
Mitigation: Avoid entering sensitive personal details unless local storage is acceptable, and review or remove local name-generator data when needed. <br>
Risk: The skill runs local Bash and Python scripts. <br>
Mitigation: Install only when comfortable running local scripts, use the documented scripts/name.sh commands, and review script contents before deployment. <br>


## Reference(s): <br>
- [Name Generator ClawHub release](https://clawhub.ai/ckchzh/name-generator) <br>
- [Name Generator tips](tips.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Markdown or plain text with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Name suggestions may include meaning notes and randomized local script output.] <br>

## Skill Version(s): <br>
2.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
