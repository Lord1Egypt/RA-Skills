#!/usr/bin/env python3
"""
lead-enrichment-scanner — executable (v1.0.0)

Usage:
  clawhub run lead-enrichment-scanner enrich --input companies.txt --output leads.csv
  clawhub run lead-enrichment-scanner enrich --input companies.txt --output leads.csv --bulk --concurrency 3
  clawhub run lead-enrichment-scanner enrich --input companies.txt --output leads.csv --resume
  clawhub run lead-enrichment-scanner enrich --input companies.txt --output leads.csv --dry-run
  clawhub run lead-enrichment-scanner drafts --input leads.csv --tone consultative --output drafts.md
  clawhub run lead-enrichment-scanner filter --input leads.csv --min-employees 50 --max-employees 500 --output leads-segmented.csv
  clawhub run lead-enrichment-scanner configure --respect-robots-txt true --rate-limit-seconds 5

Free tier: up to 10 leads per run.
"""
__version__ = "1.0.1"
SCHEMA_VERSION = 1

import argparse
import csv
import json
import logging
import os
import re
import sys
import time
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from pathlib import Path

logger = logging.getLogger("lead-enrichment-scanner")
USER_AGENT = "LeadEnrichmentScanner/1.0 (+https://clawhub.ai)"
DEFAULT_RATE_LIMIT = 5  # seconds between requests
DEFAULT_BULK_CONCURRENCY = 3
ROBOTS_TXT_CACHE = {}
LLM_API_KEY_MISSING_WARNED = False


def configure_logging(verbose=False, quiet=False):
    """Configure logging level based on flags / env."""
    level = logging.WARNING
    if verbose:
        level = logging.DEBUG
    elif not quiet:
        level = logging.INFO
    # Allow env override
    env_level = os.environ.get("CLAWHUB_LOG_LEVEL", "").upper()
    if env_level in ("DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"):
        level = getattr(logging, env_level)
    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%dT%H:%M:%S",
    )


def load_config():
    """Load skill config from ~/.openclaw/lead-enrichment-scanner.json."""
    config_path = Path.home() / ".openclaw" / "lead-enrichment-scanner.json"
    if config_path.exists():
        try:
            with open(config_path) as f:
                cfg = json.load(f)
                # Migrate from older schema versions if needed
                file_schema = cfg.get("_schema_version", 0)
                if file_schema < SCHEMA_VERSION:
                    logger.info(f"Migrating config schema from v{file_schema} to v{SCHEMA_VERSION}")
                cfg.pop("_schema_version", None)
                return cfg
        except (json.JSONDecodeError, IOError):
            pass
    return {
        "respect_robots_txt": True,
        "rate_limit_seconds": DEFAULT_RATE_LIMIT,
        "no_personal_emails": True,
        "max_concurrent": DEFAULT_BULK_CONCURRENCY,
    }


def get_llm_api_key():
    """Scope to MINIMAX only — no credential bundling."""
    key = os.environ.get("MINIMAX_API_KEY")
    if key:
        return key, "MINIMAX_API_KEY"
    return None, None


def respect_robots_txt(url, user_agent="*"):
    """Check if scraping a URL is allowed per robots.txt."""
    try:
        parsed = urllib.parse.urlparse(url)
        robots_url = f"{parsed.scheme}://{parsed.netloc}/robots.txt"
        if robots_url in ROBOTS_TXT_CACHE:
            return ROBOTS_TXT_CACHE[robots_url]
        req = urllib.request.Request(robots_url, headers={"User-Agent": user_agent})
        with urllib.request.urlopen(req, timeout=5) as r:
            content = r.read().decode("utf-8", errors="replace")
        path = parsed.path or "/"
        disallowed = False
        for line in content.split("\n"):
            line = line.strip().lower()
            if line.startswith("disallow:"):
                disallow_path = line.split(":", 1)[1].strip()
                if disallow_path and path.startswith(disallow_path):
                    disallowed = True
                    break
        ROBOTS_TXT_CACHE[robots_url] = not disallowed
        return not disallowed
    except Exception:
        return True


