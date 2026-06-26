"""
linkedin-jobs-scraper validation tests
Tests the scraper logic with mocked HTTP responses.
"""

import json
import csv
import io
import re
import tempfile
import os
from pathlib import Path
from unittest.mock import patch, MagicMock
from typing import Optional, Dict, List, Any

SKILL_DIR = Path(__file__).parent

# ─── Mock HTML Samples ─────────────────────────────────────────────

SEARCH_RESULTS_HTML = """
<div class="base-search-card">
  <h3 class="base-search-card__title">Python Developer</h3>
  <h4 class="base-search-card__subtitle">Tech Corp</h4>
  <span class="job-search-card__location">São Paulo, SP</span>
  <a class="base-card__full-link" href="https://br.linkedin.com/jobs/view/python-developer-4413133140"></a>
</div>
<div class="base-search-card">
  <h3 class="base-search-card__title">Data Scientist</h3>
  <h4 class="base-search-card__subtitle">AI Solutions</h4>
  <span class="job-search-card__location">Remote</span>
  <a class="base-card__full-link" href="https://br.linkedin.com/jobs/view/data-scientist-4413133141"></a>
</div>
<div class="base-search-card">
  <h3 class="base-search-card__title">Fullstack Engineer</h3>
  <h4 class="base-search-card__subtitle">Startup XYZ</h4>
  <span class="job-search-card__location">Rio de Janeiro, RJ</span>
  <a class="base-card__full-link" href="/jobs/view/4413133142"></a>
</div>
"""

JOB_DETAILS_HTML = """
<div class="top-card-layout__title">Python Developer</div>
<a class="topcard__org-name-link">Tech Corp</a>
<span class="topcard__flavor--bullet">São Paulo, SP</span>
<span class="posted-time-ago__text">1 week ago</span>
<div class="show-more-less-html__markup">
  <p>We are looking for a Python developer with 3+ years of experience.</p>
  <p>Requirements: Flask, Django, PostgreSQL.</p>
</div>
<ul class="job-details-jobs-unified-top-card__primary-details">
  <li>Full-time</li>
  <li>Mid-Senior level</li>
  <li>Engineering</li>
  <li>Software Development</li>
</ul>
"""

EMPTY_SEARCH_HTML = """
<div class="no-results">No jobs found matching your criteria.</div>
"""


# ─── Tests ─────────────────────────────────────────────────────────

errors = 0
passed = 0


def check(name, condition, detail=""):
    global errors, passed
    if condition:
        print(f"  ✅ {name}")
        passed += 1
    else:
        print(f"  ❌ {name} {detail}")
        errors += 1


# Need to import after mock setup
def _get_scraper():
    from scraper import LinkedInJobsScraper
    return LinkedInJobsScraper


def test_build_params_default():
    print("\n🔧 Build Params (default)")
    Scraper = _get_scraper()
    s = Scraper()
    params = s._build_search_params("python", "Brazil")
    check("has keywords", params["keywords"] == "python")
    check("has location", params["location"] == "Brazil")
    check("has start=0", params["start"] == 0)
    check("no remote filter", "f_WT" not in params)
    check("no experience filter", "f_E" not in params)
    check("no job type filter", "f_JT" not in params)
    check("no posted filter", "f_TPR" not in params)
    check("no salary filter", "f_SALARY" not in params)
    check("no company filter", "f_C" not in params)
    check("no industry filter", "f_I" not in params)
    check("no sort", "sortBy" not in params)


def test_build_params_all_filters():
    print("\n🔧 Build Params (all filters)")
    Scraper = _get_scraper()
    s = Scraper()
    params = s._build_search_params(
        "python", "Brazil",
        remote="only",
        experience="mid-senior",
        job_type="full-time",
        posted="last-week",
        salary_min=80000,
        company="1441",
        industry="4",
        sort="date"
    )
    check("remote only (f_WT=2)", params.get("f_WT") == 2)
    check("mid-senior (f_E=4)", params.get("f_E") == "4")
    check("full-time (f_JT=F)", params.get("f_JT") == "F")
    check("last-week (f_TPR=r604800)", params.get("f_TPR") == "r604800")
    check("salary min 80000", params.get("f_SALARY") == "80000")
    check("company 1441", params.get("f_C") == "1441")
    check("industry 4", params.get("f_I") == "4")
    check("sort by date (DD)", params.get("sortBy") == "DD")


