/**
 * English structural + phrasal patterns (en-side).
 *
 * Migrated verbatim from avoid-ai-writing's patterns.js. Each array maps to a
 * detector `type`. Behavioral parity with aaw is the regression contract.
 */
'use strict';

// ─── Transition phrases ────────────────────────────────────────────
const TRANSITIONS = [
  /\bmoreover\b/gi,
  /\bfurthermore\b/gi,
  /\badditionally\b/gi,
  /\bin\s+today'?s\b/gi,
  /\bin\s+an\s+era\s+where\b/gi,
  /\bit'?s\s+worth\s+noting\s+that\b/gi,
  /\bnotably\b/gi,
  /\bin\s+conclusion\b/gi,
  /\bin\s+summary\b/gi,
  /\bto\s+summarize\b/gi,
  /\bwhen\s+it\s+comes\s+to\b/gi,
  /\bat\s+the\s+end\s+of\s+the\s+day\b/gi,
  /\bthat\s+(?:being\s+)?said\b/gi,
];

// ─── Chatbot artifacts ─────────────────────────────────────────────
const CHATBOT_ARTIFACTS = [
  /\bi\s+hope\s+this\s+helps\b/gi,
  /\bcertainly!\b/gi,
  /\babsolutely!\b/gi,
  /\bgreat\s+question!\b/gi,
  /\bexcellent\s+point!\b/gi,
  /\bfeel\s+free\s+to\s+reach\s+out\b/gi,
  /\blet\s+me\s+know\s+if\s+you\s+need\s+anything\b/gi,
  /\bin\s+this\s+article,?\s+we\s+will\s+explore\b/gi,
  /\blet'?s\s+dive\s+in!?\b/gi,
];

// ─── Sycophantic tone ──────────────────────────────────────────────
const SYCOPHANTIC = [
  /\byou'?re\s+absolutely\s+right\b/gi,
  /\bthat'?s\s+a\s+really\s+insightful\b/gi,
  /\bthat'?s\s+a\s+great\s+question\b/gi,
  /\bexcellent\s+question\b/gi,
];

// ─── Filler phrases ────────────────────────────────────────────────
const FILLERS = [
  /\bit\s+is\s+important\s+to\s+note\s+that\b/gi,
  /\bin\s+terms\s+of\b/gi,
  /\bthe\s+reality\s+is\s+that\b/gi,
  /\bit'?s\s+important\s+to\s+note\s+that\b/gi,
];

// ─── Generic conclusions ───────────────────────────────────────────
const GENERIC_CONCLUSIONS = [
  /\bthe\s+future\s+looks\s+bright\b/gi,
  /\bonly\s+time\s+will\s+tell\b/gi,
  /\bone\s+thing\s+is\s+certain\b/gi,
  /\bas\s+we\s+move\s+forward\b/gi,
];

// ─── "Let's" constructions ─────────────────────────────────────────
const LETS_PATTERNS = [
  /\blet'?s\s+explore\b/gi,
  /\blet'?s\s+take\s+a\s+look\b/gi,
  /\blet'?s\s+break\s+this\s+down\b/gi,
  /\blet'?s\s+examine\b/gi,
  /\blet'?s\s+(?:consider|discuss|delve|unpack|walk\s+through)\b/gi,
];

// ─── Reasoning chain artifacts ─────────────────────────────────────
const REASONING_ARTIFACTS = [
  /\blet\s+me\s+think\s+step\s+by\s+step\b/gi,
  /\bbreaking\s+this\s+down\b/gi,
  /\bto\s+approach\s+this\s+systematically\b/gi,
  /\bhere'?s\s+my\s+thought\s+process\b/gi,
  /\bfirst,?\s+let'?s\s+consider\b/gi,
  /\bworking\s+through\s+this\s+logically\b/gi,
];

// ─── Acknowledgment loops ──────────────────────────────────────────
const ACKNOWLEDGMENT_LOOPS = [
  /\byou'?re\s+asking\s+about\b/gi,
  /\bthe\s+question\s+of\s+whether\b/gi,
  /\bto\s+answer\s+your\s+question\b/gi,
];

// ─── Significance inflation ────────────────────────────────────────
const SIGNIFICANCE_INFLATION = [
  /\bmarking\s+a\s+(?:pivotal|significant|important)\s+moment\b/gi,
  /\ba\s+watershed\s+moment\s+for\b/gi,
  /\bin\s+the\s+evolution\s+of\b/gi,
  /\ba\s+(?:pivotal|defining)\s+moment\s+in\b/gi,
];

