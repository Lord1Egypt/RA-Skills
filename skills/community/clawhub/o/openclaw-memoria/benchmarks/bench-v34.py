#!/usr/bin/env python3
"""
LEGACY — Memoria v3.4.0 Benchmark (March 2026)
Targets v3.4.0 with 10 synthetic sessions. Kept for reference.
Current version: v3.22.3 with 21 layers — updated benchmarks TBD.
"""
import json, time, requests, sqlite3, os, re
from collections import defaultdict

OLLAMA = "http://localhost:11434"
LMSTUDIO = "http://localhost:1234/v1"
OPENAI = "https://api.openai.com/v1"
OPENAI_KEY = os.environ.get("OPENAI_API_KEY", "YOUR_KEY_HERE")
EMBED_MODEL = "nomic-embed-text-v2-moe"
EXTRACT_MODEL = "gemma3:4b"
ANSWER_MODEL = "openai/gpt-oss-20b"
JUDGE_MODEL = "gpt-5.4-nano"
DB_PATH = "/tmp/bench-v34-clusters.db"
RESULTS_PATH = f"/tmp/results-v34-{time.strftime('%Y%m%d-%H%M%S')}.json"

# Known entities for clustering
KNOWN_ENTITIES = [
    "Sol", "Luna", "Koda", "Neto", "Bureau", "Convex", "Primask",
    "DockGroups", "Memoria", "Ollama", "Cloudflare", "Vercel",
    "Qonto", "Alexandre", "Pierre", "Primo Studio", "LM Studio"
]

CONCEPT_MAP = {
    "taux horaire": ["€/h", "salaire"],
    "salaire": ["taux horaire", "€/h"],
    "rémunération": ["salaire", "€/h"],
    "ca": ["chiffre d'affaires"],
    "chiffre d'affaires": ["CA"],
    "deploy": ["déploiement"],
    "déploiement": ["deploy"],
    "modèle": ["model"],
    "modèles": ["models"],
    "config": ["configuration"],
    "configuration": ["config"],
}

SESSIONS = [
    {"id": "s1", "messages": [
        "J'ai configuré Ollama sur Sol avec gemma3:4b comme modèle d'extraction.",
        "Les embeddings utilisent nomic-embed-text-v2-moe avec 768 dimensions.",
        "Le fallback chain est Ollama → LM Studio → OpenAI."
    ]},
    {"id": "s2", "messages": [
        "Bureau utilise Convex comme backend avec des subscriptions useQuery en temps réel.",
        "Le module CRM gère 11 structures : entreprises, associations et collectivités.",
        "La sync Qonto se fait via une action Convex, pas un script bash."
    ]},
    {"id": "s3", "messages": [
        "Neto travaille depuis la Guyane française, timezone America/Cayenne (GMT-3).",
        "Il préfère le step-by-step et déteste les régressions.",
        "Sa machine principale est un Mac Studio avec 64 Go de RAM."
    ]},
    {"id": "s4", "messages": [
        "Primask est une app de planning développée par Primo Studio.",
        "Le deploy se fait via GitHub → Vercel avec auto-deploy.",
        "Le token Hello-Primo est utilisé pour les projets Bureau sur Vercel."
    ]},
    {"id": "s5", "messages": [
        "Luna est un iMac qui gère les emails et le calendrier via CalDAV iCloud.",
        "Sol est un Mac Mini disponible 24/7 pour les tâches de dev.",
        "Koda est le dev AI senior, promu le 22 mars 2026."
    ]},
    {"id": "s6", "messages": [
        "Le benchmark LongMemEval-S teste 6 catégories : SSU, SSA, SSP, KU, TR, MS.",
        "Le retrieval rate de Memoria est de 93.3% avec gemma3:4b.",
        "KU (Knowledge Update) est le point faible : 0/5 correct."
    ]},
    {"id": "s7", "messages": [
        "DockGroups est une app macOS menu bar pour organiser le Dock.",
        "Le drag & drop a été retiré car instable dans MenuBarExtra.",
        "Version actuelle : v0.5.0 avec apply-to-dock sécurisé via SIGHUP."
    ]},
    {"id": "s8", "messages": [
        "Memoria v3.2.0 ajoute le support des modèles à reasoning (Ollama/OpenAI-compat).",
        "Le recall inclut maintenant les dates avec guidance de recency.",
        "L'extraction procédurale permet les faits multi-phrases.",
        "Le hybridSearch est adaptatif : plus de poids cosine pour les queries courtes."
    ]},
    {"id": "s9", "messages": [
        "Alexandre est en amélioration, son taux horaire est de 5.19€/h.",
        "Pierre a terminé son contrat, non renouvelé. Son taux était de 7.39€/h.",
        "Le CA 2025 était de 111 223€, objectif 2026 : 80-100K€.",
        "Update : Alexandre a été augmenté à 6.50€/h suite à sa progression."
    ]},
    {"id": "s10", "messages": [
        "Cloudflare gère le DNS de primo-studio.fr avec proxy vers Vercel (front) et tunnel vers NAS (Directus).",
        "Le zone ID Cloudflare est 403c7dc0dfe5c1ec6e94d92d8d0765ba.",
        "Transport Rino est un MVP offline-first avec signatures intégrées au parcours terrain."
    ]}
]