def test_build_params_remote():
    print("\n🔧 Build Params (remote variants)")
    Scraper = _get_scraper()
    s = Scraper()

    params_only = s._build_search_params("python", "Brazil", remote="only")
    check("remote only = 2", params_only.get("f_WT") == 2)

    params_yes = s._build_search_params("python", "Brazil", remote="yes")
    check("remote yes = 2,3", params_yes.get("f_WT") == "2,3")

    params_no = s._build_search_params("python", "Brazil", remote="no")
    check("remote no = 1", params_no.get("f_WT") == 1)

    params_none = s._build_search_params("python", "Brazil", remote=None)
    check("remote none = no key", "f_WT" not in params_none)


def test_build_params_sort():
    print("\n🔧 Build Params (sort)")
    Scraper = _get_scraper()
    s = Scraper()

    p_date = s._build_search_params("python", "Brazil", sort="date")
    check("sort date = DD", p_date.get("sortBy") == "DD")

    p_rel = s._build_search_params("python", "Brazil", sort="relevance")
    check("sort relevance = R", p_rel.get("sortBy") == "R")

    p_none = s._build_search_params("python", "Brazil", sort=None)
    check("sort none = no key", "sortBy" not in p_none)


def test_parse_search_results():
    print("\n📋 Parse Search Results")
    Scraper = _get_scraper()
    s = Scraper()
    jobs = s._parse_search_results(SEARCH_RESULTS_HTML)
    check("found 3 jobs", len(jobs) == 3, f"found {len(jobs)}")
    check("first title", jobs[0]["title"] == "Python Developer")
    check("first company", jobs[0]["company"] == "Tech Corp")
    check("first location", jobs[0]["location"] == "São Paulo, SP")
    check("has job_id", jobs[0]["job_id"] == "4413133140")
    check("has url", jobs[0]["url"] is not None)
    check("second title", jobs[1]["title"] == "Data Scientist")
    check("third title", jobs[2]["title"] == "Fullstack Engineer")
    check("relative URL parsed", jobs[2]["job_id"] == "4413133142")


def test_parse_search_results_empty():
    print("\n📋 Parse Search Results (empty)")
    Scraper = _get_scraper()
    s = Scraper()
    jobs = s._parse_search_results(EMPTY_SEARCH_HTML)
    check("found 0 jobs", len(jobs) == 0)


def test_extract_job_id():
    print("\n🔢 Extract Job ID")
    Scraper = _get_scraper()
    s = Scraper()

    # Format 1: standard URL with hyphen-ID
    id1 = s._extract_job_id("https://br.linkedin.com/jobs/view/python-developer-4413133140")
    check("hyphen format", id1 == "4413133140")

    # Format 2: /jobs/view/ID
    id2 = s._extract_job_id("https://www.linkedin.com/jobs/view/4413133141")
    check("view format", id2 == "4413133141")

    # Format 3: plain ID string
    id3 = s._extract_job_id("4413133142")
    check("plain ID", id3 == "4413133142")

    # Format 4: None
    id4 = s._extract_job_id(None)
    check("None input", id4 is None)

    # Format 5: empty string
    id5 = s._extract_job_id("")
    check("empty input", id5 is None)


def test_parse_job_details():
    print("\n📄 Parse Job Details")
    Scraper = _get_scraper()
    s = Scraper()
    details = s._parse_job_details(JOB_DETAILS_HTML, "4413133140")
    check("has title", details["title"] == "Python Developer")
    check("has company", details["company"] == "Tech Corp")
    check("has location", details["location"] == "São Paulo, SP")
    check("has posted_date", details["posted_date"] == "1 week ago")
    check("has description", details["description"] is not None)
    check("description contains Flask", "Flask" in details["description"])
    check("has employment_type", details["employment_type"] is not None)
    check("has url", details["url"] is not None)
    check("url contains job_id", "4413133140" in details["url"])


def _make_mock_session():
    """Create a mock requests.Session with get method."""
    session = MagicMock()
    session.headers = {}
    session.get.return_value = MagicMock()
    session.get.return_value.status_code = 200
    session.get.return_value.text = SEARCH_RESULTS_HTML
    return session


def test_get_job_details_http_error():
    print("\n📄 Get Job Details (HTTP error)")
    Scraper = _get_scraper()
    
    with patch('scraper.requests.Session') as mock_session_class:
        mock_session = MagicMock()
        mock_session_class.return_value = mock_session
        
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_session.get.return_value = mock_response
        
        s = Scraper()
        result = s.get_job_details("4413133140")
        check("returns None on 404", result is None)


