from naver_api import clean_item, fetch_news


class DummyResponse:
    def __init__(self, status_code, payload):
        self.status_code = status_code
        self._payload = payload
        self.text = ""

    def json(self):
        return self._payload


class DummySession:
    def __init__(self, payload):
        self.payload = payload

    def get(self, url, *, headers, params, timeout):
        return DummyResponse(200, self.payload)


SAMPLE = {
    "total": 3,
    "items": [
        {
            "title": "<b>반도체</b> 시장 확대",
            "description": "좋은 뉴스",
            "link": "https://news.naver.com/a",
            "originallink": "https://example.com/a",
            "pubDate": "Wed, 25 Mar 2026 10:00:00 +0900",
        },
        {
            "title": "광고성 기사",
            "description": "광고 포함",
            "link": "https://example.com/b",
            "originallink": "https://example.com/b",
            "pubDate": "Wed, 25 Mar 2026 10:00:00 +0900",
        },
    ],
}


def test_clean_item_prefers_naver_link_and_strips_html():
    item = clean_item(SAMPLE["items"][0])
    assert item.title == "반도체 시장 확대"
    assert item.link == "https://news.naver.com/a"
    assert item.publisher == "example.com"


def test_fetch_news_applies_exclude_words_and_limit():
    result = fetch_news(
        client_id="id",
        client_secret="secret",
        search_query="반도체",
        exclude_words=["광고"],
        limit=5,
        timeout=5,
        session=DummySession(SAMPLE),
    )
    assert result["displayed"] == 1
    assert result["filtered_out"] == 1
    assert result["items"][0]["title"] == "반도체 시장 확대"
