"""
🌀 anti-loop v2.0 — Command-line interface.

Usage:
    anti-loop --demo
    anti-loop --check-plan "if X then X"
    anti-loop --stats
"""

from .core import main

__all__ = ["main"]


if __name__ == "__main__":
    main()
