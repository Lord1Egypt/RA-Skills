## Description: <br>
A personal Garmin and AI health coach that analyzes sleep, activity, HRV, stress, and body battery data to produce actionable daily wellness guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[daasai](https://clawhub.ai/user/daasai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to connect Garmin wearable data and NotebookLM, configure health goals, and receive scheduled or on-demand daily wellness reports. It is intended for lifestyle coaching and self-tracking, not diagnosis or treatment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles sensitive health-derived data, Garmin account identifiers, Google/NotebookLM sessions, local health history, and logs. <br>
Mitigation: Install only if comfortable connecting Garmin and Google/NotebookLM; protect local account/session files; and delete ~/.openclaw/data/health-assistant plus related logs when resetting. <br>
Risk: Generated wellness guidance may be incomplete, inaccurate, or inappropriate for medical decisions. <br>
Mitigation: Treat outputs as lifestyle guidance only, review recommendations before acting, and consult qualified medical professionals for diagnosis, treatment, or urgent symptoms. <br>
Risk: Automatic setup can install Python packages and Playwright browser components. <br>
Mitigation: Prefer manual, reviewed dependency installation and verify the environment before regular use. <br>
Risk: The broad trigger phrase "report" can generate health reports unintentionally in normal chat. <br>
Mitigation: Use a more specific trigger phrase before regular use, such as "health report" or a dedicated scheduled command. <br>


## Reference(s): <br>
- [ClawHub Health Assistant release page](https://clawhub.ai/daasai/health-coach) <br>
- [OpenClaw](https://github.com/openclaw/openclaw) <br>
- [garth Garmin API client](https://github.com/matin/garth) <br>
- [notebooklm-py NotebookLM CLI](https://github.com/teng-lin/notebooklm-py) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text and Markdown health reports, setup prompts, and shell command guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports may include wearable metrics, trend summaries, and AI-generated recommendations for instant messaging delivery.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release metadata; artifact frontmatter reports 0.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
