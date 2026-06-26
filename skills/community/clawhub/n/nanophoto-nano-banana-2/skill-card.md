## Description: <br>
Generate or edit images with the NanoPhoto.AI Nano Banana 2 API, including text-to-image, public-URL image editing, status checks, optional Google Search prompt enhancement, and polling through the bundled script. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nanophotohq](https://clawhub.ai/user/nanophotohq) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to generate images from prompts, edit public image URLs, and check NanoPhoto generation status from an agent workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and public image URLs are sent to the NanoPhoto service. <br>
Mitigation: Submit only prompts and public image URLs you are authorized to share with NanoPhoto; avoid private or sensitive images. <br>
Risk: The NanoPhoto API key can spend account credits. <br>
Mitigation: Store NANOPHOTO_API_KEY in the platform secure environment setting and use accounts or keys with appropriate credit controls. <br>


## Reference(s): <br>
- [Nano Banana 2 API Reference](references/api.md) <br>
- [NanoPhoto homepage](https://nanophoto.ai) <br>
- [ClawHub skill page](https://clawhub.ai/nanophotohq/nanophoto-nano-banana-2) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, JSON, Guidance] <br>
**Output Format:** [Markdown with inline bash commands and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns generation IDs, image URLs, and progress details when available; requires NANOPHOTO_API_KEY.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
