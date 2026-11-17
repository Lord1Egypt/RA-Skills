# Install humanize-text-skill in Claude Code

## Quick install

```bash
git clone https://github.com/fendouai/humanize-text-skill.git
cd humanize-text-skill
npm test
```

## Option A: project-local skill

Copy or symlink the skill into your project's Claude skill directory:

```bash
mkdir -p .claude/skills/humanize-text-skill
cp /path/to/humanize-text-skill/SKILL.md .claude/skills/humanize-text-skill/
cp -R /path/to/humanize-text-skill/references .claude/skills/humanize-text-skill/
cp -R /path/to/humanize-text-skill/policy .claude/skills/humanize-text-skill/
```

`policy/` is required. If it is missing, named voice modes should fail fast.

## Option B: plugin packaging

```bash
/plugin marketplace add fendouai/humanize-text-skill
/plugin install humanize-text-skill
```

See `plugins/humanize-text-skill/` for the packaged plugin layout.

## Health check

```bash
node -e "const H=require('./detector/patterns.js'); const r=H.analyzeText('值得注意的是，我们打造了一套方案。', { voiceMode: 'casual' }); console.log({ score: r.score, hasVoice: !!r.voice, drift: r.voice && r.voice.drift });"
```

## Usage

Natural-language requests work well:

- "Make this sound less like AI."
- "Rewrite this in a blunt voice."
- "Keep the technical facts, but make the note read like a real person wrote it."

Claude Code can infer the mode from context, or you can be explicit with `rewrite`, `detect`, or `edit`.

## Requirements

- Claude Code with agentskills.io `SKILL.md` support
- Node `>=18` only if you want to run the detector locally

## Related install docs

- [other-platforms.md](./other-platforms.md)
- [../cursor-rules/humanize-text-skill.mdc](../cursor-rules/humanize-text-skill.mdc)
