import pytest

from scripts.input_parser import (
    InputTooLargeError,
    InputTooShortError,
    UnsupportedFormatError,
    detect_input_type,
    parse_resume,
    validate_jd,
)


def test_detect_text():
    assert detect_input_type(jd_text="some long jd text " * 20) == "text"


def test_detect_url():
    assert detect_input_type(jd_url="https://zhipin.com/job/123") == "url"


def test_detect_file():
    assert detect_input_type(jd_file="job.txt") == "file"


def test_detect_none_raises():
    with pytest.raises(ValueError):
        detect_input_type()


def test_detect_multiple_raises():
    with pytest.raises(ValueError):
        detect_input_type(jd_text="x", jd_url="https://y.com")


def test_validate_too_short():
    with pytest.raises(InputTooShortError):
        validate_jd("short")


def test_validate_too_long():
    with pytest.raises(InputTooLargeError):
        validate_jd("x" * 50001)


def test_validate_ok():
    text = "valid jd " * 50
    assert validate_jd(text) == text


def test_parse_resume_text_passthrough():
    text = "name: zhangsan\nskills: react"
    assert parse_resume(text) == text


def test_parse_resume_truncates():
    long_text = "x" * 25000
    result = parse_resume(long_text)
    assert len(result) <= 20000
