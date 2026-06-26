#!/usr/bin/env python3
"""
Job Lead Radar — Scrape job leads from multiple job boards.
Usage: python scrape.py [source] [query]
"""

import json
import sys
import os
from datetime import datetime

try:
    from scrapling.fetchers import Fetcher
except ImportError:
    print("ERROR: scrapling not installed. Run: pip install scrapling")
    sys.exit(1)


class JobLeadRadar:
    def __init__(self):
        self.fetcher = Fetcher()
        self.script_dir = os.path.dirname(os.path.abspath(__file__))

    def save_results(self, results):
        output_path = os.path.join(self.script_dir, "job_leads.json")
        with open(output_path, "w") as f:
            json.dump(results, f, indent=2)
        print(f"  → Saved {len(results.get('jobs', []))} jobs to {output_path}")
        return output_path

    def scrape_indeed(self, query="film producer"):
        """Scrape Indeed for jobs."""
        print(f"  Scraping Indeed: {query}")
        try:
            url = f"https://www.indeed.com/jobs?q={query.replace(' ', '+')}&l=Remote"
            r = self.fetcher.get(url)
            jobs = []
            for elem in r.css('a[href*="/job/"]')[:15]:
                title = elem.css("::text").get()
                link = elem.css("::attr(href)").get()
                if title and len(title.strip()) > 5 and link:
                    full_link = f"https://indeed.com{link}" if link.startswith("/") else link
                    jobs.append({"title": title.strip()[:100], "link": full_link})
            # Deduplicate
            seen, unique = set(), []
            for job in jobs:
                if job["title"] not in seen:
                    seen.add(job["title"])
                    unique.append(job)
            print(f"    Found {len(unique)} unique jobs")
            return {"source": "indeed", "query": query, "jobs": unique[:10]}
        except Exception as e:
            return {"source": "indeed", "error": str(e)}

    def scrape_ziprecruiter(self, query="film producer"):
        """Scrape ZipRecruiter."""
        print(f"  Scraping ZipRecruiter: {query}")
        try:
            url = f"https://www.ziprecruiter.com/jobs/search?q={query.replace(' ', '-')}"
            r = self.fetcher.get(url)
            jobs = []
            for card in r.css(".job_card")[:10]:
                title = card.css("a.job_title::text").get()
                company = card.css(".company::text").get()
                link = card.css("a.job_title::attr(href)").get()
                if title:
                    jobs.append({
                        "title": (title or "").strip(),
                        "company": (company or "").strip(),
                        "link": link or ""
                    })
            print(f"    Found {len(jobs)} jobs")
            return {"source": "ziprecruiter", "query": query, "jobs": jobs}
        except Exception as e:
            return {"source": "ziprecruiter", "error": str(e)}

    def scrape_productionhub(self):
        """Scrape ProductionHUB."""
        print("  Scraping ProductionHUB")
        try:
            r = self.fetcher.get("https://www.productionhub.com/jobs")
            jobs = []
            for card in r.css(".JobCardstyles__JobCardContainer")[:10]:
                title = card.css("a::text").get()
                company = card.css(".CompanyNamestyles__CompanyName::text").get()
                link = card.css("a::attr(href)").get()
                if title:
                    jobs.append({
                        "title": (title or "").strip(),
                        "company": (company or "").strip(),
                        "link": f"https://productionhub.com{link}" if link else ""
                    })
            print(f"    Found {len(jobs)} jobs")
            return {"source": "productionhub", "jobs": jobs}
        except Exception as e:
            return {"source": "productionhub", "error": str(e)}

    def scrape_linkedin(self, query="film producer"):
        """Scrape LinkedIn Jobs (public listings)."""
        print(f"  Scraping LinkedIn: {query}")
        try:
            url = f"https://www.linkedin.com/jobs/search/?keywords={query.replace(' ', '%20')}"
            r = self.fetcher.get(url)
            jobs = []
            for card in r.css(".job-card-container")[:10]:
                title = card.css(".job-card-list__title::text").get()
                company = card.css(".job-card-container__company-name::text").get()
                link = card.css("a::attr(href)").get()
                if title:
                    full_link = f"https://linkedin.com{link}" if link and link.startswith("/") else (link or "")
                    jobs.append({
                        "title": (title or "").strip(),
                        "company": (company or "").strip(),
                        "link": full_link
                    })
            print(f"    Found {len(jobs)} jobs")
            return {"source": "linkedin", "query": query, "jobs": jobs}
        except Exception as e:
            return {"source": "linkedin", "error": str(e)}

    def scrape_peerspace(self):
        """Scrape Peerspace (location-based production venues)."""
        print("  Scraping Peerspace")
        try:
            r = self.fetcher.get("https://www.peerspace.com")
            locations = r.css('a[href*="/locations/"]::attr(href)').getall()
            categories = r.css('a[href*="/categories/"]::text').getall()
            print(f"    Found {len(locations)} locations, {len(categories)} categories")
            return {
                "source": "peerspace",
                "locations": len(locations),
                "categories": categories[:10]
            }
        except Exception as e:
            return {"source": "peerspace", "error": str(e)}

    def run(self, sources=None, queries=None):
        """Run all or specific scrapers."""
        sources = sources or ["all"]
        queries = queries or ["film producer"]

        print("=" * 50)
        print(f"Job Lead Radar — {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        print("=" * 50)

        results = {"timestamp": datetime.now().isoformat(), "jobs": []}

        if "all" in sources:
            for q in queries:
                results["jobs"].append(self.scrape_indeed(q))
                results["jobs"].append(self.scrape_ziprecruiter(q))
            results["jobs"].append(self.scrape_productionhub())
            results["jobs"].append(self.scrape_linkedin(queries[0]))
            results["jobs"].append(self.scrape_peerspace())
        else:
            for source in sources:
                if source == "indeed":
                    q = queries[0] if queries else "film producer"
                    results["jobs"].append(self.scrape_indeed(q))
                elif source == "ziprecruiter":
                    q = queries[0] if queries else "film producer"
                    results["jobs"].append(self.scrape_ziprecruiter(q))
                elif source == "productionhub":
                    results["jobs"].append(self.scrape_productionhub())
                elif source == "linkedin":
                    q = queries[0] if queries else "film producer"
                    results["jobs"].append(self.scrape_linkedin(q))
                elif source == "peerspace":
                    results["jobs"].append(self.scrape_peerspace())

        self.save_results(results)

        total_jobs = sum(
            len(s.get("jobs", [])) for s in results["jobs"] if isinstance(s.get("jobs"), list)
        )
        print(f"\n✓ Collected {total_jobs} jobs across {len(results['jobs'])} sources")
        return results


if __name__ == "__main__":
    source = sys.argv[1] if len(sys.argv) > 1 else "all"
    query = sys.argv[2] if len(sys.argv) > 2 else "film producer"

    sources = [source] if source != "all" else ["all"]
    queries = [query]

    radar = JobLeadRadar()
    radar.run(sources=sources, queries=queries)
