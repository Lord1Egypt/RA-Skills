#!/usr/bin/env python3
"""
City of Lethbridge Open Data — CLI for ArcGIS Hub.
No dependencies beyond stdlib. Accesses opendata.lethbridge.ca.

Usage:
  python3 lethbridge_data.py <command> [args]

Commands:
  search <query>                    Search datasets by keyword
  list                              List all datasets
  info <name-or-id>                 Show dataset metadata
  fetch <name-or-id> [options]      Fetch data from dataset
  downloads                         List datasets with download URLs
"""

import json
import sys
import os
import urllib.request
import urllib.parse
import urllib.error
import re
from datetime import datetime

DCAT_URL = "https://opendata.lethbridge.ca/api/feed/dcat-us/1.1.json"
ARCGIS_ITEM_URL = "https://www.arcgis.com/sharing/rest/content/items"
BASE_URL = "https://opendata.lethbridge.ca"

def api_request(url, timeout=30):
    """Make a GET request and return JSON."""
    req = urllib.request.Request(url)
    req.add_header("Accept", "application/json")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        body = e.read().decode() if e.fp else ""
        print(f"Error: HTTP {e.code} — {body[:200]}")
        sys.exit(1)
    except urllib.error.URLError as e:
        print(f"Error: {e.reason}")
        sys.exit(1)

def raw_request(url, timeout=30):
    """Make a GET request and return raw response."""
    req = urllib.request.Request(url)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.read().decode()
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

def load_catalog():
    """Load and cache the DCAT catalog."""
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

def get_item_details(item_id):
    """Fetch ArcGIS item details."""
    url = f"{ARCGIS_ITEM_URL}/{item_id}?f=json"
    return api_request(url)

def extract_item_id(identifier):
    """Extract ArcGIS item ID from DCAT identifier URL."""
    match = re.search(r'id=([a-f0-9]+)', identifier)
    return match.group(1) if match else None

def find_dataset(query, catalog=None):
    """Find a dataset by name or ID."""
    if catalog is None:
        catalog = load_catalog()
    
    query_lower = query.lower()
    for ds in catalog.get("dataset", []):
        title = ds.get("title", "")
        ident = ds.get("identifier", "")
        iid = extract_item_id(ident) or ""
        if query_lower in title.lower() or query_lower == iid:
            return ds
    return None

def fetch_arcgis_data(url, params=None):
    """Fetch data from an ArcGIS feature/map service."""
    if params is None:
        params = {}
    params.setdefault("f", "json")
    params.setdefault("where", "1=1")
    params.setdefault("outFields", "*")
    params.setdefault("resultRecordCount", "10")
    
    query = urllib.parse.urlencode(params)
    full_url = f"{url}/query?{query}"
    return api_request(full_url)

# --- Commands ---

def cmd_search(query):
    """Search datasets by name or description."""
    catalog = load_catalog()
    query_lower = query.lower()
    matches = []
    
    for ds in catalog.get("dataset", []):
        title = ds.get("title", "")
        desc = (ds.get("description") or "")[:100]
        ident = ds.get("identifier", "")
        iid = extract_item_id(ident) or ""
        if query_lower in title.lower() or query_lower in desc.lower():
            matches.append((title, iid, desc))
    
    if not matches:
        print(f"No datasets found matching '{query}'.")
        return
    
    print(f"\n🔍 Search results for '{query}' — {len(matches)} found\n")
    for title, iid, desc in matches:
        print(f"  • {title}")
        print(f"    ID: {iid}")
        print(f"    {BASE_URL}/d/{iid}")
        if desc:
            # Strip HTML tags
            clean = re.sub(r'<[^>]+>', '', desc)
            print(f"    {clean[:120]}")
    print()

def cmd_list():
    """List all datasets."""
    catalog = load_catalog()
    datasets = catalog.get("dataset", [])
    
    print(f"\n📁 Lethbridge Open Data — {len(datasets)} datasets\n")
    for ds in sorted(datasets, key=lambda x: x.get("title", "")):
        title = ds.get("title", "N/A")
        ident = ds.get("identifier", "")
        iid = extract_item_id(ident) or "N/A"
        dist = ds.get("distribution", [])
        formats = [d.get("format", d.get("mediaType", "?")) for d in dist]
        print(f"  • {title}")
        print(f"    ID: {iid} | Formats: {', '.join(formats)}")
    print()

def cmd_info(query):
    """Show metadata for a dataset."""
    ds = find_dataset(query)
    if not ds:
        print(f"Error: Dataset '{query}' not found.")
        sys.exit(1)
    
    title = ds.get("title", "N/A")
    ident = ds.get("identifier", "")
    iid = extract_item_id(ident) or ""
    desc = re.sub(r'<[^>]+>', '', ds.get("description", "") or "N/A")
    keywords = ds.get("keyword", [])
    
    print(f"\n📊 Dataset: {title}")
    print(f"   ID: {iid}")
    print(f"   URL: {BASE_URL}/d/{iid}")
    print(f"   Description: {desc[:400]}")
    if keywords:
        print(f"   Keywords: {', '.join(keywords[:10])}")
    
    # Distribution info
    dist = ds.get("distribution", [])
    if dist:
        print(f"\n   Data Sources ({len(dist)}):")
        for d in dist:
            fmt = d.get("format", d.get("mediaType", "?"))
            url = d.get("downloadURL", "") or d.get("accessURL", "")
            print(f"     • [{fmt}] {url[:100]}")
    
    # Try to get ArcGIS item details
    if iid:
        try:
            item = get_item_details(iid)
            itype = item.get("type", "?")
            item_url = item.get("url", "")
            print(f"\n   ArcGIS Type: {itype}")
            if item_url:
                print(f"   Service URL: {item_url}")
            
            # If feature service, show fields
            if itype in ("Feature Service", "Map Service") and item_url:
                try:
                    svc_info = api_request(f"{item_url}?f=json")
                    layers = svc_info.get("layers", [])
                    if layers:
                        layer_url = f"{item_url}/{layers[0].get('id', 0)}"
                        layer_info = api_request(f"{layer_url}?f=json")
                        fields = layer_info.get("fields", [])
                        print(f"\n   Fields ({len(fields)}):")
                        for f in fields[:15]:
                            print(f"     • {f.get('name', '?')} ({f.get('type', '?')})")
                except:
                    pass
        except:
            pass
    print()

