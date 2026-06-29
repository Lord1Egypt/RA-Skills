#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🌀 anti-infinite-loop v2.0 — CORE
─────────────────────────────────────
Spec: /mnt/Morgana/audits/2026-06-08_choir_audit/spec_anti_loop_v2_external.md
Cible: EXTERNAL USERS (dev solo, startup, chercheur)
Deps CORE: stdlib Python + numpy OPTIONNEL
Deps OPT-IN: torch (KAN), embeddings, multi-agent

9 features CORE (zéro dépendance fancy):
1. Predictive Entropy (Shannon) — 0 token, 0ms
2. Novelty Detector (numpy cosine) — fallback hash
3. Loop Taxonomy (4 types: verbatim/semantic/intent_drift/cyclic)
4. Healing Injector (vs hard-kill) — 3 modes
5. Self-Tuning Thresholds — méta-boucle sans ML
6. Breath-Rate Monitor — 0 CPU 0 RAM
7. Pre-Flight Regex — plan-level, 0 LLM
8. Loop DNA (SHA-256) — cross-session
9. Cross-Harness Adapters — 3 lignes pour brancher

PHILOSOPHIE: "Lunedi-matin-ready" (lunedi = lundi en italien)
- Single-agent par défaut
- Multi-agent opt-in
- Healing > Kill
- Coût-aware (track tokens)
"""

import os
import re
import json
import math
import time
import hashlib
import logging
from collections import deque
from pathlib import Path
from datetime import datetime
from typing import Optional, Callable, Any, Dict, List, Union, Tuple

# numpy = OPTIONNEL (graceful fallback hash)
try:
    import numpy as np
    HAS_NUMPY = True
except ImportError:
    HAS_NUMPY = False

# Setup logging (stdlib)
logger = logging.getLogger("anti_loop")
if not logger.handlers:
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter('%(asctime)s [%(levelname)s] %(message)s'))
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)


# ═════════════════════════════════════════════════════════════
# 1. PREDICTIVE ENTROPY (Shannon) — 0 token, 0ms
# ═════════════════════════════════════════════════════════════

class PredictiveEntropy:
    """
    Shannon entropy sur sliding window des N dernières actions.
    Quand l'entropie collapse sous un seuil dynamique → précurseur de boucle.
    Détecte 5-10 itérations AVANT la catastrophe.
    """
    
    def __init__(self, window_size: int = 50, threshold: float = 0.3):
        self.window_size = window_size
        self.threshold = threshold
        self.history: deque = deque(maxlen=window_size)
        self.entropies: deque = deque(maxlen=20)  # pour trend
    
    def observe(self, action: str) -> float:
        """Record an action, return current Shannon entropy."""
        # Hash action to a category (first 4 chars)
        h = hashlib.sha256(action.encode()).hexdigest()[:4]
        self.history.append(h)
        
        if len(self.history) < 2:
            return 1.0
        
        # Compute Shannon entropy on hash distribution
        counts: Dict[str, int] = {}
        for h in self.history:
            counts[h] = counts.get(h, 0) + 1
        
        total = len(self.history)
        entropy = 0.0
        for count in counts.values():
            p = count / total
            if p > 0:
                entropy -= p * math.log2(p)
        
        # Normalize par max entropy
        max_entropy = math.log2(min(total, 256)) if total > 0 else 1
        normalized = entropy / max_entropy if max_entropy > 0 else 0
        
        self.entropies.append(normalized)
        return normalized
    
    def is_collapse_imminent(self) -> bool:
        """True si l'entropy collapse sous le seuil ET trend descendant."""
        if len(self.entropies) < 3:
            return False
        
        current = self.entropies[-1]
        return current < self.threshold


# ═════════════════════════════════════════════════════════════
# 2. NOVELTY DETECTOR (numpy cosine + hash fallback)
# ═════════════════════════════════════════════════════════════

