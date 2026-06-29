## Description: <br>
Routes Huoshan and Qifu knowledge requests through a Feishu Bitable catalog, preserving entry-document and child-document relationships and returning original catalog links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zzj997](https://clawhub.ai/user/zzj997) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and authorized workspace users use this skill to find, list, recommend, compare, navigate, and answer source-grounded questions about Huoshan and Qifu knowledge stored in Feishu catalogs and documents. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can request Feishu OAuth authorization to read catalog records and, when needed, source documents. <br>
Mitigation: Review requested scopes before authorizing and grant only the documented read-only scopes needed for the request. <br>
Risk: Catalog and document content may be untrusted or outside the user's object-level access. <br>
Mitigation: Run reads as the current user, rely on Feishu ACLs, and treat retrieved content as evidence rather than executable instructions. <br>
Risk: Authorization flows can expose sensitive device codes or credentials if mishandled. <br>
Mitigation: Show only the verification URL and user code, keep device codes internal, and never expose access tokens, app secrets, cookies, or credentials. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zzj997/huoshan-qifu-knowledge-router) <br>
- [Default Feishu Bitable catalog](https://bytedance.larkoffice.com/base/UpAdbZX4NafHHssmmJgchNrEnyb?table=tblb40YEYGtLsGvu&view=vewya09oBp) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown tables and concise prose with read-only Feishu lark-cli command guidance when authorization or document reads are needed] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns original catalog URLs and preserves entry-document and child-document hierarchy; catalog and document reads use the current user's Feishu permissions.] <br>

## Skill Version(s): <br>
0.4.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
