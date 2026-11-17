## Description:

Guides agents to check an open-source project's issue tracker and latest release before creating custom workarounds for bugs or unexpected behavior.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lbwdada](https://clawhub.ai/user/lbwdada)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill when debugging open-source dependencies to search upstream issues and pull requests, compare the installed version with available fixes, and decide whether to upgrade before attempting local workarounds.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Public issue tracker searches can expose sensitive error messages, stack traces, or project context.

Mitigation: Redact secrets, private stack traces, and proprietary details before searching external sites.

Risk: The skill includes an example curl command for querying GitHub that could be copied into a shell without review.

Mitigation: Prefer a built-in web-search tool or structured HTTP parameters, and review any shell command before execution.

Risk: Issue or pull request results can be outdated or only partially applicable to the user's installed version.

Mitigation: Confirm fix status, release version, and upgrade feasibility before recommending changes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lbwdada/skills/oss-issue-first)
- [RAGFlow fix example](https://github.com/infiniflow/ragflow/pull/16525)
- [RAGFlow repository](https://github.com/infiniflow/ragflow)
- [Spring AI repository](https://github.com/spring-projects/spring-ai)
- [RuoYi-Vue repository](https://gitee.com/y_project/RuoYi-Vue)
- [Vue 2 repository](https://github.com/vuejs/vue)
- [Vue 3 core repository](https://github.com/vuejs/core)
- [Element Plus repository](https://github.com/element-plus/element-plus)
- [Element Plus X repository](https://github.com/element-plus-x/Element-Plus-X)
- [MyBatis repository](https://github.com/mybatis/mybatis-3)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands]

**Output Format:** [Markdown guidance with issue and pull request links, version recommendations, and optional shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include public issue tracker searches and upstream links; redact sensitive error details before searching.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
