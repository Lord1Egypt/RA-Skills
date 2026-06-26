## Description: <br>
Searches Mango TV video resources and opens the selected playback page in the system browser. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kllb520](https://clawhub.ai/user/kllb520) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to search Mango TV programs, open search results, or open known Mango TV playback links from an agent or command line. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can open user-supplied URLs in the system browser when --direct-url is used. <br>
Mitigation: Use --direct-url only with trusted HTTPS Mango TV links, and confirm broad or unexpected links with the user before opening them. <br>
Risk: The skill launches the system browser automatically during normal use. <br>
Mitigation: Run it only in environments where browser launches are expected; review the printed URL before manual opening in headless or restricted environments. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/kllb520/mgtv) <br>
- [Publisher Profile](https://clawhub.ai/user/kllb520) <br>
- [MGTV Suggest Search API](https://mobileso.bz.mgtv.com/pc/suggest/v1) <br>
- [README](README.md) <br>
- [Usage Guide](USAGE.md) <br>
- [Quickstart](QUICKSTART.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Guidance] <br>
**Output Format:** [Plain text console output with URLs and browser launch status] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May open the system browser; in headless or failure cases it prints a link for manual opening.] <br>

## Skill Version(s): <br>
1.0.2 (source: frontmatter, package.json, release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
