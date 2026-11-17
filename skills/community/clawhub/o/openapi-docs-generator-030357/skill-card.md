## Description:

Helps backend and platform teams generate, improve, and validate OpenAPI or Swagger documentation for REST APIs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kyro-ma](https://clawhub.ai/user/kyro-ma)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to turn REST API context into practical OpenAPI or Swagger documentation, review checklists, implementation guidance, and validation steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may activate on broad API or documentation phrasing.

Mitigation: Prefer explicit invocation when users specifically want OpenAPI or Swagger documentation help.

Risk: Generated API documentation guidance can become inaccurate if the agent lacks the service routes, schemas, authentication model, or validation output.

Mitigation: Review generated documentation against the source service and run an OpenAPI or Swagger validator before publishing.

## Reference(s):

- [Requirement Plan](artifact/references/requirement-plan.md)
- [Runtime integration closure after W8](https://github.com/kudzimusar/direkt/issues/261)
- [OpenAPI specification RESTful API design](https://blog.csdn.net/2501_94476825/article/details/159013081?ops_request_misc=elastic_search_misc&request_id=cd31bca05b8e4073b3f63ab89a617b4a&biz_id=0&utm_medium=distribute.pc_search_result.none-task-blog-2~all~sobaiduend~default-4-159013081-null-null.142^v102^pc_search_result_base7&utm_term=OpenAPI%20%E6%96%87%E6%A1%A3)
- [Swagger/OpenAPI documentation generation for Wiki.js APIs](https://blog.csdn.net/gitblog_01093/article/details/151205413?ops_request_misc=elastic_search_misc&request_id=cd31bca05b8e4073b3f63ab89a617b4a&biz_id=0&utm_medium=distribute.pc_search_result.none-task-blog-2~all~baidu_landing_v2~default-5-151205413-null-null.142^v102^pc_search_result_base7&utm_term=OpenAPI%20%E6%96%87%E6%A1%A3)
- [Swagger bearer token question](https://segmentfault.com/q/1010000017381307/a-1020000017382712)
- [OpenAPI interface specification article](https://segmentfault.com/a/1190000043968971)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown, code snippets, command examples, checklists, and implementation notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include validation steps and follow-up risks for API documentation work.]

## Skill Version(s):

0.20260729.110214 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
