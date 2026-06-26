## Description: <br>
Downloads text ebooks from Z-Library and sends them to a configured Kindle email address. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiehaixin](https://clawhub.ai/user/xiehaixin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users or operators use this skill to search for a text ebook, resolve ambiguous author or publisher matches, download the selected file, and send it to their Kindle address when they have the legal right to do so. <br>

### Deployment Geography for Use: <br>
Global, subject to local copyright law and service availability. <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires Z-Library account credentials, SMTP sending credentials, and a Kindle recipient address. <br>
Mitigation: Use dedicated or app-specific credentials, prefer environment variables, and keep any auth.json file restricted to the local user. <br>
Risk: The skill logs into live website mirrors, downloads files, and sends email from the configured account. <br>
Mitigation: Review the selected mirror domains, avoid untrusted proxies, and confirm the downloaded title before allowing email delivery. <br>
Risk: Downloaded files and search screenshots are stored under /tmp/kindle_downloads. <br>
Mitigation: Clear /tmp/kindle_downloads after use and avoid running the skill on shared systems without cleanup controls. <br>
Risk: The skill can be used to download copyrighted ebooks. <br>
Mitigation: Use it only for ebooks that the user is legally authorized to download under applicable local law. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xiehaixin/kindle-download) <br>
- [Z-Library](https://zlibrary-global.se/) <br>
- [Amazon Kindle content and device settings](https://www.amazon.com/myk) <br>
- [README](artifact/README.md) <br>
- [Security notes](artifact/SECURITY.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text with shell commands, status messages, and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include local file paths and screenshot references produced by the skill scripts.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
