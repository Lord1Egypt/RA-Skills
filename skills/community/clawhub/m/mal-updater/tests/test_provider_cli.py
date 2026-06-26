from __future__ import annotations

import io
import json
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

from mal_updater.cli import main


class ProviderCliTests(unittest.TestCase):
    def test_dry_run_sync_passes_provider_to_sync_planner(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / ".MAL-Updater" / "config").mkdir(parents=True)
            output = io.StringIO()
            with patch("mal_updater.cli.build_dry_run_sync_plan", return_value=[] ) as build_mock, patch.object(
                sys, "argv", [
                    "mal-updater",
                    "--project-root",
                    str(root),
                    "dry-run-sync",
                    "--provider",
                    "hidive",
                    "--limit",
                    "5",
                ]
            ), redirect_stdout(output):
                rc = main()
            self.assertEqual(0, rc)
            self.assertEqual("hidive", build_mock.call_args.kwargs["provider"])
            payload = json.loads(output.getvalue())
            self.assertEqual([], payload["proposals"])


if __name__ == "__main__":
    unittest.main()
