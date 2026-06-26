# Tooling

## check_profiles.py

Use `scripts/check_profiles.py <username>` to run a lightweight public presence check across several major platforms.

What it does:
- builds likely profile URLs
- fetches public pages
- records HTTP status
- records final URL
- records basic page title when available

What it does not do:
- deep scraping
- login
- bypassing anti-bot systems
- proof of identity

Use it as a first-pass discovery helper, then interpret results carefully.
