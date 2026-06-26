## Description: <br>
AI Mahjong assistant that recognizes Sichuan Mahjong hands from photos and provides discard recommendations, tenpai analysis, shanten calculation, safety scoring, dingque advice, swap-3 strategy, and opponent discard-pattern predictions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sceneun1ty](https://clawhub.ai/user/sceneun1ty) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill in OpenClaw-connected chat or messaging workflows to analyze Sichuan Mahjong hands, compare discard choices, understand waits, and assess tile safety from hand or table photos. Developers can also run the bundled Python analyzer directly with encoded tile inputs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Mahjong hand or table photos may include faces, documents, location clues, or other private background details when sent through OpenClaw or connected messaging and vision services. <br>
Mitigation: Crop images to the tiles or table before sending, avoid private background content, and use the bundled analyzer only with Mahjong tile inputs. <br>
Risk: Tile recognition or strategy analysis can be wrong if the photo is unclear or the recognized hand does not match the actual tiles. <br>
Mitigation: Confirm the recognized tile list before acting on discard, tenpai, shanten, dingque, swap-3, or opponent-pattern guidance. <br>


## Reference(s): <br>
- [Mahjong Theory Reference](references/mahjong_theory.md) <br>
- [Tile Visual Guide](references/tile_visual_guide.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/sceneun1ty/mahjong-ai) <br>
- [Publisher Profile](https://clawhub.ai/user/sceneun1ty) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with tile lists, discard rankings, safety indicators, and optional shell commands for the bundled analyzer] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Photo-based workflows should ask users to confirm recognized tiles before relying on strategy analysis.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
