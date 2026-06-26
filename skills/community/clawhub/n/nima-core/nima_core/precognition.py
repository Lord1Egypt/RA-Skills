"""
NIMA Precognition — Proposal #4: Precognitive Memory Injection
==============================================================
Mine temporal patterns from memory, generate predictions via LLM,
and inject the most relevant precognitions into agent prompts.

Usage:
    from nima_core.precognition import NimaPrecognition

    pc = NimaPrecognition(
        db_path="~/.nima/memory/ladybug.lbug",
        llm_base_url="https://api.openai.com/v1",
        llm_api_key="sk-...",
        llm_model="gpt-4o-mini",
    )

    # Mine patterns and generate predictions (run daily/weekly)
    pc.run_mining_cycle()

    # Inject relevant precognitions into a task prompt
    enriched_prompt = pc.inject("Write a research summary on neural oscillations")
    print(enriched_prompt)
"""

import os

from nima_core.llm_config import resolve_llm_config
import json
import logging
import sqlite3
import struct
from collections import defaultdict
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, List, Dict, Optional

logger = logging.getLogger(__name__)

try:
    import real_ladybug as lb
    HAS_LADYBUG = True
except ImportError:
    HAS_LADYBUG = False


class NimaPrecognition:
    """
    Mine temporal patterns from LadybugDB and generate predictions.
    Predictions are stored locally and can be injected into agent prompts.
    """

    DEFAULT_PRECOG_DB = "~/.nima/memory/precognitions.sqlite"
    DEFAULT_DB = "~/.nima/memory/ladybug.lbug"

    def __init__(
        self,
        db_path: Optional[str] = None,
        precog_db_path: Optional[str] = None,
        llm_base_url: Optional[str] = None,
        llm_api_key: Optional[str] = None,
        llm_model: Optional[str] = None,
        voyage_api_key: Optional[str] = None,
        lookback_days: int = 30,
        min_memory_count: int = 25,
        min_pattern_count: int = 2,
        min_pattern_frequency: int = 3,
        min_pattern_confidence: float = 0.35,
        min_prediction_confidence: float = 0.6,
        min_predictions_to_store: int = 1,
    ):
        """
        Args:
            db_path:         Path to LadybugDB (.lbug file). If None, auto-discovers
                             from $NIMA_HOME/memory/ladybug.lbug. Precognition disabled if auto-discovery fails.
            precog_db_path:  Path to SQLite DB for storing predictions.
                             Defaults to ~/.nima/memory/precognitions.sqlite
            llm_base_url:    LLM endpoint override. Defaults to resolved NIMA_LLM_BASE_URL.
            llm_api_key:     API key override. Defaults to resolved NIMA_LLM_API_KEY.
            llm_model:       Model override. Defaults to resolved NIMA_LLM_MODEL.
            voyage_api_key:  Optional Voyage API key for embedding precognitions.
                             Falls back to VOYAGE_API_KEY env var.
            lookback_days:   How many days of history to mine for patterns.
        """
        # Auto-discover LadybugDB from NIMA_HOME if not provided
        if db_path is None:
            nima_home = Path(os.environ.get("NIMA_HOME", "~/.nima")).expanduser()
            candidate = nima_home / Path(self.DEFAULT_DB).expanduser().name
            db_path = str(candidate) if candidate.exists() else None
        self.db_path = str(Path(db_path).expanduser()) if db_path else None
        self.precog_db_path = Path(
            precog_db_path or self.DEFAULT_PRECOG_DB
        ).expanduser()
        llm_config = resolve_llm_config(api_key=llm_api_key, model=llm_model, base_url=llm_base_url)
        self.llm_base_url = llm_config.base_url
        self.llm_api_key = llm_config.api_key
        self.llm_model = llm_config.model
        self.voyage_api_key = voyage_api_key or os.environ.get("VOYAGE_API_KEY", "")
        self.lookback_days = lookback_days
        self.min_memory_count = max(1, int(min_memory_count))
        self.min_pattern_count = max(1, int(min_pattern_count))
        self.min_pattern_frequency = max(1, int(min_pattern_frequency))
        self.min_pattern_confidence = float(min_pattern_confidence)
        self.min_prediction_confidence = float(min_prediction_confidence)
        self.min_predictions_to_store = max(1, int(min_predictions_to_store))
        self._conn: Optional[sqlite3.Connection] = None

    def close(self) -> None:
        """Close the SQLite connection and release resources."""
        if self._conn is not None:
            try:
                self._conn.close()
            except (OSError, IOError, sqlite3.Error) as e:
                logger.warning(f"Failed to close NimaPrecognition connection: {e}")
            finally:
                self._conn = None

    def __del__(self) -> None:
        """Ensure connection is closed on garbage collection."""
        self.close()

    def __enter__(self) -> "NimaPrecognition":
        """Return self to support use as a context manager."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Close the connection when exiting a ``with`` block."""
        self.close()

    # ── SQLite (precognitions store) ──────────────────────────────────────────

    def _get_conn(self) -> sqlite3.Connection:
        """Return a lazily-initialised SQLite connection, creating the DB schema on first use."""
        if self._conn is None:
            self.precog_db_path.parent.mkdir(parents=True, exist_ok=True)
            self._conn = sqlite3.connect(str(self.precog_db_path))
            self._conn.execute("""
                CREATE TABLE IF NOT EXISTS precognitions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    what TEXT NOT NULL,
                    who TEXT,
                    when_predicted TEXT,
                    confidence REAL DEFAULT 0.5,
                    predicted_affect TEXT,
                    source_pattern TEXT,
                    pattern_hash TEXT,
                    status TEXT DEFAULT 'pending',
                    matched_memory_id INTEGER,
                    similarity_score REAL,
                    generated_at TEXT,
                    expires_at TEXT,
                    embedding BLOB
                )
            """)
            self._conn.commit()
        return self._conn

    # ── Pattern Mining ────────────────────────────────────────────────────────

    def mine_patterns(self) -> List[Dict]:
        """Mine recurring temporal patterns from LadybugDB."""
        if not HAS_LADYBUG or not self.db_path:
            logger.warning("LadybugDB not available — pattern mining skipped")
            return []
        if not Path(self.db_path).exists():
            logger.error(f"DB not found: {self.db_path}")
            return []

        db = lb.Database(self.db_path)
        conn = lb.Connection(db)
        try:
            conn.execute("LOAD VECTOR")
        except Exception:
            pass  # LOAD VECTOR may not be available in all versions
        cutoff_ms = int(
            (datetime.now() - timedelta(days=self.lookback_days)).timestamp() * 1000
        )

        query = f"""
        MATCH (n:MemoryNode)
        WHERE n.is_ghost = false AND n.timestamp >= {cutoff_ms}
        RETURN n.timestamp, n.who, n.text, n.summary, n.themes
        """
        try:
            rows = list(conn.execute(query))
        except Exception as e:
            logger.error(f"Pattern mining query failed: {e}")
            return []

        time_buckets: Dict[str, List] = defaultdict(list)
        for row in rows:
            ts_ms, who, text, summary, themes = row
            try:
                dt = datetime.fromtimestamp(float(ts_ms) / 1000)
                bucket = f"{dt.strftime('%A')}_{dt.hour:02d}"
                time_buckets[bucket].append(
                    {"who": who, "text": text, "summary": summary, "themes": themes}
                )
            except Exception:
                continue

        patterns = []
        for bucket, mems in time_buckets.items():
            if len(mems) < 3:
                continue

            who_counts: Dict[str, int] = defaultdict(int)
            theme_counts: Dict[str, int] = defaultdict(int)
            for m in mems:
                if m["who"] and m["who"] not in ("self", "unknown", ""):
                    who_counts[m["who"]] += 1
                if m.get("themes"):
                    try:
                        tl = (
                            json.loads(m["themes"])
                            if isinstance(m["themes"], str)
                            else m["themes"]
                        )
                        if isinstance(tl, list):
                            for t in tl:
                                theme_counts[t] += 1
                    except Exception:
                        pass

            top_who = sorted(who_counts.items(), key=lambda x: x[1], reverse=True)[:2]
            top_themes = sorted(theme_counts.items(), key=lambda x: x[1], reverse=True)[:5]
            if top_who or top_themes:
                patterns.append(
                    {
                        "bucket": bucket,
                        "frequency": len(mems),
                        "common_who": [w[0] for w in top_who],
                        "common_themes": [t[0] for t in top_themes],
                        "sample_memories": [
                            (m["summary"] or m["text"] or "")[:100] for m in mems[:3]
                        ],
                        "confidence": min(len(mems) / 10, 1.0),
                    }
                )

        logger.info(f"Mined {len(patterns)} patterns from {len(time_buckets)} time buckets")
        return patterns

    # ── LLM Prediction Generation ─────────────────────────────────────────────

    def assess_readiness(self) -> Dict[str, Any]:
        """Assess whether there is enough history to mine useful precognitions."""
        report: Dict[str, Any] = {
            "ready": False,
            "reason": "unknown",
            "memory_count": 0,
            "lookback_days": self.lookback_days,
        }
        if not HAS_LADYBUG or not self.db_path:
            report["reason"] = "memory database unavailable"
            return report
        if not Path(self.db_path).exists():
            report["reason"] = f"memory database missing: {self.db_path}"
            return report

        db = lb.Database(self.db_path)
        conn = lb.Connection(db)
        try:
            conn.execute("LOAD VECTOR")
        except Exception:
            pass

        cutoff_ms = int((datetime.now() - timedelta(days=self.lookback_days)).timestamp() * 1000)
        query = f"""
        MATCH (n:MemoryNode)
        WHERE n.is_ghost = false AND n.timestamp >= {cutoff_ms}
        RETURN COUNT(n)
        """
        try:
            row = conn.execute(query).fetchone()
            memory_count = int((row[0] if row else 0) or 0)
        except Exception as e:
            logger.error(f"Precognition readiness query failed: {e}")
            report["reason"] = "readiness query failed"
            return report

        report["memory_count"] = memory_count
        if memory_count < self.min_memory_count:
            report["reason"] = f"insufficient recent memory history ({memory_count}/{self.min_memory_count})"
            return report

        report["ready"] = True
        report["reason"] = "ok"
        return report

    def filter_useful_patterns(self, patterns: List[Dict]) -> List[Dict]:
        """Keep only patterns that meet conservative usefulness thresholds."""
        useful = []
        for pattern in patterns:
            confidence = float(pattern.get("confidence", 0.0) or 0.0)
            frequency = int(pattern.get("frequency", 0) or 0)
            if confidence < self.min_pattern_confidence:
                continue
            if frequency < self.min_pattern_frequency:
                continue
            useful.append(pattern)
        return useful

    def filter_useful_precognitions(self, precognitions: List[Dict]) -> List[Dict]:
        """Drop low-confidence or empty predictions before storage."""
        useful = []
        for p in precognitions:
            what = str(p.get("what", "") or "").strip()
            confidence = float(p.get("confidence", 0.0) or 0.0)
            if not what:
                continue
            if confidence < self.min_prediction_confidence:
                continue
            useful.append({**p, "what": what, "confidence": confidence})
        return useful

    def generate_precognitions(self, patterns: List[Dict]) -> List[Dict]:
        """Call LLM to generate predictions from mined patterns."""
        if not patterns:
            return []

        top = sorted(patterns, key=lambda x: x["frequency"], reverse=True)[:10]
        prompt = (
            "Based on these recurring patterns, generate specific predictions for the "
            "next 7 days.\n\nPatterns:\n"
            + json.dumps(top, indent=2)
            + "\n\nReturn ONLY a JSON array. Each item must have:\n"
            "  what (str), who (str|null), when_predicted (ISO timestamp),\n"
            "  confidence (0-1 float), predicted_affect (dict of Panksepp affects),\n"
            "  source_pattern (str describing the pattern).\n"
            "Only predict neutral or positive events. Timestamps within 7 days."
        )

        try:
            from nima_core.llm_client import llm_complete
            content = llm_complete(prompt, max_tokens=1000, timeout=60)
            if not content:
                logger.error("LLM unavailable or misconfigured — cannot generate precognitions")
                return []
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0].strip()
            elif "```" in content:
                content = content.split("```")[1].split("```")[0].strip()
            result = json.loads(content)
            if isinstance(result, dict):
                for key in ("predictions", "precognitions", "results"):
                    if key in result:
                        result = result[key]
                        break
            return result if isinstance(result, list) else []
        except ImportError:
            logger.error("llm_client not available")
            return []
        except Exception as e:
            logger.error(f"LLM precognition generation failed: {e}")
            return []

    # ── Storage ───────────────────────────────────────────────────────────────

    def _voyage_embedding(self, text: str) -> Optional[bytes]:
        """Optional Voyage embedding for semantic matching."""
        import urllib.request

        if not self.voyage_api_key:
            return None
        try:
            payload = json.dumps(
                {"input": [text], "model": "voyage-3-lite"}
            ).encode()
            req = urllib.request.Request(
                "https://api.voyageai.com/v1/embeddings",
                data=payload,
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {self.voyage_api_key}",
                },
            )
            with urllib.request.urlopen(req, timeout=8) as r:
                emb = json.loads(r.read())["data"][0]["embedding"]
                return struct.pack(f"{len(emb)}f", *emb)
        except Exception as e:
            logger.warning(f"Voyage embedding failed: {e}")
            return None

    def store_precognitions(self, precognitions: List[Dict]) -> int:
        """Store predictions in SQLite, deduplicating by hash."""
        import hashlib

        conn = self._get_conn()
        stored = 0
        now = datetime.now().isoformat()
        expires = (datetime.now() + timedelta(days=7)).isoformat()

        for p in precognitions:
            what = str(p.get("what", ""))
            if not what:
                continue

            h = hashlib.sha256(what.encode()).hexdigest()[:16]
            exists = conn.execute(
                "SELECT id FROM precognitions WHERE pattern_hash = ?", (h,)
            ).fetchone()
            if exists:
                continue

            emb = self._voyage_embedding(what)
            conn.execute(
                """INSERT INTO precognitions
                   (what, who, when_predicted, confidence, predicted_affect,
                    source_pattern, pattern_hash, generated_at, expires_at, embedding)
                   VALUES (?,?,?,?,?,?,?,?,?,?)""",
                (
                    what,
                    p.get("who"),
                    p.get("when_predicted"),
                    float(p.get("confidence", 0.5)),
                    json.dumps(p.get("predicted_affect", {})),
                    p.get("source_pattern", ""),
                    h,
                    now,
                    expires,
                    emb,
                ),
            )
            stored += 1

        conn.commit()
        logger.info(f"Stored {stored} new precognitions")
        return stored

    # ── Injection ─────────────────────────────────────────────────────────────

    def get_relevant(self, task: str, top_k: int = 3) -> List[Dict]:
        """Retrieve precognitions most relevant to the given task string."""
        conn = self._get_conn()
        now = datetime.now().isoformat()
        rows = conn.execute(
            """SELECT id, what, who, confidence, predicted_affect, source_pattern
               FROM precognitions
               WHERE status = 'pending' AND (expires_at IS NULL OR expires_at > ?)
               ORDER BY confidence DESC LIMIT 20""",
            (now,),
        ).fetchall()

        if not rows:
            return []

        task_words = set(task.lower().split())
        scored = []
        for row in rows:
            rid, what, who, conf, affect, pattern = row
            what_words = set(what.lower().split())
            overlap = len(task_words & what_words) / max(len(task_words), 1)
            score = 0.5 * conf + 0.5 * overlap
            scored.append((score, {"id": rid, "what": what, "who": who, "confidence": conf}))

        scored.sort(key=lambda x: x[0], reverse=True)
        return [item for _, item in scored[:top_k]]

    def inject(self, task: str, top_k: int = 3) -> str:
        """
        Inject relevant precognitions into a task prompt.
        Returns the original task if no precognitions available.
        """
        relevant = self.get_relevant(task, top_k=top_k)
        if not relevant:
            return task

        lines = ["## PRECOGNITIVE CONTEXT", "Patterns suggest these may be relevant:"]
        for p in relevant:
            conf_pct = int(p["confidence"] * 100)
            line = f"• {p['what']} (confidence: {conf_pct}%)"
            if p.get("who"):
                line += f" — likely involves {p['who']}"
            lines.append(line)
        lines.append("")

        return "\n".join(lines) + task

    # ── Full Cycle ────────────────────────────────────────────────────────────

    def run_mining_cycle(self) -> Dict[str, int]:
        """
        Full pipeline: mine patterns → generate predictions → store.
        Returns dict with counts.
        """
        readiness = self.assess_readiness()
        if not readiness.get("ready"):
            return {
                "status": "no_signal",
                "reason": readiness.get("reason", "not ready"),
                "memory_count": readiness.get("memory_count", 0),
                "patterns": 0,
                "useful_patterns": 0,
                "generated": 0,
                "useful_predictions": 0,
                "stored": 0,
            }

        patterns = self.mine_patterns()
        useful_patterns = self.filter_useful_patterns(patterns)
        if len(useful_patterns) < self.min_pattern_count:
            return {
                "status": "no_signal",
                "reason": f"not enough recurring patterns ({len(useful_patterns)}/{self.min_pattern_count})",
                "memory_count": readiness.get("memory_count", 0),
                "patterns": len(patterns),
                "useful_patterns": len(useful_patterns),
                "generated": 0,
                "useful_predictions": 0,
                "stored": 0,
            }

        precogs = self.generate_precognitions(useful_patterns)
        useful_precogs = self.filter_useful_precognitions(precogs)
        if len(useful_precogs) < self.min_predictions_to_store:
            return {
                "status": "no_signal",
                "reason": (
                    f"no actionable precognitions above confidence threshold "
                    f"({len(useful_precogs)}/{self.min_predictions_to_store})"
                ),
                "memory_count": readiness.get("memory_count", 0),
                "patterns": len(patterns),
                "useful_patterns": len(useful_patterns),
                "generated": len(precogs),
                "useful_predictions": len(useful_precogs),
                "stored": 0,
            }

        stored = self.store_precognitions(useful_precogs)
        return {
            "status": "ok",
            "reason": "ok",
            "memory_count": readiness.get("memory_count", 0),
            "patterns": len(patterns),
            "useful_patterns": len(useful_patterns),
            "generated": len(precogs),
            "useful_predictions": len(useful_precogs),
            "stored": stored,
        }

    def cleanup_expired(self) -> int:
        """Mark expired predictions as expired."""
        conn = self._get_conn()
        now = datetime.now().isoformat()
        c = conn.execute(
            "UPDATE precognitions SET status = 'expired' WHERE expires_at < ? AND status = 'pending'",
            (now,),
        )
        conn.commit()
        return c.rowcount