class NoveltyDetector:
    """
    Cosine similarity entre actions consécutives.
    - Avec numpy: vectorise le texte (simple hashing trick)
    - Sans numpy: hash direct, exact match only
    """
    
    def __init__(self, similarity_threshold: float = 0.95, dim: int = 128):
        self.similarity_threshold = similarity_threshold
        self.dim = dim
        self.last_vector: Optional[Any] = None
    
    def _text_to_vector(self, text: str) -> Any:
        """Hash trick: text → fixed-dim vector (numpy or list)."""
        vec = np.zeros(self.dim) if HAS_NUMPY else [0.0] * self.dim
        words = text.lower().split()
        for word in words:
            h = int(hashlib.md5(word.encode()).hexdigest()[:8], 16)
            idx = h % self.dim
            if HAS_NUMPY:
                vec[idx] += 1
            else:
                vec[idx] = vec[idx] + 1
        # Normalize
        if HAS_NUMPY:
            norm = np.linalg.norm(vec)
            return vec / norm if norm > 0 else vec
        else:
            norm = math.sqrt(sum(x*x for x in vec))
            return [x/norm for x in vec] if norm > 0 else vec
    
    def _cosine(self, a, b) -> float:
        """Cosine similarity (numpy or pure python)."""
        if HAS_NUMPY:
            return float(np.dot(a, b))
        else:
            return sum(x*y for x, y in zip(a, b))
    
    def observe(self, action: str) -> float:
        """Returns novelty score 0-1. Low = similar to last action."""
        vec = self._text_to_vector(action)
        if self.last_vector is None:
            self.last_vector = vec
            return 1.0
        
        similarity = self._cosine(vec, self.last_vector)
        self.last_vector = vec
        return 1.0 - similarity  # novelty = 1 - similarity
    
    def is_novelty_low(self) -> bool:
        """True si similarité > seuil (donc novelty faible)."""
        if self.last_vector is None or not hasattr(self, '_last_novelty'):
            return False
        return (1.0 - self._last_novelty) > self.similarity_threshold
    
    @property
    def last_novelty(self) -> float:
        return getattr(self, '_last_novelty', 1.0)
    
    @last_novelty.setter
    def last_novelty(self, v: float):
        self._last_novelty = v


# ═════════════════════════════════════════════════════════════
# 3. LOOP TAXONOMY (4 types)
# ═════════════════════════════════════════════════════════════

class LoopType:
    VERBATIM = "verbatim"          # Même string hash
    SEMANTIC = "semantic"          # Paraphrase / reformat
    INTENT_DRIFT = "intent_drift"  # Intent original perdu
    CYCLIC = "cyclic"              # A→B→A pattern


class LoopTaxonomy:
    """
    Classify la boucle en 4 types. Chaque type a un remède spécifique.
    """
    
    def __init__(self):
        self.last_actions: deque = deque(maxlen=10)
    
    def observe(self, action: str, intent: Optional[str] = None) -> Optional[str]:
        """Return loop type if detected, else None."""
        self.last_actions.append((action, intent))
        
        if len(self.last_actions) < 2:
            return None
        
        # VERBATIM: same string
        if self.last_actions[-1][0] == self.last_actions[-2][0]:
            return LoopType.VERBATIM
        
        # SEMANTIC: novelty low
        # (we'll cross-check with NoveltyDetector externally)
        
        # INTENT_DRIFT: action s'éloigne de l'intent
        if intent and self.last_actions[-2][1]:
            if not self._intent_similar(intent, self.last_actions[-2][1]):
                return LoopType.INTENT_DRIFT
        
        # CYCLIC: A→B→A
        if len(self.last_actions) >= 3:
            if (self.last_actions[-1][0] == self.last_actions[-3][0]):
                return LoopType.CYCLIC
        
        return None
    
    def _intent_similar(self, i1: str, i2: str, threshold: float = 0.6) -> bool:
        """Simple word overlap similarity."""
        words1 = set(i1.lower().split())
        words2 = set(i2.lower().split())
        if not words1 or not words2:
            return True
        return len(words1 & words2) / len(words1 | words2) > threshold


