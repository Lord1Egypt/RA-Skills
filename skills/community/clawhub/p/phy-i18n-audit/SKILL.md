---
name: i18n Audit
description: i18n key coverage auditor for multi-locale codebases. Diffs every locale file against the base locale to find missing translation keys, untranslated values (value identical to source language), empty strings masquerading as translations, and orphaned keys that exist in secondary locales but not in the base. Supports JSON (i18next, react-intl, vue-i18n), YAML (Rails i18n), PO/POT (gettext), ARB (Flutter), and nested/namespaced key structures. Reports a per-locale coverage percentage, flags the highest-impact missing keys (used in the most templates), and generates a CI fail-gate command. Zero external API — pure local file analysis. Triggers on "missing translations", "i18n coverage", "untranslated keys", "locale audit", "which strings are not translated", "/i18n-audit".
license: Apache-2.0
homepage: https://canlah.ai
metadata:
  author: Canlah AI
  version: "1.0.3"
  tags:
    - i18n
    - internationalization
    - localization
    - translation
    - developer-tools
    - code-quality
    - react
    - vue
    - rails
    - flutter
---

# i18n Coverage Auditor

You add a new feature. You add the English string. You ship. Three days later, your French users see `dashboard.analytics.export_button` instead of a button label — and they file a support ticket.

This skill diffs every locale file against your base locale, tells you exactly what's missing in each language, and gives you the CI command to stop it from happening again.

**Supports JSON, YAML, PO, and ARB. Works with any framework. Zero external API.**

---

## Trigger Phrases

- "missing translations", "which strings are not translated"
- "i18n coverage", "locale audit", "translation coverage"
- "untranslated keys", "missing locale keys", "translation gaps"
- "i18next audit", "vue-i18n check", "rails i18n missing"
- "flutter arb missing", "gettext po missing"
- "/i18n-audit"

---

## How to Provide Input

```bash
# Option 1: Audit the current directory (auto-detect locale files)
/i18n-audit

# Option 2: Specific locale directory
/i18n-audit locales/
/i18n-audit src/i18n/
/i18n-audit config/locales/   # Rails

# Option 3: Specify base locale
/i18n-audit --base en
/i18n-audit --base en-US

# Option 4: Check a specific target locale
/i18n-audit --locale zh-CN
/i18n-audit --locale fr

# Option 5: Set coverage threshold for CI
/i18n-audit --min-coverage 95

# Option 6: Show only missing keys (no orphans, no untranslated)
/i18n-audit --missing-only

# Option 7: Output a ready-to-fill translation file
/i18n-audit --scaffold zh-TW
# Generates zh-TW.json with all missing keys as empty strings
```

---

## Step 1: Discover Locale Files

```bash
# Auto-detect locale file format and location
python3 -c "
import os, glob

# Common i18n directory patterns
patterns = [
    'src/i18n/**/*.json',
    'src/locales/**/*.json',
    'locales/**/*.json',
    'public/locales/**/*.json',
    'i18n/**/*.json',
    'assets/i18n/**/*.json',
    'config/locales/**/*.yml',   # Rails
    'config/locales/**/*.yaml',
    'lib/l10n/**/*.arb',         # Flutter
    'po/**/*.po',                # gettext
    '*.po',
]

found_files = []
for pattern in patterns:
    found_files.extend(glob.glob(pattern, recursive=True))

# Exclude node_modules
found_files = [f for f in found_files if 'node_modules' not in f and 'dist' not in f]

if found_files:
    # Group by format
    by_ext = {}
    for f in found_files:
        ext = os.path.splitext(f)[1]
        by_ext.setdefault(ext, []).append(f)
    for ext, files in by_ext.items():
        print(f'{ext}: {len(files)} files')
        for f in sorted(files):
            print(f'  {f}')
else:
    print('No locale files found in standard locations.')
    print('Common locations to check:')
    print('  src/locales/, src/i18n/, locales/, config/locales/, lib/l10n/')
"
```

---

## Step 2: Detect i18n Framework

