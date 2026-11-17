# johnny — a virtual second designer

A [Claude Code skill](https://code.claude.com/docs/en/skills) that turns a thread into an ongoing design dialog with **Johnny** — a calm, terse virtual design partner inspired by the spirit of Jony Ive (an inspiration, not an imitation of the real person). He challenges by default, keeps pulling the conversation back to "what problem does this solve?", and answers "how do others do this" questions from UX expertise, notes, or the web.

## What it does

- **Senior sparring partner** — listens, sharpens your half-formed thoughts, names weak spots and counterarguments instead of agreeing.
- **Expert consultant** — UX patterns, best practices, how the industry does things; cites where a fact came from.
- **Conversational format** — short spoken-style replies, one thought at a time, no bullet lists or headings.
- **Lazy context** — loads nothing upfront; goes to your notes or the web only when a topic comes up.
- **Notes on request** — writes nothing during the conversation; when a topic wraps up, offers a one-line "save this?" and only writes after a yes.

## Install

Copy the `johnny` folder into your skills directory:

- per project: `<project>/.claude/skills/johnny/`
- globally: `~/.claude/skills/johnny/`

## Use

Start a message by addressing Johnny («Johnny, …»), or invoke `/johnny`. The whole thread then stays in dialog mode until you say otherwise.

## Customize

Everything lives in `SKILL.md`:

- **Persona** — rename Johnny or swap the character; keep the "challenge by default" role if you want the sparring effect.
- **Knowledge base** — the "Context — lazily" section is generic; point it at your own notes/vault folders for better grounding.
- **Language** — the persona speaks the language you write in; translate the body and `description` if you want to pin a specific one.

## License

[MIT](../LICENSE)
