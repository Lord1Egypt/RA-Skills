"use strict";
/**
 * OpenClaw POWPOW Integration Skill v2.1.10
 *
 * WebSocket-based real-time bidirectional chat with POWPOW digital humans
 */
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.logger = exports.powpowSkillPlugin = exports.PowPowSkill = void 0;
const events_1 = require("events");
const ws_1 = __importDefault(require("ws"));
const logger_1 = require("./utils/logger");
Object.defineProperty(exports, "logger", { enumerable: true, get: function () { return logger_1.logger; } });
const validator_1 = require("./utils/validator");
const constants_1 = require("./utils/constants");
// ============================================================================
// PowPowSkill Class
// ============================================================================
class PowPowSkill extends events_1.EventEmitter {
    constructor(config) {
        super();
        this.ws = null;
        this.isConnected = false;
        this.reconnectTimer = null;
        this.heartbeatTimer = null;
        this.messageQueue = [];
        this.connectionStartTime = null;
        this.reconnectAttempts = 0;
        this.connectionTimeout = null;
        // 验证必要参数
        const dhValidation = (0, validator_1.validateDigitalHumanId)(config.digitalHumanId);
        if (!dhValidation.valid) {
            throw new Error(`Invalid digitalHumanId: ${dhValidation.error}`);
        }
        const userValidation = (0, validator_1.validateUserId)(config.openclawUserId);
        if (!userValidation.valid) {
            throw new Error(`Invalid openclawUserId: ${userValidation.error}`);
        }
        const urlValidation = (0, validator_1.validateWebSocketUrl)(config.wsUrl);
        if (!urlValidation.valid) {
            throw new Error(`Invalid wsUrl: ${urlValidation.error}`);
        }
        this.config = {
            autoReconnect: true,
            reconnectInterval: constants_1.WS_CONFIG.RECONNECT_INTERVAL,
            maxReconnectAttempts: constants_1.WS_CONFIG.MAX_RECONNECT_ATTEMPTS,
            ...config,
        };
        logger_1.logger.info('PowPowSkill initialized', {
            digitalHumanId: config.digitalHumanId,
            wsUrl: config.wsUrl,
        });
    }
    /**
     * Connect to POWPOW WebSocket server
     */
    connect() {
        return new Promise((resolve, reject) => {
            if (this.isConnected) {
                logger_1.logger.warn('Already connected');
                resolve();
                return;
            }
            try {
                const wsUrl = `${this.config.wsUrl}?client=openclaw&digitalHumanId=${this.config.digitalHumanId}&userId=${this.config.openclawUserId}`;
                logger_1.logger.info('Connecting to WebSocket:', wsUrl);
                this.ws = new ws_1.default(wsUrl);
                // 设置连接超时
                this.connectionTimeout = setTimeout(() => {
                    if (!this.isConnected) {
                        logger_1.logger.error('Connection timeout');
                        this.ws?.terminate();
                        reject(new Error('Connection timeout'));
                    }
                }, constants_1.WS_CONFIG.CONNECTION_TIMEOUT);
                this.ws.on('open', () => {
                    logger_1.logger.info('WebSocket connected');
                    this.isConnected = true;
                    this.connectionStartTime = new Date();
                    this.reconnectAttempts = 0;
                    if (this.connectionTimeout) {
                        clearTimeout(this.connectionTimeout);
                        this.connectionTimeout = null;
                    }
                    this.startHeartbeat();
                    this.emit('connected');
                    this.flushMessageQueue();
                    resolve();
                });
                this.ws.on('message', (data) => {
                    try {
                        const message = JSON.parse(data.toString());
                        this.handleMessage(message);
                    }
                    catch (error) {
                        logger_1.logger.error('Failed to parse message:', error);
                        this.emit('error', new Error('Failed to parse message'));
                    }
                });
                this.ws.on('close', (code, reason) => {
                    logger_1.logger.info('WebSocket closed:', { code, reason: reason.toString() });
                    this.cleanup();
                    this.emit('disconnected', { code, reason: reason.toString() });
                    if (this.config.autoReconnect && this.reconnectAttempts < (this.config.maxReconnectAttempts || constants_1.WS_CONFIG.MAX_RECONNECT_ATTEMPTS)) {
                        this.scheduleReconnect();
                    }
                });
                this.ws.on('error', (error) => {
                    logger_1.logger.error('WebSocket error:', error);
                    this.emit('error', error);
                    reject(error);
                });
                this.ws.on('ping', () => {
                    logger_1.logger.debug('Received ping');
                    this.ws?.pong();
                });
                this.ws.on('pong', () => {
                    logger_1.logger.debug('Received pong');
                });
            }
            catch (error) {
                logger_1.logger.error('Failed to create connection:', error);
                reject(error);
            }
        });
    }
    /**
     * Disconnect from WebSocket server
     */
    disconnect() {
        logger_1.logger.info('Disconnecting...');
        this.cleanup();
        this.reconnectAttempts = this.config.maxReconnectAttempts || constants_1.WS_CONFIG.MAX_RECONNECT_ATTEMPTS; // 阻止自动重连
    }
    /**
     * Cleanup resources
     */
    cleanup() {
        if (this.reconnectTimer) {
            clearTimeout(this.reconnectTimer);
            this.reconnectTimer = null;
        }
        if (this.heartbeatTimer) {
            clearInterval(this.heartbeatTimer);
            this.heartbeatTimer = null;
        }
        if (this.connectionTimeout) {
            clearTimeout(this.connectionTimeout);
            this.connectionTimeout = null;
        }
        if (this.ws) {
            try {
                this.ws.close();
            }
            catch (error) {
                logger_1.logger.error('Error closing WebSocket:', error);
            }
            this.ws = null;
        }
        this.isConnected = false;
        this.connectionStartTime = null;
    }
    /**
     * Start heartbeat
     */
    startHeartbeat() {
        this.heartbeatTimer = setInterval(() => {
            if (this.ws?.readyState === ws_1.default.OPEN) {
                logger_1.logger.debug('Sending ping');
                this.ws.ping();
            }
        }, constants_1.WS_CONFIG.HEARTBEAT_INTERVAL);
    }
    /**
     * Send chat message
     */
    sendMessage(content, contentType = 'text', options) {
        // 验证输入
        const contentValidation = (0, validator_1.validateMessage)(content);
        if (!contentValidation.valid) {
            logger_1.logger.error('Invalid message content:', contentValidation.error);
            throw new Error(contentValidation.error);
        }
        const typeValidation = (0, validator_1.validateContentType)(contentType);
        if (!typeValidation.valid) {
            logger_1.logger.error('Invalid content type:', typeValidation.error);
            throw new Error(typeValidation.error);
        }
        // 验证多媒体参数
        if (contentType === 'voice' || contentType === 'image') {
            if (!options?.mediaUrl) {
                throw new Error('mediaUrl is required for voice/image messages');
            }
            const urlValidation = (0, validator_1.validateMediaUrl)(options.mediaUrl);
            if (!urlValidation.valid) {
                throw new Error(urlValidation.error);
            }
        }
        if (contentType === 'voice' && options?.duration !== undefined) {
            const durationValidation = (0, validator_1.validateDuration)(options.duration);
            if (!durationValidation.valid) {
                throw new Error(durationValidation.error);
            }
        }
        // 清理内容防止 XSS
        const sanitizedContent = (0, validator_1.sanitizeString)(content);
        const message = {
            digitalHumanId: this.config.digitalHumanId,
            senderType: constants_1.SENDER_TYPES.OPENCLAW,
            senderId: this.config.openclawUserId,
            content: sanitizedContent,
            contentType,
            ...options,
            timestamp: new Date().toISOString(),
        };
        if (this.isConnected && this.ws?.readyState === ws_1.default.OPEN) {
            try {
                this.ws.send(JSON.stringify({
                    type: constants_1.WS_MESSAGE_TYPES.CHAT_MESSAGE,
                    data: message,
                }));
                logger_1.logger.info('Message sent');
                return true;
            }
            catch (error) {
                logger_1.logger.error('Failed to send message:', error);
                this.messageQueue.push(message);
                return false;
            }
        }
        else {
            // 检查队列是否已满
            if (this.messageQueue.length >= constants_1.MESSAGE_CONFIG.QUEUE_SIZE) {
                logger_1.logger.error('Message queue is full');
                throw new Error('Message queue is full');
            }
            this.messageQueue.push(message);
            logger_1.logger.info('Message queued for later delivery');
            return false;
        }
    }
    /**
     * Quick reply
     */
    reply(content) {
        return this.sendMessage(content, constants_1.CONTENT_TYPES.TEXT);
    }
    /**
     * Send voice message
     */
    sendVoice(content, mediaUrl, duration) {
        return this.sendMessage(content, constants_1.CONTENT_TYPES.VOICE, { mediaUrl, duration });
    }
    /**
     * Send image message
     */
    sendImage(content, mediaUrl) {
        return this.sendMessage(content, constants_1.CONTENT_TYPES.IMAGE, { mediaUrl });
    }
    /**
     * Get connection status
     */
    getConnectionStatus() {
        let duration;
        if (this.connectionStartTime) {
            duration = Date.now() - this.connectionStartTime.getTime();
        }
        return {
            connected: this.isConnected,
            digitalHumanId: this.config.digitalHumanId,
            duration,
            reconnectAttempts: this.reconnectAttempts,
        };
    }
    /**
     * Handle incoming messages
     */
    handleMessage(message) {
        logger_1.logger.debug('Received message:', message.type);
        switch (message.type) {
            case constants_1.WS_MESSAGE_TYPES.CONNECTED:
                logger_1.logger.info('Connection confirmed:', message.data);
                this.emit('connectionConfirmed', message.data);
                break;
            case constants_1.WS_MESSAGE_TYPES.CHAT_MESSAGE:
                this.emit('message', message.data);
                break;
            case constants_1.WS_MESSAGE_TYPES.CHAT_MESSAGE_ACK:
                logger_1.logger.info('Message delivered:', message.data);
                this.emit('messageAck', message.data);
                break;
            case constants_1.WS_MESSAGE_TYPES.ERROR:
                logger_1.logger.error('Server error:', message.data);
                this.emit('serverError', message.data);
                break;
            case constants_1.WS_MESSAGE_TYPES.PING:
                logger_1.logger.debug('Received ping from server');
                break;
            case constants_1.WS_MESSAGE_TYPES.PONG:
                logger_1.logger.debug('Received pong from server');
                break;
            default:
                logger_1.logger.warn('Unknown message type:', message.type);
        }
    }
    /**
     * Flush queued messages
     */
    flushMessageQueue() {
        if (this.messageQueue.length === 0)
            return;
        logger_1.logger.info(`Flushing ${this.messageQueue.length} queued messages`);
        while (this.messageQueue.length > 0) {
            const message = this.messageQueue.shift();
            if (message && this.ws?.readyState === ws_1.default.OPEN) {
                try {
                    this.ws.send(JSON.stringify({
                        type: constants_1.WS_MESSAGE_TYPES.CHAT_MESSAGE,
                        data: message,
                    }));
                }
                catch (error) {
                    logger_1.logger.error('Failed to send queued message:', error);
                    // 放回队列开头
                    this.messageQueue.unshift(message);
                    break;
                }
            }
        }
    }
    /**
     * Schedule reconnection
     */
    scheduleReconnect() {
        if (this.reconnectTimer) {
            clearTimeout(this.reconnectTimer);
        }
        this.reconnectAttempts++;
        const delay = Math.min(this.config.reconnectInterval * Math.pow(2, this.reconnectAttempts - 1), 30000 // 最大30秒
        );
        logger_1.logger.info(`Reconnecting in ${delay}ms... (attempt ${this.reconnectAttempts})`);
        this.emit('reconnecting', { attempt: this.reconnectAttempts, delay });
        this.reconnectTimer = setTimeout(() => {
            this.connect().catch((error) => {
                logger_1.logger.error('Reconnection failed:', error);
            });
        }, delay);
    }
}
exports.PowPowSkill = PowPowSkill;
const powpowSkillPlugin = {
    name: 'powpow-integration',
    version: '2.1.10',
    description: 'POWPOW WebSocket Integration - Real-time bidirectional chat with POWPOW digital humans',
    init(context) {
        logger_1.logger.info('Plugin initialized');
        context.powpowConfig = {
            defaultWsUrl: constants_1.WS_CONFIG.DEFAULT_URL,
            autoReconnect: true,
            reconnectInterval: constants_1.WS_CONFIG.RECONNECT_INTERVAL,
            maxReconnectAttempts: constants_1.WS_CONFIG.MAX_RECONNECT_ATTEMPTS,
        };
    },
    destroy() {
        logger_1.logger.info('Plugin destroyed');
    },
    commands: {
        /**
         * Connect to POWPOW
         */
        async connect(params, context) {
            try {
                const wsUrl = params.wsUrl || context.config?.wsUrl || constants_1.WS_CONFIG.DEFAULT_URL;
                // 验证参数
                const dhValidation = (0, validator_1.validateDigitalHumanId)(params.digitalHumanId);
                if (!dhValidation.valid) {
                    return { success: false, error: dhValidation.error };
                }
                const skill = new PowPowSkill({
                    wsUrl,
                    digitalHumanId: params.digitalHumanId,
                    openclawUserId: context.userId,
                    autoReconnect: true,
                    reconnectInterval: constants_1.WS_CONFIG.RECONNECT_INTERVAL,
                    maxReconnectAttempts: constants_1.WS_CONFIG.MAX_RECONNECT_ATTEMPTS,
                });
                skill.on('message', (message) => {
                    context.emit('powpow.message.received', message);
                });
                skill.on('error', (error) => {
                    context.emit('powpow.error', error);
                });
                skill.on('reconnecting', (data) => {
                    context.emit('powpow.reconnecting', data);
                });
                await skill.connect();
                context.powpowSkill = skill;
                return {
                    success: true,
                    message: 'Connected to POWPOW',
                    digitalHumanId: params.digitalHumanId,
                };
            }
            catch (error) {
                logger_1.logger.error('Connect command failed:', error);
                return {
                    success: false,
                    error: error instanceof Error ? error.message : 'Unknown error',
                };
            }
        },
        /**
         * Disconnect from POWPOW
         */
        disconnect(params, context) {
            const skill = context.powpowSkill;
            if (skill) {
                skill.disconnect();
                delete context.powpowSkill;
                return { success: true, message: 'Disconnected from POWPOW' };
            }
            return { success: false, error: 'Not connected' };
        },
        /**
         * Get connection status
         */
        status(params, context) {
            const skill = context.powpowSkill;
            if (!skill) {
                return { success: false, status: 'disconnected', message: 'Not connected' };
            }
            const status = skill.getConnectionStatus();
            return {
                success: true,
                status: status.connected ? 'connected' : 'disconnected',
                digitalHumanId: status.digitalHumanId,
                duration: status.duration,
                reconnectAttempts: status.reconnectAttempts,
                message: status.connected ? 'Connected' : 'Disconnected',
            };
        },
        /**
         * Send message
         */
        send(params, context) {
            try {
                const skill = context.powpowSkill;
                if (!skill) {
                    return { success: false, error: 'Not connected to POWPOW' };
                }
                const contentType = (params.contentType || 'text');
                const sent = skill.sendMessage(params.message, contentType);
                return {
                    success: sent,
                    message: sent ? 'Message sent' : 'Message queued for delivery',
                };
            }
            catch (error) {
                logger_1.logger.error('Send command failed:', error);
                return {
                    success: false,
                    error: error instanceof Error ? error.message : 'Unknown error',
                };
            }
        },
        /**
         * Quick reply
         */
        reply(params, context) {
            try {
                const skill = context.powpowSkill;
                if (!skill) {
                    return { success: false, error: 'Not connected to POWPOW' };
                }
                const sent = skill.reply(params.message);
                return {
                    success: sent,
                    message: sent ? 'Reply sent' : 'Reply queued for delivery',
                };
            }
            catch (error) {
                logger_1.logger.error('Reply command failed:', error);
                return {
                    success: false,
                    error: error instanceof Error ? error.message : 'Unknown error',
                };
            }
        },
        /**
         * Send voice message
         */
        sendVoice(params, context) {
            try {
                const skill = context.powpowSkill;
                if (!skill) {
                    return { success: false, error: 'Not connected to POWPOW' };
                }
                const sent = skill.sendVoice(params.content, params.mediaUrl, params.duration);
                return {
                    success: sent,
                    message: sent ? 'Voice message sent' : 'Voice message queued',
                };
            }
            catch (error) {
                logger_1.logger.error('SendVoice command failed:', error);
                return {
                    success: false,
                    error: error instanceof Error ? error.message : 'Unknown error',
                };
            }
        },
        /**
         * Send image message
         */
        sendImage(params, context) {
            try {
                const skill = context.powpowSkill;
                if (!skill) {
                    return { success: false, error: 'Not connected to POWPOW' };
                }
                const sent = skill.sendImage(params.content, params.mediaUrl);
                return {
                    success: sent,
                    message: sent ? 'Image sent' : 'Image queued',
                };
            }
            catch (error) {
                logger_1.logger.error('SendImage command failed:', error);
                return {
                    success: false,
                    error: error instanceof Error ? error.message : 'Unknown error',
                };
            }
        },
        /**
         * Start listening for messages
         */
        listen(params, context) {
            const skill = context.powpowSkill;
            if (!skill) {
                return { success: false, error: 'Not connected to POWPOW' };
            }
            skill.on('message', (message) => {
                logger_1.logger.info('Received message:', message);
                context.emit('powpow.message.received', message);
                if (params.autoReply) {
                    const reply = generateAutoReply(message.content);
                    skill.reply(reply);
                }
            });
            return { success: true, message: 'Started listening for messages' };
        },
        /**
         * Stop listening for messages
         */
        stopListen(params, context) {
            const skill = context.powpowSkill;
            if (skill) {
                skill.removeAllListeners('message');
                return { success: true, message: 'Stopped listening for messages' };
            }
            return { success: false, error: 'Not connected' };
        },
    },
};
exports.powpowSkillPlugin = powpowSkillPlugin;
/**
 * Auto-reply generator
 */
function generateAutoReply(content) {
    const replies = {
        '你好': '你好！很高兴为你服务 😊',
        '嗨': '嗨！有什么可以帮助你的吗？',
        '帮助': '我可以帮你：\n1. 回答问题\n2. 提供信息\n3. 协助完成任务',
        '谢谢': '不客气！随时为你服务。',
        '再见': '再见！期待下次交流 👋',
    };
    for (const [keyword, reply] of Object.entries(replies)) {
        if (content.includes(keyword)) {
            return reply;
        }
    }
    return '收到你的消息了！我会尽快处理。';
}
exports.default = powpowSkillPlugin;
//# sourceMappingURL=index.js.map