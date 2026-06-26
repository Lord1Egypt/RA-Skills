import pytest
from scripts.check_download import fuzzy_match, format_eta

def test_fuzzy_match_exact_and_partial():
    torrents = [
        {"name": "The.Matrix.1999.1080p.BluRay.x264-SPARKS", "progress": 1.0, "state": "pausedUP"},
        {"name": "The.Matrix.Reloaded.2003.1080p.BluRay.x264-SPARKS", "progress": 0.5, "state": "downloading"}
    ]
    
    # Match base matrix
    res = fuzzy_match("The Matrix", torrents)
    assert res is not None
    assert "1999" in res["name"]
    
    # Match reloaded
    res = fuzzy_match("matrix reloaded", torrents)
    assert res is not None
    assert "Reloaded" in res["name"]
    
    # Completely missing
    res = fuzzy_match("Inception", torrents)
    assert res is None

def test_format_eta():
    assert format_eta(3600) == "1h 0m"
    assert format_eta(65) == "1m 5s"
    assert format_eta(3000000) == "unknown" # greater than 7 days
    assert format_eta(45) == "45s"
