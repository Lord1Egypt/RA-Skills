# Container status

The old 1.0.2 reference used Ubuntu's Snap-oriented chromium-browser package,
root-oriented configuration and ignored installation failures. Its entrypoint
also sourced executable .env files and used the old positional CLI. The ClawHub
bundle omitted the entrypoint and Compose files. The legacy Docker files and
systemd templates are retired in this release because they do not implement the
new session lifecycle or its default protections.

Version 2.0.0 currently documents a Linux **host** deployment in README.md.
No Docker image or Compose deployment is claimed to be verified.

A future container image must run as non-root, preserve a working Chrome sandbox,
provide the locked npm dependencies and xauth/Xvfb/x11vnc/noVNC assets, and pass
tests/smoke_test.sh in the exact container runtime. Do not restore --no-sandbox
or privileged mode as an implicit workaround for failed sandbox initialization.
