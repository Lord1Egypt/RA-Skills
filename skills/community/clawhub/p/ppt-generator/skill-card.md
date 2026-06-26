## Description: <br>
将用户讲稿一键生成乔布斯风极简科技感竖屏HTML演示稿，输出单个可直接运行的HTML文件。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wwlyzzyorg](https://clawhub.ai/user/wwlyzzyorg) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Presenters, educators, and content creators use this skill to convert a talk script into a minimalist, technology-styled vertical HTML slide deck. It is especially suited to Chinese-language scripts and Steve Jobs-style presentation requests. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated presentations may load TailwindCSS and fonts from third-party CDNs when opened. <br>
Mitigation: Review generated HTML before sharing or opening in restricted environments, and replace CDN links with approved local or internal assets when offline or confidentiality requirements apply. <br>
Risk: Broad activation wording may trigger the skill for many slide or presentation requests. <br>
Mitigation: Confirm that the requested output is a minimalist vertical HTML deck before using the generated result. <br>
Risk: Default behavior favors Chinese copy and a Steve Jobs-style minimalist technology aesthetic. <br>
Mitigation: Specify a different language, aspect ratio, or visual style when the intended deck should not follow those defaults. <br>


## Reference(s): <br>
- [Design Specification](references/design-spec.md) <br>
- [Slide Types](references/slide-types.md) <br>
- [HTML Template](assets/template.html) <br>
- [ClawHub Skill Page](https://clawhub.ai/wwlyzzyorg/ppt-generator) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code] <br>
**Output Format:** [Markdown sections followed by complete standalone HTML code] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs a refined script, slide structure outline, and a single runnable 9:16 HTML presentation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
