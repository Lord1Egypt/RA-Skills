#!/usr/bin/env python3
"""
DGRA Configuration Manager
Phase 1 - v0.4 Architecture

Handles API keys, timeouts, retry policies, and offline mode.
"""

import os
import json
from dataclasses import dataclass, field
from typing import Dict, Optional, List, Any
from pathlib import Path
import yaml  # v0.5 P2-3: YAML config support

# v0.5 P2-3: Config file path
DEFAULT_CONFIG_PATH = Path(__file__).parent.parent / "references" / "dgra.yaml"


@dataclass
class APIConfig:
    """API endpoint configuration with rate limiting and retry policy."""
    base_url: str
    timeout: float = 30.0  # seconds
    max_retries: int = 3
    retry_delay: float = 1.0  # initial backoff (exponential)
    rate_limit_per_sec: float = 10.0  # requests per second
    api_key: Optional[str] = None
    proxy: Optional[str] = None  # HTTP/HTTPS proxy URL


@dataclass
class DGRAGlobalConfig:
    """Global DGRA configuration including all API endpoints and runtime flags."""
    
    # Offline mode: skip all API calls, use cache + local overrides only
    offline_mode: bool = False
    
    # v0.5 P1-8: Gene list sync settings
    gene_sync_enabled: bool = True
    gene_sync_ttl_days: int = 7
    
    # v0.4.5: Somatic mode for tumor driver analysis (not germline donor screening)
    somatic_mode: bool = False
    
    # Cache settings
    cache_db_path: Path = field(default_factory=lambda: Path(__file__).parent.parent / "cache" / "dgra_cache.db")
    cache_ttl_days: int = 30  # Time-to-live for cached API responses
    
    # Analysis thresholds (same as v0.3)
    min_dp: int = 20
    min_gq: float = 90.0
    common_af_threshold: float = 0.01
    low_af_threshold: float = 0.001
    vaf_deviation_threshold: float = 0.20
    
    # Tissue context profile name
    tissue_profile: str = "general"
    
    # v0.5 P1-7: Multi-organ assessment — evaluate multiple profiles simultaneously
    # Each profile runs independently; joint report takes max tier across profiles
    multi_organ_profiles: Optional[List[str]] = None
    
    # Confidence thresholds for manual review flagging
    high_confidence_min_apis: int = 3  # Need at least N APIs responding for HIGH
    
    # API endpoint configurations (no keys needed for public endpoints)
    apis: Dict[str, APIConfig] = field(default_factory=lambda: {
        "ensembl": APIConfig(
            base_url="https://rest.ensembl.org",
            timeout=20.0,
            max_retries=2,
            retry_delay=1.0,
            rate_limit_per_sec=10.0,
        ),
        "uniprot": APIConfig(
            base_url="https://rest.uniprot.org",
            timeout=25.0,
            max_retries=2,
            retry_delay=2.0,
            rate_limit_per_sec=5.0,
        ),
        "gtex": APIConfig(
            base_url="https://gtexportal.org/api/v2",
            timeout=20.0,
            max_retries=2,
            retry_delay=2.0,
            rate_limit_per_sec=3.0,
        ),
        "gnomad": APIConfig(
            base_url="https://gnomad.broadinstitute.org/api",
            timeout=15.0,
            max_retries=2,
            retry_delay=2.0,
            rate_limit_per_sec=2.0,
        ),
        "ncbi_eutils": APIConfig(
            base_url="https://eutils.ncbi.nlm.nih.gov/entrez/eutils",
            timeout=15.0,
            max_retries=2,
            retry_delay=1.0,
            rate_limit_per_sec=3.0,  # NCBI: 3/sec without API key
        ),
        "clinvar_eutils": APIConfig(
            base_url="https://eutils.ncbi.nlm.nih.gov/entrez/eutils",
            timeout=15.0,
            max_retries=2,
            retry_delay=1.0,
            rate_limit_per_sec=3.0,
        ),
        "hgnc": APIConfig(
            base_url="https://rest.genenames.org",
            timeout=15.0,
            max_retries=2,
            retry_delay=1.0,
            rate_limit_per_sec=5.0,
        ),
    })
    
    # Override files (local patches for API blind spots)
    override_files: Dict[str, Path] = field(default_factory=lambda: {
        "pseudogene": Path(__file__).parent.parent / "references" / "pseudogene_config.json",
        "api_corrections": Path(__file__).parent.parent / "references" / "api_corrections.json",
        "tissue_profiles": Path(__file__).parent.parent / "references" / "tissue_context.json",
    })
    
    @classmethod
    def from_env(cls) -> "DGRAGlobalConfig":
        """Load configuration from environment variables."""
        config = cls()
        
        # Offline mode
        if os.environ.get("DGRA_OFFLINE", "").lower() in ("1", "true", "yes"):
            config.offline_mode = True
        
        # Override cache path
        if cache_path := os.environ.get("DGRA_CACHE_PATH"):
            config.cache_db_path = Path(cache_path)
        
        # Override tissue profile
        if tissue := os.environ.get("DGRA_TISSUE"):
            config.tissue_profile = tissue
        
        # HTTP/HTTPS proxy support
        for api_name in config.apis:
            proxy = os.environ.get("HTTP_PROXY") or os.environ.get("http_proxy") or os.environ.get("HTTPS_PROXY") or os.environ.get("https_proxy")
            if proxy:
                config.apis[api_name].proxy = proxy
        
        # NCBI API key (increases rate limit from 3/sec to 10/sec)
        if ncbi_key := os.environ.get("NCBI_API_KEY"):
            config.apis["ncbi_eutils"].api_key = ncbi_key
            config.apis["clinvar_eutils"].api_key = ncbi_key
            config.apis["ncbi_eutils"].rate_limit_per_sec = 10.0
            config.apis["clinvar_eutils"].rate_limit_per_sec = 10.0
        
        # Custom API timeouts
        for api_name in config.apis:
            env_key = f"DGRA_{api_name.upper()}_TIMEOUT"
            if timeout := os.environ.get(env_key):
                config.apis[api_name].timeout = float(timeout)
        
        return config
    
    def get_override(self, name: str) -> Optional[dict]:
        """Load a local override JSON file if it exists."""
        path = self.override_files.get(name)
        if path and path.exists():
            with open(path, 'r') as f:
                return json.load(f)
        return None


