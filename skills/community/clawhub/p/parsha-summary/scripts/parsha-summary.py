#!/usr/bin/env python3
"""
Parsha Summary - Weekly Torah Portion Summary
Lightweight wrapper around Sefaria API
"""

import json
import urllib.request
import urllib.parse
import sys
import argparse
from datetime import datetime

SEFARIA_API = "https://www.sefaria.org/api"

def fetch(path):
    """Fetch from Sefaria API."""
    url = f"{SEFARIA_API}/{path}"
    try:
        req = urllib.request.Request(url, headers={
            'User-Agent': 'ParshaSummary/1.0 (Jewish Agent Skills)'
        })
        with urllib.request.urlopen(req, timeout=15) as resp:
            return json.loads(resp.read().decode())
    except Exception as e:
        return {"error": str(e)}

def get_parsha_name():
    """Get this week's parsha from Hebcal."""
    try:
        today = datetime.now().strftime("%Y-%m-%d")
        url = f"https://www.hebcal.com/hebcal?v=1&cfg=json&year={today[:4]}&month={today[5:7]}&day={today[8:10]}&s=on"
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode())
            for item in data.get("items", []):
                if item.get("category") == "parashat":
                    return {
                        "name": item.get("title", "").replace("Parashat ", ""),
                        "hebrew": item.get("hebrew", ""),
                        "date": today,
                    }
    except:
        pass
    return None

def get_parsha_text(parsha_name):
    """Get parsha text from Sefaria."""
    # Map parsha names to Sefaria refs
    parsha_map = {
        "Bereshit": "Genesis.1.1-6.8",
        "Noach": "Genesis.6.9-11.32",
        "Lech-Lecha": "Genesis.12.1-17.27",
        "Vayera": "Genesis.18.1-22.24",
        "Chayei Sara": "Genesis.23.1-25.18",
        "Toldot": "Genesis.25.19-28.9",
        "Vayetzei": "Genesis.28.10-32.3",
        "Vayishlach": "Genesis.32.4-36.43",
        "Vayeshev": "Genesis.37.1-40.23",
        "Miketz": "Genesis.41.1-44.17",
        "Vayigash": "Genesis.44.18-47.27",
        "Vayechi": "Genesis.47.28-50.26",
        "Shemot": "Exodus.1.1-6.1",
        "Vaera": "Exodus.6.2-9.35",
        "Bo": "Exodus.10.1-13.16",
        "Beshalach": "Exodus.13.17-17.16",
        "Yitro": "Exodus.18.1-20.23",
        "Mishpatim": "Exodus.21.1-24.18",
        "Terumah": "Exodus.25.1-27.19",
        "Tetzaveh": "Exodus.27.20-30.10",
        "Ki Tisa": "Exodus.30.11-34.35",
        "Vayakhel": "Exodus.35.1-38.20",
        "Pekudei": "Exodus.38.21-40.38",
        "Vayikra": "Leviticus.1.1-5.26",
        "Tzav": "Leviticus.6.1-8.36",
        "Shemini": "Leviticus.9.1-11.47",
        "Tazria": "Leviticus.12.1-13.59",
        "Metzora": "Leviticus.14.1-15.33",
        "Achrei Mot": "Leviticus.16.1-18.30",
        "Kedoshim": "Leviticus.19.1-20.27",
        "Emor": "Leviticus.21.1-24.23",
        "Behar": "Leviticus.25.1-26.2",
        "Bechukotai": "Leviticus.26.3-27.34",
        "Bamidbar": "Numbers.1.1-4.20",
        "Naso": "Numbers.4.21-7.89",
        "Beha'alotcha": "Numbers.8.1-12.16",
        "Shelach": "Numbers.13.1-15.41",
        "Korach": "Numbers.16.1-18.32",
        "Chukat": "Numbers.19.1-22.1",
        "Balak": "Numbers.22.2-25.9",
        "Pinchas": "Numbers.25.10-30.1",
        "Matot": "Numbers.30.2-32.42",
        "Masei": "Numbers.33.1-36.13",
        "Devarim": "Deuteronomy.1.1-3.22",
        "Vaetchanan": "Deuteronomy.3.23-7.11",
        "Eikev": "Deuteronomy.7.12-11.25",
        "Re'eh": "Deuteronomy.11.26-16.17",
        "Shoftim": "Deuteronomy.16.18-21.9",
        "Ki Teitzei": "Deuteronomy.21.10-25.19",
        "Ki Tavo": "Deuteronomy.26.1-29.8",
        "Nitzavim": "Deuteronomy.29.9-30.20",
        "Vayelech": "Deuteronomy.31.1-31.30",
        "Ha'Azinu": "Deuteronomy.32.1-32.52",
        "Vezot Haberakhah": "Deuteronomy.33.1-34.12",
    }
    
    ref = parsha_map.get(parsha_name)
    if not ref:
        return {"error": f"Unknown parsha: {parsha_name}"}
    
    # Get English text
    data = fetch(f"texts/{urllib.parse.quote(ref.replace(' ', '_'))}?context=0")
    
    if "error" in data:
        return data
    
    return {
        "parsha": parsha_name,
        "ref": ref,
        "hebrew": data.get("he", {}).get("text", []) if isinstance(data.get("he", {}), dict) else [],
        "english": data.get("text", []) if isinstance(data, dict) else [],
    }

