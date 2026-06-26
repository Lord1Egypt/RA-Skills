import group_store
from group_store import create_group, get_group, list_groups, remove_group, update_group


def test_group_store_create_update_remove(tmp_path, monkeypatch):
    monkeypatch.setattr(group_store, "DB_PATH", tmp_path / "watch.db")
    group = create_group(
        name="market-watch",
        queries=["반도체 -광고", "AI 데이터센터 -주가"],
        label="시장 모니터링",
        tags=["시장", "테크", "시장"],
        context="아침 브리핑용",
        template="morning-briefing",
        schedule={"kind": "daily", "label": "매일 07:00", "time": "07:00"},
        operator_hints={"storage_target": "group"},
    )
    assert group["query_count"] == 2
    assert group["tags"] == ["시장", "테크"]
    assert group["template"] == "morning-briefing"
    assert group["schedule"]["time"] == "07:00"
    assert len(list_groups()) == 1

    updated = update_group(
        "market-watch",
        add_queries=["배터리 공급망 -광고"],
        remove_queries=["AI 데이터센터 -주가"],
        tags=["시장", "모니터링"],
        template="analyst",
    )
    assert updated["queries"] == ["반도체 -광고", "배터리 공급망 -광고"]
    assert updated["tags"] == ["시장", "모니터링"]
    assert updated["template"] == "analyst"
    assert get_group("market-watch")["query_count"] == 2
    assert remove_group("market-watch") == 1