__all__ = ["NimaPrecognition"]


# ── CLI ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import sys

    cmd = sys.argv[1] if len(sys.argv) > 1 else "mine"

    pc = NimaPrecognition()

    if cmd == "mine":
        result = pc.run_mining_cycle()
        if result.get("status") == "ok":
            print(f"Mining complete: {result['useful_patterns']} useful patterns → "
                  f"{result['useful_predictions']} useful predictions, "
                  f"{result['stored']} stored.")
            print(json.dumps(result))
    elif cmd == "status":
        readiness = pc.assess_readiness()
        conn = pc._get_conn()
        total = conn.execute("SELECT COUNT(*) FROM precognitions").fetchone()[0]
        active = conn.execute(
            "SELECT COUNT(*) FROM precognitions WHERE status IN ('active','pending')"
        ).fetchone()[0]
        print(
            f"Precognitions: {total} total, {active} active/pending | "
            f"readiness: {readiness.get('reason')} | "
            f"recent memories: {readiness.get('memory_count', 0)}"
        )
        rows = conn.execute(
            "SELECT what, confidence, status FROM precognitions ORDER BY rowid DESC LIMIT 5"
        ).fetchall()
        for r in rows:
            print(f"  [{r[2]}] {r[0][:70]} ({r[1]:.0%})")
    elif cmd == "cleanup":
        n = pc.cleanup_expired()
        print(f"Expired {n} precognitions.")
    else:
        print("Usage: python3 -m nima_core.precognition [mine|status|cleanup]")
        sys.exit(1)
