# Start And Verify

## Goal

Start the FastAPI server and confirm it is reachable before submitting a generation request.

## Start Command

From inside the `InfoDashboard` directory:

```bash
python main.py
```

The server binds to `0.0.0.0:8000` by default.

## Health Check

After startup, verify the server is running:

```bash
curl -fsS http://localhost:8000/
```

A 200 response (the chat UI HTML) confirms the server is up.

If the skill config provides a custom `url`, use that instead of `http://localhost:8000`.

## Troubleshooting

| Symptom | Likely Cause | Action |
|---------|--------------|--------|
| `ModuleNotFoundError` | Dependencies not installed | Run `pip install -e .` |
| `docker: command not found` | Docker not installed | Ask user to install Docker Desktop |
| `Cannot connect to Docker daemon` | Docker not running | Ask user to start Docker Desktop |
| Server starts but DB queries fail | frpc tunnel failed to connect | Check server logs for frpc warning; verify `tools/frpc-visitor.ini` is configured correctly |

## Confirmation Requirements

- Ask before running `python main.py`.
- Confirm the health check passes before moving to generation.
