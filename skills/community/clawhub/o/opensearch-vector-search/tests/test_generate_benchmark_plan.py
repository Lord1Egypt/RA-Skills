from __future__ import annotations

import importlib.util
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = (
    ROOT
    / "opensearch-vector-benchmark"
    / "scripts"
    / "generate_benchmark_plan.py"
)


def load_module():
    spec = importlib.util.spec_from_file_location("generate_benchmark_plan", SCRIPT)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class GenerateBenchmarkPlanTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.module = load_module()

    def parse(self, *args: str):
        return self.module.parser().parse_args(args)

    def test_managed_defaults_use_ingestion_baseline_and_dry_run(self) -> None:
        plan = self.module.build_plan(
            self.parse("--host", "example.es.amazonaws.com", "--db-label", "baseline")
        )
        self.assertEqual(plan.indexing_clients, 40)
        self.assertEqual(plan.num_per_batch, 20000)
        self.assertIn("export NUM_PER_BATCH=20000", plan.command)
        self.assertIn("--number-of-indexing-clients \\\n  40", plan.command)
        self.assertNotIn("\n+  ", plan.command)
        self.assertIn("--dry-run", plan.command)
        self.assertIn('"${OPENSEARCH_PASSWORD:?Set OPENSEARCH_PASSWORD}"', plan.command)

    def test_query_only_preserves_existing_index(self) -> None:
        plan = self.module.build_plan(
            self.parse(
                "--host",
                "example.es.amazonaws.com",
                "--db-label",
                "query",
                "--workflow",
                "query-only",
            )
        )
        self.assertIn("--skip-drop-old", plan.command)
        self.assertIn("--skip-load", plan.command)
        self.assertFalse(plan.force_merge)
        self.assertIn("--force-merge-enabled \\\n  false", plan.command)

    def test_on_disk_defaults_to_1bit_sq_baseline(self) -> None:
        plan = self.module.build_plan(
            self.parse(
                "--host",
                "example.es.amazonaws.com",
                "--db-label",
                "ondisk",
                "--on-disk",
            )
        )
        self.assertEqual(plan.ef_search, 200)
        self.assertEqual(plan.oversample_factor, 2.0)
        self.assertIn("--on-disk", plan.command)
        self.assertIn("--ef-search \\\n  200", plan.command)
        self.assertIn("--oversample-factor \\\n  2", plan.command)
        self.assertTrue(any("1-bit SQ baseline" in item for item in plan.warnings))

    def test_on_disk_preserves_explicit_query_tuning(self) -> None:
        plan = self.module.build_plan(
            self.parse(
                "--host",
                "example.es.amazonaws.com",
                "--db-label",
                "ondisk-recall",
                "--on-disk",
                "--ef-search",
                "800",
                "--oversample-factor",
                "5",
            )
        )
        self.assertEqual(plan.ef_search, 800)
        self.assertEqual(plan.oversample_factor, 5.0)
        self.assertIn("--ef-search \\\n  800", plan.command)
        self.assertIn("--oversample-factor \\\n  5", plan.command)

    def test_serverless_uses_sigv4_shape_and_one_indexing_client(self) -> None:
        plan = self.module.build_plan(
            self.parse(
                "--deployment",
                "serverless",
                "--host",
                "example.aoss.amazonaws.com",
                "--db-label",
                "aoss",
            )
        )
        self.assertEqual(plan.indexing_clients, 1)
        self.assertIsNone(plan.num_per_batch)
        self.assertIn("--serverless", plan.command)
        self.assertIn("--aws-region", plan.command)
        self.assertNotIn("OPENSEARCH_PASSWORD", plan.command)

    def test_s3vector_omits_hnsw_and_quantization_flags(self) -> None:
        plan = self.module.build_plan(
            self.parse(
                "--deployment",
                "s3vector",
                "--host",
                "example.es.amazonaws.com",
                "--db-label",
                "s3v",
            )
        )
        self.assertIn("--engine \\\n  s3vector", plan.command)
        self.assertNotIn("--ef-search", plan.command)
        self.assertNotIn("--quantization-type", plan.command)
        self.assertNotIn("--oversample-factor", plan.command)

    def test_rejects_on_disk_serverless(self) -> None:
        with self.assertRaisesRegex(ValueError, "managed"):
            self.module.build_plan(
                self.parse(
                    "--deployment",
                    "serverless",
                    "--host",
                    "example.aoss.amazonaws.com",
                    "--db-label",
                    "bad",
                    "--on-disk",
                )
            )

    def test_help_runs_without_third_party_dependencies(self) -> None:
        result = subprocess.run(
            [sys.executable, str(SCRIPT), "--help"],
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("--deployment", result.stdout)

    def test_generated_command_is_valid_bash(self) -> None:
        plan = self.module.build_plan(
            self.parse(
                "--host",
                "example.es.amazonaws.com",
                "--db-label",
                "syntax",
                "--on-disk",
            )
        )
        result = subprocess.run(
            ["bash", "-n", "-c", plan.command],
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr)


if __name__ == "__main__":
    unittest.main()