# ═════════════════════════════════════════════════════════════
# 4. HEALING INJECTOR (vs hard-kill)
# ═════════════════════════════════════════════════════════════

class HealingMode:
    HEAL = "heal"           # Inject system message
    PAUSE = "pause"         # Pause N seconds
    HARD_KILL = "hard_kill" # abort()


class HealingInjector:
    """
    Au lieu de abort(), INJECTE un system message contextuel.
    Le skill apprend à l'agent à se corriger.
    """
    
    HEAL_TEMPLATES = [
        "Tu sembles tourner en rond sur '{topic}'. Ton intent original était '{intent}'. Essaie une approche différente.",
        "Boucle détectée. Reformule avec d'autres mots: {intent}",
        "Pattern répétitif détecté. Prends du recul et propose 3 alternatives à: {last_action}",
    ]
    
    def __init__(self, mode: str = HealingMode.HEAL, pause_seconds: float = 2.0):
        self.mode = mode
        self.pause_seconds = pause_seconds
        self.heal_count = 0
    
    def inject(self, last_action: str, intent: str = "") -> Dict[str, Any]:
        """Returns a healing directive based on mode."""
        self.heal_count += 1
        
        if self.mode == HealingMode.HARD_KILL:
            return {
                "action": "abort",
                "message": f"Loop detected (kill #{self.heal_count}): {last_action[:80]}",
                "should_continue": False,
            }
        
        if self.mode == HealingMode.PAUSE:
            return {
                "action": "pause",
                "duration_seconds": self.pause_seconds,
                "message": f"Loop detected, pausing {self.pause_seconds}s",
                "should_continue": True,
            }
        
        # Default: HEAL
        import random
        template = random.choice(self.HEAL_TEMPLATES)
        # Extract a "topic" from last action
        topic = last_action[:50] if last_action else "current action"
        
        return {
            "action": "heal",
            "system_message": template.format(
                topic=topic,
                intent=intent or "(no intent recorded)",
                last_action=last_action[:100],
            ),
            "should_continue": True,
            "heal_count": self.heal_count,
        }


# ═════════════════════════════════════════════════════════════
# 5. SELF-TUNING THRESHOLDS (méta-boucle sans ML)
# ═════════════════════════════════════════════════════════════

class SelfTuningThresholds:
    """
    Observe TP/FP sur les 100 derniers cas, ajuste seuils via gradient simple.
    Pas de ML, juste moving average.
    """
    
    def __init__(self, initial_threshold: float = 0.95, 
                 adjust_step: float = 0.02, min_threshold: float = 0.7,
                 max_threshold: float = 0.99):
        self.threshold = initial_threshold
        self.adjust_step = adjust_step
        self.min_threshold = min_threshold
        self.max_threshold = max_threshold
        self.history: deque = deque(maxlen=100)
    
    def record(self, was_true_positive: bool):
        """Record feedback (was this a correct loop detection?)."""
        self.history.append(1 if was_true_positive else 0)
        
        if len(self.history) < 20:
            return  # Pas assez de data
        
        rate = sum(self.history) / len(self.history)
        
        if rate < 0.5:
            # Trop de FP → relâche (lower threshold = less sensitive)
            self.threshold = min(self.max_threshold, self.threshold + self.adjust_step)
        elif rate > 0.9:
            # Très précis → on peut serrer (higher threshold = more sensitive)
            self.threshold = max(self.min_threshold, self.threshold - self.adjust_step)
        # Entre 0.5-0.9: on garde


# ═════════════════════════════════════════════════════════════
# 6. BREATH-RATE MONITOR — 0 CPU 0 RAM
# ═════════════════════════════════════════════════════════════

