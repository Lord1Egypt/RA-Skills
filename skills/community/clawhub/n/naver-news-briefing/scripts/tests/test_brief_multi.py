import json

import naver_news_briefing as cli
from briefing_templates import build_combined_payload, render_combined_text


class DummyArgs:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


def test_build_combined_payload_and_render_text():
    payload = build_combined_payload(
        [
            {
                "query": "반도체 뉴스",
                "group_name": "market-watch",
                "label": "시장",
                "context": "아침 브리핑",
                "result": {
                    "displayed": 1,
                    "total": 10,
                    "filtered_out": 0,
                    "too_old": 0,
                    "items": [{"title": "반도체 상승", "publisher": "연합", "link": "https://example.com/a"}],
                },
            }
        ],
        template="analyst",
        source_groups=[{"name": "market-watch"}],
    )
    text = render_combined_text(payload)
    assert "네이버 뉴스 멀티 브리핑 · analyst" in text
    assert "market-watch" in text
    assert "반도체 상승" in text


def test_cmd_brief_multi_supports_group_and_query_json(monkeypatch, capsys):
    monkeypatch.setattr(cli, "get_group", lambda name: {
        "name": name,
        "label": "관심주제",
        "tags": ["태그"],
        "context": "체크 포인트",
        "queries": ["반도체 -광고"],
    })

    def fake_run_query_entry(query, *, limit, days, group=None, label=None, context=None):
        return {
            "query": query,
            "group_name": group["name"] if group else None,
            "label": label or (group.get("label") if group else None),
            "context": context or (group.get("context") if group else None),
            "result": {
                "displayed": 1,
                "total": 3,
                "filtered_out": 0,
                "too_old": 0,
                "items": [{"title": f"{query} 기사", "publisher": "연합", "link": "https://example.com/x"}],
            },
        }

    monkeypatch.setattr(cli, "_run_query_entry", fake_run_query_entry)
    args = DummyArgs(group=["market-watch"], query=["환율 뉴스"], limit=5, days=None, template="morning-briefing", json=True)
    assert cli.cmd_brief_multi(args) == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["template"] == "morning-briefing"
    assert payload["entry_count"] == 2
    assert payload["groups"][0]["name"] == "market-watch"


def test_main_brief_multi_missing_group_is_operator_friendly(monkeypatch, capsys):
    monkeypatch.setattr(cli, "get_group", lambda name: (_ for _ in ()).throw(KeyError(f"keyword group not found: {name}")))
    monkeypatch.setattr(cli, "list_groups", lambda: [{"name": "market-watch"}])
    exit_code = cli.main(["brief-multi", "--group", "missing-group"])
    captured = capsys.readouterr()
    assert exit_code == 1
    assert "등록된 키워드 그룹을(를) 찾지 못했습니다: missing-group" in captured.err
    assert "market-watch" in captured.err
