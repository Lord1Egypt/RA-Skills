from __future__ import annotations

import argparse
import os
from pathlib import Path
from typing import Any

import yaml

from second_perspective.api.main import app


def action_schema(public_base_url: str) -> dict[str, Any]:
    schema = app.openapi()
    schema["servers"] = [{"url": public_base_url.rstrip("/")}]
    components = schema.setdefault("components", {})
    security_schemes = components.setdefault("securitySchemes", {})
    security_schemes["bearerAuth"] = {"type": "http", "scheme": "bearer"}

    for path, operations in schema.get("paths", {}).items():
        if path == "/health":
            continue
        for operation in operations.values():
            if not isinstance(operation, dict) or "operationId" not in operation:
                continue
            operation["security"] = [{"bearerAuth": []}]
            operation["parameters"] = [
                parameter
                for parameter in operation.get("parameters", [])
                if parameter.get("name", "").casefold() != "authorization"
            ]

    return schema


def main() -> None:
    parser = argparse.ArgumentParser(description="Export the API as an Action-ready OpenAPI file.")
    parser.add_argument("--output", default="openapi-action.yaml")
    args = parser.parse_args()

    base_url = os.getenv("SP_PUBLIC_BASE_URL", "https://YOUR-DOMAIN.example.com")
    destination = Path(args.output)
    destination.write_text(
        yaml.safe_dump(
            action_schema(base_url),
            sort_keys=False,
            allow_unicode=True,
            width=100,
        ),
        encoding="utf-8",
    )
    print(f"Wrote {destination}")


if __name__ == "__main__":
    main()
