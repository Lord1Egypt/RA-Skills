#!/usr/bin/env node

/**
 * humanize-de.js – Deutscher KI-Text-Detektor (CLI)
 *
 * Befehle:
 *   score <datei>     Berechnet den KI-Score (0-100)
 *   analyze <datei>   Detaillierte Analyse mit allen Signalen
 *   suggest <datei>   Zeigt Ersetzungsvorschläge
 *   fix <datei>       Automatische Tier-1-Ersetzungen (schreibt neue Datei)
 *
 * Nur fs und path als Dependencies. Kein Netzwerk. Alles lokal.
 *
 * Autor: OpenClaw
 * Lizenz: MIT
 */

const fs = require('fs');
const path = require('path');

// ============================================================
//  DATENBANKEN
// ============================================================

/**
 * Tier 1 – VERBOTEN (immer ersetzen, +3 Punkte pro Treffer)
 * Format: [KI-Wort, Ersetzungsvorschlag]
 */
/**
 * Wortart-Kuerzel fuer morphologisches Fix:
 *   'adj'   → Adjektiv: Suffix-Matching -e/-en/-em/-er/-es
 *   'noun'  → Substantiv: Genitiv-s, Plural -e/-en, Dativ -en (nur sichere Faelle)
 *   'verb'  → Verb: nur Infinitiv ersetzen (kein Konjugations-Matching)
 *   'adv'   → Adverb: keine Flexion, 1:1 ersetzen
 *   'phrase' → Mehrwort: 1:1 ersetzen
 *
 * Format: [KI-Wort, Ersetzung, Wortart]
 */
const TIER1 = [
  // Adjektive (Suffix-Matching aktiv)
  ['grundlegend', 'wichtig', 'adj'],
  ['nahtlos', 'reibungslos', 'adj'],
  ['robust', 'stabil', 'adj'],
  ['skalierbar', 'erweiterbar', 'adj'],
  ['ganzheitlich', 'umfassend', 'adj'],
  ['bahnbrechend', 'wichtig', 'adj'],
  ['wegweisend', 'einflussreich', 'adj'],
  ['transformativ', 'verändernd', 'adj'],
  ['synergetisch', 'ergänzend', 'adj'],
  ['facettenreich', 'vielseitig', 'adj'],
  ['unschätzbar', 'sehr wertvoll', 'adj'],
  ['eingebettet', 'integriert', 'adj'],
  ['herausragend', 'stark', 'adj'],
  ['maßgeblich', 'stark', 'adj'],
  ['tiefgreifend', 'spürbar', 'adj'],
  ['unverzichtbar', 'nötig', 'adj'],
  ['überwältigend', 'stark', 'adj'],
  ['federführend', 'führend', 'adj'],
  ['richtungsweisend', 'wichtig', 'adj'],
  ['zukunftsweisend', 'vorausschauend', 'adj'],
  ['beispiellos', 'einmalig', 'adj'],
  ['außerordentlich', 'besonders', 'adj'],
  ['umfassend', 'vollständig', 'adj'],
  ['vielfältig', 'verschieden', 'adj'],
  ['lebendig', 'aktiv', 'adj'],
  ['entscheidend', 'wichtig', 'adj'],
  ['bemerkenswert', 'auffällig', 'adj'],
  // Adverbien (keine Flexion)
  ['hochgradig', 'sehr', 'adv'],
  ['zweifellos', 'sicher', 'adv'],
  ['unbestreitbar', 'klar', 'adv'],
  // Substantive (Genitiv-s, Plural, Dativ)
  // Format: [Wort, Ersetzung, 'noun', {from: Genus-Original, to: Genus-Ersetzung}]
  // Genus: 'm' = maskulin, 'f' = feminin, 'n' = neutrum
  // Genus-Feld nur noetig wenn sich das Genus aendert (fuer Artikel-Korrektur)
  ['Eckpfeiler', 'Basis', 'noun', {from: 'm', to: 'f'}],
  ['Katalysator', 'Antrieb', 'noun'],
  ['Tapisserie', 'Geflecht', 'noun', {from: 'f', to: 'n'}],
  ['Wandteppich', 'Geflecht', 'noun', {from: 'm', to: 'n'}],
  ['Paradigmenwechsel', 'Umdenken', 'noun', {from: 'm', to: 'n'}],
  ['Meilenstein', 'wichtiger Schritt', 'noun'],
  ['Wendepunkt', 'Umbruch', 'noun'],
  ['Schlüsselrolle', 'wichtige Rolle', 'noun'],
  ['Vorreiter', 'Pionier', 'noun'],
  ['Brennpunkt', 'Schwerpunkt', 'noun'],
  ['Paradigma', 'Denkmodell', 'noun'],
  ['Landschaft', 'Bereich', 'noun', {from: 'f', to: 'm'}],
  // Verben (nur Infinitiv)
  ['ermächtigen', 'in die Lage versetzen', 'verb'],
  ['befähigen', 'helfen', 'verb'],
  ['eintauchen', 'anschauen', 'verb'],
];

/**
 * Tier 2 – SPARSAM (max 1x pro 500 Wörter, +1 Punkt über Limit)
 */
const TIER2 = [
  'darüber hinaus', 'des Weiteren', 'zudem', 'nuanciert',
  'erleichtern', 'beleuchten', 'umfassen', 'proaktiv',
  'wesentlich', 'darauf abzielen', 'in der Lage sein',
  'ermöglichen', 'gewährleisten', 'berücksichtigen',
  'Aspekt', 'Kontext', 'relevant', 'optimieren',
  'implementieren', 'integrieren', 'adressieren',
  'transparent', 'signifikant', 'elementar', 'essenziell',
  'komplex', 'Potenzial', 'effektiv', 'effizient',
  // Erweiterung v1.1 (Session 48)
  'nutzerorientiert', 'datengetrieben', 'zukunftsfähig',
  'evidenzbasiert', 'praxiserprobt', 'niedrigschwellig',
  'Handlungsempfehlung', 'Zielsetzung', 'Fragestellung',
  'Problemstellung', 'Herangehensweise', 'Gegebenheiten',
  'fungieren', 'aufweisen', 'darstellen', 'verorten',
];

/**
 * Verbotene Phrasen (+4 Punkte pro Treffer)
 */
