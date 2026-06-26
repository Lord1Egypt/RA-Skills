import os
import sys
import json
import pytest
from scripts.request_movie import add_movie, lookup_movie
from scripts.remove_movie import find_movie_in_library, remove_from_queue

pytestmark = pytest.mark.skipif(
    not os.environ.get("RUN_LIVE_TESTS"),
    reason="Need RUN_LIVE_TESTS=1 environment variable to run against live Radarr"
)

def test_live_movie_pipeline():
    # Big Buck Bunny is an open source short film (tmdb ID 10378)
    # 1. Lookup
    movie = lookup_movie("Big Buck Bunny")
    assert movie is not None, "TMDB lookup failed"

    # 2. Add
    res = add_movie(movie, "Big Buck Bunny")
    assert res.get("status") in ("queued", "duplicate", "queued_base_version_only")

    # 3. Wait/Verify it's in library
    in_lib = find_movie_in_library("Big Buck Bunny")
    assert in_lib is not None

    # 4. Remove
    success = remove_from_queue(in_lib["id"], delete_files=True)
    assert success is True
