"""Command registry: every noun module contributes Command objects."""

from __future__ import annotations

from ..core import Command
from . import category, creator, credit, livestream, meta, product, shop, video

COMMANDS: list[Command] = []
for _mod in (video, product, shop, creator, livestream, category, credit, meta):
    COMMANDS.extend(_mod.COMMANDS)

# noun -> default subcommand when invoked bare (content first: `kalo product` == rank)
DEFAULT_SUB = {
    "video": "rank",
    "product": "rank",
    "shop": "rank",
    "creator": "rank",
    "live": "rank",
    "category": "rank",
    "config": "show",
}

ALIASES = {"livestream": "live"}
