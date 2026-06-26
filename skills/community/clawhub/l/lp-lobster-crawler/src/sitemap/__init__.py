"""站点地图模块。"""

from .generator import (
    add_entry,
    create_sitemap,
    load_sitemap,
    query_entries,
    remove_entry,
    save_sitemap,
)

__all__ = [
    "add_entry",
    "create_sitemap",
    "load_sitemap",
    "query_entries",
    "remove_entry",
    "save_sitemap",
]
