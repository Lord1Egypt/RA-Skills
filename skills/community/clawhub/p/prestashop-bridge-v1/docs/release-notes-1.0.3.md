# Release Notes 1.0.3

## Purpose
This release fixes publication trust issues by aligning version metadata, declaring the environment contract explicitly, and replacing all placeholder HMAC signatures with exact computed values.

## Changes
- Unified package version to `1.0.3` across `SKILL.md`, `_meta.json`, `README.md`, `openapi.yaml`, and eval metadata.
- Declared `.env.bridge.example` and the complete environment variable list in `_meta.json`.
- Replaced placeholder HMAC signatures with exact computed values in `examples.http` and `examples/*.http`.
- Strengthened `validators/validate_examples.py` to verify versions, environment metadata, and exact HMAC signatures.
- Expanded `docs/environment.md` and `SECURITY.md` to clarify runtime requirements and verification material.
