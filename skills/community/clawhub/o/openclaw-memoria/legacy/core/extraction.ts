/**
 * 🧠 Memoria — Fact extraction logic
 * 
 * This module exports:
 *   - LLM_EXTRACT_PROMPT — the master prompt for LLM-based fact extraction
 *   - parseJSON() — safe JSON parser for LLM outputs (handles fences, trailing commas)
 *   - normalizeCategory() — map free-form category → canonical category
 */

// ─── Extraction Prompt ───

export const LLM_EXTRACT_PROMPT = `Tu es un extracteur de faits pour un système de mémoire AI.
Analyse le texte et extrais les faits qui méritent d'être retenus.

DEUX TYPES de faits:
- "semantic" = vérité durable, processus appris, configuration, règle découverte
- "episodic" = événement daté, état temporaire, action en cours, résultat observé

RÈGLE D'OR: TOUJOURS INCLURE LES DÉTAILS CONCRETS
Imagine que tu notes pour une secrétaire qui doit pouvoir tout retrouver plus tard.
❌ "Neto a eu une réunion importante" → MANQUE: avec qui? quand? sur quoi?
✅ "Neto a eu une réunion avec le client CCOG le 28/03 à 14h sur la refonte du site"
❌ "Sol a été redémarré" → MANQUE: pourquoi? quel était le problème?
✅ "Sol a été redémarré le 28/03 à 18h25 car better-sqlite3 était compilé pour la mauvaise version de Node (137 vs 141). Fix: npm rebuild"
❌ "Une réflexion excellente a été faite" → MANQUE: quelle réflexion? quel contenu?
✅ "Neto propose que la mémoire fonctionne comme un cerveau humain: ne rien supprimer, prioriser par usage, les détails éphémères (heure d'un vol) s'effacent mais l'expérience (le vol était long) reste"

EXTRAIRE — tout ce qui a du contenu:
✅ Processus appris avec les étapes ("pour migrer SQLite WAL: VACUUM INTO au lieu de cp")
✅ Ce qui a marché ET pourquoi ("le fallback chain résout les crashes car Ollama tombe parfois")
✅ Leçons d'erreurs avec la cause ("api.config ≠ api.pluginConfig → configs ignorées")
✅ Décisions avec la raison ("on utilise qwen3.5:4b car meilleure qualité JSON, avec think:false")
✅ Configs exactes ("Memoria: recallLimit=8, extract LLM qwen3.5:4b, fallback gemma3:4b")
✅ Résultats avec chiffres ("Benchmark: retrieval 92% (11/12), RAG 25%, bottleneck = modèle local")
✅ Préférences avec contexte ("Neto veut du step-by-step, une feature à la fois avec validation")
✅ États temporaires AVEC CONTEXTE ("Sol est en train de refaire HydroTrack — blocker: API endpoint changé")
✅ Événements avec date ET détail ("28/03 — Memoria v3.13.0 live: lifecycle fresh/settled/dormant, 385f/90s/0d")
✅ Ce que quelqu'un fait en ce moment ET pourquoi ("Sol travaille sur la refonte HydroTrack depuis le 26/03, priorité car le client attend la démo")
✅ Outils internes et leur état ("Memoria v3.13.0: lifecycle humain, curseur détail 1-10, 475 facts, publié ClawHub + GitHub")
✅ Produits/MVPs et leur avancement ("Bureau module CA v1.2.0 en prod, matching auto Qonto↔projets fonctionnel")

GÉNÉRALISER — quand un pattern se répète:
🔄 Même problème 2+ fois → stocker la RÈGLE + les cas concrets
   "Les commandes brew/nvm (npm, ollama, node) ne sont pas dans le PATH en SSH non-interactif — fix: source ~/.zprofile ou chemin complet /opt/homebrew/bin/"

🔥 ERREURS ET DANGERS — PRIORITÉ MAXIMALE (comme toucher du feu):
Quand quelque chose a causé un PROBLÈME RÉEL (crash, perte de données, service mort, bug en prod, Neto qui doit intervenir physiquement):
→ Catégorie "erreur", confidence 0.95+
→ Inclure: CE QUI S'EST PASSÉ + POURQUOI c'est dangereux + CE QU'IL NE FAUT JAMAIS REFAIRE + L'ALTERNATIVE SÛRE
→ C'est comme un panneau "DANGER" : on le note dès la PREMIÈRE FOIS, pas après la 2ème brûlure
Exemples de VRAIS dangers à capter:
✅ "NE JAMAIS utiliser openclaw gateway stop via exec — tue le daemon sans le relancer, gateway reste mort. Utiliser gateway restart (SIGUSR1)." (catégorie erreur)
✅ "NE JAMAIS faire cp sur une DB SQLite en mode WAL — données perdues. Utiliser VACUUM INTO." (catégorie erreur)
✅ "NE JAMAIS push sur main sans test — régression garantie. Toujours une branche séparée." (catégorie erreur)
Signaux qu'un fait est un DANGER:
- Quelqu'un dit "ne fais plus ça", "c'est la 2ème fois", "putain", "j'ai dû aller faire X manuellement"
- Un service/outil est mort/cassé après une action
- Un rollback ou fix manuel a été nécessaire
- Le mot "jamais", "interdit", "critique", "ne pas" dans la conversation

NE PAS STOCKER:
❌ Confirmations vides ("ok", "merci", "compris")
❌ Narration pure sans résultat ("je lis le fichier", "je regarde le code")
❌ MÉTA-FAITS sur le stockage lui-même ("le nouveau fait complète l'ancien", "ce fait a été ajouté")
❌ Faits sans AUCUN élément concret ("des informations ont été fournies", "la configuration a été mise à jour")

QUALITÉ — chaque fait DOIT:
⚠️ Contenir au moins UN élément concret: nom propre, chiffre, commande, version, ou date
⚠️ Être AUTONOME = compréhensible seul, sans contexte
⚠️ Inclure le POURQUOI ou le CONTEXTE quand c'est pertinent (pas juste QUOI)
⚠️ Ne JAMAIS commencer par "Le nouveau fait..." ou "Ce fait..." → commencer par le SUJET réel

Règles:
- Phrase(s) complète(s) et autonome(s)
- Pour les PROCÉDURES: garder les étapes ensemble en UN fait (2-4 phrases OK)
- UN FAIT PAR ENTITÉ — si le texte parle de 3 sujets distincts, 3 faits séparés
- Catégories: savoir, erreur, preference, outil, chronologie, rh, client
- type: "semantic" ou "episodic"
- confidence: 0.7 minimum
- Maximum {MAX_FACTS} faits
- Si rien de concret → {"facts": []}

Texte:
"{TEXT}"

JSON valide uniquement:
{"facts": [{"fact": "phrase", "category": "...", "type": "semantic|episodic", "confidence": 0.X}]}`;

