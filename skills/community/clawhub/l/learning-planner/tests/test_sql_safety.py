from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_days_are_parameterized():
    for rel in ["src/learning_database/cards.py", "src/learning_database/sessions.py"]:
        source = (ROOT / rel).read_text()
        assert ".format(days)" not in source
        assert "-{} days" not in source
        assert "def _days_modifier" in source


if __name__ == "__main__":
    test_days_are_parameterized()
    print("passed")
