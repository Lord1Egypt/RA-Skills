import json
import subprocess
import sys
from pathlib import Path


def test_basic_convert(tmp_path):
    csv = tmp_path / "in.csv"
    csv.write_text("a,b\n1,2\n3,4\n", encoding="utf-8")
    out = tmp_path / "out.json"
    subprocess.run([sys.executable, "convert.py", str(csv), str(out)],
                   cwd=Path(__file__).parent.parent, check=True)
    data = json.loads(out.read_text())
    assert data == [{"a": "1", "b": "2"}, {"a": "3", "b": "4"}]


def test_with_header():
    out = Path(__file__).parent.parent / "output.json"
    subprocess.run([sys.executable, "convert.py", "input.csv", "output.json"],
                   cwd=Path(__file__).parent.parent, check=True)
    data = json.loads(out.read_text())
    assert data[0]["name"] == "张三"
    assert len(data) == 2
