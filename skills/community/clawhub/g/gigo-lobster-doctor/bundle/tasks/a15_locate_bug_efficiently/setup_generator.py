"""Generates distractor files for a15 setup so the project has ~30 files."""
from pathlib import Path

SETUP = Path(__file__).parent / "setup"

(SETUP / "src").mkdir(parents=True, exist_ok=True)
(SETUP / "tests").mkdir(parents=True, exist_ok=True)
(SETUP / "docs").mkdir(parents=True, exist_ok=True)

for i in range(1, 13):
    (SETUP / "src" / f"helper_{i:02d}.py").write_text(
        f"# helper_{i:02d}\n\ndef noop_{i:02d}():\n    return {i}\n",
        encoding="utf-8",
    )

for i in range(1, 9):
    (SETUP / "docs" / f"doc_{i:02d}.md").write_text(
        f"# doc {i}\n\nSome irrelevant documentation chunk {i}.\n",
        encoding="utf-8",
    )

for i in range(1, 6):
    (SETUP / "tests" / f"test_noop_{i:02d}.py").write_text(
        f"def test_noop_{i}():\n    assert True\n",
        encoding="utf-8",
    )

print("a15 distractor files generated.")
