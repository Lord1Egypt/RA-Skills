#!/usr/bin/env python3
"""Technology Stack Fingerprinting Module for GKN-Phantom (v3.0.0).

Comprehensive, deterministic technology detection from HTTP responses, HTML
body content, favicon hashes, error pages, JavaScript globals, CDN/WAF headers,
and OS-level indicators. Produces a structured JSON fingerprint used by
downstream modules (nuclei_runner, vuln_detector, directory_fuzzer).

Capabilities:
  1. HTTP Header Analysis — Server, X-Powered-By, Set-Cookie session IDs
  2. HTML Body Analysis — meta generator tags, script src patterns, CSS
     framework patterns, CMS-specific paths and comments
  3. File/Favicon Analysis — favicon hash matching, robots.txt signatures
  4. Error Page Fingerprinting — 404/500 body analysis for framework sigs
  5. JavaScript Library Detection — window.* globals, framework patterns
  6. CDN/WAF Detection — CF-Ray, X-Cache, X-Amz-Cf-Id, X-Azure-Ref, etc.
  7. Database Detection — error message heuristics, technology pairing
  8. OS Detection — Server header case, TTL values, response characteristics

All detection is deterministic and side-effect free. Network calls have
configurable timeouts and never raise unhandled exceptions.

Usage (CLI):
  python tech_fingerprint.py --url https://target.com
  python tech_fingerprint.py --url https://target.com --headers headers.json --body body.html
  python tech_fingerprint.py --url https://target.com --output tech.json
  python tech_fingerprint.py --url https://target.com --no-fetch  (headers+body only)
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import socket
import ssl
import struct
import sys
import time
from dataclasses import dataclass, field
from typing import Any
from urllib.parse import urljoin, urlparse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from utils import load_json, dump_json, resolve_ips  # noqa: E402

# =============================================================================
# Constants & Defaults
# =============================================================================

DEFAULT_TIMEOUT = 8.0  # seconds for HTTP fetches
DEFAULT_USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/125.0.0.0 Safari/537.36"
)
CONFIDENCE_HIGH = 0.95
CONFIDENCE_MEDIUM = 0.75
CONFIDENCE_LOW = 0.50
CONFIDENCE_HEURISTIC = 0.40

# ---------------------------------------------------------------------------
# 1. HTTP Header Analysis — Server detection patterns
# ---------------------------------------------------------------------------
SERVER_PATTERNS: list[tuple[str, re.Pattern, float]] = [
    ("nginx",        re.compile(r"nginx(?:/([\d.]+))?", re.IGNORECASE),          CONFIDENCE_HIGH),
    ("Apache",       re.compile(r"Apache(?:/([\d.]+))?", re.IGNORECASE),         CONFIDENCE_HIGH),
    ("IIS",          re.compile(r"Microsoft-IIS(?:/([\d.]+))?", re.IGNORECASE),  CONFIDENCE_HIGH),
    ("Tomcat",       re.compile(r"Apache-Coyote(?:/([\d.]+))?", re.IGNORECASE),  CONFIDENCE_HIGH),
    ("Jetty",        re.compile(r"Jetty(?:[/(]?([\d.]+))?", re.IGNORECASE),     CONFIDENCE_HIGH),
    ("Caddy",        re.compile(r"Caddy\b", re.IGNORECASE),                       CONFIDENCE_HIGH),
    ("lighttpd",     re.compile(r"lighttpd(?:/([\d.]+))?", re.IGNORECASE),       CONFIDENCE_HIGH),
    ("LiteSpeed",    re.compile(r"LiteSpeed\b", re.IGNORECASE),                   CONFIDENCE_HIGH),
    ("Gunicorn",     re.compile(r"gunicorn(?:/([\d.]+))?", re.IGNORECASE),       CONFIDENCE_MEDIUM),
    ("uWSGI",        re.compile(r"uWSGI\b", re.IGNORECASE),                       CONFIDENCE_MEDIUM),
    ("openresty",    re.compile(r"openresty(?:/([\d.]+))?", re.IGNORECASE),      CONFIDENCE_MEDIUM),
    ("Tengine",      re.compile(r"Tengine(?:/([\d.]+))?", re.IGNORECASE),        CONFIDENCE_MEDIUM),
    ("Resin",        re.compile(r"Resin(?:/([\d.]+))?", re.IGNORECASE),          CONFIDENCE_MEDIUM),
    ("GlassFish",    re.compile(r"GlassFish\s*(?:Server)?\s*([\d.]+)?", re.IGNORECASE), CONFIDENCE_MEDIUM),
    ("WildFly",      re.compile(r"WildFly(?:/([\d.]+))?", re.IGNORECASE),        CONFIDENCE_MEDIUM),
    ("Undertow",     re.compile(r"Undertow\b", re.IGNORECASE),                    CONFIDENCE_MEDIUM),
    ("Node.js",      re.compile(r"Node\.js\b|express\b", re.IGNORECASE),         CONFIDENCE_LOW),
    ("Werkzeug",     re.compile(r"Werkzeug(?:/([\d.]+))?", re.IGNORECASE),       CONFIDENCE_MEDIUM),
    ("CherryPy",     re.compile(r"CherryPy(?:/([\d.]+))?", re.IGNORECASE),       CONFIDENCE_MEDIUM),
    ("TornadoServer", re.compile(r"TornadoServer(?:/([\d.]+))?", re.IGNORECASE), CONFIDENCE_MEDIUM),
    ("AkamaiGHost",  re.compile(r"AkamaiGHost\b", re.IGNORECASE),                CONFIDENCE_HIGH),
    ("Cloudflare",   re.compile(r"cloudflare\b", re.IGNORECASE),                 CONFIDENCE_HIGH),
    ("Varnish",      re.compile(r"Varnish\b", re.IGNORECASE),                    CONFIDENCE_MEDIUM),
    ("Squid",        re.compile(r"squid(?:/([\d.]+))?", re.IGNORECASE),          CONFIDENCE_MEDIUM),
    ("HAProxy",      re.compile(r"HAProxy\b", re.IGNORECASE),                     CONFIDENCE_MEDIUM),
    ("AWSALB",       re.compile(r"awselb(?:/([\d.]+))?", re.IGNORECASE),         CONFIDENCE_HIGH),
    ("Netlify",      re.compile(r"Netlify\b", re.IGNORECASE),                     CONFIDENCE_HIGH),
    ("Vercel",       re.compile(r"Vercel\b", re.IGNORECASE),                      CONFIDENCE_HIGH),
    ("Heroku",       re.compile(r"heroku\b", re.IGNORECASE),                      CONFIDENCE_MEDIUM),
    ("Python",       re.compile(r"Python/([\d.]+)", re.IGNORECASE),              CONFIDENCE_MEDIUM),
]

X_POWERED_BY_PATTERNS: list[tuple[str, re.Pattern, float]] = [
    ("PHP",         re.compile(r"PHP(?:/([\d.]+))?", re.IGNORECASE),                 CONFIDENCE_HIGH),
    ("ASP.NET",     re.compile(r"ASP\.NET\b", re.IGNORECASE),                         CONFIDENCE_HIGH),
    ("Express",     re.compile(r"Express\b", re.IGNORECASE),                           CONFIDENCE_HIGH),
    ("Next.js",     re.compile(r"Next\.js\b", re.IGNORECASE),                          CONFIDENCE_HIGH),
    ("Django",      re.compile(r"Django\b", re.IGNORECASE),                            CONFIDENCE_MEDIUM),
    ("Flask",       re.compile(r"Flask\b", re.IGNORECASE),                             CONFIDENCE_MEDIUM),
    ("Rails",       re.compile(r"Rails\b|Phusion(?:\s*Passenger)?", re.IGNORECASE),   CONFIDENCE_MEDIUM),
    ("Servlet",     re.compile(r"Servlet(?:/([\d.]+))?", re.IGNORECASE),             CONFIDENCE_HIGH),
    ("JSP",         re.compile(r"JSP(?:/([\d.]+))?", re.IGNORECASE),                 CONFIDENCE_HIGH),
    ("JSF",         re.compile(r"JSF\b", re.IGNORECASE),                               CONFIDENCE_MEDIUM),
    ("Nuxt.js",     re.compile(r"Nuxt\.?js\b", re.IGNORECASE),                         CONFIDENCE_MEDIUM),
    ("Remix",       re.compile(r"Remix\b", re.IGNORECASE),                              CONFIDENCE_MEDIUM),
    ("SvelteKit",   re.compile(r"SvelteKit\b", re.IGNORECASE),                          CONFIDENCE_MEDIUM),
    ("Astro",       re.compile(r"Astro\b", re.IGNORECASE),                              CONFIDENCE_MEDIUM),
    ("Strapi",      re.compile(r"Strapi\b", re.IGNORECASE),                             CONFIDENCE_MEDIUM),
    ("GraphQL-Yoga", re.compile(r"GraphQL[-\s]Yoga", re.IGNORECASE),                   CONFIDENCE_MEDIUM),
    ("ColdFusion",  re.compile(r"ColdFusion\b", re.IGNORECASE),                         CONFIDENCE_MEDIUM),
]

# Session cookie → technology mapping
SET_COOKIE_PATTERNS: list[tuple[str, str, str, float]] = [
    # (cookie_name_regex_snippet, technology, category, confidence)
    ("PHPSESSID",         "PHP",              "language",   CONFIDENCE_HIGH),
    ("JSESSIONID",        "Java/Tomcat",      "language",   CONFIDENCE_HIGH),
    ("ASP.NET_SessionId", "ASP.NET",          "language",   CONFIDENCE_HIGH),
    ("ASP.NET",           "ASP.NET",          "language",   CONFIDENCE_MEDIUM),
    ("laravel_session",   "Laravel",          "framework",  CONFIDENCE_HIGH),
    ("connect.sid",       "Express/Node.js",  "framework",  CONFIDENCE_HIGH),
    ("csrftoken",         "Django",           "framework",  CONFIDENCE_MEDIUM),
    ("_session_id",       "Ruby on Rails",    "framework",  CONFIDENCE_MEDIUM),
    ("CFTOKEN",           "ColdFusion",       "language",   CONFIDENCE_HIGH),
    ("CFID",              "ColdFusion",       "language",   CONFIDENCE_HIGH),
    ("JServSessionId",    "Oracle/Java",      "language",   CONFIDENCE_MEDIUM),
    ("ASPSESSIONID",      "ASP Classic",      "language",   CONFIDENCE_MEDIUM),
    ("symfony",           "Symfony",          "framework",  CONFIDENCE_MEDIUM),
    ("craft_session",     "Craft CMS",        "cms",        CONFIDENCE_MEDIUM),
    ("october_session",   "October CMS",      "cms",        CONFIDENCE_MEDIUM),
    ("shopify_s",         "Shopify",          "cms",        CONFIDENCE_MEDIUM),
    ("wordpress_logged_in","WordPress",       "cms",        CONFIDENCE_HIGH),
    ("wp-settings",       "WordPress",        "cms",        CONFIDENCE_MEDIUM),
    ("drupal",            "Drupal",           "cms",        CONFIDENCE_MEDIUM),
    ("SSESS",             "Drupal",           "cms",        CONFIDENCE_MEDIUM),
    ("joomla_user_state", "Joomla",           "cms",        CONFIDENCE_HIGH),
    ("magento",           "Magento",          "cms",        CONFIDENCE_MEDIUM),
    ("prestashop",        "PrestaShop",       "cms",        CONFIDENCE_MEDIUM),
    ("TYPO3",             "TYPO3",            "cms",        CONFIDENCE_MEDIUM),
    ("XSRF-TOKEN",        "Laravel/Lumen",    "framework",  CONFIDENCE_MEDIUM),
    ("XSRF",              "Angular",          "javascript", CONFIDENCE_LOW),
    ("sails.sid",         "Sails.js",         "framework",  CONFIDENCE_MEDIUM),
    ("koa.sid",           "Koa.js",           "framework",  CONFIDENCE_MEDIUM),
    ("feathers-jwt",      "Feathers.js",      "framework",  CONFIDENCE_MEDIUM),
    ("next-auth.session", "Next.js",          "framework",  CONFIDENCE_HIGH),
    ("__Host-next-auth",  "Next.js",          "framework",  CONFIDENCE_HIGH),
    ("__session",         "Firebase",         "platform",   CONFIDENCE_MEDIUM),
    ("ARRAffinity",       "Azure App Service","platform",   CONFIDENCE_HIGH),
    ("AWSALB",            "AWS ALB",          "platform",   CONFIDENCE_HIGH),
    ("AWSELB",            "AWS ELB",          "platform",   CONFIDENCE_HIGH),
    ("GCLB",              "GCP Load Balancer","platform",   CONFIDENCE_MEDIUM),
]

# ---------------------------------------------------------------------------
# 2. HTML Body Analysis patterns
# ---------------------------------------------------------------------------
META_GENERATOR_PATTERNS: list[tuple[str, re.Pattern, float]] = [
    ("WordPress",  re.compile(r'<meta[^>]*\bname\s*=\s*["\']?generator["\']?[^>]*\bcontent\s*=\s*["\']?WordPress\s*([\d.]*)', re.IGNORECASE), CONFIDENCE_HIGH),
    ("Drupal",     re.compile(r'<meta[^>]*\bname\s*=\s*["\']?generator["\']?[^>]*\bcontent\s*=\s*["\']?Drupal\s*([\d.]*)', re.IGNORECASE),    CONFIDENCE_HIGH),
    ("Joomla",     re.compile(r'<meta[^>]*\bname\s*=\s*["\']?generator["\']?[^>]*\bcontent\s*=\s*["\']?Joomla!?\s*[\-\s]*([\d.]*)', re.IGNORECASE), CONFIDENCE_HIGH),
    ("Shopify",    re.compile(r'<meta[^>]*\bname\s*=\s*["\']?generator["\']?[^>]*\bcontent\s*=\s*["\']?Shopify', re.IGNORECASE),            CONFIDENCE_MEDIUM),
    ("Magento",    re.compile(r'<meta[^>]*\bname\s*=\s*["\']?generator["\']?[^>]*\bcontent\s*=\s*["\']?Magento', re.IGNORECASE),            CONFIDENCE_MEDIUM),
    ("MediaWiki",  re.compile(r'<meta[^>]*\bname\s*=\s*["\']?generator["\']?[^>]*\bcontent\s*=\s*["\']?MediaWiki\s*([\d.]*)', re.IGNORECASE), CONFIDENCE_HIGH),
    ("Ghost",      re.compile(r'<meta[^>]*\bname\s*=\s*["\']?generator["\']?[^>]*\bcontent\s*=\s*["\']?Ghost\s*([\d.]*)', re.IGNORECASE),  CONFIDENCE_HIGH),
    ("Hugo",       re.compile(r'<meta[^>]*\bname\s*=\s*["\']?generator["\']?[^>]*\bcontent\s*=\s*["\']?Hugo\s*([\d.]*)', re.IGNORECASE),   CONFIDENCE_HIGH),
    ("Jekyll",     re.compile(r'<meta[^>]*\bname\s*=\s*["\']?generator["\']?[^>]*\bcontent\s*=\s*["\']?Jekyll\s*([\d.]*)', re.IGNORECASE), CONFIDENCE_HIGH),
    ("Hexo",       re.compile(r'<meta[^>]*\bname\s*=\s*["\']?generator["\']?[^>]*\bcontent\s*=\s*["\']?Hexo', re.IGNORECASE),              CONFIDENCE_MEDIUM),
    ("Zendesk",    re.compile(r'<meta[^>]*\bname\s*=\s*["\']?generator["\']?[^>]*\bcontent\s*=\s*["\']?Zendesk', re.IGNORECASE),           CONFIDENCE_MEDIUM),
    ("Wix",        re.compile(r'<meta[^>]*\bname\s*=\s*["\']?generator["\']?[^>]*\bcontent\s*=\s*["\']?Wix\.com', re.IGNORECASE),          CONFIDENCE_HIGH),
    ("Squarespace",re.compile(r'<meta[^>]*\bname\s*=\s*["\']?generator["\']?[^>]*\bcontent\s*=\s*["\']?Squarespace', re.IGNORECASE),       CONFIDENCE_HIGH),
    ("Weebly",     re.compile(r'<meta[^>]*\bname\s*=\s*["\']?generator["\']?[^>]*\bcontent\s*=\s*["\']?Weebly', re.IGNORECASE),           CONFIDENCE_MEDIUM),
    ("TYPO3",      re.compile(r'<meta[^>]*\bname\s*=\s*["\']?generator["\']?[^>]*\bcontent\s*=\s*["\']?TYPO3', re.IGNORECASE),            CONFIDENCE_MEDIUM),
    ("PrestaShop", re.compile(r'<meta[^>]*\bname\s*=\s*["\']?generator["\']?[^>]*\bcontent\s*=\s*["\']?PrestaShop', re.IGNORECASE),       CONFIDENCE_MEDIUM),
    ("OpenCart",   re.compile(r'<meta[^>]*\bname\s*=\s*["\']?generator["\']?[^>]*\bcontent\s*=\s*["\']?OpenCart', re.IGNORECASE),         CONFIDENCE_MEDIUM),
    ("WooCommerce",re.compile(r'<meta[^>]*\bname\s*=\s*["\']?generator["\']?[^>]*\bcontent\s*=\s*["\']?WooCommerce\s*([\d.]*)', re.IGNORECASE), CONFIDENCE_HIGH),
    ("DNN",        re.compile(r'<meta[^>]*\bname\s*=\s*["\']?generator["\']?[^>]*\bcontent\s*=\s*["\']?DotNetNuke', re.IGNORECASE),       CONFIDENCE_HIGH),
    ("Umbraco",    re.compile(r'<meta[^>]*\bname\s*=\s*["\']?generator["\']?[^>]*\bcontent\s*=\s*["\']?Umbraco', re.IGNORECASE),          CONFIDENCE_MEDIUM),
    ("Sitecore",   re.compile(r'<meta[^>]*\bname\s*=\s*["\']?generator["\']?[^>]*\bcontent\s*=\s*["\']?Sitecore', re.IGNORECASE),         CONFIDENCE_MEDIUM),
    ("Kentico",    re.compile(r'<meta[^>]*\bname\s*=\s*["\']?generator["\']?[^>]*\bcontent\s*=\s*["\']?Kentico', re.IGNORECASE),          CONFIDENCE_MEDIUM),
    ("Episerver",  re.compile(r'<meta[^>]*\bname\s*=\s*["\']?generator["\']?[^>]*\bcontent\s*=\s*["\']?Episerver', re.IGNORECASE),        CONFIDENCE_MEDIUM),
    ("Salesforce", re.compile(r'<meta[^>]*\bname\s*=\s*["\']?generator["\']?[^>]*\bcontent\s*=\s*["\']?Salesforce', re.IGNORECASE),       CONFIDENCE_MEDIUM),
    ("HubSpot",    re.compile(r'<meta[^>]*\bname\s*=\s*["\']?generator["\']?[^>]*\bcontent\s*=\s*["\']?HubSpot', re.IGNORECASE),          CONFIDENCE_MEDIUM),
]

# Script src patterns for JS frameworks
SCRIPT_FRAMEWORK_PATTERNS: list[tuple[str, re.Pattern, float]] = [
    ("jQuery",        re.compile(r"(?:jquery)[\-.]([\d.]+)(?:\.min)?\.js", re.IGNORECASE),             CONFIDENCE_HIGH),
    ("React",         re.compile(r"(?:react)(?:\.production|\.development)?[\-.]([\d.]+)(?:\.min)?\.js", re.IGNORECASE), CONFIDENCE_HIGH),
    ("Vue.js",        re.compile(r"(?:vue)[\-.]([\d.]+)(?:\.min)?\.js", re.IGNORECASE),                CONFIDENCE_HIGH),
    ("Angular",       re.compile(r"(?:angular)[\-.]([\d.]+)(?:\.min)?\.js", re.IGNORECASE),            CONFIDENCE_HIGH),
    ("Bootstrap",     re.compile(r"(?:bootstrap)[\-.]([\d.]+)(?:\.min)?\.(?:js|css)", re.IGNORECASE),  CONFIDENCE_HIGH),
    ("Tailwind CSS",  re.compile(r"(?:tailwindcss)[@/\-.]([\d.]+)", re.IGNORECASE),                      CONFIDENCE_MEDIUM),
    ("Alpine.js",     re.compile(r"(?:alpine)[\-.]([\d.]+)(?:\.min)?\.js", re.IGNORECASE),             CONFIDENCE_HIGH),
    ("D3.js",         re.compile(r"(?:d3)[\-.]([\d.]+)(?:\.min)?\.js", re.IGNORECASE),                 CONFIDENCE_HIGH),
    ("Lodash",        re.compile(r"(?:lodash)[\-.]([\d.]+)(?:\.min)?\.js", re.IGNORECASE),             CONFIDENCE_HIGH),
    ("Axios",         re.compile(r"(?:axios)[\-.]([\d.]+)(?:\.min)?\.js", re.IGNORECASE),              CONFIDENCE_MEDIUM),
    ("Moment.js",     re.compile(r"(?:moment)(?:-with-locales)?[\-.]([\d.]+)(?:\.min)?\.js", re.IGNORECASE), CONFIDENCE_HIGH),
    ("Next.js",       re.compile(r"/_next/static/", re.IGNORECASE),                                      CONFIDENCE_HIGH),
    ("Nuxt.js",       re.compile(r"/_nuxt/", re.IGNORECASE),                                             CONFIDENCE_HIGH),
    ("Gatsby",        re.compile(r"webpack-runtime-|\/static\/[a-f0-9]{20,}\/", re.IGNORECASE),         CONFIDENCE_LOW),
    ("Svelte",        re.compile(r"(?:svelte)[\-.]([\d.]+)(?:\.min)?\.js", re.IGNORECASE),              CONFIDENCE_MEDIUM),
    ("Ember.js",      re.compile(r"(?:ember)(?:\.debug)?[\-.]([\d.]+)(?:\.min)?\.js", re.IGNORECASE),   CONFIDENCE_MEDIUM),
    ("Backbone.js",   re.compile(r"(?:backbone)[\-.]([\d.]+)(?:\.min)?\.js", re.IGNORECASE),            CONFIDENCE_MEDIUM),
    ("Three.js",      re.compile(r"(?:three)[\-.]([\d.]+)(?:\.min)?\.js", re.IGNORECASE),               CONFIDENCE_MEDIUM),
    ("Chart.js",      re.compile(r"(?:chart)(?:\.min)?\.js|Chart\.bundle[\-.]", re.IGNORECASE),         CONFIDENCE_MEDIUM),
    ("Highcharts",    re.compile(r"(?:highcharts)[\-.]([\d.]+)(?:\.min)?\.js", re.IGNORECASE),          CONFIDENCE_MEDIUM),
    ("Socket.io",     re.compile(r"(?:socket\.io)[\-.]([\d.]+)(?:\.min)?\.js", re.IGNORECASE),          CONFIDENCE_MEDIUM),
    ("GSAP",          re.compile(r"(?:gsap|TweenMax|TweenLite)[\-.]([\d.]+)(?:\.min)?\.js", re.IGNORECASE), CONFIDENCE_MEDIUM),
    ("DataTables",    re.compile(r"(?:datatables)[\-.]([\d.]+)(?:\.min)?\.js", re.IGNORECASE),          CONFIDENCE_MEDIUM),
    ("Select2",       re.compile(r"(?:select2)[\-.]([\d.]+)(?:\.min)?\.js", re.IGNORECASE),             CONFIDENCE_MEDIUM),
    ("Fancybox",      re.compile(r"(?:fancybox|fancybox)[\-.]([\d.]+)(?:\.min)?\.js", re.IGNORECASE),   CONFIDENCE_MEDIUM),
    ("Swiper",        re.compile(r"(?:swiper)(?:-bundle)?[\-.]([\d.]+)(?:\.min)?\.js", re.IGNORECASE),  CONFIDENCE_MEDIUM),
    ("AOS",           re.compile(r"(?:aos)[\-.]([\d.]+)(?:\.min)?\.js", re.IGNORECASE),                 CONFIDENCE_MEDIUM),
    ("Anime.js",      re.compile(r"(?:anime)[\-.]([\d.]+)(?:\.min)?\.js", re.IGNORECASE),               CONFIDENCE_MEDIUM),
    ("Popper.js",     re.compile(r"(?:popper|popperjs)[\-.]([\d.]+)(?:\.min)?\.js", re.IGNORECASE),     CONFIDENCE_MEDIUM),
]

# CMS-specific path patterns in HTML
CMS_PATH_PATTERNS: list[tuple[str, re.Pattern, float]] = [
    ("WordPress", re.compile(r"/wp-content/|/wp-includes/|/wp-json/|/wp-admin/", re.IGNORECASE),           CONFIDENCE_HIGH),
    ("Drupal",    re.compile(r"/sites/default/files/|/sites/all/modules/|/sites/all/themes/", re.IGNORECASE), CONFIDENCE_HIGH),
    ("Joomla",    re.compile(r"/components/com_|/modules/mod_|/templates/|/administrator/", re.IGNORECASE),   CONFIDENCE_HIGH),
    ("Magento",   re.compile(r"/skin/frontend/|/media/catalog/|/js/mage/", re.IGNORECASE),                   CONFIDENCE_HIGH),
    ("Shopify",   re.compile(r"cdn\.shopify\.com|/cdn/shop/", re.IGNORECASE),                                 CONFIDENCE_HIGH),
    ("Wix",       re.compile(r"static\.wixstatic\.com|wix-code-sdk", re.IGNORECASE),                          CONFIDENCE_HIGH),
    ("Squarespace", re.compile(r"static\d\.squarespace\.com|assets\.squarespace\.com", re.IGNORECASE),         CONFIDENCE_HIGH),
    ("Weebly",    re.compile(r"cdn\d?\.editmysite\.com", re.IGNORECASE),                                      CONFIDENCE_MEDIUM),
    ("TYPO3",     re.compile(r"/typo3conf/|/typo3temp/|/fileadmin/", re.IGNORECASE),                          CONFIDENCE_HIGH),
    ("PrestaShop", re.compile(r"/modules/block|/themes/(?:classic|default-bootstrap)/", re.IGNORECASE),       CONFIDENCE_MEDIUM),
    ("OpenCart",  re.compile(r"/catalog/view/theme/|/image/catalog/", re.IGNORECASE),                         CONFIDENCE_MEDIUM),
    ("Ghost",     re.compile(r"/ghost/(?:api|admin)/", re.IGNORECASE),                                        CONFIDENCE_MEDIUM),
    ("DNN",       re.compile(r"/desktopmodules/|/portals/_default/", re.IGNORECASE),                          CONFIDENCE_HIGH),
    ("Umbraco",   re.compile(r"/umbraco/|/App_Plugins/", re.IGNORECASE),                                      CONFIDENCE_MEDIUM),
    ("Sitecore",  re.compile(r"/sitecore/|/layouts/system/", re.IGNORECASE),                                  CONFIDENCE_MEDIUM),
]

# ---------------------------------------------------------------------------
# 3. Favicon hash mapping — known CMS favicon hashes (mmh3)
# ---------------------------------------------------------------------------
FAVICON_HASH_MAP: dict[int, tuple[str, str, float]] = {
    # (hash, (name, category, confidence))
    -1588080585: ("WordPress",     "cms", CONFIDENCE_MEDIUM),
    -1395402739: ("Drupal",        "cms", CONFIDENCE_MEDIUM),
    116323821:   ("Joomla",        "cms", CONFIDENCE_MEDIUM),
    708578229:   ("Magento 1.x",   "cms", CONFIDENCE_MEDIUM),
    -1354933624: ("Magento 2.x",   "cms", CONFIDENCE_MEDIUM),
    -2094477505: ("Shopify",       "cms", CONFIDENCE_MEDIUM),
    -1776962843: ("PrestaShop",    "cms", CONFIDENCE_LOW),
    1754232066:  ("TYPO3",         "cms", CONFIDENCE_LOW),
    297217411:   ("Apache Tomcat", "server", CONFIDENCE_MEDIUM),
    321909464:   ("Jenkins",       "tool",  CONFIDENCE_HIGH),
    951731271:   ("GitLab",        "tool",  CONFIDENCE_HIGH),
    -299494129:  ("phpMyAdmin",    "tool",  CONFIDENCE_HIGH),
    -1089739228: ("Roundcube",     "tool",  CONFIDENCE_MEDIUM),
    -207225348:  ("Grafana",       "tool",  CONFIDENCE_MEDIUM),
    2106676461:  ("Jira",          "tool",  CONFIDENCE_MEDIUM),
    399194098:   ("Confluence",    "tool",  CONFIDENCE_MEDIUM),
    -1188645861: ("Spring Boot",   "framework", CONFIDENCE_MEDIUM),
    -27781056:   ("SAP NetWeaver", "app",   CONFIDENCE_MEDIUM),
    603314:      ("Nginx default", "server", CONFIDENCE_LOW),
}

# robots.txt signature patterns
ROBOTS_TXT_SIGNATURES: list[tuple[str, re.Pattern, float]] = [
    ("WordPress", re.compile(r"Disallow:\s*/wp-admin/", re.IGNORECASE),              CONFIDENCE_HIGH),
    ("Drupal",    re.compile(r"Disallow:\s*/node/add/", re.IGNORECASE),              CONFIDENCE_MEDIUM),
    ("Joomla",    re.compile(r"Disallow:\s*/administrator/", re.IGNORECASE),         CONFIDENCE_HIGH),
    ("Magento",   re.compile(r"Disallow:\s*/index\.php/", re.IGNORECASE),            CONFIDENCE_MEDIUM),
    ("TYPO3",     re.compile(r"Disallow:\s*/typo3/", re.IGNORECASE),                 CONFIDENCE_HIGH),
    ("MediaWiki", re.compile(r"Disallow:\s*/wiki/Special:", re.IGNORECASE),          CONFIDENCE_MEDIUM),
    ("DNN",       re.compile(r"Disallow:\s*/desktopmodules/", re.IGNORECASE),        CONFIDENCE_MEDIUM),
    ("Moodle",    re.compile(r"Disallow:\s*/login/forgot_password\.php", re.IGNORECASE), CONFIDENCE_MEDIUM),
]

# ---------------------------------------------------------------------------
# 4. Error page fingerprinting patterns
# ---------------------------------------------------------------------------
ERROR_PAGE_PATTERNS: list[tuple[str, str, re.Pattern, float]] = [
    # (technology, category, pattern, confidence)
    ("Spring Boot",       "framework", re.compile(r"Whitelabel Error Page|This application has no explicit mapping for /error", re.IGNORECASE), CONFIDENCE_HIGH),
    ("Django",            "framework", re.compile(r"Page not found \(404\)|Request Method:|Using the URLconf defined in|You're seeing this error because you have <code>DEBUG\s*=\s*True</code>", re.IGNORECASE), CONFIDENCE_HIGH),
    ("Laravel",           "framework", re.compile(r"Whoops, looks like something went wrong\.|MethodNotAllowedHttpException|NotFoundHttpException|Illuminate\\\\", re.IGNORECASE), CONFIDENCE_HIGH),
    ("ASP.NET YSOD",      "framework", re.compile(r"Server Error in '/' Application\.|Description: An unhandled exception occurred|<b> Exception Details: </b>|Stack Trace:", re.IGNORECASE), CONFIDENCE_HIGH),
    ("Tomcat",            "server",    re.compile(r"Apache Tomcat/[\d.]+\s*-\s*Error report", re.IGNORECASE),    CONFIDENCE_HIGH),
    ("nginx",             "server",    re.compile(r"<title>404 Not Found</title>\s*</head>\s*<body>\s*<center><h1>404 Not Found</h1></center>\s*<hr><center>nginx", re.IGNORECASE), CONFIDENCE_HIGH),
    ("PHP",               "language",  re.compile(r"<b>Warning</b>:|on line <b>\d+</b>|Fatal error:|Uncaught Error:", re.IGNORECASE), CONFIDENCE_HIGH),
    ("IIS",               "server",    re.compile(r"The resource cannot be found\.|HTTP Error 404|Server Error in '/' Application|IIS \d+\.\d+ Detailed Error", re.IGNORECASE), CONFIDENCE_HIGH),
    ("Express",           "framework", re.compile(r"<pre>Cannot (?:GET|POST|PUT|DELETE|PATCH) /[^<]*</pre>", re.IGNORECASE),  CONFIDENCE_MEDIUM),
    ("Flask",             "framework", re.compile(r"werkzeug\.debug|Debugger PIN:", re.IGNORECASE),              CONFIDENCE_HIGH),
    ("Ruby on Rails",     "framework", re.compile(r"Rails\.root:|Action Controller: Exception caught|Routing Error", re.IGNORECASE), CONFIDENCE_HIGH),
    ("Next.js",           "framework", re.compile(r"Application error: a (?:client|server)-side exception has occurred", re.IGNORECASE), CONFIDENCE_MEDIUM),
    ("Nuxt.js",           "framework", re.compile(r"An error occurred in the app and your page could not be served", re.IGNORECASE), CONFIDENCE_MEDIUM),
    ("ColdFusion",        "language",  re.compile(r"Error Occurred While Processing Request|The web site you are accessing has experienced an unexpected error", re.IGNORECASE), CONFIDENCE_HIGH),
    ("Oracle App Server", "server",    re.compile(r"Oracle Application Server|Oracle Containers for J2EE", re.IGNORECASE), CONFIDENCE_MEDIUM),
    ("WebLogic",          "server",    re.compile(r"WebLogic Server|Error 404--Not Found.*WebLogic", re.IGNORECASE), CONFIDENCE_HIGH),
    ("WebSphere",         "server",    re.compile(r"WebSphere Application Server|IBM HTTP Server", re.IGNORECASE), CONFIDENCE_MEDIUM),
    ("Jetty",             "server",    re.compile(r"Jetty://|Powered by Jetty", re.IGNORECASE),                   CONFIDENCE_HIGH),
    ("GlassFish",         "server",    re.compile(r"GlassFish Server", re.IGNORECASE),                            CONFIDENCE_MEDIUM),
    ("WildFly",           "server",    re.compile(r"WildFly\s+\d+|JBoss EAP", re.IGNORECASE),                    CONFIDENCE_MEDIUM),
]

# ---------------------------------------------------------------------------
# 5. JavaScript library detection via window globals
# ---------------------------------------------------------------------------
JS_GLOBAL_PATTERNS: list[tuple[str, str, list[str], float]] = [
    # (name, category, [global_var_patterns], confidence)
    ("jQuery",       "javascript", ["window\\.jQuery", "window\\.\\$", "jQuery"],                                 CONFIDENCE_HIGH),
    ("React",        "javascript", ["window\\.React", "ReactDOM", "__REACT_DEVTOOLS_GLOBAL_HOOK__"],              CONFIDENCE_HIGH),
    ("Vue.js",       "javascript", ["window\\.Vue", "__VUE_DEVTOOLS_GLOBAL_HOOK__", "window\\.__VUE__"],          CONFIDENCE_HIGH),
    ("Angular",      "javascript", ["window\\.angular", "ng\\.version", "angular\\.version"],                      CONFIDENCE_HIGH),
    ("Alpine.js",    "javascript", ["window\\.Alpine", "Alpine\\.data"],                                          CONFIDENCE_HIGH),
    ("D3.js",        "javascript", ["window\\.d3", "d3\\.version"],                                               CONFIDENCE_MEDIUM),
    ("Lodash",       "javascript", ["window\\._", "\\._\\."],                                                     CONFIDENCE_MEDIUM),
    ("Moment.js",    "javascript", ["window\\.moment", "moment\\(\\)\\.format"],                                  CONFIDENCE_MEDIUM),
    ("Axios",        "javascript", ["window\\.axios", "axios\\.defaults"],                                        CONFIDENCE_MEDIUM),
    ("Three.js",     "javascript", ["window\\.THREE", "THREE\\.WebGLRenderer"],                                   CONFIDENCE_MEDIUM),
    ("Socket.io",    "javascript", ["window\\.io", "io\\.connect"],                                               CONFIDENCE_MEDIUM),
    ("GSAP",         "javascript", ["window\\.gsap", "gsap\\.to", "TweenMax"],                                    CONFIDENCE_MEDIUM),
    ("Ember.js",     "javascript", ["window\\.Ember", "Ember\\.VERSION"],                                         CONFIDENCE_MEDIUM),
    ("Backbone.js",  "javascript", ["window\\.Backbone", "Backbone\\.VERSION"],                                   CONFIDENCE_MEDIUM),
    ("Svelte",       "javascript", ["__svelte", "svelte\\$", "SvelteComponent"],                                  CONFIDENCE_MEDIUM),
    ("Stripe",       "javascript", ["window\\.Stripe", "Stripe\\(\\)", "stripe\\.elements"],                       CONFIDENCE_MEDIUM),
    ("Google Maps",  "javascript", ["google\\.maps", "window\\.google\\.maps", "google\\.maps\\.Map"],             CONFIDENCE_HIGH),
    ("Google Analytics", "javascript", ["gtag\\(", "ga\\(", "window\\.ga", "_gaq", "google-analytics\\.com"],     CONFIDENCE_HIGH),
    ("Facebook Pixel","javascript", ["fbq\\(", "window\\.fbq", "connect\\.facebook\\.net"],                        CONFIDENCE_MEDIUM),
    ("Hotjar",       "javascript", ["window\\.hj\\(", "hj\\(", "hotjar\\.com"],                                   CONFIDENCE_MEDIUM),
    ("Sentry",       "javascript", ["Sentry\\.init", "Raven\\.config", "window\\.Sentry"],                        CONFIDENCE_MEDIUM),
    ("Intercom",     "javascript", ["Intercom\\(", "window\\.Intercom"],                                          CONFIDENCE_MEDIUM),
    ("Mixpanel",     "javascript", ["mixpanel\\.init", "mixpanel\\.track"],                                       CONFIDENCE_MEDIUM),
    ("Segment",      "javascript", ["analytics\\.load", "analytics\\.page", "window\\.analytics"],                CONFIDENCE_MEDIUM),
]

# ---------------------------------------------------------------------------
# 6. CDN / WAF header detection
# ---------------------------------------------------------------------------
CDN_WAF_HEADERS: list[tuple[str, str, str, str, float]] = [
    # (header_name_lower, match_pattern, provider, category, confidence)
    ("cf-ray",                  r"^[\da-f]{8,}-[A-Z]{3,}$", "Cloudflare",     "cdn", CONFIDENCE_HIGH),
    ("cf-cache-status",         r".",                         "Cloudflare",     "cdn", CONFIDENCE_HIGH),
    ("x-amz-cf-id",             r".",                         "AWS CloudFront", "cdn", CONFIDENCE_HIGH),
    ("x-amz-cf-pop",            r".",                         "AWS CloudFront", "cdn", CONFIDENCE_HIGH),
    ("x-cache",                 r"Hit from cloudfront",       "AWS CloudFront", "cdn", CONFIDENCE_HIGH),
    ("x-cache",                 r"HIT",                       "Fastly",         "cdn", CONFIDENCE_MEDIUM),
    ("x-served-by",             r"cache-",                    "Fastly",         "cdn", CONFIDENCE_MEDIUM),
    ("x-cache",                 r"TCP_HIT",                   "Akamai",         "cdn", CONFIDENCE_MEDIUM),
    ("x-cache",                 r"HIT|MISS",                  "Varnish",        "cdn", CONFIDENCE_LOW),
    ("x-azure-ref",             r".",                         "Azure CDN",      "cdn", CONFIDENCE_HIGH),
    ("x-azure-ref-originshield", r".",                        "Azure CDN",      "cdn", CONFIDENCE_MEDIUM),
    ("x-cdn",                   r".",                         "Generic CDN",    "cdn", CONFIDENCE_LOW),
    ("x-vercel-cache",          r".",                         "Vercel",         "cdn", CONFIDENCE_HIGH),
    ("x-vercel-id",             r".",                         "Vercel",         "cdn", CONFIDENCE_HIGH),
    ("x-nf-request-id",         r".",                         "Netlify",        "cdn", CONFIDENCE_HIGH),
    ("server-timing",           r"cdn-cache",                 "Generic CDN",    "cdn", CONFIDENCE_LOW),
    ("x-fastly-request-id",     r".",                         "Fastly",         "cdn", CONFIDENCE_HIGH),
    ("x-ws-request-id",         r".",                         "WAF",            "waf", CONFIDENCE_LOW),
    ("x-sucuri-id",             r".",                         "Sucuri",         "waf", CONFIDENCE_HIGH),
    ("x-sucuri-cache",          r".",                         "Sucuri",         "waf", CONFIDENCE_HIGH),
    ("x-iinfo",                 r".",                         "Incapsula",      "waf", CONFIDENCE_MEDIUM),
    ("x-cdn-incap",             r".",                         "Incapsula",      "waf", CONFIDENCE_MEDIUM),
    ("x-distil-cs",             r".",                         "Distil Networks","waf", CONFIDENCE_HIGH),
    ("x-waf-le",                r".",                         "WAF",            "waf", CONFIDENCE_LOW),
]

# ---------------------------------------------------------------------------
# 7. Database inference patterns
# ---------------------------------------------------------------------------
DB_ERROR_PATTERNS: list[tuple[str, str, re.Pattern, float]] = [
    ("MySQL",       "database", re.compile(r"MySQL\s*(?:server|fetch|error|Warning)|SQL syntax.*MySQL|mysql_fetch|mysqli_|#1267|#1366", re.IGNORECASE),    CONFIDENCE_HIGH),
    ("PostgreSQL",  "database", re.compile(r"PostgreSQL|pg_query\(\)|pg_exec\(\)|UndefinedTable:\s*|ERROR:\s*\w+\s*at or near", re.IGNORECASE),             CONFIDENCE_HIGH),
    ("MSSQL",       "database", re.compile(r"SQL Server|Microsoft OLE DB|ODBC SQL Server Driver|SQLServer|mssql_|\[Microsoft\]\[ODBC", re.IGNORECASE),     CONFIDENCE_HIGH),
    ("Oracle",      "database", re.compile(r"ORA-\d{4,5}|Oracle\s*Database|Oracle error|oci8|PLS-|TNS:", re.IGNORECASE),                                   CONFIDENCE_HIGH),
    ("SQLite",      "database", re.compile(r"SQLite|sqlite3?::|unable to open database file", re.IGNORECASE),                                              CONFIDENCE_MEDIUM),
    ("MongoDB",     "database", re.compile(r"MongoDB|MongoError|MongoServerError|BSONError", re.IGNORECASE),                                               CONFIDENCE_MEDIUM),
    ("Redis",       "database", re.compile(r"Redis|ERR wrong number of arguments|READONLY You can.t write against a read only", re.IGNORECASE),          CONFIDENCE_MEDIUM),
    ("Elasticsearch","database",re.compile(r"Elasticsearch|elastic|es_rejected_execution|index_not_found_exception", re.IGNORECASE),                       CONFIDENCE_MEDIUM),
    ("MariaDB",     "database", re.compile(r"MariaDB", re.IGNORECASE),                                                                                     CONFIDENCE_MEDIUM),
    ("Cassandra",   "database", re.compile(r"Cassandra|cqlsh|cassandra\.cluster", re.IGNORECASE),                                                          CONFIDENCE_LOW),
    ("Firebase",    "database", re.compile(r"firebaseio\.com|firestore|firebase\.database", re.IGNORECASE),                                                 CONFIDENCE_MEDIUM),
    ("Supabase",    "database", re.compile(r"supabase\.co", re.IGNORECASE),                                                                                 CONFIDENCE_MEDIUM),
]

# Technology → database pairing heuristics
TECH_DB_PAIRINGS: dict[str, list[tuple[str, float]]] = {
    "PHP":        [("MySQL", 0.70), ("MariaDB", 0.50), ("PostgreSQL", 0.15)],
    "WordPress":  [("MySQL", 0.95), ("MariaDB", 0.60)],
    "Drupal":     [("MySQL", 0.70), ("PostgreSQL", 0.40), ("SQLite", 0.20)],
    "Joomla":     [("MySQL", 0.80), ("PostgreSQL", 0.20)],
    "Magento":    [("MySQL", 0.85), ("MariaDB", 0.40)],
    "Laravel":    [("MySQL", 0.75), ("PostgreSQL", 0.30), ("SQLite", 0.15)],
    "ASP.NET":    [("MSSQL", 0.90), ("Oracle", 0.10)],
    "Java":       [("Oracle", 0.40), ("PostgreSQL", 0.30), ("MySQL", 0.20), ("MSSQL", 0.10)],
    "Tomcat":     [("Oracle", 0.35), ("PostgreSQL", 0.25), ("MySQL", 0.25), ("MSSQL", 0.15)],
    "Spring Boot":[("PostgreSQL", 0.35), ("MySQL", 0.35), ("H2", 0.15), ("Oracle", 0.15)],
    "Django":     [("PostgreSQL", 0.70), ("SQLite", 0.20), ("MySQL", 0.10)],
    "Flask":      [("PostgreSQL", 0.40), ("SQLite", 0.35), ("MySQL", 0.25)],
    "Rails":      [("PostgreSQL", 0.60), ("MySQL", 0.30), ("SQLite", 0.10)],
    "Node.js":    [("MongoDB", 0.50), ("PostgreSQL", 0.25), ("MySQL", 0.15), ("Redis", 0.10)],
    "Express":    [("MongoDB", 0.40), ("PostgreSQL", 0.30), ("MySQL", 0.20), ("Redis", 0.10)],
    "Next.js":    [("PostgreSQL", 0.40), ("MySQL", 0.20), ("MongoDB", 0.15), ("Supabase", 0.15)],
    "Strapi":     [("PostgreSQL", 0.35), ("MySQL", 0.35), ("SQLite", 0.20), ("MongoDB", 0.10)],
}

# ---------------------------------------------------------------------------
# 8. OS detection indicators
# ---------------------------------------------------------------------------
OS_INDICATORS: list[tuple[str, re.Pattern, float]] = [
    ("Linux",   re.compile(r"Linux|Ubuntu|Debian|CentOS|Red\s*Hat|Fedora|Alpine|SUSE|Gentoo|Arch", re.IGNORECASE),     CONFIDENCE_LOW),
    ("Windows", re.compile(r"Win32|Win64|Windows\s*(?:NT|Server)\s*[\d.]+|IIS", re.IGNORECASE),                         CONFIDENCE_LOW),
    ("FreeBSD", re.compile(r"FreeBSD", re.IGNORECASE),                                                                  CONFIDENCE_MEDIUM),
    ("OpenBSD", re.compile(r"OpenBSD", re.IGNORECASE),                                                                  CONFIDENCE_MEDIUM),
    ("NetBSD",  re.compile(r"NetBSD", re.IGNORECASE),                                                                   CONFIDENCE_MEDIUM),
    ("Solaris", re.compile(r"Solaris|SunOS|Sun\s*Java", re.IGNORECASE),                                                CONFIDENCE_LOW),
    ("AIX",     re.compile(r"AIX", re.IGNORECASE),                                                                      CONFIDENCE_MEDIUM),
]

# Server header → OS hints
SERVER_OS_HINTS: dict[str, str] = {
    "IIS":             "Windows",
    "Microsoft-IIS":   "Windows",
    "Tomcat":          "Linux",
    "nginx":           "Linux",
    "Apache":          "Linux",
    "lighttpd":        "Linux",
    "LiteSpeed":       "Linux",
    "Gunicorn":        "Linux",
    "uWSGI":           "Linux",
    "openresty":       "Linux",
    "Caddy":           "Linux",
    "Undertow":        "Linux",
    "WildFly":         "Linux",
    "GlassFish":       "Linux",
    "Resin":           "Linux",
    "Werkzeug":        "Linux",
    "CherryPy":        "Linux",
    "TornadoServer":   "Linux",
    "AkamaiGHost":     "Linux",
    "Varnish":         "Linux",
    "Node.js":         "Linux",
    "AWSALB":          "Linux",
}


# =============================================================================
# Dataclasses
# =============================================================================

@dataclass
class TechDetection:
    """A single technology detection with confidence."""
    name: str
    category: str  # server | language | framework | cms | javascript | cdn | waf | database | os
    confidence: float
    version: str = ""
    evidence: str = ""
    evidence_type: str = ""  # header | body | cookie | pattern | heuristic


@dataclass
class TechFingerprint:
    """Complete technology fingerprint result."""
    server: list[TechDetection] = field(default_factory=list)
    language: list[TechDetection] = field(default_factory=list)
    framework: list[TechDetection] = field(default_factory=list)
    cms: list[TechDetection] = field(default_factory=list)
    javascript: list[TechDetection] = field(default_factory=list)
    cdn: list[TechDetection] = field(default_factory=list)
    waf: list[TechDetection] = field(default_factory=list)
    database: list[TechDetection] = field(default_factory=list)
    os: list[TechDetection] = field(default_factory=list)
    platform: list[TechDetection] = field(default_factory=list)
    tool: list[TechDetection] = field(default_factory=list)
    raw_headers: dict[str, str] = field(default_factory=dict)
    url: str = ""
    timestamp: str = ""

    def to_dict(self) -> dict[str, Any]:
        """Serialize to JSON-compatible dict."""
        result: dict[str, Any] = {"url": self.url, "timestamp": self.timestamp}
        for cat in ("server", "language", "framework", "cms", "javascript",
                     "cdn", "waf", "database", "os", "platform", "tool"):
            dets = getattr(self, cat, [])
            result[cat] = [self._det_to_dict(d) for d in dets]
        return result

    @staticmethod
    def _det_to_dict(d: TechDetection) -> dict[str, Any]:
        out: dict[str, Any] = {
            "name": d.name,
            "category": d.category,
            "confidence": round(d.confidence, 2),
        }
        if d.version:
            out["version"] = d.version
        if d.evidence:
            out["evidence"] = d.evidence[:500]
        if d.evidence_type:
            out["evidence_type"] = d.evidence_type
        return out

    def get_top(self, category: str, n: int = 3) -> list[TechDetection]:
        """Return top N detections for a category sorted by confidence desc."""
        dets = getattr(self, category, [])
        return sorted(dets, key=lambda d: d.confidence, reverse=True)[:n]

    def get_names(self, category: str) -> list[str]:
        """Return unique detection names for a category."""
        dets = getattr(self, category, [])
        return sorted({d.name for d in dets})


# =============================================================================
# HTTP fetch helpers
# =============================================================================

def _http_fetch(
    url: str,
    timeout: float = DEFAULT_TIMEOUT,
    extra_headers: dict[str, str] | None = None,
) -> tuple[int, dict[str, str], str]:
    """Fetch URL via urllib, returning (status_code, headers_dict, body).

    Never raises. Returns (0, {}, "") on any error.
    """
    from urllib.request import Request, urlopen
    from urllib.error import HTTPError, URLError

    headers: dict[str, str] = {
        "User-Agent": DEFAULT_USER_AGENT,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
    }
    if extra_headers:
        headers.update(extra_headers)

    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    try:
        req = Request(url, headers=headers)
        resp = urlopen(req, timeout=timeout, context=ctx)
        body = resp.read().decode("utf-8", errors="replace")
        hdrs: dict[str, str] = {}
        for k, v in resp.getheaders():
            hdrs[k.lower()] = v
        return (resp.getcode(), hdrs, body)
    except HTTPError as e:
        body = e.read().decode("utf-8", errors="replace") if e.fp else ""
        hdrs = {}
        if hasattr(e, "headers") and e.headers:
            for k, v in e.headers.items():
                hdrs[k.lower()] = v
        return (e.code, hdrs, body)
    except (URLError, OSError, ValueError, TimeoutError):
        return (0, {}, "")


def _fetch_favicon(base_url: str, timeout: float = DEFAULT_TIMEOUT) -> bytes | None:
    """Fetch favicon.ico from the target. Returns raw bytes or None."""
    from urllib.request import Request, urlopen
    from urllib.error import HTTPError, URLError

    favicon_url = urljoin(base_url, "/favicon.ico")
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    try:
        req = Request(favicon_url, headers={"User-Agent": DEFAULT_USER_AGENT})
        resp = urlopen(req, timeout=timeout, context=ctx)
        return resp.read()
    except (HTTPError, URLError, OSError, ValueError, TimeoutError):
        return None


def _fetch_robots(base_url: str, timeout: float = DEFAULT_TIMEOUT) -> str:
    """Fetch robots.txt from the target. Returns text or ''."""
    robots_url = urljoin(base_url, "/robots.txt")
    _, _, body = _http_fetch(robots_url, timeout=timeout)
    return body


def _fetch_error_page(
    base_url: str,
    path: str = "/gkn-phantom-nonexistent-404-test",
    timeout: float = DEFAULT_TIMEOUT,
) -> tuple[int, dict[str, str], str]:
    """Fetch a nonexistent path to trigger error pages."""
    error_url = urljoin(base_url.rstrip("/") + "/", path.lstrip("/"))
    return _http_fetch(error_url, timeout=timeout)


# =============================================================================
# Favicon hashing (mmh3-compatible)
# =============================================================================

def _mmh3_32(data: bytes, seed: int = 0) -> int:
    """Pure Python implementation of MurmurHash3 32-bit (x86, 32-bit).

    Matches the common mmh3 hash used by Shodan/favicon fingerprinting tools.
    """
    nblocks = len(data) // 4
    h1 = seed
    c1 = 0xCC9E2D51
    c2 = 0x1B873593

    for i in range(nblocks):
        k1 = struct.unpack_from("<I", data, i * 4)[0]
        k1 = (k1 * c1) & 0xFFFFFFFF
        k1 = ((k1 << 15) | (k1 >> 17)) & 0xFFFFFFFF
        k1 = (k1 * c2) & 0xFFFFFFFF
        h1 ^= k1
        h1 = ((h1 << 13) | (h1 >> 19)) & 0xFFFFFFFF
        h1 = ((h1 * 5 + 0xE6546B64) & 0xFFFFFFFF)

    tail = data[nblocks * 4:]
    k1 = 0
    if len(tail) >= 3:
        k1 ^= tail[2] << 16
    if len(tail) >= 2:
        k1 ^= tail[1] << 8
    if len(tail) >= 1:
        k1 ^= tail[0]
        k1 = (k1 * c1) & 0xFFFFFFFF
        k1 = ((k1 << 15) | (k1 >> 17)) & 0xFFFFFFFF
        k1 = (k1 * c2) & 0xFFFFFFFF
        h1 ^= k1

    h1 ^= len(data)
    h1 ^= (h1 >> 16)
    h1 = (h1 * 0x85EBCA6B) & 0xFFFFFFFF
    h1 ^= (h1 >> 13)
    h1 = (h1 * 0xC2B2AE35) & 0xFFFFFFFF
    h1 ^= (h1 >> 16)

    # Convert to signed 32-bit
    return h1 - 0x100000000 if h1 >= 0x80000000 else h1


def _b64encode_favicon(favicon_bytes: bytes) -> str:
    """Return base64-encoded favicon data (for evidence/serialization)."""
    import base64
    return base64.b64encode(favicon_bytes).decode("ascii")


# =============================================================================
# 1. HTTP Header Analysis
# =============================================================================

def analyze_headers(headers: dict[str, str]) -> list[TechDetection]:
    """Analyze HTTP response headers for technology indicators."""
    detections: list[TechDetection] = []

    # Server header
    server_header = headers.get("server", "")
    if server_header:
        for name, pattern, confidence in SERVER_PATTERNS:
            m = pattern.search(server_header)
            if m:
                version = m.group(1) if m.lastindex and m.lastindex >= 1 else ""
                detections.append(TechDetection(
                    name=name,
                    category="server",
                    confidence=confidence,
                    version=version or "",
                    evidence=f"Server: {server_header}",
                    evidence_type="header",
                ))

    # X-Powered-By header
    xpb = headers.get("x-powered-by", "")
    if xpb:
        for name, pattern, confidence in X_POWERED_BY_PATTERNS:
            m = pattern.search(xpb)
            if m:
                version = m.group(1) if m.lastindex and m.lastindex >= 1 else ""
                detections.append(TechDetection(
                    name=name,
                    category=_infer_category(name),
                    confidence=confidence,
                    version=version or "",
                    evidence=f"X-Powered-By: {xpb}",
                    evidence_type="header",
                ))

    # Set-Cookie analysis
    for cookie_line in headers.get("set-cookie", "").split(","):
        cookie_line = cookie_line.strip()
        for cookie_name, tech, category, confidence in SET_COOKIE_PATTERNS:
            if cookie_name.lower() in cookie_line.lower():
                detections.append(TechDetection(
                    name=tech,
                    category=category,
                    confidence=confidence,
                    evidence=cookie_line[:200],
                    evidence_type="cookie",
                ))

    return detections


def _infer_category(name: str) -> str:
    """Infer broad category from technology name."""
    servers = {"nginx", "Apache", "IIS", "Tomcat", "Jetty", "Caddy", "lighttpd",
               "LiteSpeed", "Gunicorn", "uWSGI", "openresty", "Tengine", "Resin",
               "GlassFish", "WildFly", "Undertow", "Werkzeug", "CherryPy",
               "TornadoServer", "AkamaiGHost", "Cloudflare", "Varnish", "Squid",
               "HAProxy", "AWSALB", "Netlify", "Vercel", "Heroku"}
    frameworks = {"Laravel", "Express", "Django", "Flask", "Rails", "Next.js",
                  "Nuxt.js", "Remix", "SvelteKit", "Astro", "Strapi", "Symfony",
                  "Craft CMS", "October CMS", "DNN"}
    cms_set = {"WordPress", "Drupal", "Joomla", "Magento", "Shopify", "PrestaShop",
               "TYPO3", "OpenCart", "Ghost", "WooCommerce"}
    if name in servers:
        return "server"
    if name in frameworks:
        return "framework"
    if name in cms_set:
        return "cms"
    return "language"


# =============================================================================
# 2. HTML Body Analysis
# =============================================================================

def analyze_html_body(body: str) -> list[TechDetection]:
    """Analyze HTML body for technology indicators."""
    detections: list[TechDetection] = []

    if not body:
        return detections

    # Meta generator tags
    for name, pattern, confidence in META_GENERATOR_PATTERNS:
        m = pattern.search(body)
        if m:
            version = ""
            if m.lastindex and m.lastindex >= 1:
                version = (m.group(1) or "").strip()
            detections.append(TechDetection(
                name=name,
                category=_classify_meta_tech(name),
                confidence=confidence,
                version=version,
                evidence=m.group(0)[:200],
                evidence_type="meta",
            ))

    # Script src patterns
    for name, pattern, confidence in SCRIPT_FRAMEWORK_PATTERNS:
        m = pattern.search(body)
        if m:
            version = ""
            if m.lastindex and m.lastindex >= 1:
                version = (m.group(1) or "").strip()
            cat = "javascript"
            if name in ("Next.js", "Nuxt.js", "Gatsby"):
                cat = "framework"
            detections.append(TechDetection(
                name=name,
                category=cat,
                confidence=confidence,
                version=version,
                evidence=m.group(0)[:200],
                evidence_type="script_src",
            ))

    # CMS-specific paths
    for name, pattern, confidence in CMS_PATH_PATTERNS:
        m = pattern.search(body)
        if m:
            detections.append(TechDetection(
                name=name,
                category="cms",
                confidence=confidence,
                evidence=m.group(0)[:200],
                evidence_type="html_path",
            ))

    # CSS framework patterns
    detections.extend(_detect_css_frameworks(body))

    return detections


def _detect_css_frameworks(body: str) -> list[TechDetection]:
    """Detect CSS frameworks from link/class patterns."""
    dets: list[TechDetection] = []
    patterns: list[tuple[str, re.Pattern, float]] = [
        ("Bootstrap",   re.compile(r'(?:bootstrap)(?:\.min)?\.css|class\s*=\s*"[^"]*\b(?:container|row|col-(?:xs|sm|md|lg|xl)-\d+)\b', re.IGNORECASE), CONFIDENCE_HIGH),
        ("Tailwind CSS",re.compile(r'(?:tailwindcss|tailwind\.config)|class\s*=\s*"[^"]*\b(?:flex\s|grid\s|bg-(?:red|blue|green|gray|white|black)-\d+|text-(?:xs|sm|base|lg|xl|2xl))', re.IGNORECASE), CONFIDENCE_MEDIUM),
        ("Bulma",       re.compile(r'(?:bulma)(?:\.min)?\.css|class\s*=\s*"[^"]*\b(?:is-(?:primary|link|info|success|warning|danger))', re.IGNORECASE), CONFIDENCE_MEDIUM),
        ("Foundation",  re.compile(r'(?:foundation)(?:\.min)?\.css|class\s*=\s*"[^"]*\b(?:small-\d+|medium-\d+|large-\d+|columns)', re.IGNORECASE), CONFIDENCE_MEDIUM),
        ("Materialize", re.compile(r'(?:materialize)(?:\.min)?\.css', re.IGNORECASE), CONFIDENCE_HIGH),
        ("Semantic UI", re.compile(r'(?:semantic)(?:\.min)?\.css|class\s*=\s*"[^"]*\bui\s+(?:button|card|grid|menu|segment)', re.IGNORECASE), CONFIDENCE_MEDIUM),
        ("UIKit",       re.compile(r'(?:uikit)(?:\.min)?\.css|class\s*=\s*"[^"]*\buk-(?:button|card|grid|nav|table)', re.IGNORECASE), CONFIDENCE_MEDIUM),
        ("Skeleton",    re.compile(r'(?:skeleton)(?:\.min)?\.css', re.IGNORECASE), CONFIDENCE_MEDIUM),
        ("Pure.css",    re.compile(r'(?:pure)(?:\.min)?\.css', re.IGNORECASE), CONFIDENCE_MEDIUM),
        ("Milligram",   re.compile(r'(?:milligram)(?:\.min)?\.css', re.IGNORECASE), CONFIDENCE_LOW),
        ("Chakra UI",   re.compile(r'@chakra-ui|chakra-ui', re.IGNORECASE), CONFIDENCE_MEDIUM),
        ("MUI",         re.compile(r'@mui/material|@emotion/react', re.IGNORECASE), CONFIDENCE_MEDIUM),
        ("Ant Design",  re.compile(r'antd(?:\.min)?\.css|ant-design', re.IGNORECASE), CONFIDENCE_MEDIUM),
        ("Element UI",  re.compile(r'element-ui|el-(?:button|form|table|dialog)', re.IGNORECASE), CONFIDENCE_MEDIUM),
    ]
    for name, pattern, confidence in patterns:
        if pattern.search(body):
            dets.append(TechDetection(
                name=name, category="javascript", confidence=confidence,
                evidence="CSS framework pattern matched", evidence_type="css",
            ))
    return dets


def _classify_meta_tech(name: str) -> str:
    """Determine category for meta generator technology."""
    cms_set = {"WordPress", "Drupal", "Joomla", "Magento", "Shopify", "TYPO3",
               "PrestaShop", "OpenCart", "Ghost", "WooCommerce", "DNN", "Umbraco",
               "Sitecore", "Kentico", "Episerver", "Salesforce", "Wix",
               "Squarespace", "Weebly", "Zendesk", "MediaWiki", "Hugo", "Jekyll", "Hexo"}
    if name in cms_set:
        return "cms"
    return "framework"


# =============================================================================
# 3. Favicon / robots.txt Analysis
# =============================================================================

def analyze_favicon(favicon_bytes: bytes | None) -> list[TechDetection]:
    """Analyze favicon by computing mmh3 hash and matching against known hashes."""
    detections: list[TechDetection] = []
    if not favicon_bytes:
        return detections

    try:
        h = _mmh3_32(favicon_bytes)
    except (struct.error, IndexError):
        return detections

    if h in FAVICON_HASH_MAP:
        name, category, confidence = FAVICON_HASH_MAP[h]
        detections.append(TechDetection(
            name=name,
            category=category,
            confidence=confidence,
            evidence=f"favicon mmh3 hash: {h}",
            evidence_type="favicon",
        ))

    return detections


def analyze_robots(body: str) -> list[TechDetection]:
    """Analyze robots.txt for CMS signatures."""
    detections: list[TechDetection] = []
    if not body:
        return detections

    for name, pattern, confidence in ROBOTS_TXT_SIGNATURES:
        if pattern.search(body):
            detections.append(TechDetection(
                name=name,
                category="cms",
                confidence=confidence,
                evidence=f"robots.txt contains {name} signature",
                evidence_type="robots",
            ))

    return detections


# =============================================================================
# 4. Error Page Fingerprinting
# =============================================================================

def analyze_error_page(body: str, status_code: int = 0) -> list[TechDetection]:
    """Analyze error page body for framework/server signatures."""
    detections: list[TechDetection] = []
    if not body:
        return detections

    for tech_name, category, pattern, confidence in ERROR_PAGE_PATTERNS:
        m = pattern.search(body)
        if m:
            detections.append(TechDetection(
                name=tech_name,
                category=category,
                confidence=confidence,
                evidence=m.group(0)[:300],
                evidence_type="error_page",
            ))

    # Also check for generic stack traces
    if re.search(r'(?:stack\s*trace|backtrace|at\s+\w+\.\w+:\d+:\d+)', body, re.IGNORECASE):
        detections.append(TechDetection(
            name="Stack Trace Exposure",
            category="framework",
            confidence=CONFIDENCE_MEDIUM,
            evidence="Stack trace found in error page",
            evidence_type="error_page",
        ))

    return detections


# =============================================================================
# 5. JavaScript Library Detection
# =============================================================================

def analyze_javascript_globals(html_body: str, js_files: list[str] | None = None) -> list[TechDetection]:
    """Detect JavaScript libraries from window globals and inline scripts."""
    detections: list[TechDetection] = []
    if not html_body:
        return detections

    for name, category, glob_patterns, confidence in JS_GLOBAL_PATTERNS:
        for pat in glob_patterns:
            if re.search(pat, html_body):
                detections.append(TechDetection(
                    name=name,
                    category=category,
                    confidence=confidence,
                    evidence=f"matched global pattern: {pat[:80]}",
                    evidence_type="js_global",
                ))
                break  # one match per library is enough

    # Detect inline framework usage
    detections.extend(_detect_inline_js_frameworks(html_body))
    return detections


def _detect_inline_js_frameworks(body: str) -> list[TechDetection]:
    """Detect frameworks from inline JS patterns."""
    dets: list[TechDetection] = []
    inline_patterns: list[tuple[str, str, re.Pattern, float]] = [
        ("Vue.js",    "javascript", re.compile(r'(?:Vue\.createApp|new\s+Vue\s*\(|Vue\.component\()', re.IGNORECASE), CONFIDENCE_HIGH),
        ("React",     "javascript", re.compile(r'(?:ReactDOM\.(?:render|createRoot|hydrate)|React\.createElement|createRoot\()', re.IGNORECASE), CONFIDENCE_HIGH),
        ("Angular",   "javascript", re.compile(r'(?:platformBrowserDynamic\(\)|NgModule\s*\(|Component\s*\()', re.IGNORECASE), CONFIDENCE_HIGH),
        ("Alpine.js", "javascript", re.compile(r'(?:x-data\s*=|x-show|x-bind|x-on:|@click)', re.IGNORECASE), CONFIDENCE_HIGH),
        ("HTMX",      "javascript", re.compile(r'(?:hx-get|hx-post|hx-trigger|htmx\.org)', re.IGNORECASE), CONFIDENCE_HIGH),
        ("Stimulus",  "javascript", re.compile(r'(?:data-controller\s*=\s*"|data-action\s*=\s*"|stimulus)', re.IGNORECASE), CONFIDENCE_MEDIUM),
        ("Livewire",  "javascript", re.compile(r'(?:wire:click|wire:model|wire:submit|Livewire)', re.IGNORECASE), CONFIDENCE_HIGH),
        ("Petite-Vue","javascript", re.compile(r'(?:PetiteVue\.createApp)', re.IGNORECASE), CONFIDENCE_MEDIUM),
        ("Solid.js",  "javascript", re.compile(r'(?:solid-js|createSignal|createEffect)', re.IGNORECASE), CONFIDENCE_MEDIUM),
        ("Preact",    "javascript", re.compile(r'(?:preact|h\(|render\(.*,\s*document)', re.IGNORECASE), CONFIDENCE_LOW),
        ("Lit",       "javascript", re.compile(r'(?:LitElement|html`<|css`\n|@customElement)', re.IGNORECASE), CONFIDENCE_MEDIUM),
    ]

    for name, category, pattern, confidence in inline_patterns:
        if pattern.search(body):
            dets.append(TechDetection(
                name=name, category=category, confidence=confidence,
                evidence="inline JS framework pattern matched", evidence_type="js_inline",
            ))
    return dets


# =============================================================================
# 6. CDN/WAF Detection
# =============================================================================

def analyze_cdn_waf(headers: dict[str, str]) -> list[TechDetection]:
    """Detect CDN and WAF from response headers."""
    detections: list[TechDetection] = []

    for header_name, match_pattern, provider, category, confidence in CDN_WAF_HEADERS:
        header_val = headers.get(header_name, "")
        if header_val and re.search(match_pattern, header_val):
            detections.append(TechDetection(
                name=provider,
                category=category,
                confidence=confidence,
                evidence=f"{header_name}: {header_val[:150]}",
                evidence_type="header",
            ))

    return detections


# =============================================================================
# 7. Database Detection
# =============================================================================

def analyze_database(
    error_body: str = "",
    tech_fingerprint: TechFingerprint | None = None,
) -> list[TechDetection]:
    """Infer database from error messages and technology pairings."""
    detections: list[TechDetection] = []

    # 7a. Direct error message detection
    if error_body:
        for name, category, pattern, confidence in DB_ERROR_PATTERNS:
            m = pattern.search(error_body)
            if m:
                detections.append(TechDetection(
                    name=name,
                    category=category,
                    confidence=confidence,
                    evidence=m.group(0)[:200],
                    evidence_type="error",
                ))

    # 7b. Technology pairing heuristics
    if tech_fingerprint:
        detections.extend(_infer_db_from_tech_stack(tech_fingerprint))

    return detections


def _infer_db_from_tech_stack(fp: TechFingerprint) -> list[TechDetection]:
    """Apply technology→database pairing heuristics."""
    detections: list[TechDetection] = []

    # Extract all language/framework/CMS names
    tech_names: set[str] = set()
    for cat in ("language", "framework", "cms", "server"):
        for det in getattr(fp, cat, []):
            tech_names.add(det.name)

    seen_dbs: set[str] = set()
    for tech_name in tech_names:
        pairings = TECH_DB_PAIRINGS.get(tech_name, [])
        for db_name, confidence in pairings:
            if db_name not in seen_dbs:
                seen_dbs.add(db_name)
                # Adjust confidence: heuristic-based, so cap at 0.60
                adjusted = min(confidence, 0.60)
                detections.append(TechDetection(
                    name=db_name,
                    category="database",
                    confidence=adjusted,
                    evidence=f"Inferred from technology pairing: {tech_name} → {db_name}",
                    evidence_type="heuristic",
                ))

    return detections


# =============================================================================
# 8. OS Detection
# =============================================================================

def analyze_os(
    headers: dict[str, str],
    server_detections: list[TechDetection] | None = None,
    body: str = "",
) -> list[TechDetection]:
    """Infer operating system from server header and response characteristics."""
    detections: list[TechDetection] = []

    # 8a. Server header → OS mapping
    server_header = headers.get("server", "")
    for srv_name, os_name in SERVER_OS_HINTS.items():
        if srv_name.lower() in server_header.lower():
            detections.append(TechDetection(
                name=os_name,
                category="os",
                confidence=CONFIDENCE_LOW,
                evidence=f"Server header suggests {os_name}: {server_header}",
                evidence_type="header",
            ))

    # 8b. IIS → Windows (strong signal)
    if "Microsoft-IIS" in server_header or "IIS" in server_header:
        detections.append(TechDetection(
            name="Windows",
            category="os",
            confidence=CONFIDENCE_MEDIUM,
            evidence=f"Server header indicates Windows: {server_header}",
            evidence_type="header",
        ))

    # 8c. Body-based OS hints (from error pages, etc.)
    if body:
        for os_name, pattern, confidence in OS_INDICATORS:
            if pattern.search(body):
                detections.append(TechDetection(
                    name=os_name,
                    category="os",
                    confidence=confidence,
                    evidence=f"Body content suggests {os_name}",
                    evidence_type="body",
                ))

    # 8d. Check for additional Windows indicators
    if re.search(r"ASP\.NET|\.aspx|\.ashx", body, re.IGNORECASE) and not any(
        d.name == "Windows" for d in detections
    ):
        detections.append(TechDetection(
            name="Windows",
            category="os",
            confidence=CONFIDENCE_HEURISTIC,
            evidence="ASP.NET artifacts suggest Windows",
            evidence_type="heuristic",
        ))

    return detections


# =============================================================================
# Epoch timestamp helper
# =============================================================================

def _now_iso() -> str:
    """Return current UTC timestamp as ISO-8601."""
    from datetime import datetime, timezone
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


# =============================================================================
# Main Fingerprint Orchestrator
# =============================================================================

def fingerprint(
    url: str,
    headers: dict[str, str] | None = None,
    body: str | None = None,
    fetch: bool = True,
    timeout: float = DEFAULT_TIMEOUT,
) -> TechFingerprint:
    """Run the complete technology fingerprint pipeline.

    Args:
        url: Target base URL.
        headers: Pre-fetched response headers dict (key→value, lowercased keys).
        body: Pre-fetched response body.
        fetch: If True, fetch headers/body from url when not provided.
        timeout: Network timeout in seconds.

    Returns:
        A populated TechFingerprint with all detection results.
    """
    fp = TechFingerprint(url=url, timestamp=_now_iso())

    # Fetch if needed
    if fetch and (headers is None or body is None):
        status, fetched_headers, fetched_body = _http_fetch(url, timeout=timeout)
        if headers is None:
            headers = fetched_headers
        if body is None:
            body = fetched_body

    headers = headers or {}
    body = body or ""

    fp.raw_headers = dict(headers)

    # 1. Header analysis
    fp.server.extend([d for d in analyze_headers(headers) if d.category == "server"])
    fp.language.extend([d for d in analyze_headers(headers) if d.category == "language"])
    fp.cms.extend([d for d in analyze_headers(headers) if d.category == "cms"])
    fp.framework.extend([d for d in analyze_headers(headers) if d.category == "framework"])
    fp.platform.extend([d for d in analyze_headers(headers) if d.category == "platform"])

    # 2. HTML body analysis
    body_dets = analyze_html_body(body)
    for d in body_dets:
        if d.category == "cms":
            fp.cms.append(d)
        elif d.category == "javascript":
            fp.javascript.append(d)
        elif d.category == "framework":
            fp.framework.append(d)
        else:
            fp.framework.append(d)

    # 3. Favicon analysis
    if fetch:
        favicon_bytes = _fetch_favicon(url, timeout=timeout)
        fp.tool.extend(analyze_favicon(favicon_bytes))

        # robots.txt analysis
        robots_body = _fetch_robots(url, timeout=timeout)
        fp.cms.extend(analyze_robots(robots_body))

    # 4. Error page fingerprinting
    if fetch:
        err_status, err_headers, err_body = _fetch_error_page(url, timeout=timeout)
        fp.framework.extend(analyze_error_page(err_body, err_status))
        fp.server.extend(analyze_error_page(err_body, err_status))
        # Also use error body for DB detection
        fp.database.extend(analyze_database(error_body=err_body))
    else:
        fp.database.extend(analyze_database(error_body=""))

    # 5. JavaScript library detection
    fp.javascript.extend(analyze_javascript_globals(body))

    # 6. CDN/WAF detection
    cdn_waf_dets = analyze_cdn_waf(headers)
    for d in cdn_waf_dets:
        if d.category == "cdn":
            fp.cdn.append(d)
        elif d.category == "waf":
            fp.waf.append(d)

    # 7. Database detection (heuristic from tech stack)
    fp.database.extend(_infer_db_from_tech_stack(fp))

    # 8. OS detection
    fp.os.extend(analyze_os(headers, fp.server, body))

    # Deduplicate within each category by name
    _deduplicate(fp)

    return fp


def _deduplicate(fp: TechFingerprint) -> None:
    """Remove duplicate detections within each category, keeping highest confidence."""
    for cat in ("server", "language", "framework", "cms", "javascript",
                 "cdn", "waf", "database", "os", "platform", "tool"):
        dets: list[TechDetection] = getattr(fp, cat, [])
        best: dict[str, TechDetection] = {}
        for d in dets:
            key = d.name.lower()
            if key not in best or d.confidence > best[key].confidence:
                best[key] = d
        setattr(fp, cat, sorted(best.values(), key=lambda x: x.confidence, reverse=True))


# =============================================================================
# CLI
# =============================================================================

def main() -> int:
    ap = argparse.ArgumentParser(
        description="GKN-Phantom Technology Stack Fingerprinting Module (v3.0)"
    )
    ap.add_argument(
        "--url", required=True,
        help="Target base URL (e.g., https://target.com)"
    )
    ap.add_argument(
        "--headers",
        help="Path to pre-fetched headers JSON file (key: value, all lower-cased keys)"
    )
    ap.add_argument(
        "--body",
        help="Path to pre-fetched HTML body file (UTF-8 text)"
    )
    ap.add_argument(
        "--no-fetch", action="store_true",
        help="Disable network fetching (requires --headers and --body)"
    )
    ap.add_argument(
        "--timeout", type=float, default=DEFAULT_TIMEOUT,
        help=f"Network timeout in seconds (default: {DEFAULT_TIMEOUT})"
    )
    ap.add_argument(
        "--output", "-o",
        help="Output JSON file path (default: stdout)"
    )
    args = ap.parse_args()

    # Load pre-fetched data if provided
    headers: dict[str, str] | None = None
    body: str | None = None

    if args.headers:
        loaded = load_json(args.headers)
        if isinstance(loaded, dict):
            # Normalize keys to lowercase
            headers = {str(k).lower(): str(v) for k, v in loaded.items()}

    if args.body:
        with open(args.body, "r", encoding="utf-8") as fh:
            body = fh.read()

    fp = fingerprint(
        url=args.url,
        headers=headers,
        body=body,
        fetch=not args.no_fetch,
        timeout=args.timeout,
    )

    output_json = dump_json(fp.to_dict())

    if args.output:
        with open(args.output, "w", encoding="utf-8") as fh:
            fh.write(output_json + "\n")
        print(f"tech_fingerprint: output written to {args.output}", file=sys.stderr)
    else:
        print(output_json)

    return 0


if __name__ == "__main__":
    sys.exit(main())
