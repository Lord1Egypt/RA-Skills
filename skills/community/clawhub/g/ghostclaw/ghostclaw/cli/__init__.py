try:
    from importlib.metadata import version as get_version
except ImportError:
    # For Python < 3.8
    try:
        from importlib_metadata import version as get_version
    except ImportError:
        def get_version(_):
            return "0.1.4"

try:
    __version__ = get_version("ghostclaw")
except Exception:
    __version__ = "0.1.4"
