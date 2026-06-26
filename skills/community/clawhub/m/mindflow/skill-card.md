## Description: <br>
Converts text, Markdown files, or TXT files into image-based mind maps with configurable output format and resolution. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[NewToolAI](https://clawhub.ai/user/NewToolAI) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and content creators use Mindflow to turn text, notes, Markdown, or TXT files into image-based mind maps for summarization, planning, and study workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Installing JavaScript dependencies and running Puppeteer introduces normal local runtime and browser-rendering exposure. <br>
Mitigation: Install dependencies from trusted registries, keep them updated, and run rendering in a constrained local environment. <br>
Risk: Rendering arbitrary untrusted HTML can expose the local environment to unsafe content or unwanted network activity. <br>
Mitigation: Use intended text, Markdown, or TXT inputs; sanitize untrusted HTML or block network access before rendering. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/NewToolAI/mindflow) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown workflow guidance with generated PNG or JPEG image files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated mind map Markdown is limited to 300 tokens and up to 4 hierarchy levels; the renderer supports PNG, JPEG, and JPG outputs.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