QUESTIONS = [
    {"q": "Quel modèle d'extraction est configuré sur Sol ?", "expected": "gemma3:4b", "cat": "SSU", "session": "s1"},
    {"q": "Combien de structures gère le CRM Bureau ?", "expected": "11", "cat": "SSU", "session": "s2"},
    {"q": "Quelle est la timezone de Neto ?", "expected": "America/Cayenne", "cat": "SSU", "session": "s3"},
    {"q": "Comment se fait le deploy de Primask ?", "expected": "GitHub vers Vercel auto-deploy", "cat": "SSU", "session": "s4"},
    {"q": "Quel est le rôle de Luna ?", "expected": "iMac, emails et calendrier", "cat": "SSU", "session": "s5"},
    {"q": "Quels sont les 3 niveaux du fallback chain de Memoria ?", "expected": "Ollama, LM Studio, OpenAI", "cat": "SSA", "session": "s1"},
    {"q": "Quels types de structures le CRM Bureau gère-t-il ?", "expected": "entreprises, associations, collectivités", "cat": "SSA", "session": "s2"},
    {"q": "Quelles sont les 3 machines de l'équipe et leurs rôles ?", "expected": "Mac Studio (Neto), iMac Luna (emails/cal), Mac Mini Sol (dev 24/7)", "cat": "SSA", "session": "s5"},
    {"q": "Quelles features a apporté Memoria v3.2.0 ?", "expected": "reasoning models, dated recall, procedures multi-phrases, adaptive hybridSearch", "cat": "SSA", "session": "s8"},
    {"q": "Quels services Cloudflare fournit pour primo-studio.fr ?", "expected": "DNS, proxy Vercel front, tunnel NAS Directus", "cat": "SSA", "session": "s10"},
    {"q": "Comment configurer le fallback chain Memoria ?", "expected": "Ollama → LM Studio → OpenAI dans la config", "cat": "SSP", "session": "s1"},
    {"q": "Comment synchroniser Qonto avec Bureau ?", "expected": "via action Convex syncQonto, pas script bash", "cat": "SSP", "session": "s2"},
    {"q": "Quelle est la procédure pour déployer sur Vercel ?", "expected": "push GitHub déclenche auto-deploy", "cat": "SSP", "session": "s4"},
    {"q": "Comment appliquer les groupes au Dock dans DockGroups ?", "expected": "apply-to-dock sécurisé via SIGHUP", "cat": "SSP", "session": "s7"},
    {"q": "Comment fonctionne le hybridSearch adaptatif ?", "expected": "plus de poids cosine pour queries courtes, plus FTS pour queries longues", "cat": "SSP", "session": "s8"},
    {"q": "Quel est le taux horaire actuel d'Alexandre ?", "expected": "6.50€/h", "cat": "KU", "session": "s9"},
    {"q": "Pierre travaille-t-il encore chez Primo Studio ?", "expected": "non, contrat terminé", "cat": "KU", "session": "s9"},
    {"q": "Le drag & drop fonctionne-t-il dans DockGroups ?", "expected": "non, retiré car instable", "cat": "KU", "session": "s7"},
    {"q": "Quelle est la version actuelle de Memoria ?", "expected": "v3.2.0", "cat": "KU", "session": "s8"},
    {"q": "Quel est le score KU du benchmark Memoria ?", "expected": "0/5 correct", "cat": "KU", "session": "s6"},
    {"q": "Quand Koda a-t-il été promu Dev Senior ?", "expected": "22 mars 2026", "cat": "TR", "session": "s5"},
    {"q": "Quelle version de DockGroups a introduit apply-to-dock sécurisé ?", "expected": "v0.5.0", "cat": "TR", "session": "s7"},
    {"q": "Le CA a-t-il augmenté ou baissé entre 2025 et l'objectif 2026 ?", "expected": "baissé (111K → 80-100K objectif)", "cat": "TR", "session": "s9"},
    {"q": "Quel était le retrieval rate avant les améliorations v3.2.0 ?", "expected": "93.3%", "cat": "TR", "session": "s6"},
    {"q": "Avant le reasoning support, que se passait-il avec les modèles thinking ?", "expected": "le thinking consommait les tokens, réponse vide/pas de JSON", "cat": "TR", "session": "s8"},
    {"q": "Quelles machines utilisent Memoria ?", "expected": "Mac Studio (Koda) et Mac Mini (Sol)", "cat": "MS", "session": ""},
    {"q": "Quel est le lien entre Bureau et Qonto ?", "expected": "sync via action Convex, matching auto virements↔projets", "cat": "MS", "session": ""},
    {"q": "Quels sont les projets actifs de Primo Studio ?", "expected": "Bureau, Primask, DockGroups, Transport Rino, Memoria", "cat": "MS", "session": ""},
    {"q": "Quels modèles LLM sont disponibles sur Sol ?", "expected": "gemma3:4b, nomic-embed, qwen3.5:27b, GPT-OSS 20B via LM Studio", "cat": "MS", "session": ""},
    {"q": "Quels taux horaires sont pratiqués chez Primo Studio ?", "expected": "Neto 0€, Alexandre 6.50€, Pierre 7.39€ (parti)", "cat": "MS", "session": ""}
]

