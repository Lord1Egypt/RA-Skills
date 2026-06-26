## Description: <br>
Creates visually structured HTML operation-guide pages for Web UI walkthroughs, feature explanations, and agent import tutorials. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[2239721014-ops](https://clawhub.ai/user/2239721014-ops) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and documentation authors use this skill to generate polished Web UI operation guides with feature cards, screenshot placeholders, step-by-step instructions, code blocks, FAQs, and sharing links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can steer an agent toward publishing generated HTML to a hardcoded GitHub repository, branch, and output path. <br>
Mitigation: Confirm the repository, branch, output path, generated file contents, and final publication intent before any git commit or push. <br>
Risk: Generated guide content may contain incorrect UI descriptions, outdated steps, or misleading screenshot placeholders. <br>
Mitigation: Review the final HTML guide against the target interface and replace placeholders with approved screenshots before sharing. <br>
Risk: Publishing generated files can expose internal workflows, screenshots, or instructions if sensitive content is included. <br>
Mitigation: Screen the generated page for secrets, private URLs, customer data, and internal-only details before upload. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/2239721014-ops/instruction-web) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [HTML guide content with Markdown status notes, shell command snippets, and generated CDN or preview links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create HTML files intended for a configured workplace-doc output directory and may propose GitHub commit and push commands for publication.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
