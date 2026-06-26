## Description: <br>
Scans local image folders, reports supported image formats and file metadata, and groups results by filename-based style categories. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mrxolin](https://clawhub.ai/user/mrxolin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, creators, and photo-library maintainers can use this skill to scan an explicit local photo directory and produce a quick report of image files, formats, sizes, timestamps, and filename-based categories before deciding how to organize files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Scanning broad or sensitive folders can expose filenames, paths, sizes, and timestamps in reports. <br>
Mitigation: Run the skill only on an explicit photo directory and review any report before sharing it. <br>
Risk: Style and color classifications may be incomplete or inaccurate. <br>
Mitigation: Treat classifications as a starting point and verify important results before relying on them for organization. <br>
Risk: Automatic file organization claims may be misunderstood as fully implemented file-moving behavior. <br>
Mitigation: Review the generated report first and confirm any future file-moving workflow before allowing it to modify files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mrxolin/image-scanner) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Markdown or plain text with optional shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports local file metadata and filename-based classifications; color analysis and file moving should be treated as limited unless separately verified.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
