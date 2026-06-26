#!/usr/bin/env node
/**
 * update.js — обновление Налогового кодекса РК
 *
 * Рекомендуемый способ (безопасный):
 *   1. Скачайте HTML вручную в браузере с adilet.zan.kz
 *   2. Передайте файлы через --html-ru и --html-kaz
 *
 *   node update.js --doc=K2600000XXX --name="НК РК 2027" --effective=2027-01-01 \
 *                  --html-ru=./nk-ru.html --html-kaz=./nk-kaz.html
 *
 * Автоматическое скачивание (требует --insecure):
 *   adilet.zan.kz использует сертификат НУЦ РК, не входящий в trust store Node.js.
 *   Флаг --insecure отключает проверку TLS — используйте только в доверенной сети.
 *
 *   node update.js --doc=K2600000XXX --name="НК РК 2027" --effective=2027-01-01 --insecure
 *
 * После выполнения:
 *   data/tax-code-current-ru.md   — новый кодекс (ru)
 *   data/tax-code-current-kaz.md  — новый кодекс (kaz)
 *   data/tax-code-outdated-ru.md  — предыдущий кодекс (ru)
 *   data/tax-code-outdated-kaz.md — предыдущий кодекс (kaz)
 *   data/versions.json            — обновлены метаданные
 */

import { readFileSync, writeFileSync, existsSync, renameSync } from "fs";
import { join, dirname } from "path";
import { fileURLToPath } from "url";
import { parseHtml, fetchHtml, parseArgs, applyInsecure } from "./_shared.mjs";

const __dirname  = dirname(fileURLToPath(import.meta.url));
const DATA_DIR   = join(__dirname, "..", "data");
const VERS_FILE  = join(DATA_DIR, "versions.json");

// ── CLI args ───────────────────────────────────────────────────────────────────
const args = parseArgs();

const docId       = args["doc"];
const name        = args["name"];
const effective   = args["effective"];
const htmlRuFile  = args["html-ru"]  ?? null;
const htmlKazFile = args["html-kaz"] ?? null;
const insecure    = args["insecure"] === true || args["insecure"] === "true";

if (!docId || !name || !effective) {
  console.error([
    "Использование (рекомендуется — локальные файлы):",
    '  node update.js --doc=K2600000XXX --name="НК РК 2027" --effective=2027-01-01 \\',
    "                 --html-ru=./nk-ru.html --html-kaz=./nk-kaz.html",
    "",
    "Автоскачивание (только в доверенной сети!):",
    '  node update.js --doc=K2600000XXX --name="НК РК 2027" --effective=2027-01-01 --insecure',
  ].join("\n"));
  process.exit(1);
}

// Применяем --insecure только если явно указан и только для этого процесса
applyInsecure(insecure);

// ── Count articles in markdown ─────────────────────────────────────────────────
function countArticles(md) {
  return (md.match(/^## (?:Статья\s+\d+|[\d]+-бап)/gm) ?? []).length;
}

// ── Main ───────────────────────────────────────────────────────────────────────
async function main() {
  console.log(`\n🔄 Обновление НК РК`);
  console.log(`   Новый кодекс : ${name} (${docId})`);
  console.log(`   Действует с  : ${effective}\n`);

  // Read current versions.json
  let versions = {};
  if (existsSync(VERS_FILE)) {
    versions = JSON.parse(readFileSync(VERS_FILE, "utf-8"));
  }

  const localFiles = { ru: htmlRuFile, kaz: htmlKazFile };
  const hasPartialLocal = (htmlRuFile && !htmlKazFile) || (!htmlRuFile && htmlKazFile);
  if (hasPartialLocal) {
    const missing = htmlRuFile ? "kaz" : "ru";
    const provided = htmlRuFile ? "--html-ru" : "--html-kaz";
    if (!insecure) {
      throw new Error(
        `Указан ${provided} без --html-${missing}.\n` +
        `Добавьте --html-${missing}=... или --insecure для автоматического скачивания ${missing}-версии.`
      );
    }
    console.warn(`⚠️  ${provided} указан, --html-${missing} отсутствует — ${missing} будет скачан автоматически.`);
  }
  const needsFetch = !htmlRuFile || !htmlKazFile;
  if (needsFetch && !insecure) {
    throw new Error(
      "Для автоматического скачивания с adilet.zan.kz добавьте флаг --insecure.\n" +
      "Рекомендуется: скачайте HTML вручную и передайте через --html-ru и --html-kaz."
    );
  }

  for (const lang of ["ru", "kaz"]) {
    console.log(`── Язык: ${lang} ──`);

    // Get HTML
    let html;
    if (localFiles[lang]) {
      console.log(`  Читаю локальный файл: ${localFiles[lang]}`);
      html = readFileSync(localFiles[lang], "utf-8");
    } else {
      html = await fetchHtml(docId, lang);
    }

    // Parse
    process.stdout.write(`  Парсинг HTML → Markdown ...`);
    const md = parseHtml(html);
    const articleCount = countArticles(md);
    console.log(` ${Math.round(md.length / 1024)}KB, статей: ${articleCount}`);

    if (articleCount < 10) {
      throw new Error(`Слишком мало статей (${articleCount}) для ${lang} — возможно, страница не загрузилась корректно.`);
    }

    // Rotate files: current → outdated
    const currentFile  = join(DATA_DIR, `tax-code-current-${lang}.md`);
    const outdatedFile = join(DATA_DIR, `tax-code-outdated-${lang}.md`);

    if (existsSync(currentFile)) {
      console.log(`  Архивирую current-${lang}.md → outdated-${lang}.md`);
      renameSync(currentFile, outdatedFile);
    }

    // Write new current
    console.log(`  Записываю tax-code-current-${lang}.md`);
    writeFileSync(currentFile, md, "utf-8");

    console.log();
  }

  // Update versions.json
  const newVersions = {
    current: {
      doc:       docId,
      name,
      effective,
      updatedAt: new Date().toISOString().slice(0, 10),
    },
    outdated: versions.current
      ? {
          doc:       versions.current.doc,
          name:      versions.current.name,
          effective: versions.current.effective,
          retired:   new Date().toISOString().slice(0, 10),
        }
      : (versions.outdated ?? null),
  };

  writeFileSync(VERS_FILE, JSON.stringify(newVersions, null, 2) + "\n", "utf-8");

  console.log("✅ Готово!");
  console.log(`   Актуальный : ${newVersions.current.name} (${newVersions.current.doc})`);
  if (newVersions.outdated) {
    console.log(`   Устаревший : ${newVersions.outdated.name} (${newVersions.outdated.doc})`);
  }
  console.log("\nНикаких изменений в коде не требуется при следующем обновлении — только запустить update.js снова.");
}

main().catch(e => {
  console.error(`\n❌ Ошибка: ${e.message}`);
  process.exit(1);
});
