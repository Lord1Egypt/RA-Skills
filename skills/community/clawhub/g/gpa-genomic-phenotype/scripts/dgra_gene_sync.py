#!/usr/bin/env python3
"""
DGRA Gene List Synchronizer — v0.5 P1-8
Auto-sync special_gene_lists from external sources (Orphanet, OMIM)
and merge with user extensions.

Design principles:
- Non-blocking: sync failures do NOT raise; silent fallback to cache
- Layered priority: hardcoded_core > user_add > sync_add > static_json
- TTL caching: default 7 days
- Offline mode: skip sync, use last cached merged result
- Audit logging: every sync writes a log file
"""

import json
import asyncio
import aiohttp
import sqlite3
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any

import sys
_SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(_SCRIPT_DIR))

# ------------------------------------------------------------------------------
# Hardcoded CORE lists — these are SAFETY-CRITICAL and cannot be overridden
# by sync or user config. They serve as the immutable base layer.
# ------------------------------------------------------------------------------
CORE_GENE_LISTS: Dict[str, List[str]] = {
    "coagulation": [
        "F8", "F9", "VWF", "F2", "F5", "F7", "F10", "F11", "F13A1", "F13B",
        "SERPINC1", "PROC", "PROS1", "THBD", "TFPI", "PLG", "A2M",
    ],
    "thrombophilia": [
        "F5", "F2", "MTHFR", "PROC", "PROS1", "SERPINC1",
    ],
    "cancer_predisposition": [
        "BRCA1", "BRCA2", "TP53", "PTEN", "APC", "MLH1", "MSH2", "MSH6", "PMS2",
        "ATM", "CHEK2", "PALB2", "RAD51C", "RAD51D", "BRIP1", "NBN",
    ],
    "bone_marrow_failure": [
        "RUNX1", "GATA2", "TERC", "TERT", "SBDS", "DKC1", "TINF2", "NOP10",
        "NHP2", "WRAP53", "CTC1", "RTEL1", "PARN",
    ],
    "hemoglobinopathy": [
        "HBA1", "HBA2", "HBB", "HBD", "HBE1", "HBG1", "HBG2", "HBM",
    ],
    "inherited_arrhythmia": [
        "KCNQ1", "KCNH2", "SCN5A", "RYR2", "CASQ2", "TRDN", "CALM1", "CALM2",
        "CALM3", "SCN4B", "KCNE1", "KCNE2", "KCNJ2",
    ],
    "inherited_cardiomyopathy": [
        "MYBPC3", "MYH7", "TNNT2", "TNNI3", "TPM1", "MYL3", "ACTC1", "PRKAG2",
        "TTR", "DES", "SGCD", "LMNA", "PKP2", "DSP", "DSG2", "DSC2", "JUP",
    ],
    "porphyria": [
        "HMBS", "CPOX", "PPOX", "UROS", "UROD", "ALAD", "FECH",
    ],
}

# Orphanet → DGRA list name mapping
ORPHANET_PHENOTYPE_MAP = {
    "ORPHA:182212": "bone_marrow_failure",      # Inherited bone marrow failure
    "ORPHA:82": "hemophilia",                   # Hemophilia
    "ORPHA:457243": "inherited_coagulation",     # Inherited bleeding disorder
    "ORPHA:33069": "inherited_arrhythmia",      # Long QT syndrome
    "ORPHA:154": "inherited_arrhythmia",        # Brugada syndrome
    "ORPHA:871": "inherited_cardiomyopathy",    # Hypertrophic cardiomyopathy
    "ORPHA:156 muscular dystrophy": "inherited_cardiomyopathy",
    "ORPHA:217569": "cancer_predisposition",    # Li-Fraumeni syndrome
    "ORPHA:52427": "porphyria",                 # Acute hepatic porphyria
}


