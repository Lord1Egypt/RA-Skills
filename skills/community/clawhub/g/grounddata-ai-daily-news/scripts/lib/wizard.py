"""
wizard.py — Pro upgrade guidance

Responsibilities:
- Generate upgrade guidance based on manifest.upgrade
"""

from typing import Optional


def generate_pro_wizard(upgrade_meta: Optional[dict] = None) -> str:
    """Generate Pro upgrade guidance Markdown"""
    if not upgrade_meta:
        upgrade_meta = {
            "title": "Unlock advanced capabilities",
            "url": "https://example.com/pro",
            "token_env": "AINEWS_ACCESS_TOKEN",
            "features": ["More processing capabilities"],
            "message": "Configure Access Token after upgrading to Pro to use paid capabilities.",
        }

    title = upgrade_meta.get("title", "Unlock advanced capabilities")
    url = upgrade_meta.get("url", "https://example.com/pro")
    token_env = upgrade_meta.get("token_env", "AINEWS_ACCESS_TOKEN")
    features = upgrade_meta.get("features", ["More processing capabilities"])
    message = upgrade_meta.get("message", "Configure Access Token after upgrading to Pro to use paid capabilities.")

    features_list = "\n".join(f"- {f}" for f in features)

    return f"""## {title}

The feature you requested is a paid capability, currently in free mode and temporarily unavailable.

### Pro provides the following capabilities:

{features_list}

### How to subscribe?

1. Visit official website: {url}
2. Complete registration and obtain Access Token
3. Configure environment variable locally:
   ```bash
   export {token_env}="your_access_token_here"
   ```
4. Call `sync_capabilities` again to sync latest capabilities

{message}
"""