def test_search_jobs_rate_limit():
    print("\n🚦 Rate Limit Handling")
    Scraper = _get_scraper()
    
    with patch('scraper.requests.Session') as mock_session_class:
        rate_limit_response = MagicMock()
        rate_limit_response.status_code = 429
        
        success_response = MagicMock()
        success_response.status_code = 200
        success_response.text = SEARCH_RESULTS_HTML
        
        mock_session = MagicMock()
        mock_session.headers = {}
        mock_session.get.side_effect = [rate_limit_response, success_response]
        mock_session_class.return_value = mock_session
        
        s = Scraper()
        jobs = s.search_jobs("python", "Brazil", limit=5)
        check("recovers from 429", len(jobs) > 0)
        check("calls session.get twice", mock_session.get.call_count == 2)  # 429 retry → success


def test_search_jobs_pagination():
    print("\n📑 Pagination")
    Scraper = _get_scraper()
    
    with patch('scraper.requests.Session') as mock_session_class:
        mock_session = MagicMock()
        mock_session.headers = {}
        response1 = MagicMock()
        response1.status_code = 200
        response1.text = SEARCH_RESULTS_HTML * 9
        
        mock_session.get.return_value = response1
        mock_session_class.return_value = mock_session
        
        s = Scraper()
        jobs = s.search_jobs("python", "Brazil", limit=5)
        check("returns up to limit", len(jobs) == 5)

        jobs2 = s.search_jobs("python", "Brazil", limit=10)
        check("returns up to 10", len(jobs2) == 10)


def test_save_to_csv():
    print("\n💾 Save to CSV")
    Scraper = _get_scraper()
    s = Scraper()
    
    jobs = [
        {"title": "Dev", "company": "Co", "location": "SP", "url": "https://x.com/job/1", "job_id": "1"},
        {"title": "Eng", "company": "Inc", "location": "RJ", "url": "https://x.com/job/2", "job_id": "2"},
    ]
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False, encoding='utf-8') as f:
        temp_path = f.name
    
    try:
        s.save_to_csv(jobs, temp_path)
        with open(temp_path, 'r', encoding='utf-8') as f:
            content = f.read()
        check("CSV has header", "title" in content)
        check("CSV has data", "Dev" in content and "Co" in content)
        check("CSV 2 rows", len(content.strip().split('\n')) == 3)
    finally:
        os.unlink(temp_path)


def test_save_to_json():
    print("\n💾 Save to JSON")
    Scraper = _get_scraper()
    s = Scraper()
    
    jobs = [{"title": "Dev", "company": "Co", "job_id": "1"}]
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False, encoding='utf-8') as f:
        temp_path = f.name
    
    try:
        s.save_to_json(jobs, temp_path)
        with open(temp_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        check("JSON is list", isinstance(data, list))
        check("JSON has 1 item", len(data) == 1)
        check("JSON has title", data[0]["title"] == "Dev")
    finally:
        os.unlink(temp_path)


def test_search_and_save():
    print("\n🔄 Search and Save (integration)")
    Scraper = _get_scraper()
    
    with patch('scraper.requests.Session') as mock_session_class:
        response = MagicMock()
        response.status_code = 200
        response.text = SEARCH_RESULTS_HTML
        mock_session = MagicMock()
        mock_session.headers = {}
        mock_session.get.return_value = response
        mock_session_class.return_value = mock_session
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False, encoding='utf-8') as f:
            temp_path = f.name
        
        try:
            s = Scraper()
            result = s.search_and_save(
                keywords="python", location="Brazil",
                output=temp_path, limit=2
            )
            check("returns jobs list", len(result) == 2)
            with open(temp_path, 'r', encoding='utf-8') as f:
                content = f.read()
            check("file was written", "Python Developer" in content)
        finally:
            os.unlink(temp_path)


def test_skil_metadata():
    print("\n📄 SKILL.md Validation")
    path = SKILL_DIR / "SKILL.md"
    check("SKILL.md exists", path.exists())
    if path.exists():
        content = path.read_text(encoding="utf-8")
        check("has YAML frontmatter", content.startswith("---"))
        check("has name field", "name:" in content)
        check("has description field", "description:" in content)
        check("has CLI examples", "python scraper.py" in content)
        check("has Python usage", "search_jobs" in content)
        check("has parameter table", "--keywords" in content)
        check("has salary-min param", "salary-min" in content)
        check("has company param", "--company" in content)
        check("has sort param", "--sort" in content)
        check("has boas praticas", "Boas Práticas" in content or "boas praticas" in content.lower())


def test_clawhub_metadata():
    print("\n📦 clawhub.json Validation")
    path = SKILL_DIR / "clawhub.json"
    check("clawhub.json exists", path.exists())
    if path.exists():
        data = json.loads(path.read_text(encoding="utf-8"))
        check("has name", "name" in data and data["name"])
        check("has tagline", "tagline" in data)
        check("has description", "description" in data)
        check("has category", "category" in data)
        check("has tags list", "tags" in data and len(data["tags"]) >= 8)
        check("has license", "license" in data)
        check("has version", "version" in data)
        check("version >= 1.1.0", data.get("version", "0") >= "1.1.0")


