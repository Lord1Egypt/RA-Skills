## Description: <br>
Provides classical Chinese poetry generation and poetry lookup using the chinese-poetry dataset. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Wscats](https://clawhub.ai/user/Wscats) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to generate classical Chinese poems by theme, style, and form, or to retrieve and analyze poems by author, title, keyword, dynasty, or collection. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The setup script downloads a large external poetry dataset from GitHub before first use. <br>
Mitigation: For reproducible or higher-trust environments, pin the dataset repository to a known commit and verify the downloaded contents before use. <br>


## Reference(s): <br>
- [Poetry on ClawHub](https://clawhub.ai/Wscats/poetry) <br>
- [chinese-poetry dataset](https://github.com/chinese-poetry/chinese-poetry) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown or structured Chinese text containing generated poetry, lookup results, annotations, and creation notes.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May rely on a local chinese-poetry dataset downloaded before first use.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
