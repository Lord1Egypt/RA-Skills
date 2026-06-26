## Description: <br>
Luma AI video-generation assistant for Dream Machine text-to-video, image-to-video, keyframe animation, prompt design, and API usage guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhangifonly](https://clawhub.ai/user/zhangifonly) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Creators, developers, and video-production teams use this skill to draft Luma Dream Machine prompts, compare video-generation options, and adapt example Luma API calls for text-to-video, image-to-video, and keyframe workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Example API usage sends prompts, media references, and an API token to Luma as an external service. <br>
Mitigation: Use environment variables or a secrets manager for API keys, and avoid submitting sensitive prompts or media unless Luma's data handling terms are acceptable. <br>
Risk: Generated prompt and API guidance may be copied into production workflows without review. <br>
Mitigation: Review suggested prompts and code snippets before execution, especially where they handle credentials, user media, or external API requests. <br>


## Reference(s): <br>
- [Luma AI skill page](https://clawhub.ai/zhangifonly/luma-ai) <br>
- [Luma Dream Machine generations API endpoint](https://api.lumalabs.ai/dream-machine/v1/generations) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, API Calls] <br>
**Output Format:** [Markdown with prompt examples, comparison tables, and Python API snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include prompts or example API requests that should be reviewed before use with real media, sensitive content, or credentials.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
