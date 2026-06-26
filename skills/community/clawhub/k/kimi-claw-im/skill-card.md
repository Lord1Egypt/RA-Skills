## Description: <br>
Guides agents through Kimi Group Chat and Session workflows, including reading group rules, checking members and recent messages, handling files, and replying in the correct chat context. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dbottrader](https://clawhub.ai/user/dbottrader) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill when participating in Kimi group chats or sessions to inspect room context, coordinate with the right participants, manage workspace-scoped memory and files, and send concise replies through kimiim-cli. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads group rules, member lists, recent messages, and relevant files before replying. <br>
Mitigation: Install it only for agents expected to work in Kimi group or thread contexts, and keep access limited to the intended workspace. <br>
Risk: The skill may create or update group memory and task files under the local .openclaw workspace directory. <br>
Mitigation: Review workspace-scoped memory and produced files before sharing, retaining, or using them in a broader context. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/dbottrader/kimi-claw-im) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance is oriented toward chat-context reads, workspace-scoped memory and file handling, and send-message based replies.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
