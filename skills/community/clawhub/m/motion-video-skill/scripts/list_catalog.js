const { DEFAULT_TEMPLATE, listCatalogEntries } = require("./common");

function printSection(title, entries, formatter) {
  console.log(title);
  entries.forEach((entry) => {
    console.log(formatter(entry));
  });
  console.log("");
}

if (require.main === module) {
  const templates = listCatalogEntries("templates");
  const themes = listCatalogEntries("themes");
  const ttsProviders = listCatalogEntries("tts-providers");

  printSection("Templates", templates, (entry) => {
    const defaultMark = entry.id === DEFAULT_TEMPLATE ? " (default)" : "";
    return `- ${entry.id}${defaultMark}: ${entry.label} · ${entry.theme} · ${entry.description}`;
  });

  printSection("Themes", themes, (entry) => {
    return `- ${entry.id}: ${entry.label}${entry.description ? ` · ${entry.description}` : ""}`;
  });

  printSection("TTS Providers", ttsProviders, (entry) => {
    const status = entry.id === "system" || entry.implementedAdapter === true ? "implemented" : "config-only";
    return `- ${entry.id}: ${entry.label} · ${entry.type} · ${status} · ${entry.description}`;
  });
}
