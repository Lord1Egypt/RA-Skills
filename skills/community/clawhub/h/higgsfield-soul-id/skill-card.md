## Description: <br>
Train a Soul Character, a personalized model on a person's face that Higgsfield uses for identity-faithful image and video generation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[higgsfield](https://clawhub.ai/user/higgsfield) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and creators use this skill to train a reusable Higgsfield Soul identity model from face photos, then use the returned Soul reference with Higgsfield image or cinematic generation tools. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can install a remote Higgsfield CLI before training begins. <br>
Mitigation: Verify the Higgsfield CLI and installer through a trusted source before running the embedded install command. <br>
Risk: The skill uploads face photos to create a reusable identity model. <br>
Mitigation: Only upload photos of yourself or someone who has explicitly consented, and review Higgsfield retention and deletion options for trained Soul models. <br>
Risk: Soul training may affect the user's Higgsfield account or paid plan. <br>
Mitigation: Confirm the intended Higgsfield account and paid-plan requirements before submitting training. <br>


## Reference(s): <br>
- [Photo Guide](references/photo-guide.md) <br>
- [Soul Troubleshooting](references/troubleshooting.md) <br>
- [Higgsfield CLI installer](https://raw.githubusercontent.com/higgsfield-ai/cli/main/install.sh) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks and concise status guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May install or invoke the Higgsfield CLI, upload local face photos, poll training, and return a Soul reference for later generation.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
