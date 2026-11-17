## Description:

Guides agents to apply a Pipeline Architecture pattern for business workflow reads, writes, authorization checks, transactions, audit logging, and external side effects in existing Python/FastAPI, TypeScript/Node.js, Payload CMS, Cloudflare Workers, and claimed Flutter/Dart projects.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jivecheng](https://clawhub.ai/user/jivecheng)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering agents use this skill when modifying projects that already follow the Pipeline Architecture pattern and need structured business workflows for APIs, writes, authorization, multi-step processing, transactions, audit logs, or cross-system side effects. It helps select the correct language or platform reference before proposing code, with supplements for Payload CMS and Cloudflare Workers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill provides high-impact workflow guidance for writes, transactions, authorization checks, and external side effects.

Mitigation: Review generated implementation plans before execution and require tests around authorization, transaction boundaries, audit logs, and external side-effect handling.

Risk: Payload CMS usage can bypass pipeline authorization if access rules and required authorization Steps are incomplete.

Mitigation: For business collections, confirm the custom endpoint path is enforced, collection access is configured intentionally, and authorization Steps are present and tested.

Risk: The release claims Flutter support, but the artifact does not include references/flutter.md.

Mitigation: Do not rely on the claimed Flutter support until the missing Flutter reference is supplied and reviewed.

## Reference(s):

- [Pipeline Architecture Skill](https://clawhub.ai/jivecheng/skills/pipeline-architecture)
- [Cloudflare Workers Reference](references/cloudflare-workers.md)
- [Payload CMS Reference](references/payload-cms.md)
- [Python/FastAPI Reference](references/python.md)
- [TypeScript/Node.js Reference](references/typescript.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, configuration, shell commands]

**Output Format:** [Markdown guidance with code and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only architecture guidance; no direct API calls or tool execution are defined by the skill.]

## Skill Version(s):

1.0.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
