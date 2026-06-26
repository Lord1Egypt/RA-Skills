# Quickstart CLI (OpenClaw + OpenDataLoader)

## Goal
Provide a minimal and robust path to convert PDFs without MCP, using CLI only.

## Step 0 (required): installation security
Before running any pip install command, review:
docs/security-before-install.md

## Requirements
- Java 11+
- Python 3.10+
- Installed package

## Recommended installation (safe baseline)
1) Create and activate an isolated environment:
python -m venv .venv
.venv\Scripts\activate

2) Verify package metadata before install:
pip install --upgrade pip
pip index versions opendataloader-pdf
pip show opendataloader-pdf

3) Install a pinned version (example pattern):
pip install "opendataloader-pdf[hybrid]==<version>"

4) Freeze dependencies for reproducibility:
pip freeze > requirements.lock.txt

## Quick checks
java -version
opendataloader-pdf --help

## Base conversion
opendataloader-pdf file1.pdf file2.pdf ./folder/ -o ./output -f json,markdown

## Performance rule
Always process files in batches (single call) to avoid JVM startup overhead per invocation.

## Recommended output for OpenClaw
- json for metadata and bounding boxes
- markdown for natural LLM context
- default combination: json,markdown
