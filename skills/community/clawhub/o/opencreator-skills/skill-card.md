## Description: <br>
Operate and build OpenCreator workflows via API by searching templates, running and polling workflows, delivering generated media, or designing workflow graphs with nodes and edges. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhuozhihaicloud](https://clawhub.ai/user/zhuozhihaicloud) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, creators, and workflow operators use this skill to search and run OpenCreator templates or design workflow graphs for UGC ads, ecommerce image sets, storyboard videos, lipsync, and similar media workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can run or modify production OpenCreator workflows using a user-provided API key. <br>
Mitigation: Use a scoped OpenCreator API key where possible, review template and workflow actions before execution, and monitor runs until terminal status. <br>
Risk: User media may be uploaded to third-party file hosts outside OpenCreator. <br>
Mitigation: Avoid sensitive, regulated, private, or third-party face and voice media unless rights and consent are confirmed; prefer controlled storage with known retention and access policies. <br>
Risk: Generated media workflows can use product, face, voice, or advertising inputs in ways that require consent and review. <br>
Mitigation: Confirm input rights, brand permissions, and usage consent before running workflows or publishing generated media. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/zhuozhihaicloud/opencreator-skills) <br>
- [Publisher profile](https://clawhub.ai/user/zhuozhihaicloud) <br>
- [README](artifact/README.md) <br>
- [Skill definition](artifact/SKILL.md) <br>
- [Operate Mode API workflows](artifact/references/api-workflows.md) <br>
- [Node catalog](artifact/references/node-catalog.md) <br>
- [Operator playbook](artifact/references/operator-playbook.md) <br>
- [Workflow best practices](artifact/references/best-practices.md) <br>
- [UGC lipsync ad scenario](artifact/references/scenarios/scenario-ugc-lipsync-ad.md) <br>
- [Storyboard video scenario](artifact/references/scenarios/scenario-storyboard-video.md) <br>
- [Ecommerce multi-image scenario](artifact/references/scenarios/scenario-ecommerce-multi-image.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with API examples, JSON workflow graphs, shell commands, configuration instructions, and direct media delivery.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May require an OpenCreator API key, production API access, user-provided media inputs, and polling until workflow completion.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