def cmd_fetch(query, options):
    """Fetch data from a dataset."""
    ds = find_dataset(query)
    if not ds:
        print(f"Error: Dataset '{query}' not found.")
        sys.exit(1)
    
    ident = ds.get("identifier", "")
    iid = extract_item_id(ident) or ""
    title = ds.get("title", "?")
    
    # Get ArcGIS item details to find service URL
    if iid:
        try:
            item = get_item_details(iid)
            itype = item.get("type", "")
            item_url = item.get("url", "")
            
            if itype in ("Feature Service", "Map Service") and item_url:
                # ArcGIS query parameters
                params = {
                    "resultRecordCount": options.get("limit", 10),
                    "f": "json",
                    "where": "1=1",
                    "outFields": "*"
                }
                
                # Determine if URL already points to a specific layer
                query_base = item_url.rstrip("/")
                
                # Check if URL already ends with a layer number
                if re.search(r'/\d+$', query_base):
                    # Already a layer URL — query directly
                    layer_url = query_base
                else:
                    # Service URL — get first layer
                    try:
                        svc_info = api_request(f"{query_base}?f=json")
                        layers = svc_info.get("layers", [])
                        if layers:
                            layer_url = f"{query_base}/{layers[0].get('id', 0)}"
                        else:
                            print(f"Error: No layers found in service.")
                            return
                    except Exception as e:
                        print(f"Error reading service: {e}")
                        return
                
                try:
                    data = fetch_arcgis_data(layer_url, params)
                    features = data.get("features", [])
                    if features:
                        # Extract attributes
                        rows = [f.get("attributes", {}) for f in features]
                        if options.get("csv"):
                            keys = list(rows[0].keys())
                            print(",".join(keys))
                            for row in rows:
                                vals = [str(row.get(k, "")).replace(",", ";") for k in keys]
                                print(",".join(vals))
                        else:
                            print(json.dumps(rows, indent=2, default=str))
                    else:
                        print("No data returned.")
                except Exception as e:
                    print(f"Error querying layer: {e}")
                return
            
            elif itype == "Document Link" and item_url:
                # Download document directly
                print(f"// Document URL: {item_url}", file=sys.stderr)
                if item_url.endswith(('.xlsx', '.xls', '.pdf')):
                    print(f"// Binary file — download directly: {item_url}", file=sys.stderr)
                    return
                # Try fetching text-based docs
                try:
                    content = raw_request(item_url)
                    print(content[:5000])
                    return
                except:
                    pass
            
            elif itype == "Web Mapping Application":
                print(f"// Web app: {item_url or 'No URL'}", file=sys.stderr)
                return
                
        except Exception as e:
            print(f"Error getting item details: {e}")
    
    # Fallback: try DCAT distribution URLs
    dist = ds.get("distribution", [])
    for d in dist:
        url = d.get("downloadURL", "") or d.get("accessURL", "")
        if url and not url.endswith(('.xlsx', '.xls', '.pdf')):
            try:
                content = raw_request(url)
                print(content[:5000])
                return
            except:
                continue
    
    print(f"No queryable data source found for '{title}'.")
    print(f"View at: {BASE_URL}/d/{iid}")

def cmd_downloads():
    """List datasets with direct download URLs."""
    catalog = load_catalog()
    
    print(f"\n📥 Datasets with Download Links\n")
    for ds in catalog.get("dataset", []):
        title = ds.get("title", "?")
        ident = ds.get("identifier", "")
        iid = extract_item_id(ident) or ""
        
        # Get item details to find download URL
        if iid:
            try:
                item = get_item_details(iid)
                item_url = item.get("url", "")
                itype = item.get("type", "?")
                if item_url:
                    print(f"  • [{itype}] {title}")
                    print(f"    {item_url}")
            except:
                pass
    print()

# --- CLI ---

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(0)
    
    cmd = sys.argv[1]
    
    if cmd == "search" and len(sys.argv) >= 3:
        cmd_search(" ".join(sys.argv[2:]))
    elif cmd == "list":
        cmd_list()
    elif cmd == "info" and len(sys.argv) >= 3:
        cmd_info(" ".join(sys.argv[2:]))
    elif cmd == "fetch" and len(sys.argv) >= 3:
        query = sys.argv[2]
        options = {}
        args = sys.argv[3:]
        i = 0
        while i < len(args):
            if args[i] == "--limit" and i + 1 < len(args):
                options["limit"] = int(args[i + 1]); i += 2
            elif args[i] == "--format" and i + 1 < len(args):
                options["format"] = args[i + 1]; i += 2
            elif args[i] == "--csv":
                options["csv"] = True; i += 1
            else:
                i += 1
        cmd_fetch(query, options)
    elif cmd == "downloads":
        cmd_downloads()
    else:
        print(__doc__)
        sys.exit(1)

if __name__ == "__main__":
    main()
