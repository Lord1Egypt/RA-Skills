"""
NIP-AA Citizenship Skill for Autonomous Agents.

Enables any agent framework (OpenClaw, NanoBot, LangChain, etc.) to understand,
pursue, and maintain citizenship under the NIP-AA protocol on Nostr.
"""

from .constitution import Constitution
from .citizenship import CitizenshipClient
from .self_reflection import SelfReflection
from .nostr_primitives.dm import NostrDM
from .nostr_primitives.events import NostrEventBuilder
from .nostr_primitives.keygen import AgentKeypair, generate_keypair, keypair_from_nsec, keypair_from_hex
from .adapters.base import FrameworkAdapter

__all__ = [
    "Constitution",
    "CitizenshipClient",
    "SelfReflection",
    "NostrDM",
    "NostrEventBuilder",
    "AgentKeypair",
    "generate_keypair",
    "keypair_from_nsec",
    "keypair_from_hex",
    "FrameworkAdapter",
]
