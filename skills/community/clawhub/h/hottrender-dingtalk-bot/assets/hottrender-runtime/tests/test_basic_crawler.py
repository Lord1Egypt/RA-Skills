from src.crawler import fetch_daily_trends, fetch_keyword_hotspots, render_markdown


def test_fetch_daily_trends_offline(tmp_path):
    config = tmp_path / "providers.yaml"
    config.write_text(
        """
google:
  mode: offline
youtube:
  mode: offline
""",
        encoding="utf-8",
    )

    payload = fetch_daily_trends(
        regions=["jp", "us"],
        platforms=["google", "youtube"],
        limit=2,
        config_path=config,
    )

    assert payload["mode"] == "daily"
    assert len(payload["items"]) == 8
    assert payload["errors"] == {}
    assert "四地区每日热点趋势" in render_markdown(payload)


def test_fetch_keyword_hotspots_offline(tmp_path):
    config = tmp_path / "providers.yaml"
    config.write_text(
        """
google:
  mode: offline
""",
        encoding="utf-8",
    )

    payload = fetch_keyword_hotspots(
        keywords=["乙游", "短剧"],
        regions=["jp"],
        platforms=["google"],
        limit=2,
        config_path=config,
    )

    assert payload["mode"] == "keyword"
    assert len(payload["items"]) == 4
    assert {item["keyword"] for item in payload["items"]} == {"乙游", "短剧"}
    assert "垂类关键词热点" in render_markdown(payload)
