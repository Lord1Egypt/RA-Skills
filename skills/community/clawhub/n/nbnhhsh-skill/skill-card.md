## Description: <br>
Translate Chinese pinyin initialisms and internet abbreviations to their possible full Chinese meanings, supporting multiple terms at once. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[JayeGT002](https://clawhub.ai/user/JayeGT002) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to look up Chinese pinyin initialisms and internet abbreviations, including batch queries, and return possible full Chinese interpretations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad trigger wording may activate the skill when the user did not intend a pinyin abbreviation lookup. <br>
Mitigation: Confirm intent before using the lookup flow for vague prompts or unexplained strings. <br>
Risk: Lookup text may be sent to an external API. <br>
Mitigation: Avoid using the skill on private, confidential, or sensitive text. <br>
Risk: The API may have rate limits or pending-review results. <br>
Mitigation: Respect rate limits, avoid unnecessary repeated queries, and present pending-review or ambiguous results as uncertain. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/JayeGT002/nbnhhsh-skill) <br>
- [nbnhhsh lookup API](https://lab.magiconch.com/api/nbnhhsh/guess) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks and plain-text lookup results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May return multiple possible interpretations for each abbreviation; API responses can include pending-review results.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
