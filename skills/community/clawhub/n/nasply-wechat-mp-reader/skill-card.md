## Description: <br>
Fetches WeChat Official Account articles from a public account name or article URL, returning article content, account metadata, and optional account article lists. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nasplycc](https://clawhub.ai/user/nasplycc) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to extract WeChat Official Account article content, identify the publishing account, search account candidates, manage MP sessions, and produce Markdown or structured JSON for archives or downstream analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can obtain and persist logged-in WeChat MP backend session credentials in local files. <br>
Mitigation: Use public article extraction when possible; only scan the QR code or provide WECHAT_MP_COOKIE and WECHAT_MP_TOKEN in trusted runtimes, prefer a low-risk WeChat MP account, and delete scripts/cache/session.json plus login-state artifacts after use. <br>
Risk: Account search and article-list features depend on valid WeChat MP backend cookies and tokens. <br>
Mitigation: Check session validity before backend operations and fall back to article-URL-based extraction when the session is missing, invalid, or untrusted. <br>
Risk: WeChat pages and backend endpoints are brittle and can return verification or shell pages. <br>
Mitigation: Treat browser fallback and partial-success warnings as normal outcomes, and review extracted Markdown or JSON before downstream use. <br>


## Reference(s): <br>
- [WeChat MP Reader skill page](https://clawhub.ai/nasplycc/nasply-wechat-mp-reader) <br>
- [WeChat MP Reader Design](references/design.md) <br>
- [WeChat MP Reader Usage Guide](references/usage.md) <br>
- [WeChat Official Accounts Platform](https://mp.weixin.qq.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance and JSON objects, with shell commands when invoking the bundled CLI] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write local session, login, and cache files during session workflows; article extraction can include HTML, Markdown, images, account metadata, and warnings.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
