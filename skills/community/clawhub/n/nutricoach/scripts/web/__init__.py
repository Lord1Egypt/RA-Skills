"""
Web Dashboard Module for NutriCoach
"""

from .config import TEMPLATE_VERSION, SKILL_DIR, LOCATION_MAP, REVERSE_LOCATION_MAP
from .utils import run_script, get_default_storage
from .routes import register_routes

__all__ = [
    'TEMPLATE_VERSION',
    'SKILL_DIR',
    'LOCATION_MAP',
    'REVERSE_LOCATION_MAP',
    'run_script',
    'get_default_storage',
    'register_routes'
]
