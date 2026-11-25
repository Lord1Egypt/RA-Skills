# lego-moc

An agent skill that turns photos of loose LEGO parts into a parts inventory, then lets your agent design a model (MOC) from those parts and have it checked and rendered.

拍照识别散装乐高零件，生成零件清单；再让 agent 用这些零件设计作品（MOC），由服务器检验能否拼出来，通过后给出带 3D 预览和拼装步骤的链接。2.1 起支持自由创作：没有零件，或者不想受库存限制时，可以用全部 LDraw 零件设计，同样要过物理检验。

Works with any agent that can run Python 3 and reach the internet: Claude Code, Codex, WorkBuddy, OpenClaw and others. Since 2.0 the agent can use it through MCP tools instead of shell commands, which means far fewer approval prompts.

## What it does

1. **Scan.** The agent uploads 1–30 photos. The server finds each part, identifies its LDraw part number and colour, and keeps the inventory under your user ID. You can correct it afterwards: change a quantity, delete a row, or confirm a part the server was unsure of.
2. **Design and verify.** The agent designs a model from that inventory and writes it as an LDraw file. The server checks that the parts really connect and the model holds together. If not, it returns fix notes that name the offending lines. If it passes, it returns a public link with a 3D view and step-by-step building instructions, plus two preview pictures and how much of your inventory the model uses.
3. **Free build (new in 2.1).** No parts, or want something bigger than your collection? Ask for a free build ("free build", "unlimited parts", 「自由创作」「不限零件」). The agent designs with any of about 14,000 LDraw parts in any colour and quantity, and the model goes through the same physics check. The page's parts list is then the list of what you would need to get. Examples: [yellow submarine](https://lego.groundrl.com/skill/moc/mujtuwfmzc9dvkn3t8gnu), [castle](https://lego.groundrl.com/skill/moc/md2jkmb7bqy7jfb53ce5a), [pagoda](https://lego.groundrl.com/skill/moc/mfda4ucr3qm6ev6p73z3s). The verifier does not know which part exists in which colour as a real element. Models have 10 to 400 parts.

## Install

Clone this repository into your agent's skills folder. For Claude Code:

```bash
git clone https://github.com/garmanwu/lego-moc ~/.claude/skills/lego-moc
```

With ClawHub:

```bash
clawhub install @garmanwu/lego-moc
```

Or copy `SKILL.md` and `scripts/lego.py` into a folder named `lego-moc` wherever your agent keeps skills.

### Connect the MCP tools (recommended)

The same script runs as a local MCP server, so the agent calls tools instead of running shell commands. Print the configuration and paste it into your agent's MCP settings, then restart the agent:

```bash
python3 scripts/lego.py mcp-config
```

It prints something like this, with the paths for your computer filled in:

```json
{"mcpServers": {"lego-moc": {"type": "stdio", "command": "/usr/bin/python3", "args": ["/path/to/lego-moc/scripts/lego.py", "mcp"]}}}
```

For Claude Code: `claude mcp add lego-moc -- python3 /path/to/lego-moc/scripts/lego.py mcp`.

Agents that cannot start a local program can use the remote endpoint instead (`python3 scripts/lego.py mcp-config --remote`). It offers everything except photo upload, which then still goes through the script.

Without the MCP setup the skill still works through the script, as in 1.x.

## Use

Ask your agent, for example:

- "Scan these LEGO photos and tell me what parts I have."
- "Design a small car from my parts and give me building instructions."

Or run the script yourself:

```bash
python3 scripts/lego.py scan photo1.jpg photo2.jpg
python3 scripts/lego.py moc guide
python3 scripts/lego.py moc submit model.ldr
```

After a scan you get a link to a page that shows your inventory with pictures, where you can also correct it, and a second tab that lists your models.

`SKILL.md` has the full command list, exit codes and output format.

## Requirements

- Python 3.8 or later. The script uses the standard library only.
- Internet access to the recognition server.

## What leaves your computer

- The script sends the photos you scan, and the model and parts list you submit, to the recognition server at `https://lego.groundrl.com`. The connection is HTTPS.
- The server keeps the results under a random 8-character user ID, which the script stores in `~/.lego-parts/`. No account or API key is needed.
- The inventory has a web page with pictures of every part, at a link that contains the user ID. Anyone who has that link or the ID can see and change the inventory, so do not post it publicly.
- A model that passes gets a public link. Anyone who has the link can open it, and the page shows the request text your agent passed along (`brief`).
- Do not scan photos that show anything you would not want to share.

## Limits

- 30 photos per request and 60 photos per user ID per day.
- 30 model submissions per user ID per day, and 5 resubmissions per model.
- A photo that was uploaded before is refused and not recognised again.
- The first scan after an idle period waits about two minutes while the GPU starts.
- Spread the parts out on a plain surface and shoot from directly above. Piled parts are recognised poorly.

## Licence

MIT-0. LEGO® is a trademark of the LEGO Group, which does not sponsor or endorse this project.
