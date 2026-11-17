## Description:

Analyzes Go/Weiqi board photos or 19x19 text boards with local KataGo and recommends the next move at beginner, intermediate, advanced, or all strength levels.

This skill is ready for commercial/non-commercial use.

## Publisher:

[imcaptor](https://clawhub.ai/user/imcaptor)

### License/Terms of Use:

MIT-0

## Use Case:

Go players and agent developers use this skill to convert board photos or board_ascii text into level-adjusted KataGo next-move recommendations. It returns enough engine data and visual overlays for the user to review the recognized board and compare candidate moves.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs local Python/OpenCV code and starts a local KataGo subprocess.

Mitigation: Install and run it only in an environment where local Python, OpenCV, and KataGo execution is acceptable.

Risk: Correction retries may save local copies of board photos and candidate labels in the recognition-label directory.

Mitigation: Avoid sensitive photos, set a controlled recognition-label directory, or delete the directory when retention is not desired.

Risk: Incorrect board recognition can make the recommended move unreliable.

Mitigation: Compare the source overlay or result image with the physical board and correct the board before relying on the recommendation.

Risk: Captures, ko/state ambiguity, or an unknown side to move can invalidate continuation analysis.

Mitigation: Ask for the side to move and re-shoot or reset the board after captures or ambiguous game-state changes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/imcaptor/skills/go-next-move)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, JSON, files, guidance]

**Output Format:** [Markdown guidance with shell commands plus JSON analysis results and optional image-file paths from the local analyzer]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires local python3 and katago; may write result images, overlays, temporary files, and local recognition-label bundles when correction retry is used.]

## Skill Version(s):

0.1.2 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
