#!/usr/bin/env python3
"""
Health Coach Web Dashboard Server v3 - Modular Design
"""

import argparse
import os
import sys

from flask import Flask, render_template

# Add web module to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from web import TEMPLATE_VERSION, SKILL_DIR, register_routes

app = Flask(__name__,
            template_folder=os.path.join(SKILL_DIR, 'templates'),
            static_folder=os.path.join(SKILL_DIR, 'scripts', 'web', 'static'))

CURRENT_USER = None


def get_current_user():
    return CURRENT_USER


@app.route('/')
def dashboard():
    return render_template('dashboard.html', user=CURRENT_USER)


def main():
    global CURRENT_USER

    parser = argparse.ArgumentParser(description='Health Coach Web Dashboard v3')
    parser.add_argument('--user', required=True, help='Username')
    parser.add_argument('--port', type=int, default=8080, help='Port (default: 8080)')
    args = parser.parse_args()

    CURRENT_USER = args.user

    # Register API routes
    register_routes(app, get_current_user)

    print(f"🌐 Health Coach Dashboard v3 (Template: {TEMPLATE_VERSION})")
    print(f"   User: {CURRENT_USER}")
    print(f"   URL: http://localhost:{args.port}")
    print(f"   Press Ctrl+C to stop\n")

    try:
        app.run(host='0.0.0.0', port=args.port, debug=False)
    except KeyboardInterrupt:
        print("\n✓ Server stopped")
        sys.exit(0)


if __name__ == '__main__':
    main()
