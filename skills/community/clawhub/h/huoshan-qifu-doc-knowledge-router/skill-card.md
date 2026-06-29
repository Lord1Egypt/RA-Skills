## Description: <br>
Routes Huoshan and Qifu knowledge requests through the default structured Feishu document INDEX and returns relevant original Feishu links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zzj997](https://clawhub.ai/user/zzj997) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and internal knowledge workers use this skill to find, recommend, or verify Huoshan/Qifu Feishu learning documents from a structured INDEX while preserving original Feishu document links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may activate for broad source-grounded-answer requests beyond the intended Huoshan/Qifu document-routing use case. <br>
Mitigation: Use it only when the user explicitly requests Huoshan/Qifu knowledge routing or Feishu document recommendations, and keep the trigger wording narrow during review. <br>
Risk: The agent may request read-only Feishu Wiki and Docx scopes and use the current user's document access. <br>
Mitigation: Install only for users who expect Feishu reads, approve only the minimal read-only scopes, and rely on existing document ACLs for access control. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/zzj997/huoshan-qifu-doc-knowledge-router) <br>
- [Default Feishu Wiki INDEX](https://bytedance.larkoffice.com/wiki/UOzdwymi8ibRgBko04bcX1yRnNh) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with Feishu document links and concise status notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Preserves directory-provided detail URLs and marks whether recommendations are based on directory metadata or source text.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
