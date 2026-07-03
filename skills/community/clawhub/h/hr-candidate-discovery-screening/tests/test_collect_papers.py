from __future__ import annotations

import json
from dataclasses import replace
from datetime import date
from pathlib import Path

import pytest
import requests

from collect_papers import (
    ACLXMLCollector,
    CrossrefCollector,
    OpenAlexCollector,
    OpenReviewCollector,
    OfficialHTMLCollector,
    coerce_config_date,
    deduplicate_works,
    extract_official_detail_links,
    normalize_acl_xml,
    normalize_citation_detail,
    normalize_openreview_note,
    normalize_openalex_works,
    parse_date_range,
    reconstruct_abstract,
)
from models import PaperRecord


FIXTURES = Path(__file__).parent / "fixtures"


@pytest.fixture
def fixture_works():
    return json.loads((FIXTURES / "openalex_works.json").read_text(encoding="utf-8"))


def test_reconstructs_openalex_abstract():
    assert reconstruct_abstract({"vision": [0], "language": [1], "model": [2]}) == (
        "vision language model"
    )
    assert reconstruct_abstract(None) is None


def test_keeps_closed_date_bounds_and_rejects_retracted_or_preprint(fixture_works):
    source = {
        "key": "mixed-fixture",
        "official_domains": ["openaccess.thecvf.com", "jmlr.org"],
    }

    works = normalize_openalex_works(
        fixture_works,
        source=source,
        start_date=date(2025, 6, 11),
        end_date=date(2026, 6, 11),
    )

    assert [work.title for work in works] == ["Boundary Paper", "Accepted Paper"]
    assert works[0].abstract == "vision language model"
    assert works[0].doi == "10.1000/boundary"
    assert works[0].original_keywords == ("Vision-language model",)


def test_deduplicates_by_doi_then_source_id_then_title():
    base = PaperRecord(
        source_key="cvpr",
        source_type="conference",
        source_record_id="W1",
        doi="10.1000/test",
        title="A Test Paper",
        normalized_title="a test paper",
        publication_date=date(2026, 1, 1),
    )
    records = [
        base,
        replace(base, source_record_id="W2"),
        replace(base, doi=None, source_record_id="W1"),
        replace(base, doi=None, source_record_id="W3"),
    ]

    unique = deduplicate_works(records)

    assert len(unique) == 1
    assert unique[0].doi == "10.1000/test"


def test_parse_date_range_requires_both_dates_and_valid_order():
    with pytest.raises(ValueError, match="start_date"):
        parse_date_range(None, "2026-06-11")
    with pytest.raises(ValueError, match="must not be after"):
        parse_date_range("2026-06-12", "2026-06-11")

    assert parse_date_range("2025-06-11", "2026-06-11") == (
        date(2025, 6, 11),
        date(2026, 6, 11),
    )


class FakeResponse:
    def __init__(self, payload):
        self.payload = payload

    def raise_for_status(self):
        return None

    def json(self):
        return self.payload


class FakeHttp:
    def __init__(self, responses):
        self.responses = list(responses)
        self.calls = []

    def get(self, url, **kwargs):
        self.calls.append((url, kwargs))
        response = self.responses.pop(0)
        if isinstance(response, Exception):
            raise response
        return FakeResponse(response)


def test_openalex_collector_persists_cursor_before_retryable_failure(
    initialized_database, fixture_works
):
    first_page = {
        "meta": {"next_cursor": "cursor-2"},
        "results": [fixture_works["results"][0]],
    }
    http = FakeHttp(
        [
            {
                "results": [
                    {
                        "id": "https://openalex.org/S1",
                        "display_name": "Proceedings of CVPR",
                    }
                ]
            },
            first_page,
            requests.ConnectionError("temporary failure"),
        ]
    )
    source = {
        "key": "cvpr",
        "name": "IEEE/CVF Conference on Computer Vision and Pattern Recognition",
        "aliases": ["CVPR"],
        "official_domains": ["openaccess.thecvf.com"],
    }

    collector = OpenAlexCollector(http=http, database=initialized_database)
    with pytest.raises(requests.ConnectionError):
        collector.collect(source, date(2025, 6, 11), date(2026, 6, 11))

    assert initialized_database.get_source_checkpoint(
        "cvpr", "2025-06-11", "2026-06-11"
    ) == "cursor-2"
    assert initialized_database.status()["papers"] == 1


def test_crossref_collector_normalizes_and_saves_journal_record(
    initialized_database,
):
    http = FakeHttp(
        [
            {
                "message": {
                    "next-cursor": "",
                    "items": [
                        {
                            "DOI": "10.5555/JMLR.TEST",
                            "title": ["A Journal Result"],
                            "abstract": "<jats:p>Useful abstract.</jats:p>",
                            "published-online": {"date-parts": [[2026, 6, 1]]},
                            "URL": "https://jmlr.org/papers/v27/test.html",
                            "author": [
                                {
                                    "given": "Ming",
                                    "family": "Li",
                                    "ORCID": "https://orcid.org/0000-0001-0000-0000",
                                }
                            ],
                        }
                    ],
                }
            }
        ]
    )
    source = {
        "key": "jmlr",
        "name": "Journal of Machine Learning Research",
        "issns": ["1532-4435"],
        "official_domains": ["jmlr.org"],
    }

    result = CrossrefCollector(http=http, database=initialized_database).collect(
        source, date(2026, 6, 1), date(2026, 6, 2)
    )

    assert result.saved == 1
    row = initialized_database.fetch_one(
        "SELECT doi, title, abstract FROM papers WHERE source_key = ?", ("jmlr",)
    )
    assert dict(row) == {
        "doi": "10.5555/jmlr.test",
        "title": "A Journal Result",
        "abstract": "Useful abstract.",
    }


