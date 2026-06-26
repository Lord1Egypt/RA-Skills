
import sys
import json
from playwright.sync_api import sync_playwright


import argparse

def fetch_papers(limit=10):
    results = []
    with sync_playwright() as p:
        try:
            # Launch Chromium (headless)
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            
            # Go to the Daily Papers page
            try:
                page.goto("https://huggingface.co/papers", timeout=60000, wait_until="domcontentloaded")
            except:
                print("Warning: Page Load Timeout. Attempting to extract partial content.", file=sys.stderr)
            
            # Wait for articles to load
            page.wait_for_selector("article", timeout=15000)
            
            # Extract basic data first
            articles = page.query_selector_all("article")
            
            candidates = []
            for art in articles:
                if len(candidates) >= limit:
                    break
                try:
                    # Title is usually in an h3
                    title_el = art.query_selector("h3")
                    if not title_el: continue
                    title = title_el.inner_text().strip()
                    
                    # Link is in the h3 > a
                    link_el = title_el.query_selector("a")
                    if not link_el: continue
                    href = link_el.get_attribute("href")
                    if href.startswith("/"):
                        href = "https://huggingface.co" + href
                        
                    candidates.append({
                        "title": title,
                        "url": href,
                        "heat": "Trending",
                        "summary": ""
                    })
                except: continue

            # Now fetch details for each candidate
            for item in candidates:
                try:
                    sys.stderr.write(f" Visiting details: {item['url']}\n")
                    try:
                        page.goto(item['url'], timeout=60000, wait_until="domcontentloaded")
                    except:
                        sys.stderr.write("   -> Detail Page Timeout (Partial/Continue)\n")

                    # 1. Abstract
                    abstract_text = ""
                    paragraphs = page.query_selector_all("p")
                    for p in paragraphs:
                        txt = p.inner_text()
                        if len(txt) > 200:
                            abstract_text = txt
                            break 
                    if abstract_text:
                        item['summary'] = abstract_text

                    # 2. GitHub Link
                    gh_el = page.query_selector("a[href*='github.com']")
                    if gh_el:
                         item['github'] = gh_el.get_attribute("href")
                         sys.stderr.write(f"   -> Found GitHub: {item['github']}\n")
                    
                    # 3. Heat (Upvotes)
                    # Use JS to find button with +Number
                    heat_text = page.evaluate("""() => {
                        const btns = Array.from(document.querySelectorAll('button'));
                        const heatBtn = btns.find(b => /^\\+\\d+$/.test(b.innerText.trim()));
                        return heatBtn ? heatBtn.innerText.trim() : null;
                    }""")
                    if heat_text:
                        item['heat'] = heat_text
                        sys.stderr.write(f"   -> Found Heat: {heat_text}\n")
                        
                except Exception as e:
                    item['summary'] = f"Failed to fetch details: {str(e)}"
                results.append(item)
            
            browser.close()
            
        except Exception as e:
            sys.stderr.write(f"Playwright Error: {str(e)}\n")
            sys.exit(1)
            
    print(json.dumps(results))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=10, help="Number of papers to fetch")
    args = parser.parse_args()
    fetch_papers(limit=args.limit)
