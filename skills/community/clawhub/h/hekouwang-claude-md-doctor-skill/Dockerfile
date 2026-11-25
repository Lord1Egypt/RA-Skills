# hekouwang-claude-md-doctor-skill · 免费 CLI 体检器
# 零依赖：仅需 Python 标准库。
FROM python:3.12.7-slim-bookworm

LABEL org.opencontainers.image.title="hekouwang-claude-md-doctor-skill"
LABEL org.opencontainers.image.description="CLAUDE.md health checker — score + fixes"
LABEL org.opencontainers.image.licenses="MIT"
LABEL org.opencontainers.image.source="https://github.com/huiyonghkw/hekouwang-claude-md-doctor-skill"

WORKDIR /app
COPY check.py /app/check.py

# 把你的项目挂到 /work 即可体检（示例锁定版本 tag，别用无 tag 镜像）：
#   docker build -t hekouwang-claude-md-doctor:1.3.7 .
#   docker run --rm -v "$PWD:/work" hekouwang-claude-md-doctor:1.3.7          # 体检当前项目
#   docker run --rm -v "$PWD:/work" hekouwang-claude-md-doctor:1.3.7 /work --json
ENTRYPOINT ["python3", "/app/check.py"]
CMD ["/work"]