def test_openreview_collector_uses_accepted_venue_and_published_date(
    initialized_database,
):
    note = {
        "id": "note-1",
        "pdate": 1740009600000,
        "content": {
            "title": {"value": "Accepted OpenReview Paper"},
            "abstract": {"value": "A complete abstract."},
            "keywords": {"value": ["Reasoning", "Agents"]},
            "authors": {"value": ["Ming Li", "Wei Zhang"]},
            "authorids": {"value": ["~Ming_Li1", "~Wei_Zhang1"]},
            "venueid": {"value": "ICLR.cc/2025/Conference"},
        },
    }
    http = FakeHttp([{"notes": [note]}, {"notes": []}])
    source = {
        "key": "iclr",
        "name": "International Conference on Learning Representations",
        "type": "conference",
        "venue_id_template": "ICLR.cc/{year}/Conference",
        "official_domains": ["openreview.net"],
    }

    result = OpenReviewCollector(http=http, database=initialized_database).collect(
        source, date(2025, 1, 1), date(2025, 12, 31)
    )

    assert result.saved == 1
    row = initialized_database.fetch_one(
        """
        SELECT title, abstract, original_keywords_json, official_url
        FROM papers WHERE source_key = 'iclr'
        """
    )
    assert row["title"] == "Accepted OpenReview Paper"
    assert row["abstract"] == "A complete abstract."
    assert json.loads(row["original_keywords_json"]) == ["Reasoning", "Agents"]
    assert row["official_url"] == "https://openreview.net/forum?id=note-1"


def test_openreview_note_outside_range_is_rejected():
    note = {
        "id": "old",
        "pdate": 1609459200000,
        "content": {
            "title": {"value": "Old"},
            "abstract": {"value": "Old abstract"},
            "venueid": {"value": "ICLR.cc/2021/Conference"},
        },
    }

    assert normalize_openreview_note(
        note,
        {"key": "iclr", "type": "conference"},
        date(2025, 1, 1),
        date(2025, 12, 31),
    ) is None


def test_cvf_official_detail_extracts_abstract_authors_and_fallback_date():
    detail_html = """
    <html><head>
      <meta name="citation_title" content="Official Vision Paper">
      <meta name="citation_author" content="Li, Ming">
      <meta name="citation_author" content="Zhang, Wei">
      <meta name="citation_publication_date" content="2025">
      <meta name="citation_doi" content="10.1109/CVPR.TEST">
    </head><body><div id="abstract">A vision abstract.</div></body></html>
    """
    source = {"key": "cvpr", "type": "conference"}

    record = normalize_citation_detail(
        detail_html,
        source,
        "https://openaccess.thecvf.com/content/CVPR2025/html/test.html",
        fallback_date=date(2025, 6, 11),
    )

    assert record.title == "Official Vision Paper"
    assert record.abstract == "A vision abstract."
    assert record.publication_date == date(2025, 6, 11)
    assert record.authors[0]["name"] == "Li, Ming"
    assert record.doi == "10.1109/cvpr.test"


def test_official_index_link_extraction_supports_cvf_pmlr_and_jmlr():
    cvf = '<dt class="ptitle"><a href="/content/CVPR2025/html/a.html">A</a></dt>'
    pmlr = (
        '<div class="paper"><p class="links">'
        '<a href="https://proceedings.mlr.press/v267/a.html">abs</a></p></div>'
    )
    jmlr = '<dt>A</dt><dd><a href="/papers/v26/a.html">abs</a></dd>'

    assert extract_official_detail_links(
        cvf, "cvf", "https://openaccess.thecvf.com/CVPR2025"
    ) == ["https://openaccess.thecvf.com/content/CVPR2025/html/a.html"]
    assert extract_official_detail_links(
        pmlr, "pmlr", "https://proceedings.mlr.press/v267/"
    ) == ["https://proceedings.mlr.press/v267/a.html"]
    assert extract_official_detail_links(
        jmlr, "jmlr", "https://www.jmlr.org/papers/v26/"
    ) == ["https://www.jmlr.org/papers/v26/a.html"]


def test_acl_xml_extracts_main_conference_paper():
    xml_text = """<?xml version="1.0" encoding="UTF-8"?>
    <collection id="2025.acl">
      <volume id="long">
        <meta><month>July</month><year>2025</year></meta>
        <paper id="1">
          <title>ACL Paper</title>
          <author orcid="0000-0001"><first>Ming</first><last>Li</last></author>
          <abstract>ACL abstract.</abstract>
          <url>2025.acl-long.1</url>
          <doi>10.18653/v1/2025.acl-long.1</doi>
        </paper>
      </volume>
    </collection>"""

    records = normalize_acl_xml(
        xml_text,
        {"key": "acl", "type": "conference"},
        date(2025, 6, 1),
        date(2025, 8, 1),
    )

    assert len(records) == 1
    assert records[0].title == "ACL Paper"
    assert records[0].abstract == "ACL abstract."
    assert records[0].official_url == "https://aclanthology.org/2025.acl-long.1/"


def test_yaml_date_object_is_accepted_as_publication_date():
    assert coerce_config_date(date(2025, 6, 11)) == date(2025, 6, 11)
    assert coerce_config_date("2025-06-11") == date(2025, 6, 11)