# =============================================================================
# YAML Config Loader (v0.5 P2-3)
# =============================================================================

def _resolve_path(base_dir: Path, path_str: str) -> Path:
    """Resolve a path string relative to base_dir if not absolute."""
    p = Path(path_str)
    if p.is_absolute():
        return p
    return base_dir / p


@dataclass
class DGRAFileConfig:
    """v0.5 P2-3: Configuration loaded from YAML file at runtime.
    
    Bridges YAML file → DGRAGlobalConfig / DGRAConfig.
    """
    api_endpoints: Optional[Dict[str, Dict[str, Any]]] = None
    thresholds: Optional[Dict[str, Any]] = None
    tier_rules: Optional[Dict[str, List[str]]] = None
    tissue_profiles: Optional[Dict[str, Any]] = None
    cache: Optional[Dict[str, Any]] = None
    offline: Optional[Dict[str, Any]] = None
    gene_sync: Optional[Dict[str, Any]] = None
    evidence: Optional[Dict[str, Any]] = None
    proxy: Optional[Dict[str, str]] = None
    
    @classmethod
    def from_yaml(cls, yaml_path: Path) -> "DGRAFileConfig":
        """Load configuration from a YAML file."""
        if not yaml_path.exists():
            raise FileNotFoundError(f"DGRA config file not found: {yaml_path}")
        with open(yaml_path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f) or {}
        return cls(
            api_endpoints=data.get("api_endpoints"),
            thresholds=data.get("thresholds"),
            tier_rules=data.get("tier_rules"),
            tissue_profiles=data.get("tissue_profiles"),
            cache=data.get("cache"),
            offline=data.get("offline"),
            gene_sync=data.get("gene_sync"),
            evidence=data.get("evidence"),
            proxy=data.get("proxy"),
        )
    
    def apply_to_global(self, global_config: DGRAGlobalConfig, base_dir: Path) -> None:
        """Apply file config overrides to an existing DGRAGlobalConfig."""
        # API endpoints override
        if self.api_endpoints:
            for api_name, ep in self.api_endpoints.items():
                if api_name in global_config.apis:
                    cfg = global_config.apis[api_name]
                    if "base_url" in ep:
                        cfg.base_url = ep["base_url"]
                    if "timeout" in ep:
                        cfg.timeout = float(ep["timeout"])
                    if "max_retries" in ep:
                        cfg.max_retries = int(ep["max_retries"])
                    if "retry_delay" in ep:
                        cfg.retry_delay = float(ep["retry_delay"])
                    if "rate_limit_per_sec" in ep:
                        cfg.rate_limit_per_sec = float(ep["rate_limit_per_sec"])
                    if "api_key" in ep:
                        cfg.api_key = ep["api_key"]
        
        # Thresholds override
        if self.thresholds:
            t = self.thresholds
            if "min_dp" in t:
                global_config.min_dp = int(t["min_dp"])
            if "min_gq" in t:
                global_config.min_gq = float(t["min_gq"])
            if "common_af_threshold" in t:
                global_config.common_af_threshold = float(t["common_af_threshold"])
            if "low_af_threshold" in t:
                global_config.low_af_threshold = float(t["low_af_threshold"])
            if "vaf_deviation_threshold" in t:
                global_config.vaf_deviation_threshold = float(t["vaf_deviation_threshold"])
        
        # Cache override
        if self.cache:
            c = self.cache
            if "db_path" in c:
                global_config.cache_db_path = _resolve_path(base_dir, c["db_path"])
            if "ttl_days" in c:
                global_config.cache_ttl_days = int(c["ttl_days"])
            if "gene_sync_ttl_days" in c:
                global_config.gene_sync_ttl_days = int(c["gene_sync_ttl_days"])
        
        # Offline override
        if self.offline:
            o = self.offline
            if "enabled" in o:
                global_config.offline_mode = bool(o["enabled"])
        
        # Gene sync override
        if self.gene_sync:
            gs = self.gene_sync
            if "enabled" in gs:
                global_config.gene_sync_enabled = bool(gs["enabled"])
        
        # Evidence / confidence override
        if self.evidence:
            e = self.evidence
            if "high_confidence_min_apis" in e:
                global_config.high_confidence_min_apis = int(e["high_confidence_min_apis"])
        
        # Proxy override
        if self.proxy:
            for api_name in global_config.apis:
                http_p = self.proxy.get("http") or self.proxy.get("https")
                if http_p:
                    global_config.apis[api_name].proxy = http_p
    
    def apply_to_user_config(self, user_config: "DGRAConfig") -> None:
        """Apply file config overrides to a user-facing DGRAConfig."""
        if self.thresholds:
            t = self.thresholds
            if "min_dp" in t:
                user_config.min_dp = int(t["min_dp"])
            if "min_gq" in t:
                user_config.min_gq = float(t["min_gq"])
            if "common_af_threshold" in t:
                user_config.common_af_threshold = float(t["common_af_threshold"])
            if "low_af_threshold" in t:
                user_config.low_af_threshold = float(t["low_af_threshold"])
            if "vaf_deviation_threshold" in t:
                user_config.vaf_deviation_threshold = float(t["vaf_deviation_threshold"])
        
        if self.evidence:
            e = self.evidence
            if "detail_level" in e:
                user_config.evidence_detail = str(e["detail_level"])
        
        if self.gene_sync:
            gs = self.gene_sync
            if "enabled" in gs:
                user_config.gene_sync_enabled = bool(gs["enabled"])