def generate_summary(parsha_data, max_words=150):
    """Generate a brief summary from parsha text."""
    if "error" in parsha_data:
        return parsha_data
    
    english = parsha_data.get("english", [])
    hebrew = parsha_data.get("hebrew", [])
    
    # Sefaria returns nested arrays for verses
    flat_verses = []
    for item in english:
        if isinstance(item, list):
            flat_verses.extend(item)
        elif isinstance(item, str):
            flat_verses.append(item)
    
    # Join verses and truncate
    text = " ".join(flat_verses[:5]) if flat_verses else ""
    
    # Extract first sentence or ~150 words
    # Strip HTML tags for clean output
    import re
    clean_text = re.sub(r'<[^\u003e]+\u003e', '', text)
    words = clean_text.split()
    summary = " ".join(words[:max_words])
    
    if len(words) > max_words:
        summary += "..."
    
    # Get key themes (first few verse references)
    # Flatten sample verses too
    sample_verses = []
    for item in english[:3]:
        if isinstance(item, list):
            sample_verses.extend(item)
        elif isinstance(item, str):
            sample_verses.append(item)
    # Strip HTML tags from sample verses
    clean_samples = []
    for v in sample_verses[:3]:
        clean_v = re.sub(r'<[^\u003e]+\u003e', '', str(v))
        clean_samples.append(clean_v)
    verses = clean_samples
    
    return {
        "parsha": parsha_data["parsha"],
        "ref": parsha_data["ref"],
        "summary": summary,
        "verse_count": len(english),
        "sample_verses": verses[:3],
        "hebrew_available": bool(hebrew),
    }

def main():
    parser = argparse.ArgumentParser(description="Parsha Summary")
    parser.add_argument("parsha", nargs="?", help="Parsha name (default: this week)")
    parser.add_argument("--words", "-w", type=int, default=150, help="Max words in summary")
    parser.add_argument("--json", "-j", action="store_true", help="JSON output")
    parser.add_argument("--hebrew", "-H", action="store_true", help="Include Hebrew text")
    
    args = parser.parse_args()
    
    if args.parsha:
        parsha_name = args.parsha
    else:
        info = get_parsha_name()
        if not info:
            print("❌ Could not determine this week's parsha")
            sys.exit(1)
        parsha_name = info["name"]
    
    print(f"📜 Loading: {parsha_name}...")
    
    data = get_parsha_text(parsha_name)
    if "error" in data:
        print(f"❌ Error: {data['error']}")
        sys.exit(1)
    
    summary = generate_summary(data, max_words=args.words)
    
    if args.json:
        print(json.dumps(summary, indent=2, ensure_ascii=False))
    else:
        print(f"\n📖 {summary['parsha']}")
        print(f"   {summary['ref']}")
        print(f"   {summary['verse_count']} verses")
        print(f"\n{summary['summary']}")
        
        if args.hebrew and summary.get("hebrew_available"):
            print("\n🕎 Hebrew text available (use --json for full text)")
        
        if summary.get("sample_verses"):
            print("\n📖 Sample verses:")
            for i, v in enumerate(summary["sample_verses"][:2], 1):
                print(f"   {i}. {v[:100]}...")

if __name__ == "__main__":
    main()
