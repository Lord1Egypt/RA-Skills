## Description: <br>
Uses a Playwright persistent browser context to scrape login-required sites including YouTube, GitHub, Hugging Face, Reddit, Kaggle, and X/Twitter, and triggers when users request external web search or specify those sites. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ckncg](https://clawhub.ai/user/ckncg) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to gather plain-text content from authenticated or JavaScript-heavy websites through a persistent Playwright browser profile. It is intended for workflows where the operator has authorized access to the target site and needs text extraction rather than screenshots. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reuses a persistent authenticated browser profile and may access logged-in content automatically. <br>
Mitigation: Use a dedicated low-privilege browser profile, confirm each authenticated site before use, and avoid private messages, settings, billing pages, or profiles active in another browser session. <br>
Risk: Broad automatic triggers for external search and popular sites can scrape more authenticated content than intended. <br>
Mitigation: Limit invocation to explicitly approved domains and review the target URL and selector before running the browser workflow. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ckncg/persistent-browser) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with Python and shell command examples plus extracted plain text guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a persistent authenticated browser profile and site-specific wait times before returning page text.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
