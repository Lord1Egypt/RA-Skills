from scripts.arxiv_utils import extract_arxiv_ids_from_text, sort_arxiv_ids


def test_extract_arxiv_ids_from_text_handles_variants():
    text = """
    See arXiv:2301.00001v2 and arxiv 2402.12345.
    Another mention: 2301.00001 and 2503.54321v3.
    """
    assert extract_arxiv_ids_from_text(text) == ["2301.00001", "2402.12345", "2503.54321"]


def test_sort_arxiv_ids_deduplicates():
    assert sort_arxiv_ids(["2402.12345", "2301.00001", "2402.12345"]) == ["2301.00001", "2402.12345"]
