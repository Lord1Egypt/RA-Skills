FROM python:3.13-slim

WORKDIR /app

COPY . /app

RUN chmod +x /app/scripts/mai.py /app/scripts/mai_registry.py /app/scripts/verify.sh \
  && mkdir -p /data

VOLUME ["/data"]

EXPOSE 8765

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD python3 -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8765/health', timeout=2).read()"

CMD ["python3", "scripts/mai_registry.py", "serve", "--data", "/data/mai-registry.json", "--host", "0.0.0.0", "--port", "8765", "--rate-limit-per-minute", "60"]
