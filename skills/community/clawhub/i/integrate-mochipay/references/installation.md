# Install and use

Current published download: https://mochi.bz/Developers/Skill.aspx
ClawHub: https://clawhub.ai/hznetnewpower/skills/integrate-mochipay
Guide: https://mochi.bz/Developers/Skill.aspx

ZIP contains one integrate-mochipay folder with SKILL.md, references, assets and an optional Python helper. It does not install a gateway, open an account or grant store/API access.

## Claude

Enable code execution/file creation if the account/workspace permits. Open Customize > Skills > + > Create skill > Upload a skill, upload the complete ZIP and enable it. Ask: "Use MochiPay Integration to connect my store." A conversation attachment is not persistent installation.
Official: https://support.claude.com/en/articles/12512180-use-skills-in-claude

## Claude Code

Extract to ~/.claude/skills/integrate-mochipay/SKILL.md (personal) or <project>/.claude/skills/integrate-mochipay/SKILL.md (project). Avoid duplicate nested folders. Invoke /integrate-mochipay or request MochiPay setup. Follow client refresh guidance if absent.
Official: https://code.claude.com/docs/en/skills

## Codex CLI / IDE

Extract to ~/.agents/skills/integrate-mochipay/SKILL.md (personal) or <project>/.agents/skills/integrate-mochipay/SKILL.md (project). Run /skills or mention $integrate-mochipay. Codex detects skills automatically; check path/discovery if absent.
Official: https://learn.chatgpt.com/docs/build-skills

## Other assistants

Follow the client's documented Agent Skills support: https://agentskills.io/specification. Generic chatbots and ordinary ChatGPT conversations do not necessarily install skill ZIPs. File/network/script tools and account features vary. No MCP server is bundled. Python3 is optional for offline checks; guidance works without it.

Free under the included MIT-0 license; MochiPay service subscriptions and AI-tool charges/features are separate. Merchant authorization/private configuration are required for store/API actions. Official ClawHub listing: https://clawhub.ai/hznetnewpower/skills/integrate-mochipay.
