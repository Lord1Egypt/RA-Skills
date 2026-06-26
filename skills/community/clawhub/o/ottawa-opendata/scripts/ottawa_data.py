#!/usr/bin/env python3
"""
City of Ottawa Open Data — CLI for ArcGIS Hub.
No dependencies beyond stdlib. Accesses open.ottawa.ca.
"""

import json, sys, os, urllib.request, urllib.parse, urllib.error, re
from datetime import datetime

DCAT_URL = "https://open.ottawa.ca/api/feed/dcat-us/1.1.json"
ARCGIS_ITEM_URL = "https://www.arcgis.com/sharing/rest/content/items"
BASE_URL = "https://open.ottawa.ca"

def api_request(url, timeout=30):
    req = urllib.request.Request(url)
    req.add_header("Accept", "application/json")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode())
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

def fetch_from_service(url, params):
    """Fetch from ArcGIS with proper URL encoding."""
    query = urllib.parse.urlencode(params, safe='')
    full_url = f"{url}/query?{query}"
    return api_request(full_url)

def load_catalog():
    cache_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".cache")
    os.makedirs(cache_dir, exist_ok=True)
    cache_file = os.path.join(cache_dir, "catalog_cache.json")
    if os.path.exists(cache_file):
        age = datetime.now().timestamp() - os.path.getmtime(cache_file)
        if age < 3600:
            return json.loads(open(cache_file).read())
    data = api_request(DCAT_URL)
    with open(cache_file, "w") as f:
        json.dump(data, f)
    return data

def extract_item_id(identifier):
    match = re.search(r'id=([a-f0-9]+)', identifier)
    return match.group(1) if match else None

def find_dataset(query, catalog=None):
    if catalog is None:
        catalog = load_catalog()
    q = query.lower()
    # Normalize Unicode dashes
    q = q.replace('\u2013', '-').replace('\u2014', '-')
    for ds in catalog.get("dataset", []):
        title = ds.get("title", "")
        iid = extract_item_id(ds.get("identifier", "")) or ""
        title_norm = title.lower().replace('\u2013', '-').replace('\u2014', '-')
        if q in title_norm or q == iid:
            return ds
    return None

def cmd_search(query):
    catalog = load_catalog()
    q = query.lower()
    matches = []
    for ds in catalog.get("dataset", []):
        title = ds.get("title", "")
        iid = extract_item_id(ds.get("identifier", "")) or ""
        if q in title.lower():
            matches.append((title, iid))
    if not matches:
        print(f"No datasets found matching '{query}'.")
        return
    print(f"\n🔍 Search results for '{query}' — {len(matches)} found\n")
    for title, iid in matches:
        print(f"  • {title}")
        print(f"    ID: {iid}")

def cmd_list():
    catalog = load_catalog()
    datasets = catalog.get("dataset", [])
    print(f"\n📁 Ottawa Open Data — {len(datasets)} datasets\n")
    for ds in sorted(datasets, key=lambda x: x.get("title", "")):
        title = ds.get("title", "N/A")
        iid = extract_item_id(ds.get("identifier", "")) or ""
        print(f"  • {title} — {iid}")

def cmd_info(query):
    ds = find_dataset(query)
    if not ds:
        print(f"Error: Dataset '{query}' not found.")
        sys.exit(1)
    title = ds.get("title", "N/A")
    iid = extract_item_id(ds.get("identifier", "")) or ""
    desc = re.sub(r'<[^>]+>', '', ds.get("description", "") or "N/A")
    keywords = ds.get("keyword", [])
    print(f"\n📊 Dataset: {title}")
    print(f"   ID: {iid}")
    print(f"   URL: {BASE_URL}/d/{iid}")
    print(f"   Description: {desc[:400]}")
    if keywords:
        print(f"   Keywords: {', '.join(keywords[:10])}")
    dist = ds.get("distribution", [])
    if dist:
        print(f"\n   Data Sources ({len(dist)}):")
        for d in dist:
            fmt = d.get("format", d.get("mediaType", "?"))
            url = d.get("downloadURL", "") or d.get("accessURL", "")
            print(f"     • [{fmt}] {url[:100]}")
    if iid:
        try:
            item = api_request(f"{ARCGIS_ITEM_URL}/{iid}?f=json")
            print(f"\n   ArcGIS Type: {item.get('type', '?')}")
            if item.get("url"):
                print(f"   Service URL: {item['url']}")
        except:
            pass

def cmd_fetch(query, options):
    ds = find_dataset(query)
    if not ds:
        print(f"Error: Dataset '{query}' not found.")
        sys.exit(1)
    iid = extract_item_id(ds.get("identifier", "")) or ""
    title = ds.get("title", "?")
    if iid:
        try:
            item = api_request(f"{ARCGIS_ITEM_URL}/{iid}?f=json")
            itype = item.get("type", "")
            item_url = item.get("url", "")
            if itype in ("Feature Service", "Map Service") and item_url:
                url_base = item_url.rstrip("/")
                if re.search(r'/\d+$', url_base):
                    layer_url = url_base
                else:
                    svc = api_request(f"{url_base}?f=json")
                    layers = svc.get("layers", [])
                    if not layers:
                        print("No layers found.")
                        return
                    layer_url = f"{url_base}/{layers[0]['id']}"
                params = {"resultRecordCount": options.get("limit", 10), "f": "json", "where": "1=1", "outFields": "*"}
                query_url = f"{layer_url}/query?" + urllib.parse.urlencode(params)
                data = api_request(query_url)
                features = data.get("features", [])
                if features:
                    rows = [f.get("attributes", {}) for f in features]
                    if options.get("csv"):
                        keys = list(rows[0].keys())
                        print(",".join(keys))
                        for row in rows:
                            print(",".join([str(row.get(k, "")).replace(",", ";") for k in keys]))
                    else:
                        print(json.dumps(rows, indent=2, default=str))
                    return
            elif itype == "Document Link" and item_url:
                print(f"// Document: {item_url}", file=sys.stderr)
                return
        except Exception as e:
            print(f"Error: {e}")
    print(f"No queryable data source found for '{title}'.")

def cmd_downloads():
    catalog = load_catalog()
    print(f"\n📥 Datasets with Download Links\n")
    for ds in catalog.get("dataset", []):
        title = ds.get("title", "?")
        iid = extract_item_id(ds.get("identifier", "")) or ""
        if iid:
            try:
                item = api_request(f"{ARCGIS_ITEM_URL}/{iid}?f=json")
                if item.get("url"):
                    print(f"  • [{item.get('type', '?')}] {title}")
                    print(f"    {item['url']}")
            except:
                pass

def main():
    if len(sys.argv) < 2:
        print(__doc__); sys.exit(0)
    cmd = sys.argv[1]
    options = {}
    args = sys.argv[2:]
    if cmd == "search" and args:
        cmd_search(" ".join(args))
    elif cmd == "list":
        cmd_list()
    elif cmd == "info" and args:
        cmd_info(" ".join(args))
    elif cmd == "fetch" and args:
        query = args[0]
        i = 1
        while i < len(args):
            if args[i] == "--limit" and i+1 < len(args):
                options["limit"] = int(args[i+1]); i += 2
            elif args[i] == "--csv":
                options["csv"] = True; i += 1
            else: i += 1
        cmd_fetch(query, options)
    elif cmd == "downloads":
        cmd_downloads()

if __name__ == "__main__":
    main()
