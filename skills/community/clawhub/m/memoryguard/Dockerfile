FROM python:3.12-slim

WORKDIR /app

COPY pyproject.toml setup.py ./
COPY src/ ./src/
COPY README.md ./

RUN pip install --no-cache-dir -e .

ENTRYPOINT ["python", "-m", "memoryguard.mcp_server"]