def fetch_url(url, timeout=10, rate_limit=DEFAULT_RATE_LIMIT):
    """Fetch URL with SSRF protection: HTTPS only, block private IP ranges."""
    # SSRF protection: only HTTPS, validate target
    parsed = urllib.parse.urlparse(url)
    if parsed.scheme != "https":
        return None
    host = parsed.netloc or parsed.path.split("/")[0]
    # Basic private-IP block (covers most common SSRF targets)
    private_keywords = ["localhost", "127.", "0.", "10.", "172.16", "172.17", "172.18",
                        "172.19", "172.20", "172.21", "172.22", "172.23", "172.24",
                        "172.25", "172.26", "172.27", "172.28", "172.29", "172.30", 
                        "172.31", "192.168.", "169.254.", "metadata.", "169.254.169.254"]
    for kw in private_keywords:
        if host.startswith(kw) or kw in host:
            logger.debug(f"SSRF block: {host}")
            return None

    config = load_config()
    if config.get("respect_robots_txt", True) and not respect_robots_txt(url):
        return None
    rl = rate_limit if rate_limit else config.get("rate_limit_seconds", DEFAULT_RATE_LIMIT)
    time.sleep(rl)
    try:
        req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.read().decode("utf-8", errors="replace")
    except Exception as e:
        return None


