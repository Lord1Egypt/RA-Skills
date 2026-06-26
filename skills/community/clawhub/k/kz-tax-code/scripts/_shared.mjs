/**
 * _shared.mjs — общий код для fetch.js и update.js
 * Парсер HTML → Markdown и вспомогательные утилиты.
 */

// ── HTML → Markdown parser ─────────────────────────────────────────────────────
export function parseHtml(html) {
  let content = html;

  const articleMatch = html.match(/<article[^>]*>([\s\S]*?)<\/article>/i);
  if (articleMatch) {
    content = articleMatch[1];
  } else {
    const divMatch = html.match(/<div[^>]*class="[^"]*doc[^"]*"[^>]*>([\s\S]*?)<\/div>/i);
    if (divMatch) content = divMatch[1];
  }

  content = content
    .replace(/<script[\s\S]*?<\/script>/gi, "")
    .replace(/<style[\s\S]*?<\/style>/gi, "");

  function clean(s) {
    return s
      .replace(/<br\s*\/?>/gi, " ")   // <br> → пробел до удаления тегов, иначе слова слипаются
      .replace(/<[^>]+>/g, "")
      .replace(/&nbsp;/g, " ")
      .replace(/&amp;/g, "&")
      .replace(/&lt;/g, "<")
      .replace(/&gt;/g, ">")
      .replace(/&quot;/g, '"')
      .replace(/&#(\d+);/g, (_, n) => String.fromCharCode(parseInt(n)))
      .replace(/\s+/g, " ")
      .trim();
  }

  const lines = [];
  const parts = content.split(/<\/(?:p|h[1-4]|li|div|td|tr)>/i);

  for (const part of parts) {
    const m = part.match(/<(h[1-4]|p|li|td)[^>]*>([\s\S]*)$/i);
    if (!m) continue;
    const tag  = m[1].toLowerCase();
    const text = clean(m[2]);
    if (!text || text.length < 2) continue;

    // [\.\-]? — точка/дефис необязательны (как в search.js splitArticles).
    // Без этого статьи вида "Статья 363 Ставки налога" (без точки) не стали бы заголовком.
    const isRuArticle  = /^Статья\s+\d+[\.\-\s]/.test(text);
    const isKazArticle = /^\d+-бап[.\s]/.test(text);

    if      (tag === "h1")                        lines.push("# " + text);
    else if (tag === "h2")                        lines.push("## " + text);
    else if (tag === "h3") {
      if (isKazArticle || isRuArticle) lines.push("\n## " + text);
      else                             lines.push("### " + text);
    }
    else if (tag === "h4")                        lines.push("#### " + text);
    else if (tag === "li")                        lines.push("- " + text);
    else if (isRuArticle || isKazArticle)         lines.push("\n## " + text);
    else                                          lines.push(text);
  }

  return lines.join("\n\n").replace(/\n{4,}/g, "\n\n\n").trim();
}

// ── Fetch HTML from adilet.zan.kz ─────────────────────────────────────────────
export async function fetchHtml(doc, langCode) {
  const siteLang = langCode === "kaz" ? "kaz" : "rus";
  const url = `https://adilet.zan.kz/${siteLang}/docs/${doc}`;
  console.log(`  Загрузка ${url} ...`);

  const res = await fetch(url, {
    headers: {
      "User-Agent": "Mozilla/5.0 (compatible; LawFetcher/1.0)",
      "Accept":     "text/html,application/xhtml+xml",
    },
    signal: AbortSignal.timeout(120_000),
  });

  if (!res.ok) throw new Error(`HTTP ${res.status} ${res.statusText} — ${url}`);

  const buf = await res.arrayBuffer();
  const ct  = res.headers.get("content-type") ?? "";
  const encMatch = ct.match(/charset=([^\s;]+)/i);
  const enc = encMatch ? encMatch[1].toLowerCase() : null;

  if (enc && enc !== "utf-8" && enc !== "utf8") {
    try { return new TextDecoder(enc).decode(buf); } catch {}
  }
  try {
    return new TextDecoder("utf-8", { fatal: true }).decode(buf);
  } catch {
    return new TextDecoder("windows-1251").decode(buf);
  }
}

// ── CLI args parser ────────────────────────────────────────────────────────────
export function parseArgs(argv = process.argv.slice(2)) {
  return Object.fromEntries(
    argv
      .filter(a => a.startsWith("--"))
      .map(a => {
        const eq = a.indexOf("=");
        return eq === -1 ? [a.slice(2), true] : [a.slice(2, eq), a.slice(eq + 1)];
      })
  );
}

// ── Apply --insecure flag ──────────────────────────────────────────────────────
export function applyInsecure(insecure) {
  if (insecure) {
    console.warn("⚠️  --insecure: проверка TLS отключена. Используйте только в доверенной сети.");
    process.env.NODE_TLS_REJECT_UNAUTHORIZED = "0";
  }
}
