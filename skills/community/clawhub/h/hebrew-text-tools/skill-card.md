## Description: <br>
Hebrew text processing utilities for transliteration, gematria calculation, nikud removal, letter identification, and Hebrew number formatting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[abeperl](https://clawhub.ai/user/abeperl) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to process Hebrew text offline, including transliteration, gematria calculation, vowel-point removal, letter-name listing, right-to-left reversal, and Hebrew number formatting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Transliteration is Ashkenazi-style and may not match Sephardi, Israeli, academic, or community-specific expectations. <br>
Mitigation: Review transliteration output before using it in user-facing, educational, liturgical, or archival material. <br>
Risk: Hebrew number formatting is limited to values from 1 to 999. <br>
Mitigation: Use a specialized formatter or manual review for numbers outside the documented range. <br>
Risk: Right-to-left reversal is basic and may produce incorrect ordering for mixed Hebrew and non-Hebrew text. <br>
Mitigation: Manually inspect mixed-direction text output and use a Unicode-aware bidi library for production text layout. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/abeperl/hebrew-text-tools) <br>
- [Publisher Profile](https://clawhub.ai/user/abeperl) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Plain text, JSON, Markdown, and Python or shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces offline Hebrew text-processing results; CLI output can be plain text or JSON.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
