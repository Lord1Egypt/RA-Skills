Running headful-browser-vnc in Docker

This repository includes a reference Dockerfile and docker-compose.yml to run the skill in a containerized environment. The container bundles Xvfb, x11vnc, Chromium, and helper scripts so the runtime behaves consistently across hosts that support Docker.

Quickstart (build + run):

1) Build the image (from skills/headful-browser-vnc/docker):
   docker build -t headful-browser-vnc:latest .

2) Create a skill-local .env next to the repo (or mount one). Minimal example:
   VNC_PASSFILE=/root/.vnc/passwd
   VNC_DISPLAY=:99
   VNC_RESOLUTION=1366x768
   REMOTE_DEBUG_PORT=9222

3) Run with docker-compose (binds ports 5900, 9222)
   docker-compose up --build -d

Notes and security
- Exposing the container's VNC port to the network is risky. Prefer SSH port forwarding into the host or limit docker-compose ports to localhost (127.0.0.1:5900:5900) where possible.
- For production, run as a non-root user inside container and bind mount an artifacts directory for persistence.
- The Dockerfile provided is a reference and intentionally permissive; create hardened images for production use.

If you want I can refine the Dockerfile (smaller base image, install Google Chrome .deb instead of apt chromium, add non-root user) — reply make-docker-refine.

---
Dockerfile (reference)

The original Dockerfile content is provided below as an inline code block because ClawHub does not accept Dockerfile uploads. Use this as the canonical build instructions to reproduce the container image.

```Dockerfile
FROM ubuntu:22.04
ENV DEBIAN_FRONTEND=noninteractive

# Install runtime deps: Xvfb, x11vnc, fonts, curl, ca-certificates, supervisor
RUN apt-get update \
  && apt-get install -y --no-install-recommends \
     ca-certificates curl wget gnupg2 ca-certificates tzdata \
     xvfb x11vnc fluxbox x11-utils \
     fonts-noto-cjk fontconfig \
     python3 python3-pip nodejs npm \
     net-tools procps socat \
  && rm -rf /var/lib/apt/lists/*

# Install Chromium (snap not suitable in container) — use chromium-browser from apt
RUN apt-get update && apt-get install -y --no-install-recommends chromium-browser || true && rm -rf /var/lib/apt/lists/*

# Optional: install noVNC/websockify via pip for simplicity
RUN pip3 install websockify

# Create app directory
WORKDIR /opt/headful-browser-vnc
COPY . /opt/headful-browser-vnc

# Expose common ports (VNC, devtools)
EXPOSE 5900 5901 9222 6080

# Default env
ENV VNC_DISPLAY=:99 \
    VNC_RESOLUTION=1366x768 \
    REMOTE_DEBUG_PORT=9222 \
    VNC_PASSFILE=/root/.vnc/passwd \
    VNC_IMPLEMENTATION=auto

# Entrypoint: start VNC and keep container running; user overrides recommended via docker-compose
COPY docker/entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
CMD ["debug",":99","1366x768"]
```
