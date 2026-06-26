#!/usr/bin/env python3
"""
OpenClaw Expert Brain - Ask via nlm CLI
Usa notebooklm-mcp-cli (nlm) para queries a NotebookLM.
MIT License.
"""
import argparse
import subprocess
import sys
import os

DEFAULT_NOTEBOOK_ID = os.environ.get(
    "OPENCLAW_NOTEBOOK_ID",
    "577a138c-807f-45d7-9ff4-cb1d6da190c0"
)

def ask(question, notebook_id=None):
    nb_id = notebook_id or DEFAULT_NOTEBOOK_ID
    try:
        result = subprocess.run(
            ["nlm", "notebook", "query", nb_id, question],
            capture_output=True,
            text=True,
            timeout=60
        )
        if result.returncode == 0:
            raw = result.stdout.strip()
            try:
                import json
                data = json.loads(raw)
                return data.get("value", {}).get("answer", raw)
            except (json.JSONDecodeError, AttributeError):
                return raw
        else:
            return f"ERROR: {result.stderr.strip() or 'Query failed'}"
    except FileNotFoundError:
        return "ERROR: nlm no encontrado. Instala: pip install notebooklm-mcp-cli"
    except subprocess.TimeoutExpired:
        return "ERROR: Timeout esperando respuesta de NotebookLM (60s)"

def main():
    parser = argparse.ArgumentParser(description="OpenClaw Expert Brain")
    parser.add_argument("--question", "-q", required=True, help="Pregunta a hacer")
    parser.add_argument("--notebook-id", help="ID del notebook NotebookLM")
    args = parser.parse_args()

    answer = ask(args.question, args.notebook_id)
    print(answer)

if __name__ == "__main__":
    main()
