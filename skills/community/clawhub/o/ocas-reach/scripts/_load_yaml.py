"""Minimal YAML loader — thin wrapper around PyYAML (always available)."""
import yaml
import sys

_HELP_ARGS = {"--help", "-h"}
if set(sys.argv[1:]) & _HELP_ARGS:
    print((__doc__ or "").strip() or "Usage: python3 _load_yaml.py")
    sys.exit(0)

# Optimization: Use C-based CSafeLoader if available in PyYAML for ~8x faster parsing
# on large files like sources.yml (~186ms down to ~23ms).
try:
    from yaml import CSafeLoader as _SafeLoader
except ImportError:
    from yaml import SafeLoader as _SafeLoader


def _load_yaml_min(text):
    """Parse YAML text. PyYAML is a project dependency."""
    return yaml.load(text, Loader=_SafeLoader)
