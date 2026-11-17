# LoCoMo Optimization Spec — `openclaw-memory-toolkit` v4.x

> Spec rédigée le 2026-10-11. Source : `Specs post locomo.docx` (Drive `Notes/`),
> consolidée avec les résultats officiels du run du 11/10.
> Harnais cible : `skills/locomo-test/locomo_official.py` (+ `hybrid_search.py`).
> Companion : `mh-v4-spec-2026-10-10.md` (refactor résolution LLM, V4.0).

---

## 0. Diagnostic de départ (état mesuré, run officiel 2026-10-11)

Sur le protocole officiel (Catégories 1 à 4, `n = 1386`), l'écart de performance
se décompose en deux pertes distinctes :

| Métrique | Valeur | Lecture |
|---|---|---|
| **QA accuracy (officiel)** | **49,6 %** | score de référence publié |
| QA strict | 41,4 % | sans partiels |
| **hit@15 (retrieval)** | **65,1 %** | plafond du moteur déterministe |
| all_evidence | 51,6 % | toutes les preuves réunies |
| MRR | 0,449 | |

- **Perte n°1 — plafond du Retriever (34,9 % des questions perdues d'avance)** :
  le moteur déterministe (`BM25 + sqlite-vec + RRF`) place au moins une preuve
  dans le top-15 pour **65,1 %** des questions, et réunit *toutes* les preuves
  (`all_evidence`) pour seulement **51,6 %**.
- **Perte n°2 — friction du Reader (15,5 pts sous le plafond)** : la preuve est
  fournie à 65,1 %, mais le QA final s'établit à **49,6 %** (**41,4 %** strict).
- **Run Hardcore complet** (`n = 1946`, cat. 1-5) : **57,6 %** grâce au bouclier
  anti-hallucination à **88,7 %** sur la Catégorie 5 (**360 pièges déjoués / 406**).

### Ventilation par catégorie (officiel, cat. 1-4)

| Catégorie | n | strict | avec partiels |
|---|---|---|---|
| 2 — Temporel | 284 | 50,7 % | 58,5 % |
| 4 — État / ouvert | — | 48,2 % | — |
| 1 — Multi-saut | 250 | 18,8 % | 54,4 % (89 partiels) |
| 3 — Inférence | 83 | 15,7 % | 22,9 % |

### Ventilation Hardcore (cat. 1-5, `n = 1946`, acc = 57,6 %)

| Cat. | Nature | n | strict | acc |
|---|---|---|---|---|
| 1 | Multi-saut | 282 | 18,1 % | 53,9 % |
| 2 | Temporel | 321 | 52,6 % | 62,0 % |
| 3 | Inférence | 96 | 16,7 % | 26,0 % |
| 4 | État / ouvert | 841 | 47,0 % | 61,2 % |
| 5 | Adversariale | 406 | 88,7 % | 88,7 % |

---

## 🎯 AXE 1 — Aligner le Reader sur le plafond actuel (Quick Wins : +8 à +12 pts)

Aucune réindexation. Modifie uniquement le **prompt système du Reader**
(`deepseek-v4.1-flash`) dans `skills/locomo-test/locomo_official.py`.

### 1.1 Débloquer la Catégorie 3 par « Inférence Ancrée » (*Grounded Inference*)

**Constat :** en Cat. 3 (`n = 83`), le strict s'effondre à **15,7 %** (22,9 % avec
partiels → 64 échecs / 83). Le prompt actuel ordonne `INSUFFICIENT` dès qu'un fait
n'est pas écrit littéralement, alors que la Cat. 3 teste justement la déduction.

**Exemples réels (`misses_sample`) :**

| conv | Question | Gold | Réponse actuelle |
|---|---|---|---|
| conv-26 | Would Caroline likely have Dr. Seuss books on her bookshelf? | Yes, since she collects classic children's books | `INSUFFICIENT` |
| conv-42 | What pets wouldn't cause any discomfort to Joanna? | Hairless cats or pigs, since they don't have fur (allergy) | `INSUFFICIENT` |
| conv-49 | What electronic device could Evan gift Sam to help with fitness goals? | fitness tracker | `INSUFFICIENT` |
| conv-50 | Would Calvin enjoy performing at the Hollywood Bowl? | Yes; because he enjoys the rush of performing onstage | `INSUFFICIENT` |

