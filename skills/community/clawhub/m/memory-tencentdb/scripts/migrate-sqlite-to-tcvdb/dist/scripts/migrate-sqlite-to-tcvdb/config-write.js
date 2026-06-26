import fs from "node:fs/promises";
import JSON5 from "json5";
function asRecord(value) {
    return value !== null && typeof value === "object" && !Array.isArray(value)
        ? { ...value }
        : {};
}
export function buildMigrationPluginConfigPatch(target) {
    return {
        storeBackend: "tcvdb",
        tcvdb: {
            url: target.url,
            username: target.username,
            apiKey: target.apiKey,
            database: target.database,
            alias: target.alias,
            embeddingModel: target.embeddingModel,
            timeout: target.timeout,
        },
        bm25: {
            enabled: target.bm25Enabled,
            language: target.bm25Language,
        },
    };
}
function applyPluginConfigPatch(sourceConfig, pluginId, patch) {
    const nextConfig = asRecord(sourceConfig);
    const plugins = asRecord(nextConfig.plugins);
    const entries = asRecord(plugins.entries);
    const targetEntry = asRecord(entries[pluginId]);
    const targetPluginConfig = asRecord(targetEntry.config);
    const patchTcvdb = asRecord(patch.tcvdb);
    const patchBm25 = asRecord(patch.bm25);
    const mergedPluginConfig = {
        ...targetPluginConfig,
        ...patch,
        tcvdb: {
            ...asRecord(targetPluginConfig.tcvdb),
            ...patchTcvdb,
        },
        bm25: {
            ...asRecord(targetPluginConfig.bm25),
            ...patchBm25,
        },
    };
    entries[pluginId] = {
        ...targetEntry,
        config: mergedPluginConfig,
    };
    plugins.entries = entries;
    nextConfig.plugins = plugins;
    return nextConfig;
}
export async function writeMigrationPluginConfig(params, deps = {}) {
    const fsImpl = deps.fs ?? fs;
    const parseConfig = deps.parseConfig ?? ((raw) => JSON5.parse(raw));
    let parsed;
    try {
        parsed = parseConfig(await fsImpl.readFile(params.configPath, "utf-8"));
    }
    catch {
        throw new Error(`Config migration writer only supports single-file JSON/JSON5: ${params.configPath}`);
    }
    const nextConfig = applyPluginConfigPatch(asRecord(parsed), params.pluginId, buildMigrationPluginConfigPatch({
        ...params.tcvdb,
        bm25Enabled: params.bm25.enabled,
        bm25Language: params.bm25.language,
    }));
    await fsImpl.writeFile(params.configPath, `${JSON.stringify(nextConfig, null, 2)}\n`, "utf-8");
}