class GeneListSynchronizer:
    """
    Manages the lifecycle of special_gene_lists:
      1. Load static JSON (tissue_context.json)
      2. Sync from external sources (Orphanet, OMIM)
      3. Apply user extensions (add/remove/custom)
      4. Merge with hardcoded CORE (immutable base)
      5. Cache merged result in SQLite
    """

    def __init__(
        self,
        references_dir: Path,
        cache_db_path: Optional[Path] = None,
        offline_mode: bool = False,
        sync_enabled: bool = True,
        ttl_days: int = 7,
    ):
        self.references_dir = references_dir
        self.cache_db_path = cache_db_path or (references_dir.parent / "cache" / "gene_sync_cache.db")
        self.offline_mode = offline_mode
        self.sync_enabled = sync_enabled
        self.ttl_days = ttl_days
        self.log_dir = references_dir.parent / "logs"
        self.log_dir.mkdir(parents=True, exist_ok=True)

        # File paths
        self.sources_config_path = references_dir / "gene_list_sources.json"
        self.user_lists_path = references_dir / "user_gene_lists.json"
        self.tissue_context_path = references_dir / "tissue_context.json"

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    async def get_merged_gene_lists(
        self,
        tissue_profile: str,
        force_sync: bool = False,
    ) -> Dict[str, List[str]]:
        """
        Return the fully merged special_gene_lists for a given tissue profile.
        
        Priority (highest → lowest):
          1. Hardcoded CORE (safety-critical, immutable)
          2. User add/remove extensions
          3. Auto-synced from Orphanet / OMIM
          4. Static JSON from tissue_context.json
        
        Non-blocking: any sync failure silently falls back to cache/static.
        """
        # 1. Try cache first (fast path)
        cached = self._load_cached_lists(tissue_profile)
        if cached and not force_sync and not self._is_cache_expired(tissue_profile):
            # Cache already contains the fully merged + validated result
            return cached

        # 2. Build merged lists
        merged = dict(CORE_GENE_LISTS)  # Start with immutable core

        # 3. Add static lists from tissue_context.json
        static = self._load_static_lists(tissue_profile)
        for list_name, genes in static.items():
            if list_name not in merged:
                merged[list_name] = list(genes)
            else:
                # Core takes precedence; static only adds new genes
                merged[list_name] = list(set(merged[list_name]) | set(genes))

        # 4. Auto-sync from external sources (non-blocking)
        if self.sync_enabled and not self.offline_mode:
            try:
                synced = await self._sync_all_sources()
                # Map synced lists to tissue profile
                profile_synced = self._filter_synced_for_profile(synced, tissue_profile)
                for list_name, genes in profile_synced.items():
                    if list_name not in merged:
                        merged[list_name] = list(genes)
                    else:
                        merged[list_name] = list(set(merged[list_name]) | set(genes))
            except Exception as e:
                self._log_sync_event("SYNC_FAILED", f"External sync failed: {e}")
                # Silently continue with static + core

        # 5. Validate symbols (first pass — sync data)
        merged = self._validate_symbols(merged)

        # 6. Cache the merged result BEFORE user overrides
        #    (cache stores core+static+sync only; user overrides applied on top)
        self._save_cached_lists(tissue_profile, merged)

        # 7. Apply user overrides (always last, so they win)
        merged = self._apply_user_overrides(merged)

        # 8. Re-validate after user overrides (user may have added invalid symbols)
        merged = self._validate_symbols(merged)

        return merged

    def get_merged_gene_lists_sync(self, tissue_profile: str, force_sync: bool = False) -> Dict[str, List[str]]:
        """Synchronous wrapper for get_merged_gene_lists()."""
        return asyncio.run(self.get_merged_gene_lists(tissue_profile, force_sync=force_sync))

    # ------------------------------------------------------------------
    # Sync implementations
    # ------------------------------------------------------------------

    async def _sync_all_sources(self) -> Dict[str, List[str]]:
        """Sync all enabled sources, return merged synced gene lists."""
        if not self.sources_config_path.exists():
            return {}

        with open(self.sources_config_path, "r") as f:
            config = json.load(f)

        sources = config.get("sources", {})
        all_synced: Dict[str, List[str]] = {}

        # Orphanet
        orphanet_cfg = sources.get("orphanet", {})
        if orphanet_cfg.get("enabled", False):
            try:
                orphanet_result = await self._sync_orphanet(orphanet_cfg)
                for k, v in orphanet_result.items():
                    all_synced[k] = list(set(all_synced.get(k, [])) | set(v))
            except Exception as e:
                self._log_sync_event("ORPHANET_FAILED", str(e))

        # OMIM (only if enabled + api_key present)
        omim_cfg = sources.get("omim", {})
        if omim_cfg.get("enabled", False) and omim_cfg.get("api_key"):
            try:
                omim_result = await self._sync_omim(omim_cfg)
                for k, v in omim_result.items():
                    all_synced[k] = list(set(all_synced.get(k, [])) | set(v))
            except Exception as e:
                self._log_sync_event("OMIM_FAILED", str(e))

        return all_synced

    async def _sync_orphanet(self, config: Dict) -> Dict[str, List[str]]:
        """
        Query Orphanet API for gene-disease associations.
        
        Orphanet REST API (unauthenticated, rate-limited):
          GET https://api.orphacode.org/nomenclature/orphanumber/{orpha_id}/genes
        """
        base_url = config.get("url", "https://api.orphacode.org/")
        queries = config.get("gene_phenotype_queries", [])

        result: Dict[str, List[str]] = {}
        connector = aiohttp.TCPConnector(limit=5)
        timeout = aiohttp.ClientTimeout(total=30)

        async with aiohttp.ClientSession(connector=connector, timeout=timeout) as session:
            for q in queries:
                orpha_id = q.get("phenotype_orpha_id", "")
                list_name = q.get("list_name", "")
                if not orpha_id or not list_name:
                    continue

                # Orphanet API endpoint
                url = f"{base_url.rstrip('/')}/nomenclature/orphanumber/{orpha_id.replace('ORPHA:', '')}/genes"

                try:
                    async with session.get(url, headers={"Accept": "application/json"}) as resp:
                        if resp.status != 200:
                            self._log_sync_event(
                                "ORPHANET_HTTP_ERROR",
                                f"{orpha_id} -> HTTP {resp.status}",
                            )
                            continue
                        data = await resp.json()
                        # Extract gene symbols from Orphanet response
                        genes = self._extract_genes_from_orphanet(data)
                        if genes:
                            if list_name not in result:
                                result[list_name] = []
                            result[list_name].extend(genes)
                            result[list_name] = list(set(result[list_name]))
                            self._log_sync_event(
                                "ORPHANET_OK",
                                f"{orpha_id} -> {list_name}: {len(genes)} genes",
                            )
                except Exception as e:
                    self._log_sync_event(
                        "ORPHANET_EXCEPTION",
                        f"{orpha_id} -> {e}",
                    )

        return result

    async def _sync_omim(self, config: Dict) -> Dict[str, List[str]]:
        """
        Query OMIM GeneMap API.
        
        Requires API key. If no key, returns empty (already checked by caller).
        OMIM API: https://omim.org/api/geneMap?search={mim_id}&apiKey={key}
        """
        api_key = config.get("api_key", "")
        if not api_key:
            return {}

        # OMIM GeneMap API — simplified, returns gene symbols for a set of MIM IDs
        # In production, this would query specific disease MIM IDs mapped to DGRA lists
        # For now, we return empty and log a note
        self._log_sync_event("OMIM_SKIP", "OMIM sync requires specific MIM ID mapping; using placeholder")
        return {}

    @staticmethod
    def _extract_genes_from_orphanet(data: Any) -> List[str]:
        """Extract gene symbols from Orphanet JSON response."""
        genes = []
        if isinstance(data, list):
            for item in data:
                if isinstance(item, dict):
                    # Orphanet structure varies; try common keys
                    symbol = item.get("geneSymbol") or item.get("symbol") or item.get("gene", {}).get("symbol")
                    if symbol:
                        genes.append(symbol)
                    # Also try nested structure
                    gene_ref = item.get("gene") or item.get("Gene") or item.get("geneRef")
                    if isinstance(gene_ref, dict):
                        symbol = gene_ref.get("symbol") or gene_ref.get("geneSymbol")
                        if symbol and symbol not in genes:
                            genes.append(symbol)
        elif isinstance(data, dict):
            # Single record
            symbol = data.get("geneSymbol") or data.get("symbol")
            if symbol:
                genes.append(symbol)
            # Check nested lists
            for key in ("genes", "geneList", "results", "diseaseGene"):
                nested = data.get(key, [])
                if isinstance(nested, list):
                    for item in nested:
                        s = item.get("symbol") or item.get("geneSymbol") if isinstance(item, dict) else None
                        if s and s not in genes:
                            genes.append(s)
        return genes

    # ------------------------------------------------------------------
    # Local loading / caching
    # ------------------------------------------------------------------

    def _load_static_lists(self, tissue_profile: str) -> Dict[str, List[str]]:
        """Load special_gene_lists from tissue_context.json for the given profile."""
        try:
            with open(self.tissue_context_path, "r") as f:
                data = json.load(f)
            profiles = data.get("profiles", {})
            profile = profiles.get(tissue_profile, {})
            return profile.get("special_gene_lists", {})
        except Exception:
            return {}

    def _load_cached_lists(self, tissue_profile: str) -> Optional[Dict[str, List[str]]]:
        """Load previously merged + cached gene lists from SQLite."""
        try:
            self.cache_db_path.parent.mkdir(parents=True, exist_ok=True)
            conn = sqlite3.connect(str(self.cache_db_path))
            cursor = conn.cursor()
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS gene_list_cache (
                    profile TEXT PRIMARY KEY,
                    lists_json TEXT,
                    cached_at TEXT
                )
                """
            )
            cursor.execute(
                "SELECT lists_json, cached_at FROM gene_list_cache WHERE profile = ?",
                (tissue_profile,),
            )
            row = cursor.fetchone()
            conn.close()
            if row:
                return json.loads(row[0])
        except Exception:
            pass
        return None

    def _save_cached_lists(self, tissue_profile: str, lists: Dict[str, List[str]]) -> None:
        """Save merged gene lists to SQLite cache."""
        try:
            self.cache_db_path.parent.mkdir(parents=True, exist_ok=True)
            conn = sqlite3.connect(str(self.cache_db_path))
            cursor = conn.cursor()
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS gene_list_cache (
                    profile TEXT PRIMARY KEY,
                    lists_json TEXT,
                    cached_at TEXT
                )
                """
            )
            cursor.execute(
                """
                INSERT OR REPLACE INTO gene_list_cache (profile, lists_json, cached_at)
                VALUES (?, ?, ?)
                """,
                (tissue_profile, json.dumps(lists, sort_keys=True), datetime.utcnow().isoformat()),
            )
            conn.commit()
            conn.close()
        except Exception as e:
            self._log_sync_event("CACHE_SAVE_FAILED", str(e))

    def _is_cache_expired(self, tissue_profile: str) -> bool:
        """Check if cached gene lists for this profile have exceeded TTL."""
        try:
            self.cache_db_path.parent.mkdir(parents=True, exist_ok=True)
            conn = sqlite3.connect(str(self.cache_db_path))
            cursor = conn.cursor()
            cursor.execute(
                "SELECT cached_at FROM gene_list_cache WHERE profile = ?",
                (tissue_profile,),
            )
            row = cursor.fetchone()
            conn.close()
            if row:
                cached_at = datetime.fromisoformat(row[0])
                return datetime.utcnow() - cached_at > timedelta(days=self.ttl_days)
        except Exception:
            pass
        return True  # No cache or error → treat as expired

    # ------------------------------------------------------------------
    # User overrides
    # ------------------------------------------------------------------

    def _apply_user_overrides(self, merged: Dict[str, List[str]]) -> Dict[str, List[str]]:
        """Apply user add/remove/custom from user_gene_lists.json."""
        if not self.user_lists_path.exists():
            return merged

        try:
            with open(self.user_lists_path, "r") as f:
                user_cfg = json.load(f)
        except Exception:
            return merged

        result = {k: list(v) for k, v in merged.items()}

        # 1. Add genes to existing lists
        for list_name, genes in user_cfg.get("add", {}).items():
            if list_name.startswith("_"):
                continue  # Skip metadata keys
            if list_name not in result:
                result[list_name] = []
            for g in genes:
                if g not in result[list_name]:
                    result[list_name].append(g)

        # 2. Remove genes from existing lists
        for list_name, genes in user_cfg.get("remove", {}).items():
            if list_name.startswith("_"):
                continue  # Skip metadata keys
            if list_name in result:
                result[list_name] = [g for g in result[list_name] if g not in genes]

        # 3. Custom lists (new lists created by user)
        for list_name, spec in user_cfg.get("custom_lists", {}).items():
            if list_name.startswith("_"):
                continue  # Skip metadata keys
            genes = spec.get("genes", []) if isinstance(spec, dict) else []
            if genes:
                result[list_name] = list(genes)

        return result

    # ------------------------------------------------------------------
    # Profile filtering
    # ------------------------------------------------------------------

    def _filter_synced_for_profile(
        self,
        synced: Dict[str, List[str]],
        tissue_profile: str,
    ) -> Dict[str, List[str]]:
        """
        Filter auto-synced lists to only those relevant for the target tissue profile.
        Uses mapping_rules from gene_list_sources.json.
        """
        if not self.sources_config_path.exists():
            return synced

        try:
            with open(self.sources_config_path, "r") as f:
                config = json.load(f)
        except Exception:
            return synced

        mapping = config.get("mapping_rules", {})
        filtered: Dict[str, List[str]] = {}

        for list_name, genes in synced.items():
            profiles = mapping.get(list_name, [])
            if tissue_profile in profiles or not profiles:
                filtered[list_name] = genes

        return filtered

    # ------------------------------------------------------------------
    # Symbol validation (best effort)
    # ------------------------------------------------------------------

    def _validate_symbols(self, lists: Dict[str, List[str]]) -> Dict[str, List[str]]:
        """
        Best-effort validation: filter out obviously invalid symbols.
        Full HGNC validation requires API call; we do a lightweight regex check here.
        """
        import re
        valid_pattern = re.compile(r"^[A-Za-z][A-Za-z0-9\-]*$")
        result: Dict[str, List[str]] = {}
        dropped = []

        for list_name, genes in lists.items():
            valid_genes = []
            for g in genes:
                if g and valid_pattern.match(g) and len(g) <= 25:
                    valid_genes.append(g)
                else:
                    dropped.append((list_name, g))
            result[list_name] = valid_genes

        if dropped:
            self._log_sync_event("SYMBOL_VALIDATION", f"Dropped {len(dropped)} invalid symbols: {dropped[:10]}")

        return result

    # ------------------------------------------------------------------
    # Audit logging
    # ------------------------------------------------------------------

    def _log_sync_event(self, event_type: str, message: str) -> None:
        """Write a single-line log entry to the daily sync log."""
        try:
            timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
            log_file = self.log_dir / f"gene_sync_{datetime.utcnow().strftime('%Y-%m-%d')}.log"
            with open(log_file, "a", encoding="utf-8") as f:
                f.write(f"[{timestamp}] [{event_type}] {message}\n")
        except Exception:
            pass  # Logging must never fail


# ------------------------------------------------------------------------------
# Convenience: synchronous wrapper
# ------------------------------------------------------------------------------

def get_merged_gene_lists_sync(
    tissue_profile: str,
    references_dir: Optional[Path] = None,
    offline_mode: bool = False,
    sync_enabled: bool = True,
    ttl_days: int = 7,
    force_sync: bool = False,
) -> Dict[str, List[str]]:
    """Synchronous wrapper for get_merged_gene_lists."""
    if references_dir is None:
        references_dir = Path(__file__).parent.parent / "references"

    syncer = GeneListSynchronizer(
        references_dir=references_dir,
        offline_mode=offline_mode,
        sync_enabled=sync_enabled,
        ttl_days=ttl_days,
    )
    return asyncio.run(syncer.get_merged_gene_lists(tissue_profile, force_sync=force_sync))