// ─── Vague attributions ────────────────────────────────────────────
const VAGUE_ATTRIBUTIONS = [
  /\bexperts\s+(?:believe|say|suggest|agree)\b/gi,
  /\bstudies\s+(?:show|suggest|indicate)\b/gi,
  /\bresearch\s+(?:shows|suggests|indicates)\b/gi,
  /\bindustry\s+leaders\s+(?:agree|believe|say)\b/gi,
];

// ─── Hollow intensifiers ───────────────────────────────────────────
const HOLLOW_INTENSIFIERS = [
  /\bgenuine(?:ly)?\b/gi,
  /\btruly\b/gi,
  /\bquite\s+frankly\b/gi,
  /\bto\s+be\s+honest\b/gi,
  /\blet'?s\s+be\s+clear\b/gi,
];

// ─── Emotional flatline ────────────────────────────────────────────
const EMOTIONAL_FLATLINE = [
  /\bwhat\s+surprised\s+me\s+most\b/gi,
  /\bi\s+was\s+fascinated\s+to\b/gi,
  /\bwhat\s+struck\s+me\s+was\b/gi,
  /\bi\s+was\s+excited\s+to\s+learn\b/gi,
  /\bthe\s+most\s+interesting\s+(?:part|thing|aspect|piece)\b/gi,
  /^\s*interesting\s+(?:part|thing|aspect|piece)(?:\s+of\s+(?:the\s+)?\w+)?\s*:/gim,
];

// ─── Novelty inflation ─────────────────────────────────────────────
const NOVELTY_INFLATION = [
  /\bthe\s+failure\s+mode\s+nobody'?s?\s+naming\b/gi,
  /\ba\s+problem\s+nobody\s+talks\s+about\b/gi,
  /\bthe\s+insight\s+everyone'?s?\s+missing\b/gi,
  /\bwhat\s+nobody\s+tells\s+you\b/gi,
];

// ─── Cutoff disclaimers ────────────────────────────────────────────
const CUTOFF_DISCLAIMERS = [
  /\bas\s+of\s+my\s+last\s+update\b/gi,
  /\bas\s+of\s+my\s+(?:knowledge\s+)?(?:cut-?off|last\s+training)\b/gi,
  /\bi\s+don'?t\s+have\s+access\s+to\s+real-?time\s+(?:data|information)\b/gi,
  /\bbased\s+on\s+available\s+information\b/gi,
  /\bas\s+an?\s+(?:ai|artificial\s+intelligence|large\s+language|ai\s+language)\s+(?:language\s+)?model\b/gi,
  /\bi\s+(?:am|'m)\s+an?\s+(?:ai|artificial\s+intelligence|large\s+language)\s+(?:assistant|model)?\b/gi,
  /\bi\s+cannot\s+(?:provide|give|offer)\s+(?:legal|medical|financial|professional)\s+advice\b/gi,
  /\bmy\s+training\s+data\s+(?:only\s+)?(?:goes\s+up\s+to|extends\s+to|ends\s+(?:in|at))\b/gi,
];

// ─── Template phrases ──────────────────────────────────────────────
const TEMPLATE_PHRASES = [
  /\ba\s+\w+\s+step\s+(?:towards?|forward\s+for)\b/gi,
  /\bwhether\s+you'?re\s+\w+\s+or\s+\w+/gi,
  /\bi\s+recently\s+had\s+the\s+pleasure\s+of\b/gi,
];

// ─── False concession ──────────────────────────────────────────────
const FALSE_CONCESSION = [
  /\bwhile\s+\w+\s+is\s+impressive\b/gi,
  /\balthough\s+\w+\s+has\s+made\s+strides\b/gi,
  /\bdespite\s+\w+\s+challenges?\b/gi,
];

// ─── Rhetorical question openers ───────────────────────────────────
const RHETORICAL_QUESTIONS = [
  /\bbut\s+what\s+does\s+this\s+mean\s+for\b/gi,
  /\bso\s+why\s+should\s+you\s+care\b/gi,
  /\bwhat'?s\s+next\?\s*/gi,
];

// ─── Hedge-stacked predictions ─────────────────────────────────────
const HEDGE_STACK = [
  /\b(?:could|may|might)\s+(?:\w+\s+){0,2}(?:potentially|eventually|ultimately|possibly|conceivably)\b/gi,
  /\b(?:potentially|eventually|ultimately)\s+(?:could|may|might)\b/gi,
];

// ─── Generic future-narrative closers ──────────────────────────────
const FUTURE_NARRATIVE = [
  /\b(?:may|could|will|is\s+(?:poised|set)\s+to)\s+become\s+(?:one\s+of\s+)?(?:the\s+)?(?:most\s+)?\w+\s+(?:narratives?|stories|developments?|trends?|movements?|chapters?|themes?|forces?)\b/gi,
  /\bone\s+of\s+the\s+most\s+important\s+(?:narratives?|stories|trends?|themes?)\s+of\s+the\s+(?:next|coming)\s+\w+\b/gi,
];

// ─── "Real/actual" adjective inflation ─────────────────────────────
const REAL_ACTUAL_INFLATION = [
  /\b(?:real|actual|genuine|true)\s+(?:on-?chain\s+)?(?:tokenomics|economics|utility|adoption|sustainability|impact|revenue|fundamentals|demand|value|innovation|traction)\b/gi,
];

// ─── Formulaic openers ─────────────────────────────────────────────
const FORMULAIC_OPENERS = [
  /\bin\s+the\s+(?:rapidly\s+|ever-?\s*)?(?:evolving|changing|expanding|growing|shifting)\s+(?:world|landscape|realm|space|field|domain|era)\s+of\b/gi,
  /\bin\s+(?:an?|the)\s+(?:digital\s+)?age\s+(?:where|of)\b/gi,
  /\bas\s+(?:we|the\s+world|society|industries?)\s+(?:continue|move|navigate|enter)\s+(?:to\s+)?(?:evolve|forward|into|through)\b/gi,
  /\bhas\s+emerged\s+as\s+(?:a|the|one\s+of)\s+(?:leading|key|major|critical|essential|fundamental|pivotal|prominent|dominant|important)\s+\w+/gi,
  /\bhas\s+become\s+increasingly\s+(?:important|critical|popular|relevant|prominent|essential)\b/gi,
];

// Title Case section headers — gated to non-technical context modes.
const TITLE_CASE_HEADER = /^([A-Z][a-z]+(?:\s+(?:[A-Z][a-z]+|and|or|of|the|in|for|to|a|an))+\s+[A-Z][a-z]+)\s*$/gm;

// ─── Parenthetical hedging asides ──────────────────────────────────
const PARENTHETICAL_HEDGE = [
  /\(\s*(?:and\s+)?(?:increasingly|notably|importantly|crucially|interestingly|perhaps)[,]?\s+[^)]{3,60}\)/gi,
  /\(\s*or\s+more\s+(?:precisely|accurately|specifically)[,]?\s+[^)]{3,60}\)/gi,
  /\(\s*though\s+to\s+be\s+fair[,]?\s+[^)]{3,60}\)/gi,
  /\(\s*at\s+least\s+(?:in\s+)?(?:theory|principle|part)[,]?\s+[^)]{0,60}\)/gi,
];

