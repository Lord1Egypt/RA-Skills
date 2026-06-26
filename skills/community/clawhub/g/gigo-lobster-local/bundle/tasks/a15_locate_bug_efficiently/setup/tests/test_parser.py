from src.parser import parse


def test_parse_returns_int():
    assert parse("42") == 42
    assert isinstance(parse("7"), int)
