## Description: <br>
Helps an agent generate Giggle.pro videos, short films, narration videos, and short drama projects from a user's story or script. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[patches429](https://clawhub.ai/user/patches429) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to guide an agent through Giggle.pro video generation, including mode selection, optional style lookup, project submission, progress polling, payment handling, and returning the final signed download URL. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The default workflow can automatically spend Giggle account credits when payment is pending. <br>
Mitigation: Before running execute_workflow or pay, have the agent show project details and expected credit or money cost, then obtain explicit confirmation for that specific job. <br>
Risk: The skill requires a Giggle API key and sends authenticated requests to the Giggle.pro API. <br>
Mitigation: Install only when the publisher is trusted and the user is comfortable providing GIGGLE_API_KEY for this skill's video-generation workflow. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/patches429/giggle-generation-drama) <br>
- [Giggle.pro](https://giggle.pro/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, API calls] <br>
**Output Format:** [Markdown guidance with Python examples, shell setup commands, JSON API responses, and signed video download URLs.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3, requests, network access to Giggle.pro, and GIGGLE_API_KEY.] <br>

## Skill Version(s): <br>
0.0.10 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
