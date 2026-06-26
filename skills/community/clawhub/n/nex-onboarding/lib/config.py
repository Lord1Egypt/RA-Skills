"""
Nex Onboarding - Configuration
MIT-0 License - Copyright 2026 Nex AI (Kevin Blancaflor)
"""

import os
from pathlib import Path

# Data directory
DATA_DIR = Path.home() / ".nex-onboarding"
DATA_DIR.mkdir(parents=True, exist_ok=True)

# Database
DB_PATH = DATA_DIR / "onboarding.db"

# Templates directory
TEMPLATES_DIR = DATA_DIR / "templates"
TEMPLATES_DIR.mkdir(parents=True, exist_ok=True)

# Step categories
CATEGORIES = ["admin", "technical", "design", "content", "communication", "delivery", "qa"]

# Step statuses
STATUSES = ["pending", "in_progress", "completed", "skipped", "blocked"]

# Onboarding statuses
ONBOARDING_STATUSES = ["active", "completed", "paused", "cancelled"]

# Retainer tiers
RETAINER_TIERS = ["starter", "standard", "premium", "enterprise"]

# Default onboarding template for Nex AI (web agency)
DEFAULT_CHECKLIST = [
    {
        "step": 1,
        "title": "Contract & betaling",
        "description": "Contract getekend en eerste betaling ontvangen",
        "category": "admin",
        "required": True,
    },
    {
        "step": 2,
        "title": "Subdomein aanmaken",
        "description": "demo.klantnaam.nex-ai.be configureren op Cloudflare",
        "category": "technical",
        "required": True,
    },
    {
        "step": 3,
        "title": "GHL sub-account",
        "description": "GoHighLevel sub-account aanmaken en configureren",
        "category": "technical",
        "required": True,
    },
    {
        "step": 4,
        "title": "Demo website bouwen",
        "description": "Demo site klaarzetten op subdomein",
        "category": "delivery",
        "required": True,
    },
    {
        "step": 5,
        "title": "Logo & branding opvragen",
        "description": "Logo, kleuren, fonts opvragen bij klant",
        "category": "design",
        "required": True,
    },
    {
        "step": 6,
        "title": "Content verzamelen",
        "description": "Teksten, foto's, testimonials opvragen",
        "category": "content",
        "required": True,
    },
    {
        "step": 7,
        "title": "Welkomstmail sturen",
        "description": "Onboarding welkomstmail met timeline en verwachtingen",
        "category": "communication",
        "required": True,
    },
    {
        "step": 8,
        "title": "Kickoff call plannen",
        "description": "Eerste videocall inplannen met klant",
        "category": "communication",
        "required": True,
    },
    {
        "step": 9,
        "title": "DNS overdracht",
        "description": "Domein verwijzen naar nieuwe hosting/Cloudflare",
        "category": "technical",
        "required": False,
    },
    {
        "step": 10,
        "title": "Google Analytics/Search Console",
        "description": "Analytics en Search Console instellen",
        "category": "technical",
        "required": False,
    },
    {
        "step": 11,
        "title": "SSL certificaat",
        "description": "SSL instellen via Cloudflare",
        "category": "technical",
        "required": True,
    },
    {
        "step": 12,
        "title": "Email forwarding",
        "description": "Email forwarding configureren voor klant domein",
        "category": "technical",
        "required": False,
    },
    {
        "step": 13,
        "title": "Formulieren testen",
        "description": "Contactformulieren en automations testen",
        "category": "qa",
        "required": True,
    },
    {
        "step": 14,
        "title": "Mobiel testen",
        "description": "Website testen op mobiel en tablet",
        "category": "qa",
        "required": True,
    },
    {
        "step": 15,
        "title": "Go-live check",
        "description": "Laatste controle voor go-live",
        "category": "qa",
        "required": True,
    },
    {
        "step": 16,
        "title": "Domein live zetten",
        "description": "DNS naar productie wijzigen",
        "category": "technical",
        "required": True,
    },
    {
        "step": 17,
        "title": "Klant training",
        "description": "Korte training over CMS/dashboard gebruik",
        "category": "communication",
        "required": False,
    },
    {
        "step": 18,
        "title": "Handover documentatie",
        "description": "Login gegevens en handleiding delen",
        "category": "delivery",
        "required": True,
    },
    {
        "step": 19,
        "title": "Feedback vragen",
        "description": "Na 1 week: feedback en tevredenheid checken",
        "category": "communication",
        "required": True,
    },
    {
        "step": 20,
        "title": "Afronding",
        "description": "Onboarding afsluiten, overgaan naar retainer support",
        "category": "admin",
        "required": True,
    },
]
