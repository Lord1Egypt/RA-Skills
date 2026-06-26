"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.normalizeAlias = normalizeAlias;
exports.findDevicesByAlias = findDevicesByAlias;
exports.resolveDeviceByAlias = resolveDeviceByAlias;
exports.readRegistryDevices = readRegistryDevices;
exports.getDeviceById = getDeviceById;
exports.writeRegistryDevices = writeRegistryDevices;
exports.getRegistryPathForDisplay = getRegistryPathForDisplay;
const promises_1 = require("node:fs/promises");
const node_path_1 = require("node:path");
const types_1 = require("./types");
const merossClient_1 = require("./merossClient");
function uniqueStrings(values) {
    const result = [];
    const seen = new Set();
    for (const raw of values) {
        const clean = (0, types_1.normalizeWhitespace)(raw);
        if (clean.length === 0) {
            continue;
        }
        const key = clean.toLowerCase();
        if (seen.has(key)) {
            continue;
        }
        seen.add(key);
        result.push(clean);
    }
    return result;
}
function normalizeCapabilities(capabilities) {
    if (!Array.isArray(capabilities)) {
        return ['switch'];
    }
    const filtered = capabilities
        .map((value) => String(value).trim().toLowerCase())
        .filter((value) => value === 'switch');
    return filtered.length > 0 ? ['switch'] : ['switch'];
}
function sanitizeDevice(raw) {
    if (!(0, types_1.isRecord)(raw)) {
        throw new types_1.SkillError('REGISTRY_ERROR', 'Registry contains an invalid device entry.');
    }
    const deviceIdRaw = raw.deviceId;
    if (typeof deviceIdRaw !== 'string' || (0, types_1.normalizeWhitespace)(deviceIdRaw).length === 0) {
        throw new types_1.SkillError('REGISTRY_ERROR', 'Registry device is missing a valid deviceId.');
    }
    const deviceId = (0, types_1.normalizeWhitespace)(deviceIdRaw);
    const aliasesRaw = Array.isArray(raw.aliases) ? raw.aliases.map((value) => String(value)) : [];
    const aliases = uniqueStrings(aliasesRaw);
    if (!(0, types_1.isRecord)(raw.meross)) {
        throw new types_1.SkillError('REGISTRY_ERROR', `Registry device '${deviceId}' is missing meross binding.`);
    }
    const uuidRaw = raw.meross.uuid;
    const channelRaw = raw.meross.channel;
    if (typeof uuidRaw !== 'string' || (0, types_1.normalizeWhitespace)(uuidRaw).length === 0) {
        throw new types_1.SkillError('REGISTRY_ERROR', `Registry device '${deviceId}' has invalid meross.uuid.`);
    }
    const channelNumber = typeof channelRaw === 'number' ? channelRaw : Number(channelRaw);
    if (!Number.isInteger(channelNumber) || channelNumber < 0) {
        throw new types_1.SkillError('REGISTRY_ERROR', `Registry device '${deviceId}' has invalid meross.channel.`);
    }
    return {
        deviceId,
        aliases,
        meross: {
            uuid: (0, types_1.normalizeWhitespace)(uuidRaw),
            channel: channelNumber
        },
        capabilities: normalizeCapabilities(raw.capabilities)
    };
}
function sanitizeRegistry(raw) {
    if (!(0, types_1.isRecord)(raw)) {
        throw new types_1.SkillError('REGISTRY_ERROR', 'Registry root must be an object.');
    }
    const rawDevices = raw.devices;
    if (!Array.isArray(rawDevices)) {
        return { devices: [] };
    }
    const devices = rawDevices.map((device) => sanitizeDevice(device));
    const seenDeviceIds = new Set();
    for (const device of devices) {
        const key = device.deviceId.toLowerCase();
        if (seenDeviceIds.has(key)) {
            throw new types_1.SkillError('REGISTRY_ERROR', `Duplicate deviceId '${device.deviceId}' in registry.`);
        }
        seenDeviceIds.add(key);
    }
    return { devices };
}
async function ensureRegistryFile(path) {
    await (0, promises_1.mkdir)((0, node_path_1.dirname)(path), { recursive: true });
    try {
        await (0, promises_1.readFile)(path, 'utf8');
    }
    catch {
        await (0, promises_1.writeFile)(path, JSON.stringify({ devices: [] }, null, 2), { encoding: 'utf8', mode: 0o600 });
    }
    try {
        await (0, promises_1.chmod)(path, 0o600);
    }
    catch {
        // Best-effort only; chmod is not reliable on every filesystem.
    }
}
async function writeRegistry(path, data) {
    const tmpPath = `${path}.${process.pid}.${Date.now()}.tmp`;
    const json = `${JSON.stringify(data, null, 2)}\n`;
    await (0, promises_1.writeFile)(tmpPath, json, { encoding: 'utf8', mode: 0o600 });
    await (0, promises_1.rename)(tmpPath, path);
    try {
        await (0, promises_1.chmod)(path, 0o600);
    }
    catch {
        // Best-effort only; chmod is not reliable on every filesystem.
    }
}
function normalizeAlias(alias) {
    return (0, types_1.normalizeWhitespace)(alias).toLowerCase();
}
function findDevicesByAlias(devices, alias) {
    const normalized = normalizeAlias(alias);
    if (!normalized) {
        return [];
    }
    return devices.filter((device) => {
        return device.aliases.some((deviceAlias) => normalizeAlias(deviceAlias) === normalized);
    });
}
function resolveDeviceByAlias(devices, aliasOrId, allowUniqueFuzzy = false) {
    const token = (0, types_1.normalizeWhitespace)(aliasOrId);
    if (token.length === 0) {
        return undefined;
    }
    const direct = devices.find((device) => device.deviceId.toLowerCase() === token.toLowerCase());
    if (direct) {
        return direct;
    }
    const exactAliasMatches = findDevicesByAlias(devices, token);
    if (exactAliasMatches.length === 1) {
        return exactAliasMatches[0];
    }
    if (exactAliasMatches.length > 1) {
        throw new types_1.SkillError('AMBIGUOUS_DEVICE', `Alias '${token}' matches multiple devices.`);
    }
    if (!allowUniqueFuzzy) {
        return undefined;
    }
    const normalizedToken = normalizeAlias(token);
    const fuzzyMatches = devices.filter((device) => device.aliases.some((alias) => normalizeAlias(alias).includes(normalizedToken)));
    if (fuzzyMatches.length === 1) {
        return fuzzyMatches[0];
    }
    if (fuzzyMatches.length > 1) {
        throw new types_1.SkillError('AMBIGUOUS_DEVICE', `Alias '${token}' fuzzy-matches multiple devices.`);
    }
    return undefined;
}
async function readRegistryDevices() {
    const registryPath = merossClient_1.DEFAULT_REGISTRY_PATH;
    try {
        await ensureRegistryFile(registryPath);
        const raw = await (0, promises_1.readFile)(registryPath, 'utf8');
        const parsed = JSON.parse(raw);
        const registry = sanitizeRegistry(parsed);
        return registry.devices;
    }
    catch (error) {
        if (error instanceof types_1.SkillError) {
            throw error;
        }
        throw new types_1.SkillError('REGISTRY_ERROR', `Failed to read registry '${registryPath}'.`, error);
    }
}
async function getDeviceById(deviceId) {
    const normalized = (0, types_1.normalizeWhitespace)(deviceId);
    const devices = await readRegistryDevices();
    return devices.find((device) => device.deviceId.toLowerCase() === normalized.toLowerCase());
}
async function writeRegistryDevices(devices) {
    const registryPath = merossClient_1.DEFAULT_REGISTRY_PATH;
    try {
        await ensureRegistryFile(registryPath);
        const next = sanitizeRegistry({ devices });
        next.devices.sort((a, b) => a.deviceId.localeCompare(b.deviceId));
        await writeRegistry(registryPath, next);
    }
    catch (error) {
        if (error instanceof types_1.SkillError) {
            throw error;
        }
        throw new types_1.SkillError('REGISTRY_ERROR', `Failed to write registry '${registryPath}'.`, error);
    }
}
function getRegistryPathForDisplay() {
    return merossClient_1.DEFAULT_REGISTRY_PATH;
}
