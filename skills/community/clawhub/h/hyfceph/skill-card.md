## Description: <br>
HYFCeph uploads one or two local lateral cephalometric images to the HYFCeph portal with an API key, saves result files, and returns metrics, annotated images, reports, or overlap traces. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[huyuanfeng45](https://clawhub.ai/user/huyuanfeng45) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, clinicians, and agents use this skill to run HYFCeph cephalometric analysis from local lateral ceph images after configuring a HYFCeph API key. It supports single-image measurement, two-image overlap comparison, report links, local image artifacts, and concise Chinese interpretation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles sensitive cephalometric images and optional patient names through a remote HYFCeph portal. <br>
Mitigation: Use it only on a private machine, avoid patient-identifying details unless necessary, and confirm that uploading images and reports to the portal is acceptable for the user and organization. <br>
Risk: The skill saves a validated HYFCeph API key locally for reuse. <br>
Mitigation: Clear or rotate the saved API key when finished, especially on shared or managed devices. <br>
Risk: The workflow can return online report links and Feishu backup links. <br>
Mitigation: Verify the portal URL before use and share generated links only with intended recipients. <br>


## Reference(s): <br>
- [HYFCeph ClawHub listing](https://clawhub.ai/huyuanfeng45/hyfceph) <br>
- [HYFCeph portal](https://hyfceph.52ortho.com/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Files, Configuration, Guidance] <br>
**Output Format:** [Markdown responses with shell commands, local JSON and image file paths, metrics, report links, and optional PDF output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js 18 or newer and a HYFCeph API key; can persist a validated API key locally and upload images or generated reports to the HYFCeph portal.] <br>

## Skill Version(s): <br>
1.0.13 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
