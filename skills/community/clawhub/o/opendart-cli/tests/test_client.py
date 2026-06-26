import io
import json
import zipfile
from pathlib import Path

import pytest
import responses

from opendart_cli.client import OpenDartClient, OpenDartError


@pytest.fixture
def client(tmp_path, monkeypatch):
    monkeypatch.setenv("OPENDART_API_KEY", "x" * 40)
    return OpenDartClient(cache_dir=tmp_path)


@responses.activate
def test_company_success(client):
    responses.add(
        responses.GET,
        "https://opendart.fss.or.kr/api/company.json",
        json={"status": "000", "message": "정상", "corp_name": "삼성전자"},
    )
    out = client.company("00126380")
    assert out["corp_name"] == "삼성전자"


@responses.activate
def test_auth_error(client):
    responses.add(
        responses.GET,
        "https://opendart.fss.or.kr/api/company.json",
        json={"status": "010", "message": "키가 등록되지 않았습니다."},
    )
    with pytest.raises(OpenDartError) as exc:
        client.company("00126380")
    assert exc.value.status == "010"


@responses.activate
def test_corp_code_refresh(client, tmp_path):
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, mode="w") as zf:
        zf.writestr(
            "CORPCODE.xml",
            """<?xml version=\"1.0\" encoding=\"UTF-8\"?>
<result>
  <list>
    <corp_code>00126380</corp_code>
    <corp_name>삼성전자</corp_name>
    <stock_code>005930</stock_code>
    <modify_date>20260101</modify_date>
  </list>
  <list>
    <corp_code>00258801</corp_code>
    <corp_name>카카오</corp_name>
    <stock_code>035720</stock_code>
    <modify_date>20260101</modify_date>
  </list>
</result>
""",
        )
    responses.add(
        responses.GET,
        "https://opendart.fss.or.kr/api/corpCode.xml",
        body=buf.getvalue(),
        content_type="application/octet-stream",
    )
    rows = client.refresh_corp_codes()
    assert len(rows) == 2
    cached = json.loads(client.corp_code_cache_path().read_text(encoding="utf-8"))
    assert cached[0]["corp_name"] == "삼성전자"

    matches = client.find_corp("카카오")
    assert matches and matches[0]["corp_code"] == "00258801"

    matches_by_stock = client.find_corp("005930")
    assert matches_by_stock and matches_by_stock[0]["corp_name"] == "삼성전자"


def test_missing_key(monkeypatch, tmp_path):
    monkeypatch.delenv("OPENDART_API_KEY", raising=False)
    with pytest.raises(OpenDartError):
        OpenDartClient(cache_dir=tmp_path)