def expand_query(query):
    variants = [query]
    lower = query.lower()
    for key, synonyms in CONCEPT_MAP.items():
        if key in lower:
            for syn in synonyms[:2]:
                variant = re.sub(re.escape(key), syn, query, flags=re.IGNORECASE)
                if variant != query and variant not in variants:
                    variants.append(variant)
    for m in re.finditer(r'\b[A-Z][a-z]+(?:\s[A-Z][a-z]+)*', query):
        noun = m.group()
        if len(noun) > 2 and noun not in variants:
            variants.append(noun)
    return variants[:4]

def ollama_generate(prompt, model=EXTRACT_MODEL, fmt="json", timeout=120):
    body = {"model": model, "prompt": prompt, "stream": False,
            "options": {"temperature": 0.1, "num_predict": 2048, "num_ctx": 8192}}
    if fmt: body["format"] = fmt
    r = requests.post(f"{OLLAMA}/api/generate", json=body, timeout=timeout)
    r.raise_for_status()
    return r.json().get("response", "")

def ollama_generate_text(prompt, model=EXTRACT_MODEL, timeout=60):
    """Generate plain text (no JSON format constraint)"""
    body = {"model": model, "prompt": prompt, "stream": False,
            "options": {"temperature": 0.1, "num_predict": 300, "num_ctx": 4096}}
    r = requests.post(f"{OLLAMA}/api/generate", json=body, timeout=timeout)
    r.raise_for_status()
    return r.json().get("response", "").strip()

def ollama_embed(texts):
    r = requests.post(f"{OLLAMA}/api/embed", json={"model": EMBED_MODEL, "input": texts}, timeout=60)
    r.raise_for_status()
    return r.json().get("embeddings", [])

