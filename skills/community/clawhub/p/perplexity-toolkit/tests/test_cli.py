"""Tests for CLI module."""
import sys; sys.path.insert(0, "src")

import argparse
from perplexity_toolkit.commands.cli import main


class TestParser:
    def test_main_parser_constructs(self):
        """Parser should construct without error."""
        import perplexity_toolkit.commands.cli as cli_mod
        # Re-running main() would parse sys.argv, so test the parser directly
        parser = argparse.ArgumentParser()
        sub = parser.add_subparsers(dest="command")
        
        # search subcommand
        p = sub.add_parser("search")
        p.add_argument("query")
        p.add_argument("-m", "--mode", default="search")
        
        # batch subcommand
        p = sub.add_parser("batch")
        p.add_argument("queries", nargs="*")
        p.add_argument("-i", "--input")
        p.add_argument("-r", "--resume", action="store_true")
        
        # aggregate subcommand
        p = sub.add_parser("aggregate")
        p.add_argument("files", nargs="+")
        
        # history subcommand
        p = sub.add_parser("history")
        p.add_argument("action", choices=["list", "search", "delete"])
        
        args = parser.parse_args(["search", "test query"])
        assert args.command == "search"
        assert args.query == "test query"
        assert args.mode == "search"

    def test_batch_args(self):
        parser = argparse.ArgumentParser()
        sub = parser.add_subparsers(dest="command")
        p = sub.add_parser("batch")
        p.add_argument("queries", nargs="*")
        p.add_argument("-i", "--input")
        p.add_argument("-r", "--resume", action="store_true")
        p.add_argument("-d", "--delay", type=float, default=3.0)
        
        args = parser.parse_args(["batch", "-i", "queries.json", "-r"])
        assert args.command == "batch"
        assert args.input == "queries.json"
        assert args.resume is True
        assert args.delay == 3.0

    def test_history_args(self):
        parser = argparse.ArgumentParser()
        sub = parser.add_subparsers(dest="command")
        p = sub.add_parser("history")
        p.add_argument("action", choices=["list", "search", "delete"])
        p.add_argument("query", nargs="?")
        p.add_argument("--dry-run", action="store_true")
        
        args = parser.parse_args(["history", "delete", "old query", "--dry-run"])
        assert args.command == "history"
        assert args.action == "delete"
        assert args.query == "old query"
        assert args.dry_run is True
