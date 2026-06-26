## Description: <br>
Optimizes web fetching by using Cloudflare's Markdown for Agents, reducing token consumption by ~80%. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[howtimeschange](https://clawhub.ai/user/howtimeschange) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to request Markdown responses during web fetches when available, falling back to HTML while preserving response metadata. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The helper can fetch arbitrary URLs supplied by an agent or caller. <br>
Mitigation: Use it only for URLs the caller intends the agent to access, and keep normal URL allow-listing or review controls in place. <br>
Risk: Fetched content, response headers, and token-savings URL logs may be visible to the caller or console. <br>
Mitigation: Avoid using the helper on sensitive pages unless that visibility is acceptable, and disable or review token-savings logging in sensitive workflows. <br>
Risk: HTML fallback uses simple tag stripping and may produce incomplete or misleading extracted text. <br>
Mitigation: Treat fallback extraction as a convenience path and review important fetched content before relying on it. <br>


## Reference(s): <br>
- [Markdown Fetch on ClawHub](https://clawhub.ai/howtimeschange/markdown-fetch) <br>
- [Publisher profile: howtimeschange](https://clawhub.ai/user/howtimeschange) <br>


## Skill Output: <br>
**Output Type(s):** [code, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JavaScript examples and helper functions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Fetch results may include Markdown or HTML content, status metadata, response headers, and optional token-savings values.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
