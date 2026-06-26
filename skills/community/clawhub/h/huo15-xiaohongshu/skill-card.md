## Description: <br>
Huo15 Xiaohongshu helps users draft, analyze, coach, and refine Xiaohongshu content, including topic research, viral-note reverse engineering, compliance checks, publishing checklists, and weekly reviews. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhaobod1](https://clawhub.ai/user/zhaobod1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content creators, brand operators, and social-media teams use this skill to plan, draft, critique, revise, and review Xiaohongshu posts. It also supports read-only research workflows for public Xiaohongshu content and personal performance review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill includes logged-in Xiaohongshu scraping and anti-detection browser automation that may create platform-terms or account-risk concerns. <br>
Mitigation: Use the browser_bridge, scrape, safety_check, track_post, and A/B compare features only on accounts where the user understands and accepts those risks; prefer read-only workflows and review the skill's quota and health checks before use. <br>
Risk: The skill can use Xiaohongshu cookies or a logged-in Chrome profile. <br>
Mitigation: Install only if comfortable granting access to that session data, and avoid sharing cookies or profiles across accounts. <br>
Risk: If Anthropic LLM support is enabled, draft and brand content may be sent to that provider. <br>
Mitigation: Use the LLM features only for content that may be shared with the configured provider, and review generated rewrites manually before publishing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zhaobod1/huo15-xiaohongshu) <br>
- [Xiaohongshu](https://www.xiaohongshu.com) <br>
- [README](README.md) <br>
- [Version history](docs/changelog.md) <br>
- [Allen copywriting method](data/allen_method.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and plain text with optional JSON files and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local draft, profile, snapshot, and review files under the user's Xiaohongshu workspace.] <br>

## Skill Version(s): <br>
3.10.0 (source: server release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