const VERBOTENE_PHRASEN = [
  'es ist wichtig zu beachten',
  'nicht nur... sondern auch',
  'nicht nur',
  'in der heutigen welt',
  'in einer welt, in der',
  'in einer welt in der',
  'lass uns ehrlich sein',
  'um ehrlich zu sein',
  'darüber hinaus',
  'des weiteren',
  'ermöglicht es',
  'bietet die möglichkeit',
  'grundlegend anders',
  'im kern',
  'im grunde',
  'zusammenfassend lässt sich sagen',
  'es lässt sich festhalten',
  'abschließend sei gesagt',
  'wie bereits erwähnt',
  'an dieser stelle sei erwähnt',
  'es sei darauf hingewiesen',
  'in anbetracht der tatsache',
  'aufgrund der tatsache',
  'im folgenden wird erläutert',
  'es gilt zu beachten',
  'nicht zuletzt',
  'zu guter letzt',
  'last but not least',
  // Erweiterung v1.1 (Session 48)
  'in diesem zusammenhang',
  'vor dem hintergrund',
  'im rahmen von',
  'unter berücksichtigung',
  'es zeigt sich, dass',
  'es zeigt sich dass',
  'es wird deutlich, dass',
  'es wird deutlich dass',
  'eine vielzahl von',
  'eine reihe von',
  'einen wesentlichen beitrag',
  'im hinblick auf',
  'hinsichtlich',
  'dies unterstreicht',
  'es bleibt abzuwarten',
  'es bleibt spannend',
  'die zukunft wird zeigen',
  'spielt eine entscheidende rolle',
  'von entscheidender bedeutung',
  'stellt einen wichtigen schritt dar',
];

/**
 * Chatbot-Artefakte (+5 Punkte pro Treffer)
 */
const CHATBOT_ARTEFAKTE = [
  'tolle frage',
  'gute frage',
  'hervorragende frage',
  'ausgezeichnete frage',
  'ich hoffe, das hilft',
  'ich hoffe das hilft',
  'lass mich wissen',
  'lassen sie mich wissen',
  'gerne!',
  'natürlich!',
  'selbstverständlich!',
  'da haben sie völlig recht',
  'da hast du völlig recht',
  'stand meiner letzten schulung',
  'soweit mir bekannt',
  'zum zeitpunkt meines wissens',
];

// ============================================================
//  HILFSFUNKTIONEN
// ============================================================

/**
 * Text in Sätze aufteilen (einfache Heuristik)
 */
function splitSentences(text) {
  // Sätze an . ! ? trennen, aber nicht bei Abkürzungen wie "z.B." oder "etc."
  const raw = text.replace(/([.!?])\s+/g, '$1\n').split('\n');
  return raw
    .map(s => s.trim())
    .filter(s => s.length > 0 && s.split(/\s+/).length >= 1);
}

/**
 * Wörter aus Text extrahieren (lowercase, ohne Satzzeichen)
 */
function tokenize(text) {
  return text
    .toLowerCase()
    .replace(/[^\wäöüß\s-]/g, ' ')
    .split(/\s+/)
    .filter(w => w.length > 0);
}

/**
 * Standardabweichung berechnen
 */
function stddev(arr) {
  const n = arr.length;
  if (n === 0) return 0;
  const mean = arr.reduce((a, b) => a + b, 0) / n;
  const variance = arr.reduce((sum, val) => sum + (val - mean) ** 2, 0) / n;
  return Math.sqrt(variance);
}

/**
 * Mittelwert berechnen
 */
function mean(arr) {
  if (arr.length === 0) return 0;
  return arr.reduce((a, b) => a + b, 0) / arr.length;
}

// ============================================================
//  ANALYSE-FUNKTIONEN
// ============================================================

/**
 * Adjektiv-Suffixe fuer morphologisches Matching.
 * Deutsche Adjektive koennen diese Endungen haben: -e, -en, -em, -er, -es.
 * Optional: Grundform ohne Suffix (praedikativ: "das ist wichtig").
 */
const ADJ_SUFFIXES = '(?:es|en|em|er|e)?';

/**
 * Substantiv-Suffixe fuer einfaches morphologisches Matching.
 * Deckt Genitiv-s, Plural -e/-en, Dativ-Plural -en ab.
 * Bewusst konservativ – lieber mal nicht matchen als falsch ersetzen.
 */
const NOUN_SUFFIXES = '(?:s|es|en|e)?';

/**
 * Baut den passenden Regex fuer ein Tier-1-Wort basierend auf Wortart.
 */
function buildTier1Regex(word, type) {
  const escaped = word.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  switch (type) {
    case 'adj':
      return new RegExp(`\\b${escaped}(${ADJ_SUFFIXES})\\b`, 'gi');
    case 'noun':
      return new RegExp(`\\b${escaped}(${NOUN_SUFFIXES})\\b`, 'gi');
    case 'verb':
      // Nur Infinitiv matchen – Konjugation ist zu komplex
      return new RegExp(`\\b${escaped}\\b`, 'gi');
    default: // 'adv', 'phrase'
      return new RegExp(`\\b${escaped}\\b`, 'gi');
  }
}

/**
 * Tier-1-Wörter finden (mit morphologischem Matching)
 */
function findTier1(text) {
  const hits = [];
  for (const [word, replacement, type] of TIER1) {
    const regex = buildTier1Regex(word, type);
    let match;
    while ((match = regex.exec(text)) !== null) {
      const suffix = match[1] || '';
      hits.push({
        word: word,
        matched: match[0],
        replacement: replacement,
        suffix: suffix,
        type: type,
        position: match.index,
        tier: 1,
      });
    }
  }
  return hits;
}

/**
 * Tier-2-Wörter finden und Dichte prüfen
 */
function findTier2(text) {
  const lower = text.toLowerCase();
  const wordCount = tokenize(text).length;
  const maxAllowed = Math.max(1, Math.floor(wordCount / 500));
  const hits = [];

  for (const word of TIER2) {
    const regex = new RegExp(word.toLowerCase().replace(/[.*+?^${}()|[\]\\]/g, '\\$&'), 'gi');
    let count = 0;
    let match;
    while ((match = regex.exec(lower)) !== null) {
      count++;
      if (count > maxAllowed) {
        hits.push({
          word: word,
          position: match.index,
          tier: 2,
          count: count,
          maxAllowed: maxAllowed,
        });
      }
    }
  }
  return hits;
}

