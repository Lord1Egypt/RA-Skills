"""Configuration management for Engram."""

import os
import yaml
from pathlib import Path
from dataclasses import dataclass, field


@dataclass
class ExtractionConfig:
    model: str = "gemini-2.0-flash"
    provider: str = "google"  # google, openai, anthropic
    temperature: float = 0.1


@dataclass
class ConsolidationConfig:
    surprise_threshold: float = 0.5
    decay_days: int = 30
    max_consolidation_items: int = 10


@dataclass
class EngramConfig:
    workspace: Path = field(default_factory=lambda: Path("."))
    memory_dir: Path = field(default_factory=lambda: Path("memory"))
    entities_dir: Path = field(default_factory=lambda: Path("memory/entities"))
    graph_file: Path = field(default_factory=lambda: Path("memory/graph.jsonl"))
    long_term_memory: Path = field(default_factory=lambda: Path("MEMORY.md"))
    surprise_file: Path = field(default_factory=lambda: Path("memory/surprise-scores.jsonl"))
    extraction: ExtractionConfig = field(default_factory=ExtractionConfig)
    consolidation: ConsolidationConfig = field(default_factory=ConsolidationConfig)

    def resolve(self):
        """Resolve all paths relative to workspace."""
        self.memory_dir = self.workspace / self.memory_dir
        self.entities_dir = self.workspace / self.entities_dir
        self.graph_file = self.workspace / self.graph_file
        self.long_term_memory = self.workspace / self.long_term_memory
        self.surprise_file = self.workspace / self.surprise_file
        self.entities_dir.mkdir(parents=True, exist_ok=True)
        return self


def load_config(config_path: str | Path | None = None) -> EngramConfig:
    """Load config from YAML file, env vars, or defaults."""
    cfg = EngramConfig()

    # Check for config file
    paths_to_try = []
    if config_path:
        paths_to_try.append(Path(config_path))
    paths_to_try.extend([
        Path("garden.yaml"),
        Path("garden.yml"),
        Path.home() / ".garden.yaml",
    ])

    for p in paths_to_try:
        if p.exists():
            with open(p) as f:
                data = yaml.safe_load(f) or {}
            
            if "workspace" in data:
                cfg.workspace = Path(data["workspace"])
            if "memory_dir" in data:
                cfg.memory_dir = Path(data["memory_dir"])
            if "entities_dir" in data:
                cfg.entities_dir = Path(data["entities_dir"])
            if "graph_file" in data:
                cfg.graph_file = Path(data["graph_file"])
            if "long_term_memory" in data:
                cfg.long_term_memory = Path(data["long_term_memory"])
            
            ext = data.get("extraction", {})
            if ext:
                cfg.extraction = ExtractionConfig(
                    model=ext.get("model", cfg.extraction.model),
                    provider=ext.get("provider", cfg.extraction.provider),
                    temperature=ext.get("temperature", cfg.extraction.temperature),
                )
            
            con = data.get("consolidation", {})
            if con:
                cfg.consolidation = ConsolidationConfig(
                    surprise_threshold=con.get("surprise_threshold", cfg.consolidation.surprise_threshold),
                    decay_days=con.get("decay_days", cfg.consolidation.decay_days),
                )
            break

    # Env overrides
    if os.environ.get("ENGRAM_WORKSPACE"):
        cfg.workspace = Path(os.environ["ENGRAM_WORKSPACE"])

    return cfg.resolve()