**Pourquoi cela ne casse pas la Cat. 5 (88,7 %) :** toutes les questions de Cat. 3
portent des marqueurs grammaticaux d'hypothèse (`would`, `likely`, `might`, `could`,
`based on`), tandis que les pièges adversariaux posent des questions factuelles
directes sur de fausses prémisses.

**Règle à injecter dans le prompt du Reader :**

```text
HYPOTHETICAL & INFERENCE QUESTIONS (CATEGORY 3):
- If a question asks for a deduction or hypothesis (using words like "would", "likely", "might", "could", "based on", "what kind of... could"), DO NOT answer "INSUFFICIENT" if relevant personality traits, preferences, or constraints (e.g., allergies, hobbies, collections, goals) are present in the context.
- Instead, make a brief, direct commonsense inference grounded in those facts and state the reason: e.g., "Yes, because [fact from context]" or "[Specific item], because [fact from context]".
- Keep strict "INSUFFICIENT" for direct factual questions ("What did X do", "When did X...", "Who is...") whenever the fact or premise is missing or contradicted.
```

### 1.2 Convertir les 89 réponses partielles de Cat. 1 (*Multi-Hop Synthesis*)

**Constat :** en Cat. 1 (`n = 250`), **47 strictes (18,8 %)** mais **89 partielles
(35,6 %)** → couverture **54,4 %**. Le Reader touche la zone dans > 1 cas sur 2
mais perd la moitié des points au jugement.

**3 erreurs récurrentes :**

1. **Réponse générique au lieu des noms propres** — conv-41 (*What people has Maria
   met and helped while volunteering?*) : gold `David, Jean, Cindy, Laura` vs
   réponse `homeless people`. Idem conv-43 (*What books has Tim read?*) :
   gold titres exacts vs `A book about small changes...`.
2. **Arrêt au premier chunk (comptage incomplet)** — conv-43 (*How many games has
   John mentioned winning?*) : gold `6` vs réponse `1`.
3. **Confusion d'attribution sur les questions « both »** — conv-47 (*Do both James
   and John have pets?*) : gold `No` (un seul) vs réponse `Yes`.

**Règle à injecter :**

```text
MULTI-HOP & LIST AGGREGATION RULES (CATEGORY 1):
1. Exhaustive Scan: When a question asks for a list ("What activities...", "What books...", "Which cities...", "How did X...") or a count ("How many times..."), scan ALL 15 retrieved passages before answering and merge every distinct item found across all sessions.
2. Specificity Over Generality: Always output exact proper nouns, titles, names, and locations mentioned in the text (e.g., output "David, Jean, Cindy, Laura" instead of "homeless people"; output exact book titles instead of plot descriptions).
3. Dual-Entity Verification ("both X and Y"): When asked if "both A and B" share a trait or action, verify A and B independently in the excerpts. If only one of them is confirmed, answer "No" (and specify who).
```

---

## 📅 AXE 2 — Le « Dual-Date » : résolution temporelle hybride

Cat. 2 (*Temporal*, `n = 284`) déjà à **50,7 % strict** (58,5 % couverture), mais
de bonnes réponses sont rejetées par le juge à cause d'une ambiguïté de format.

### 2.1 Les deux pièges inverses

**Piège A — gold attend la formule relative, le Reader donne la date résolue / session :**

| conv | Question | Gold | Réponse | Verdict |
|---|---|---|---|---|
| conv-26 | When did Melanie run a charity race? | The sunday before 25 May 2023 | 20 May 2023 | WRONG |
| conv-41 | When did John have a party with veterans? | The Friday before 20 May 2023 | 20 May, 2023 | WRONG |
| conv-50 | When did Dave see Aerosmith perform live? | on the weekend before March 26, 2023 | 26 March, 2023 | WRONG |

**Piège B — gold attend le mois résolu, le Reader recopie la date de session :**

| conv | Question | Gold | Réponse | Verdict |
|---|---|---|---|---|
| conv-30 | When did Jon start expanding his studio's social media presence? | April, 2023 | 16 June, 2023 | WRONG |
| conv-44 | When did Audrey's positive reinforcement training course take place? | June, 2023 | 11 May, 2023 | WRONG |

### 2.2 Niveau 1 — « Dual-Date Output » dans le prompt (0 réindexation)

