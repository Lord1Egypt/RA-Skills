## Description: <br>
Trainer Buddy Pro is an AI fitness coaching skill that generates equipment-aware workouts, tracks workout history and personal records, adapts programming around injuries, and provides form guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nollio](https://clawhub.ai/user/nollio) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users use this skill as a chat-based strength coach for workout generation, progress logging, split planning, form cues, and injury-aware exercise substitutions. The skill is intended for general fitness guidance and explicitly directs users to qualified healthcare providers for medical concerns. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores and changes sensitive fitness profile data, including body metrics, injuries, and physical limitations. <br>
Mitigation: Review profile changes before saving them, keep local data protected, and define consent, deletion, and retention rules before using dashboard or cloud-backed modes. <br>
Risk: Workout guidance may be mistaken for medical or rehabilitation advice. <br>
Mitigation: Keep the medical disclaimer visible in user interactions, avoid diagnosis or rehabilitation protocols, and direct users to qualified healthcare providers for pain, injury, or emergency symptoms. <br>
Risk: The bundled backup script is identified by the security guidance as unsafe to run until fixed. <br>
Mitigation: Do not run the backup script in production workflows until it has been repaired and re-reviewed. <br>
Risk: Optional dashboard or cloud storage can expose sensitive fitness and injury data without appropriate safeguards. <br>
Mitigation: Add authentication, access controls, and clear data handling rules before enabling Supabase, cloud sync, or shared dashboard deployments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nollio/normieclaw-trainer-buddy-pro) <br>
- [Publisher profile](https://clawhub.ai/user/nollio) <br>
- [README](artifact/README.md) <br>
- [Security audit](artifact/SECURITY.md) <br>
- [Dashboard specification](artifact/dashboard-kit/DASHBOARD-SPEC.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON data structures, shell command blocks, and workout templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local JSON files for user profiles, workout logs, personal records, and configuration when the host agent grants file access.] <br>

## Skill Version(s): <br>
1.0.3 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
