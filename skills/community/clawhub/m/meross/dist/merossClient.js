"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.MerossClient = exports.DEFAULT_REGISTRY_PATH = void 0;
const meross_cloud_1 = __importDefault(require("meross-cloud"));
const logger_1 = require("./logger");
const types_1 = require("./types");
const node_path_1 = require("node:path");
exports.DEFAULT_REGISTRY_PATH = (0, node_path_1.join)(__dirname, '..', 'devices.json');
function asNonEmptyString(value) {
    if (!value) {
        return undefined;
    }
    const trimmed = value.trim();
    return trimmed.length > 0 ? trimmed : undefined;
}
function extractErrorMessage(error) {
    if (error instanceof Error) {
        return error.message;
    }
    if (typeof error === 'string') {
        return error;
    }
    return 'Unknown error';
}
function getOnlineFromDefinition(definition) {
    return definition.onlineStatus === 1;
}
function parseOnOffFromEntry(entry) {
    if (!(0, types_1.isRecord)(entry)) {
        return undefined;
    }
    const onoff = entry.onoff;
    if (typeof onoff === 'number') {
        return onoff;
    }
    return undefined;
}
function parseSwitchFromPayload(payload, channel) {
    if (!(0, types_1.isRecord)(payload)) {
        throw new types_1.SkillError('MEROSS_API_ERROR', 'Invalid response payload for switch state.');
    }
    const root = (0, types_1.isRecord)(payload.all) ? payload.all : payload;
    const digest = (0, types_1.isRecord)(root.digest) ? root.digest : root;
    const togglex = digest.togglex;
    if (Array.isArray(togglex)) {
        const byChannel = togglex.find((entry) => (0, types_1.isRecord)(entry) && entry.channel === channel);
        const exact = parseOnOffFromEntry(byChannel);
        if (exact !== undefined) {
            return exact === 1 ? 'on' : 'off';
        }
        const first = parseOnOffFromEntry(togglex[0]);
        if (first !== undefined) {
            return first === 1 ? 'on' : 'off';
        }
    }
    const singleToggleX = parseOnOffFromEntry(togglex);
    if (singleToggleX !== undefined) {
        return singleToggleX === 1 ? 'on' : 'off';
    }
    const toggle = parseOnOffFromEntry(digest.toggle);
    if (toggle !== undefined) {
        return toggle === 1 ? 'on' : 'off';
    }
    throw new types_1.SkillError('MEROSS_API_ERROR', 'No switch state found in Meross response payload.');
}
function getRawMessageNamespace(message) {
    if (!(0, types_1.isRecord)(message)) {
        return undefined;
    }
    const raw = message;
    if (!(0, types_1.isRecord)(raw.header) || typeof raw.header.namespace !== 'string') {
        return undefined;
    }
    return raw.header.namespace;
}
function getRawMessagePayload(message) {
    if (!(0, types_1.isRecord)(message)) {
        return message;
    }
    if (Object.prototype.hasOwnProperty.call(message, 'payload')) {
        return message.payload;
    }
    return message;
}
class MerossClient {
    constructor(logger = (0, logger_1.createLogger)('meross-client', MerossClient.DEFAULT_LOG_LEVEL)) {
        this.cloud = null;
        this.connectPromise = null;
        this.connected = false;
        this.shuttingDown = false;
        this.definitions = new Map();
        this.discoveryCache = null;
        this.deviceLocks = new Map();
        this.logger = logger;
        this.cacheTtlMs = MerossClient.DEFAULT_CACHE_TTL_MS;
        this.timeoutMs = MerossClient.DEFAULT_TIMEOUT_MS;
        this.region = asNonEmptyString(process.env.MEROSS_REGION);
    }
    getCloudOptions() {
        const email = asNonEmptyString(process.env.MEROSS_EMAIL);
        const password = asNonEmptyString(process.env.MEROSS_PASSWORD);
        if (!email || !password) {
            throw new types_1.SkillError('AUTH_FAILED', 'Missing Meross credentials. Set MEROSS_EMAIL and MEROSS_PASSWORD.');
        }
        return {
            email,
            password,
            timeout: this.timeoutMs,
            logger: (message) => this.logger.debug(String(message))
        };
    }
    async shutdown() {
        if (!this.cloud) {
            return;
        }
        const toClose = this.cloud;
        this.shuttingDown = true;
        this.cloud = null;
        this.connected = false;
        this.discoveryCache = null;
        this.definitions.clear();
        try {
            if (typeof toClose.disconnectAll === 'function') {
                // Force close to avoid long-lived MQTT handles keeping the CLI process alive.
                toClose.disconnectAll(true);
            }
            await Promise.race([
                new Promise((resolve) => {
                    try {
                        toClose.logout(() => resolve());
                    }
                    catch {
                        resolve();
                    }
                }),
                new Promise((resolve) => {
                    setTimeout(resolve, MerossClient.SHUTDOWN_TIMEOUT_MS);
                })
            ]);
        }
        finally {
            this.shuttingDown = false;
        }
    }
    isExpectedDisconnectError(error) {
        const message = extractErrorMessage(error).toLowerCase();
        return (message.includes('client disconnecting') ||
            message.includes('client disconnected') ||
            message.includes('connection closed'));
    }
    createCloudInstance() {
        const cloud = new meross_cloud_1.default(this.getCloudOptions());
        if (this.region) {
            this.logger.debug('MEROSS_REGION configured (library decides final region via API redirect).', {
                region: this.region
            });
        }
        cloud.on('deviceInitialized', (_deviceId, definition) => {
            this.definitions.set(definition.uuid, definition);
        });
        cloud.on('error', (error, deviceId) => {
            if (this.isExpectedDisconnectError(error)) {
                this.logger.debug('Ignoring expected Meross disconnect error.', {
                    deviceId,
                    error: String(error)
                });
                return;
            }
            this.logger.error('Meross runtime error', { deviceId, error: String(error) });
        });
        return cloud;
    }
    withTimeout(promise, timeoutMs, operation) {
        return new Promise((resolve, reject) => {
            const timer = setTimeout(() => {
                reject(new types_1.SkillError('MEROSS_API_ERROR', `${operation} timed out after ${timeoutMs}ms.`));
            }, timeoutMs);
            promise
                .then((value) => {
                clearTimeout(timer);
                resolve(value);
            })
                .catch((error) => {
                clearTimeout(timer);
                reject(error);
            });
        });
    }
    async ensureConnected(forceReconnect = false) {
        if (forceReconnect) {
            this.connected = false;
            this.cloud = null;
            this.definitions.clear();
            this.discoveryCache = null;
        }
        if (this.connected && this.cloud) {
            return;
        }
        if (this.connectPromise) {
            return this.connectPromise;
        }
        this.connectPromise = (async () => {
            if (!this.cloud) {
                this.cloud = this.createCloudInstance();
            }
            await this.withTimeout(new Promise((resolve, reject) => {
                this.cloud?.connect((error) => {
                    if (error) {
                        reject(error);
                        return;
                    }
                    resolve();
                });
            }), this.timeoutMs * 3, 'Meross connect');
            this.connected = true;
            this.discoveryCache = null;
        })();
        try {
            await this.connectPromise;
        }
        finally {
            this.connectPromise = null;
        }
    }
    isAuthError(error) {
        const message = extractErrorMessage(error).toLowerCase();
        return (message.includes('token') ||
            message.includes('auth') ||
            message.includes('email missing') ||
            message.includes('password missing') ||
            message.includes('login'));
    }
    mapMerossError(error, fallbackMessage) {
        if (error instanceof types_1.SkillError) {
            return error;
        }
        const message = extractErrorMessage(error);
        if (message.toLowerCase().includes('no data connection')) {
            return new types_1.SkillError('DEVICE_OFFLINE', 'Device is offline or not reachable.', error);
        }
        if (this.isAuthError(error)) {
            return new types_1.SkillError('AUTH_FAILED', `Meross authentication failed: ${message}`, error);
        }
        return new types_1.SkillError('MEROSS_API_ERROR', `${fallbackMessage}: ${message}`, error);
    }
    async withAuthRetry(operation) {
        try {
            return await operation();
        }
        catch (error) {
            if (!this.isAuthError(error)) {
                throw error;
            }
            this.logger.info('Auth error detected, reconnecting once.');
            await this.ensureConnected(true);
            return operation();
        }
    }
    async runWithDeviceLock(uuid, operation) {
        const previous = this.deviceLocks.get(uuid) ?? Promise.resolve();
        const next = previous.catch(() => undefined).then(operation);
        this.deviceLocks.set(uuid, next);
        try {
            return await next;
        }
        finally {
            if (this.deviceLocks.get(uuid) === next) {
                this.deviceLocks.delete(uuid);
            }
        }
    }
    getCloudDevice(uuid) {
        if (!this.cloud) {
            throw new types_1.SkillError('INTERNAL_ERROR', 'Meross cloud connection is not initialized.');
        }
        const device = this.cloud.getDevice(uuid);
        if (!device) {
            throw new types_1.SkillError('DEVICE_NOT_FOUND', `Meross cloud device '${uuid}' was not found.`);
        }
        return device;
    }
    async dispatchSwitchCommand(uuid, channel, value) {
        await this.ensureConnected();
        const device = this.getCloudDevice(uuid);
        const onoff = value === 'on';
        try {
            // Do not provide callback: meross-cloud then does not await MQTT ACK.
            device.controlToggleX(channel, onoff);
            return;
        }
        catch (error) {
            if (channel !== 0) {
                throw error;
            }
        }
        device.controlToggle(onoff);
    }
    async sleep(delayMs) {
        await new Promise((resolve) => {
            setTimeout(resolve, delayMs);
        });
    }
    async deviceCall(uuid, operationName, call, timeoutMs = this.timeoutMs * 2, rawFallbackNamespace) {
        await this.ensureConnected();
        const device = this.getCloudDevice(uuid);
        const trackingDevice = device;
        return new Promise((resolve, reject) => {
            let settled = false;
            let messageId;
            const cleanupPendingAck = () => {
                if (!messageId || !trackingDevice.waitingMessageIds) {
                    return;
                }
                const pending = trackingDevice.waitingMessageIds[messageId];
                if (!pending) {
                    return;
                }
                if (pending.timeout) {
                    clearTimeout(pending.timeout);
                }
                delete trackingDevice.waitingMessageIds[messageId];
            };
            const cleanupRawListener = () => {
                if (!rawFallbackNamespace) {
                    return;
                }
                device.removeListener('rawData', onRawData);
            };
            const settleResolve = (value) => {
                if (settled) {
                    return;
                }
                settled = true;
                clearTimeout(timeout);
                cleanupPendingAck();
                cleanupRawListener();
                resolve(value);
            };
            const settleReject = (error) => {
                if (settled) {
                    return;
                }
                settled = true;
                clearTimeout(timeout);
                cleanupPendingAck();
                cleanupRawListener();
                reject(error);
            };
            const onRawData = (rawMessage) => {
                if (!rawFallbackNamespace || settled) {
                    return;
                }
                const namespace = getRawMessageNamespace(rawMessage);
                if (namespace !== rawFallbackNamespace) {
                    return;
                }
                settleResolve(getRawMessagePayload(rawMessage));
            };
            const timeout = setTimeout(() => {
                settleReject(new types_1.SkillError('MEROSS_API_ERROR', `${operationName} timed out after ${timeoutMs}ms.`));
            }, timeoutMs);
            if (rawFallbackNamespace) {
                device.on('rawData', onRawData);
            }
            try {
                const returnedMessageId = call(device, (error, data) => {
                    if (error) {
                        settleReject(error);
                        return;
                    }
                    settleResolve(data);
                });
                if (typeof returnedMessageId === 'string') {
                    messageId = returnedMessageId;
                }
            }
            catch (error) {
                settleReject(error);
            }
        });
    }
    async readSwitchStateOnce(uuid, channel, timeoutMs = this.timeoutMs * 2) {
        const readAttempts = [
            {
                operationName: `getSystemAllData(${uuid})#warmup`,
                rawFallbackNamespace: 'Appliance.System.All',
                call: (device, callback) => device.getSystemAllData(callback)
            },
            {
                operationName: `getSystemAllData(${uuid})#retry`,
                rawFallbackNamespace: 'Appliance.System.All',
                call: (device, callback) => device.getSystemAllData(callback)
            },
            {
                operationName: `getControlToggleX(${uuid},channel=${channel})`,
                rawFallbackNamespace: 'Appliance.Control.ToggleX',
                call: (device, callback) => device.publishMessage('GET', 'Appliance.Control.ToggleX', {
                    togglex: [{ channel }]
                }, callback)
            },
            {
                operationName: `getControlToggleX(${uuid})`,
                rawFallbackNamespace: 'Appliance.Control.ToggleX',
                call: (device, callback) => device.publishMessage('GET', 'Appliance.Control.ToggleX', {}, callback)
            }
        ];
        if (channel === 0) {
            readAttempts.push({
                operationName: `getControlToggle(${uuid})`,
                rawFallbackNamespace: 'Appliance.Control.Toggle',
                call: (device, callback) => device.publishMessage('GET', 'Appliance.Control.Toggle', {}, callback)
            });
        }
        const deadline = Date.now() + timeoutMs;
        let lastError;
        for (const attempt of readAttempts) {
            const remainingMs = deadline - Date.now();
            if (remainingMs < MerossClient.MIN_STATE_READ_ATTEMPT_TIMEOUT_MS) {
                break;
            }
            const attemptTimeoutMs = Math.max(MerossClient.MIN_STATE_READ_ATTEMPT_TIMEOUT_MS, Math.min(remainingMs, MerossClient.MAX_STATE_READ_ATTEMPT_TIMEOUT_MS));
            try {
                const payload = await this.deviceCall(uuid, attempt.operationName, attempt.call, attemptTimeoutMs, attempt.rawFallbackNamespace);
                return {
                    switch: parseSwitchFromPayload(payload, channel),
                    lastUpdated: new Date().toISOString()
                };
            }
            catch (error) {
                lastError = error;
            }
        }
        if (lastError) {
            throw lastError;
        }
        throw new types_1.SkillError('MEROSS_API_ERROR', `Failed to read switch state for '${uuid}' within ${timeoutMs}ms.`);
    }
    async verifySwitchState(uuid, channel, expected) {
        let lastObserved;
        let lastError;
        for (let attempt = 1; attempt <= MerossClient.SET_VERIFY_ATTEMPTS; attempt += 1) {
            try {
                const state = await this.withAuthRetry(() => this.readSwitchStateOnce(uuid, channel, MerossClient.SET_VERIFY_READ_TIMEOUT_MS));
                lastObserved = state.switch;
                if (state.switch === expected) {
                    return {
                        verified: true,
                        verification: {
                            attempts: attempt,
                            observed: state.switch
                        }
                    };
                }
            }
            catch (error) {
                lastError = error;
            }
            if (attempt < MerossClient.SET_VERIFY_ATTEMPTS) {
                await this.sleep(MerossClient.SET_VERIFY_DELAY_MS);
            }
        }
        return {
            verified: false,
            verification: {
                attempts: MerossClient.SET_VERIFY_ATTEMPTS,
                observed: lastObserved,
                error: lastError ? extractErrorMessage(lastError) : undefined
            }
        };
    }
    collectDefinitions() {
        if (this.definitions.size > 0) {
            return Array.from(this.definitions.values());
        }
        if (!this.cloud) {
            return [];
        }
        const runtime = this.cloud;
        const fromRuntime = [];
        if (!runtime.devices) {
            return fromRuntime;
        }
        for (const value of Object.values(runtime.devices)) {
            if (value.dev) {
                fromRuntime.push(value.dev);
            }
        }
        return fromRuntime;
    }
    async discoverCloudDevices(forceRefresh = false) {
        return this.withAuthRetry(async () => {
            if (!forceRefresh && this.discoveryCache && this.discoveryCache.expiresAt > Date.now()) {
                return this.discoveryCache.devices;
            }
            await this.ensureConnected();
            const devices = this.collectDefinitions().map((definition) => ({
                uuid: definition.uuid,
                name: definition.devName || definition.uuid,
                online: getOnlineFromDefinition(definition)
            }));
            devices.sort((a, b) => a.name.localeCompare(b.name));
            this.discoveryCache = {
                expiresAt: Date.now() + this.cacheTtlMs,
                devices
            };
            return devices;
        }).catch((error) => {
            throw this.mapMerossError(error, 'Failed to discover cloud devices');
        });
    }
    async getOnlineStatus(uuid) {
        const devices = await this.discoverCloudDevices();
        const cloudDevice = devices.find((device) => device.uuid === uuid);
        if (!cloudDevice) {
            throw new types_1.SkillError('DEVICE_NOT_FOUND', `Meross cloud device '${uuid}' was not found.`);
        }
        return cloudDevice.online;
    }
    async getSwitchState(uuid, channel) {
        return this.runWithDeviceLock(uuid, async () => {
            try {
                return await this.withAuthRetry(() => this.readSwitchStateOnce(uuid, channel));
            }
            catch (error) {
                throw this.mapMerossError(error, `Failed to read switch state for '${uuid}'`);
            }
        });
    }
    async setSwitchState(uuid, channel, value) {
        return this.runWithDeviceLock(uuid, async () => {
            try {
                await this.withAuthRetry(() => this.dispatchSwitchCommand(uuid, channel, value));
                return await this.verifySwitchState(uuid, channel, value);
            }
            catch (error) {
                throw this.mapMerossError(error, `Failed to set switch state for '${uuid}'`);
            }
        });
    }
}
exports.MerossClient = MerossClient;
MerossClient.DEFAULT_CACHE_TTL_MS = 30 * 1000;
MerossClient.DEFAULT_TIMEOUT_MS = 10000;
MerossClient.DEFAULT_LOG_LEVEL = 'error';
MerossClient.SHUTDOWN_TIMEOUT_MS = 2000;
MerossClient.SET_VERIFY_ATTEMPTS = 3;
MerossClient.SET_VERIFY_DELAY_MS = 400;
MerossClient.SET_VERIFY_READ_TIMEOUT_MS = 2500;
MerossClient.MIN_STATE_READ_ATTEMPT_TIMEOUT_MS = 800;
MerossClient.MAX_STATE_READ_ATTEMPT_TIMEOUT_MS = 3500;
