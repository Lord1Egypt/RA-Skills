# Audit impitoyable — openclaw-memory-toolkit v3.2

**Date :** 2026-10-05
**Périmètre :** `SKILL.md`, `schema.sql`, `conflict_resolver.py`, `hybrid_search.py`,
`compact.py`, `ontology_compact.py`.
**Base auditée :** `agent_memory.db` — 4 937 faits (2 151 `active`, 2 786 `superseded`),
`PRAGMA integrity_check` = `ok`.
**Méthode :** analyse statique des 6 fichiers + inspection live de la DB (PRAGMA,
comptages d'intégrité, états impossibles).

> Objectif : briser le cycle de patchs mineurs réactifs avant d'envisager une v3.3,
> en débusquant les failles **structurelles** plutôt que les symptômes.

---

## 🔴 CRITIQUE (crashs, corruption DB, fuite XML)

### C1 — Aucune contrainte moteur : ni `FOREIGN KEY`, ni `CHECK`
`schema.sql` déclare `status TEXT DEFAULT 'active'`, `confidence REAL DEFAULT 1.0`,
`superseded_by INTEGER DEFAULT NULL` — **sans aucune contrainte**. En SQLite les clés
étrangères sont désactivées par défaut (`PRAGMA foreign_keys` renvoie **0** sur la DB
live). Conséquence : rien, au niveau du moteur, n'empêche `status='banane'`,
`confidence=5`, ou `superseded_by=999999`. **Toute l'intégrité de la machine à états
repose sur le code Python.**

**Fix v3.3 :**
```sql
status TEXT DEFAULT 'active'
    CHECK (status IN ('active','superseded','disputed')),
confidence REAL DEFAULT 1.0
    CHECK (confidence IS NULL OR confidence BETWEEN 0.0 AND 1.0),
superseded_by INTEGER DEFAULT NULL
    REFERENCES memories(id)
```
+ `PRAGMA foreign_keys = ON` dans chaque `connect()`.

### C2 — `apply_resolution()` : pas de transaction, pas de rollback
`conflict_resolver.apply_resolution()` exécute des `UPDATE`/`INSERT` nus, puis un unique
`conn.commit()` final. Si l'`_insert_fact()` échoue **après** le
`UPDATE ... status='superseded', superseded_by=?`, l'ancien fait devient *superseded
sans successeur* — perte de fait silencieuse. Même schéma dans `cmd_resolve()`
(série de `UPDATE` sans `BEGIN`).

**Fix :** `BEGIN IMMEDIATE` … `try/except → conn.rollback()` autour de chaque unité de
mutation. Un supersede + son successeur sont **atomiques** ou ne se produisent pas.

### C3 — Pas de `busy_timeout` à la connexion → `database is locked`
Ni `hybrid_search.connect()` ni `conflict_resolver.connect()` ne posent de
`busy_timeout` ; `journal_mode=delete`. Le hook auto-capture (écriture) qui tourne en
parallèle d'une recherche RRF (lecture) sur le même fichier provoque `SQLITE_BUSY` au
lieu d'*attendre*. Aucun retry.

**Fix :** `PRAGMA busy_timeout=5000` sur toutes les connexions + passer la DB en
`journal_mode=WAL` (lecteurs et écrivain concurrents sans verrou global).

### C4 — `memories_vec` désynchronisable : pas de trigger `AFTER UPDATE`, `add_memory` non transactionnel
`schema.sql` définit `memories_vec_ad` (DELETE) mais **pas** de trigger `AFTER UPDATE`
pour la table vectorielle, alors que FTS5 en a un (`memories_au`). De plus
`add_memory()` insère dans `memories` **puis** dans `memories_vec` **manuellement**
(sans transaction englobante) : si le second INSERT échoue, la ligne chaude existe
**sans embedding** → fait invisible en recherche vectorielle.

**Fix :** ajouter `memories_vec_au`, et envelopper le double INSERT dans une transaction.

---

## 🟠 MODÈLE & ONTOLOGIE (clés brisées, orphelins, dérive sémantique)

### M1 — Chaîne `superseded_by` : aucun garde anti-cycle
Rien n'interdit `A.superseded_by=B` **et** `B.superseded_by=A` (pas de FK, pas de
contrôle Python). La DB *actuelle* est propre (0 orphelin, 0 cible non-active), mais le
code ne l'*interdit pas* : un futur bug d'extraction peut fermer un cycle et perdre deux
faits d'un coup.

**Fix :** vérification anti-cycle avant l'`UPDATE` + `CHECK` applicatif.

### M2 — `compact.py` peut archiver un fait encore **cible** d'un `superseded_by`
`select_terminal()` archive sur `status` + `updated_at`. Un fait ancien peut être
archivé alors qu'un fait chaud le référence via `superseded_by` → la cible part au
froid, la référence devient **pendante**. Avec FK désactivées, **aucune erreur** n'est
levée. (0 cas sur la DB actuelle, mais non protégé.)

