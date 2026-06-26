"""
infinity-router — unlimited free AI routing via OpenRouter.

Package layout
--------------
models.py   Model registry: fetch, score, cache, rate-limit state
probe.py    HTTP health check and latency measurement
targets.py  Config-target writers: OpenClaw, Claude Code
cli.py      `infinity-router` CLI entry point
daemon.py   `infinity-router-daemon` entry point
"""

__version__ = "2.1.0"
