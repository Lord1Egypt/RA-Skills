# jettyd skill — examples

Runnable examples showing how to integrate the jettyd IoT platform.

| File | What it shows |
|------|--------------|
| `langchain_tool.py` | Wrap the jettyd REST API as LangChain tools and drive them with a GPT-4o agent |

## Quick start

See the `langchain_tool.py` file header for dependency requirements.

```bash
export OPENAI_API_KEY=sk-...
python skills/jettyd/examples/langchain_tool.py
```

The API key is read automatically from `~/.openclaw/openclaw.json`
(`skills.entries.jettyd.apiKey`) or from the `JETTYD_API_KEY` environment variable.
