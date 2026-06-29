---
source: "hr-resume-evaluation/tests/test_llm_client.py"
core_kind: "code_project_core"
file_type: "py"
generated: "2026-06-14T08:55:07"
tags:
  - core-file
  - code-project-core
  - py
---
<!-- CORE_FILE_NOTE_V1 -->
# test_llm_client.py

- Source file: [[hr-resume-evaluation/tests/test_llm_client.py|test_llm_client.py]]
- Folder index: [[hr-resume-evaluation/tests/资料索引|资料索引]]
- Core kind: `code_project_core`
- Size: 10.40 KB
- Modified: 2026-06-13T15:23:37

## Summary
- PY source sample: 358 lines.
- Imports: json, pytest, requests, scripts.llm_client
- Functions: test_load_model_config_reads_yaml, test_missing_api_key_raises, test_build_messages_contains_no_secret, test_build_messages_includes_deterministic_candidate_id, test_build_messages_includes_score_formulas, test_build_messages_includes_scoring_weights, _test_config, test_evaluate_with_model_posts_json_and_parses_content, test_non_retryable_http_error_fails_once, test_malformed_json_retries_and_succeeds, test_repeated_malformed_json_fails_sanitized_after_retries, test_retryable_http_error_retries

## Related files
- [[hr-resume-evaluation/tests/test_parse_documents.py.core|test_parse_documents.py]] - same folder
- [[hr-resume-evaluation/tests/test_validate_results.py.core|test_validate_results.py]] - same folder
- [[hr-resume-evaluation/tests/test_render_reports.py.core|test_render_reports.py]] - same folder
- [[hr-resume-evaluation/tests/test_evaluate_resumes.py.core|test_evaluate_resumes.py]] - same folder
- [[hr-resume-evaluation/tests/test_end_to_end_outputs.py.core|test_end_to_end_outputs.py]] - same folder

## Graph tags
- #core-file/code-project-core
- #file-type/py

## Content preview
```py
import json

import pytest
import requests

from scripts.llm_client import (
    MissingApiKey,
    ModelConfig,
    ModelResponseError,
    build_messages,
    evaluate_with_model,
    load_model_config,
)


def test_load_model_config_reads_yaml(tmp_path):
    config_path = tmp_path / "model.yaml"
    config_path.write_text(
        "\n".join(
            [
                "base_url: https://api.example.com",
                "chat_completions_path: /chat/completions",
                "model: test-model",
                "api_key_env: TEST_API_KEY",
                "timeout_seconds: 30",
                "max_retries: 1",
                "temperature: 0.1",
            ]
        ),
        encoding="utf-8",
    )

    config = load_model_config(config_path)

    assert config.model == "test-model"
    assert config.api_key_env == "TEST_API_KEY"


def test_missing_api_key_raises(monkeypatch, tmp_path):
    monkeypatch.delenv("TEST_API_KEY", raising=False)
    config_path = tmp_path / "model.yaml"
    config_path.write_text(
        "\n".join(
            [
                "base_url: https://api.example.com",
                "model: test-model",
                "api_key_env: TEST_API_
```

## Processing notes
- encoding=utf-8-sig
