## Description: <br>
HTTP客户端 - 发送GET/POST/PUT/DELETE请求，自定义请求头/Body，响应验证，超时控制，重试机制 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[534422530](https://clawhub.ai/user/534422530) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to prepare Python-based HTTP client code and guidance for calling REST or GraphQL APIs, including request methods, headers, bodies, timeouts, retries, authentication, and response inspection. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can help send credentials or private request data to external endpoints. <br>
Mitigation: Use it only for intentional requests to trusted endpoints, and avoid placing secrets in headers or bodies unless the destination is trusted. <br>
Risk: Request history may retain sensitive URLs, headers, bodies, or tokens. <br>
Mitigation: Review whether request history redacts tokens or can be disabled or cleared before using the generated client with sensitive data. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/534422530/laosi-http-client) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/534422530) <br>


## Skill Output: <br>
**Output Type(s):** [code, guidance, configuration] <br>
**Output Format:** [Markdown with Python code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include example API requests, authentication headers, retry settings, timeout values, and response-validation guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
