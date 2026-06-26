## Description: <br>
ht-skills lets an OpenClaw agent manage 灏天文库 personal garden collections, documents, hierarchy, image uploads, image groups, usage quotas, promotion requests, and document-fragment retrieval. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[1044197988](https://clawhub.ai/user/1044197988) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to let an OpenClaw agent create, update, move, retrieve, and organize content in their 灏天文库 personal garden, including document assets and uploaded images. It can also retrieve relevant document fragments from public collection indexes so the agent can answer or draft with cited source snippets. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses an account token that can authorize access to personal garden content and image assets. <br>
Mitigation: Store the token in HT_SKILL_TOKEN or a protected secret store, avoid committing config.json, and rotate the token if exposure is suspected. <br>
Risk: Write, move, upload, and promotion-request actions can change user content or consume account quota. <br>
Mitigation: Review the intended command, target collection or document ID, and quota status before running write or upload operations. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/1044197988/ht-skills) <br>
- [灏天文库 website](https://www.aiknowledge.cn) <br>
- [灏天文库 public collection catalog](https://aiknowledge.cn/article/66521-%E7%81%8F%E5%A4%A9%E6%96%87%E5%BA%93%E6%96%87%E9%9B%86%E5%AE%8C%E6%95%B4%E7%9B%AE%E5%BD%95%E5%85%AC%E5%BC%80) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON API responses from helper scripts.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a 灏天文库 API token supplied through HT_SKILL_TOKEN or config.json.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
