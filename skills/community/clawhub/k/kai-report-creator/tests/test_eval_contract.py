import csv
import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "scripts" / "run-report-evals.py"
MANIFEST = ROOT / "evals" / "report-cases.csv"
RUBRIC_SCHEMA = ROOT / "evals" / "rubric.schema.json"
FAILURE_MAP = ROOT / "evals" / "failure-map.md"


def load_manifest() -> list[dict[str, str]]:
    with MANIFEST.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def test_eval_artifacts_exist():
    assert SCRIPT.exists()
    assert MANIFEST.exists()
    assert RUBRIC_SCHEMA.exists()
    assert FAILURE_MAP.exists()


def test_manifest_paths_resolve():
    rows = load_manifest()
    assert len(rows) >= 3
    for row in rows:
        assert row["case_id"]
        assert (ROOT / row["source_path"]).exists(), row
        assert (ROOT / row["ir_path"]).exists(), row
        assert (ROOT / row["html_path"]).exists(), row


def test_rubric_schema_has_expected_layers():
    schema = json.loads(RUBRIC_SCHEMA.read_text(encoding="utf-8"))
    scores = schema["properties"]["scores"]["properties"]
    assert sorted(scores.keys()) == [
        "async_readability",
        "compression",
        "ir_contract",
        "render_integrity",
    ]


def test_eval_runner_passes_for_repo_cases(tmp_path: Path):
    json_out = tmp_path / "report-evals.json"
    packet_dir = tmp_path / "packets"
    result = subprocess.run(
        [
            sys.executable,
            str(SCRIPT),
            "--root",
            str(ROOT),
            "--format",
            "json",
            "--json-out",
            str(json_out),
            "--packet-dir",
            str(packet_dir),
        ],
        capture_output=True,
        text=True,
        timeout=20,
    )
    assert result.returncode == 0, result.stdout + result.stderr

    payload = json.loads(result.stdout)
    assert payload["summary"]["total"] >= 3
    assert payload["summary"]["failed"] == 0
    assert payload["summary"]["rubric_ready"] == payload["summary"]["total"]
    assert json.loads(json_out.read_text(encoding="utf-8"))["summary"]["failed"] == 0

    packet_files = sorted(packet_dir.glob("*.json"))
    assert len(packet_files) == payload["summary"]["total"]
    packet = json.loads(packet_files[0].read_text(encoding="utf-8"))
    assert packet["rubric_schema"] == "evals/rubric.schema.json"
    assert packet["headings"]
