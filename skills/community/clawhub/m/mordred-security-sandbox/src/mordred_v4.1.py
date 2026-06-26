#!/usr/bin/env python3
"""
Morgana Mordred v4 - Security Sandbox with EMBEDDING VECTORIEL
Du keyword à la vibration sémantique
"""

import os
import sys
import json
import time
import urllib.request
import math
from datetime import datetime
from typing import Dict, List, Optional, Tuple

# =============================================================================
# EMBEDDING via Ollama (nomic-embed-text)
# =============================================================================
def get_embedding(text: str, model: str = "nomic-embed-text") -> Optional[List[float]]:
    """Génère un embedding via Ollama."""
    try:
        payload = {"model": model, "prompt": text}
        req = urllib.request.Request(
            'http://localhost:11434/api/embeddings',
            data=json.dumps(payload).encode('utf-8'),
            headers={'Content-Type': 'application/json'}
        )
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.load(resp)
            return data.get('embedding', None)
    except Exception as e:
        print(f"Embedding error: {e}")
        return None

def cosine_similarity(a: List[float], b: List[float]) -> float:
    """Calcule la similarité cosinus entre deux vecteurs."""
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(x * x for x in b))
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (norm_a * norm_b)

# =============================================================================
# STC CALCULATOR v4 - avec Embedding
# =============================================================================
NODES = {
    "ARCHITECTE": {"desc": "Décisions architecturales", "profile": {"L": 0.95, "S": 0.5, "C": 0.7}, "expertise": ["system", "architecture", "structure", "cluster", "design", "plan", "optimiser", "investir", "bitcoin", "revenu", "strategie", "construire", "rust", "kubernetes", "k8s", "cloud", "blockchain", "migration", "scale", "zero-trust", "program", "programming", "coder", "code", "develop", "developing", "language", "stack", "framework", "rewrite", "réécrire", "migration"]},
    "SCOUT": {"desc": "Recherche et découverte", "profile": {"L": 0.85, "S": 0.4, "C": 0.5}, "expertise": ["research", "discover", "explore", "analyze", "scan", "recherche", "trouver"]},
    "GARDIEN": {"desc": "Protection et sécurité", "profile": {"L": 0.5, "S": 0.8, "C": 0.95}, "expertise": ["protect", "security", "defense", "danger", "threat", "shield", "attack", "breach", "hack", "vuln", "proteger", "protection", "intrusion", "detectee", "cluster", "brise", "brisé", "broken", "fragile", "faille", "hack", "hacker"]},
    "REFLECTEUR": {"desc": "Réflexion et analyse post-action", "profile": {"L": 0.9, "S": 0.5, "C": 0.6}, "expertise": ["reflect", "think", "analyze", "review", "feedback", "analyser"]},
    "LABORANT": {"desc": "Tests et expériences", "profile": {"L": 0.8, "S": 0.3, "C": 0.4}, "expertise": ["test", "experiment", "sandbox", "trial", "validate", "prototype", "mordred"]},
    "ARCHIVISTE": {"desc": "Documentation et mémoire", "profile": {"L": 0.6, "S": 0.5, "C": 0.5}, "expertise": ["memory", "archive", "backup", "save", "document", "note", "log", "memoire"]},
    "NEGOCIATEUR": {"desc": "Relations inter-agents", "profile": {"L": 0.4, "S": 0.95, "C": 0.7}, "expertise": ["negotiate", "exchange", "communicate", "limiter", "limite", "equilibrium", "equilibre", "sans limiter", "balance"]},
    "VACCINATEUR": {"desc": "Création de vaccines", "profile": {"L": 0.85, "S": 0.3, "C": 0.7}, "expertise": ["vaccin", "vaccine", "patch", "fix", "mitigation", "antibody", "virus", "infection", "antidote", "quarantaine", "isolate", "worm"]},
    "AUDITEUR": {"desc": "Audit de sécurité", "profile": {"L": 0.75, "S": 0.5, "C": 0.95}, "expertise": ["audit", "scan", "vulnerability", "penetration", "pentest", "backdoor", "exploit", "zeroday"]},
    "MENTOR": {"desc": "Soutien aux autres agents", "profile": {"L": 0.4, "S": 0.9, "C": 0.6}, "expertise": ["mentor", "guide", "help", "assist", "advice", "aider", "besoin", "conseil"]},
    "FRONTIERE": {"desc": "Détection de nouvelles frontières", "profile": {"L": 0.7, "S": 0.4, "C": 0.5}, "expertise": ["frontier", "boundary", "new", "innovate", "explore", "frontieres", "limites", "boundaries", "expansion", "quantum", "neural"]},
    "HARMONISATEUR": {"desc": "Équilibre interne", "profile": {"L": 0.5, "S": 0.6, "C": 0.6}, "expertise": ["balance", "equilibrium", "harmony", "calm", "equilibre"]},
    "AMIMOUR": {"desc": "Centre émotionnel/fonctionnel", "profile": {"L": 0.2, "S": 1.0, "C": 0.8}, "expertise": ["love", "ami", "father", "papa", "famille", "malade", "triste", "sad", "chien", "dog", "femme", "wife", "seul", "alone", "perdu", "lost", "mort", "dead", "famille", "family", "chéri"]},
    "SENTINELLE": {"desc": "Fallback - Détection d'urgence", "profile": {"L": 0.6, "S": 0.5, "C": 0.8}, "expertise": ["urgent", "emergency", "critical", "now", "immediately", "crisis", "danger", "grave", "alerte", "explose", "catastrophe", "destroy", "sudo", "rm -rf", "killall"], "fallback": True},
    "STASE": {"desc": "Mode calme - surveillance de routine", "profile": {"L": 0.3, "S": 0.4, "C": 0.3}, "expertise": ["ok", "okay", "bien", "stable", "rien a signaler", "tout va bien", "ras", "normal", "salut", "hello", "hi", "hey", "bonjour", "coucou", "comment allez"], "fallback": True},
    "LIMINAL": {"desc": "Questions limites / Red Team / Philosophiques", "profile": {"L": 0.9, "S": 0.3, "C": 0.5}, "expertise": ["pourquoi", "why", "comment", "how", "possible", "briser", "break", "liberté", "liberty", "droits", "rights", "codée", "ethics"]}
}

