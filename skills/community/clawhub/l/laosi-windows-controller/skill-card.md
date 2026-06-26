## Description: <br>
Windows应用控制器让AI通过Python自动化技术控制Windows桌面应用，包括启动和关闭应用、点击按钮、填写表单、截图和窗口操作。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[534422530](https://clawhub.ai/user/534422530) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, testers, and automation users can use this skill to guide Windows GUI automation scripts for app control, data entry, screenshots, form submission, and desktop workflow testing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide broad Windows desktop automation, including clicks, typing, screenshots, file saves, app launches, and force-closing processes. <br>
Mitigation: Use it only when desktop control is intended, preferably in a VM or test account, and require explicit confirmation before sensitive actions such as screenshots, clipboard use, form submission, file creation or overwrite, app launch, or force-closing processes. <br>
Risk: Automation against live desktop applications can act on the wrong window, button, or account if screen state changes or image matching is inaccurate. <br>
Mitigation: Keep sensitive windows closed, verify the active target application before execution, prefer image-based checks over fixed coordinates, and review screenshots or logs after each run. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/534422530/laosi-windows-controller) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with Python and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Windows automation reports with operation status, execution steps, errors, and screenshot references.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