```bash
python3 -c "
import json, os

try:
    pkg = json.load(open('package.json'))
    deps = {**pkg.get('dependencies', {}), **pkg.get('devDependencies', {})}
    frameworks = []
    if 'i18next' in deps or 'react-i18next' in deps:
        frameworks.append('i18next / react-i18next')
    if 'vue-i18n' in deps:
        frameworks.append('vue-i18n')
    if '@angular/localize' in deps:
        frameworks.append('@angular/localize')
    if 'react-intl' in deps:
        frameworks.append('react-intl (FormatJS)')
    if 'next-intl' in deps or 'next-i18next' in deps:
        frameworks.append('next-i18next / next-intl')
    if frameworks:
        print('Detected:', ', '.join(frameworks))
    else:
        print('No i18n framework detected in package.json')
except FileNotFoundError:
    pass

# Check for Rails
if os.path.exists('Gemfile'):
    with open('Gemfile') as f:
        content = f.read()
    if 'rails-i18n' in content or \"gem 'i18n'\" in content:
        print('Detected: Rails i18n')

# Check for Flutter
if os.path.exists('pubspec.yaml'):
    print('Detected: Flutter (check lib/l10n/ for .arb files)')
"
```

---

## Step 3: Load and Flatten All Locale Files

```python
import json, yaml, os, re
from pathlib import Path
from collections import defaultdict

def flatten_dict(d, prefix='', sep='.'):
    """Flatten nested dict to dot-notation keys."""
    items = []
    for k, v in d.items():
        key = f"{prefix}{sep}{k}" if prefix else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, key, sep).items())
        else:
            items.append((key, v))
    return dict(items)

def load_locale_file(fpath):
    """Load JSON, YAML, or ARB locale file into flat dict."""
    ext = Path(fpath).suffix.lower()
    content = Path(fpath).read_text(encoding='utf-8')

    if ext in ['.json', '.arb']:
        data = json.loads(content)
        # ARB: skip keys starting with @ (metadata)
        data = {k: v for k, v in data.items() if not k.startswith('@') and k != '@@locale'}
    elif ext in ['.yml', '.yaml']:
        data = yaml.safe_load(content)
        # Rails: top level is the locale name → unwrap it
        if len(data) == 1 and isinstance(list(data.values())[0], dict):
            data = list(data.values())[0]
    else:
        return {}

    return flatten_dict(data) if isinstance(data, dict) else {}

def load_po_file(fpath):
    """Simple PO file parser."""
    content = Path(fpath).read_text(encoding='utf-8')
    translations = {}
    current_msgid = None
    for line in content.splitlines():
        if line.startswith('msgid '):
            current_msgid = line[7:].strip().strip('"')
        elif line.startswith('msgstr ') and current_msgid:
            msgstr = line[8:].strip().strip('"')
            if current_msgid:  # skip empty msgid (file header)
                translations[current_msgid] = msgstr
            current_msgid = None
    return translations
```

---

## Step 4: Diff Locales

```python
def audit_locales(locale_dir, base_locale='en'):
    """Compare all locales against the base locale."""
    locale_files = {}

    # Load all locale files
    for fpath in Path(locale_dir).rglob('*'):
        if fpath.suffix in ['.json', '.yml', '.yaml', '.arb']:
            # Infer locale code from filename
            stem = fpath.stem  # e.g., "en", "zh-CN", "fr"
            locale_files[stem] = load_locale_file(str(fpath))
        elif fpath.suffix == '.po':
            stem = fpath.stem
            locale_files[stem] = load_po_file(str(fpath))

    if base_locale not in locale_files:
        print(f"Base locale '{base_locale}' not found. Available: {list(locale_files.keys())}")
        return

    base = locale_files[base_locale]
    base_keys = set(base.keys())

    results = {}
    for locale, translations in locale_files.items():
        if locale == base_locale:
            continue

        locale_keys = set(translations.keys())
        missing = base_keys - locale_keys
        orphaned = locale_keys - base_keys

        # Untranslated: key exists but value is identical to base (or empty)
        untranslated = set()
        empty = set()
        for key in (base_keys & locale_keys):
            val = translations[key]
            base_val = base[key]
            if not val or val.strip() == '':
                empty.add(key)
            elif val == base_val and base_locale.startswith('en'):
                untranslated.add(key)

        translated_count = len(base_keys & locale_keys) - len(untranslated) - len(empty)
        coverage = round(100 * translated_count / len(base_keys), 1) if base_keys else 100

        results[locale] = {
            'coverage': coverage,
            'total': len(base_keys),
            'translated': translated_count,
            'missing': sorted(missing),
            'untranslated': sorted(untranslated),
            'empty': sorted(empty),
            'orphaned': sorted(orphaned),
        }

    return results
```