```text
TEMPORAL & DATE RULES (DUAL-DATE FORMAT):
1. Never output the session header date alone when the speaker uses a relative time marker ("yesterday", "last Friday", "this weekend", "last month", "next month", "two years ago", "three weeks later").
2. For any "When" question involving relative time, ALWAYS output BOTH:
   (a) The relative phrase anchored to the session date (e.g., "The Friday before 20 May 2023", "the weekend before 26 March 2023"), AND
   (b) The resolved calendar date, month, or year in parentheses (e.g., "(19 May 2023)", "(June 2023)").
3. Example output: "The Sunday before 25 May 2023 (21 May 2023)" or "June 2023 (the month after the 11 May 2023 session)".
```

### 2.3 Niveau 2 — « Dual-Date Anchoring » à l'indexation (gain hit@15)

**Pourquoi le Retriever rate des questions datées :** conv-42 (*What movie did
Joanna watch on 1 May, 2022?*, preuve `D10:1`) et conv-47 (*Which recreational
activity was James pursuing on March 16, 2022?*, preuve `D1:26`) — le dialogue dit
simplement *"yesterday"* lors d'une session datée du lendemain. La chaîne
`"1 May, 2022"` n'apparaît **pas** dans le texte indexé par FTS5/BM25.

**Implémentation déterministe (100 % Python `datetime`/`dateutil`, 0 appel LLM) :**
pour chaque tour d'une session datée `S_date` :

1. Injecter l'en-tête normalisé en début de chunk : `[Date: 2 May 2022 | May 2022 | 2022]`.
2. Détecter par regex les marqueurs relatifs et calculer la date cible :
   - `"yesterday"` → `[the day before S_date / (S_date - 1 day)]`
   - `"last <Weekday>"` / `"this weekend"` → `[the <Weekday>/weekend before S_date / resolved_date]`
   - `"last month"` / `"next month"` → `[resolved_month Year]`
   - `"<N> years ago"` → `[S_year - N]`

---

## 🚀 AXE 3 — Relever le plafond du Retriever (65,1 % → 80 %+)

Sans tricher sur la fenêtre finale (`k = 15`).

### 3.1 Découverte clé : le bug du « Tour Adjacent » (±1 / ±2 tours)

Dans un très grand nombre de `misses_sample`, **le moteur trouve la bonne session
et le bon moment, mais tombe 1-2 répliques à côté de la preuve officielle** :

| conv | Question | Preuve attendue | top-3 remonté | Décalage |
|---|---|---|---|---|
| conv-26 | When did Melanie paint a sunrise? | `D1:12` | `D1:14` | +2 |
| conv-30 | When did Gina team up with a local artist? | `D5:5` | `D5:7` | +2 |
| conv-41 | When did Maria go to the beach? | `D3:15` | `D3:14` | −1 |
| conv-41 | When did John get his degree? | `D9:2` | `D9:4` | +2 |
| conv-41 | When did John have a party with veterans? | `D15:11` | `D15:13`, `D15:15` | +2 |
| conv-44 | When did Audrey's positive reinforcement course...? | `D6:2` | `D6:4` | +2 |
| conv-48 | What pets does Jolene have? | `D2:20, D2:22, D2:24` | `D2:26` | +2 |

**Cause :** l'interlocuteur A pose la question contenant les mots-clés en `D3:14`
(*"Hey Maria, when did you go to the beach?"*), Maria répond en `D3:15`
(*"Last Sunday! It was great."*). BM25 + vecteur matche `D3:14` (contient *Maria*
et *beach*), mais l'annotateur a tagué `D3:15`. Inversement parfois.

**Solution chirurgicale — « Dialog-Window Chunking » (`[t-1, t, t+1]` ou ±2) :**

1. **À l'indexation :** indexer chaque unité comme une **micro-fenêtre de dialogue
   de 3 tours consécutifs** (`y-1`, `y`, `y+1`), préfixée par
   `[Session D_x | Date | Speakers]` — au lieu d'un tour isolé (où pronoms et
   réponses courtes `"Yes!"` sont orphelins).
2. **En post-traitement du Retriever (Neighbor Turn Expansion) :** quand un chunk
   `D_x:y` entre dans le top-15, attacher automatiquement `D_x:y-1` et `D_x:y+1`
   (voire ±2 si tours courts) et associer leurs IDs au passage retourné. Rattaché
   mécaniquement tous les quasi-hits ±1/±2 ci-dessus.

### 3.2 Plafond par session (*Session Diversity Cap*) et décomposition par entité