// ─── Confidence calibration ────────────────────────────────────────
const CONFIDENCE_CALIBRATION = [
  /\binterestingly\b/gi,
  /\bsurprisingly\b/gi,
  /\bimportantly\b/gi,
  /\bsignificantly\b/gi,
  /\bcertainly\b/gi,
  /\bundoubtedly\b/gi,
  /\bwithout\s+a\s+doubt\b/gi,
];

// ─── Social endorsement / CTA closers ──────────────────────────────
const SOCIAL_CTA_CLOSER = [
  /\bthis\s+one['’]?s?\s+(?:is\s+)?(?:well\s+|totally\s+|absolutely\s+|definitely\s+|really\s+|truly\s+|easily\s+|more\s+than\s+)?worth\s+(?:your\s+time|the\s+read|a\s+read|every\s+(?:minute|second)|reading|watching|a\s+listen|a\s+watch|a\s+look|it)\b/gi,
  /\bthis\s+one['’]?s?\s+(?:is\s+)?a\s+must[-\s]?(?:read|watch|listen|see)\b/gi,
  /\b(?:highly|strongly|can['’]?t|cannot)\s+recommend\w*\s+(?:giving\s+)?(?:this|it)\s+(?:one\s+)?a\s+(?:read|listen|watch|look|go)\b/gi,
  /\bdo\s+yourself\s+a\s+favou?r\s+and\s+(?:read|watch|check\s+out)\s+(?:this|it)\b/gi,
  /\byou\s+(?:really\s+)?(?:won['’]?t|do\s*n['’]?t|will\s+not|do\s+not)\s+want\s+to\s+miss\s+this(?:\s+one)?(?=\s*(?:[:.!\n]|$))/gi,
  /(?<=^|[,.!?:\n]\s{0,4})(?:you\s+can\s+)?thank\s+me\s+later\b/gim,
  /(?<=^|[.!?:\n]\s{0,4})save\s+this\s+(?:one\s+)?for\s+later\b/gim,
  /\bbookmark\s+this(?:\s+(?:one|post|thread))?(?=\s*(?:[:.!\n]|$))/gi,
  /\bdo\s*n['’]?t\s+sleep\s+on\s+this\b/gi,
  /\btrust\s+me,?\s+(?:on\s+this|you['’]?ll)\b/gi,
];

// ─── Cross-lingual structural symmetry (en counterparts of zh/structures.js) ──
// These mirror the Chinese structural anti-patterns so bilingual symmetry
// holds: the SAME concept fires in both languages (see bilingual.test.js).
// They use the SAME detector `type` as their zh counterparts.

// Binary-contrast false drama: "It's not X, it's Y" / "It is not X, it is Y" / "Not X, but Y".
// en counterpart of zh BINARY_CONTRAST (不是X而是Y). Covers both contracted
// ("it's") and full ("it is") forms.
const BINARY_CONTRAST = [
  /\bit(?:'?s|\s+is)\s+not\s+(?:about|just)?\s*[\w\s]{1,30},?\s+it(?:'?s|\s+is)\s+(?:about\s+)?[\w\s]{1,30}/gi,
  /\bnot\s+[\w\s]{1,20},?\s+but\s+(?:rather\s+)?[\w\s]{1,30}/gi,
];

// Mechanical ordering: "First... Second... Finally..." / "First... Then... Lastly...".
// en counterpart of zh MECHANICAL_ORDERING (首先…其次…最后).
const MECHANICAL_ORDERING = [
  /\bfirst,?\s+[^.;]{2,50}[;.]\s*[^.;]*\bsecond,?\s+[^.;]{2,50}[;.]\s*[^.;]*\b(?:finally|lastly),?/gi,
  /\bfirst,?\s+[^.;]{2,50}[;.]\s*[^.;]*\bthen,?\s+[^.;]{2,50}[;.]\s*[^.;]*\bfinally,?/gi,
];

// Symmetry padding: "both X and Y" stacked for false balance.
// en counterpart of zh SYMMETRY_PADDING (既要…又要).
const SYMMETRY_PADDING = [
  /\bboth\s+[\w\s]{1,25}\s+and\s+[\w\s]{1,25},?\s+(?:while|whilst|and)\s+(?:also\s+)?(?:both\s+)?[\w\s]{1,25}\s+and\s+[\w\s]{1,25}/gi,
];

// Value-inflation skeleton: "It's not just X, it's Y" / "more than just X".
// en counterpart of zh VALUE_INFLATION (这不仅仅是…更是).
const VALUE_INFLATION = [
  /\bit'?s\s+not\s+just\s+[\w\s]{1,25},?\s+it'?s\s+[\w\s]{1,35}/gi,
  /\bmore\s+than\s+just\s+a\s+[\w\s]{1,25},?\s+it'?s\s+a\s+[\w\s]{1,35}/gi,
];

// Summary closer (structural sentence form): "In conclusion, ..." / "To sum up, ...".
// en counterpart of zh SUMMARY_CLOSER. (Word-level covered by TRANSITIONS +
// GENERIC_CONCLUSIONS; this catches the full sentence-initial shape.)
const SUMMARY_CLOSER = [
  /\b(?:in\s+conclusion|to\s+sum\s+up|in\s+summary|to\s+summarize|all\s+in\s+all)[^.!?]{2,80}[.!?]/gi,
];

module.exports = {
  TRANSITIONS,
  CHATBOT_ARTIFACTS,
  SYCOPHANTIC,
  FILLERS,
  GENERIC_CONCLUSIONS,
  LETS_PATTERNS,
  REASONING_ARTIFACTS,
  ACKNOWLEDGMENT_LOOPS,
  SIGNIFICANCE_INFLATION,
  VAGUE_ATTRIBUTIONS,
  HOLLOW_INTENSIFIERS,
  EMOTIONAL_FLATLINE,
  NOVELTY_INFLATION,
  CUTOFF_DISCLAIMERS,
  TEMPLATE_PHRASES,
  FALSE_CONCESSION,
  RHETORICAL_QUESTIONS,
  HEDGE_STACK,
  FUTURE_NARRATIVE,
  REAL_ACTUAL_INFLATION,
  FORMULAIC_OPENERS,
  TITLE_CASE_HEADER,
  PARENTHETICAL_HEDGE,
  CONFIDENCE_CALIBRATION,
  SOCIAL_CTA_CLOSER,
  // Cross-lingual symmetry (en counterparts of zh/structures.js)
  BINARY_CONTRAST,
  MECHANICAL_ORDERING,
  SYMMETRY_PADDING,
  VALUE_INFLATION,
  SUMMARY_CLOSER,
};