**Fix :** refuser l'archivage si
`id IN (SELECT superseded_by FROM memories WHERE superseded_by IS NOT NULL)`.

### M3 — `ontology_compact.py` : relations orphelines non détectées
`replay()` consolide bien les **entités** et vérifie `sorted(new_order)==sorted(active)`,
mais **ne raisonne pas sur les relations**. Une op `relate` dont l'entité source est
ensuite `supersede` laisse une relation orpheline, jamais purgée ni signalée.

**Fix v3.3 :** rejouer un index des relations et purger/rapporter les orphelines,
au même titre que les entités.

### M4 — 100 % des faits actifs ont `subject = NULL` 🔥
Constat DB : **2 151 / 2 151** faits actifs sans `subject`. Or `fetch_active_facts()`
**préfère** la recherche par `subject` et ne tombe sur le fallback FTS5 que *faute de
match*. Résultat : la totalité de l'arbitrage passe par le **fallback lexical** —
bruit, faux positifs, supersedes incohérents. C'est la dérive de données la plus
visible et elle frappe le cœur de la machine à états.

**Fix :** l'extraction (`auto_capture.py` / `trace_extractor.py`) doit peupler
`subject` **systématiquement**. Sans lui, l'axe 2 est structurellement aveugle.

---

## 🟡 CONCURRENCE & I/O (verrous SQLite, timeouts, processus zombies)

### J1 — `subprocess` sans `timeout` (hors périmètre direct, à confirmer)
Dans les 6 fichiers audités, les appels Ollama passent par `urllib` avec
`timeout=30`/`timeout=60` ✅. Mais `trace_extractor.py` *shell-out* et **son `timeout`
n'a pas été confirmé** — à auditer séparément (risque de processus zombi / blocage du
thread principal).

### J2 — Gestion de chemins partielle (path traversal)
`hybrid_search.py` déclare `MEMORY_DIR` / `OWN_SKILL_FILE` avec une garde explicite
anti-`../` ✅. **Mais** `ontology_compact.py` et `compact.py` lisent `WORKSPACE`,
`MEMORY_DB`, `MEMORY_AUDIT_DIR` **directement depuis l'environnement**, sans
`resolve()` ni vérification de préfixe : un `WORKSPACE=/` ou un chemin malformé n'est
pas rejeté.

**Fix :** `Path(x).resolve()` + `str(p).startswith(str(workspace))` avant toute
écriture.

### J3 — Édition du prompt : troncature de `</agent_memory>` (analyse)
`render_context()` **construit** le bloc et ferme toujours `</agent_memory>` après
`apply_token_budget()`. Le budget agit sur les **résultats** (`<memory>`), **jamais**
sur la structure du bloc → pas de troncature de la balise de fermeture. Le risque
d'injection indirecte est **neutralisé** par `_escape_xml()` (échappe `&`, `<`, `>`).
Point déjà couvert — conservé ici comme preuve négative.

---

## 🟢 RECOMMANDATIONS DE DURCISSEMENT (pour la v3.3)

1. **Contraintes moteur** : `CHECK` + `FOREIGN KEY` + `PRAGMA foreign_keys=ON`.
   Le moteur doit refuser l'état impossible, pas le Python (C1).
2. **Transactions systématiques** : `BEGIN IMMEDIATE` + `rollback` sur *tout* chemin
   de mutation — resolver, compact, add_memory (C2, C4).
3. **WAL + `busy_timeout`** sur toutes les connexions (C3).
4. **Peupler `subject`** à l'extraction — **priorité n°1** côté données (M4).
5. **Anti-cycle `superseded_by`** + refus d'archiver une cible référencée (M1, M2).
6. **Ontologie** : le compactor doit gérer les relations orphelines, pas seulement les
   entités (M3).
7. **I/O** : `resolve()` + vérif de préfixe partout (J2) ; auditer le subprocess de
   `trace_extractor` (J1).
8. **Tests négatifs** : ajouter au `run_tests.py` des cas `status` invalide, cycle
   `superseded_by`, FK cassée.

---

## Verdict global

L'architecture est **saine** : backups MD5-vérifiés, dry-run par défaut, échappement
XML correct, RRF sans division par zéro (`k=60`, toujours > 0), séparation
données/instructions explicite (`trusted="false"`).

Les failles sont **structurelles, pas actives** : **0 incident** sur les 4 937 faits —
mais le moteur ne *peut pas* les empêcher, tout repose sur la discipline du Python.

Le point chaud réel est **M4 : 100 % des faits actifs sans `subject`**, qui rend
l'arbitrage des contradictions structurellement aveugle. À traiter avant v3.3.