def extract_company_info_from_html(html, company_name):
    """Extract basic info from a company homepage."""
    info = {
        "name": company_name,
        "description": "",
        "emails_found": [],
        "social_links": [],
    }
    if not html:
        return info
    # Description from meta tags
    for pattern in [
        r'<meta[^>]+name=["\']description["\'][^>]+content=["\']([^"\']+)["\']',
        r'<meta[^>]+property=["\']og:description["\'][^>]+content=["\']([^"\']+)["\']',
        r'<meta[^>]+name=["\']twitter:description["\'][^>]+content=["\']([^"\']+)["\']',
    ]:
        m = re.search(pattern, html, re.IGNORECASE)
        if m:
            info["description"] = m.group(1).strip()[:300]
            break
    # Emails
    info["emails_found"] = list(set(re.findall(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", html)))[:5]
    # Social links
    for network in ["linkedin.com", "twitter.com", "x.com", "github.com"]:
        matches = re.findall(rf'href=["\']([^"\']*{re.escape(network)}[^"\']*)["\']', html, re.IGNORECASE)
        info["social_links"].extend(matches[:2])
    return info


def guess_domain(company_name):
    """Best-guess domain from a company name."""
    name = re.sub(r"[^a-zA-Z0-9\s]", "", company_name.lower()).strip()
    parts = name.split()
    candidates = [
        name.replace(" ", "") + ".com",
        (parts[0] if parts else name) + ".com",
    ]
    return candidates[0]


def guess_email_patterns(company_name):
    """Generate likely email patterns for a company."""
    name = re.sub(r"[^a-zA-Z0-9\s]", "", company_name.lower()).strip()
    parts = name.split()
    domain = guess_domain(company_name)
    if not parts:
        return []
    return [
        f"{{firstname}}@{domain}",
        f"{{firstname}}.{{lastname}}@{domain}",
        f"{{firstinitial}}{{lastname}}@{domain}",
    ]


def call_llm(prompt, model="minimax/MiniMax-M3", max_tokens=800):
    """Call LLM via pinned minimax endpoint. TT3 fix: no LLM_BASE_URL override."""
    global LLM_API_KEY_MISSING_WARNED
    api_key, key_var = get_llm_api_key()
    if not api_key:
        if not LLM_API_KEY_MISSING_WARNED:
            logger.warning(
                "LLM enrichment disabled: no MINIMAX_API_KEY found.\n"
                "  Set: export MINIMAX_API_KEY=\"***\"\n"
                "  Fields like industry and employee_estimate will be empty without it."
            )
            LLM_API_KEY_MISSING_WARNED = True
        return None
    base_url = "https://api.minimax.chat/v1"  # pinned, no env override
    try:
        data = json.dumps({
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": max_tokens,
            "temperature": 0.3,
        }).encode()
        req = urllib.request.Request(
            f"{base_url}/chat/completions",
            data=data,
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
                "User-Agent": USER_AGENT,
            }
        )
        with urllib.request.urlopen(req, timeout=30) as r:
            result = json.loads(r.read())
            return result["choices"][0]["message"]["content"].strip()
    except urllib.error.HTTPError as e:
        if e.code == 401:
            if not LLM_API_KEY_MISSING_WARNED:
                logger.warning(f"LLM auth failed (401) — check MINIMAX_API_KEY has credits.")
                LLM_API_KEY_MISSING_WARNED = True
        elif e.code == 429:
            logger.warning(f"LLM rate limited (429), skipping this lead")
        else:
            logger.warning(f"LLM HTTP {e.code}")
        return None
    except Exception as e:
        logger.warning(f"LLM call failed: {type(e).__name__}: {str(e)[:100]}")
        return None


def enrich_lead(company_name, rate_limit=DEFAULT_RATE_LIMIT):
    """Enrich a single company: scrape site + LLM extraction."""
    domain = guess_domain(company_name)
    url = f"https://{domain}"

    html = fetch_url(url, rate_limit=rate_limit)
    info = extract_company_info_from_html(html, company_name)
    info["domain"] = domain
    info["email_patterns"] = guess_email_patterns(company_name)

    if info["description"]:
        prompt = f"""Given this company name and website description, extract structured info.

Company: {company_name}
Domain: {domain}
Description: {info['description']}

Reply ONLY in this exact JSON format (no markdown, no preamble):
{{"industry": "<one of: SaaS, E-commerce, FinTech, Healthcare, Real Estate, Marketing, Consulting, Other>", "employee_estimate": "<one of: 1-10, 11-50, 51-200, 201-500, 501-1000, 1000+>", "decision_maker_title": "<most likely decision-maker title for outreach>", "company_summary": "<one sentence summary>"}}
"""
        llm_response = call_llm(prompt)
        if llm_response:
            try:
                json_match = re.search(r"\{.*\}", llm_response, re.DOTALL)
                if json_match:
                    parsed = json.loads(json_match.group())
                    info.update(parsed)
            except Exception:
                pass

    return info


def load_existing_leads(output_path):
    """Load already-processed leads from output file (for --resume)."""
    if not os.path.exists(output_path):
        return []
    try:
        leads = []
        with open(output_path) as f:
            reader = csv.DictReader(f)
            for row in reader:
                leads.append(row)
        return leads
    except Exception:
        return []


def already_processed(company_name, existing_leads):
    """Check if company was already processed."""
    for lead in existing_leads:
        if lead.get("name", "").lower() == company_name.lower():
            return True
    return False


def cmd_enrich(args):
    """Enrich a list of companies."""
    if not os.path.exists(args.input):
        logger.error(f"ERROR: input file not found: {args.input}")
        sys.exit(1)

    with open(args.input) as f:
        companies = [line.strip() for line in f if line.strip()]

    # Tier limits (skip message in dry-run mode so the dry-run shows the full plan)
    if not args.dry_run:
        if not args.pro and len(companies) > 10:
            print(f"Free tier limited to 10 companies. You provided {len(companies)}.")
            print(f"Use --pro flag for higher limits (paid tier).")
            companies = companies[:10]
        elif args.pro and len(companies) > 500:
            print(f"Pro tier limited to 500 companies. Truncating.")
            companies = companies[:500]

    # Resume support
    existing = []
    if args.resume:
        existing = load_existing_leads(args.output)
        if existing:
            logger.info(f"Resume mode: {len(existing)} already in {args.output}, skipping those.")
            before = len(companies)
            companies = [c for c in companies if not already_processed(c, existing)]
            logger.info(f"  → {len(companies)} remaining to process (was {before})")

    if not companies:
        logger.info("Nothing to process.")
        if existing:
            logger.info(f"  Output file already has {len(existing)} leads.")
        return

    # Dry run
    if args.dry_run:
        logger.info(f"\n[DRY RUN] Would process {len(companies)} companies:")
        for i, c in enumerate(companies[:20], 1):
            logger.info(f"  {i}. {c} → {guess_domain(c)}")
        if len(companies) > 20:
            logger.info(f"  ... and {len(companies) - 20} more")
        if args.bulk:
            logger.info(f"  Mode: bulk (parallel, concurrency={args.concurrency})")
        else:
            logger.info(f"  Mode: sequential (~{len(companies) * args.rate_limit}s estimated)")
        logger.info(f"  Output: {args.output}")
        return

    rate_limit = args.rate_limit
    start_time = time.time()

    # Decide mode: bulk (parallel) or sequential
    leads_new = []
    if args.bulk:
        config = load_config()
        concurrency = args.concurrency or config.get("max_concurrent", DEFAULT_BULK_CONCURRENCY)
        logger.info(f"Bulk mode: {len(companies)} companies, concurrency={concurrency}")
        # Note: rate_limit per worker is reduced since multiple workers
        effective_rl = max(1, rate_limit // concurrency)
        with ThreadPoolExecutor(max_workers=concurrency) as executor:
            futures = {executor.submit(enrich_lead, c, effective_rl): c for c in companies}
            for i, future in enumerate(as_completed(futures), 1):
                company = futures[future]
                try:
                    lead = future.result()
                    leads_new.append(lead)
                    elapsed = time.time() - start_time
                    rate = i / elapsed if elapsed > 0 else 0
                    eta = (len(companies) - i) / rate if rate > 0 else 0
                    logger.info(f"[{i}/{len(companies)}] ✓ {company} (elapsed: {elapsed:.0f}s, ETA: {eta:.0f}s)")
                except Exception as e:
                    logger.info(f"[{i}/{len(companies)}] ✗ {company}: {e}")
    else:
        logger.info(f"Sequential mode: {len(companies)} companies, rate limit {rate_limit}s/request")
        for i, company in enumerate(companies, 1):
            try:
                lead = enrich_lead(company, rate_limit=rate_limit)
                leads_new.append(lead)
                elapsed = time.time() - start_time
                rate = i / elapsed if elapsed > 0 else 0
                eta = (len(companies) - i) / rate if rate > 0 else 0
                logger.info(f"[{i}/{len(companies)}] ✓ {company} (elapsed: {elapsed:.0f}s, ETA: {eta:.0f}s)")
            except KeyboardInterrupt:
                logger.info(f"\nInterrupted at {i}/{len(companies)}. Saving partial results...")
                break
            except Exception as e:
                logger.info(f"[{i}/{len(companies)}] ✗ {company}: {e}")

    # Combine with existing (if --resume)
    all_leads = existing + leads_new if args.resume else leads_new

    # Write CSV
    fieldnames = [
        "name", "domain", "industry", "employee_estimate",
        "decision_maker_title", "company_summary", "description",
        "emails_found", "social_links", "email_patterns",
    ]
    with open(args.output, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for lead in all_leads:
            for key in ["emails_found", "social_links", "email_patterns"]:
                if isinstance(lead.get(key), list):
                    lead[key] = ", ".join(lead[key])
            writer.writerow(lead)

    elapsed = time.time() - start_time
    logger.info(f"\n✓ Wrote {len(all_leads)} leads ({len(leads_new)} new, {len(existing)} existing) → {args.output}")
    logger.info(f"  Elapsed: {elapsed:.0f}s")


def cmd_drafts(args):
    """Generate personalized outreach drafts."""
    if not os.path.exists(args.input):
        logger.error(f"ERROR: input file not found: {args.input}")
        sys.exit(1)

    leads = []
    with open(args.input) as f:
        reader = csv.DictReader(f)
        for row in reader:
            leads.append(row)

    if not args.pro and len(leads) > 10:
        print(f"Free tier limited to 10 drafts. You provided {len(leads)}.")
        leads = leads[:10]

    tone = args.tone
    variants = args.variants

    if args.dry_run:
        logger.info(f"\n[DRY RUN] Would generate {variants} drafts each for {len(leads)} leads")
        logger.info(f"  Tone: {tone}")
        logger.info(f"  Output: {args.output}")
        return

    drafts_output = []
    for i, lead in enumerate(leads, 1):
        prompt = f"""Write {variants} personalized cold outreach variants to a {lead.get('decision_maker_title', 'decision-maker')} at {lead.get('name', 'a company')} ({lead.get('industry', 'their industry')}).

Tone: {tone}
Company description: {lead.get('description') or lead.get('company_summary') or 'N/A'}

Each variant should be 3-4 sentences max. Start with a specific observation about their company, not a generic intro.

Format each variant as:
## Variant 1: <subject line>
<body>

## Variant 2: <subject line>
<body>

(etc.)
"""
        llm_response = call_llm(prompt, max_tokens=600)
        if llm_response:
            drafts_output.append(f"# Outreach Drafts for {lead.get('name', 'Unknown')}\n\n{llm_response}\n\n---\n")
        else:
            drafts_output.append(f"# Outreach Drafts for {lead.get('name', 'Unknown')}\n\n[LLM unavailable — add drafts manually]\n\n---\n")
        logger.info(f"[{i}/{len(leads)}] {'✓' if llm_response else '⚠'} {lead.get('name', 'Unknown')}")

    with open(args.output, "w") as f:
        f.write("\n".join(drafts_output))

    logger.info(f"\n✓ Generated drafts for {len(leads)} leads → {args.output}")


def cmd_filter(args):
    """Filter leads by employee count, industry, etc."""
    if not os.path.exists(args.input):
        logger.error(f"ERROR: input file not found: {args.input}")
        sys.exit(1)

    leads = []
    with open(args.input) as f:
        reader = csv.DictReader(f)
        for row in reader:
            leads.append(row)

    if not leads:
        logger.info("No leads in input.")
        return

    filtered = []
    for lead in leads:
        emp = lead.get("employee_estimate", "")
        if args.min_employees is not None or args.max_employees is not None:
            if not emp:
                continue
            try:
                emp_min, emp_max = emp.split("-")
                emp_min = int(emp_min)
                emp_max_str = emp_max.rstrip("+") if emp_max.endswith("+") else emp_max
                emp_max = int(emp_max_str) if emp_max_str.isdigit() else 9999
                if args.min_employees is not None and emp_max < args.min_employees:
                    continue
                if args.max_employees is not None and emp_min > args.max_employees:
                    continue
            except Exception:
                continue
        if args.industry and lead.get("industry") != args.industry:
            continue
        filtered.append(lead)

    fieldnames = list(leads[0].keys()) if leads else []
    with open(args.output, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(filtered)

    logger.info(f"\n✓ Filtered {len(leads)} → {len(filtered)} leads → {args.output}")
    if args.min_employees or args.max_employees or args.industry:
        logger.info(f"  Criteria: min={args.min_employees}, max={args.max_employees}, industry={args.industry}")


def cmd_configure(args):
    """Show / set skill configuration."""
    config = load_config()

    changed = False
    if args.respect_robots_txt is not None:
        config["respect_robots_txt"] = args.respect_robots_txt
        changed = True
    if args.rate_limit_seconds is not None:
        config["rate_limit_seconds"] = args.rate_limit_seconds
        changed = True
    if args.no_personal_emails is not None:
        config["no_personal_emails"] = args.no_personal_emails
        changed = True
    if args.max_concurrent is not None:
        config["max_concurrent"] = args.max_concurrent
        changed = True

    if changed:
        config_path = Path.home() / ".openclaw" / "lead-enrichment-scanner.json"
        config_path.parent.mkdir(parents=True, exist_ok=True)
        # Wrap with schema version
        wrapped = {"_schema_version": SCHEMA_VERSION, **config}
        with open(config_path, "w") as f:
            json.dump(wrapped, f, indent=2)
        logger.info(f"Configuration updated (schema v{SCHEMA_VERSION}):")
    else:
        logger.info(f"\nCurrent configuration:")
    for k, v in config.items():
        logger.info(f"  {k}: {v}")


def main():
    parser = argparse.ArgumentParser(description="Lead Enrichment Scanner")
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    parser.add_argument("--verbose", "-v", action="store_true", help="Enable debug logging")
    parser.add_argument("--quiet", "-q", action="store_true", help="Suppress info logging")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # enrich
    p_enrich = subparsers.add_parser("enrich", help="Enrich a list of companies")
    p_enrich.add_argument("--input", required=True, help="Input file with company names (one per line)")
    p_enrich.add_argument("--output", required=True, help="Output CSV path")
    p_enrich.add_argument("--rate-limit", type=int, default=DEFAULT_RATE_LIMIT, help="Seconds between requests")
    p_enrich.add_argument("--bulk", action="store_true", help="Use parallel processing")
    p_enrich.add_argument("--concurrency", type=int, default=None, help=f"Parallel workers (default from config, default {DEFAULT_BULK_CONCURRENCY})")
    p_enrich.add_argument("--resume", action="store_true", help="Skip already-processed companies in output file")
    p_enrich.add_argument("--dry-run", action="store_true", help="Preview what would happen without making requests")
    p_enrich.add_argument("--pro", action="store_true", help="Use pro tier (up to 500 leads)")
    p_enrich.set_defaults(func=cmd_enrich)

    # drafts
    p_drafts = subparsers.add_parser("drafts", help="Generate personalized outreach drafts")
    p_drafts.add_argument("--input", required=True, help="Input leads CSV")
    p_drafts.add_argument("--output", required=True, help="Output drafts MD")
    p_drafts.add_argument("--tone", default="consultative", help="consultative | cold | warm | follow-up | referral")
    p_drafts.add_argument("--variants", type=int, default=3, help="Number of variants per lead")
    p_drafts.add_argument("--dry-run", action="store_true", help="Preview without generating")
    p_drafts.add_argument("--pro", action="store_true", help="Use pro tier")
    p_drafts.set_defaults(func=cmd_drafts)

    # filter
    p_filter = subparsers.add_parser("filter", help="Filter leads by criteria")
    p_filter.add_argument("--input", required=True, help="Input leads CSV")
    p_filter.add_argument("--output", required=True, help="Output filtered CSV")
    p_filter.add_argument("--min-employees", type=int, help="Minimum employee count")
    p_filter.add_argument("--max-employees", type=int, help="Maximum employee count")
    p_filter.add_argument("--industry", help="Industry filter")
    p_filter.set_defaults(func=cmd_filter)

    # configure
    p_config = subparsers.add_parser("configure", help="Configure the skill")
    p_config.add_argument("--respect-robots-txt", type=lambda x: x.lower() == "true", default=None)
    p_config.add_argument("--rate-limit-seconds", type=int, default=None)
    p_config.add_argument("--no-personal-emails", type=lambda x: x.lower() == "true", default=None)
    p_config.add_argument("--max-concurrent", type=int, default=None)
    p_config.set_defaults(func=cmd_configure)

    args = parser.parse_args()
    configure_logging(verbose=getattr(args, "verbose", False), quiet=getattr(args, "quiet", False))
    logger.debug(f"lead-enrichment-scanner v{__version__}")
    args.func(args)


if __name__ == "__main__":
    main()