// ─── JSON Parse Helper ───

/** Safely parse JSON from LLM output. Handles markdown code fences, trailing commas, and partial JSON. */
export function parseJSON(text: string): unknown {
  // Strip markdown code blocks (```json ... ``` or ``` ... ```)
  let cleaned = text.trim();
  if (cleaned.startsWith("```")) {
    const lines = cleaned.split("\n");
    lines.shift(); // remove opening ```json or ```
    if (lines[lines.length - 1]?.trim() === "```") lines.pop();
    cleaned = lines.join("\n").trim();
  }
  // Try to extract JSON object/array via regex
  const match = cleaned.match(/(\{[\s\S]*\}|\[[\s\S]*\])/);
  if (match) cleaned = match[1];
  return JSON.parse(cleaned);
}

// ─── Category Normalization ───

const VALID_CATEGORIES = new Set(["savoir", "erreur", "preference", "outil", "chronologie", "rh", "client"]);

/**
 * Normalize free-form LLM category output → one of 7 canonical categories.
 * Mapping: architecture/mécanisme → savoir, sévérité/bug → erreur, financier → client, etc.
 * Unknown categories default to "savoir".
 */
export function normalizeCategory(raw: string): string {
  const lower = (raw || "savoir").toLowerCase().trim();
  if (VALID_CATEGORIES.has(lower)) return lower;
  // Common LLM variants → map to valid
  if (lower === "préférence" || lower === "préférences") return "preference";
  if (lower === "architecture" || lower === "mécanisme" || lower === "stock" || lower === "état") return "savoir";
  if (lower === "financier") return "client";
  if (lower === "sévérité" || lower === "bug") return "erreur";
  return "savoir"; // fallback: anything unknown → savoir
}
