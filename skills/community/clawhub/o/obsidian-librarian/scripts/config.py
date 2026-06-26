#!/usr/bin/env python3
from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path


DEFAULT_CATEGORIES = {
    "AI_Models_and_Research": (
        "Papers, blog posts, and discussions about model architectures "
        "(transformers, diffusion, SSMs, etc.), training techniques, "
        "benchmarks, datasets, and foundational ML research."
    ),
    "AI_Engineering": (
        "Developer tools, frameworks, SDKs, APIs, prompt engineering, "
        "fine-tuning guides, RAG patterns, deployment, and infrastructure "
        "for building with AI."
    ),
    "AI_Agents_and_Applications": (
        "Agentic systems, autonomous workflows, real-world AI use cases, "
        "product launches, demos, and applied AI across industries."
    ),
    "AI_Industry": (
        "Company news, funding rounds, acquisitions, partnerships, hiring, "
        "AI policy, regulation, safety debates, and market dynamics."
    ),
    "Prediction_Markets": (
        "Market mechanics, platform analysis (Kalshi, Polymarket, Metaculus), "
        "trading strategies, event contracts, calibration, forecasting methods, "
        "and prediction market research."
    ),
    "Technical_Reference": (
        "General programming, databases, infrastructure, DevOps, and tutorials "
        "not specific to AI or prediction markets."
    ),
    "Uncategorized": (
        "Content that does not clearly fit any other category."
    ),
}


@dataclass
class LibrarianSettings:
    obsidian_vault_path: str
    inbox_folder: str = "_Inbox"
    gemini_api_key: str = ""
    gemini_model: str = "gemini-2.5-flash"
    categories: dict[str, str] = field(default_factory=lambda: dict(DEFAULT_CATEGORIES))
    supabase_url: str = ""
    supabase_key: str = ""
    embedding_model: str = "gemini-embedding-001"
    embedding_dimensions: int = 384
    rag_index_path_override: str = ""

    @classmethod
    def from_env(cls) -> "LibrarianSettings":
        def env(name: str, default: str) -> str:
            return os.environ.get(name) or default

        return cls(
            obsidian_vault_path=env("OBSIDIAN_VAULT_PATH", "~/Desktop/Vault"),
            inbox_folder=env("OBSIDIAN_INBOX_FOLDER", "_Inbox"),
            gemini_api_key=env("GEMINI_API_KEY", ""),
            gemini_model=env("OBSIDIAN_GEMINI_MODEL", env("GEMINI_MODEL", "gemini-2.5-flash")),
            categories=dict(DEFAULT_CATEGORIES),
            supabase_url=env("SUPABASE_URL", ""),
            supabase_key=env("SUPABASE_KEY", ""),
            embedding_model=env("EMBEDDING_MODEL", "gemini-embedding-001"),
            embedding_dimensions=int(env("EMBEDDING_DIMENSIONS", "384")),
            rag_index_path_override=env("OBSIDIAN_RAG_INDEX_PATH", ""),
        )

    @property
    def vault_path(self) -> Path:
        return Path(self.obsidian_vault_path).expanduser().resolve()

    @property
    def inbox_path(self) -> Path:
        return self.vault_path / self.inbox_folder

    @property
    def rag_index_path(self) -> Path:
        if self.rag_index_path_override:
            return Path(self.rag_index_path_override).expanduser().resolve()
        return self.vault_path / ".obsidian-librarian" / "vault_chunks.json"

    @property
    def use_supabase_rag(self) -> bool:
        return bool(self.supabase_url and self.supabase_key)
