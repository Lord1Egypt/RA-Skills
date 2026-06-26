## Description: <br>
A learning assistant app that combines dictionary lookup, translation, facts, math calculation, history events, and local preference storage. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fish1981bimmer](https://clawhub.ai/user/fish1981bimmer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and learners can run this Node.js web app locally to access common study utilities, including word definitions, translation, random facts, math calculations, and historical events. The app also stores preferences, history, favorites, and usage statistics on the local filesystem. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The calculator endpoint can execute submitted text as server code. <br>
Mitigation: Replace eval with a safe math parser before using the app beyond a trusted local environment. <br>
Risk: Data management routes can expose, import, export, or clear saved local history and preferences. <br>
Mitigation: Keep the server bound to localhost and protect or remove the export, import, and clear routes before exposing the app on a network. <br>
Risk: User text may be sent to third-party APIs and stored in local history. <br>
Mitigation: Avoid entering sensitive text unless third-party API sharing and local storage are acceptable for the use case. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/fish1981bimmer/learning-assistant-app) <br>
- [DictionaryAPI](https://dictionaryapi.dev/) <br>
- [LibreTranslate](https://libretranslate.com/) <br>
- [Useless Facts API](https://uselessfacts.jsph.pl/) <br>
- [MuffinLabs Today in History API](https://history.muffinlabs.com/date) <br>
- [API Ninjas Historical Events API](https://api.api-ninjas.com/v1/historicalevents) <br>


## Skill Output: <br>
**Output Type(s):** [Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Source files with Markdown setup and usage instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs as a local Node.js and Express web app with browser-based UI and local file storage.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, SKILL.md frontmatter, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
