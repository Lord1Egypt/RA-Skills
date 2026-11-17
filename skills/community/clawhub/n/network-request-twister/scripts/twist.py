#!/usr/bin/env python3
"""Entry point for twist — CDP network interceptor.

Usage:
    python twist.py --launch -c rules.json -u https://example.com
    python twist.py --list-targets
"""

from twist.cli import main

if __name__ == "__main__":
    main()
