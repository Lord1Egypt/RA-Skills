## Description: <br>
Lazarus helps an agent recover Google-indexed content from defunct websites using the Wayback Machine, clean it into Markdown, and guide deployment after user review. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[adsorgcn](https://clawhub.ai/user/adsorgcn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, site maintainers, and content recovery operators use this skill to scout defunct domains, recover archived pages that show Google indexing signals, review recovered material, and prepare static-site deployment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Recovered pages may include copyrighted material, trademarks, or assets that the user does not have rights to reuse. <br>
Mitigation: Confirm reuse rights before publication and remove, replace, or rewrite material that cannot be cleared. <br>
Risk: Recovered pages may contain personal data, credentials, internal URLs, account endpoints, or other sensitive material. <br>
Mitigation: Review all generated files before deployment and redact or remove sensitive findings before publishing. <br>
Risk: The skill may create recovered content files from external archive sources. <br>
Mitigation: Require explicit user confirmation for the output path, file count, and estimated disk use before writing files. <br>


## Reference(s): <br>
- [Lazarus on ClawHub](https://clawhub.ai/adsorgcn/lazarus) <br>
- [Publisher profile](https://clawhub.ai/user/adsorgcn) <br>
- [iLang homepage](https://ilang.ai) <br>
- [AutoCode](https://github.com/ilang-ai/autocode) <br>
- [Internet Archive account signup](https://archive.org/account/signup) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Conversational guidance with Markdown file content, directory plans, metadata tables, and deployment instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Asks for confirmation before writing files and organizes recovered pages by index status when recovery proceeds.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
