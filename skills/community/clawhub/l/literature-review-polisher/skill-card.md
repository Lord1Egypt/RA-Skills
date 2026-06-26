## Description: <br>
Polish and improve literature reviews for students and researchers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jeoyee](https://clawhub.ai/user/jeoyee) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Students and researchers use this skill to analyze literature-review structure, citation density, and critical framing, then produce a polished draft suited to the selected academic level. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Pasted literature-review drafts are sent to Moonshot/Kimi for polishing. <br>
Mitigation: Do not use confidential, unpublished, regulated, or student-identifying material unless that external processing is acceptable. <br>
Risk: The artifact embeds a live-looking Kimi API key. <br>
Mitigation: Treat the key as exposed and replace it with a user-controlled secret such as an environment variable before use. <br>
Risk: Polished output is saved in the current working folder. <br>
Mitigation: Run the skill in an appropriate workspace and review saved files before sharing or relying on them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jeoyee/literature-review-polisher) <br>
- [Moonshot/Kimi API endpoint](https://api.moonshot.cn/v1) <br>


## Skill Output: <br>
**Output Type(s):** [text, guidance, files] <br>
**Output Format:** [Console text and saved plain-text polished output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May call Moonshot/Kimi and write polished output to the current working folder.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence; artifact frontmatter lists 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
