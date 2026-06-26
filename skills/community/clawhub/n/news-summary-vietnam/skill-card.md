## Description: <br>
News Summary gathers Vietnamese headlines from Bao Moi, VnExpress, Tuoi Tre, and Dan Tri, then posts linked summaries to a configured Telegram channel. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[padit69](https://clawhub.ai/user/padit69) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and operators use this skill to automate daily Vietnamese news digests and publish them to a Telegram channel with links back to the original articles. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Telegram bot credentials may be exposed or over-privileged if reused broadly or committed with configuration files. <br>
Mitigation: Use a dedicated Telegram bot with only channel-posting permissions and keep config.json out of source control. <br>
Risk: The install flow can add a recurring cron job that continues posting after the user no longer expects it. <br>
Mitigation: Inspect the cron line after running install.sh and remove the cron job when scheduled posts are no longer wanted. <br>
Risk: Multiple config search paths can make the skill use a different Telegram token or channel than intended. <br>
Mitigation: Verify which config.json file will be used before running the scheduled poster. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/padit69/news-summary-vietnam) <br>
- [Bao Moi](https://baomoi.com) <br>
- [VnExpress RSS feed](https://vnexpress.net/rss/tin-moi-nhat.rss) <br>
- [Tuoi Tre RSS feed](https://tuoitre.vn/rss/homepage.rss) <br>
- [Dan Tri RSS feed](https://dantri.com.vn/rss/home.rss) <br>
- [Telegram Bot API sendMessage endpoint](https://api.telegram.org/bot{BOT_TOKEN}/sendMessage) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Telegram HTML message text with linked news items, plus setup guidance and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a user-provided Telegram bot token and chat ID; scheduled posting is configured through cron.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