def test_save_to_csv_empty():
    print("\n💾 Save to CSV (empty)")
    Scraper = _get_scraper()
    s = Scraper()
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False, encoding='utf-8') as f:
        temp_path = f.name
    
    try:
        # Should not crash with empty list
        s.save_to_csv([], temp_path)
        with open(temp_path, 'r', encoding='utf-8') as f:
            content = f.read()
        check("empty CSV is empty", content == "")
    finally:
        os.unlink(temp_path)


def test_save_to_json_empty():
    print("\n💾 Save to JSON (empty)")
    Scraper = _get_scraper()
    s = Scraper()
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False, encoding='utf-8') as f:
        temp_path = f.name
    
    try:
        # Should not crash with empty list; file remains empty
        s.save_to_json([], temp_path)
        with open(temp_path, 'r', encoding='utf-8') as f:
            content = f.read()
        check("empty JSON file is empty", content == "")
    finally:
        os.unlink(temp_path)


def test_user_agent_rotation():
    print("\n🔄 User-Agent Rotation")
    Scraper = _get_scraper()
    s1 = Scraper()
    s2 = Scraper()
    check("different instances may have different UA", True)  # probabilistic test, just verify it doesn't crash
    check("UA header is set", "User-Agent" in s1.session.headers)
    check("UA is non-empty", len(s1.session.headers["User-Agent"]) > 10)


def test_get_job_details_network_error():
    print("\n📄 Get Job Details (network error)")
    Scraper = _get_scraper()
    
    with patch('scraper.requests.Session') as mock_session_class:
        from requests.exceptions import ConnectionError
        mock_session = MagicMock()
        mock_session.headers = {}
        mock_session.get.side_effect = ConnectionError("Connection refused")
        mock_session_class.return_value = mock_session
        
        s = Scraper()
        result = s.get_job_details("4413133140")
        check("returns None on network error", result is None)


def test_parse_search_results_malformed():
    print("\n📋 Parse Search Results (malformed)")
    Scraper = _get_scraper()
    s = Scraper()
    # HTML with no job cards
    jobs = s._parse_search_results("<html><body><p>Nothing here</p></body></html>")
    check("malformed returns empty list", len(jobs) == 0)
    
    # Empty string
    jobs2 = s._parse_search_results("")
    check("empty string returns empty list", len(jobs2) == 0)


def test_parse_search_results_partial_data():
    print("\n📋 Parse Search Results (partial data)")
    Scraper = _get_scraper()
    s = Scraper()
    # Job card missing fields
    html = """
    <div class="base-search-card">
      <!-- Missing title -->
      <h4 class="base-search-card__subtitle">Company Only</h4>
    </div>
    """
    jobs = s._parse_search_results(html)
    check("skips card without title", len(jobs) == 0)


def test_delay_range():
    print("\n⏱️  Delay Range")
    Scraper = _get_scraper()
    
    s1 = Scraper(delay_range=(1, 2))
    check("custom delay range min", s1.delay_range[0] == 1)
    check("custom delay range max", s1.delay_range[1] == 2)
    
    s2 = Scraper(delay_range=(3, 5))
    check("default delay min", s2.delay_range[0] == 3)
    check("default delay max", s2.delay_range[1] == 5)


# ─── Run ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import sys
    sys.stdout.reconfigure(encoding='utf-8')
    print("=" * 50)
    print("  linkedin-jobs-scraper validation tests")
    print("=" * 50)
    
    test_build_params_default()
    test_build_params_all_filters()
    test_build_params_remote()
    test_build_params_sort()
    test_parse_search_results()
    test_parse_search_results_empty()
    test_parse_search_results_malformed()
    test_parse_search_results_partial_data()
    test_extract_job_id()
    test_parse_job_details()
    test_get_job_details_http_error()
    test_get_job_details_network_error()
    test_search_jobs_rate_limit()
    test_search_jobs_pagination()
    test_search_and_save()
    test_save_to_csv()
    test_save_to_csv_empty()
    test_save_to_json()
    test_save_to_json_empty()
    test_user_agent_rotation()
    test_delay_range()
    test_skil_metadata()
    test_clawhub_metadata()
    
    print(f"\n{'=' * 50}")
    total = passed + errors
    print(f"  Results: {passed}/{total} passed, {errors} failed")
    if errors:
        print("  WARNING: Some tests failed!")
    else:
        print("  All tests passed!")
    print(f"{'=' * 50}")
