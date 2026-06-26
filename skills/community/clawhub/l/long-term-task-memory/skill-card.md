## Description: <br>
按需调用火山引擎 Milvus 向量数据库进行长期记忆存储与检索，支持灵活的数据格式区分角色、事件、项目等维度；当用户明确要求保存、查询、更新或删除长期记忆时使用 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zuoanCo](https://clawhub.ai/user/zuoanCo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill when a user explicitly asks to save, search, update, or delete long-term task, event, project, decision, or note memory in a Milvus-backed store. It is suited for workflows that need persistent memory organized by category, role, project, event, status, priority, tags, context, and metadata. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Remote long-term memory storage can retain sensitive personal, business, or secret data beyond the current agent session. <br>
Mitigation: Avoid storing secrets or sensitive data, protect the .env file, and use a dedicated least-privilege Milvus account. <br>
Risk: Delete and --recreate operations can remove stored memory records or collections. <br>
Mitigation: Require clear user confirmation before destructive operations and back up important collections before recreation or deletion. <br>


## Reference(s): <br>
- [Memory data format reference](references/memory-format.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, JSON, Text] <br>
**Output Format:** [Markdown guidance with shell commands and JSON memory records] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Milvus connection configuration through MILVUS_URI and MILVUS_TOKEN.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
