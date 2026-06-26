#!/usr/bin/env node
/**
 * search.js — поиск по Налоговому кодексу РК или любому другому закону
 *
 * По НК РК (версия current/outdated):
 *   node search.js --article=503 [--version=current|outdated] [--lang=ru|kaz]
 *   node search.js --keyword="дивиденды нерезидент" [--version=outdated] [--lang=ru]
 *   node search.js --topic="НДС экспорт освобождение" [--lang=ru]
 *
 * По произвольному файлу (скачанному через fetch.js):
 *   node search.js --file=skills/kz-tax-code/data/budget-current-ru.md --keyword="месячный расчётный"
 *   node search.js --file=skills/kz-tax-code/data/osms-ru.md --topic="ставка взносов ВОСМС"
 * (пути указываются от CWD — корня workspace)
 *
 * Возвращает JSON: { version, versionName, lang, query, totalArticles, found, results }
 */

import { readFileSync, existsSync } from "fs";
import { join, dirname } from "path";
import { fileURLToPath } from "url";
import { parseArgs } from "./_shared.mjs";

const __dirname = dirname(fileURLToPath(import.meta.url));
const DATA_DIR   = join(__dirname, "..", "data");
const VERS_FILE  = join(DATA_DIR, "versions.json");
const LAWS_FILE  = join(DATA_DIR, "laws.json");

const CONTEXT_PARAGRAPHS_BEFORE = 2;
const CONTEXT_PARAGRAPHS_AFTER  = 5;
const MAX_RESULTS                = 10;
const TITLE_BOOST                = 3;
const MIN_TOPIC_SCORE            = 1;
const TITLE_FIRST_BOOST          = 10; // extra boost for title-first matches

// ── versions.json + laws.json ──────────────────────────────────────────────────
let versionsMeta = {};
try { versionsMeta = JSON.parse(readFileSync(VERS_FILE, "utf-8")); } catch {}

let lawsMeta = {};
try { lawsMeta = JSON.parse(readFileSync(LAWS_FILE, "utf-8")); } catch {}

// Термины, которые НЕ находятся в НК РК — нужно искать через fetch.js + laws.json
// Ключ → имя закона (для подсказки пользователю)
const EXTERNAL_TERMS = (() => {
  const map = {};
  for (const [key, law] of Object.entries(lawsMeta)) {
    if (key.startsWith("_")) continue;
    const name = typeof law.name === "object" ? law.name.ru : law.name;
    for (const lang of ["ru", "kaz"]) {
      for (const term of (law.contains?.[lang] ?? [])) {
        map[term.toLowerCase()] = { lawKey: key, name };
      }
    }
  }
  return map;
})();

// ── Abbreviation dictionary ────────────────────────────────────────────────────
const ABBREVIATIONS = {
  // Русский
  "кпн":       "корпоративный подоходный налог",
  "ипн":       "индивидуальный подоходный налог",
  "ндс":       "налог на добавленную стоимость",
  "сн":        "социальный налог",
  "опв":       "обязательные пенсионные взносы",
  "осмс":      "обязательное социальное медицинское страхование",
  "восмс":     "взносы работодателя осмс",
  // "со" намеренно исключено: двухбуквенный предлог в русском ("со стороны",
  // "со временем"), вызывает ложные расширения запросов. Для поиска по
  // социальным отчислениям использовать полный термин или --topic.
  // "со":     "социальные отчисления",
  "мсб":       "малый средний бизнес",
  "нк":        "налоговый кодекс",
  "сгд":       "совокупный годовой доход",
  "кгд":       "комитет государственных доходов",
  "мрп":       "месячный расчётный показатель",
  "мзп":       "минимальная заработная плата",
  "нпа":       "нормативный правовой акт",
  "рк":        "республика казахстан",
  "ип":        "индивидуальный предприниматель",
  "юл":        "юридическое лицо",
  "фл":        "физическое лицо",
  "тоо":       "товарищество ограниченной ответственностью",
  "ао":        "акционерное общество",
  // Казахский
  "ққс":       "қосылған құн салығы",
  "аек":       "айлық есептік көрсеткіш",
  "еам":       "еңбекақының ең төмен мөлшері",
  "мжж":       "міндетті жинақтаушы зейнетақы жарналары",
  "мжжж":      "міндетті жұмыс беруші зейнетақы жарналары",
  "әа":        "әлеуметтік аударымдар",
  "мәмс":      "міндетті әлеуметтік медициналық сақтандыру",
  "жтс":       "жеке табыс салығы",
  "ктс":       "корпоративтік табыс салығы",
  "әм":        "әлеуметтік медициналық сақтандыру",
  "мжм":       "міндетті жинақтаушы зейнетақы жарналары",
  "қр":        "қазақстан республикасы",
  "жк":        "жеке кәсіпкер",
  "зт":        "заңды тұлға",
  "жт":        "жеке тұлға",
};

