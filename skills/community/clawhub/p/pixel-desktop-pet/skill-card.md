## Description: <br>
Deploys a pixel-art desktop pet with floating and home-garden modes, four explorable scenes, care mechanics, walk animations, and Python 3.11+ Tkinter/Pillow requirements. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[whitezhiiii](https://clawhub.ai/user/whitezhiiii) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to install and run a Python/Tkinter desktop pet with a mini floating character, a home-garden mode, care interactions, customization, and optional chat. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security review flags unexpected online data flows, including remote asset downloads, background network requests, and optional third-party AI chat. <br>
Mitigation: Review the script before running it, allow only expected network endpoints, and use the AI chat feature only when comfortable sending chat and pet context to the configured service. <br>
Risk: The desktop app may read nearby IDENTITY.md and USER.md files and stores pet state in ~/.nbw_pet_save.json. <br>
Mitigation: Run it from a dedicated directory without sensitive profile files nearby, and review or remove the local save file when no longer needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/whitezhiiii/pixel-desktop-pet) <br>
- [Cozy People sprite credits](https://pixelfight.itch.io/) <br>
- [CraftPix background credits](https://craftpix.net/freebies/) <br>
- [Remote asset download location](https://raw.githubusercontent.com/whitezhiiii/desktop-pet/main/assets/) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash commands and file placement guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides copying the desktop_pet.py script and assets, installing Pillow, and running a Tkinter desktop app.] <br>

## Skill Version(s): <br>
11.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
