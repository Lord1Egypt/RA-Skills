# hekouwang-claude-skill-doctor-skill · 免费 CLI 体检器
# 零依赖：仅需 Python 标准库。
FROM python:3.12-slim@sha256:a6e34c598f2467ed0e9a8d349809fcd8b5c603269512df273a0bb1784edc11b1

LABEL org.opencontainers.image.title="hekouwang-claude-skill-doctor-skill"
LABEL org.opencontainers.image.description="Agent Skill (SKILL.md) health checker — score + fixes"
LABEL org.opencontainers.image.licenses="MIT"
LABEL org.opencontainers.image.source="https://github.com/huiyonghkw/hekouwang-claude-skill-doctor-skill"

WORKDIR /app
COPY check.py /app/check.py

# 把要体检的 skill 目录只读挂到 /work：
#   docker build -t claude-skill-doctor .
#   docker run --rm -v "$PWD:/work:ro" claude-skill-doctor
#   docker run --rm -v "$PWD:/work:ro" claude-skill-doctor /work --json
ENTRYPOINT ["python3", "/app/check.py"]
CMD ["/work"]