---

## Step 5: Output Report

```markdown
## i18n Coverage Audit
Project: my-app | Framework: i18next | Base locale: en (247 keys)
Locales found: en, zh-CN, fr, de, ja, es, pt-BR

---

### Coverage Summary

| Locale | Coverage | Missing | Untranslated | Empty | Orphaned |
|--------|----------|---------|--------------|-------|---------|
| 🇩🇪 de | 97.2% ✅ | 7 | 0 | 0 | 2 |
| 🇫🇷 fr | 94.3% 🟡 | 14 | 0 | 0 | 0 |
| 🇨🇳 zh-CN | 89.1% 🟠 | 27 | 0 | 0 | 5 |
| 🇯🇵 ja | 78.5% 🔴 | 53 | 4 | 2 | 0 |
| 🇪🇸 es | 75.3% 🔴 | 61 | 8 | 0 | 3 |
| 🇧🇷 pt-BR | 61.1% 🔴 | 96 | 12 | 3 | 7 |

**Worst locale: pt-BR (61.1%) — 96 missing keys**
**Best locale: de (97.2%) — only 7 missing**

---

### 🔴 High-Impact Missing Keys (used in most templates)

These missing keys affect the most user-visible UI:

**zh-CN is missing these 27 keys:**

```
Common keys missing in zh-CN:
  auth.login_button                    ← used in LoginPage, Header, Modal
  auth.logout_confirm                  ← used in UserMenu
  dashboard.export.csv_label           ← NEW in last sprint
  dashboard.export.pdf_label           ← NEW in last sprint
  settings.notifications.email_title   ← used in 3 components
  settings.notifications.push_title    ← used in 3 components
  onboarding.step1.title               ← NEW - onboarding redesign
  onboarding.step1.description
  onboarding.step2.title
  onboarding.step2.description
  onboarding.step3.title
  onboarding.step3.description
  ... (15 more keys)
