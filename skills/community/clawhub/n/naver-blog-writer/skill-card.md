## Description: <br>
Publish prepared content to Naver Blog from an authenticated local browser on the buyer machine. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[y80163442-boop](https://clawhub.ai/user/y80163442-boop) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and OpenClaw agents use this skill to publish already-prepared posts to Naver Blog through a local macOS runner after setup, dry run, and login checks. It is intended for publishing, not drafting, SEO planning, or topic ideation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Installation delegates persistent local publishing authority to the external @y80163442/naver-thin-runner package, which was not included for review. <br>
Mitigation: Install only if the publisher and runner package are trusted, verify how to stop and uninstall the service, and confirm the daemon is local-only and authenticated before use. <br>
Risk: Live publishing can post content to a real Naver Blog account. <br>
Mitigation: Run doctor/capabilities and publish_dry_run first, complete a final account and content check, and use publish_live only after confirming the prepared title, body, tags, and account. <br>
Risk: Fallback setup can use a broad ACP_ADMIN_API_KEY. <br>
Mitigation: Prefer OPENCLAW_OFFERING_EXECUTE_URL and avoid broad admin API keys where possible. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/y80163442-boop/naver-blog-writer) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, JSON] <br>
**Output Format:** [Markdown instructions with bash command examples and JSON result field names] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Live publishing returns naver_publish_result; dry runs return preview data with a synthetic published_url; readiness checks return doctor/capabilities JSON.] <br>

## Skill Version(s): <br>
0.6.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
