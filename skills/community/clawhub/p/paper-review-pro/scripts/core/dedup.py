"""
去重模块
"""


def deduplicate(papers, index):
    existing_titles = set(p["title"] for p in index["papers"])
    existing_urls = set(p["url"] for p in index["papers"])

    result = []
    for p in papers:
        if p["title"] in existing_titles:
            continue
        if p["url"] in existing_urls:
            continue
        result.append(p)

    return result