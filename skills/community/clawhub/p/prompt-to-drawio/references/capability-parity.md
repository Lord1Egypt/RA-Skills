# Capability Parity Notes

This skill maps core Next AI Draw.io capabilities into CLI flows.

## Mapped

- Prompt-based diagram creation -> `generate`
- ID-based diagram edits -> `edit` (LLM JSON operations + local XML apply)
- File ingestion (text/pdf/image) -> `--file`
- URL ingestion -> `--url`
- Shape library lookup -> `library` and `--shape-library`
- Visual validation loop -> `--validate` + `--validation-retries`
- Image export -> `--out-image` or `export`
- Edit history snapshots -> auto backup before edit

## Not Included

- Browser chat UI and streaming UI states
- Multi-user session persistence and UI history panels
- Provider-specific SDK abstractions (this skill uses OpenAI-compatible HTTP API)
