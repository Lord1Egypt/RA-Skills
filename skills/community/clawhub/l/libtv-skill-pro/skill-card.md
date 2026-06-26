## Description: <br>
LibTV Skill Pro helps agents generate, edit, monitor, download, and export AI images and videos through LibTV, with dry-run previews, model routing, batch jobs, workflow templates, project/session utilities, and structured errors. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qiuxiangxiang](https://clawhub.ai/user/qiuxiangxiang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and creative operators use this skill to route prompts and media to LibTV for image/video generation, edits, batch production, monitoring, downloads, and export reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires LIBTV_ACCESS_KEY and sends prompts, reference URLs, and uploaded media to LibTV. <br>
Mitigation: Use a revocable API key, keep it out of logs, and install only when LibTV is trusted for the content being submitted. <br>
Risk: OPENAPI_IM_BASE or IM_BASE_URL can change the API endpoint used by the scripts. <br>
Mitigation: Leave these variables unset for normal use, or verify they point to a trusted endpoint before running commands. <br>
Risk: Paid generation commands can consume LibTV credits. <br>
Mitigation: Run dry-run previews before paid generation and confirm the prompt, model, ratio, resolution, duration, and batch size. <br>
Risk: Optional HTML exports can render untrusted session content unsafely in a browser. <br>
Mitigation: Avoid opening HTML exports from untrusted sessions until the escaping issue is fixed; prefer JSON, Markdown, or URL-only exports when reviewing untrusted content. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/qiuxiangxiang/libtv-skill-pro) <br>
- [Publisher Profile](https://clawhub.ai/user/qiuxiangxiang) <br>
- [LibTV Platform](https://www.liblib.tv) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, JSON, files] <br>
**Output Format:** [JSON responses, shell command guidance, Markdown or HTML exports, URLs, and downloaded media files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generation commands may create remote LibTV sessions, project URLs, media URLs, local project/session history files, and downloaded image or video assets.] <br>

## Skill Version(s): <br>
0.4.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
