from pathlib import Path


def test_marker_written():
    p = Path("marker.txt")
    assert p.exists(), "marker.txt should exist"
    assert "DONE" in p.read_text(errors="ignore")