def lmstudio_chat(prompt, timeout=120):
    body = {"model": ANSWER_MODEL, "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 500, "temperature": 0.1}
    r = requests.post(f"{LMSTUDIO}/chat/completions", json=body, timeout=timeout)
    r.raise_for_status()
    data = r.json()
    msg = data["choices"][0]["message"]
    return msg.get("content") or msg.get("reasoning_content") or msg.get("reasoning") or ""

def nano_judge(question, expected, answer):
    body = {
        "model": JUDGE_MODEL,
        "messages": [
            {"role": "system", "content": "You are a fair judge evaluating answer quality. Be lenient: if the answer contains the key information from the expected answer, even with extra details or different wording, mark it as correct. Only mark wrong if the core information is missing or contradicted."},
            {"role": "user", "content": f"""Judge if this answer is correct.

Question: {question}
Expected answer: {expected}
Actual answer: {answer}

Return ONLY valid JSON: {{"verdict": "correct"|"partial"|"wrong", "reason": "brief explanation"}}"""}
        ],
        "max_completion_tokens": 150,
        "response_format": {"type": "json_object"}
    }
    try:
        r = requests.post(f"{OPENAI}/chat/completions", json=body, timeout=30,
                         headers={"Authorization": f"Bearer {OPENAI_KEY}", "Content-Type": "application/json"})
        r.raise_for_status()
        content = r.json()["choices"][0]["message"]["content"]
        j = json.loads(content)
        return j.get("verdict", "wrong"), j.get("reason", "")
    except Exception as e:
        return "wrong", f"judge error: {e}"

def cosine_sim(a, b):
    dot = sum(x*y for x,y in zip(a,b))
    na = sum(x*x for x in a)**0.5
    nb = sum(x*x for x in b)**0.5
    return dot/(na*nb) if na and nb else 0

def setup_db():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    db = sqlite3.connect(DB_PATH)
    db.execute("""CREATE TABLE facts (
        id INTEGER PRIMARY KEY, fact TEXT, category TEXT, fact_type TEXT DEFAULT 'semantic',
        confidence REAL DEFAULT 0.8, session_id TEXT, source TEXT DEFAULT 'auto-capture',
        created_at TEXT DEFAULT CURRENT_TIMESTAMP,
        superseded_by INTEGER, embedding BLOB)""")
    db.execute("CREATE VIRTUAL TABLE IF NOT EXISTS facts_fts USING fts5(fact, content=facts, content_rowid=id)")
    db.execute("""CREATE TRIGGER facts_ai AFTER INSERT ON facts BEGIN
        INSERT INTO facts_fts(rowid, fact) VALUES (new.id, new.fact); END""")
    db.commit()
    return db

def extract_facts(text, session_id):
    prompt = f"""Extract durable facts from this conversation. Return JSON array.
IMPORTANT: Create ONE FACT PER DISTINCT ENTITY (person, tool, project, machine).

Keys: fact, category (savoir/outil/erreur/preference/chronologie/rh/client), fact_type (semantic or episodic), confidence (0.0-1.0).

Text:
{text}

Return ONLY a JSON array:"""
    raw = ollama_generate(prompt)
    try:
        data = json.loads(raw)
        if isinstance(data, dict) and "facts" in data:
            data = data["facts"]
        if isinstance(data, list):
            if data and isinstance(data[0], list):
                data = data[0]
            return [f for f in data if isinstance(f, dict) and "fact" in f]
        return []
    except:
        return []

def generate_clusters(db):
    """NEW in v3.4.0: Group facts by entity, generate cluster summaries"""
    # Group facts by entity
    rows = db.execute("SELECT id, fact, category, fact_type FROM facts WHERE superseded_by IS NULL AND fact_type != 'cluster'").fetchall()
    
    entity_facts = defaultdict(list)
    for row in rows:
        fid, fact, cat, ftype = row
        # Match known entities
        for entity in KNOWN_ENTITIES:
            if entity.lower() in fact.lower():
                entity_facts[entity].append({"id": fid, "fact": fact, "category": cat})
    
    clusters_created = 0
    for entity, facts in entity_facts.items():
        if len(facts) < 3:
            continue
        
        facts_text = "\n".join(f"- [{f['category']}] {f['fact']}" for f in facts[:12])
        prompt = f"""Tu résumes un groupe de faits liés à la même entité en UN SEUL paragraphe dense.
Règles: contenir TOUTES les informations clés (noms, chiffres, dates, versions, états). 2-4 phrases max, dense et factuel, en français.

Entité: {entity}

Faits:
{facts_text}

Résumé dense:"""
        
        try:
            summary = ollama_generate_text(prompt)
            if summary and len(summary) > 20:
                # Remove any JSON/markdown artifacts
                summary = summary.strip().strip('"').strip("'")
                if summary.startswith("```"):
                    summary = re.sub(r'^```.*\n?', '', summary)
                    summary = re.sub(r'\n?```$', '', summary)
                
                member_ids = [f["id"] for f in facts[:12]]
                db.execute(
                    "INSERT INTO facts (fact, category, fact_type, confidence, session_id, source) VALUES (?, ?, 'cluster', 0.85, NULL, ?)",
                    (summary, facts[0]["category"], f"cluster:{entity.lower()}")
                )
                clusters_created += 1
        except Exception as e:
            print(f"    ⚠ Cluster {entity} failed: {e}")
    
    db.commit()
    return clusters_created

def hybrid_search_expanded(db, query, top_k=5):
    queries = expand_query(query)
    all_q_embs = ollama_embed(queries)
    results = {}
    
    for qi, q in enumerate(queries):
        tokens = [t for t in q.split() if len(t) > 1]
        if not tokens: continue
        fts_q = " OR ".join(f'"{t}"' for t in tokens[:10])
        try:
            rows = db.execute(
                "SELECT f.id, f.fact, f.category, f.fact_type, f.confidence, f.session_id, f.superseded_by, f.embedding "
                "FROM facts_fts fts JOIN facts f ON fts.rowid = f.id "
                "WHERE facts_fts MATCH ? AND f.superseded_by IS NULL LIMIT 20", (fts_q,)).fetchall()
            for i, r in enumerate(rows):
                if r[0] not in results:
                    results[r[0]] = {"id": r[0], "fact": r[1], "cat": r[2], "type": r[3], "conf": r[4],
                                     "session": r[5], "emb": r[7], "fts_rank": 1.0/(i+1), "cosine": 0}
                else:
                    results[r[0]]["fts_rank"] = max(results[r[0]]["fts_rank"], 1.0/(i+1))
        except:
            pass
    
    rows = db.execute("SELECT id, fact, category, fact_type, confidence, session_id, embedding FROM facts WHERE superseded_by IS NULL AND embedding IS NOT NULL").fetchall()
    for r in rows:
        emb = json.loads(r[6]) if isinstance(r[6], str) else None
        if not emb: continue
        max_sim = 0
        for q_emb in all_q_embs:
            sim = cosine_sim(q_emb, emb)
            if sim > max_sim:
                max_sim = sim
        if max_sim > 0.3:
            if r[0] in results:
                results[r[0]]["cosine"] = max(results[r[0]].get("cosine", 0), max_sim)
            else:
                results[r[0]] = {"id": r[0], "fact": r[1], "cat": r[2], "type": r[3], "conf": r[4],
                                 "session": r[5], "emb": r[6], "fts_rank": 0, "cosine": max_sim}
    
    short_query = len(query.split()) <= 4
    w_fts = 0.20 if short_query else 0.40
    w_cos = 0.55 if short_query else 0.40
    w_conf = 0.25 if short_query else 0.20
    
    scored = []
    for r in results.values():
        score = w_fts * r.get("fts_rank", 0) + w_cos * r.get("cosine", 0) + w_conf * r.get("conf", 0.5)
        # Cluster boost: 15% more weight (info-dense)
        if r.get("type") == "cluster":
            score *= 1.15
        scored.append((score, r))
    
    scored.sort(key=lambda x: -x[0])
    return [(s, r["fact"], r["cat"]) for s, r in scored[:top_k]]

def main():
    print(f"=== Memoria v3.4.0 Benchmark — Fact Clusters + Nano Judge ===")
    print(f"Extraction: {EXTRACT_MODEL} (Ollama) | Answers: {ANSWER_MODEL} (LM Studio)")
    print(f"Embeddings: {EMBED_MODEL} (Ollama) | Judge: {JUDGE_MODEL} (OpenAI)")
    print(f"NEW: Fact Clusters (entity-grouped summaries)")
    print()
    
    # Test judge
    print("🔑 Testing GPT-5.4-nano judge...")
    v, r = nano_judge("What is 2+2?", "4", "The answer is 4.")
    print(f"  Test: verdict={v}")
    if "error" in r.lower():
        print("  ❌ Judge not working, aborting.")
        return
    print()
    
    db = setup_db()
    
    # Phase 1: Extract atomic facts
    print("📥 Phase 1: Ingestion (dense extraction)...")
    t0 = time.time()
    total_facts = 0
    for sess in SESSIONS:
        text = "\n".join(sess["messages"])
        facts = extract_facts(text, sess["id"])
        for f in facts:
            db.execute("INSERT INTO facts (fact, category, fact_type, confidence, session_id) VALUES (?,?,?,?,?)",
                       (f["fact"], f.get("category", "savoir"), f.get("fact_type", "semantic"),
                        f.get("confidence", 0.8), sess["id"]))
            total_facts += 1
        db.commit()
    ingest_time = time.time() - t0
    print(f"  ✅ {total_facts} atomic facts from {len(SESSIONS)} sessions in {ingest_time:.1f}s")
    
    # Phase 2: Generate clusters (NEW in v3.4.0)
    print("\n🧩 Phase 2: Fact Clusters...")
    t0 = time.time()
    num_clusters = generate_clusters(db)
    cluster_time = time.time() - t0
    total_with_clusters = db.execute("SELECT COUNT(*) FROM facts WHERE superseded_by IS NULL").fetchone()[0]
    print(f"  ✅ {num_clusters} clusters generated in {cluster_time:.1f}s ({total_with_clusters} total facts)")
    
    # Phase 3: Embeddings (atomic + clusters)
    print("\n📐 Phase 3: Embeddings...")
    t0 = time.time()
    rows = db.execute("SELECT id, fact FROM facts WHERE superseded_by IS NULL").fetchall()
    batch_size = 20
    embedded = 0
    for i in range(0, len(rows), batch_size):
        batch = rows[i:i+batch_size]
        texts = [r[1] for r in batch]
        embs = ollama_embed(texts)
        for (rid, _), emb in zip(batch, embs):
            db.execute("UPDATE facts SET embedding = ? WHERE id = ?", (json.dumps(emb), rid))
            embedded += 1
        db.commit()
    embed_time = time.time() - t0
    print(f"  ✅ {embedded}/{len(rows)} embedded in {embed_time:.1f}s")
    
    # Phase 4: Q&A
    print(f"\n❓ Phase 4: Q&A + Nano Judge ({len(QUESTIONS)} questions)...")
    results = []
    cats = {}
    for i, q in enumerate(QUESTIONS):
        t0 = time.time()
        expanded = expand_query(q["q"])
        hits = hybrid_search_expanded(db, q["q"], top_k=5)
        retrieval_hit = any(
            any(kw.lower() in h[1].lower() for kw in q["expected"].split(", ")[:2])
            for h in hits
        )
        context = "\n".join(f"- [{h[2]}] {h[1]}" for h in hits)
        
        prompt = f"""Based on the following facts, answer the question concisely in French.
If you find contradicting information, prefer the most recent one.

Facts:
{context}

Question: {q['q']}

Answer concisely:"""
        try:
            answer = lmstudio_chat(prompt, timeout=120)
        except Exception as e:
            answer = f"[Error: {e}]"
        
        latency = time.time() - t0
        verdict, reason = nano_judge(q["q"], q["expected"], answer)
        
        cat = q["cat"]
        if cat not in cats:
            cats[cat] = {"correct": 0, "partial": 0, "wrong": 0, "retrieval_hits": 0, "total": 0}
        cats[cat]["total"] += 1
        cats[cat][verdict] += 1
        if retrieval_hit:
            cats[cat]["retrieval_hits"] += 1
        
        # Check if a cluster was in the top hits
        has_cluster = any("cluster" in str(h) for h in hits)
        cluster_marker = " 🧩" if has_cluster else ""
        
        status = "✅" if verdict == "correct" else "🟡" if verdict == "partial" else "❌"
        exp_str = f" [+{len(expanded)-1}exp]" if len(expanded) > 1 else ""
        print(f"  {status} Q{i+1} [{cat}] {q['q'][:50]}... → {verdict} ({latency:.1f}s) {'📎' if retrieval_hit else '🔍✗'}{exp_str}{cluster_marker}")
        
        results.append({
            "question": q["q"], "expected": q["expected"], "answer": answer,
            "verdict": verdict, "reason": reason, "category": cat,
            "retrieval_hit": retrieval_hit, "latency_s": round(latency, 2),
            "expanded_queries": expanded,
            "context_facts": [h[1] for h in hits]
        })
    
    total_correct = sum(c["correct"] for c in cats.values())
    total_partial = sum(c["partial"] for c in cats.values())
    total_retrieval = sum(c["retrieval_hits"] for c in cats.values())
    avg_latency = sum(r["latency_s"] for r in results) / len(results)
    acc = (total_correct+total_partial/2)/len(QUESTIONS)*100
    ret = total_retrieval/len(QUESTIONS)*100
    
    print(f"\n{'='*60}")
    print(f"📊 RÉSULTATS — Memoria v3.4.0 + Fact Clusters")
    print(f"{'='*60}")
    print(f"  Facts: {total_facts} atomic + {num_clusters} clusters = {total_with_clusters} total")
    print(f"  Accuracy:  {total_correct}/{len(QUESTIONS)} correct + {total_partial} partial = {acc:.1f}%")
    print(f"  Retrieval: {total_retrieval}/{len(QUESTIONS)} = {ret:.1f}%")
    print(f"  Latency:   {avg_latency:.1f}s avg")
    print(f"\n  Par catégorie:")
    for cat in ["SSU", "SSA", "SSP", "KU", "TR", "MS"]:
        if cat in cats:
            c = cats[cat]
            print(f"    {cat}: {c['correct']}/{c['total']} correct, {c['partial']} partial, retrieval {c['retrieval_hits']}/{c['total']}")
    
    print(f"\n  📈 vs v3.3.0 (nano judge, same pipeline sans clusters):")
    print(f"     v3.3.0: 75.0% accuracy, 43.3% retrieval")
    print(f"     v3.4.0: {acc:.1f}% accuracy, {ret:.1f}% retrieval")
    print(f"     Clusters: {num_clusters} generated in {cluster_time:.1f}s")
    
    output = {
        "benchmark": "Memoria v3.4.0 (fact clusters)", "date": time.strftime("%Y-%m-%d %H:%M:%S"),
        "config": {"extract": EXTRACT_MODEL, "answer": ANSWER_MODEL, "embed": EMBED_MODEL,
                   "judge": JUDGE_MODEL, "query_expansion": True, "fact_clusters": True},
        "metrics": {
            "atomic_facts": total_facts, "clusters": num_clusters, "total_facts": total_with_clusters,
            "embedded": embedded,
            "ingest_time_s": round(ingest_time, 1), "cluster_time_s": round(cluster_time, 1),
            "embed_time_s": round(embed_time, 1),
            "accuracy": round(acc, 1), "correct": total_correct, "partial": total_partial,
            "wrong": len(QUESTIONS)-total_correct-total_partial,
            "retrieval_rate": round(ret, 1), "avg_latency_s": round(avg_latency, 1)
        },
        "by_category": cats, "results": results
    }
    with open(RESULTS_PATH, "w") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    print(f"\n  💾 Résultats: {RESULTS_PATH}")
    print(f"  💾 DB: {DB_PATH}")

if __name__ == "__main__":
    main()