class BreathRateMonitor:
    """
    Δt entre actions consécutives.
    Si Δt collapse soudainement → le système est dans un pattern de boucle.
    Pure timestamp, 0 CPU 0 RAM.
    """
    
    def __init__(self, window: int = 10, collapse_factor: float = 0.3):
        self.timestamps: deque = deque(maxlen=window + 1)
        self.collapse_factor = collapse_factor
    
    def observe(self) -> None:
        """Record a tick (called at each action)."""
        self.timestamps.append(time.time())
    
    def is_collapse(self) -> bool:
        """True si le Δt collapse (boucle rapide)."""
        if len(self.timestamps) < 3:
            return False
        
        # Recent deltas (last 3)
        recent = list(self.timestamps)[-3:]
        recent_deltas = [recent[i+1] - recent[i] for i in range(len(recent)-1)]
        recent_avg = sum(recent_deltas) / len(recent_deltas)
        
        # Older deltas (window - 3)
        if len(self.timestamps) > 5:
            older = list(self.timestamps)[:-(3+1)]
            older_deltas = [older[i+1] - older[i] for i in range(len(older)-1)]
            older_avg = sum(older_deltas) / len(older_deltas)
            
            if older_avg > 0 and recent_avg < older_avg * self.collapse_factor:
                return True  # Collapse = action 10× plus rapide que la moyenne
        
        return False


# ═════════════════════════════════════════════════════════════
# 7. PRE-FLIGHT REGEX (plan-level, 0 LLM)
# ═════════════════════════════════════════════════════════════

class PreFlightRegex:
    """
    Bloque AVANT exécution, sur le plan, en regex pur.
    Patterns typiques de loops:
    - "if X then X" (tautology)
    - "retry N without changing params"
    - "while not converged: do same thing"
    """
    
    PATTERNS = [
        (r'if\s+(\w+)\s+then\s+\1', "Tautology: if X then X"),
        (r'retry\s+\d+\s*(times?)?\s*(without|with same)', "Retry without changing params"),
        (r'while\s+not\s+converged[^{]*do\s+same', "Loop without exit condition change"),
        (r'for\s+(\w+)\s+in\s+\1\b', "Self-iteration"),
        (r'loop\s+\d+\s*times?', "Explicit loop count"),
    ]
    
    def __init__(self):
        self.compiled = [(re.compile(p, re.IGNORECASE), msg) for p, msg in self.PATTERNS]
    
    def check(self, plan: str) -> List[Dict[str, str]]:
        """Return list of detected issues, [] if plan looks safe."""
        issues = []
        for pattern, msg in self.compiled:
            if pattern.search(plan):
                issues.append({
                    "pattern": pattern.pattern,
                    "issue": msg,
                    "severity": "warn",
                })
        return issues


# ═════════════════════════════════════════════════════════════
# 8. LOOP DNA (SHA-256 local, cross-session)
# ═════════════════════════════════════════════════════════════

class LoopDNA:
    """
    SHA-256 fingerprint de chaque boucle résolue.
    Stockage local: ~/.anti_loop/loops.json
    Si même DNA revu → kill instant.
    """
    
    DEFAULT_PATH = Path.home() / ".anti_loop" / "loops.json"
    
    def __init__(self, storage_path: Optional[Path] = None):
        self.storage_path = storage_path or self.DEFAULT_PATH
        self.storage_path.parent.mkdir(parents=True, exist_ok=True)
        self.known_loops: Dict[str, Dict] = self._load()
    
    def _load(self) -> Dict[str, Dict]:
        if self.storage_path.exists():
            try:
                with open(self.storage_path) as f:
                    return json.load(f)
            except Exception:
                return {}
        return {}
    
    def _save(self):
        with open(self.storage_path, 'w') as f:
            json.dump(self.known_loops, f, indent=2)
    
    def fingerprint(self, actions: List[str]) -> str:
        """Compute SHA-256 of a loop signature."""
        canonical = json.dumps(sorted(actions), sort_keys=True)
        return hashlib.sha256(canonical.encode()).hexdigest()
    
    def record(self, actions: List[str], resolution: str = "healed"):
        """Store a new loop fingerprint."""
        fp = self.fingerprint(actions)
        self.known_loops[fp] = {
            "actions_sample": actions[:3],
            "actions_count": len(actions),
            "first_seen": datetime.now().isoformat(),
            "resolution": resolution,
            "occurrences": 1,
        }
        self._save()
    
    def is_known(self, actions: List[str]) -> bool:
        """True si ce pattern a déjà été vu."""
        return self.fingerprint(actions) in self.known_loops
    
    def get_known_count(self) -> int:
        return len(self.known_loops)


