
# OpenClaw Web Gateway

## Type
interface

## Runtime
python

## Description
Lightweight Flask web interface that forwards chat requests to a configured OpenClaw HTTP endpoint.

The gateway provides a browser chat UI and stores minimal local state.

## Requirements
- Python 3.10+
- A reachable OpenClaw instance

## Configuration

Configuration is done using environment variables.

Typical values:

OPENCLAW_BASE=http://127.0.0.1:18789

OPENCLAW_AUTH=
OPENCLAW_AGENT=main
OPENCLAW_CHANNEL=web-gateway
OPENCLAW_MODEL=default
DEFAULT_USER=family
PORT=5002


`OPENCLAW_AUTH` is optional and only required if the upstream OpenClaw endpoint requires authentication.

## Run


python app.py

Then open:

http://127.0.0.1:5002


## Notes

The application may create small local runtime files in directories such as:

memory/
state/


These directories are intended for local runtime data and should not be committed to version control.
