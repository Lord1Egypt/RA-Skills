import watch_store
from watch_store import add_rule, get_rule, list_rules, mark_seen, remove_rule


def test_watch_store_add_list_seen_remove(tmp_path, monkeypatch):
    monkeypatch.setattr(watch_store, "DB_PATH", tmp_path / "watch.db")
    rule = add_rule(
        name="semiconductor",
        raw_query="반도체 -광고",
        search_query="반도체",
        db_keyword="반도체",
        exclude_words=["광고"],
        fetch_key="반도체|광고",
        days=7,
        limit=10,
        label="반도체 감시",
        tags=["watch", "interval"],
        context="1시간마다 모니터링",
        template="watch-alert",
        schedule={"kind": "interval", "interval_minutes": 60, "label": "1시간마다"},
        operator_hints={"storage_target": "watch", "delivery_format": "watch-json"},
    )
    assert rule["name"] == "semiconductor"
    assert rule["template"] == "watch-alert"
    assert rule["schedule"]["interval_minutes"] == 60
    assert get_rule("semiconductor")["label"] == "반도체 감시"
    assert len(list_rules()) == 1
    first = mark_seen(rule["id"], [{"link": "https://example.com/a", "pub_date_iso": "2026-03-25T10:00:00+09:00"}])
    second = mark_seen(rule["id"], [{"link": "https://example.com/a", "pub_date_iso": "2026-03-25T10:00:00+09:00"}])
    assert len(first) == 1
    assert len(second) == 0
    assert remove_rule("semiconductor") == 1
