"""
Platform connectors — one module per channel.

Each connector exposes a uniform interface:
    PLATFORM          — str identifier ("x", "linkedin")
    ConnectorError    — platform-specific exception (subclass of RuntimeError)
    load_credentials  — load API credentials for an account
    post              — publish a single post
    post_thread       — publish a thread/series
    comment           — reply to an existing post
    follow            — follow an account
    get_stats         — get engagement stats

Usage:
    from act.connectors import load
    connector = load("x")
    result = connector.post(text="hello", account="myaccount")
"""


def load(platform: str):
    """Load a connector module by platform name."""
    if platform == "x":
        from act.connectors import x
        return x
    elif platform == "linkedin":
        from act.connectors import linkedin
        return linkedin
    raise ValueError(f"Unknown platform: {platform}. Available: x, linkedin")
