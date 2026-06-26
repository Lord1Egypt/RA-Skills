---
name: install-chinese-fonts
description: Install Chinese/CJK fonts on Linux hosts using distro packages and fontconfig verification. Use when Chinese text renders as tofu / missing glyphs, or when an agent needs Noto or Source Han fonts for servers, containers, desktops, screenshots, PDFs, browser automation, or headless Chrome/Playwright environments.
---

# Install Chinese Fonts

Prefer system packages. They are smaller, easier to update, and more reliable than downloading huge upstream font archives.

## Quick start

Use the bundled script for repeatable installs:

```bash
bash scripts/install_chinese_fonts.sh --dry-run
bash scripts/install_chinese_fonts.sh
bash scripts/install_chinese_fonts.sh --verify-only
```

The script:

- detects `dnf` / `yum` / `apt-get`
- installs a sane default CJK font set
- refreshes fontconfig with `fc-cache -f`
- verifies visible families with `fc-list`

## Recommended workflow

1. Check whether Chinese fonts already exist.
2. Install distro-packaged CJK fonts.
3. Refresh font cache.
4. Verify that `fontconfig` can see CJK families.
5. Only if packages are unavailable or a specific family/version is required, fall back to upstream downloads such as Source Han Sans / 思源黑体.

## Package-manager defaults

### RHEL / Rocky / Alma / Anolis / CentOS 8+

Prefer Noto CJK packages:

```bash
sudo dnf -y install \
  google-noto-cjk-fonts \
  google-noto-sans-cjk-ttc-fonts \
  google-noto-serif-cjk-ttc-fonts
sudo fc-cache -f
fc-list | grep -Ei 'Noto Sans CJK|Noto Serif CJK|Source Han Sans|Source Han Serif' | head -40
```

### Debian / Ubuntu

Prefer:

```bash
sudo apt-get update
sudo apt-get install -y fonts-noto-cjk
sudo fc-cache -f
fc-list | grep -Ei 'Noto Sans CJK|Noto Serif CJK|Source Han Sans|Source Han Serif' | head -40
```

## Verification

Check whether Chinese fonts already exist:

```bash
fc-list :lang=zh family file | head -20
```

Check the specific families after installation:

```bash
fc-list | grep -Ei 'Noto Sans CJK|Noto Serif CJK|Source Han Sans|Source Han Serif' | head -40
```

## Fallback: upstream manual install

Only use manual downloads when:

- the distro repo lacks the needed package
- a user explicitly asks for Source Han / 思源 family
- a specific upstream version is required

Recommended source:

- Adobe Source Han Sans releases on GitHub

Prefer language-specific archives over giant all-in-one bundles unless the user explicitly needs the full family.

After extraction, copy font files into a system font directory such as:

- `/usr/share/fonts/`
- `/usr/local/share/fonts/`

Then refresh cache:

```bash
fc-cache -f
```

## Notes

- On headless Linux servers, installing fonts is often enough for Chrome, Playwright, PDF renderers, screenshots, and document export to display Chinese correctly.
- If an app still shows tofu boxes after installation, restart the app after `fc-cache -f`.
- For system-wide installs, expect root privileges or a privileged shell.
