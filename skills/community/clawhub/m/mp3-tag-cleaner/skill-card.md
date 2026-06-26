## Description: <br>
Batch remove promotional metadata from MP3 ID3v1 and ID3v2 tags while preserving audio data and file integrity. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[haiyangzhang888](https://clawhub.ai/user/haiyangzhang888) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
People maintaining MP3 libraries use this skill to remove promotional or unwanted ID3 metadata from batches of audio files. It helps prepare cleaner file collections while keeping the audio payload playable. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Bulk processing permanently removes MP3 tags, including ID3v1, ID3v2 text frames, comments, and cover art. <br>
Mitigation: Use the skill only on backed-up MP3s, inspect the generated file list before execution, and test on a small sample before processing a full library. <br>
Risk: The cleanup workflow uses a temporary folder at C:\Temp\MP3Work_ID3 and may delete that folder during execution. <br>
Mitigation: Confirm that C:\Temp\MP3Work_ID3 contains no important files before running the cleaner. <br>
Risk: A precompiled executable may not be independently verified against the reviewed source. <br>
Mitigation: Compile the executable from the reviewed C# source or verify the executable before trusting it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/haiyangzhang888/mp3-tag-cleaner) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, code] <br>
**Output Format:** [Markdown with inline Windows command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill guides an agent to prepare an MP3 file list, run a tag-cleaning executable or reviewed C# source, and verify results.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
