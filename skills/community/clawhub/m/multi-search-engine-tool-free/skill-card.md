## Description: <br>
This skill helps personal users generate and compare search links across major Chinese and international search engines. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and individual users can use this skill to prepare multi-source web searches, compare search providers, and generate encoded search URLs for technical research or quick knowledge lookup. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries can be sent to public search engines and may expose confidential text. <br>
Mitigation: Use only non-sensitive queries; do not include secrets, credentials, private project names, internal logs, or other confidential information unless disclosure to the selected search provider is acceptable. <br>
Risk: Generated or opened links may navigate the agent or browser to external search providers. <br>
Mitigation: Review generated URLs and choose the intended search provider before opening links. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/multi-search-engine-tool-free) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with inline shell/Python snippets and generated search URLs.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Free edition generates search links rather than returning fetched search-result contents.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
