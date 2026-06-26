"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const logger_1 = require("./logger");
const merossClient_1 = require("./merossClient");
const registry_1 = require("./registry");
const types_1 = require("./types");
const VALID_COMMANDS = [
    'list-devices',
    'get-state',
    'set-device',
    'discover-cloud-devices',
    'setup-once'
];
const logger = (0, logger_1.createLogger)('cli', 'error');
function isCommand(value) {
    return VALID_COMMANDS.includes(value);
}
function parseJsonInput(raw) {
    try {
        return JSON.parse(raw);
    }
    catch (error) {
        throw new types_1.SkillError('INVALID_INPUT', 'Input must be valid JSON.', error);
    }
}
async function readStdinIfAvailable() {
    if (process.stdin.isTTY) {
        return undefined;
    }
    return new Promise((resolve, reject) => {
        let data = '';
        process.stdin.setEncoding('utf8');
        process.stdin.on('data', (chunk) => {
            data += chunk;
        });
        process.stdin.on('end', () => resolve(data));
        process.stdin.on('error', reject);
    });
}
function parseObjectInput(input, command) {
    if (!(0, types_1.isRecord)(input)) {
        throw new types_1.SkillError('INVALID_INPUT', `${command} payload must be a JSON object.`);
    }
    return input;
}
function parseDeviceId(input) {
    if (!(0, types_1.isRecord)(input) || typeof input.deviceId !== 'string') {
        throw new types_1.SkillError('INVALID_INPUT', "Input must contain string field 'deviceId'.");
    }
    const deviceId = (0, types_1.normalizeWhitespace)(input.deviceId);
    if (deviceId.length === 0) {
        throw new types_1.SkillError('INVALID_INPUT', "Field 'deviceId' cannot be empty.");
    }
    return deviceId;
}
function parseSwitchValue(value) {
    if (value === 'on' || value === 'off') {
        return value;
    }
    throw new types_1.SkillError('INVALID_INPUT', "Field 'value' must be 'on' or 'off'.");
}
function parseCapability(value) {
    if (value === 'switch') {
        return value;
    }
    throw new types_1.SkillError('INVALID_INPUT', "Field 'capability' must be 'switch'.");
}
function requireSwitchConfirmation(input, device, capability, value) {
    const expected = {
        userConfirmed: true,
        deviceId: device.deviceId,
        capability,
        value
    };
    if (!(0, types_1.isRecord)(input.confirmation)) {
        throw new types_1.SkillError('CONFIRMATION_REQUIRED', `set-device requires explicit user confirmation: ${JSON.stringify(expected)}.`);
    }
    if (input.confirmation.userConfirmed !== true ||
        input.confirmation.deviceId !== expected.deviceId ||
        input.confirmation.capability !== expected.capability ||
        input.confirmation.value !== expected.value) {
        throw new types_1.SkillError('CONFIRMATION_REQUIRED', `Confirmation must exactly match target/action: ${JSON.stringify(expected)}.`);
    }
}
function normalizeUuid(uuid) {
    const normalized = (0, types_1.normalizeWhitespace)(uuid).toLowerCase();
    if (!normalized) {
        throw new types_1.SkillError('MEROSS_API_ERROR', `Invalid Meross UUID '${uuid}'.`);
    }
    return normalized;
}
function uuidKey(uuid) {
    const compact = normalizeUuid(uuid).replace(/[^a-z0-9]/g, '');
    if (!compact) {
        throw new types_1.SkillError('MEROSS_API_ERROR', `Invalid Meross UUID '${uuid}'.`);
    }
    return compact;
}
function uniqueAliases(...sources) {
    const result = [];
    const seen = new Set();
    for (const source of sources) {
        for (const aliasRaw of source) {
            const alias = (0, types_1.normalizeWhitespace)(aliasRaw);
            if (!alias) {
                continue;
            }
            const key = alias.toLowerCase();
            if (seen.has(key)) {
                continue;
            }
            seen.add(key);
            result.push(alias);
        }
    }
    return result;
}
function sameDevice(a, b) {
    return JSON.stringify(a) === JSON.stringify(b);
}
async function parseInputPayload(rawArg) {
    if (rawArg && rawArg.trim().length > 0) {
        return parseJsonInput(rawArg);
    }
    const stdin = await readStdinIfAvailable();
    if (stdin && stdin.trim().length > 0) {
        return parseJsonInput(stdin);
    }
    return {};
}
function printSuccess(payload) {
    process.stdout.write(`${JSON.stringify(payload)}\n`);
}
function printErrorAndExit(error) {
    const payload = (0, types_1.toErrorPayload)(error);
    process.stderr.write(`${JSON.stringify(payload)}\n`);
    process.exit(1);
}
async function handleListDevices(client) {
    const devices = await (0, registry_1.readRegistryDevices)();
    let cloudMap = new Map();
    try {
        const cloudDevices = await client.discoverCloudDevices();
        cloudMap = new Map(cloudDevices.map((device) => [uuidKey(device.uuid), device.online]));
    }
    catch (error) {
        logger.info('Cloud discovery failed during list-devices; returning registry-only list.', {
            error: error instanceof Error ? error.message : String(error)
        });
    }
    return {
        devices: devices.map((device) => ({
            deviceId: device.deviceId,
            aliases: device.aliases,
            online: cloudMap.get(uuidKey(device.meross.uuid)) ?? false,
            capabilities: device.capabilities,
            meross: device.meross
        }))
    };
}
async function handleGetState(client, input) {
    const deviceId = parseDeviceId(input);
    const device = await (0, registry_1.getDeviceById)(deviceId);
    if (!device) {
        throw new types_1.SkillError('DEVICE_NOT_FOUND', `No device with deviceId '${deviceId}' found in registry.`);
    }
    if (!device.capabilities.includes('switch')) {
        throw new types_1.SkillError('INVALID_INPUT', `Device '${device.deviceId}' does not support switch capability.`);
    }
    const online = await client.getOnlineStatus(device.meross.uuid);
    if (!online) {
        throw new types_1.SkillError('DEVICE_OFFLINE', `Device '${device.deviceId}' is offline.`);
    }
    const state = await client.getSwitchState(device.meross.uuid, device.meross.channel);
    return {
        deviceId: device.deviceId,
        online,
        state
    };
}
async function handleSetDevice(client, input) {
    if (!(0, types_1.isRecord)(input)) {
        throw new types_1.SkillError('INVALID_INPUT', 'set-device payload must be an object.');
    }
    const deviceId = parseDeviceId(input);
    const capability = parseCapability(input.capability);
    const value = parseSwitchValue(input.value);
    const device = await (0, registry_1.getDeviceById)(deviceId);
    if (!device) {
        throw new types_1.SkillError('DEVICE_NOT_FOUND', `No device with deviceId '${deviceId}' found in registry.`);
    }
    if (!device.capabilities.includes(capability)) {
        throw new types_1.SkillError('INVALID_INPUT', `Device '${device.deviceId}' does not support capability '${capability}'.`);
    }
    requireSwitchConfirmation(input, device, capability, value);
    const online = await client.getOnlineStatus(device.meross.uuid);
    if (!online) {
        throw new types_1.SkillError('DEVICE_OFFLINE', `Device '${device.deviceId}' is offline.`);
    }
    const setResult = await client.setSwitchState(device.meross.uuid, device.meross.channel, value);
    const response = {
        ok: true,
        deviceId: device.deviceId,
        applied: {
            capability,
            value
        },
        at: new Date().toISOString(),
        verified: setResult.verified
    };
    if (!setResult.verified) {
        response.verification = setResult.verification;
    }
    return response;
}
async function handleDiscoverCloudDevices(client) {
    const devices = await client.discoverCloudDevices(true);
    return {
        devices: devices.map((device) => ({
            uuid: normalizeUuid(device.uuid),
            name: device.name,
            online: device.online
        }))
    };
}
async function handleSetupOnce(client, input) {
    parseObjectInput(input, 'setup-once');
    const [discovered, existing] = await Promise.all([
        client.discoverCloudDevices(true),
        (0, registry_1.readRegistryDevices)()
    ]);
    const existingByUuid = new Map();
    for (const device of existing) {
        existingByUuid.set(uuidKey(device.meross.uuid), device);
    }
    const counts = {
        discovered: discovered.length,
        written: 0,
        updated: 0,
        added: 0
    };
    const nextDevices = discovered.map((cloudDevice) => {
        const uuid = normalizeUuid(cloudDevice.uuid);
        const key = uuidKey(uuid);
        const existingDevice = existingByUuid.get(key);
        const nextDevice = {
            deviceId: `plug_${key}`,
            aliases: uniqueAliases(existingDevice?.aliases ?? [], cloudDevice.name ? [cloudDevice.name] : []),
            meross: {
                uuid,
                channel: 0
            },
            capabilities: ['switch']
        };
        if (!existingDevice) {
            counts.added += 1;
            return nextDevice;
        }
        if (!sameDevice(existingDevice, nextDevice)) {
            counts.updated += 1;
        }
        return nextDevice;
    });
    counts.written = nextDevices.length;
    await (0, registry_1.writeRegistryDevices)(nextDevices);
    return {
        ok: true,
        at: new Date().toISOString(),
        registryPath: (0, registry_1.getRegistryPathForDisplay)(),
        counts
    };
}
async function run() {
    const commandArg = process.argv[2];
    if (!commandArg || !isCommand(commandArg)) {
        throw new types_1.SkillError('INVALID_INPUT', `Unknown command. Use one of: ${VALID_COMMANDS.join(', ')}.`);
    }
    const payload = await parseInputPayload(process.argv[3]);
    const client = new merossClient_1.MerossClient();
    let result;
    try {
        if (commandArg === 'list-devices') {
            result = await handleListDevices(client);
        }
        else if (commandArg === 'get-state') {
            result = await handleGetState(client, payload);
        }
        else if (commandArg === 'set-device') {
            result = await handleSetDevice(client, payload);
        }
        else if (commandArg === 'discover-cloud-devices') {
            result = await handleDiscoverCloudDevices(client);
        }
        else if (commandArg === 'setup-once') {
            result = await handleSetupOnce(client, payload);
        }
        else {
            throw new types_1.SkillError('INVALID_INPUT', `Unsupported command '${commandArg}'.`);
        }
    }
    finally {
        await client.shutdown();
    }
    printSuccess(result);
}
run().catch((error) => {
    printErrorAndExit(error);
});
process.on('unhandledRejection', (error) => {
    printErrorAndExit(error);
});