/**
 * Verbotene Phrasen finden
 */
function findVerbotenePhrasen(text) {
  const lower = text.toLowerCase();
  const hits = [];
  for (const phrase of VERBOTENE_PHRASEN) {
    const regex = new RegExp(phrase.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'), 'gi');
    let match;
    while ((match = regex.exec(lower)) !== null) {
      hits.push({
        phrase: phrase,
        position: match.index,
      });
    }
  }
  return hits;
}

/**
 * Chatbot-Artefakte finden
 */
function findChatbotArtefakte(text) {
  const lower = text.toLowerCase();
  const hits = [];
  for (const artifact of CHATBOT_ARTEFAKTE) {
    if (lower.includes(artifact)) {
      hits.push({ artifact: artifact });
    }
  }
  return hits;
}

/**
 * Burstiness berechnen
 */
function calcBurstiness(sentences) {
  if (sentences.length < 20) return { value: null, note: 'Zu wenige Sätze (<20)' };
  const lengths = sentences.map(s => tokenize(s).length);
  const m = mean(lengths);
  const s = stddev(lengths);
  if (s + m === 0) return { value: 0, note: 'Alle Sätze gleich lang' };
  return { value: (s - m) / (s + m) };
}

/**
 * Type-Token-Ratio berechnen (gleitendes 100-Wort-Fenster)
 */
function calcTTR(text) {
  const tokens = tokenize(text);
  if (tokens.length < 50) return { value: null, note: 'Zu wenige Wörter (<50)' };

  const windowSize = 100;
  const ttrs = [];

  for (let i = 0; i <= tokens.length - windowSize; i += 50) {
    const window = tokens.slice(i, i + windowSize);
    const unique = new Set(window);
    ttrs.push(unique.size / window.length);
  }

  if (ttrs.length === 0) {
    const unique = new Set(tokens);
    return { value: unique.size / tokens.length };
  }

  return { value: mean(ttrs) };
}

/**
 * Satzlängen-CoV berechnen
 */
function calcCoV(sentences) {
  if (sentences.length < 5) return { value: null, note: 'Zu wenige Sätze (<5)' };
  const lengths = sentences.map(s => tokenize(s).length);
  const m = mean(lengths);
  if (m === 0) return { value: 0 };
  const s = stddev(lengths);
  return { value: s / m };
}

/**
 * Trigramm-Wiederholung berechnen
 */
function calcTrigramRepeat(text) {
  const sentences = splitSentences(text);
  const trigramCounts = {};
  let totalTrigrams = 0;

  for (const sentence of sentences) {
    const tokens = tokenize(sentence);
    for (let i = 0; i < tokens.length - 2; i++) {
      const trigram = `${tokens[i]} ${tokens[i + 1]} ${tokens[i + 2]}`;
      trigramCounts[trigram] = (trigramCounts[trigram] || 0) + 1;
      totalTrigrams++;
    }
  }

  if (totalTrigrams === 0) return { value: 0 };

  const repeated = Object.values(trigramCounts).filter(c => c > 1).length;
  return { value: repeated / totalTrigrams };
}

/**
 * Deutsche Silbenzählung (vereinfacht)
 */
function countSyllablesDE(word) {
  word = word.toLowerCase().replace(/[^a-zäöüß]/g, '');
  if (word.length <= 2) return 1;

  // Diphthonge als 1 Silbe zählen
  let processed = word
    .replace(/ei/g, 'X')
    .replace(/ai/g, 'X')
    .replace(/au/g, 'X')
    .replace(/eu/g, 'X')
    .replace(/äu/g, 'X')
    .replace(/ie/g, 'X');

  const vowels = processed.match(/[aeiouäöüX]/g);
  return vowels ? Math.max(1, vowels.length) : 1;
}

/**
 * Flesch-DE Lesbarkeit berechnen
 */
function calcFleschDE(text) {
  const sentences = splitSentences(text);
  const tokens = tokenize(text);
  if (sentences.length < 3 || tokens.length < 30) {
    return { value: null, note: 'Zu wenig Text für Flesch-Berechnung' };
  }

  const totalSyllables = tokens.reduce((sum, w) => sum + countSyllablesDE(w), 0);
  const avgSentenceLength = tokens.length / sentences.length;
  const avgSyllablesPerWord = totalSyllables / tokens.length;

  // Deutsche Flesch-Formel
  const flesch = 180 - avgSentenceLength - (58.5 * avgSyllablesPerWord);
  return { value: Math.max(0, Math.min(100, flesch)) };
}

/**
 * Co-Occurrence-Sets prüfen (Wort-Cluster in Absätzen)
 */
const CO_OCCURRENCE_SETS = [
  // Set 1: Bedeutungs-Aufblasung
  ['grundlegend', 'maßgeblich', 'entscheidend', 'tiefgreifend', 'bahnbrechend',
   'wegweisend', 'meilenstein', 'wendepunkt', 'paradigmenwechsel'],
  // Set 2: Werbesprache
  ['nahtlos', 'robust', 'skalierbar', 'ganzheitlich', 'umfassend',
   'herausragend', 'innovativ', 'zukunftsweisend'],
  // Set 3: Abstrakte Metaphern
  ['landschaft', 'eckpfeiler', 'katalysator', 'facettenreich',
   'tapisserie', 'eingebettet', 'ökosystem'],
  // Set 4: Aktions-Verben
  ['ermächtigen', 'befähigen', 'ermöglichen', 'gewährleisten',
   'erleichtern', 'optimieren', 'implementieren', 'integrieren'],
  // Set 5: Übergangs-Füller
  ['darüber hinaus', 'des weiteren', 'zudem', 'nicht zuletzt',
   'abschließend', 'zusammenfassend', 'im folgenden'],
  // Set 6: Anglizismen-Cluster (v1.1)
  ['benchmark', 'best practice', 'use case', 'alignment', 'empowerment',
   'impact', 'leverage', 'onboarding', 'upskilling', 'gamechanger'],
  // Set 7: Nominalstil-Cluster (v1.1)
  ['zielsetzung', 'fragestellung', 'problemstellung',
   'handlungsempfehlung', 'herangehensweise', 'gegebenheiten'],
];

function findCoOccurrences(text) {
  // Absätze trennen
  const paragraphs = text.split(/\n\s*\n/).filter(p => p.trim().length > 0);
  const alarms = [];

  for (let pi = 0; pi < paragraphs.length; pi++) {
    const lower = paragraphs[pi].toLowerCase();
    for (let si = 0; si < CO_OCCURRENCE_SETS.length; si++) {
      const matches = CO_OCCURRENCE_SETS[si].filter(word => lower.includes(word));
      if (matches.length >= 3) {
        alarms.push({
          paragraph: pi + 1,
          set: si + 1,
          matches: matches,
          count: matches.length,
        });
      }
    }
  }
  return alarms;
}

/**
 * Personality-Bonus berechnen
 */
function calcPersonalityBonus(text) {
  let bonus = 0;
  const details = [];

  // Einschübe in Klammern
  const klammerMatches = text.match(/\([^)]{5,60}\)/g);
  if (klammerMatches && klammerMatches.length > 0) {
    bonus -= 3;
    details.push(`Einschübe in Klammern: ${klammerMatches.length}x (-3)`);
  }

  // Satzrhythmus prüfen
  const sentences = splitSentences(text);
  const lengths = sentences.map(s => tokenize(s).length);
  let monotone = false;
  for (let i = 0; i < lengths.length - 2; i++) {
    if (Math.abs(lengths[i] - lengths[i + 1]) < 3 &&
        Math.abs(lengths[i + 1] - lengths[i + 2]) < 3) {
      monotone = true;
      break;
    }
  }
  if (!monotone && sentences.length >= 5) {
    bonus -= 5;
    details.push('Satzrhythmus variiert (-5)');
  }

  // Kontraktionen
  const kontraktionen = text.match(/\b(gibt's|ist's|hat's|geht's|war's|kann's|muss's|werd's|wär's|hätt's)\b/gi);
  if (kontraktionen && kontraktionen.length > 0) {
    bonus -= 2;
    details.push(`Kontraktionen: ${kontraktionen.length}x (-2)`);
  }

  // Konkrete Zahlen
  const zahlen = text.match(/\d+[.,]?\d*\s*(%|€|\$|Prozent|Euro|Dollar|Stunden|Tage|Wochen|Monate|Jahre)/g);
  if (zahlen && zahlen.length >= 2) {
    bonus -= 3;
    details.push(`Konkrete Zahlen/Einheiten: ${zahlen.length}x (-3)`);
  }

  // Satzfragmente (Sätze unter 4 Wörtern)
  const fragmente = sentences.filter(s => tokenize(s).length <= 3 && tokenize(s).length > 0);
  if (fragmente.length > 0) {
    bonus -= 2;
    details.push(`Satzfragmente: ${fragmente.length}x (-2)`);
  }

  return { bonus, details };
}

