"""
gpa_phenotype_match.py — Phenotype Association Engine (v0.7)

Core principle: Use external LLM API for semantic matching, NO local synonym library.
"""

import os
import json
import asyncio
from typing import List, Dict, Optional
from pathlib import Path


class PhenotypeMatcher:
    """
    Phenotype association analysis engine.
    Core: Call external LLM API for semantic matching, no local static synonym library.
    """

    def __init__(self, llm_api_key: Optional[str] = None, llm_model: str = "gpt-4o-mini",
                 refs_dir: Optional[Path] = None):
        self.api_key = llm_api_key or os.environ.get("OPENAI_API_KEY")
        self.model = llm_model
        self.gene_phenotype_cache: Dict[str, List[str]] = {}
        self._local_db: Optional[Dict] = None
        # Load local gene-phenotype fact database
        if refs_dir is None:
            refs_dir = Path(__file__).resolve().parent.parent / "references"
        self.refs_dir = refs_dir
        self._load_local_db()

    def _load_local_db(self) -> None:
        db_path = self.refs_dir / "gene_phenotype_map.json"
        if db_path.exists():
            with open(db_path, "r", encoding="utf-8") as f:
                self._local_db = json.load(f)
        else:
            self._local_db = {}

    async def match(self, gene_symbol: str, user_phenotypes: str) -> Dict:
        """
        Input: gene_symbol="CAPN3", user_phenotypes="远端肌无力、肌源性损害、缓慢进展"
        Output: {score, matched_terms, known_phenotypes, explanation, reasoning, confidence, warning}

        Flow:
        1. Query known phenotypes for gene (OMIM/ClinVar/Orphanet, cached, NOT a keyword library)
        2. Call LLM API to judge semantic similarity
        3. Return structured result
        """
        # Step 1: Get known phenotypes
        known_phenotypes = await self._get_known_phenotypes(gene_symbol)

        # Step 2: Call LLM for semantic match
        if self.api_key:
            result = await self._llm_semantic_match(gene_symbol, user_phenotypes, known_phenotypes)
        else:
            result = self._fallback_keyword_match(user_phenotypes, known_phenotypes)
            result["warning"] = (
                "LLM API key not configured, using fallback keyword match. "
                "Set OPENAI_API_KEY for better accuracy."
            )

        result["gene"] = gene_symbol
        result["user_phenotypes"] = user_phenotypes
        result["known_phenotypes"] = known_phenotypes
        return result

    async def match_batch(self, gene_symbols: List[str], user_phenotypes: str) -> List[Dict]:
        """Batch match multiple genes concurrently."""
        tasks = [self.match(g, user_phenotypes) for g in gene_symbols]
        return await asyncio.gather(*tasks)

    async def _get_known_phenotypes(self, gene_symbol: str) -> List[str]:
        """
        Query known phenotypes for a gene.
        Data source priority:
        1. Local cache (gene_phenotype_cache)
        2. Built-in top gene-phenotype fact table (references/gene_phenotype_map.json)
        """
        if gene_symbol in self.gene_phenotype_cache:
            return self.gene_phenotype_cache[gene_symbol]

        phenotypes: List[str] = []

        # From built-in local database (fact data, NOT synonym library)
        if self._local_db and gene_symbol in self._local_db:
            entries = self._local_db[gene_symbol].get("phenotypes", [])
            phenotypes.extend(e.get("name", "") for e in entries if e.get("name"))

        # Deduplicate and cache
        unique = list(set(p for p in phenotypes if p))
        self.gene_phenotype_cache[gene_symbol] = unique
        return unique

    async def _llm_semantic_match(self, gene: str, user_phenotypes: str, known_phenotypes: List[str]) -> Dict:
        """
        Call LLM API for semantic similarity judgment.
        Returns: {score, matched_pairs, explanation, confidence, reasoning}
        """
        if not known_phenotypes:
            return {
                "score": 0.0,
                "matched_pairs": [],
                "explanation": "No known phenotypes found for this gene.",
                "confidence": "low",
                "reasoning": "Gene not in phenotype database.",
            }

        prompt = self._build_match_prompt(gene, user_phenotypes, known_phenotypes)

        try:
            import aiohttp
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    "https://api.openai.com/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json",
                    },
                    json={
                        "model": self.model,
                        "messages": [{"role": "user", "content": prompt}],
                        "temperature": 0.1,
                        "response_format": {"type": "json_object"},
                    },
                    timeout=aiohttp.ClientTimeout(total=30),
                ) as resp:
                    if resp.status != 200:
                        text = await resp.text()
                        return {
                            "score": 0.0,
                            "matched_pairs": [],
                            "explanation": f"LLM API error (HTTP {resp.status}): {text[:200]}",
                            "confidence": "low",
                            "reasoning": "API request failed.",
                        }
                    data = await resp.json()
                    content = data["choices"][0]["message"]["content"]
                    parsed = json.loads(content)
                    return {
                        "score": float(parsed.get("score", 0.0)),
                        "matched_pairs": parsed.get("matched_pairs", []),
                        "explanation": parsed.get("explanation", ""),
                        "confidence": parsed.get("confidence", "low"),
                        "reasoning": parsed.get("reasoning", ""),
                    }
        except Exception as e:
            return {
                "score": 0.0,
                "matched_pairs": [],
                "explanation": f"LLM API exception: {str(e)[:200]}",
                "confidence": "low",
                "reasoning": "API call failed, falling back.",
            }

    def _build_match_prompt(self, gene: str, user_phenotypes: str, known_phenotypes: List[str]) -> str:
        known_str = json.dumps(known_phenotypes, ensure_ascii=False, indent=2)
        return (
            f"You are a medical genetics expert. Evaluate the semantic association between "
            f"the known disease phenotypes of gene {gene} and the user's clinical phenotypes.\n\n"
            f"Gene: {gene}\n"
            f"Known phenotypes: {known_str}\n"
            f"User phenotypes: {user_phenotypes}\n\n"
            f"Please answer:\n"
            f'1. Semantic association score (0-1): ___\n'
            f'2. Matched phenotype pairs: ___\n'
            f'3. Brief explanation: ___\n'
            f'4. Confidence (high/medium/low): ___\n'
            f'5. Reasoning: ___\n\n'
            f'Output as JSON: '
            f'{{"score": float, "matched_pairs": [["user_term", "known_phenotype"], ...], '
            f'"explanation": str, "confidence": str, "reasoning": str}}'
        )

    def _fallback_keyword_match(self, user_phenotypes: str, known_phenotypes: List[str]) -> Dict:
        """
        Fallback when no LLM API key.
        NOT a synonym library — simple keyword overlap (Chinese/English).
        This is a degraded scheme, accuracy far below LLM.
        """
        if not known_phenotypes:
            return {
                "score": 0.0,
                "matched_pairs": [],
                "explanation": "No known phenotypes found for this gene.",
                "confidence": "low",
                "reasoning": "Gene not in phenotype database.",
            }

        # Split user phenotypes by common delimiters
        raw = user_phenotypes.replace("。", "、").replace(",", "、").replace(";", "、").replace(" ", "、")
        user_terms = [t.strip() for t in raw.split("。") if t.strip()]

        matches = []
        max_score = 0.0
        best_explanation = "No keyword overlap"

        for known in known_phenotypes:
            overlap = []
            for term in user_terms:
                if term.lower() in known.lower() or known.lower() in term.lower():
                    overlap.append([term, known])
            score = len(overlap) / max(len(user_terms), 1)
            if score > max_score:
                max_score = score
                matches = overlap
                if overlap:
                    best_explanation = f"Fallback keyword overlap: {len(overlap)} terms matched"

        return {
            "score": min(max_score, 1.0),
            "matched_pairs": matches,
            "explanation": best_explanation,
            "confidence": "low",
            "reasoning": "No LLM API key. Using degraded keyword overlap fallback.",
        }
