#!/usr/bin/env python3
"""
City of Montreal Open Data — CLI for the CKAN API.
No dependencies beyond stdlib. Accesses donnees.montreal.ca.
"""

import json, sys, os, urllib.request, urllib.parse, urllib.error
from datetime import datetime

CKAN_API = "https://donnees.montreal.ca/api/3/action"

def api_request(endpoint, params=None):
    url = f"{CKAN_API}/{endpoint}"
    if params:
        url += "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url)
    req.add_header("Accept", "application/json")
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        print(f"Error: HTTP {e.code}")
        sys.exit(1)

def load_catalog():
    cache_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".cache")
    os.makedirs(cache_dir, exist_ok=True)
    cache_file = os.path.join(cache_dir, "catalog_cache.json")
    if os.path.exists(cache_file):
        age = datetime.now().timestamp() - os.path.getmtime(cache_file)
        if age < 3600:
            return json.loads(open(cache_file).read())
    data = api_request("package_search", {"rows": 500})
    results = data.get("result", {}).get("results", [])
    datasets = []
    for pkg in results:
        datasets.append({
            "name": pkg.get("name", ""),
            "title": pkg.get("title", ""),
            "notes": (pkg.get("notes") or "")[:100],
            "resources": len(pkg.get("resources", [])),
            "datastore_resources": len([r for r in pkg.get("resources", []) if r.get("datastore_active")]),
            "tags": [t.get("display_name", "") for t in pkg.get("tags", [])[:5]]
        })
    with open(cache_file, "w") as f:
        json.dump(datasets, f)
    return datasets

def cmd_search(query):
    datasets = load_catalog()
    q = query.lower()
    matches = [d for d in datasets if q in d.get("title", "").lower() or q in d.get("name", "").lower()]
    if not matches:
        print(f"Aucun dataset trouvé pour '{query}'.")
        return
    print(f"\n🔍 Résultats pour '{query}' — {len(matches)} trouvé(s)\n")
    for d in matches:
        ds = d.get("datastore_resources", 0)
        qf = f" [{ds} requêtable]" if ds else ""
        print(f"  • {d['title']}{qf}")
        print(f"    ID: {d['name']}")

def cmd_list():
    datasets = load_catalog()
    print(f"\n📁 Montréal — {len(datasets)} datasets\n")
    for d in sorted(datasets, key=lambda x: x.get("title", "")):
        ds = d.get("datastore_resources", 0)
        qf = f" [{ds} DS]" if ds else ""
        print(f"  • {d['title']} ({d['resources']} res{qf}) — {d['name']}")

def cmd_searchable():
    datasets = load_catalog()
    q = [d for d in datasets if d.get("datastore_resources", 0) > 0]
    print(f"\n📊 Datasets requêtables — {len(q)} of {len(datasets)}\n")
    for d in sorted(q, key=lambda x: -x.get("datastore_resources", 0)):
        print(f"  • {d['title']} [{d['datastore_resources']} resources] — {d['name']}")

def cmd_info(dataset_id):
    data = api_request("package_show", {"id": dataset_id})
    pkg = data.get("result", {})
    print(f"\n📊 Dataset: {pkg.get('title', 'N/A')}")
    print(f"   ID: {dataset_id}")
    print(f"   URL: https://donnees.montreal.ca/dataset/{dataset_id}")
    print(f"   Description: {(pkg.get('notes') or 'N/A')[:400]}")
    tags = [t.get("display_name", "") for t in pkg.get("tags", [])]
    if tags:
        print(f"   Mots-clés: {', '.join(tags[:10])}")
    resources = pkg.get("resources", [])
    if resources:
        print(f"\n   Resources ({len(resources)}):")
        for r in resources:
            ds = " [Datastore]" if r.get("datastore_active") else ""
            print(f"     • [{r.get('format', '?')}]{ds} {r.get('name', '?')}")
            print(f"       ID: {r.get('id', '')}")

def cmd_fetch(dataset_id, options):
    data = api_request("package_show", {"id": dataset_id})
    resources = data.get("result", {}).get("resources", [])
    ds_res = [r for r in resources if r.get("datastore_active")]
    if not ds_res:
        print(f"Erreur: Aucune resource requêtable dans '{dataset_id}'.")
        sys.exit(1)
    rid = ds_res[0]["id"]
    params = {"resource_id": rid, "limit": int(options.get("limit", 10))}
    data = api_request("datastore_search", params)
    records = data.get("result", {}).get("records", [])
    if not records:
        print("Aucune donnée retournée.")
        return
    if options.get("csv"):
        keys = list(records[0].keys())
        print(",".join(keys))
        for row in records:
            print(",".join([str(row.get(k, "")).replace(",", ";") for k in keys]))
    else:
        print(json.dumps(records, indent=2, default=str))

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
    elif cmd == "searchable":
        cmd_searchable()
    elif cmd == "info" and args:
        cmd_info(args[0])
    elif cmd == "fetch" and args:
        dataset_id = args[0]
        i = 1
        while i < len(args):
            if args[i] == "--limit" and i+1 < len(args):
                options["limit"] = args[i+1]; i += 2
            elif args[i] == "--csv":
                options["csv"] = True; i += 1
            else: i += 1
        cmd_fetch(dataset_id, options)

if __name__ == "__main__":
    main()