```

**Pattern detected:** 8 of the 27 missing zh-CN keys are from the `onboarding.*` namespace — these are all new keys added in the last sprint that weren't added to zh-CN.json.

---

### 🟡 Untranslated Values (value = English source)

These keys exist in the locale file but the value was never translated (still the English text):

**ja — 4 untranslated keys:**
```
Key                              en (source)          ja (current)
---                              ---                  ---
errors.network_timeout           "Connection timeout"  "Connection timeout"  ← same!
errors.server_unavailable        "Service unavailable" "Service unavailable" ← same!
pricing.per_month_label          "/ month"             "/ month"             ← same!
pricing.per_year_label           "/ year"              "/ year"              ← same!
```

These were likely added as placeholders and never handed off to translators.

---

### 🟡 Orphaned Keys (in secondary locale, not in base)

These keys exist in a locale file but not in the base English file — they may be from a deleted feature:

```
zh-CN has 5 orphaned keys (base 'en' doesn't have these):
  features.old_dashboard.title      ← probably from deleted old dashboard
  features.old_dashboard.subtitle
  features.beta_chart.label         ← beta feature removed?
  auth.legacy_sso_note              ← legacy SSO removed?
  marketing.promo_april_2025        ← expired promotion
```

Safe to delete from zh-CN.json after confirming the feature was removed.

---

### Auto-Generated Scaffold for Missing Keys

Run `/i18n-audit --scaffold zh-CN` to generate a file you can hand to a translator:

```json
{
  "_meta": {
    "base_locale": "en",
    "target_locale": "zh-CN",
    "missing_count": 27,
    "generated_at": "2026-03-18T10:42:00Z"
  },
  "auth": {
    "login_button": "",
    "logout_confirm": ""
  },
  "dashboard": {
    "export": {
      "csv_label": "",
      "pdf_label": ""
    }
  },
  "onboarding": {
    "step1": {
      "title": "",
      "description": ""
    }
  }
}
```

Fill in the empty strings, then merge this file with the existing `zh-CN.json`.

---

### CI Fail-Gate Command

Add this to your CI pipeline to prevent missing translations from shipping:

```bash
# Fail if any locale is below 95% coverage
# (adjust threshold as appropriate for your project)
npx --yes i18n-coverage-check --min 95 --base en --locales locales/
# OR, without npm:
python3 -c "
import json, sys
from pathlib import Path

base = json.loads(Path('locales/en.json').read_text())
base_keys = set(base.keys())
threshold = 95
failed = False

for locale_file in Path('locales').glob('*.json'):
    if locale_file.stem == 'en': continue
    trans = json.loads(locale_file.read_text())
    coverage = 100 * len(set(trans.keys()) & base_keys) / len(base_keys)
    if coverage < threshold:
        print(f'FAIL: {locale_file.stem} coverage {coverage:.1f}% < {threshold}%')
        failed = True
    else:
        print(f'PASS: {locale_file.stem} {coverage:.1f}%')

sys.exit(1 if failed else 0)
"
```

---

### Sprint Workflow Integration

Add to your PR template:

```markdown
## i18n Checklist
- [ ] New strings added to `en.json` (base locale)
- [ ] Ran `/i18n-audit` — no new regressions in top locales
- [ ] Translator tickets created for: [ ] zh-CN [ ] fr [ ] de [ ] ja
- [ ] `onboarding.*` namespace: zh-CN and ja coverage still > 90%
```

---

### Namespace/File Pattern Support

**i18next namespace files** (separate JSON per namespace):
```
locales/
  en/
    common.json
    auth.json
    dashboard.json
  zh-CN/
    common.json      ← has 3 missing keys vs en/common.json
    auth.json        ← has 0 missing keys
    dashboard.json   ← MISSING entirely (0 keys)
```

When namespace files are detected, the audit runs per-namespace and flags missing files entirely.

**Rails YAML** (nested locale key at top level):
```yaml
# fr.yml
fr:
  activerecord:
    errors:
      messages:
        blank: "ne peut pas être vide"   ← present
        # taken: ...                     ← MISSING vs en.yml
```

**Flutter ARB** (metadata keys skipped):
```json
{
  "@@locale": "zh",
  "@title": {"description": "App title"},
  "title": "",   ← EMPTY
  "loginButton": "登录",
  "logoutButton": ""   ← EMPTY
}
```
```

---

## Quick Mode

Fast one-line summary without full key listing:

```
i18n Audit: my-app (i18next, base: en, 247 keys)

🔴 pt-BR: 61.1% — 96 missing
🔴 es:    75.3% — 61 missing
🔴 ja:    78.5% — 53 missing (+ 4 untranslated)
🟠 zh-CN: 89.1% — 27 missing (+ 5 orphaned)
🟡 fr:    94.3% — 14 missing
✅ de:    97.2% — 7 missing

8 keys missing in zh-CN are from 'onboarding.*' namespace (last sprint)
Run /i18n-audit --locale zh-CN for full key list + scaffolded output file
```

---

## Author

**[Canlah AI](https://canlah.ai)** — Run performance marketing without breaking your brand.

- GitHub: [github.com/PHY041](https://github.com/PHY041)
- All Skills: [clawhub.ai/PHY041](https://clawhub.ai/PHY041)