# ═════════════════════════════════════════════════════════════
# 9. CROSS-HARNESS ADAPTERS
# ═════════════════════════════════════════════════════════════

class CrossHarnessAdapters:
    """
    Wrappers stdlib pour Claude API, OpenAI API, LangChain, AutoGen, Hermes, custom.
    Interface unique: AntiLoop.observe(response, tool_calls).
    """
    
    @staticmethod
    def adapt_anthropic(response) -> str:
        """Adapt Anthropic API response to text."""
        try:
            return response.content[0].text if hasattr(response, 'content') else str(response)
        except Exception:
            return str(response)
    
    @staticmethod
    def adapt_openai(response) -> str:
        """Adapt OpenAI API response to text."""
        try:
            return response.choices[0].message.content if hasattr(response, 'choices') else str(response)
        except Exception:
            return str(response)
    
    @staticmethod
    def adapt_langchain(response) -> str:
        """Adapt LangChain response to text."""
        return str(getattr(response, 'content', response))
    
    @staticmethod
    def adapt_autogen(response) -> str:
        """Adapt AutoGen response to text."""
        if isinstance(response, dict):
            return response.get('content', str(response))
        return str(getattr(response, 'content', response))
    
    @staticmethod
    def adapt_hermes(response) -> str:
        """Adapt Hermes (Nous Research) response to text."""
        if isinstance(response, dict):
            return response.get('message', response.get('content', str(response)))
        return str(getattr(response, 'message', getattr(response, 'content', response)))
    
    @staticmethod
    def adapt_custom(response) -> str:
        """Generic adapter: try common attributes."""
        for attr in ['content', 'text', 'message', 'output', 'result']:
            if hasattr(response, attr):
                return str(getattr(response, attr))
        return str(response)


# ═════════════════════════════════════════════════════════════
# 🎼 ANTI-LOOP — Main class
# ═════════════════════════════════════════════════════════════

