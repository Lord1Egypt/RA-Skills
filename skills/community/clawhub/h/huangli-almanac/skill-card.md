## Description: <br>
Looks up Chinese huangli almanac information for a queried date, including Gregorian and lunar date details, ganzhi, five elements, auspicious activities, and avoided activities. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bettersao](https://clawhub.ai/user/bettersao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents can use this skill to answer date-specific huangli questions and provide culturally relevant almanac guidance for planning events such as weddings, openings, moving, renovation, or burial ceremonies. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Date queries are sent to api.tiax.cn and responses depend on that third-party service. <br>
Mitigation: Avoid using the skill for highly private event dates unless third-party processing is acceptable, and review returned almanac guidance before relying on it for decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bettersao/huangli-almanac) <br>
- [tiax.cn API homepage](https://api.tiax.cn) <br>
- [tiax.cn almanac endpoint](https://api.tiax.cn/almanac/) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Plain text or Markdown with formatted Chinese almanac fields and optional shell command examples.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Sends year, month, and day inputs to api.tiax.cn; no API key is required.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