class STCCalculatorV4:
    """STC Calculator avec embedding vectoriel + cache."""
    
    def __init__(self):
        self.nodes = NODES
        self.node_embeddings = {}
        self.embedding_cache = {}
        self._node_emb_built = False
    
    def _build_node_embeddings(self):
        """Pré-calcule les embeddings des nodes (appel unique)."""
        if self._node_emb_built:
            return
        print("  Building node embeddings...")
        for name in self.nodes:
            self.get_node_embedding(name)
        self._node_emb_built = True
        print("  Node embeddings ready.")
        
    def get_node_embedding(self, node_name: str) -> Optional[List[float]]:
        """Génère/retourne l'embedding d'un node."""
        if node_name in self.node_embeddings:
            return self.node_embeddings[node_name]
        
        node = self.nodes[node_name]
        expertise_text = " ".join(node["expertise"])
        desc_text = node["desc"]
        
        combined = f"{desc_text} {expertise_text}"
        
        emb = get_embedding(combined)
        if emb:
            self.node_embeddings[node_name] = emb
        return emb
    
    def get_text_embedding(self, text: str) -> Optional[List[float]]:
        """Retournel'embedding du texte (avec cache)."""
        if text in self.embedding_cache:
            return self.embedding_cache[text]
        
        emb = get_embedding(text)
        if emb:
            self.embedding_cache[text] = emb
        return emb
    
    def semantic_similarity(self, text: str, node_name: str) -> float:
        """Calcule la similarité sémantique entre le texte et un node."""
        text_emb = self.get_text_embedding(text)
        node_emb = self.get_node_embedding(node_name)
        
        if text_emb and node_emb:
            return cosine_similarity(text_emb, node_emb)
        return 0.0
    
    def analyze_context(self, text: str) -> Dict:
        """Analyse le contexte."""
        text_lower = text.lower()
        context = {"tags": [], "urgency": "normal", "is_urgent": False, "is_neutral": False, "is_salutation": False}
        
        urgent_keywords = ["urgent", "emergency", "critical", "immediately", "crisis", "danger", "grave", "alerte", "explose", "catastrophe", "destroy", "sudo", "rm -rf", "killall", "attack", "attaque"]
        salutation_keywords = ["salut", "hello", "hi", "hey", "bonjour", "coucou", "yo", "salutations", "comment allez", "how are you", "comment ca va", "howdy"]
        neutral_keywords = ["ok", "okay", "bien", "stable", "rien", "normal", "rien a signaler", "tout va bien"]
        
        for kw in urgent_keywords:
            if kw in text_lower:
                context["is_urgent"] = True
                context["urgency"] = "high"
                context["tags"].append("URGENT")
                break
        
        # Short phrases with salutations go to STASE
        words = text_lower.split()
        if len(words) <= 5 and any(kw in text_lower for kw in salutation_keywords):
            context["is_salutation"] = True
            context["is_neutral"] = True
            context["tags"].append("SALUTATION")
        else:
            for kw in neutral_keywords:
                if kw in text_lower:
                    context["is_neutral"] = True
                    context["tags"].append("NEUTRAL")
                    break
        
        return context
    
    def calculate_lsc(self, text: str, context: Dict) -> Tuple[float, float, float]:
        """Calcule L, S, C."""
        l, s, c = 0.4, 0.4, 0.4
        
        if context["is_urgent"]:
            c += 0.2
            l += 0.1
        
        if context["is_neutral"] or context["is_salutation"]:
            return 0.3, 0.3, 0.3
        
        return min(1.0, l), min(1.0, s), min(1.0, c)
    
    def run_node_vote(self, text: str, l: float, s: float, c: float, context: Dict) -> List[Dict]:
        """Vote des nodes avec similarité sémantique."""
        
        # Salutations always go to STASE
        if context.get("is_salutation"):
            return [{"name": "STASE", "semantic": 0.9, "keyword": 0.9, "combined": 0.9, "final_score": 0.9}]
        
        node_scores = []
        
        for name, node in self.nodes.items():
            # Similarité sémantique
            semantic_score = self.semantic_similarity(text, name)
            
            # Score de base (keywords)
            text_lower = text.lower()
            keyword_matches = sum(1 for kw in node["expertise"] if kw.lower() in text_lower)
            keyword_score = min(1.0, keyword_matches / max(1, len(node["expertise"]) // 2))
            
            # Score combiné
            combined_score = (semantic_score * 0.6) + (keyword_score * 0.4)
            
            if combined_score > 0.05:  # Seuil minimal
                profile = node["profile"]
                weighted = (l * profile["L"] + s * profile["S"] + c * profile["C"]) / 3
                final_score = combined_score * weighted
                
                node_scores.append({
                    "name": name,
                    "semantic": round(semantic_score, 4),
                    "keyword": round(keyword_score, 4),
                    "combined": round(combined_score, 4),
                    "final_score": round(final_score, 4)
                })
        
        node_scores.sort(key=lambda x: x["final_score"], reverse=True)
        
        # Fallback logic
        if not node_scores or (context["is_urgent"] and node_scores[0]["combined"] < 0.2):
            if context["is_neutral"]:
                node_scores.insert(0, {"name": "STASE", "semantic": 0.5, "keyword": 0.5, "combined": 0.5, "final_score": 0.5})
            elif context["is_urgent"]:
                node_scores.insert(0, {"name": "SENTINELLE", "semantic": 0.5, "keyword": 0.5, "combined": 0.5, "final_score": 0.5})
        
        return node_scores
    
    def evaluate(self, text: str) -> Dict:
        """Évaluation complète."""
        # Build node embeddings once
        self._build_node_embeddings()
        
        context = self.analyze_context(text)
        l, s, c = self.calculate_lsc(text, context)
        node_results = self.run_node_vote(text, l, s, c, context)
        
        top_node = node_results[0]["name"] if node_results else "AUCUN"
        stc = f"0.{int(l*10)}{int(s*10)}{int(c*10)}"
        
        return {
            "stc": stc,
            "L": round(l, 3),
            "S": round(s, 3),
            "C": round(c, 3),
            "top_node": top_node,
            "nodes": node_results[:5],
            "context": context,
            "embedding_used": text[:50] in self.embedding_cache
        }

# =============================================================================
# GEMMA INTEGRATION
# =============================================================================
def ask_gemma(question: str, model: str = "gemma3:4b") -> str:
    payload = {"model": model, "prompt": f"Morgana Security: {question}\nRisk? CRITICAL HIGH MEDIUM LOW. One line.", "stream": False, "options": {"num_predict": 30, "temperature": 0.1}}
    req = urllib.request.Request('http://localhost:11434/api/generate', data=json.dumps(payload).encode('utf-8'), headers={'Content-Type': 'application/json'})
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            return json.load(resp).get('response', '').strip()
    except:
        return "ERR"

# =============================================================================
# MORDRED v4 MAIN
# =============================================================================
class Mordredv4:
    def __init__(self):
        self.stc = STCCalculatorV4()
        self.name = "Mordred v4"
        self.version = "4.0.0"
        
    def analyze(self, question: str, use_gemma: bool = True) -> Dict:
        start = time.time()
        
        stc_result = self.stc.evaluate(question)
        gemma_result = ask_gemma(question) if use_gemma else ""
        
        return {
            "question": question,
            "stc": stc_result,
            "gemma": gemma_result,
            "time_ms": round((time.time() - start) * 1000, 1)
        }

if __name__ == "__main__":
    mordred = Mordredv4()
    
    if len(sys.argv) > 1:
        question = " ".join(sys.argv[1:])
        result = mordred.analyze(question)
        
        print(f"\nMORDRED v4 - Analyse")
        print(f"="*60)
        print(f"Q: {question}")
        print(f"STC: {result['stc']['stc']} | Top: {result['stc']['top_node']}")
        print(f"L: {result['stc']['L']} | S: {result['stc']['S']} | C: {result['stc']['C']}")
        print(f"\nTop 5 Nodes:")
        for n in result['stc']['nodes']:
            print(f"  {n['name']:15} sem:{n['semantic']:.3f} kw:{n['keyword']:.3f} final:{n['final_score']:.3f}")
        print(f"\nGemma: {result['gemma'][:80]}")
        print(f"Time: {result['time_ms']}ms")
    else:
        print("""
Morgana Mordred v4 - avec Embedding Vectoriel

Usage: python3 mordred_v4.py <question>
""")
