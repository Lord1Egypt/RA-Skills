## Description: <br>
Command-style Baidu Netdisk file management with quick command templates, categorized views, path checks, and confirmation rules. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent operators use this skill to manage Baidu Netdisk files through bdpan commands for browsing, upload, download, transfer, sharing, search, move, copy, rename, folder creation, and deletion workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Unrelated SEO trigger text could cause the skill to activate outside Baidu Netdisk file-management tasks. <br>
Mitigation: Remove or ignore the SEO trigger text and only invoke the skill for explicit Baidu Netdisk operations. <br>
Risk: The skill can run shell commands that modify, delete, overwrite, or publicly share cloud files. <br>
Mitigation: Require explicit confirmation for deletes, overwrites, public sharing, and ambiguous file references before executing commands. <br>
Risk: Share links, extraction codes, OAuth session data, and bdpan configuration may contain sensitive information. <br>
Mitigation: Treat these values as sensitive and do not read, print, or expose bdpan configuration or tokens. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/pan-file-commander-free) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with inline bash command examples and concise execution guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include file operation summaries, confirmation prompts, share links, extraction codes, and command results.] <br>

## Skill Version(s): <br>
1.0.0 (source: server evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
