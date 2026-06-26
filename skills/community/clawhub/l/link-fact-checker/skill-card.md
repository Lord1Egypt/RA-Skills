## Description: <br>
Checks whether provided URLs are accessible and helps verify online information by comparing it against multiple sources. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wumingyu1688-sudo](https://clawhub.ai/user/wumingyu1688-sudo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to check link availability and produce concise verification summaries for online content. It is most useful for public URLs and factual claims that can be compared against cited sources. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Checking private, internal, localhost, cloud-metadata, or sensitive document links may expose information or create unintended network access. <br>
Mitigation: Use only public URLs and avoid submitting private, internal, localhost, cloud-metadata, or sensitive document links. <br>
Risk: The artifact reports fact checks as pending and the security summary notes that fact-checking is incomplete. <br>
Mitigation: Treat factual conclusions as advisory unless the agent provides independent cited source comparisons. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wumingyu1688-sudo/link-fact-checker) <br>
- [Publisher profile](https://clawhub.ai/user/wumingyu1688-sudo) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown-style verification summary or JSON-like run result] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes URL status information when a URL is provided; fact checking may require independent cited source comparison.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
