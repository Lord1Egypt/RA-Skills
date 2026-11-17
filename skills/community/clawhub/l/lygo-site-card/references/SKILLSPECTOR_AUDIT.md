# SkillSpector notes — lygo-site-card v1.0.0

Expected **network** hits: `urllib.request` in `scripts/site_card.py` for HTTPS GET.

Expected **no** hits: subprocess, os.system, eval/exec, pickle, git push, HF upload.

`self_check.py` is offline (local HTML fixture).

If a scanner flags urllib as HIGH, that is a **claim match**: frontmatter `https_get: user-supplied URL` is intentional.
