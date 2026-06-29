## Description: <br>
进击的知识库 helps agents archive WeChat, Douyin, Xiaohongshu, public-account articles, and local files by downloading or parsing content, uploading it to Tencent Docs, and recording it in an index sheet. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hitjcl](https://clawhub.ai/user/hitjcl) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to turn social media links, public-account articles, and supported local files into organized Tencent Docs knowledge-base entries. It is intended for content collection, upload, and indexing workflows that require the user to configure their own Tencent Docs space and index sheet. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill downloads content, may use platform cookies, sends some links to external services, uploads files to Tencent Docs, and writes persistent index records. <br>
Mitigation: Start with non-sensitive content, avoid personal session cookies unless necessary, and verify the configured Tencent Docs space, file ID, and sheet ID before use. <br>
Risk: The security scan flagged under-disclosed data flow and command-execution risks around shell execution, upload destinations, and external services. <br>
Mitigation: Review or patch shell execution paths and upload destination validation before trusting the skill with private or business data. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hitjcl/knowledge-base) <br>
- [Tencent Docs](https://docs.qq.com) <br>
- [Python](https://python.org) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, files] <br>
**Output Format:** [Markdown guidance, shell command examples, JSON helper-script results, and generated local files such as downloaded media or caption text.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May upload content to Tencent Docs and append records to a configured Tencent Docs index sheet.] <br>

## Skill Version(s): <br>
2.4.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
