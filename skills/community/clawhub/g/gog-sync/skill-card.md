## Description: <br>
Sync GOG game library, save files, and custom configs across devices. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[terrycarter1985](https://clawhub.ai/user/terrycarter1985) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Players and game-library maintainers use this skill to sync GOG libraries, save files, and selected custom configuration files across devices or remote storage. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Rsync can overwrite files or copy data to an unintended remote destination. <br>
Mitigation: Inspect sync.sh, replace placeholder user@remote destinations with a controlled host, and run a manual backup or rsync dry run before first use. <br>
Risk: A broad GOG_CONFIG_DIR value could sync files outside the intended game configuration scope. <br>
Mitigation: Keep GOG_CONFIG_DIR limited to game configuration folders before running sync-config. <br>


## Reference(s): <br>
- [GOG Sync ClawHub Release](https://clawhub.ai/terrycarter1985/gog-sync) <br>
- [terrycarter1985 ClawHub Profile](https://clawhub.ai/user/terrycarter1985) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration values] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires rsync; gogrepo is optional for full library sync.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
