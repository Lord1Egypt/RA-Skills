#!/usr/bin/env node
/**
 * fetch.js — скачать любой документ с adilet.zan.kz → Markdown
 *
 * Запускать из корня workspace. Пути --out и --html резолвируются от CWD.
 *
 * Рекомендуемый способ (безопасный — без TLS-рисков):
 *   1. Откройте нужную страницу в браузере на adilet.zan.kz
 *   2. Сохраните как HTML
 *   3. node skills/kz-tax-code/scripts/fetch.js \
 *        --doc=XXXXXXXXX \
 *        --out=skills/kz-tax-code/data/output.md \
 *        --html=skills/kz-tax-code/data/saved.html
 *
 * Автоматическое скачивание (только в доверенной сети):
 *   node skills/kz-tax-code/scripts/fetch.js \
 *     --doc=XXXXXXXXX --out=skills/kz-tax-code/data/output.md --insecure
 *
 * Примеры документов (актуальны на 2026 год, коды хранятся в data/laws.json):
 *   Z2500000065 — Закон о республиканском бюджете (МРП, МЗП)
 *   Z1500000405 — Закон об ОСМС (ВОСМС, ОСМС)
 *   Z2100000021 — Закон об обязательном социальном страховании (СО)
 *   Z1300000105 — Закон о пенсионном обеспечении (ОПВ, ОПВР)
 *
 * Номер документа — из URL: https://adilet.zan.kz/rus/docs/Z2500000065
 */

import { readFileSync, writeFileSync } from "fs";
import { parseHtml, fetchHtml, parseArgs, applyInsecure } from "./_shared.mjs";

const args     = parseArgs();
const docId    = args["doc"];
const outFile  = args["out"];
const lang     = args["lang"]     ?? "ru";
const htmlFile = args["html"]     ?? null;
const insecure = args["insecure"] === true || args["insecure"] === "true";

if (!docId || !outFile) {
  console.error([
    "Использование:",
    "  node fetch.js --doc=XXXXXXXXX --out=./output.md [--lang=ru|kaz] [--insecure]",
    "",
    "С локальным HTML (без --insecure):",
    "  node fetch.js --doc=XXXXXXXXX --out=./output.md --html=./local.html",
  ].join("\n"));
  process.exit(1);
}

if (!htmlFile && !insecure) {
  console.error([
    "Ошибка: для скачивания с adilet.zan.kz укажите --insecure (только в доверенной сети).",
    "Рекомендуется: скачайте HTML вручную и передайте через --html=./file.html",
  ].join("\n"));
  process.exit(1);
}

applyInsecure(insecure);

async function main() {
  console.log(`\n📥 Документ : ${docId}`);
  console.log(`   Язык     : ${lang}`);
  console.log(`   Файл     : ${outFile}\n`);

  let html;
  if (htmlFile) {
    console.log(`  Читаю локальный файл: ${htmlFile}`);
    html = readFileSync(htmlFile, "utf-8");
  } else {
    html = await fetchHtml(docId, lang);
  }

  process.stdout.write(`  Парсинг HTML → Markdown ...`);
  const md = parseHtml(html);
  const sectionCount = (md.match(/^## /gm) ?? []).length;
  console.log(` ${Math.round(md.length / 1024)}KB, разделов: ${sectionCount}`);

  if (md.length < 1000) {
    throw new Error("Документ слишком короткий — возможно, страница не загрузилась.");
  }

  writeFileSync(outFile, md, "utf-8");
  console.log(`\n✅ Сохранено: ${outFile}`);
}

main().catch(e => {
  console.error(`\n❌ Ошибка: ${e.message}`);
  process.exit(1);
});
