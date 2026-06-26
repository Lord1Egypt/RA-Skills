# karpathy-llm-wiki

OpenClaw skill. LLM-maintained persistent wiki from your sources.

Based on [Karpathy's LLM-Wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f).

## Install

```bash
npx clawhub@latest install karpathy-llm-wiki
```

## Usage

```
"Add this article to my wiki: ..."
"What do I know about <topic>?"
"Lint my wiki"
"Initialize a new wiki"
```

Default wiki root: `~/wiki` — override in `~/.agent-wiki.json`:
```json
{ "wikiRoot": "/path/to/wiki" }
```

## License

MIT
