FROM python:3.12-slim

WORKDIR /app

COPY pyproject.toml README-zh.md ./
COPY src ./src

RUN pip install --no-cache-dir .
RUN addgroup --system app && adduser --system --ingroup app app

ENV PYTHONUNBUFFERED=1 SP_ENV=production
EXPOSE 8000
USER app

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD ["python", "-c", "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/health', timeout=2)"]

CMD ["uvicorn", "second_perspective.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
