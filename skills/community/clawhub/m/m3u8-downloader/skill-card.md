## Description: <br>
Download encrypted m3u8/HLS videos using parallel downloads. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[EasonC13](https://clawhub.ai/user/EasonC13) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to extract HLS playlist details, download m3u8 video segments in parallel, handle AES-128 encrypted streams, and merge the result into an MP4 file. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Unchecked output names can cause the helper script to write or delete unexpected paths. <br>
Mitigation: Use only simple output names made of letters, numbers, dashes, or underscores, and avoid slashes, '..', and shell metacharacters. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/EasonC13/m3u8-downloader) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Code] <br>
**Output Format:** [Markdown with inline bash and JavaScript code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces download and merge instructions; the helper script saves an MP4 file under ~/Downloads.] <br>

## Skill Version(s): <br>
1.0.0 (source: evidence.release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