// Множество аббревиатур для защиты при токенизации
const ABBREV_SET = new Set(Object.keys(ABBREVIATIONS));

function expandAbbreviations(text) {
  // Важно: проверяем аббревиатуры только как ОТДЕЛЬНЫЕ слова, не как подстроки.
  // Иначе "со" матчит "особенности", "нк" матчит "накопленного" и т.д.
  // ё→е нормализация уже применена до вызова этой функции.
  const words = new Set(
    text.toLowerCase().split(/[\s,;.!?()\[\]\/\\0-9«»"'\-–—]+/).filter(w => w.length > 0)
  );
  const expansions = [];
  for (const [abbr, full] of Object.entries(ABBREVIATIONS)) {
    if (words.has(abbr)) expansions.push(full);
  }
  return expansions.length > 0 ? `${text} ${expansions.join(" ")}` : text;
}

function normalize(text) {
  // ё→е: в русских текстах ё и е часто взаимозаменяются (упрощённый/упрощенный).
  // Нормализация предотвращает промахи при поиске из-за этого различия.
  return expandAbbreviations(text.toLowerCase().replace(/ё/g, "е"));
}

// ── Prefix / stem matching ─────────────────────────────────────────────────────
/**
 * Сколько символов использовать при prefix-сравнении.
 * Длинные слова имеют более длинный суффикс склонения → обрезаем больше.
 */
function stemLen(word) {
  if (word.length > 10) return 6;
  if (word.length > 7)  return 5;
  if (word.length > 4)  return 4;
  return word.length; // короткие слова: точное совпадение
}

/**
 * Проверяет, содержит ли нормализованный текст ключевое слово
 * с учётом морфологии (prefix matching для слов длиннее 3 символов).
 * Аббревиатуры (≤4 символа) сравниваются точно.
 */
function textContainsKeyword(normText, kw) {
  // Сначала точное вхождение
  if (normText.includes(kw)) return true;
  // Для коротких слов и аббревиатур — только точное
  if (kw.length <= 3 || ABBREV_SET.has(kw)) return false;
  // Prefix-matching: ищем любое слово в тексте с тем же корнем
  const kwPfx = kw.slice(0, stemLen(kw));
  return normText.split(/\s+/).some(w =>
    w.length > 3 && w.slice(0, Math.min(stemLen(w), kwPfx.length)) === kwPfx
  );
}

/**
 * Разбивает строку на токены с аббревиатурами (используется для параграфного поиска).
 */
function tokenize(text) {
  return text
    .toLowerCase().replace(/ё/g, "е")  // ё→е для единообразия с normalize()
    .split(/[\s,;.!?()\[\]\/\\]+/)
    .filter(w => w.length > 1);
}

/**
 * Строгая токенизация БЕЗ раскрытия аббревиатур.
 * Используется для title-first поиска, чтобы слова раскрытия ("налог",
 * "подоходный" и т.д.) не давали ложных совпадений в заголовках чужих статей.
 */
function tokenizeStrict(text) {
  return text
    .toLowerCase().replace(/ё/g, "е")  // ё→е для единообразия с normalize()
    .split(/[\s,;.!?()\[\]\/\\]+/)
    .filter(w => w.length > 2);
}

// ── File loader ────────────────────────────────────────────────────────────────
function loadFile(version, lang) {
  const path = join(DATA_DIR, `tax-code-${version}-${lang}.md`);
  if (!existsSync(path)) {
    throw new Error(`Файл не найден: tax-code-${version}-${lang}.md. Проверьте data/ или запустите update.js.`);
  }
  return readFileSync(path, "utf-8");
}

function loadCustomFile(filePath) {
  // Резолвим относительно CWD (рабочей директории), а не scripts/.
  // Это позволяет запускать из корня workspace:
  //   node skills/kz-tax-code/scripts/search.js --file=skills/kz-tax-code/data/budget.md
  const resolved = filePath.startsWith("/") || filePath.match(/^[A-Za-z]:/)
    ? filePath
    : join(process.cwd(), filePath);
  if (!existsSync(resolved)) {
    throw new Error(`Файл не найден: ${resolved}`);
  }
  return readFileSync(resolved, "utf-8");
}

// ── Split file into article blocks ─────────────────────────────────────────────
function splitArticles(content) {
  const lines = content.split("\n");
  const articles = [];
  let current = null;

  for (const line of lines) {
    const match = line.match(/^## ((?:Статья|Artikel)\s+(\d+)[\.\-]?(.*)|(\d+)-(бап|статья)(.*))$/i);
    if (match) {
      if (current) articles.push(current);
      const num  = match[2] || match[4];
      const full = match[1].trim();
      current = {
        number:    parseInt(num),
        title:     full,
        titleNorm: normalize(full),
        text:      line + "\n",
        lines:     [line],
      };
    } else if (current) {
      if (line.match(/^## /) && !line.match(/^## (Статья|[\d]+-бап)/i)) {
        articles.push(current);
        current = null;
      } else {
        current.text += line + "\n";
        current.lines.push(line);
      }
    }
  }
  if (current) articles.push(current);
  return articles;
}

// ── Split file into paragraphs ─────────────────────────────────────────────────
function splitParagraphs(content) {
  return content.split(/\n\n+/).filter(p => p.trim().length > 0);
}

// ── Highlight ──────────────────────────────────────────────────────────────────
function highlight(text, keyword) {
  if (!keyword) return text;
  const re = new RegExp(`(${escapeRegex(keyword)})`, "gi");
  return text.replace(re, "**$1**");
}

function escapeRegex(str) {
  return str.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
}

// ── Find article that contains a paragraph ────────────────────────────────────
function findArticleForParagraph(articles, para) {
  return articles.find(a => a.text.includes(para)) ?? null;
}

// ── Score a paragraph against keywords (с prefix matching) ────────────────────
/**
 * expandedKeywords — расширенные слова (с аббревиатурами) для поиска в тексте параграфа.
 * rawWords         — исходные слова БЕЗ expansion для title-boost.
 *
 * Разделение необходимо: expansion ("индивидуальный", "подоходный") матчит
 * заголовки ЧУЖИХ статей и создаёт ложные буст-ы при title-boost.
 * В тексте параграфа expansion нужен для полноты поиска.
 */
function scoreParagraph(para, article, expandedKeywords, rawWords = expandedKeywords) {
  const norm = normalize(para);
  // Текст параграфа: expanded (высокий recall)
  let score = expandedKeywords.reduce((s, kw) => s + (textContainsKeyword(norm, kw) ? 1 : 0), 0);
  if (article) {
    // Title-boost: только strict слова (без expansion)
    const titleBonus = rawWords.reduce(
      (s, kw) => s + (textContainsKeyword(article.titleNorm, kw) ? 1 : 0), 0
    );
    score += titleBonus * TITLE_BOOST;
  }
  return score;
}

// ── Title-first pass ───────────────────────────────────────────────────────────
/**
 * Ищет статьи, в заголовках которых встречаются ключевые слова.
 * rawWords — исходные слова запроса БЕЗ раскрытия аббревиатур,
 * чтобы слова-раскрытия ("налог", "подоходный") не давали ложных совпадений.
 * Возвращает только результаты с ≥ 1 совпавшим словом, отсортированные по счёту.
 */
function searchByTitle(articles, rawWords, excludeArticles = new Set()) {
  const results = [];
  for (const article of articles) {
    if (excludeArticles.has(article.number)) continue;
    // Используем titleNorm (с expansion) для поиска rawWords (без expansion)
    // Для аббревиатур (≤4 символа или в ABBREV_SET) дополнительно проверяем,
    // содержит ли заголовок слова из расшифровки — это позволяет "ндс" найти
    // статью с "налог на добавленную стоимость" в заголовке.
    const matched = rawWords.filter(kw => {
      if (textContainsKeyword(article.titleNorm, kw)) return true;
      // Для известных аббревиатур: проверяем значимые слова расшифровки в заголовке.
      // Берём слова > 5 символов и требуем, чтобы ВСЕ они присутствовали в заголовке.
      // "ндс" → ["добавленную", "стоимость"] — оба должны быть в заголовке.
      // Это позволяет "ндс" найти "Ставки налога на добавленную стоимость"
      // и не матчить просто "Ставки налога" (СН, ИПН и т.д.).
      if (ABBREV_SET.has(kw) && ABBREVIATIONS[kw]) {
        const expWords = ABBREVIATIONS[kw].split(/\s+/).filter(w => w.length > 5);
        return expWords.length > 0 && expWords.every(w => textContainsKeyword(article.titleNorm, w));
      }
      return false;
    });
    // Требуем ВСЕ rawWords в заголовке — иначе слишком много ложных совпадений.
    // Одно совпавшее слово не означает, что статья о нужном налоге.
    if (matched.length < rawWords.length) continue;
    results.push({
      article:         article.number,
      title:           article.title,
      text:            article.text.trim(),
      score:           matched.length * TITLE_FIRST_BOOST,
      matchedKeywords: matched,
      // context не включается: для title_match агент читает `text` (полный текст статьи).
      // context в других режимах — подсвеченный фрагмент; здесь он не нужен.
      matchType:       "title_match",
    });
  }
  return results.sort((a, b) => b.score - a.score);
}

// ── Search by article number ───────────────────────────────────────────────────
function searchByArticle(articles, num) {
  return articles
    .filter(a => a.number === num)
    .map(a => ({
      article:   a.number,
      title:     a.title,
      text:      a.text.trim(),
      matchType: "article",
    }));
}

// ── Search by keyword ──────────────────────────────────────────────────────────
function searchByKeyword(content, articles, keyword) {
  const kwNorm     = normalize(keyword);
  const paragraphs = splitParagraphs(content);
  const results    = [];
  const seenArticles = new Set();

  // Pass 1: точное вхождение фразы
  for (let i = 0; i < paragraphs.length; i++) {
    const paraNorm = normalize(paragraphs[i]);
    if (!paraNorm.includes(kwNorm)) continue;

    const article = findArticleForParagraph(articles, paragraphs[i]);
    if (article && seenArticles.has(article.number)) continue;
    if (article) seenArticles.add(article.number);

    const before = paragraphs.slice(Math.max(0, i - CONTEXT_PARAGRAPHS_BEFORE), i);
    const after  = paragraphs.slice(i + 1, i + 1 + CONTEXT_PARAGRAPHS_AFTER);

    results.push({
      article:        article?.number ?? null,
      title:          article?.title  ?? null,
      // text не включается: используй --article=N для полного текста статьи.
      // В keyword-режиме достаточно context с подсвеченным фрагментом.
      matchParagraph: highlight(paragraphs[i], keyword),
      context:        [...before, `>>> ${highlight(paragraphs[i], keyword)} <<<`, ...after].join("\n\n"),
      matchType:      "keyword_exact",
    });

    if (results.length >= MAX_RESULTS) break;
  }

  // Pass 2: нашли мало или ничего — дополняем title-first + topic fallback.
  // Порог < 4: даже при наличии нескольких keyword_exact совпадений можно пропустить
  // ключевые статьи (например, статьи с нужным содержимым, но другой грамматической формой).
  if (results.length < 4) {
    const rawWords    = tokenizeStrict(keyword);           // без expansion — для заголовков
    const expandedWords = tokenize(kwNorm).filter(w => w.length > 1); // с expansion — для параграфов

    // Title-first: строгие слова запроса против нормализованных заголовков
    const titleHits = searchByTitle(articles, rawWords, seenArticles);
    titleHits.forEach(r => { seenArticles.add(r.article); results.push(r); });

    // Topic fallback по параграфам с expansion для оставшихся слотов
    if (results.length < MAX_RESULTS && expandedWords.length > 1) {
      const topicResults = searchByTopic(content, articles, expandedWords, seenArticles);
      topicResults.forEach(r => { r.matchType = "keyword_fallback"; results.push(r); });
    }
  }

  return results.slice(0, MAX_RESULTS);
}

// ── Search by topic ────────────────────────────────────────────────────────────
function searchByTopic(content, articles, keywordsOrTopic, excludeArticles = new Set()) {
  let keywords; // expanded — для параграфов
  let rawWords; // strict  — для заголовков

  if (typeof keywordsOrTopic === "string") {
    keywords = tokenize(normalize(keywordsOrTopic)).filter(w => w.length > 1);
    rawWords = tokenizeStrict(keywordsOrTopic);
  } else {
    // keywordsOrTopic уже массив (expandedWords из searchByKeyword fallback).
    // Используем его и для параграфов, и для заголовков — expansion уже включён.
    keywords = keywordsOrTopic;
    rawWords = keywordsOrTopic;
  }

  const seenArticles = new Set(excludeArticles);
  const results      = [];

  // Pass 1: title-first со строгими словами (без expansion)
  const titleHits = searchByTitle(articles, rawWords, seenArticles);
  for (const hit of titleHits) {
    seenArticles.add(hit.article);
    results.push(hit);
    if (results.length >= MAX_RESULTS) return results;
  }

  // Pass 2: параграфный поиск с prefix matching
  const paragraphs = splitParagraphs(content);

  const scored = paragraphs.map((para, idx) => {
    const article = findArticleForParagraph(articles, para);
    if (article && seenArticles.has(article.number)) return null;
    const score = scoreParagraph(para, article, keywords, rawWords);
    return score >= MIN_TOPIC_SCORE ? { para, idx, article, score } : null;
  })
  .filter(Boolean)
  .sort((a, b) => b.score - a.score);

  for (const { para, idx, article, score } of scored) {
    if (article && seenArticles.has(article.number)) continue;
    if (article) seenArticles.add(article.number);

    const before = paragraphs.slice(Math.max(0, idx - CONTEXT_PARAGRAPHS_BEFORE), idx);
    const after  = paragraphs.slice(idx + 1, idx + 1 + CONTEXT_PARAGRAPHS_AFTER);

    let highlighted = para;
    for (const kw of keywords) highlighted = highlight(highlighted, kw);

    results.push({
      article:         article?.number ?? null,
      title:           article?.title  ?? null,
      // text не включается: используй --article=N для полного текста статьи.
      // В topic-режиме достаточно context с подсвеченным фрагментом.
      score,
      matchedKeywords: keywords.filter(kw => textContainsKeyword(normalize(para), kw)),
      context:         [...before, `>>> ${highlighted} <<<`, ...after].join("\n\n"),
      matchType:       "topic",
    });

    if (results.length >= MAX_RESULTS) break;
  }

  return results;
}

// ── Main ───────────────────────────────────────────────────────────────────────
const args = parseArgs();

const version    = args.version ?? "current";
const article    = args.article ? parseInt(args.article) : null;
const keyword    = args.keyword ?? null;
const topic      = args.topic   ?? null;
const customFile = args.file    ?? null;

// Авто-определение языка.
// 1. Казахские буквы (ә ғ қ ң ө ү ұ і һ) → однозначно kaz.
// 2. Чисто-кириллические казахские аббревиатуры (АЕК, МЖЖ, МЖЖЖ, ЕАМ) →
//    не содержат казахских букв, но являются казахскими терминами.
const KAZ_CYRILLIC_ABBREVS = new Set(["аек", "мжж", "мжжж", "еам"]);

function detectLang(text) {
  if (!text) return "ru";
  if (/[әғқңөүұіһӘҒҚҢӨҮҰІҺ]/.test(text)) return "kaz";
  const words = text.toLowerCase().split(/[\s,;.!?()\[\]\/\\0-9«»"'\-–—]+/);
  if (words.some(w => KAZ_CYRILLIC_ABBREVS.has(w))) return "kaz";
  return "ru";
}
const queryText = keyword ?? topic ?? "";
const lang = args.lang
  ? args.lang.toLowerCase()
  : detectLang(queryText);

if (!customFile && !["current", "outdated"].includes(version)) {
  console.error(`Ошибка: --version должен быть "current" или "outdated"`);
  process.exit(1);
}

if (!article && !keyword && !topic) {
  console.error([
    "Использование: node search.js --article=N | --keyword=<текст> | --topic=<текст>",
    "  [--version=current|outdated] [--lang=ru|kaz]",
    "  [--file=path/to/law.md]  — поиск по произвольному файлу (fetch.js)",
  ].join("\n"));
  process.exit(1);
}

try {
  let content, versionLabel, versionName;

  if (customFile) {
    content     = loadCustomFile(customFile);
    versionLabel = "custom";
    versionName  = customFile.split(/[\\/]/).pop();  // имя файла как label
  } else {
    content     = loadFile(version, lang);
    versionLabel = version;
    versionName  = versionsMeta[version]?.name ?? version;
  }

  const articles = splitArticles(content);

  let results;
  if (article !== null)  results = searchByArticle(articles, article);
  else if (keyword)      results = searchByKeyword(content, articles, keyword);
  else                   results = searchByTopic(content, articles, topic);

  // Проверяем, содержит ли запрос термины вне НК РК (МРП, АЕК, ОПВ, МЖЖ и т.д.)
  // Если да — добавляем подсказку: искать через fetch.js + laws.json
  // Минимум 3 символа: исключаем предлоги ("со", "на", "из") и предотвращаем
  // ложные срабатывания externalHints для коротких слов-предлогов.
  const queryWords = (keyword ?? topic ?? "")
    .toLowerCase().split(/[\s,;.!?()\[\]\/\\0-9«»"'\-–—]+/).filter(w => w.length >= 3);
  const externalMatches = queryWords
    .map(w => EXTERNAL_TERMS[w])
    .filter(Boolean)
    .filter((v, i, a) => a.findIndex(x => x.lawKey === v.lawKey) === i); // unique by lawKey

  const externalHints = externalMatches.length > 0 && !customFile
    ? externalMatches.map(m => {
        // Выбираем имя закона на языке запроса
        const lawMeta = lawsMeta[m.lawKey];
        const lawName = typeof lawMeta?.name === "object"
          ? (lang === "kaz" ? lawMeta.name.kaz : lawMeta.name.ru)
          : m.name;
        const message = lang === "kaz"
          ? `«${lawName}» — бұл термин ҚР Салық кодексінде жоқ. fetch.js арқылы жүктеп алыңыз, одан кейін --file параметрімен іздеңіз. Құжат кодтары data/laws.json-да.`
          : `Термин находится вне НК РК — в «${lawName}». Используйте fetch.js для скачивания, затем --file для поиска. Коды документов в data/laws.json.`;
        return { message, lawKey: m.lawKey };
      })
    : undefined;

  console.log(JSON.stringify({
    version:       versionLabel,
    versionName,
    lang,
    query:         { article, keyword, topic, file: customFile ?? undefined },
    totalArticles: articles.length,
    found:         results.length > 0,
    results,
    ...(externalHints ? { externalHints } : {}),
  }, null, 2));
} catch (e) {
  console.error(JSON.stringify({ found: false, error: e.message }));
  process.exit(1);
}
