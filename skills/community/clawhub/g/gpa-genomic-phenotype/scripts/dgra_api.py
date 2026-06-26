#!/usr/bin/env python3
"""
DGRA API Query Layer
Phase 1 - v0.4 Architecture

Async API wrappers for Ensembl, UniProt, GTEx, gnomAD, and NCBI E-utilities.
Each wrapper implements: query -> cache check -> API call -> cache store -> return.
All functions are async and use aiohttp for concurrent requests.

Skeleton implementation: defines interfaces, implements basic HTTP logic,
leaves full response parsing for Phase 2.
"""

import asyncio
import aiohttp
import hashlib
import json
import time
from typing import Optional, Dict, Any, List
from pathlib import Path

from dgra_config import DGRAGlobalConfig, APIConfig
from dgra_cache import DGRACache


class DGRAAPIError(Exception):
    """Base exception for API errors."""
    def __init__(self, api_name: str, message: str, status: Optional[int] = None, 
                 response: Optional[str] = None):
        self.api_name = api_name
        self.status = status
        self.response = response
        super().__init__(f"[{api_name}] {message}")


class DGRAAPIClient:
    """
    Unified async API client for all DGRA external data sources.
    
    Handles:
    - Cache lookup before API call
    - Rate limiting (per-API token bucket)
    - Retry with exponential backoff
    - Response caching on success
    - Offline mode fallback (skip API, return cached or None)
    """
    
    def __init__(self, config: DGRAGlobalConfig, cache: DGRACache):
        self.config = config
        self.cache = cache
        self._session: Optional[aiohttp.ClientSession] = None
        self._last_request_time: Dict[str, float] = {}  # api_name -> timestamp
    
    async def __aenter__(self):
        self._session = aiohttp.ClientSession(
            connector=aiohttp.TCPConnector(limit=50, limit_per_host=20),
            timeout=aiohttp.ClientTimeout(total=120),
            trust_env=True,  # Auto-read HTTP_PROXY / HTTPS_PROXY from environment
        )
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self._session:
            await self._session.close()
            self._session = None
    
    async def _rate_limit(self, api_name: str):
        """Enforce per-API rate limit using token bucket logic."""
        cfg = self.config.apis[api_name]
        min_interval = 1.0 / cfg.rate_limit_per_sec
        now = time.time()
        last = self._last_request_time.get(api_name, 0)
        elapsed = now - last
        if elapsed < min_interval:
            await asyncio.sleep(min_interval - elapsed)
        self._last_request_time[api_name] = time.time()
    
    async def _request_with_retry(
        self, 
        api_name: str,
        endpoint: str,
        method: str = "GET",
        params: Optional[Dict] = None,
        json_body: Optional[Dict] = None,
        headers: Optional[Dict] = None,
    ) -> Dict[str, Any]:
        """
        Execute HTTP request with cache check, rate limiting, and retry.
        
        Returns dict with keys:
        - data: parsed JSON response
        - http_status: HTTP status code
        - from_cache: bool
        - confidence: 'high' if cache hit, 'medium' if API success, 'low' if partial
        """
        cfg = self.config.apis[api_name]
        url = f"{cfg.base_url}/{endpoint.lstrip('/')}"
        
        # Phase 1: Check cache (skip if offline mode - we already checked before calling)
        cache_key_params = {"url": url, **(params or {})}
        cached = self.cache.get(api_name, **cache_key_params)
        
        if cached:
            return {
                "data": cached["data"],
                "http_status": cached["http_status"],
                "from_cache": True,
                "confidence": cached["confidence"],
            }
        
        # Offline mode: no cache hit = return None
        if self.config.offline_mode:
            return {
                "data": None,
                "http_status": None,
                "from_cache": False,
                "confidence": "low",
                "error": "Offline mode: no cached data available",
            }
        
        # Phase 2: API call with retry
        last_error = None
        for attempt in range(cfg.max_retries):
            try:
                await self._rate_limit(api_name)
                
                async with self._session.request(
                    method=method,
                    url=url,
                    params=params,
                    json=json_body,
                    headers=headers,
                    proxy=cfg.proxy,  # Explicit proxy from config; falls back to env via trust_env if None
                    timeout=aiohttp.ClientTimeout(total=cfg.timeout),
                ) as response:
                    http_status = response.status
                    
                    if http_status == 200:
                        try:
                            data = await response.json()
                        except Exception:
                            # Try to parse text as JSON fallback
                            text = await response.text()
                            try:
                                data = json.loads(text)
                            except Exception:
                                # Not valid JSON — don't cache, return as error
                                return {
                                    "data": None,
                                    "http_status": http_status,
                                    "from_cache": False,
                                    "confidence": "low",
                                    "error": f"HTTP 200 but response is not valid JSON (len={len(text)})",
                                }
                        
                        # Cache successful response
                        self.cache.set(
                            api_name=api_name,
                            response_data=data,
                            http_status=http_status,
                            confidence="medium",
                            **cache_key_params
                        )
                        
                        return {
                            "data": data,
                            "http_status": http_status,
                            "from_cache": False,
                            "confidence": "medium",
                        }
                    
                    elif http_status == 404:
                        # Not found - cache the negative result with shorter TTL
                        self.cache.set(
                            api_name=api_name,
                            response_data={"error": "not_found", "status": 404},
                            http_status=404,
                            confidence="medium",
                            ttl_days=7,  # Shorter TTL for negatives
                            **cache_key_params
                        )
                        return {
                            "data": None,
                            "http_status": 404,
                            "from_cache": False,
                            "confidence": "medium",
                            "error": "Not found",
                        }
                    
                    elif http_status == 429:
                        # Rate limited - read Retry-After header and wait
                        retry_after = response.headers.get("Retry-After")
                        if retry_after:
                            wait = int(retry_after)
                        else:
                            wait = cfg.retry_delay * (2 ** attempt)
                        last_error = DGRAAPIError(api_name, f"Rate limited (429), retry after {wait}s", http_status)
                        print(f"[DGRA API] {api_name}: Rate limited (429), waiting {wait}s before retry {attempt+1}/{cfg.max_retries}")
                        await asyncio.sleep(wait)
                        continue
                    
                    elif http_status in (502, 503, 504):
                        # Gateway/server temporarily unavailable - retry
                        last_error = DGRAAPIError(api_name, f"Server temporarily unavailable ({http_status})", http_status)
                        wait = cfg.retry_delay * (2 ** attempt)
                        print(f"[DGRA API] {api_name}: HTTP {http_status}, retrying in {wait}s (attempt {attempt+1}/{cfg.max_retries})")
                        await asyncio.sleep(wait)
                        continue
                    
                    elif http_status >= 500:
                        # Other server errors - retry with backoff
                        last_error = DGRAAPIError(api_name, f"Server error {http_status}", http_status)
                        wait = cfg.retry_delay * (2 ** attempt)
                        print(f"[DGRA API] {api_name}: HTTP {http_status}, retrying in {wait}s (attempt {attempt+1}/{cfg.max_retries})")
                        await asyncio.sleep(wait)
                        continue
                    
                    else:
                        # Client error or other - don't retry
                        text = await response.text()
                        return {
                            "data": None,
                            "http_status": http_status,
                            "from_cache": False,
                            "confidence": "low",
                            "error": f"HTTP {http_status}: {text[:200]}",
                        }
            
            except asyncio.TimeoutError:
                last_error = DGRAAPIError(api_name, f"Timeout after {cfg.timeout}s")
                wait = cfg.retry_delay * (2 ** attempt)
                print(f"[DGRA API] {api_name}: Timeout, retrying in {wait}s (attempt {attempt+1}/{cfg.max_retries})")
                await asyncio.sleep(wait)
                continue
            
            except aiohttp.ClientError as e:
                last_error = DGRAAPIError(api_name, f"Connection error: {e}")
                wait = cfg.retry_delay * (2 ** attempt)
                print(f"[DGRA API] {api_name}: Connection error ({e}), retrying in {wait}s (attempt {attempt+1}/{cfg.max_retries})")
                await asyncio.sleep(wait)
                continue
        
        # All retries exhausted
        return {
            "data": None,
            "http_status": last_error.status if last_error else None,
            "from_cache": False,
            "confidence": "low",
            "error": str(last_error) if last_error else "All retries failed",
        }
    
    # =====================================================================
    # Ensembl REST API
    # =====================================================================
    
    async def query_ensembl_gene(self, gene_symbol: str) -> Dict[str, Any]:
        """
        Query Ensembl for gene canonical transcript, biotype, and basic info.
        
        Endpoint: GET /lookup/symbol/homo_sapiens/{gene_symbol}?expand=1
        
        Returns:
        {
            "canonical_transcript": "ENST...",
            "biotype": "protein_coding",
            "description": "...",
            "seq_region_name": "chr...",
            "start": 12345,
            "end": 67890,
            "strand": 1,
            "source": "ensembl|cache",
            "confidence": "high|medium|low",
        }
        """
        result = await self._request_with_retry(
            api_name="ensembl",
            endpoint=f"/lookup/symbol/homo_sapiens/{gene_symbol}",
            params={"expand": "1", "content-type": "application/json"},
        )
        
        if result["data"] and result["http_status"] == 200:
            data = result["data"]
            # Extract canonical transcript (usually the first or longest)
            transcripts = data.get("Transcript", [])
            canonical = None
            for tx in transcripts:
                if tx.get("is_canonical", 0) == 1:
                    canonical = tx["id"]
                    break
            if not canonical and transcripts:
                canonical = transcripts[0]["id"]  # Fallback to first
            
            return {
                "canonical_transcript": canonical,
                "biotype": data.get("biotype"),
                "description": data.get("description"),
                "seq_region_name": data.get("seq_region_name"),
                "start": data.get("start"),
                "end": data.get("end"),
                "strand": data.get("strand"),
                "source": "cache" if result["from_cache"] else "ensembl",
                "confidence": result["confidence"],
                "raw": data,  # Keep full response for Phase 2 parsing
            }
        
        return {
            "canonical_transcript": None,
            "biotype": None,
            "description": None,
            "source": "failed",
            "confidence": "low",
            "error": result.get("error"),
            "raw": None,
        }
    
    async def query_ensembl_transcript_info(self, transcript_id: str) -> Dict[str, Any]:
        """
        Query Ensembl for transcript details (CDS, exons, translation).
        
        Endpoint: GET /lookup/id/{transcript_id}?expand=1
        """
        result = await self._request_with_retry(
            api_name="ensembl",
            endpoint=f"/lookup/id/{transcript_id}",
            params={"expand": "1"},
        )
        
        if result["data"] and result["http_status"] == 200:
            data = result["data"]
            return {
                "transcript_id": data.get("id"),
                "display_name": data.get("display_name"),
                "biotype": data.get("biotype"),
                "cds_length": len(data.get("CDS", [])),
                "exon_count": len(data.get("Exon", [])),
                "translation_id": data.get("Translation", {}).get("id") if data.get("Translation") else None,
                "source": "cache" if result["from_cache"] else "ensembl",
                "confidence": result["confidence"],
                "raw": data,
            }
        
        return {
            "transcript_id": transcript_id,
            "source": "failed",
            "confidence": "low",
            "error": result.get("error"),
            "raw": None,
        }
    

    async def query_ensembl_vep_region(self, chrom: str, pos: int, ref: str, alt: str) -> Dict[str, Any]:
        """
        Query Ensembl VEP for canonical transcript annotation of a specific variant.

        Endpoint: POST /vep/human/region
        Body: ["{chrom} {pos} . {ref} {alt} . . ."]
        Params: canonical=1&domains=1&protein=1&hgvs=1&mane_select=1

        Parses VEP JSON response to extract canonical transcript's:
        - consequence_terms
        - impact
        - hgvsc
        - hgvsp
        - transcript_id
        - protein_domains

        Returns structured dict with these fields.
        """
        variant_string = f"{chrom} {pos} . {ref} {alt} . . ."
        # Include body hash in params for cache key uniqueness (server ignores unknown params)
        body_hash = hashlib.md5(json.dumps([variant_string], sort_keys=True).encode()).hexdigest()[:16]
        params = {
            "canonical": "1",
            "domains": "1",
            "protein": "1",
            "hgvs": "1",
            "mane_select": "1",
            "_body_hash": body_hash,
        }
        result = await self._request_with_retry(
            api_name="ensembl",
            endpoint="/vep/human/region",
            method="POST",
            json_body=[variant_string],
            params=params,
        )

        if result["data"] and result["http_status"] == 200:
            data = result["data"]
            if not data or not isinstance(data, list):
                return {
                    "consequence_terms": [],
                    "impact": None,
                    "hgvsc": None,
                    "hgvsp": None,
                    "transcript_id": None,
                    "protein_domains": [],
                    "source": "failed",
                    "confidence": "low",
                    "error": "Invalid VEP response format (expected list)",
                }

            parsed = self._parse_vep_batch_response(data, [{"chrom": chrom, "pos": pos, "ref": ref, "alt": alt}])
            if parsed:
                return parsed[0]

        return {
            "consequence_terms": [],
            "impact": None,
            "hgvsc": None,
            "hgvsp": None,
            "transcript_id": None,
            "protein_domains": [],
            "source": "failed",
            "confidence": "low",
            "error": result.get("error"),
        }

    def _parse_vep_batch_response(self, data: List[Dict], variants: List[Dict]) -> List[Dict]:
        """Parse VEP batch response, matching results to input variants.

        For each variant result, finds the canonical transcript consequence
        (prioritizing: canonical=1 > MANE Select > protein_coding > first).
        """
        results = []
        for idx, variant_result in enumerate(data):
            if not isinstance(variant_result, dict):
                results.append({
                    "error": "Invalid VEP response format",
                    "source": "failed",
                    "confidence": "low",
                })
                continue

            tx_consequences = variant_result.get("transcript_consequences", [])
            canonical_tx = None
            # Priority 1: canonical=1
            for tx in tx_consequences:
                if tx.get("canonical") == 1:
                    canonical_tx = tx
                    break
            # Priority 2: MANE Select
            if not canonical_tx:
                for tx in tx_consequences:
                    if tx.get("mane_select"):
                        canonical_tx = tx
                        break
            # Priority 3: protein_coding biotype
            if not canonical_tx:
                for tx in tx_consequences:
                    if tx.get("biotype") == "protein_coding":
                        canonical_tx = tx
                        break
            # Priority 4: first available
            if not canonical_tx and tx_consequences:
                canonical_tx = tx_consequences[0]

            if canonical_tx:
                # Parse protein_domains
                # VEP returns protein_domains as list of strings: "Db:ID:Name" or dicts
                domains = []
                raw_domains = canonical_tx.get("protein_domains", [])
                for d in raw_domains:
                    if isinstance(d, dict):
                        domains.append({
                            "name": d.get("name", d.get("description", "unnamed")),
                            "start": d.get("start", d.get("beg")),
                            "end": d.get("end"),
                            "db": d.get("db"),
                        })
                    elif isinstance(d, str):
                        parts = d.split(":")
                        if len(parts) >= 3:
                            domains.append({
                                "name": parts[2],
                                "db": parts[0],
                                "interpro_id": parts[1] if len(parts) > 1 else None,
                            })
                        elif len(parts) == 2:
                            domains.append({
                                "name": parts[1],
                                "db": parts[0],
                            })

                results.append({
                    "consequence_terms": canonical_tx.get("consequence_terms", []),
                    "impact": canonical_tx.get("impact"),
                    "hgvsc": canonical_tx.get("hgvsc"),
                    "hgvsp": canonical_tx.get("hgvsp"),
                    "transcript_id": canonical_tx.get("transcript_id"),
                    "gene_symbol": canonical_tx.get("gene_symbol"),
                    "protein_domains": domains,
                    "source": "ensembl",
                    "confidence": "medium",
                    "raw": variant_result,
                })
            else:
                results.append({
                    "error": "No transcript consequences found",
                    "source": "ensembl",
                    "confidence": "low",
                })

        return results

    async def batch_query_vep_region(self, variants: List[Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
        """
        Batch query Ensembl VEP for multiple variants with controlled concurrency.

        VEP API accepts multiple variants per POST request.
        Strategy: chunk variants (max 50 per request) + semaphore (max 5 concurrent).

        Args:
            variants: List of dicts with keys chrom, pos, ref, alt, and optionally key.

        Returns:
            Dict mapping variant key -> VEP result dict.
        """
        if not variants:
            return {}

        CHUNK_SIZE = 50
        MAX_CONCURRENT = 5
        semaphore = asyncio.Semaphore(MAX_CONCURRENT)

        async def _query_chunk(chunk: List[Dict]) -> List[Dict]:
            async with semaphore:
                body = [f"{v['chrom']} {v['pos']} . {v['ref']} {v['alt']} . . ." for v in chunk]
                # Body hash for cache key uniqueness
                body_hash = hashlib.md5(json.dumps(body, sort_keys=True).encode()).hexdigest()[:16]
                params = {
                    "canonical": "1",
                    "domains": "1",
                    "protein": "1",
                    "hgvs": "1",
                    "mane_select": "1",
                    "_body_hash": body_hash,
                }
                result = await self._request_with_retry(
                    api_name="ensembl",
                    endpoint="/vep/human/region",
                    method="POST",
                    json_body=body,
                    params=params,
                )
                if result["data"] and result["http_status"] == 200:
                    return self._parse_vep_batch_response(result["data"], chunk)
                else:
                    return [{"error": result.get("error"), "source": "failed", "confidence": "low"} for _ in chunk]

        all_results = {}
        total = len(variants)
        for i in range(0, total, CHUNK_SIZE):
            chunk = variants[i:i + CHUNK_SIZE]
            chunk_results = await _query_chunk(chunk)
            for v, r in zip(chunk, chunk_results):
                key = v.get("key", f"{v['chrom']}:{v['pos']}_{v['ref']}>{v['alt']}")
                all_results[key] = r
            # Brief pause between chunks
            if i + CHUNK_SIZE < total:
                await asyncio.sleep(0.5)

        return all_results

    # =====================================================================
    # UniProt REST API
    # =====================================================================
    
    async def query_uniprot_by_gene(self, gene_symbol: str) -> Dict[str, Any]:
        """
        Query UniProt for protein entry by gene symbol.
        
        Step 1: Search gene -> uniprot ID mapping
        Step 2: Query /uniprotkb/{id}.json for full entry
        
        Returns:
        {
            "uniprot_id": "P12345",
            "protein_name": "...",
            "sequence_length": 1250,
            "domains": [
                {"name": "Motor domain", "start": 1, "end": 780, "type": "DOMAIN"},
                ...
            ],
            "go_terms": ["GO:0005524", ...],
            "source": "uniprot|cache",
            "confidence": "high|medium|low",
        }
        """
        # Step 1: Search — fetch up to 5 results, prefer reviewed/canonical with longest sequence
        search_result = await self._request_with_retry(
            api_name="uniprot",
            endpoint="/uniprotkb/search",
            params={
                "query": f"gene:{gene_symbol} AND organism_id:9606",
                "format": "json",
                "size": 5,
            },
        )
        
        if not (search_result["data"] and search_result["http_status"] == 200):
            return {
                "uniprot_id": None,
                "protein_name": None,
                "domains": [],
                "go_terms": [],
                "interpro_ids": [],
                "source": "failed",
                "confidence": "low",
                "error": search_result.get("error"),
            }
        
        # Extract uniprot ID from search results — prefer reviewed + longest sequence
        search_data = search_result["data"]
        results = search_data.get("results", [])
        if not results:
            return {
                "uniprot_id": None,
                "protein_name": None,
                "domains": [],
                "go_terms": [],
                "interpro_ids": [],
                "source": "uniprot",
                "confidence": "medium",
                "error": "No UniProt entry found for gene",
            }
        
        # Pick best entry: reviewed (Swiss-Prot) preferred, then longest sequence
        def _entry_score(entry):
            is_reviewed = 1 if entry.get("entryType") == "UniProtKB reviewed (Swiss-Prot)" else 0
            seq_len = entry.get("sequence", {}).get("length", 0) or 0
            return (is_reviewed, seq_len)
        
        sorted_results = sorted(results, key=_entry_score, reverse=True)
        best_entry = sorted_results[0]
        uniprot_id = best_entry.get("primaryAccession")
        
        # Step 2: Fetch full entry
        entry_result = await self._request_with_retry(
            api_name="uniprot",
            endpoint=f"/uniprotkb/{uniprot_id}.json",
        )
        
        if entry_result["data"] and entry_result["http_status"] == 200:
            data = entry_result["data"]
            
            # Extract domains from features
            domains = []
            for feature in data.get("features", []):
                if feature.get("type", "").lower() in ("domain", "region", "repeat", "zn_fing", "dna_bind"):
                    loc = feature.get("location", {})
                    start = loc.get("start", {}).get("value")
                    end = loc.get("end", {}).get("value")
                    if start and end:
                        domains.append({
                            "name": feature.get("description", "unnamed"),
                            "start": start,
                            "end": end,
                            "type": feature.get("type"),
                        })
            
            # Extract GO terms
            go_terms = []
            for ref in data.get("uniProtKBCrossReferences", []):
                if ref.get("database") == "GO":
                    go_id = ref.get("id")
                    if go_id:
                        go_terms.append(go_id)
            
            # Extract InterPro IDs
            interpro_ids = []
            for ref in data.get("uniProtKBCrossReferences", []):
                if ref.get("database") == "InterPro":
                    ip_id = ref.get("id")
                    if ip_id:
                        interpro_ids.append(ip_id)
            
            # Protein name
            protein_desc = data.get("proteinDescription", {})
            rec_name = protein_desc.get("recommendedName", {}).get("fullName", {}).get("value", "")
            
            seq_length = None
            seq_info = data.get("sequence", {})
            if seq_info:
                seq_length = seq_info.get("length")
            
            return {
                "uniprot_id": uniprot_id,
                "protein_name": rec_name,
                "sequence_length": seq_length,
                "domains": domains,
                "go_terms": go_terms,
                "interpro_ids": interpro_ids,
                "source": "cache" if entry_result["from_cache"] else "uniprot",
                "confidence": entry_result["confidence"],
                "raw": data,
            }
        
        return {
            "uniprot_id": uniprot_id,
            "protein_name": None,
            "domains": [],
            "go_terms": [],
            "interpro_ids": [],
            "source": "failed",
            "confidence": "low",
            "error": entry_result.get("error"),
        }
    
    # =====================================================================
    # GTEx Portal API
    # =====================================================================
    
    async def query_gtex_expression(self, gene_id: str, tissue: str) -> Dict[str, Any]:
        """
        Query GTEx v2 API for median gene expression in a specific tissue.
        
        GTEx v2 requires versioned gencodeIds (e.g. ENSG00000110799.13).
        Two-step process:
          1. Resolve gene symbol -> versioned gencodeId (cached)
          2. Query medianGeneExpression endpoint
        
        Returns:
        {
            "gene": "VWF",
            "tissue": "Whole_Blood",
            "median_tpm": 268.7,
            "unit": "TPM",
            "source": "gtex|cache",
            "confidence": "medium",
        }
        """
        # --- Step 1: Resolve gene symbol -> versioned gencodeId ---
        gencode_map = self._load_gencode_cache()
        gencode_id = gencode_map.get(gene_id)
        
        if not gencode_id:
            # Query GTEx get_genes endpoint
            search_result = await self._request_with_retry(
                api_name="gtex",
                endpoint="/reference/gene",
                params={
                    "geneId": gene_id,
                    "page": 0,
                    "itemsPerPage": 10,
                },
            )
            
            if search_result["data"] and search_result["http_status"] == 200:
                data = search_result["data"]
                items = data.get("data", [])
                if items:
                    # Prefer exact symbol match
                    for item in items:
                        if item.get("geneSymbol") == gene_id:
                            gencode_id = item.get("gencodeId")
                            break
                    if not gencode_id:
                        gencode_id = items[0].get("gencodeId")
                
                if gencode_id:
                    gencode_map[gene_id] = gencode_id
                    self._save_gencode_cache(gencode_map)
        
        if not gencode_id:
            return {
                "gene": gene_id,
                "tissue": tissue,
                "median_tpm": None,
                "unit": "TPM",
                "source": "failed",
                "confidence": "low",
                "error": f"Could not resolve gencodeId for {gene_id}",
            }
        
        # --- Step 2: Query medianGeneExpression ---
        # GTEx tissue IDs use underscores: "Whole_Blood", "Heart_Left_Ventricle"
        gtex_tissue = tissue.replace(" - ", "_").replace(" ", "_")
        
        result = await self._request_with_retry(
            api_name="gtex",
            endpoint="/expression/medianGeneExpression",
            params={
                "gencodeId": gencode_id,
                "tissueSiteDetailIds": gtex_tissue,
                "datasetId": "gtex_v8",
            },
        )
        
        if result["data"] and result["http_status"] == 200:
            data = result["data"]
            items = data.get("data", [])
            
            # Find the tissue-specific record
            median_val = None
            for item in items:
                if item.get("tissueSiteDetailId") == gtex_tissue:
                    median_val = item.get("median")
                    break
            
            # Fallback: if tissue not found but data exists, return first (for debugging)
            if median_val is None and items:
                median_val = items[0].get("median")
            
            return {
                "gene": gene_id,
                "tissue": tissue,
                "median_tpm": median_val,
                "unit": "TPM",
                "gencode_id": gencode_id,
                "source": "cache" if result["from_cache"] else "gtex",
                "confidence": result["confidence"],
                "raw": data,
            }
        
        return {
            "gene": gene_id,
            "tissue": tissue,
            "median_tpm": None,
            "unit": "TPM",
            "gencode_id": gencode_id,
            "source": "failed",
            "confidence": "low",
            "error": result.get("error"),
        }
    
    def _load_gencode_cache(self) -> Dict[str, str]:
        """Load gene symbol -> gencodeId mapping cache."""
        _script_dir = Path(__file__).resolve().parent
        cache_path = _script_dir / ".." / "references" / "offline_data" / "gtex_gencode_map.json"
        if cache_path.exists():
            try:
                with open(cache_path, "r") as f:
                    return json.load(f)
            except Exception:
                pass
        return {}
    
    def _save_gencode_cache(self, cache: Dict[str, str]) -> None:
        """Save gene symbol -> gencodeId mapping cache."""
        _script_dir = Path(__file__).resolve().parent
        cache_path = _script_dir / ".." / "references" / "offline_data" / "gtex_gencode_map.json"
        cache_path.parent.mkdir(parents=True, exist_ok=True)
        with open(cache_path, "w") as f:
            json.dump(cache, f, indent=2, sort_keys=True)
    
    async def query_gtex_expression_multi(self, gene_id: str, tissues: List[str]) -> List[Dict[str, Any]]:
        """
        Query GTEx v2 API for median gene expression across multiple tissues.
        
        Uses asyncio.gather to concurrently query all tissues.
        Returns a list of individual tissue results.
        
        Args:
            gene_id: Gene symbol (e.g., "VWF")
            tissues: List of GTEx tissue names (e.g., ["Bone Marrow", "Whole Blood"])
            
        Returns:
            List of result dicts, one per tissue (same format as query_gtex_expression)
        """
        if not tissues:
            return []
        
        # Launch concurrent queries for all tissues
        tasks = [self.query_gtex_expression(gene_id, tissue) for tissue in tissues]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        processed = []
        for tissue, result in zip(tissues, results):
            if isinstance(result, Exception):
                processed.append({
                    "gene": gene_id,
                    "tissue": tissue,
                    "median_tpm": None,
                    "unit": "TPM",
                    "source": "failed",
                    "confidence": "low",
                    "error": str(result),
                })
            else:
                processed.append(result)
        
        return processed
    
    # =====================================================================
    # gnomAD GraphQL API
    # =====================================================================
    
    async def query_gnomad_variant(self, chrom: str, pos: int, ref: str, alt: str,
                                    dataset: str = "gnomad_r4",
                                    populations: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Query gnomAD for variant allele frequency and constraint metrics.
        v0.5 P1-1: Population subgroup frequencies (EAS, AMR, AFR, NFE, SAS, etc.)
        
        Uses GraphQL API. Returns structured frequency data including per-population AFs.
        
        Args:
            populations: List of population codes to query. Default: ["EAS", "AMR", "AFR", "NFE", "SAS", "ASJ", "FIN"]
        
        Returns:
        {
            "variant_id": "1-12345-A-G",
            "af": 0.00123,           # overall combined AF
            "af_popmax": 0.00234,   # max across populations
            "af_populations": {      # per-population AFs
                "EAS": {"af": 0.0001, "ac": 1, "an": 15278},
                "AMR": {"af": 0.0023, "ac": 3, "an": 13000},
                ...
            },
            "an": 152000,
            "hom_count": 2,
            "gene_constraint": {"lof_z": 2.5, "pLI": 0.99},
            "source": "gnomad|cache",
            "confidence": "medium",
        }
        """
        if populations is None:
            populations = ["EAS", "AMR", "AFR", "NFE", "SAS", "ASJ", "FIN", "MID", "OTH"]
        
        # Build populations query fragment dynamically
        pop_fields = "\n".join(
            f"""                {pop} {{
                    ac
                    an
                    homozygote_count
                }}""" for pop in populations
        )
        
        query = f"""
        query VariantQuery($variantId: String!, $datasetId: DatasetId!) {{
            variant(variantId: $variantId, dataset: $datasetId) {{
                variantId
                exome {{
                    af
                    an
                    ac
                    homozygote_count
                    populations {{
{pop_fields}
                    }}
                }}
                genome {{
                    af
                    an
                    ac
                    homozygote_count
                    populations {{
{pop_fields}
                    }}
                }}
            }}
        }}
        """
        variant_id = f"{chrom}-{pos}-{ref}-{alt}"
        
        result = await self._request_with_retry(
            api_name="gnomad",
            endpoint="/",
            method="POST",
            json_body={
                "query": query,
                "variables": {
                    "variantId": variant_id,
                    "datasetId": dataset,
                },
            },
        )
        
        if result["data"] and result["http_status"] == 200:
            data = result["data"]
            variant_data = data.get("data", {}).get("variant", {})
            
            if not variant_data:
                return {
                    "variant_id": variant_id,
                    "af": None,
                    "af_popmax": None,
                    "af_populations": {},
                    "status": "NOT_CAPTURED",
                    "source": "gnomad",
                    "confidence": "medium",
                    "note": "Variant not in gnomAD dataset",
                    "raw": data,
                }
            
            # Combine exome + genome AF
            exome = variant_data.get("exome", {}) or {}
            genome = variant_data.get("genome", {}) or {}
            
            exome_af = exome.get("af")
            genome_af = genome.get("af")
            
            # Use whichever is available, prefer combined
            if exome_af is not None and genome_af is not None:
                combined_af = (exome_af * exome.get("an", 0) + genome_af * genome.get("an", 0)) / \
                              (exome.get("an", 0) + genome.get("an", 1))
            elif exome_af is not None:
                combined_af = exome_af
            elif genome_af is not None:
                combined_af = genome_af
            else:
                combined_af = None
            
            # v0.5 P1-1: Aggregate per-population frequencies across exome + genome
            af_populations = {}
            ex_pops = exome.get("populations", {}) or {}
            gen_pops = genome.get("populations", {}) or {}
            
            all_pops = set(ex_pops.keys()) | set(gen_pops.keys())
            popmax_af = 0.0
            
            for pop in all_pops:
                ex_pop = ex_pops.get(pop, {}) or {}
                gen_pop = gen_pops.get(pop, {}) or {}
                
                ex_ac = ex_pop.get("ac", 0) or 0
                ex_an = ex_pop.get("an", 0) or 0
                ex_hom = ex_pop.get("homozygote_count", 0) or 0
                
                gen_ac = gen_pop.get("ac", 0) or 0
                gen_an = gen_pop.get("an", 0) or 0
                gen_hom = gen_pop.get("homozygote_count", 0) or 0
                
                total_ac = ex_ac + gen_ac
                total_an = ex_an + gen_an
                total_hom = ex_hom + gen_hom
                
                pop_af = total_ac / total_an if total_an > 0 else None
                
                if pop_af is not None:
                    af_populations[pop] = {
                        "af": pop_af,
                        "ac": total_ac,
                        "an": total_an,
                        "homozygote_count": total_hom,
                    }
                    if pop_af > popmax_af:
                        popmax_af = pop_af
            
            return {
                "variant_id": variant_id,
                "af": combined_af,
                "af_popmax": popmax_af if af_populations else None,
                "af_populations": af_populations,
                "af_exome": exome_af,
                "af_genome": genome_af,
                "an_exome": exome.get("an"),
                "an_genome": genome.get("an"),
                "hom_count": (exome.get("homozygote_count") or 0) + (genome.get("homozygote_count") or 0),
                "status": "CAPTURED",
                "source": "cache" if result["from_cache"] else "gnomad",
                "confidence": result["confidence"],
                "raw": data,
            }
        
        return {
            "variant_id": variant_id,
            "af": None,
            "af_popmax": None,
            "af_populations": {},
            "status": "QUERY_FAILED",
            "source": "failed",
            "confidence": "low",
            "error": result.get("error"),
        }
    
    # =====================================================================
    # gnomAD Gene Constraint (v0.5 P1-4: pLI/LOEUF)
    # =====================================================================
    
    async def query_gnomad_gene_constraint(self, gene_symbol: str) -> Dict[str, Any]:
        """
        Query gnomAD gene constraint metrics (pLI, LOEUF, lof_z, mis_z).
        
        Uses GraphQL API. Returns structured constraint data.
        
        Returns:
        {
            "gene": "BRCA1",
            "pLI": 1.0,
            "lof_z": 5.2,
            "mis_z": 3.1,
            "loeuf": 0.12,       # Loss-of-function observed/expected upper bound fraction
            "oe_lof": 0.08,       # Observed/expected LOF
            "source": "gnomad|cache",
            "confidence": "medium",
        }
        """
        query = """
        query GeneConstraint($geneSymbol: String!, $datasetId: DatasetId!) {
            gene(gene_symbol: $geneSymbol, reference_genome: GRCh38) {
                gnomad_constraint {
                    pLI
                    oe_lof
                    oe_lof_upper  # LOEUF
                    oe_lof_lower
                    lof_z
                    mis_z
                }
            }
        }
        """
        
        result = await self._request_with_retry(
            api_name="gnomad",
            endpoint="/",
            method="POST",
            json_body={
                "query": query,
                "variables": {
                    "geneSymbol": gene_symbol,
                    "datasetId": "gnomad_r4",
                },
            },
        )
        
        if result["data"] and result["http_status"] == 200:
            data = result["data"]
            gene_data = data.get("data", {}).get("gene", {})
            constraint = gene_data.get("gnomad_constraint", {}) if gene_data else {}
            
            if not constraint:
                return {
                    "gene": gene_symbol,
                    "pLI": None,
                    "lof_z": None,
                    "mis_z": None,
                    "loeuf": None,
                    "oe_lof": None,
                    "status": "NO_CONSTRAINT_DATA",
                    "source": "gnomad",
                    "confidence": "medium",
                    "note": f"No constraint data for {gene_symbol}",
                }
            
            return {
                "gene": gene_symbol,
                "pLI": constraint.get("pLI"),
                "lof_z": constraint.get("lof_z"),
                "mis_z": constraint.get("mis_z"),
                "loeuf": constraint.get("oe_lof_upper"),
                "oe_lof": constraint.get("oe_lof"),
                "oe_lof_lower": constraint.get("oe_lof_lower"),
                "status": "CAPTURED",
                "source": "cache" if result["from_cache"] else "gnomad",
                "confidence": result["confidence"],
            }
        
        return {
            "gene": gene_symbol,
            "pLI": None,
            "lof_z": None,
            "mis_z": None,
            "loeuf": None,
            "oe_lof": None,
            "status": "QUERY_FAILED",
            "source": "failed",
            "confidence": "low",
            "error": result.get("error"),
        }
    
    # =====================================================================
    # NCBI E-utilities (ClinVar, Gene)
    # =====================================================================
    
    async def query_ncbi_clinvar(self, gene: str, hgvs: Optional[str] = None) -> Dict[str, Any]:
        """
        Query ClinVar via NCBI E-utilities for clinical significance.
        
        Uses esearch to find ClinVar records, then efetch for details.
        
        Returns:
        {
            "gene": "VWF",
            "clinvar_id": "RCV000012345.6",
            "clinical_significance": "Pathogenic",
            "review_status": "practice_guideline",
            "source": "clinvar|cache",
            "confidence": "medium",
        }
        """
        # Step 1: esearch
        search_term = f"{gene}[Gene] AND ClinVar[Title]"
        if hgvs:
            search_term += f" AND {hgvs}"
        
        search_result = await self._request_with_retry(
            api_name="clinvar_eutils",
            endpoint="/esearch.fcgi",
            params={
                "db": "clinvar",
                "term": search_term,
                "retmode": "json",
                "retmax": 5,
            },
        )
        
        if not (search_result["data"] and search_result["http_status"] == 200):
            return {
                "gene": gene,
                "clinvar_id": None,
                "clinical_significance": None,
                "source": "failed",
                "confidence": "low",
                "error": search_result.get("error"),
            }
        
        search_data = search_result["data"]
        idlist = search_data.get("esearchresult", {}).get("idlist", [])
        
        if not idlist:
            return {
                "gene": gene,
                "clinvar_id": None,
                "clinical_significance": None,
                "source": "clinvar",
                "confidence": "medium",
                "note": "No ClinVar records found",
            }
        
        # Step 2: efetch first record
        clinvar_id = idlist[0]
        fetch_result = await self._request_with_retry(
            api_name="clinvar_eutils",
            endpoint="/efetch.fcgi",
            params={
                "db": "clinvar",
                "id": clinvar_id,
                "retmode": "json",
            },
        )
        
        if fetch_result["data"] and fetch_result["http_status"] == 200:
            # Parse ClinVar JSON (structure is complex, Phase 2 will do full parsing)
            # Skeleton: just return the raw data for now
            return {
                "gene": gene,
                "clinvar_id": clinvar_id,
                "clinical_significance": "pending_parsing",  # Phase 2
                "review_status": "pending_parsing",
                "source": "cache" if fetch_result["from_cache"] else "clinvar",
                "confidence": fetch_result["confidence"],
                "raw": fetch_result["data"],
            }
        
        return {
            "gene": gene,
            "clinvar_id": clinvar_id,
            "clinical_significance": None,
            "source": "failed",
            "confidence": "low",
            "error": fetch_result.get("error"),
        }
    
    # =====================================================================
    # HGNC Symbol Normalization (v0.5 P1-2)
    # =====================================================================
    
    async def query_hgnc_symbol(self, symbol: str) -> Dict[str, Any]:
        """
        Query HGNC REST API to validate and normalize a gene symbol.
        
        Uses /search/symbol:{symbol} endpoint. Returns approval status,
        previous/alias symbols, and HGNC ID.
        
        Returns:
        {
            "input": "BRCA1",
            "approved_symbol": "BRCA1",
            "hgnc_id": "HGNC:1100",
            "status": "approved",       # approved | previous | alias | withdrawn | not_found
            "previous_symbols": [],
            "alias_symbols": [],
            "locus_type": "gene with protein product",
            "source": "hgnc|cache",
            "confidence": "medium",
        }
        """
        result = await self._request_with_retry(
            api_name="hgnc",
            endpoint=f"/search/symbol:{symbol}",
            headers={"Accept": "application/json"},
        )
        
        if result["data"] and result["http_status"] == 200:
            data = result["data"]
            docs = data.get("response", {}).get("docs", [])
            
            if not docs:
                return {
                    "input": symbol,
                    "approved_symbol": symbol,
                    "hgnc_id": None,
                    "status": "not_found",
                    "previous_symbols": [],
                    "alias_symbols": [],
                    "locus_type": None,
                    "source": "hgnc",
                    "confidence": "medium",
                }
            
            doc = docs[0]  # Best match
            hgnc_id = doc.get("hgnc_id")
            approved = doc.get("symbol")
            status = doc.get("status", "unknown")
            
            # HGNC returns status as strings like "Approved", "Entry Withdrawn"
            status_norm = status.lower().replace(" ", "_")
            if "approved" in status_norm and "withdrawn" not in status_norm:
                status_code = "approved"
            elif "withdrawn" in status_norm:
                status_code = "withdrawn"
            elif status_norm == "previous":
                status_code = "previous"
            elif status_norm == "alias":
                status_code = "alias"
            else:
                status_code = "unknown"
            
            # If input doesn't match approved symbol, check if it's a previous/alias
            if symbol.upper() != approved.upper():
                # Check previous symbols
                prev_syms = doc.get("prev_symbol", [])
                if symbol.upper() in [s.upper() for s in prev_syms]:
                    status_code = "previous"
                
                # Check alias symbols
                alias_syms = doc.get("alias_symbol", [])
                if symbol.upper() in [s.upper() for s in alias_syms]:
                    status_code = "alias"
            
            return {
                "input": symbol,
                "approved_symbol": approved,
                "hgnc_id": hgnc_id,
                "status": status_code,
                "previous_symbols": doc.get("prev_symbol", []),
                "alias_symbols": doc.get("alias_symbol", []),
                "locus_type": doc.get("locus_type"),
                "source": "cache" if result["from_cache"] else "hgnc",
                "confidence": result["confidence"],
            }
        
        return {
            "input": symbol,
            "approved_symbol": symbol,
            "hgnc_id": None,
            "status": "query_failed",
            "previous_symbols": [],
            "alias_symbols": [],
            "locus_type": None,
            "source": "failed",
            "confidence": "low",
            "error": result.get("error"),
        }
    
    async def batch_normalize_gene_symbols(
        self,
        symbols: List[str],
    ) -> Dict[str, Dict[str, Any]]:
        """
        Batch normalize gene symbols via HGNC API.
        
        Returns dict mapping original symbol -> normalization result.
        Uses batch_query_genes with hgnc query_type internally.
        """
        return await self.batch_query_genes(symbols, query_type="hgnc")
    
    # =====================================================================
    # Batch Query Support
    # =====================================================================
    
    async def batch_query_genes(
        self,
        gene_symbols: List[str],
        query_type: str = "uniprot",
        **kwargs
    ) -> Dict[str, Dict[str, Any]]:
        """
        Execute batch queries with controlled concurrency.
        
        Strategy: semaphore (max 20 concurrent) + chunked batches (30 per batch)
        to avoid overwhelming public APIs while maintaining throughput.
        """
        CHUNK_SIZE = 30
        MAX_CONCURRENT = 20
        semaphore = asyncio.Semaphore(MAX_CONCURRENT)
        
        async def _query_one(gene: str) -> Dict[str, Any]:
            async with semaphore:
                if query_type == "uniprot":
                    return await self.query_uniprot_by_gene(gene)
                elif query_type == "ensembl":
                    return await self.query_ensembl_gene(gene)
                elif query_type == "gtex":
                    tissue = kwargs.get("tissue", "Whole Blood")
                    return await self.query_gtex_expression(gene, tissue)
                elif query_type == "gtex_multi":
                    tissues = kwargs.get("tissues", ["Whole Blood"])
                    return await self.query_gtex_expression_multi(gene, tissues)
                elif query_type == "hgnc":
                    return await self.query_hgnc_symbol(gene)
                elif query_type == "gnomad_constraint":
                    return await self.query_gnomad_gene_constraint(gene)
                else:
                    raise ValueError(f"Unknown query_type: {query_type}")
        
        results = {}
        total = len(gene_symbols)
        
        for i in range(0, total, CHUNK_SIZE):
            chunk = gene_symbols[i:i + CHUNK_SIZE]
            # Create tasks for this chunk
            chunk_tasks = {gene: asyncio.create_task(_query_one(gene)) for gene in chunk}
            # Wait for all in this chunk
            chunk_results = await asyncio.gather(*chunk_tasks.values(), return_exceptions=True)
            # Store results
            for gene, result in zip(chunk_tasks.keys(), chunk_results):
                if isinstance(result, Exception):
                    results[gene] = {
                        "gene": gene,
                        "source": "failed",
                        "confidence": "low",
                        "error": str(result),
                    }
                else:
                    results[gene] = result
            
            # Brief pause between chunks to be polite to APIs
            if i + CHUNK_SIZE < total:
                await asyncio.sleep(0.5)
        
        return results


# =============================================================================
# Standalone convenience functions for non-async contexts
# =============================================================================

def run_async(coro):
    """Run an async coroutine from sync code."""
    return asyncio.run(coro)


async def demo():
    """Demo: query a few genes across multiple APIs."""
    from dgra_config import DGRAGlobalConfig
    
    config = DGRAGlobalConfig.from_env()
    cache = DGRACache(config.cache_db_path, default_ttl_days=config.cache_ttl_days)
    
    async with DGRAAPIClient(config, cache) as client:
        # Test Ensembl
        print("=== Ensembl: MYH11 ===")
        result = await client.query_ensembl_gene("MYH11")
        print(f"  Canonical: {result.get('canonical_transcript')}")
        print(f"  Biotype: {result.get('biotype')}")
        print(f"  Source: {result.get('source')}")
        
        # Test UniProt
        print("\n=== UniProt: MYH11 ===")
        result = await client.query_uniprot_by_gene("MYH11")
        print(f"  ID: {result.get('uniprot_id')}")
        print(f"  Length: {result.get('sequence_length')}")
        print(f"  Domains: {len(result.get('domains', []))}")
        print(f"  GO terms: {len(result.get('go_terms', []))}")
        print(f"  Source: {result.get('source')}")
        
        # Test cache stats
        print("\n=== Cache Stats ===")
        stats = cache.get_stats()
        for api, s in stats.items():
            print(f"  {api}: hits={s['hits']}, misses={s['misses']}, rate={s['hit_rate']:.1%}")


if __name__ == "__main__":
    run_async(demo())
