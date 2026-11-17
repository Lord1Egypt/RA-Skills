# syntax=docker/dockerfile:1
#
# Build context is the repository root:
#   docker build -f containers/Dockerfile .
#
# One definition, four variants. The two "missing dependency" axes are
# independent, so they are build arguments rather than a stage chain: a linear
# chain cannot express "handoff deps without runtime" and "runtime without
# handoff deps" at the same time. A change to the base reaches every variant.

FROM debian:bookworm-slim AS base

ARG TARGETARCH
ENV LINE_OA_CONTAINER_BUILD_ARCH="${TARGETARCH}"
ENV DEBIAN_FRONTEND=noninteractive

# Common to every variant. python3 stays in the base because the handoff script
# uses it to pick free loopback ports; the "runtime" axis below is specifically
# a Python environment containing Playwright. Chromium comes from the
# distribution rather than a Playwright managed download, because Playwright
# does not cover linux-arm64 uniformly.
RUN apt-get update && apt-get install -y --no-install-recommends \
      ca-certificates \
      curl \
      gnupg \
      procps \
      python3 \
      chromium \
      chromium-sandbox \
    && rm -rf /var/lib/apt/lists/*

# Runtime/cache data. Deliberately outside the read-only source mount and
# outside the browser profile.
ENV LINE_OA_SEND_CHAT_RUNTIME_DIR=/opt/line-oa-runtime
ENV LINE_OA_SEND_CHAT_CHROMIUM_PROFILE=/opt/data/chromium
ENV LINE_OA_CHROMIUM=/usr/bin/chromium

# Chromium refuses to run as root without its sandbox disabled. Rather than
# teach the scripts a container-only flag, the image runs them as an
# unprivileged user -- which is also how the scripts are meant to run in
# production, under a service identity that owns the profile.
RUN useradd --create-home --uid 1000 --shell /bin/bash lineoa

# Both directories are created here, before the VOLUME declaration, so the
# volume inherits an owner the unprivileged user can write to.
RUN mkdir -p "$LINE_OA_SEND_CHAT_RUNTIME_DIR" "$LINE_OA_SEND_CHAT_CHROMIUM_PROFILE" \
    && chmod 700 "$LINE_OA_SEND_CHAT_RUNTIME_DIR" "$LINE_OA_SEND_CHAT_CHROMIUM_PROFILE" \
    && chown lineoa:lineoa "$LINE_OA_SEND_CHAT_RUNTIME_DIR" "$LINE_OA_SEND_CHAT_CHROMIUM_PROFILE"

COPY containers/entrypoint.sh /usr/local/bin/line-oa-entrypoint
RUN chmod 755 /usr/local/bin/line-oa-entrypoint


FROM base AS variant

# 1 = present, 0 = absent. Defaults describe the "full" variant.
ARG WITH_HANDOFF_DEPS=1
ARG WITH_RUNTIME=1
ARG WITH_PROFILE=0

# Handoff dependencies. cloudflared is not in the Debian repositories, so it
# comes from Cloudflare's signed apt repository -- the same sequence
# start_line_oa_vnc_handoff.sh already prints when it finds the command missing.
RUN if [ "$WITH_HANDOFF_DEPS" = "1" ]; then \
      set -eux; \
      apt-get update; \
      apt-get install -y --no-install-recommends \
        xvfb x11vnc novnc websockify caddy; \
      curl -fsSL https://pkg.cloudflare.com/cloudflare-main.gpg \
        -o /usr/share/keyrings/cloudflare-main.gpg; \
      printf 'deb [signed-by=/usr/share/keyrings/cloudflare-main.gpg] https://pkg.cloudflare.com/cloudflared any main\n' \
        > /etc/apt/sources.list.d/cloudflared.list; \
      apt-get update; \
      apt-get install -y --no-install-recommends cloudflared; \
      rm -rf /var/lib/apt/lists/*; \
    fi

# The Python/Playwright runtime, provisioned by the repository's own setup
# script through its --skip-browser-install path. uv is installed only inside
# this branch on purpose: run_line_oa_chat.sh falls back to
# `uv run --with playwright`, so leaving uv in the no-runtime variant would let
# it silently succeed and the variant would prove nothing.
COPY --from=ghcr.io/astral-sh/uv:0.9.7 /uv /tmp/uv
COPY scripts/setup_line_oa_runtime.sh /tmp/setup_line_oa_runtime.sh
RUN if [ "$WITH_RUNTIME" = "1" ]; then \
      set -eux; \
      install -m 755 /tmp/uv /usr/local/bin/uv; \
      bash /tmp/setup_line_oa_runtime.sh \
        --runtime-dir "$LINE_OA_SEND_CHAT_RUNTIME_DIR" \
        --skip-browser-install; \
      chown -R lineoa:lineoa "$LINE_OA_SEND_CHAT_RUNTIME_DIR"; \
    fi; \
    rm -f /tmp/uv /tmp/setup_line_oa_runtime.sh

# Present but unauthenticated profile. An empty directory would make this
# variant identical to "full", so Chromium is run once to materialize a real
# profile: initialized, previously used, and holding no LINE session. Seeded
# before the VOLUME declaration so it reaches the volume on first run.
# --no-sandbox appears here and nowhere else. BuildKit cannot take the
# --security-opt that lets Chromium build its namespace sandbox, and this run is
# only seeding profile bytes -- it is not the code under test, and the resulting
# profile is byte-identical either way. The scripts themselves never see it.
RUN if [ "$WITH_PROFILE" = "1" ]; then \
      set -eux; \
      runuser -u lineoa -- chromium \
        --headless \
        --no-sandbox \
        --no-first-run \
        --no-default-browser-check \
        --user-data-dir="$LINE_OA_SEND_CHAT_CHROMIUM_PROFILE" \
        --dump-dom about:blank > /dev/null; \
      test -e "$LINE_OA_SEND_CHAT_CHROMIUM_PROFILE/Default"; \
    fi

# The profile is I/O heavy, so it lives on container-native storage rather than
# a host bind mount. Declaring it here means that holds even when the run
# command forgets to name a volume.
VOLUME ["/opt/data/chromium"]

# Sources are mounted read-only at run time; nothing is copied in.
WORKDIR /workspace
USER lineoa

ENTRYPOINT ["/usr/local/bin/line-oa-entrypoint"]
CMD ["bash"]
