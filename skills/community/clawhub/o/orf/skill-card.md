## Description: <br>
ORF fetches German-language ORF news headlines focused on Austrian and international politics, excludes sports, sends each item as title, age, and link, and generates a cartoon ZiB studio image from the selected stories. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cpojer](https://clawhub.ai/user/cpojer) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use ORF to pull a short German-language ORF news digest, prioritize politics and major headlines, and produce a companion ZiB-style generated image. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read a Gemini/Nano Banana API key from the environment or a local OpenClaw config file. <br>
Mitigation: Prefer setting GEMINI_API_KEY explicitly and review local credential access before installing or running the skill. <br>
Risk: The image-generation helper installs unpinned Python packages at runtime into ./tmp/orf-venv. <br>
Mitigation: Verify the dependencies before use and remove or rebuild the generated virtual environment when needed. <br>


## Reference(s): <br>
- [ORF News](https://news.orf.at/) <br>
- [ORF RSS Feeds](https://rss.orf.at/) <br>
- [ORF News RSS](https://rss.orf.at/news.xml) <br>
- [ORF Austria RSS](https://rss.orf.at/oesterreich.xml) <br>
- [ClawHub ORF Skill Page](https://clawhub.ai/cpojer/orf) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Image, Shell commands] <br>
**Output Format:** [Plain text news-item messages plus a generated PNG image; helper scripts can emit JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [News count is capped at 15; output excludes sports and uses ORF RSS/news links.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
