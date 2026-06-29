---
source: "hr-resume-evaluation/scripts/llm_client.py"
core_kind: "code_project_core"
file_type: "py"
generated: "2026-06-14T08:55:07"
tags:
  - core-file
  - code-project-core
  - py
---
<!-- CORE_FILE_NOTE_V1 -->
# llm_client.py

- Source file: [[hr-resume-evaluation/scripts/llm_client.py|llm_client.py]]
- Folder index: [[hr-resume-evaluation/scripts/资料索引|资料索引]]
- Core kind: `code_project_core`
- Size: 7.58 KB
- Modified: 2026-06-13T15:23:04

## Summary
- PY source sample: 215 lines.
- Imports: dataclasses, pathlib, typing, json, os, time, requests, yaml
- Classes: MissingApiKey, ModelResponseError, ModelConfig
- Functions: load_model_config, build_messages, _http_status_code, _is_retryable_status, _raise_model_error, _parse_model_response, evaluate_with_model

## Related files
- [[hr-resume-evaluation/scripts/__init__.py.core|__init__.py]] - same folder
- [[hr-resume-evaluation/scripts/parse_documents.py.core|parse_documents.py]] - same folder
- [[hr-resume-evaluation/scripts/validate_results.py.core|validate_results.py]] - same folder
- [[hr-resume-evaluation/scripts/render_reports.py.core|render_reports.py]] - same folder
- [[hr-resume-evaluation/scripts/evaluate_resumes.py.core|evaluate_resumes.py]] - same folder

## Graph tags
- #core-file/code-project-core
- #file-type/py

## Content preview
```py
from dataclasses import dataclass
from pathlib import Path
from typing import Any
import json
import os
import time

import requests
import yaml


class MissingApiKey(RuntimeError):
    pass


class ModelResponseError(RuntimeError):
    pass


@dataclass(frozen=True)
class ModelConfig:
    base_url: str
    chat_completions_path: str
    model: str
    api_key_env: str
    timeout_seconds: int
    max_retries: int
    temperature: float

    def api_key(self) -> str:
        value = os.environ.get(self.api_key_env)
        if not value:
            raise MissingApiKey(f"Missing API key environment variable: {self.api_key_env}")
        return value

    @property
    def endpoint(self) -> str:
        return f"{self.base_url.rstrip('/')}/{self.chat_completions_path.lstrip('/')}"


def load_model_config(path: str | Path) -> ModelConfig:
    data = yaml.safe_load(Path(path).read_text(encoding="utf-8")) or {}
    return ModelConfig(
        base_url=data["base_url"],
        chat_completions_path=data.get("chat_completions_path", "/chat/completions"),
        model=data["model"],
        api_key_env=data["api_key_env"],
        timeout_seconds=data.get("timeout_seconds", 120),
```

## Processing notes
- encoding=utf-8-sig
