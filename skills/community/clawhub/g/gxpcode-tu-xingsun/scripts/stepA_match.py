# GxpCode Skill — Step A: 按域名匹配已有 parser
# 用法: python stepA_match.py <URL>

import sys
import yaml
import os
from urllib.parse import urlparse

SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SOURCES_PATH = os.path.join(SKILL_DIR, "resources", "sources.yaml")


def match(url: str) -> dict:
    domain = urlparse(url).netloc

    with open(SOURCES_PATH, "r", encoding="utf-8") as f:
        sources = yaml.safe_load(f).get("sources", [])

    # 找同域名下已有的 web 源
    same_domain = []
    for s in sources:
        if s.get("type") != "web":
            continue
        if urlparse(s.get("url", "")).netloc == domain:
            same_domain.append(s)

    if same_domain:
        parser = same_domain[0].get("parser", "")
        return {
            "matched": True,
            "parser": parser,
            "domain": domain,
            "examples": [s["name"] for s in same_domain],
        }
    else:
        return {
            "matched": False,
            "domain": domain,
            "action": "new",
        }


if __name__ == "__main__":
    url = sys.argv[1]
    result = match(url)
    import json
    print(json.dumps(result, ensure_ascii=False, indent=2))
