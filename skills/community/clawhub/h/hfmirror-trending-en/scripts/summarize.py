import json
import os
import sys
import urllib.request

# Default trending API URL for HF-Mirror
TRENDING_API_URL = "https://hf-mirror.com/api/trending"

def format_params(num):
    if num is None:
        return "-"
    if num >= 1e9:
        return f"~{num/1e9:.2f}B"
    if num >= 1e6:
        return f"~{num/1e6:.2f}M"
    return str(num)

def fetch_trending_data(url=TRENDING_API_URL):
    try:
        print(f"Fetching trending data from {url}...")
        headers = {'User-Agent': 'hfmirror-trending-en-skill/1.0'}
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read().decode('utf-8'))
    except Exception as e:
        print(f"Error fetching data: {e}")
        return None

def summarize_trending(data, md_path=None):
    if not data:
        return "No data to summarize."

    items = data.get("recentlyTrending", [])
    
    models = []
    datasets = []
    spaces = []

    for item in items:
        rtype = item.get("repoType")
        repo = item.get("repoData", {})
        
        if rtype == "model":
            models.append({
                "id": repo.get("id", "-"),
                "downloads": repo.get("downloads", 0),
                "likes": repo.get("likes", 0),
                "params": format_params(repo.get("numParameters")),
                "pipeline": repo.get("pipeline_tag", "-"),
                "updated": repo.get("lastModified", "")[:10]
            })
        elif rtype == "dataset":
            datasets.append({
                "id": repo.get("id", "-"),
                "downloads": repo.get("downloads", 0),
                "likes": repo.get("likes", 0),
                "rows": repo.get("datasetsServerInfo", {}).get("numRows", "-"),
                "updated": repo.get("lastModified", "")[:10]
            })
        elif rtype == "space":
            spaces.append({
                "title": repo.get("title", repo.get("id", "-")),
                "id": repo.get("id", "-"),
                "likes": repo.get("likes", 0),
                "category": repo.get("ai_category", "-"),
                "hardware": repo.get("runtime", {}).get("hardware", {}).get("current", "-"),
                "updated": repo.get("lastModified", "")[:10]
            })

    output = []
    output.append("# Hugging Face Trending Resources In-Depth Report\n")
    output.append("---")
    
    # Models Table
    output.append("\n## 1. Trending Models\n")
    output.append("| Model ID | Downloads | Likes | Parameters | Pipeline Tag | Updated |")
    output.append("| :--- | :--- | :--- | :--- | :--- | :--- |")
    for m in sorted(models, key=lambda x: x['downloads'], reverse=True):
        output.append(f"| `{m['id']}` | {m['downloads']:,} | {m['likes']:,} | {m['params']} | {m['pipeline']} | {m['updated']} |")

    # Datasets Table
    output.append("\n## 2. Trending Datasets\n")
    output.append("| Dataset ID | Downloads | Likes | Rows | Updated |")
    output.append("| :--- | :--- | :--- | :--- | :--- |")
    for d in sorted(datasets, key=lambda x: x['downloads'], reverse=True):
        rows = f"{d['rows']:,}" if isinstance(d['rows'], int) else d['rows']
        output.append(f"| `{d['id']}` | {d['downloads']:,} | {d['likes']:,} | {rows} | {d['updated']} |")

    # Spaces Table
    output.append("\n## 3. Trending Spaces\n")
    output.append("| Space Title | ID | Likes | AI Category | Hardware | Updated |")
    output.append("| :--- | :--- | :--- | :--- | :--- | :--- |")
    for s in sorted(spaces, key=lambda x: x['likes'], reverse=True):
        output.append(f"| `{s['title']}` | `{s['id']}` | {s['likes']:,} | {s['category']} | {s['hardware']} | {s['updated']} |")

    result_md = "\n".join(output)
    
    if md_path:
        with open(md_path, 'w', encoding='utf-8') as f:
            f.write(result_md)
        print(f"Summary generated successfully: {md_path}")
    
    return result_md

if __name__ == "__main__":
    # Simple CLI support
    # Case 1: python summarize.py --fetch [out.md]
    # Case 2: python summarize.py [input.json] [out.md]
    
    if "--fetch" in sys.argv:
        data = fetch_trending_data()
        out_path = sys.argv[2] if len(sys.argv) > 2 else "trending_summary.md"
        summarize_trending(data, out_path)
    elif len(sys.argv) >= 3:
        with open(sys.argv[1], 'r', encoding='utf-8') as f:
            data = json.load(f)
        summarize_trending(data, sys.argv[2])
    else:
        print("Usage:")
        print("  python summarize.py --fetch [output_md]")
        print("  python summarize.py <input_json> <output_md>")