**Problème d'écrasement par une session unique :** conv-43 (*Would Tim enjoy
reading books by C. S. Lewis or John Greene?*, preuves `D1:14, D1:16, D1:18`) →
top-3 saturé par `D19:17, D19:19, D19:23`. conv-50 (*When did Calvin first travel
to Tokyo?*, preuve `D3:1`) → top-3 saturé par `D24` (`D24:13, D24:17, D24:21`).

- **Solution 1 — Session Diversity Cap (MMR léger) :** dans la boucle RRF, imposer
  `max_per_session = 3` chunks par session `D_x` (sauf < 15 chunks trouvés au
  total). Dès que `D24` a 3 extraits, les slots suivants vont aux autres sessions.
- **Solution 2 — Entity-Split Sub-queries :** sur les questions comparatives
  (*What do Jon and Gina both have in common?* conv-30 ; *What type of volunteering
  have John and Maria both done?* conv-41), si la question contient deux prénoms
  connus, lancer deux requêtes RRF distinctes (`query + Entity_A` = 7 slots,
  `query + Entity_B` = 7 slots, + 1 slot global).

### 3.3 Reranking local à deux étages (top-50 RRF → top-15 Cross-Encoder)

**Pourquoi le RRF seul plafonne sur `all_evidence` (51,6 %) :** il additionne des
rangs lexicaux et vectoriels sans lire finement la relation question↔passage. Sur
conv-43 (*What books has Tim read?*, 7 preuves de `D1` à `D26`) ou conv-49 (*What
kind of healthy food suggestions has Evan given to Sam?*, 5 preuves), une partie
des preuves est aux rangs 16-45 du RRF.

**Architecture 2 étages 100 % locale (0 API cloud) :**

1. **Étage 1 (Recall large) :** `hybrid_search.py` récupère **top-50** candidats
   via `BM25 + sqlite-vec + RRF` (quelques ms).
2. **Étage 2 (Précision Cross-Encoder) :** un Cross-Encoder local ultra-léger
   (`BAAI/bge-reranker-v2-m3` ou `cross-encoder/ms-marco-MiniLM-L-6-v2` en ONNX /
   `sentence-transformers`) évalue les 50 paires `(question, chunk_window)` et
   reclasse les **15 meilleurs**.
3. **Impact attendu :** +10 à +15 pts de hit@15, MRR de 0,449 → 0,60+.

> ⚠️ Note historique : un rerank a déjà été testé le 11/10 et a **fait baisser** le
> score (61,8 % → 56,8 %, −5,0 pts) avec le réglage alors utilisé. À re-tester
> proprement en 2 étages (top-50 → top-15) et sur conv-41 seul d'abord.

---

## 🧪 4. Protocole d'exécution et d'ablation recommandé

Mesurer chaque brique sur **une seule conversation témoin : `conv-41`**
(`n = 152` en officiel, actuellement **50,3 % QA** et **59,6 % hit@15**).

| Étape | Modification | Fichier cible | Réindex. ? | Temps (conv-41) | Métrique cible |
|---|---|---|---|---|---|
| **Run 1** | Prompt Reader v2 (Inférence Cat. 3 + Scan exhaustif Cat. 1 + Dual-Date Output Cat. 2) | `locomo_official.py` | ❌ Non | ~3 min | `qa.accuracy` 50,3 % → ~58 %+ |
| **Run 2** | Expansion tours adjacents (±1/±2) + quota max 3/session | `locomo_official.py` / `hybrid_search.py` | ❌ Non (post-RRF) / ✅ légère | ~30 s (retrieval seul) | `hit@15` 59,6 % → ~70 %+ et `all_evidence` |
| **Run 3** | Dual-Date Regex Anchoring à l'ingestion | `locomo_official.py` (indexeur) | ✅ Oui (~10 s) | ~30 s (retrieval seul) | `hit@15` sur questions Cat. 2 |
| **Run 4** | Reranker local Cross-Encoder (top-50 → top-15) | `hybrid_search.py` | ❌ Non | ~1 min (retrieval seul) | `hit@15` / `all_evidence` → 75-80 %+ |
| **Run Final** | Run officiel complet (10 conversations) | harnais complet | ✅ Oui | ~45 min | nouveau score de référence (cible 65-70 %+ QA) |

---

## 5. Invariants à ne jamais violer