// ============================================================
//  GEDANKENSTRICH-ERKENNUNG (Muster #13)
// ============================================================

/**
 * Zählt En-Dashes (–) im Fließtext.
 * Ignoriert:
 *   - QR-Code-Platzhalter: [QR-CODE: ID – Beschreibung]
 *   - Code-Blöcke (``` ... ```)
 *   - Inline-Code (`...`)
 * Regel aus ki-muster.md: >3 pro ~250 Wörter = HOCH (+5 Punkte pro Überschreitung)
 */
function countGedankenstriche(text) {
  // Code-Blöcke entfernen
  let cleaned = text.replace(/```[\s\S]*?```/g, '');
  // Inline-Code entfernen
  cleaned = cleaned.replace(/`[^`]+`/g, '');
  // QR-Code-Platzhalter entfernen
  cleaned = cleaned.replace(/\[QR-CODE:[^\]]*\]/g, '');

  // Alle En-Dashes im bereinigten Text finden
  const matches = cleaned.match(/–/g);
  const total = matches ? matches.length : 0;

  // Wörter zählen für Dichte-Berechnung
  const words = tokenize(cleaned).length;
  const pages = Math.max(1, Math.round(words / 250));
  const perPage = words > 0 ? total / pages : 0;

  // Schwelle: >3 pro 250 Wörter
  const threshold = pages * 3;
  const excess = Math.max(0, total - threshold);

  return {
    total,
    words,
    pages,
    perPage: perPage.toFixed(1),
    threshold,
    excess,
  };
}

// ============================================================
//  SCORE-BERECHNUNG
// ============================================================

function calculateScore(text) {
  let score = 0;
  const report = {
    tier1: [],
    tier2: [],
    phrasen: [],
    chatbot: [],
    gedankenstriche: {},
    statistik: {},
    coOccurrence: [],
    personality: {},
    details: [],
  };

  // Tier 1
  const t1 = findTier1(text);
  report.tier1 = t1;
  score += t1.length * 3;
  if (t1.length > 0) report.details.push(`Tier-1-Wörter: ${t1.length}x (+${t1.length * 3})`);

  // Tier 2
  const t2 = findTier2(text);
  report.tier2 = t2;
  score += t2.length * 1;
  if (t2.length > 0) report.details.push(`Tier-2-Überschuss: ${t2.length}x (+${t2.length})`);

  // Verbotene Phrasen
  const vp = findVerbotenePhrasen(text);
  report.phrasen = vp;
  score += vp.length * 4;
  if (vp.length > 0) report.details.push(`Verbotene Phrasen: ${vp.length}x (+${vp.length * 4})`);

  // Chatbot-Artefakte
  const ca = findChatbotArtefakte(text);
  report.chatbot = ca;
  score += ca.length * 5;
  if (ca.length > 0) report.details.push(`Chatbot-Artefakte: ${ca.length}x (+${ca.length * 5})`);

  // Gedankenstriche (Muster #13)
  const gs = countGedankenstriche(text);
  report.gedankenstriche = gs;
  if (gs.excess > 0) {
    const gsScore = Math.min(gs.excess * 5, 25); // Max +25 Punkte (Cap)
    score += gsScore;
    report.details.push(`Gedankenstriche: ${gs.total}x in ~${gs.pages} Seite(n), ${gs.perPage}/Seite (Limit 3/Seite → ${gs.excess} über Limit → +${gsScore})`);
  }

  // Statistik
  const sentences = splitSentences(text);

  const burstiness = calcBurstiness(sentences);
  report.statistik.burstiness = burstiness;
  if (burstiness.value !== null && burstiness.value < 0.3) {
    score += 10;
    report.details.push(`Burstiness: ${burstiness.value.toFixed(3)} (<0.3 → +10)`);
  }

  const ttr = calcTTR(text);
  report.statistik.ttr = ttr;
  if (ttr.value !== null && ttr.value < 0.5) {
    score += 5;
    report.details.push(`TTR: ${ttr.value.toFixed(3)} (<0.5 → +5)`);
  }

  const cov = calcCoV(sentences);
  report.statistik.cov = cov;
  if (cov.value !== null && cov.value < 0.3) {
    score += 5;
    report.details.push(`CoV: ${cov.value.toFixed(3)} (<0.3 → +5)`);
  }

  const trigram = calcTrigramRepeat(text);
  report.statistik.trigram = trigram;
  if (trigram.value > 0.10) {
    score += 5;
    report.details.push(`Trigramm-Rate: ${trigram.value.toFixed(3)} (>0.10 → +5)`);
  }

  // Flesch-DE (Signal 5)
  const flesch = calcFleschDE(text);
  report.statistik.flesch = flesch;
  if (flesch.value !== null && flesch.value >= 40 && flesch.value <= 50) {
    score += 3;
    report.details.push(`Flesch-DE: ${flesch.value.toFixed(1)} (KI-Sweetspot 40–50 → +3)`);
  }

  // Co-Occurrence-Sets
  const coOcc = findCoOccurrences(text);
  report.coOccurrence = coOcc;
  if (coOcc.length > 0) {
    const coOccScore = coOcc.length * 5;
    score += coOccScore;
    report.details.push(`Co-Occurrence-Alarm: ${coOcc.length} Cluster (+${coOccScore})`);
  }

  // Personality Bonus
  const personality = calcPersonalityBonus(text);
  report.personality = personality;
  score += personality.bonus;

  // Clamp
  score = Math.max(0, Math.min(100, score));
  report.score = score;

  return report;
}

// ============================================================
//  BEWERTUNG
// ============================================================

function getBewertung(score) {
  if (score <= 20) return 'Klingt menschlich';
  if (score <= 40) return 'Leicht maschinell';
  if (score <= 60) return 'Gemischt';
  if (score <= 80) return 'Offensichtlich KI';
  return 'ChatGPT-Standard';
}

// ============================================================
//  OUTPUT-FORMATIERUNG
// ============================================================

function formatScore(report) {
  const bewertung = getBewertung(report.score);
  return `\n  SCORE: ${report.score} / 100  →  ${bewertung}\n`;
}

function formatAnalyze(report, text) {
  const lines = [];
  const wordCount = tokenize(text).length;
  const sentenceCount = splitSentences(text).length;

  lines.push('');
  lines.push('═══════════════════════════════════════════');
  lines.push('  HUMANIZER-DE · Analyse-Report');
  lines.push('═══════════════════════════════════════════');
  lines.push('');
  lines.push(`  SCORE: ${report.score} / 100  →  ${getBewertung(report.score)}`);
  lines.push(`  Wörter: ${wordCount} | Sätze: ${sentenceCount}`);
  lines.push('');

  // Tier 1
  lines.push('───────────────────────────────────────────');
  lines.push(`  1. TIER-1-WÖRTER (${report.tier1.length} gefunden, +${report.tier1.length * 3} Pkt)`);
  lines.push('───────────────────────────────────────────');
  if (report.tier1.length === 0) {
    lines.push('  Keine Tier-1-Wörter gefunden. Gut!');
  } else {
    // Deduplizieren
    const seen = new Set();
    for (const hit of report.tier1) {
      const key = hit.word.toLowerCase();
      if (!seen.has(key)) {
        seen.add(key);
        const count = report.tier1.filter(h => h.word.toLowerCase() === key).length;
        lines.push(`  ▸ "${hit.word}" (${count}x) → "${hit.replacement}"`);
      }
    }
  }
  lines.push('');

  // Verbotene Phrasen
  lines.push('───────────────────────────────────────────');
  lines.push(`  2. VERBOTENE PHRASEN (${report.phrasen.length} gefunden, +${report.phrasen.length * 4} Pkt)`);
  lines.push('───────────────────────────────────────────');
  if (report.phrasen.length === 0) {
    lines.push('  Keine verbotenen Phrasen gefunden. Gut!');
  } else {
    const seen = new Set();
    for (const hit of report.phrasen) {
      if (!seen.has(hit.phrase)) {
        seen.add(hit.phrase);
        lines.push(`  ▸ "${hit.phrase}"`);
      }
    }
  }
  lines.push('');

  // Chatbot-Artefakte
  if (report.chatbot.length > 0) {
    lines.push('───────────────────────────────────────────');
    lines.push(`  3. CHATBOT-ARTEFAKTE (${report.chatbot.length} gefunden, +${report.chatbot.length * 5} Pkt)`);
    lines.push('───────────────────────────────────────────');
    for (const hit of report.chatbot) {
      lines.push(`  ▸ "${hit.artifact}"`);
    }
    lines.push('');
  }

  // Gedankenstriche (Muster #13)
  const gs = report.gedankenstriche;
  if (gs && gs.total > 0) {
    lines.push('───────────────────────────────────────────');
    const gsScore = gs.excess > 0 ? Math.min(gs.excess * 5, 25) : 0;
    lines.push(`  4. GEDANKENSTRICHE (${gs.total} gefunden, ${gs.perPage}/Seite, +${gsScore} Pkt)`);
    lines.push('───────────────────────────────────────────');
    if (gs.excess > 0) {
      lines.push(`  ✗ ${gs.total} En-Dashes (–) in ~${gs.pages} Seite(n) → ${gs.excess} über Limit (3/Seite)`);
      lines.push('  KI streut Gedankenstriche wie Konfetti. Ersetze durch Punkt, Komma oder Umformulierung.');
    } else {
      lines.push(`  ✓ ${gs.total} En-Dashes (–) in ~${gs.pages} Seite(n) → im Rahmen`);
    }
    lines.push('');
  }

  // Statistik
  lines.push('───────────────────────────────────────────');
  lines.push('  5. STATISTIK');
  lines.push('───────────────────────────────────────────');

  const b = report.statistik.burstiness;
  if (b.value !== null) {
    const status = b.value >= 0.3 ? '✓ menschlich' : '✗ KI-typisch';
    lines.push(`  Burstiness:       ${b.value.toFixed(3)}  ${status}`);
  } else {
    lines.push(`  Burstiness:       – (${b.note})`);
  }

  const t = report.statistik.ttr;
  if (t.value !== null) {
    const status = t.value >= 0.5 ? '✓ menschlich' : '✗ KI-typisch';
    lines.push(`  TTR:              ${t.value.toFixed(3)}  ${status}`);
  } else {
    lines.push(`  TTR:              – (${t.note})`);
  }

  const c = report.statistik.cov;
  if (c.value !== null) {
    const status = c.value >= 0.3 ? '✓ menschlich' : '✗ KI-typisch';
    lines.push(`  Satzlängen-CoV:   ${c.value.toFixed(3)}  ${status}`);
  } else {
    lines.push(`  Satzlängen-CoV:   – (${c.note})`);
  }

  const tr = report.statistik.trigram;
  const trStatus = tr.value <= 0.10 ? '✓ normal' : '✗ KI-typisch';
  lines.push(`  Trigramm-Rate:    ${tr.value.toFixed(3)}  ${trStatus}`);

  const fl = report.statistik.flesch;
  if (fl && fl.value !== null) {
    const flStatus = (fl.value >= 40 && fl.value <= 50) ? '✗ KI-Sweetspot' : '✓ ok';
    lines.push(`  Flesch-DE:        ${fl.value.toFixed(1)}   ${flStatus}`);
  } else if (fl) {
    lines.push(`  Flesch-DE:        – (${fl.note})`);
  }
  lines.push('');

  // Co-Occurrence
  if (report.coOccurrence && report.coOccurrence.length > 0) {
    lines.push('───────────────────────────────────────────');
    lines.push(`  5b. CO-OCCURRENCE-ALARM (${report.coOccurrence.length} Cluster, +${report.coOccurrence.length * 5} Pkt)`);
    lines.push('───────────────────────────────────────────');
    for (const alarm of report.coOccurrence) {
      lines.push(`  ▸ Absatz ${alarm.paragraph}, Set ${alarm.set}: ${alarm.matches.join(', ')} (${alarm.count} Treffer)`);
    }
    lines.push('');
  }

  // Personality
  lines.push('───────────────────────────────────────────');
  lines.push(`  5. PERSONALITY-BONUS (${report.personality.bonus} Pkt)`);
  lines.push('───────────────────────────────────────────');
  if (report.personality.details.length === 0) {
    lines.push('  Keine menschlichen Stilmittel erkannt.');
  } else {
    for (const d of report.personality.details) {
      lines.push(`  ▸ ${d}`);
    }
  }
  lines.push('');

  // Score-Aufschlüsselung
  lines.push('───────────────────────────────────────────');
  lines.push('  6. SCORE-DETAILS');
  lines.push('───────────────────────────────────────────');
  for (const d of report.details) {
    lines.push(`  ▸ ${d}`);
  }
  lines.push('');
  lines.push('═══════════════════════════════════════════');

  return lines.join('\n');
}

function formatSuggest(report) {
  const lines = [];
  lines.push('');
  lines.push('  ERSETZUNGSVORSCHLÄGE');
  lines.push('  ────────────────────');

  if (report.tier1.length === 0 && report.phrasen.length === 0) {
    lines.push('  Keine Ersetzungen nötig!');
    return lines.join('\n');
  }

  // Tier 1
  const seen = new Set();
  for (const hit of report.tier1) {
    const key = hit.word.toLowerCase();
    if (!seen.has(key)) {
      seen.add(key);
      lines.push(`  "${hit.word}" → "${hit.replacement}"`);
    }
  }

  // Phrasen
  for (const hit of report.phrasen) {
    lines.push(`  "${hit.phrase}" → [streichen oder umschreiben]`);
  }

  lines.push('');
  return lines.join('\n');
}

// ============================================================
//  FIX-FUNKTION
// ============================================================

/**
 * Wendet das Suffix des Originals auf das Ersatzwort an.
 * Behaelt Gross/Kleinschreibung des Originals bei.
 *
 * Beispiele:
 *   applyMorphFix("grundlegendes", "wichtig", "es", "adj") → "wichtiges"
 *   applyMorphFix("Grundlegenden", "wichtig", "en", "adj") → "Wichtigen"
 *   applyMorphFix("Meilensteins", "wichtiger Schritt", "s", "noun") → "Wichtigen Schritts"
 *   applyMorphFix("hochgradig", "sehr", "", "adv") → "sehr"
 */
function applyMorphFix(originalMatch, replacement, suffix, type) {
  let result;

  if (type === 'adj' && suffix) {
    // Adjektiv mit Endung: Suffix an Ersatzwort haengen
    result = replacement + suffix;
  } else if (type === 'noun' && suffix) {
    // Substantiv: Suffix ans letzte Wort der Ersetzung haengen
    // z.B. "wichtiger Schritt" + "s" → "wichtiger Schritts"
    // ABER: Wenn das Wort schon auf -s/-is/-us/-x/-z endet, kein -s/-es anhaengen
    const words = replacement.split(' ');
    const lastWord = words[words.length - 1];
    if ((suffix === 's' || suffix === 'es') && /[sxzß]$/i.test(lastWord)) {
      // "Basis" + "s" → "Basis" (nicht "Basiss")
      // Suffix weglassen – Wort ist schon im richtigen Form
    } else {
      words[words.length - 1] += suffix;
    }
    result = words.join(' ');
  } else {
    result = replacement;
  }

  // Gross/Kleinschreibung vom Original uebernehmen
  // Substantive behalten Grossschreibung (deutsch), Adjektive/Adverben nicht
  if (type === 'noun') {
    // Substantiv-Ersetzung: Erstes Wort gross (Nomen), Rest behalten
    // "Meilenstein" → "Wichtiger Schritt" (nicht "wichtiger Schritt")
    if (result[0] === result[0].toLowerCase()) {
      result = result[0].toUpperCase() + result.slice(1);
    }
  } else {
    // Adjektive/Adverben: Casing vom Original uebernehmen
    if (originalMatch[0] === originalMatch[0].toUpperCase() && result[0] === result[0].toLowerCase()) {
      result = result[0].toUpperCase() + result.slice(1);
    } else if (originalMatch[0] === originalMatch[0].toLowerCase() && result[0] === result[0].toUpperCase()) {
      result = result[0].toLowerCase() + result.slice(1);
    }
  }

  return result;
}

/**
 * Deutsche Artikel-Korrektur bei Genus-Wechsel.
 *
 * Problem: Einige Artikelformen sind mehrdeutig ("der" = Nom-m ODER Gen-f ODER Dat-f).
 * Loesung: Eindeutige Formen werden immer korrigiert. Mehrdeutige Formen werden
 * per Heuristik aufgeloest (Praeposition davor → Dativ, Satzanfang → Nominativ).
 *
 * Format: Array von [artikel_alt, artikel_neu, kasus_info]
 * Reihenfolge: Laengere/spezifischere Formen zuerst (eines vor ein).
 */
const ARTIKEL_REGELN = {
  'm->f': [
    // Eindeutig:
    ['des', 'der'],     // Gen-m → Gen-f
    ['dem', 'der'],     // Dat-m → Dat-f
    ['den', 'die'],     // Akk-m → Akk-f
    ['der', 'die'],     // Nom-m → Nom-f (ACHTUNG: "der" ist auch Gen-f/Dat-f, aber als m→f ist es Nom)
    ['eines', 'einer'], // Gen
    ['einem', 'einer'], // Dat
    ['einen', 'eine'],  // Akk
    ['ein', 'eine'],    // Nom
  ],
  'm->n': [
    ['der', 'das'],     // Nom
    ['den', 'das'],     // Akk-m → Akk-n
    // des→des, dem→dem: gleich, kein Eintrag noetig
    ['einen', 'ein'],   // Akk
    ['ein', 'ein'],     // Nom (gleich, aber fuer Vollstaendigkeit)
  ],
  'f->m': [
    ['die', 'der'],     // Nom-f → Nom-m (Default; Akk wuerde "den" brauchen, aber Nom ist haeufiger)
    ['eine', 'ein'],    // Nom-f → Nom-m
    ['einen', 'einen'], // Akk bleibt
    // "der" (Gen-f oder Dat-f) → wird per Praepositions-Heuristik in fixArtikelBefore aufgeloest
    ['der', '__DAT_OR_GEN__'], // Platzhalter, wird unten behandelt
    ['einer', '__DAT_OR_GEN_U__'], // Platzhalter
  ],
  'f->n': [
    ['die', 'das'],     // Nom/Akk-f → Nom/Akk-n
    ['eine', 'ein'],    // Nom/Akk
  ],
  'n->m': [
    ['das', 'der'],     // Nom-n → Nom-m
    // des→des, dem→dem: gleich
    ['ein', 'ein'],     // gleich
  ],
  'n->f': [
    ['das', 'die'],     // Nom/Akk-n → Nom/Akk-f
    ['ein', 'eine'],    // Nom/Akk
  ],
};

/**
 * Korrigiert den Artikel vor einem ersetzten Substantiv.
 * Sucht 1-3 Woerter vor der Ersetzungsposition nach einem Artikel
 * und passt ihn an das neue Genus an.
 *
 * @param {string} text - Der gesamte Text
 * @param {number} pos - Position des ersetzten Substantivs
 * @param {object} genus - {from: 'm', to: 'f'} etc.
 * @returns {string} - Text mit korrigiertem Artikel
 */
function fixArtikelBefore(text, pos, genus) {
  if (!genus || genus.from === genus.to) return text;

  const key = `${genus.from}->${genus.to}`;
  const regeln = ARTIKEL_REGELN[key];
  if (!regeln) return text;

  // Finde 1-3 Woerter vor pos (Artikel + evtl. Adjektiv/Praeposition dazwischen)
  const before = text.substring(Math.max(0, pos - 40), pos);
  // Suche letzten Artikel im Vorfeld (max 2 Woerter vor dem Substantiv)
  const artikelRegex = /\b(eines|einer|einem|einen|eine|ein|der|die|das|des|dem|den)\b(?=\s+(?:\S+\s+)?$)/i;
  const match = before.match(artikelRegex);
  if (!match) return text;

  const artikelLower = match[1].toLowerCase();

  // Passende Regel finden
  let newArtikel = null;
  for (const [alt, neu] of regeln) {
    if (artikelLower === alt) {
      newArtikel = neu;
      break;
    }
  }
  if (!newArtikel) return text;

  // Mehrdeutigkeit aufloesen: "der" kann Gen-f oder Dat-f sein
  // Heuristik: Dativ-Praeposition davor → Dativ, sonst Genitiv
  const DATIV_PRAEP = /\b(in|an|auf|bei|mit|nach|von|zu|aus|seit|unter|über|vor|hinter|neben|zwischen)\s*$/i;
  if (newArtikel === '__DAT_OR_GEN__') {
    const contextBefore = text.substring(Math.max(0, pos - 60), Math.max(0, pos - 40) + match.index);
    newArtikel = DATIV_PRAEP.test(contextBefore)
      ? (genus.to === 'm' ? 'dem' : genus.to === 'f' ? 'der' : 'dem')  // Dativ
      : (genus.to === 'm' ? 'des' : genus.to === 'f' ? 'der' : 'des'); // Genitiv
  } else if (newArtikel === '__DAT_OR_GEN_U__') {
    const contextBefore = text.substring(Math.max(0, pos - 60), Math.max(0, pos - 40) + match.index);
    newArtikel = DATIV_PRAEP.test(contextBefore)
      ? (genus.to === 'm' ? 'einem' : genus.to === 'f' ? 'einer' : 'einem')
      : (genus.to === 'm' ? 'eines' : genus.to === 'f' ? 'einer' : 'eines');
  }

  // Gross/Klein beibehalten
  if (match[1][0] === match[1][0].toUpperCase()) {
    newArtikel = newArtikel[0].toUpperCase() + newArtikel.slice(1);
  }

  const artikelStart = Math.max(0, pos - 40) + match.index;
  const artikelEnd = artikelStart + match[1].length;
  return text.substring(0, artikelStart) + newArtikel + text.substring(artikelEnd);
}

function fixText(text) {
  let fixed = text;

  // Tier-1-Wörter ersetzen (morphologisch korrekt)
  // Substantive mit Genus-Wechsel merken fuer Artikel-Korrektur
  const artikelFixes = [];
  for (const entry of TIER1) {
    const [word, replacement, type] = entry;
    const genus = entry[3] || null; // Genus-Mapping (nur bei Substantiven mit Wechsel)
    const regex = buildTier1Regex(word, type);

    if (type === 'noun' && genus) {
      // Erst Positionen sammeln, dann rueckwaerts ersetzen (damit Positionen stimmen)
      let match;
      const matches = [];
      while ((match = regex.exec(fixed)) !== null) {
        matches.push({ index: match.index, match: match[0], suffix: match[1] || '' });
      }
      // Rueckwaerts ersetzen damit Positionen nicht verrutschen
      for (let i = matches.length - 1; i >= 0; i--) {
        const m = matches[i];
        const newWord = applyMorphFix(m.match, replacement, m.suffix, type);
        fixed = fixed.substring(0, m.index) + newWord + fixed.substring(m.index + m.match.length);
        // Artikel-Korrektur direkt nach Substantiv-Ersetzung
        fixed = fixArtikelBefore(fixed, m.index, genus);
      }
    } else {
      fixed = fixed.replace(regex, (match, suffix) => {
        return applyMorphFix(match, replacement, suffix || '', type);
      });
    }
  }

  // Verbotene Phrasen ersetzen (die einfachen Fälle)
  const phrasenReplace = [
    ['es ist wichtig zu beachten, dass ', ''],
    ['es ist wichtig zu beachten dass ', ''],
    ['darüber hinaus ', 'Außerdem '],
    ['des weiteren ', 'Außerdem '],
    ['aufgrund der tatsache, dass ', 'Weil '],
    ['aufgrund der tatsache dass ', 'Weil '],
    ['in anbetracht der tatsache, dass ', 'Da '],
    ['in anbetracht der tatsache dass ', 'Da '],
    ['zusammenfassend lässt sich sagen, dass ', ''],
    ['zusammenfassend lässt sich sagen dass ', ''],
    ['es lässt sich festhalten, dass ', ''],
    ['es lässt sich festhalten dass ', ''],
    ['im folgenden wird erläutert', ''],
    ['es gilt zu beachten, dass ', ''],
    ['es gilt zu beachten dass ', ''],
    ['wie bereits erwähnt ', ''],
    ['nicht zuletzt ', 'Außerdem '],
    ['zu guter letzt ', 'Zum Schluss: '],
    ['last but not least ', 'Und: '],
  ];

  for (const [phrase, replacement] of phrasenReplace) {
    const regex = new RegExp(phrase.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'), 'gi');
    fixed = fixed.replace(regex, replacement);
  }

  return fixed;
}

// ============================================================
//  CLI
// ============================================================

function printUsage() {
  console.log(`
  humanize-de.js – Deutscher KI-Text-Detektor

  Verwendung:
    node humanize-de.js score <datei>     Score (0-100)
    node humanize-de.js analyze <datei>   Detaillierte Analyse
    node humanize-de.js suggest <datei>   Ersetzungsvorschläge
    node humanize-de.js fix <datei>       Auto-Fix (schreibt <datei>.fixed.md)

  Score-Skala:
    0-20   Klingt menschlich
    21-40  Leicht maschinell
    41-60  Gemischt
    61-80  Offensichtlich KI
    81-100 ChatGPT-Standard
  `);
}

function main() {
  const args = process.argv.slice(2);

  if (args.length < 2) {
    printUsage();
    process.exit(1);
  }

  const command = args[0];
  const filePath = args[1];

  // Datei lesen
  if (!fs.existsSync(filePath)) {
    console.error(`  Fehler: Datei nicht gefunden: ${filePath}`);
    process.exit(1);
  }

  const text = fs.readFileSync(filePath, 'utf-8');

  if (text.trim().length === 0) {
    console.error('  Fehler: Datei ist leer.');
    process.exit(1);
  }

  // Markdown-Formatierung entfernen (nur Text analysieren)
  const cleanText = text
    .replace(/^#+\s.*/gm, '')          // Überschriften entfernen
    .replace(/^\s*[-*]\s/gm, '')       // Bullet Points entfernen
    .replace(/\*\*([^*]+)\*\*/g, '$1') // Fett entfernen
    .replace(/\*([^*]+)\*/g, '$1')     // Kursiv entfernen
    .replace(/`[^`]+`/g, '')           // Inline-Code entfernen
    .replace(/```[\s\S]*?```/g, '')    // Code-Blöcke entfernen
    .replace(/\[([^\]]+)\]\([^)]+\)/g, '$1') // Links entfernen
    .replace(/^\s*>\s/gm, '')          // Blockquotes entfernen
    .replace(/^\s*\|.*\|.*$/gm, '')    // Tabellen entfernen
    .replace(/---+/g, '')              // Horizontale Linien entfernen
    .replace(/\n{3,}/g, '\n\n')        // Mehrfache Leerzeilen reduzieren
    .trim();

  const report = calculateScore(cleanText);

  switch (command) {
    case 'score':
      console.log(formatScore(report));
      break;

    case 'analyze':
      console.log(formatAnalyze(report, cleanText));
      break;

    case 'suggest':
      console.log(formatSuggest(report));
      break;

    case 'fix': {
      const fixed = fixText(text);
      const ext = path.extname(filePath);
      const base = path.basename(filePath, ext);
      const dir = path.dirname(filePath);

      // Backup der Originaldatei erstellen
      const bakPath = path.join(dir, `${base}${ext}.bak`);
      if (!fs.existsSync(bakPath)) {
        fs.writeFileSync(bakPath, text, 'utf-8');
        console.log(`  Backup erstellt: ${bakPath}`);
      }

      const outPath = path.join(dir, `${base}.fixed${ext}`);
      fs.writeFileSync(outPath, fixed, 'utf-8');

      // Score vorher/nachher
      const reportBefore = calculateScore(cleanText);
      const fixedClean = fixed
        .replace(/^#+\s.*/gm, '')
        .replace(/\*\*([^*]+)\*\*/g, '$1')
        .replace(/`[^`]+`/g, '')
        .replace(/```[\s\S]*?```/g, '')
        .trim();
      const reportAfter = calculateScore(fixedClean);

      console.log(`
  Fix angewendet!
  ────────────────
  Vorher:  ${reportBefore.score} / 100
  Nachher: ${reportAfter.score} / 100
  Differenz: ${reportBefore.score - reportAfter.score} Punkte verbessert

  Gespeichert: ${outPath}
      `);
      break;
    }

    default:
      console.error(`  Unbekannter Befehl: ${command}`);
      printUsage();
      process.exit(1);
  }
}

main();
