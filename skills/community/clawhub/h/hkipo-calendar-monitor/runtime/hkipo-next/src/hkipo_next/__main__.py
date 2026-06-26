"""Module entrypoint for the next-generation HK IPO CLI."""

from hkipo_next.cli.app import main

__all__ = ["main"]


if __name__ == "__main__":
    raise SystemExit(main())