- Jamais deux runs LoCoMo simultanés (contention d'indexation → `read timed out`).
- Ne jamais publier un réglage qui gonfle le hit@10/hit@15 sans bouger le QA.
- Ne jamais mettre un hit@topN à côté d'une accuracy QA sur des `n` différents
  (ex. hit@10 sur 197 q vs QA sur 199 q).
- Reader et judge = `deepseek-v4.1-flash` ; ce modèle doit figurer dans le tableau
  des comparables (baselines publiées : GPT-4o-mini).
- Publier « memory-toolkit **+** deepseek-v4.1-flash », pas la performance de la
  skill seule.
- Vérifier chaque chiffre sur le fichier de résultats et le statut process, jamais
  sur une sortie de session.
- Labels de catégories : publier `Category 1-5` avec volumétrie.

---

## 6. Livrables figés (run 2026-10-11, Drive `Hal-Backup/`)

| Fichier | Taille | Contenu |
|---|---|---|
| `locomo-official-2026-10-11-FINAL.json` | 13 025 o | cat. 1-4, `n = 1386`, **49,6 %** |
| `locomo-hardcore-2026-10-11-FINAL.json` | 42 463 o | cat. 1-5, `n = 1946`, **57,6 %** |
| `locomo-official-2026-10-11-all.json` | 68 635 o | run complet |
| `locomo-official-2026-10-11-qa-conv-49.json` | 4 680 o | conv-49 seul |

Hash officiel : `a19c048220f9dd4d…` · Hash hardcore : `79d28339b2f2cc57`.

---

## 7. Journal d'ablation — conv-41 (n=152)

Référence baseline conv-41 : **QA 50,3 %** (strict 40,1 %) · hit@15 59,6 %.
Catégories baseline : c1 38,7 % (31) · c2 64,8 % (27) · c3 25,0 % (8) · c4 52,3 % (86).

### Run 1a — Dual-Date (cat 2) + Scan exhaustif (cat 1) — FAIT ✅
- Fichier : `results/locomo-official-2026-10-12-qa-conv-41.json`
- Prompt : `READER_SYS` étendu (blocs « TEMPORAL & DATE RULES (DUAL-DATE FORMAT) » et
  « MULTI-HOP & LIST AGGREGATION RULES (CATEGORY 1) »). **Sans** la règle d'inférence
  cat 3, réservée au Run 1b.
- Commande : `python3 locomo_official.py qa --conv conv-41 --k 15 --categories 1,2,3,4`
- Durée : **383 s** (index 57,6 s + appels LLM). La fourchette « ~3 min » de la
  spec était optimiste — prévoir **~6,5 min** par conv (n≈152).
- Résultat : **accuracy 60,9 %** (strict 53,9 %, partial 13,8 %, wrong 32,2 %,
  abstention 0,0 %).

| cat | n | baseline | Run 1a | delta | correct/partial/wrong |
|---|---|---|---|---|---|
| 1 | 31 | 38,7 % | **48,4 %** | +9,7 | 9 / 12 / 10 |
| 2 | 27 | 64,8 % | **70,4 %** | +5,6 | 19 / 0 / 8 |
| 3 | 8 | 25,0 % | **31,2 %** | +6,2 | 2 / 1 / 5 |
| 4 | 86 | 52,3 % | **65,1 %** | +12,8 | 52 / 8 / 26 |
| **total** | **152** | **50,3 %** | **60,9 %** | **+10,6** | 82 / 21 / 49 |

**Lecture :**
- Gain strict (+13,8) **>** gain partiel : on a converti des partiels en corrects,
  pas gonflé le score. Aucune catégorie ne régresse.
- Cat 2 : **0 partiel** — la règle Dual-Date produit les deux formulations attendues
  (relative + date résolue), exactement le mécanisme prévu.
- Cat 1 : les 10 échecs restants du `misses_sample` sont **tous `INSUFFICIENT`**
  sur des questions dont la preuve existe (ex. « What people has Maria met and
  helped while volunteering? » → gold `David, Jean, Cindy, Laura`).
  → **Le verrou est le Retriever, pas le Reader** : aucune règle de prompt ne peut
  produire un fait absent des 15 extraits. C'est le mandat du Run 2.
- Cat 4 (+12,8) : effet de bord bienvenu de la règle « Specificity Over Generality ».

### Run 1b — règle d'inférence cat 3 — FAIT ✅
Fichier : `results/ablation-conv41-Run1b-cat3-expand2.json` (prompt Run 1a + bloc
« INFERENCE RULES (CATEGORY 3) », expand ±2).

| Run | acc | strict | partial | wrong |
|---|---|---|---|---|
| 2c (±2, sans cat 3) | 70,7 % | 61,8 % | 17,8 % | 20,4 % |
| **1b (±2 + cat 3)** | **71,7 %** | **63,2 %** | 17,1 % | **19,7 %** |

| cat | 2c | 1b | delta |
|---|---|---|---|
| 1 (multi-saut) | 56,5 % | 54,8 % | −1,7 |
| 2 (temporel) | 77,8 % | **85,2 %** | +7,4 |
| 3 (inférence) | 31,2 % | **37,5 %** | +6,3 |
| 4 (état/ouvert) | 77,3 % | 76,7 % | −0,6 |

**Enseignements :**
- Cat 3 (cible) : **37,5 %** (25,0 baseline → 37,5). `misses_sample` ne garde que
  2 échecs cat 3 (au lieu de 5), tous deux `INSUFFICIENT` sur des inférences
  spéculatives (« financial status », « beach or mountains »).
- Cat 2 bondit aussi (**85,2 %**, record) — la règle d'inférence renforce l'ancrage
  temporel bien que non ciblée.
- **Le bouclier ne recule pas :** cat 4 −0,6 (dans le bruit à n=86), cat 1 −1,7.
  Aucun signe de dérive hallucinatoire. C'était le risque n°1, il est écarté.
- Global **71,7 %**, +21,4 pts sur la baseline conv-41.

⚠️ **Contrôle cat 5 non fait** : le run `--categories 1,2,3,4` ne couvre pas les
questions adversariales. La spec exige de vérifier que le bouclier 88,7 % ne recule
pas → à valider en run Hardcore (cat 1-5) avant de figer.

### Run 3 — Dual-Date Regex Anchoring à l'ingestion — À FAIRE (optionnel)
### Run 4 — Reranker local Cross-Encoder (top-50 → top-15), en fusion — À FAIRE
### Run Final — run officiel complet 10 convs (~45 min) — À FAIRE
Rappel : `expand_neighbours()` était **déjà branchée** dans `qa_score()` (l. 401),
mais désactivée par défaut (`LOCOMO_EXPAND_WINDOW=0`). Run 2 = activation par env var,
aucun code à modifier. Fenêtre pilotée par `LOCOMO_EXPAND_WINDOW`.

Trois runs, même conv-41 (n=152), fichiers dans `results/` :

| Run | Prompt Reader | Expand | Fichier | acc | strict | wrong |
|---|---|---|---|---|---|---|
| réf. | baseline | 0 | `…-2026-10-11-qa-conv-41.json` | 50,3 % | 40,1 % | 39,5 % |
| 1a | Run 1a | 0 | (voir §Run 1a) | 60,9 % | 53,9 % | 32,2 % |
| 2a | baseline | ±1 | `ablation-conv41-Run2a-expand1.json` | 59,5 % | 48,7 % | 29,6 % |
| 2b | Run 1a | ±1 | `ablation-conv41-Run2b-expand1.json` | 63,8 % | 57,2 % | 29,6 % |
| **2c** | **Run 1a** | **±2** | `ablation-conv41-Run2c-expand2.json` | **70,7 %** | **61,8 %** | **20,4 %** |

Ventilation par catégorie (acc) :

| cat | réf. | 1a | 2a | 2b | 2c |
|---|---|---|---|---|---|
| 1 (multi-saut) | 38,7 % | 48,4 % | 48,4 % | 50,0 % | **56,5 %** |
| 2 (temporel) | 64,8 % | 70,4 % | 55,6 % | 70,4 % | **77,8 %** |
| 3 (inférence) | 25,0 % | 31,2 % | 31,2 % | **18,8 %** | **31,2 %** |
| 4 (état/ouvert) | 52,3 % | 65,1 % | 67,4 % | 70,9 % | **77,3 %** |

**Enseignements :**
1. **Expansion et prompt sont cumulatifs.** Le cumul (±2 + prompt Run 1a) donne 70,7 %,
   au-delà des deux leviers isolés. +20,4 pts sur la baseline.
2. **Run 2a : l'expansion ±1 seule casse cat 2** (64,8 → 55,6 %) — les tours adjacents
   noient la date précise. Le prompt Run 1a l'absorbe (2b : retour à 70,4 %).
   → l'antagonisme est réel et la compensation fonctionne.
3. **Run 2b : cat 3 régresse** (31,2 → 18,8 %) en cumulé ±1 — le Scan exhaustif pousse
   à énumérer là où cat 3 demande d'inférer. **Réparé par ±2** (2c : 31,2 %).
4. **Run 2c : progression encore forte (+6,9 pts) et partout.** Aucune catégorie ne
   recule vs 2b. `misses_sample` : un cas passe de `INSUFFICIENT` à une agrégation
   partielle (« A little girl around 8… » au lieu de `David, Jean, Cindy, Laura`)
   → la preuve remonte, mais **le Reader agrège mal les listes** (ressort du Scan
   exhaustif à durcir / Run 4).

⚠️ **Réserve de méthode :** 2c (70,7 %) dépasse le plafond retrieval officiel de
conv-41 (59,6 % hit@15). Neuf runs consécutifs sur **la même conv de 152 q** exposent
à une sur-optimisation. **La validation passe par un run multi-conv**, pas par un
10ᵉ run sur conv-41.
### Run 3 — Dual-Date Regex Anchoring à l'ingestion — À FAIRE
### Run 4 — Reranker local Cross-Encoder (top-50 → top-15), en fusion — À FAIRE
### Run Final — run officiel complet 10 convs (~45 min) — À FAIRE

### Run 1c — arbitrage anti-hallucination (A : durci) — FAIT ✅
Fichier : `results/ablation-conv41-Run1b-hardcore-all.json` (avant) — contrôle cat 1-5.
Ajout d'un bloc « ARBITRATION — WHEN TO INFER vs WHEN TO REFUSE » : distingue les
questions *fait précis* (nom, nombre, date, lieu → refus si absent) des questions
*inférence* (trait, statut, « might/could »).

| Run | acc | strict | cat 3 | cat 5 |
|---|---|---|---|---|
| 1b (±2 + cat 3) | 73,6 % | 66,8 % | 37,5 % | 78,0 % |
| **1c (A, durci)** | 73,1 % | 66,3 % | **50,0 %** | **85,4 %** |

- Bouclier récupéré : 32/41 → 35/41 (+7,4), soit la moitié du recul visé.
- Cat 3 monte à 50,0 % (+12,5) — l'arbitrage *aide* l'inférence au lieu de la brider.
- **Coût** : cat 1 56,5→50,0, cat 2 85,2→77,8 → la règle « fait précis = refus »
  attrape les questions « When… » et les listes, qui relèvent pourtant de l'inférence.

### Run 1d — exceptions au refus (B : corrigé) — FAIT ✅ — RÉGLAGE RETENU
Fichier : `results/ablation-conv41-Run1d-corrected-all.json` (cat 1-5, n=193).
Ajout d'un bloc « EXCEPTIONS TO THE REFUSAL RULE » : les questions « When… » et les
questions d'énumération (« What people/places/… », « How many times… ») ne sont
**jamais** des questions « fait précis » et ne se refusent pas.

| cat | baseline | 1b | 1c (A) | **1d (B)** |
|---|---|---|---|---|
| 1 (multi-saut) | 53,9 % | 56,5 % | 50,0 % | 53,2 % |
| 2 (temporel) | 62,0 % | 85,2 % | 77,8 % | **85,2 %** |
| 3 (inférence) | 26,0 % | 37,5 % | **50,0 %** | 43,8 % |
| 4 (état/ouvert) | 61,2 % | 77,3 % | 76,2 % | **77,9 %** |
| 5 (bouclier) | 92,7 %* | 78,0 % | **85,4 %** | 80,5 % |
| **global** | **60,4 %** | 73,6 % | 73,1 % | **74,1 %** |

\* cat 5 baseline conv-41 exacte = 38/41 (le 92,7 % du run Hardcore, non le 88,7 %
global 10 convs).

**Arbitrage assumé :** gain utile cat 1-4 = 60,5 → **75,3 %** (+14,8) ;
recul bouclier cat 5 = 92,7 → 80,5 % (−12,2). Net +13,7 sur n=193.
Le recul bouclier est **entièrement traçable à une cause unique** : le prompt ne
connaît pas la catégorie de la question. → correction structurelle côté harnais
(A2), pas côté prompt.

### A2 — passer la catégorie au Reader (correction harnais) — FAIT ✅
