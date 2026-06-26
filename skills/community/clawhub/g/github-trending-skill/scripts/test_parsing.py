import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from scripts.utils import parse_trending

SAMPLE_HTML = """
<html><body>
<article class="Box-row">
  <h2><a href="/octocat/hello">octocat/hello</a></h2>
  <p>Sample repository</p>
  <span itemprop="programmingLanguage">Python</span>
  <a href="/octocat/hello/stargazers">1,234</a>
  <span class="d-inline-block float-sm-right">56 stars today</span>
</article>
</body></html>
"""


def main() -> None:
    items = parse_trending(SAMPLE_HTML)
    assert items and items[0]["name"] == "octocat/hello"
    assert items[0]["stars_total"] == 1234
    assert items[0]["stars_period"] == 56
    print("parse_trending: ok")


if __name__ == "__main__":
    main()
