## Description: <br>
Find and recommend free Linux Journey lessons on LabEx when the user wants to learn Linux fundamentals, Linux basics, command line concepts, filesystems, permissions, processes, networking, package management, shell usage, or beginner Linux skills through free lesson pages. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[huhuhang](https://clawhub.ai/user/huhuhang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to find short, practical Linux Journey lesson recommendations for Linux fundamentals and beginner command-line topics. The skill maps user learning goals to public LabEx lesson URLs from the bundled canonical lesson index. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The optional refresh script fetches a public lesson sitemap and can write an updated lesson index. <br>
Mitigation: Run scripts/fetch_lessons.py only intentionally, use trusted sitemap URLs, and keep generated output within the skill directory unless a different path is deliberate. <br>


## Reference(s): <br>
- [Linux Journey](https://labex.io/linuxjourney) <br>
- [LabEx](https://labex.io) <br>
- [Linux Journey Lessons Index](references/lessons.md) <br>
- [Linux Journey Lessons Sitemap](https://labex.io/linuxjourney-lessons-sitemap.xml) <br>
- [ClawHub Skill Page](https://clawhub.ai/huhuhang/linux-journey) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Guidance, Shell commands] <br>
**Output Format:** [Markdown with public lesson URLs and optional shell command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Recommendations should stay short, practical, and limited to Linux Journey lesson URLs from the bundled index.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