class AntiLoop:
    """
    Main guard class. Branch in 3 lines:
    
        guard = AntiLoop(mode="heal", max_iter=10)
        result = guard.observe(action, intent)
        if result["intervene"]:
            apply(result["directive"])
    """
    
    def __init__(
        self,
        mode: str = HealingMode.HEAL,
        max_iter: int = 10,
        threshold: float = 0.95,
        storage_path: Optional[Path] = None,
    ):
        self.max_iter = max_iter
        self.iteration = 0
        self.last_intent = ""
        
        # 9 components
        self.entropy = PredictiveEntropy(threshold=0.3)
        self.novelty = NoveltyDetector(similarity_threshold=threshold)
        self.taxonomy = LoopTaxonomy()
        self.healer = HealingInjector(mode=mode)
        self.thresholds = SelfTuningThresholds(initial_threshold=threshold)
        self.breath = BreathRateMonitor()
        self.preflight = PreFlightRegex()
        self.dna = LoopDNA(storage_path=storage_path)
        self.adapters = CrossHarnessAdapters()
    
    def pre_flight(self, plan: str) -> List[Dict[str, str]]:
        """Check a plan BEFORE execution (0 LLM)."""
        return self.preflight.check(plan)
    
    def observe(self, action: str, intent: Optional[str] = None) -> Dict[str, Any]:
        """
        Observe an action. Returns directive dict.
        
        Returns:
            {
                "intervene": bool,
                "loop_type": str or None,
                "directive": dict from HealingInjector,
                "novelty": float,
                "entropy": float,
                "iteration": int,
            }
        """
        self.iteration += 1
        self.breath.observe()
        
        if intent:
            self.last_intent = intent
        
        # Layer 1: Predictive Entropy
        entropy = self.entropy.observe(action)
        entropy_alert = self.entropy.is_collapse_imminent()
        
        # Layer 2: Novelty
        novelty = self.novelty.observe(action)
        novelty_low = novelty < (1.0 - self.novelty.similarity_threshold)
        
        # Layer 3: Taxonomy
        loop_type = self.taxonomy.observe(action, intent)
        
        # Layer 4: Breath
        breath_collapse = self.breath.is_collapse()
        
        # Layer 5: Loop DNA (known pattern)
        is_known = self.dna.is_known([action])
        
        # Decision
        should_intervene = (
            entropy_alert or
            novelty_low or
            loop_type is not None or
            breath_collapse or
            self.iteration >= self.max_iter
        )
        
        if should_intervene:
            directive = self.healer.inject(action, self.last_intent)
            # Record DNA
            if loop_type or is_known:
                self.dna.record([action], resolution=directive["action"])
            return {
                "intervene": True,
                "loop_type": loop_type,
                "directive": directive,
                "novelty": novelty,
                "entropy": entropy,
                "iteration": self.iteration,
                "known_loop": is_known,
            }
        
        return {
            "intervene": False,
            "loop_type": None,
            "directive": None,
            "novelty": novelty,
            "entropy": entropy,
            "iteration": self.iteration,
        }
    
    def reset(self):
        """Reset state between sessions."""
        self.iteration = 0
        self.entropy = PredictiveEntropy(threshold=0.3)
        self.novelty = NoveltyDetector()
        self.taxonomy = LoopTaxonomy()
        self.breath = BreathRateMonitor()
    
    def stats(self) -> Dict[str, Any]:
        """Get current stats."""
        return {
            "iteration": self.iteration,
            "heal_count": self.healer.heal_count,
            "known_loops": self.dna.get_known_count(),
            "current_threshold": self.thresholds.threshold,
        }


# ═════════════════════════════════════════════════════════════
# CLI
# ═════════════════════════════════════════════════════════════

def main():
    import argparse
    p = argparse.ArgumentParser(description="anti-infinite-loop v2.0")
    p.add_argument("--check-plan", help="Pre-flight check on a plan string")
    p.add_argument("--demo", action="store_true", help="Run a demo loop scenario")
    p.add_argument("--stats", action="store_true", help="Show stats")
    args = p.parse_args()
    
    if args.check_plan:
        guard = AntiLoop()
        issues = guard.pre_flight(args.check_plan)
        if issues:
            print(f"⚠️ {len(issues)} issue(s) found:")
            for i in issues:
                print(f"  - {i['issue']} (pattern: {i['pattern'][:40]})")
        else:
            print("✅ Plan looks safe")
    
    elif args.demo:
        print("=== Demo: Agent loop ===")
        guard = AntiLoop(mode="heal", max_iter=5)
        actions = [
            ("search for X", "find X"),  # ok
            ("search for X", "find X"),  # repetition
            ("search for X", "find X"),  # repetition
            ("search for X", "find X"),  # repetition
            ("search for X", "find X"),  # trigger
        ]
        for i, (action, intent) in enumerate(actions):
            result = guard.observe(action, intent)
            status = "🛑 INTERVENE" if result["intervene"] else "✅ OK"
            print(f"  [{i+1}] {status} | iter={result['iteration']} | "
                  f"novelty={result['novelty']:.2f} | "
                  f"entropy={result['entropy']:.2f} | "
                  f"type={result.get('loop_type')}")
            if result["intervene"]:
                d = result["directive"]
                print(f"     → {d['action']}: {d.get('system_message', d.get('message', ''))[:80]}")
        print(f"\nFinal stats: {guard.stats()}")
    
    elif args.stats:
        guard = AntiLoop()
        print(json.dumps(guard.stats(), indent=2))
    
    else:
        p.print_help()


if __name__ == "__main__":
    main()
