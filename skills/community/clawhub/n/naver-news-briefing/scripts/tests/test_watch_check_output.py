import naver_news_briefing as cli


class DummyArgs:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


def test_cmd_watch_check_renders_friendlier_status(monkeypatch, capsys):
    monkeypatch.setattr(cli, "get_rule", lambda name: {
        "id": 1,
        "name": name,
        "search_query": "방미심위",
        "exclude_words": [],
        "days": None,
    })

    monkeypatch.setattr(cli, "_run_rule", lambda rule: {
        "rule": rule,
        "summary": {
            "query": "방미심위",
            "total": 1068,
            "displayed": 10,
            "new_count": 2,
            "filtered_out": 0,
            "too_old": 0,
        },
        "new_items": [
            {
                "title": "새 기사 A",
                "publisher": "연합",
                "link": "https://example.com/a",
                "pub_date": "Fri, 27 Mar 2026 17:05:00 +0900",
            },
            {
                "title": "새 기사 B",
                "publisher": "뉴스1",
                "link": "https://example.com/b",
                "pub_date": "Fri, 27 Mar 2026 16:50:00 +0900",
            },
        ],
        "all_items": [
            {
                "title": "새 기사 A",
                "publisher": "연합",
                "link": "https://example.com/a",
                "pub_date_iso": "2026-03-27T17:05:00+09:00",
            }
        ],
    })

    args = DummyArgs(name_or_id="bangmisimwi", json=False)
    assert cli.cmd_watch_check(args) == 0
    out = capsys.readouterr().out
    assert "관련 상위 1건을 확인했고 이번 체크에서 신규 기사 2건이 추가됐습니다." in out
    assert "전체 검색 결과: 1068건" in out
    assert "이번 확인 신규 기사: 2건" in out
    assert "현재 검색 상위 기사 수: 1건" in out
    assert "현재 기준 최신 기사 시각: 2026-03-27T17:05:00+09:00" in out
    assert "watch: bangmisimwi 신규 기사 요약" in out
