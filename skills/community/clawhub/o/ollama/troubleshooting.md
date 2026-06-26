# Troubleshooting

## API Does Not Respond

Symptoms:
- `curl http://127.0.0.1:11434/api/tags` fails
- local apps report connection refused

Checks:
1. confirm the Ollama process is running
2. start `ollama serve` in the foreground if needed
3. verify the app is pointing at the correct host and port

## Slow Inference

Symptoms:
- responses take much longer than expected
- laptop fans spike or the host feels memory-bound

Checks:
1. inspect `ollama ps` for CPU or mixed CPU/GPU loading
2. reduce model size or context length
3. verify disk space and avoid swap pressure before blaming the model family

## Wrong or Missing Structured Output

Symptoms:
- prose appears when downstream code expects JSON

Checks:
1. disable streaming for that request
2. set `format: "json"` or a JSON schema
3. force low temperature and parse the result before acting

## Broken Modelfile Behavior

Symptoms:
- prompt behavior changed after creating a custom model
- the app prompt and model instructions appear to conflict

Checks:
1. inspect `ollama show --modelfile MODEL:TAG`
2. compare `SYSTEM`, `TEMPLATE`, and `PARAMETER` settings against the app prompt
3. rebuild under a new model name so rollback is easy

## Weak Retrieval

Symptoms:
- RAG answers feel vague even when the source text exists locally

Checks:
1. verify indexing and querying use the same embedding model
2. inspect top-k retrieved chunks directly
3. tune chunking and metadata before switching chat models

## Port Exposure Risk

Symptoms:
- user wants LAN or server access quickly

Checks:
1. keep localhost-only binding until approval is explicit
2. document auth, firewall, proxy, and scope before exposure
3. treat public or shared-network exposure as a separate security decision
