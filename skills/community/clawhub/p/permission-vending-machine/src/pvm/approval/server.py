"""
Approval HTTP server — Flask app for handling Discord/email approval callbacks.

Run as: pvm serve [--port 8080]

Sets up two endpoints:
  GET  /                 — Approval status dashboard
  POST /approve/<token>  — Approve a request by token
  POST /deny/<token>     — Deny a request by token

The PVM Discord notification embeds include links to these endpoints so Tyler
can approve/deny by clicking links in the notification.
"""

from __future__ import annotations

import argparse
import logging
from typing import Callable, Optional

from flask import Flask, jsonify, request as flask_request

logger = logging.getLogger(__name__)


def create_app(
    on_approve: Callable[[str, str], None],  # (token, approver)
    on_deny: Callable[[str, str], None],      # (token, approver)
    approver_name: str = "Tyler",
) -> Flask:
    """
    Build the Flask approval server.

    `on_approve(token, approver)` is called when /approve/<token> is hit.
    `on_deny(token, approver)` is called when /deny/<token> is hit.
    """
    app = Flask(__name__)
    app.config["JSON_SORT_KEYS"] = False

    _on_approve = on_approve
    _on_deny = on_deny
    _approver = approver_name

    @app.route("/")
    def index():
        return """
        <!DOCTYPE html>
        <html>
        <head>
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <title>PVM — Permission Vending Machine</title>
            <style>
                body { font-family: -apple-system, BlinkMacSystemFont, sans-serif;
                       background: #0f172a; color: #e2e8f0; margin: 0;
                       min-height: 100vh; display: flex; align-items: center; justify-content: center; }
                .card { background: #1e293b; padding: 48px 64px; border-radius: 16px;
                        max-width: 500px; box-shadow: 0 20px 60px rgba(0,0,0,0.4); }
                h1 { color: #f8fafc; margin: 0 0 8px; font-size: 28px; }
                .subtitle { color: #94a3b8; margin: 0 0 32px; font-size: 16px; }
                .status { background: #065f46; color: #6ee7b7; padding: 12px 20px;
                          border-radius: 8px; font-weight: bold; margin-bottom: 32px;
                          display: inline-block; }
                h3 { color: #94a3b8; font-size: 13px; text-transform: uppercase;
                     letter-spacing: 1px; margin: 24px 0 12px; }
                code { background: #334155; padding: 4px 10px; border-radius: 6px;
                       font-size: 14px; color: #7dd3fc; display: block; margin-bottom: 8px; }
            </style>
        </head>
        <body>
            <div class="card">
                <h1>🤖 PVM</h1>
                <p class="subtitle">Permission Vending Machine — Approval Server</p>
                <span class="status">● Running</span>
                <h3>How to approve</h3>
                <code>GET /approve/&lt;token&gt;</code>
                <code>GET /deny/&lt;token&gt;</code>
                <h3>Also works</h3>
                <code>Reply APPROVE &lt;token&gt; via iMessage or email</code>
            </div>
        </body>
        </html>
        """

    @app.route("/approve/<token>", methods=["GET", "POST"])
    def approve(token: str):
        logger.info("APPROVE received via HTTP: token=%s", token)
        try:
            _on_approve(token, _approver)
            return f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta name="viewport" content="width=device-width, initial-scale=1">
                <title>✅ Approved — PVM</title>
                <style>
                    body {{ font-family: -apple-system, BlinkMacSystemFont, sans-serif;
                           display: flex; align-items: center; justify-content: center;
                           min-height: 100vh; margin: 0; background: #1a1a2e; }}
                    .card {{ background: #16213e; color: #e2e8f0; padding: 48px 64px;
                            border-radius: 16px; text-align: center; box-shadow: 0 20px 60px rgba(0,0,0,0.5); }}
                    .emoji {{ font-size: 72px; margin-bottom: 16px; }}
                    h1 {{ color: #34d399; margin: 0 0 12px; font-size: 32px; }}
                    p {{ color: #94a3b8; margin: 0 0 24px; font-size: 18px; }}
                    .token {{ font-family: monospace; background: #0f3460;
                             padding: 8px 16px; border-radius: 8px; color: #60a5fa;
                             font-size: 14px; display: inline-block; margin-bottom: 24px; }}
                    .btn {{ background: #34d399; color: #065f46; padding: 14px 32px;
                            border-radius: 8px; text-decoration: none; font-weight: bold;
                            font-size: 16px; display: inline-block; }}
                </style>
            </head>
            <body>
                <div class="card">
                    <div class="emoji">✅</div>
                    <h1>Approved!</h1>
                    <p>The agent can now proceed with the requested operation.</p>
                    <div class="token">{token}</div><br>
                    <a href="/" class="btn">Back to PVM</a>
                </div>
            </body>
            </html>
            """
        except Exception as exc:
            logger.exception("Approve failed for token %s", token)
            return jsonify({"status": "error", "message": str(exc)}), 500

    @app.route("/deny/<token>", methods=["GET", "POST"])
    def deny(token: str):
        logger.info("DENY received via HTTP: token=%s", token)
        try:
            _on_deny(token, _approver)
            return f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta name="viewport" content="width=device-width, initial-scale=1">
                <title>❌ Denied — PVM</title>
                <style>
                    body {{ font-family: -apple-system, BlinkMacSystemFont, sans-serif;
                           display: flex; align-items: center; justify-content: center;
                           min-height: 100vh; margin: 0; background: #1a1a2e; }}
                    .card {{ background: #16213e; color: #e2e8f0; padding: 48px 64px;
                            border-radius: 16px; text-align: center; box-shadow: 0 20px 60px rgba(0,0,0,0.5); }}
                    .emoji {{ font-size: 72px; margin-bottom: 16px; }}
                    h1 {{ color: #f87171; margin: 0 0 12px; font-size: 32px; }}
                    p {{ color: #94a3b8; margin: 0 0 24px; font-size: 18px; }}
                    .token {{ font-family: monospace; background: #0f3460;
                             padding: 8px 16px; border-radius: 8px; color: #60a5fa;
                             font-size: 14px; display: inline-block; margin-bottom: 24px; }}
                    .btn {{ background: #475569; color: #e2e8f0; padding: 14px 32px;
                            border-radius: 8px; text-decoration: none; font-weight: bold;
                            font-size: 16px; display: inline-block; }}
                </style>
            </head>
            <body>
                <div class="card">
                    <div class="emoji">❌</div>
                    <h1>Denied</h1>
                    <p>The agent has been notified. The request was denied.</p>
                    <div class="token">{token}</div><br>
                    <a href="/" class="btn">Back to PVM</a>
                </div>
            </body>
            </html>
            """
        except Exception as exc:
            logger.exception("Deny failed for token %s", token)
            return jsonify({"status": "error", "message": str(exc)}), 500

    @app.route("/health")
    def health():
        return jsonify({"status": "ok"})

    return app


def run_server(
    on_approve: Callable[[str, str], None],
    on_deny: Callable[[str, str], None],
    host: str = "0.0.0.0",
    port: int = 7823,
    approver_name: str = "Tyler",
    debug: bool = False,
) -> None:
    """Run the approval server. Blocks indefinitely."""
    app = create_app(on_approve=on_approve, on_deny=on_deny, approver_name=approver_name)
    # Bind to all interfaces so Tyler can hit it from his phone on LAN
    app.run(host=host, port=port, debug=debug)
