/**
 * MQTT Client Library for OpenClaw
 *
 * Full MQTT Client with:
 * - Connection Management (Auto-Reconnect, Keep-Alive, LWT, Graceful Disconnect)
 * - Subscription Management (Wildcards, QoS, Dynamic Subscribe/Unsubscribe)
 * - Message Handling (Publish, Retained Messages, JSON Parsing)
 * - OpenClaw Integration (Config from .env/openclaw.json, Logging)
 *
 * @author OpenClaw
 * @version 1.1.0
 *
 * SPDX-License-Identifier: MIT-0
 */

const mqtt = require('mqtt');
const crypto = require('crypto');
const os = require('os');
const EventEmitter = require('events');
const fs = require('fs');
const path = require('path');

/**
 * Generates a unique MQTT Client-ID based on hostname, PID and timestamp
 * @returns {string} Unique Client-ID with prefix "oc-"
 */
function generateUniqueClientId() {
  const unique = `${os.hostname()}-${process.pid}-${Date.now()}`;
  return 'oc-' + crypto.createHash('sha256').update(unique).digest('hex').substring(0, 20);
}

// Default configuration - automatically reads from process.env (OpenClaw config)
const DEFAULTS = {
  broker: process.env.MQTT_BROKER, // undefined if not set - will be validated later
  port: process.env.MQTT_BROKER_PORT ? parseInt(process.env.MQTT_BROKER_PORT) : 1883,
  username: process.env.MQTT_USERNAME,
  password: process.env.MQTT_PASSWORD,
  clientId: process.env.MQTT_CLIENT_ID || 'openclaw', // Overridden in constructor if not set
  protocolVersion: parseInt(process.env.MQTT_PROTOCOL_VERSION) || 4, // 4 = MQTT 3.1.1, 5 = MQTT 5.0
  reconnectPeriod: parseInt(process.env.MQTT_RECONNECT_PERIOD) || 5000,
  connectTimeout: parseInt(process.env.MQTT_CONNECT_TIMEOUT) || 30000,
  keepalive: parseInt(process.env.MQTT_KEEPALIVE) || 60,
  maxReconnectAttempts: parseInt(process.env.MQTT_MAX_RECONNECT_ATTEMPTS) || Infinity,
  messageHistorySize: parseInt(process.env.MQTT_HISTORY_SIZE) || 50,
  parseJson: process.env.MQTT_PARSE_JSON !== 'false',
  logLevel: process.env.MQTT_LOG_LEVEL || 'info',
  validateConfig: true, // New option: Config validation at startup
  allowEmptyBroker: false // Whether empty broker URL is allowed (for testing)
};

// Log level constants
const LOG_LEVELS = {
  debug: 0,
  info: 1,
  warn: 2,
  error: 3
};

class MqttClient extends EventEmitter {
  /**
   * Creates a new MQTT Client
   * @param {Object} options - Configuration options
   */
  constructor(options = {}) {
    super();

    // Client-ID: Hash as default, explicit IDs override
    const clientId = options.clientId || process.env.MQTT_CLIENT_ID || generateUniqueClientId();

    // Merge options with defaults
    this.options = { ...DEFAULTS, ...options, clientId };

    // Internal state
    this._client = null;
    this._connected = false;
    this._reconnecting = false;
    this._reconnectAttempts = 0;
    this._subscriptions = new Map();
    this._messageHistory = [];
    this._messageHistoryByTopic = new Map(); // Optimized: grouped by topic
    this._lastConnected = null;
    this._lastError = null;
    this._messagesReceived = 0;
    this._messagesSent = 0;
    this._disconnecting = false;
    this._connectResolve = null;
    this._connectReject = null;

    // Extended health monitoring
    this._connectionStartTime = null;
    this._latency = [];
    this._lastPingTime = null;
    this._pingInterval = null;
    this._latencyCheckEnabled = this.options.latencyCheck !== false;
    this._latencyCheckInterval = this.options.latencyCheckInterval || 30000;

    // Threshold trigger system
    this._triggers = new Map();
    this._triggerCooldowns = new Map();

    // Logging
    this._currentLogLevel = LOG_LEVELS[this.options.logLevel] ?? 1;

    // Validate config immediately in constructor (for early error detection)
    if (this.options.validateConfig) {
      this._validateConfig();
    }

    this._log('debug', 'MqttClient instance created', {
      broker: this.options.broker,
      clientId: this.options.clientId
    });
  }

  /**
   * Logs a message
   * @private
   */
  _log(level, message, meta = {}) {
    const numericLevel = LOG_LEVELS[level] ?? 1;
    if (numericLevel >= this._currentLogLevel) {
      const timestamp = new Date().toISOString();
      const logFn = level === 'error' ? console.error :
                    level === 'warn' ? console.warn : console.log;
      const metaStr = Object.keys(meta).length ? JSON.stringify(meta) : '';
      logFn(`[MQTT] [${timestamp}] [${level.toUpperCase()}] ${message} ${metaStr}`);
    }
  }

  /**
   * Loads configuration from openclaw.json if present
   * @private
   */
  _loadOpenClawConfig() {
    const possiblePaths = [
      path.join(process.env.HOME || process.env.USERPROFILE, '.openclaw', 'openclaw.json'),
      path.join(process.cwd(), 'openclaw.json'),
      path.join(process.cwd(), '.openclaw', 'openclaw.json'),
      path.join(__dirname, '..', '..', 'openclaw.json')
    ];

    for (const configPath of possiblePaths) {
      try {
        if (fs.existsSync(configPath)) {
          const config = JSON.parse(fs.readFileSync(configPath, 'utf8'));
          // FIX: Use correct path
          const env = config.skills?.entries?.['mqtt-client']?.env;
          if (env) {
            this._log('debug', `Loaded config from ${configPath}`);
            return {
              broker: env.MQTT_BROKER,
              port: parseInt(env.MQTT_BROKER_PORT) || 1883,
              username: env.MQTT_USERNAME,
              password: env.MQTT_PASSWORD,
              clientId: env.MQTT_CLIENT_ID,
              protocolVersion: parseInt(env.MQTT_PROTOCOL_VERSION) || 4,
              subscribeTopic: env.MQTT_SUBSCRIBE_TOPIC
            };
          }
        }
      } catch {
        // Ignore errors, continue to next path
      }
    }
    return {};
  }

  /**
   * Validates configuration at startup
   * @private
   */
  _validateConfig() {
    const errors = [];

    // Check broker (treat empty strings as "not set")
    if (!this.options.broker || this.options.broker.trim() === '') {
      errors.push('MQTT_BROKER is required');
    }

    // Check port
    if (this.options.port && (isNaN(this.options.port) || this.options.port < 1 || this.options.port > 65535)) {
      errors.push('MQTT_BROKER_PORT must be between 1 and 65535');
    }

    // Check username/password combination
    const hasUsername = this.options.username && this.options.username.trim() !== '';
    const hasPassword = this.options.password && this.options.password.trim() !== '';
    // Username without password is OK (e.g. local brokers without auth)
    // Only warn if one is set but not the other -> Warning (not Error)

    // Check client ID
    if (!this.options.clientId || this.options.clientId.length > 23) {
      errors.push('MQTT_CLIENT_ID must be set and not exceed 23 characters (MQTT spec)');
    }

    if (errors.length > 0) {
      const errorMsg = 'MQTT Config Validation Failed: ' + errors.join('; ');
      this._log('error', errorMsg);
      throw new Error(errorMsg);
    }

    this._log('debug', 'Config validation passed');
  }

  /**
   * Build full broker URL from broker + port
   * Supports: "host", "host:1883", "mqtt://host", "mqtt://host:1883"
   * @private
   */
  _buildBrokerUrl(broker, port) {
    let url = broker;

    // Add protocol if not present
    if (!url.includes('://')) {
      url = `mqtt://${url}`;
    }

    // Extract existing port from URL if present
    const portMatch = url.match(/^(.+):(\d+)$/);
    if (!portMatch) {
      // No port in URL - add port
      url = `${url}:${port}`;
    }
    // If port already in URL -> keep it

    return url;
  }

  /**
   * Creates MQTT client options
   * @private
   */
  _buildClientOptions() {
    // Validate config if enabled
    if (this.options.validateConfig) {
      this._validateConfig();
    }

    const opts = {
      clientId: this.options.clientId,
      reconnectPeriod: this.options.reconnectPeriod,
      connectTimeout: this.options.connectTimeout,
      keepalive: this.options.keepalive,
      clean: true,
      rejectUnauthorized: false
    };

    // Credentials
    if (this.options.username) opts.username = this.options.username;
    if (this.options.password) opts.password = this.options.password;

    // LWT
    if (this.options.will) opts.will = this.options.will;

    // TLS
    if (this.options.tls) opts.tls = this.options.tls;

    // MQTT 5.0 Properties
    if (this.options.properties) opts.properties = this.options.properties;

    // Protocol Version (4 = MQTT 3.1.1, 5 = MQTT 5.0)
    if (this.options.protocolVersion) opts.protocolVersion = this.options.protocolVersion;

    // Override with openclaw.json if present
    const openclawConfig = this._loadOpenClawConfig();
    if (openclawConfig.broker) this.options.broker = openclawConfig.broker;
    if (openclawConfig.port) this.options.port = openclawConfig.port;
    if (openclawConfig.username) opts.username = openclawConfig.username;
    if (openclawConfig.password) opts.password = openclawConfig.password;
    if (openclawConfig.clientId) this.options.clientId = openclawConfig.clientId;
    if (openclawConfig.protocolVersion) this.options.protocolVersion = openclawConfig.protocolVersion;
    if (openclawConfig.tls) opts.tls = openclawConfig.tls;
    if (openclawConfig.properties) opts.properties = openclawConfig.properties;

    // Build full broker URL
    const brokerUrl = this._buildBrokerUrl(this.options.broker, this.options.port);

    this._log('debug', 'Client options built', {
      broker: brokerUrl,
      clientId: opts.clientId,
      keepalive: opts.keepalive
    });

    return opts;
  }

  /**
   * Connects to the MQTT Broker
   * @returns {Promise<void>}
   */
  connect() {
    return new Promise((resolve, reject) => {
      if (this._connected) {
        this._log('warn', 'Already connected');
        resolve();
        return;
      }

      if (this._client) {
        this._log('warn', 'Reusing existing client instance');
      }

      // Build options and full broker URL
      const opts = this._buildClientOptions();
      const brokerUrl = this._buildBrokerUrl(this.options.broker, this.options.port);

      this._log('info', `Connecting to ${brokerUrl}...`);

      this._client = mqtt.connect(brokerUrl, opts);

      // Store promise callbacks for reuse
      this._connectResolve = resolve;
      this._connectReject = reject;

      const connectTimeout = setTimeout(() => {
        if (!this._connected && !this._reconnecting) {
          this._log('error', 'Connection timeout');
          this._client.end();
          reject(new Error('Connection timeout'));
        }
      }, this.options.connectTimeout);

      this._client.on('connect', (connack) => {
        clearTimeout(connectTimeout);

        if (this._disconnecting) {
          this._log('info', 'Received connect while disconnecting, ignoring');
          return;
        }

        this._connected = true;
        this._reconnecting = false;
        this._reconnectAttempts = 0;
        this._lastConnected = new Date();
        this._connectionStartTime = Date.now();

        // Reset reconnect delay after successful connection (for exponential backoff)
        if (this._client && this.options.exponentialBackoff) {
          this._client.options.reconnectPeriod = this.options.reconnectPeriod;
        }

        this._log('info', `Connected to ${brokerUrl}`, {
          sessionPresent: connack.sessionPresent
        });

        this.emit('connect', connack);

        // Start latency monitoring
        this._startLatencyCheck();

        // Resubscribe to previous topics
        this._resubscribe();

        if (this._connectResolve) {
          this._connectResolve();
          this._connectResolve = null;
          this._connectReject = null;
        }
      });

      this._client.on('error', (err) => {
        clearTimeout(connectTimeout);

        // Categorize errors
        let errorType = 'connection';
        if (err.message.includes('ECONNREFUSED')) errorType = 'connection_refused';
        else if (err.message.includes('ETIMEDOUT')) errorType = 'timeout';
        else if (err.message.includes('ENOTFOUND')) errorType = 'dns_error';
        else if (err.message.includes('certificate')) errorType = 'tls_error';

        this._log('error', `MQTT ${errorType} error`, { error: err.message });

        // Store last error for health check
        this._lastError = { type: errorType, message: err.message, time: new Date() };
        this.emit('error', err);

        if (!this._connected && this._connectReject) {
          this._connectReject(err);
          this._connectResolve = null;
          this._connectReject = null;
        }
      });

      this._client.on('close', () => {
        if (this._disconnecting) return;

        const wasConnected = this._connected;
        this._connected = false;

        if (wasConnected) {
          this._log('info', 'Disconnected from broker');
          this.emit('disconnect');
          this.emit('close');
        }
      });

      this._client.on('offline', () => {
        this._connected = false;
        this._log('warn', 'Client went offline');
        this.emit('offline');
      });

      this._client.on('reconnect', () => {
        if (this._disconnecting) {
          this._client.end();
          return;
        }

        this._reconnecting = true;
        this._reconnectAttempts++;

        // Optional: Calculate exponential backoff
        let reconnectDelay = this.options.reconnectPeriod;
        if (this.options.exponentialBackoff) {
          // Max delay = reconnectPeriod * 2^attempt, capped at 5 minutes
          reconnectDelay = Math.min(
            this.options.reconnectPeriod * Math.pow(2, this._reconnectAttempts - 1),
            300000
          );
          this._client.options.reconnectPeriod = reconnectDelay;
        }

        this._log('info', `Reconnecting... (attempt ${this._reconnectAttempts}, delay: ${reconnectDelay}ms)`);
        this.emit('reconnecting', this._reconnectAttempts);

        // Check max reconnect attempts
        if (this._reconnectAttempts > this.options.maxReconnectAttempts) {
          this._log('error', 'Max reconnect attempts reached');
          this._client.end();
          const err = new Error('Max reconnect attempts reached');
          this.emit('error', err);

          if (this._connectReject) {
            this._connectReject(err);
            this._connectResolve = null;
            this._connectReject = null;
          }
        }
      });

      this._client.on('message', (topic, payload, packet) => {
        this._messagesReceived++;

        // Parse JSON if enabled
        let parsedPayload = payload;
        if (this.options.parseJson) {
          try {
            // Handle Buffer
            const str = payload instanceof Buffer ? payload.toString() : payload;
            parsedPayload = JSON.parse(str);
            parsedPayload = typeof parsedPayload === 'object' ? parsedPayload : str;
          } catch {
            // Fallback to string or Buffer
            parsedPayload = payload instanceof Buffer ? payload.toString() : payload;
          }
        } else if (payload instanceof Buffer) {
          parsedPayload = payload.toString();
        }

        // Store in history
        this._addToHistory(topic, parsedPayload, packet);

        this._log('debug', `Message received`, {
          topic,
          qos: packet.qos,
          retain: packet.retain
        });

        // Check triggers
        this._checkTriggers(topic, parsedPayload);

        this.emit('message', topic, parsedPayload, packet);
      });
    });
  }

  /**
   * Adds message to history (global and per topic)
   * @private
   * @param {string} topic - MQTT Topic
   * @param {*} payload - Message payload
   * @param {Object} packet - MQTT Packet
   */
  _addToHistory(topic, payload, packet) {
    const entry = {
      topic,
      payload,
      packet,
      timestamp: new Date()
    };

    // Add to global history
    this._messageHistory.push(entry);

    // Optimized: Add to topic-specific history
    if (!this._messageHistoryByTopic.has(topic)) {
      this._messageHistoryByTopic.set(topic, []);
    }
    const topicHistory = this._messageHistoryByTopic.get(topic);
    topicHistory.push(entry);

    // Limit history size (global and per topic)
    const maxPerTopic = Math.min(20, this.options.messageHistorySize); // Max 20 per topic

    if (this._messageHistory.length > this.options.messageHistorySize) {
      this._messageHistory = this._messageHistory.slice(-this.options.messageHistorySize);
    }

    if (topicHistory.length > maxPerTopic) {
      this._messageHistoryByTopic.set(topic, topicHistory.slice(-maxPerTopic));
    }
  }

  /**
   * Resubscribes to all previous topics after reconnect
   * @private
   * @returns {Promise<void>}
   */
  async _resubscribe() {
    if (this._subscriptions.size > 0) {
      this._log('info', `Resubscribing to ${this._subscriptions.size} topics`);

      const promises = [];
      for (const [topic, options] of this._subscriptions) {
        promises.push(
          this._subscribeInternal(topic, options).catch(err => {
            this._log('error', `Failed to resubscribe to ${topic}`, { error: err.message });
            return null;
          })
        );
      }

      await Promise.all(promises);
    }
  }

  /**
   * Internal subscribe
   * @private
   * @param {string} topic - Topic to subscribe to
   * @param {Object} options - Subscribe options (qos)
   * @returns {Promise<Array>} Array of granted QoS
   */
  _subscribeInternal(topic, options = {}) {
    return new Promise((resolve, reject) => {
      const qos = options.qos || 0;

      this._client.subscribe(topic, { qos }, (err, granted) => {
        if (err) {
          this._log('error', `Subscribe error for ${topic}`, { error: err.message });
          reject(err);
        } else {
          this._log('debug', `Subscribed to ${topic}`, { qos: granted[0]?.qos });
          resolve(granted);
        }
      });
    });
  }

  /**
   * Subscribes to a topic
   * @param {string|string[]} topic - Topic(s) to subscribe to
   * @param {Object} options - Options (qos, etc.)
   * @returns {Promise<Array>} Array of granted results
   */
  async subscribe(topic, options = {}) {
    if (!this._connected) {
      throw new Error('Not connected');
    }

    const topics = Array.isArray(topic) ? topic : [topic];
    const results = [];

    for (const t of topics) {
      // Store subscription
      this._subscriptions.set(t, options);

      const result = await this._subscribeInternal(t, options);
      results.push(result);
    }

    return results;
  }

  /**
   * Unsubscribes from a topic
   * @param {string|string[]} topic - Topic(s)
   * @returns {Promise}
   */
  async unsubscribe(topic) {
    if (!this._connected) {
      throw new Error('Not connected');
    }

    const topics = Array.isArray(topic) ? topic : [topic];
    const results = [];

    for (const t of topics) {
      this._subscriptions.delete(t);

      const result = await new Promise((resolve, reject) => {
        this._client.unsubscribe(t, (err) => {
          if (err) {
            this._log('error', `Unsubscribe error for ${t}`, { error: err.message });
            reject(err);
          } else {
            this._log('debug', `Unsubscribed from ${t}`);
            resolve();
          }
        });
      });

      results.push(result);
    }

    return results;
  }

  /**
   * Unsubscribes from all topics
   * @returns {Promise}
   */
  async unsubscribeAll() {
    const topics = Array.from(this._subscriptions.keys());
    this._subscriptions.clear();

    if (topics.length > 0 && this._connected) {
      return this.unsubscribe(topics);
    }

    return [];
  }

  /**
   * Publishes a message
   * @param {string} topic - Topic
   * @param {string|Object|Buffer} payload - Message
   * @param {Object} options - Options (qos, retain, properties for MQTT 5.0)
   * @returns {Promise}
   */
  async publish(topic, payload, options = {}) {
    if (!this._connected) {
      throw new Error('Not connected');
    }

    // Stringify if object
    let messagePayload = payload;
    if (typeof payload === 'object' && payload !== null && !(payload instanceof Buffer)) {
      messagePayload = JSON.stringify(payload);
    }

    const publishOptions = {
      qos: options.qos || 0,
      retain: options.retain || false
    };

    // MQTT 5.0 properties
    if (options.properties) {
      publishOptions.properties = options.properties;
    }

    return new Promise((resolve, reject) => {
      this._client.publish(topic, messagePayload, publishOptions, (err) => {
        if (err) {
          this._log('error', `Publish error on ${topic}`, { error: err.message });
          reject(err);
        } else {
          this._messagesSent++;
          this._log('debug', `Published to ${topic}`, {
            qos: publishOptions.qos,
            retain: publishOptions.retain
          });
          resolve();
        }
      });
    });
  }

  /**
   * Disconnects cleanly
   * @param {number} timeout - Timeout in ms
   * @returns {Promise}
   */
  async disconnect(timeout = 5000) {
    if (!this._client) {
      this._log('info', 'No client instance to disconnect');
      return;
    }

    this._disconnecting = true;
    this._log('info', 'Disconnecting...');

    return new Promise((resolve) => {
      const disconnectTimeout = setTimeout(() => {
        this._log('warn', 'Disconnect timeout, forcing close');
        this._client.end();
        this._cleanupAfterDisconnect();
        resolve();
      }, timeout);

      this._client.end(true, {}, () => {
        clearTimeout(disconnectTimeout);
        this._log('info', 'Disconnected gracefully');
        this.emit('disconnect');
        this._cleanupAfterDisconnect();
        resolve();
      });
    });
  }

  /**
   * Forces connection to end
   * @returns {void}
   */
  end() {
    this._disconnecting = true;
    this._log('info', 'Forcing disconnect');

    if (this._client) {
      this._client.end();
      this._cleanupAfterDisconnect();
    }

    this.emit('close');
  }

  /**
   * Cleanup after disconnect
   * @private
   */
  _cleanupAfterDisconnect() {
    this._connected = false;
    this._reconnecting = false;
    this._disconnecting = false;
    this._connectionStartTime = null;

    // Stop latency monitoring
    this._stopLatencyCheck();
  }

  /**
   * Checks if a topic matches a pattern (supports wildcards)
   * @private
   */
  _topicMatches(pattern, topic) {
    const patternParts = pattern.split('/');
    const topicParts = topic.split('/');

    for (let i = 0; i < patternParts.length; i++) {
      const p = patternParts[i];

      // Multi-level wildcard (#) matches anything remaining
      if (p === '#') {
        return true;
      }

      // Single-level wildcard (+) matches exactly one level
      if (p === '+') {
        // Need at least one part remaining, or be at the end of pattern
        if (i >= topicParts.length && i < patternParts.length - 1) {
          return false;
        }
        continue;
      }

      // Exact match required
      if (i >= topicParts.length || p !== topicParts[i]) {
        return false;
      }
    }

    // All pattern parts must be consumed
    return patternParts.length === topicParts.length;
  }

  /**
   * Returns message history
   * @param {string} [topic] - Optional: Only messages for this topic (wildcards supported)
   * @returns {Array}
   */
  getMessageHistory(topic) {
    if (!topic) {
      return [...this._messageHistory];
    }

    return this._messageHistory.filter(msg => this._topicMatches(topic, msg.topic));
  }

  /**
   * Returns all messages
   * @returns {Array}
   */
  getAllMessages() {
    return this.getMessageHistory();
  }

  /**
   * Finds the last message for a topic
   * @param {string} topic - Topic (wildcards supported)
   * @returns {Object|null}
   */
  getLastMessage(topic) {
    const history = this.getMessageHistory(topic);
    return history.length > 0 ? history[history.length - 1] : null;
  }

  /**
   * Returns health status
   * @returns {Object}
   */
  getHealth() {
    const latencyStats = this._getLatencyStats();

    return {
      connected: this._connected,
      reconnecting: this._reconnecting,
      disconnecting: this._disconnecting,
      reconnectAttempts: this._reconnectAttempts,
      lastConnected: this._lastConnected,
      lastError: this._lastError,
      connectionStartTime: this._connectionStartTime,
      messagesReceived: this._messagesReceived,
      messagesSent: this._messagesSent,
      subscriptionCount: this._subscriptions.size,
      broker: this.options.broker,
      port: this.options.port,
      uptime: this._lastConnected ? Date.now() - this._lastConnected.getTime() : 0,
      latency: latencyStats,
      triggerCount: this._triggers.size
    };
  }

  /**
   * Returns current status
   * @returns {Object}
   */
  getState() {
    let status = 'disconnected';
    if (this._disconnecting) {
      status = 'disconnecting';
    } else if (this._reconnecting) {
      status = 'reconnecting';
    } else if (this._connected) {
      status = 'connected';
    }

    const latencyStats = this._getLatencyStats();

    return {
      status,
      broker: this.options.broker,
      clientId: this.options.clientId,
      subscriptions: Array.from(this._subscriptions.keys()),
      subscriptionsCount: this._subscriptions.size,
      latency: latencyStats,
      activeTriggers: this._triggers.size
    };
  }

  // =========================================================================
  // Latency Monitoring
  // =========================================================================

  /**
   * Starts periodic latency measurement
   * @private
   */
  _startLatencyCheck() {
    if (!this._latencyCheckEnabled || this._pingInterval) return;

    // Initial latency measurement after 5 seconds
    setTimeout(() => this._measureLatency(), 5000);

    // Periodic measurement
    this._pingInterval = setInterval(() => {
      this._measureLatency();
    }, this._latencyCheckInterval);

    this._log('debug', 'Latency check started', {
      interval: this._latencyCheckInterval
    });
  }

  /**
   * Measures latency to broker
   * @private
   */
  _measureLatency() {
    if (!this._connected || !this._client) return;

    const startTime = Date.now();

    // Send ping with publish and listen on the same topic
    const pingTopic = `openclaw/health/ping/${this.options.clientId}`;
    const responseTopic = `openclaw/health/pong/${this.options.clientId}`;

    // Short-term listener for pong
    const pongHandler = (topic, payload) => {
      if (topic === responseTopic) {
        const latency = Date.now() - startTime;
        this._latency.push(latency);

        // Limit latency history to 100 entries
        if (this._latency.length > 100) {
          this._latency = this._latency.slice(-100);
        }

        this._log('debug', 'Latency measured', { latency });
        this.emit('latency', latency);
      }
    };

    // Timeout for ping
    const pingTimeout = setTimeout(() => {
      this._client.removeListener('message', pongHandler);
      this._log('warn', 'Latency check timeout');
    }, 10000);

    this._client.on('message', pongHandler);

    // Subscribe temporarily to pong topic
    this._client.subscribe(responseTopic, { qos: 0 }, (err) => {
      if (err) {
        clearTimeout(pingTimeout);
        this._client.removeListener('message', pongHandler);
        return;
      }

      // Send ping
      this._client.publish(pingTopic, String(startTime), { qos: 0 }, (err) => {
        if (err) {
          clearTimeout(pingTimeout);
          this._client.removeListener('message', pongHandler);
          this._client.unsubscribe(responseTopic);
        }
      });
    });

    // Cleanup after 15 seconds
    setTimeout(() => {
      clearTimeout(pingTimeout);
      this._client?.removeListener('message', pongHandler);
      this._client?.unsubscribe(responseTopic).catch(() => {});
    }, 15000);
  }

  /**
   * Stops latency monitoring
   * @private
   */
  _stopLatencyCheck() {
    if (this._pingInterval) {
      clearInterval(this._pingInterval);
      this._pingInterval = null;
      this._log('debug', 'Latency check stopped');
    }
  }

  /**
   * Calculates latency statistics
   * @private
   * @returns {Object} Latency statistics (current, average, min, max, samples)
   */
  _getLatencyStats() {
    if (this._latency.length === 0) {
      return { current: 0, average: 0, min: 0, max: 0, samples: 0 };
    }

    const avgLatency = Math.round(this._latency.reduce((a, b) => a + b, 0) / this._latency.length);
    const minLatency = Math.min(...this._latency);
    const maxLatency = Math.max(...this._latency);
    const current = this._latency[this._latency.length - 1];

    return {
      current,
      average: avgLatency,
      min: minLatency,
      max: maxLatency,
      samples: this._latency.length
    };
  }

  // =========================================================================
  // Threshold Trigger System
  // =========================================================================

  /**
   * Adds a threshold trigger
   * @param {string} id - Unique trigger ID
   * @param {Object} config - Trigger configuration
   * @returns {void}
   */
  addTrigger(id, config) {
    const trigger = {
      id,
      topic: config.topic,           // MQTT topic pattern (wildcards supported)
      path: config.path,             // JSON path to value (e.g. "battery" or "sensors.temp.value")
      operator: config.operator || '>', // >, <, >=, <=, ==, !=, contains
      threshold: config.threshold,   // Threshold value
      valueType: config.valueType || 'number', // number, string, boolean
      cooldown: config.cooldown || 60000, // Cooldown in ms (default 60s)
      callback: config.callback,     // Function to be called
      enabled: config.enabled !== false,
      description: config.description || `Trigger ${id}`
    };

    this._triggers.set(id, trigger);
    this._triggerCooldowns.set(id, 0);

    this._log('info', 'Trigger added', {
      id,
      topic: trigger.topic,
      threshold: trigger.threshold,
      operator: trigger.operator
    });

    // Emit event
    this.emit('trigger:added', trigger);
  }

  /**
   * Removes a trigger
   * @param {string} id - Trigger ID
   * @returns {boolean}
   */
  removeTrigger(id) {
    const removed = this._triggers.delete(id);
    this._triggerCooldowns.delete(id);

    if (removed) {
      this._log('info', 'Trigger removed', { id });
      this.emit('trigger:removed', { id });
    }

    return removed;
  }

  /**
   * Enables/disables a trigger
   * @param {string} id - Trigger ID
   * @param {boolean} enabled - Enable/Disable
   * @returns {boolean}
   */
  setTriggerEnabled(id, enabled) {
    const trigger = this._triggers.get(id);
    if (!trigger) return false;

    trigger.enabled = enabled;
    this._log('info', 'Trigger toggled', { id, enabled });
    this.emit('trigger:toggled', { id, enabled });

    return true;
  }

  /**
   * Returns all triggers
   * @returns {Array}
   */
  getTriggers() {
    return Array.from(this._triggers.values()).map(t => ({
      id: t.id,
      topic: t.topic,
      path: t.path,
      operator: t.operator,
      threshold: t.threshold,
      enabled: t.enabled,
      description: t.description
    }));
  }

  /**
   * Checks incoming message against all triggers
   * @private
   */
  _checkTriggers(topic, payload) {
    for (const [id, trigger] of this._triggers) {
      if (!trigger.enabled) continue;

      // Check if topic matches pattern
      if (!this._topicMatches(trigger.topic, topic)) continue;

      // Extract value from payload
      const value = this._extractValue(payload, trigger.path);
      if (value === undefined) continue;

      // Check threshold
      const triggered = this._evaluateCondition(value, trigger.operator, trigger.threshold, trigger.valueType);

      if (triggered) {
        this._handleTrigger(id, trigger, topic, value);
      }
    }
  }

  /**
   * Extracts a value from an object using path
   * @private
   */
  _extractValue(payload, path) {
    if (!path) return payload;
    if (typeof payload !== 'object' || payload === null) return undefined;

    const parts = path.split('.');
    let current = payload;

    for (const part of parts) {
      if (current === undefined || current === null) return undefined;
      current = current[part];
    }

    return current;
  }

  /**
   * Evaluates a condition
   * @private
   */
  _evaluateCondition(value, operator, threshold, valueType) {
    // Convert to appropriate type
    let numValue = value;
    let numThreshold = threshold;

    if (valueType === 'number') {
      numValue = parseFloat(value);
      numThreshold = parseFloat(threshold);
      if (isNaN(numValue) || isNaN(numThreshold)) return false;
    }

    switch (operator) {
      case '>': return numValue > numThreshold;
      case '<': return numValue < numThreshold;
      case '>=': return numValue >= numThreshold;
      case '<=': return numValue <= numThreshold;
      case '==': return value == threshold;
      case '===': return value === threshold;
      case '!=': return value != threshold;
      case '!==': return value !== threshold;
      case 'contains': return String(value).includes(String(threshold));
      case 'startsWith': return String(value).startsWith(String(threshold));
      case 'endsWith': return String(value).endsWith(String(threshold));
      default: return false;
    }
  }

  /**
   * Processes a triggered trigger
   * @private
   */
  _handleTrigger(id, trigger, topic, value) {
    const now = Date.now();
    const lastTriggered = this._triggerCooldowns.get(id) || 0;

    // Check cooldown
    if (now - lastTriggered < trigger.cooldown) {
      this._log('debug', 'Trigger in cooldown', { id, remaining: trigger.cooldown - (now - lastTriggered) });
      return;
    }

    // Update cooldown
    this._triggerCooldowns.set(id, now);

    const triggerEvent = {
      id,
      topic,
      value,
      threshold: trigger.threshold,
      operator: trigger.operator,
      timestamp: new Date(),
      description: trigger.description
    };

    this._log('info', 'Trigger fired!', triggerEvent);

    // Call callback
    if (trigger.callback && typeof trigger.callback === 'function') {
      try {
        trigger.callback(triggerEvent);
      } catch (err) {
        this._log('error', 'Trigger callback error', { id, error: err.message });
      }
    }

    // Emit event
    this.emit('trigger:fired', triggerEvent);
  }

  /**
   * Checks connection status
   * @returns {boolean}
   */
  isConnected() {
    return this._connected;
  }

  /**
   * Resets message history
   * @returns {void}
   */
  clearHistory() {
    this._messageHistory = [];
    this._messageHistoryByTopic.clear();
    this._log('info', 'Message history cleared');
  }

  /**
   * Resets subscriptions (without unsubscribing from broker)
   * @returns {void}
   */
  clearSubscriptions() {
    this._subscriptions.clear();
    this._log('info', 'Subscriptions cleared');
  }

  /**
   * Resets all statistics
   * @returns {void}
   */
  resetStats() {
    this._messagesReceived = 0;
    this._messagesSent = 0;
    this._latency = [];
    this._log('info', 'Statistics reset');
  }

  /**
   * Resets all triggers
   * @returns {void}
   */
  clearTriggers() {
    this._triggers.clear();
    this._triggerCooldowns.clear();
    this._log('info', 'All triggers cleared');
  }

  /**
   * Returns access to internal mqtt.Client (for advanced usage)
   * @returns {mqtt.Client|null}
   */
  getClient() {
    return this._client;
  }
}

// =========================================================================
// Auto-Setup Function for OpenClaw Config
// =========================================================================

const CONFIG_PATH = path.join(process.env.HOME || process.env.USERPROFILE, '.openclaw', 'openclaw.json');

/**
 * Loads existing OpenClaw configuration
 * @returns {Object} The full config
 */
function loadOpenClawConfig() {
  try {
    if (fs.existsSync(CONFIG_PATH)) {
      return JSON.parse(fs.readFileSync(CONFIG_PATH, 'utf8'));
    }
  } catch (err) {
    // Silent error handling - config will be recreated if needed
  }
  return {};
}

/**
 * Auto-Setup: Creates or extends the mqtt-client config in openclaw.json
 * Automatically called when importing the module
 * @param {boolean} forceSetup - If true, config is always rewritten
 * @returns {Promise<Object>} The mqtt-client config
 */
async function autoSetupConfig(forceSetup = false) {
  const config = loadOpenClawConfig();
  
  // Initialize structures if needed
  if (!config.skills) config.skills = {};
  if (!config.skills.entries) config.skills.entries = {};
  
  const skillKey = 'mqtt-client';
  
  // Template for new config
  const template = {
    enabled: true,
    env: {
      MQTT_BROKER: 'localhost',
      MQTT_BROKER_PORT: '1883',
      MQTT_USERNAME: '',
      MQTT_PASSWORD: '',
      MQTT_CLIENT_ID: '',
      MQTT_PROTOCOL_VERSION: '4',
      MQTT_SUBSCRIBE_TOPIC: '#'
    }
  };
  
  let isNew = false;
  
  if (!config.skills.entries[skillKey]) {
    // New skill entry - add complete template
    config.skills.entries[skillKey] = JSON.parse(JSON.stringify(template));
    isNew = true;
  } else {
    // Existing - only extend if structure is missing
    const existing = config.skills.entries[skillKey];
    
    // Make sure enabled exists
    if (existing.enabled === undefined) {
      existing.enabled = true;
    }
    
    // Make sure env exists
    if (!existing.env) {
      existing.env = template.env;
    } else {
      // Add missing env variables (does NOT overwrite existing values)
      for (const [key, value] of Object.entries(template.env)) {
        if (existing.env[key] === undefined) {
          existing.env[key] = value;
        }
      }
    }
  }
  
  // Save if new config or forceSetup
  if (isNew || forceSetup) {
    const dir = path.dirname(CONFIG_PATH);
    if (!fs.existsSync(dir)) {
      fs.mkdirSync(dir, { recursive: true });
    }
    fs.writeFileSync(CONFIG_PATH, JSON.stringify(config, null, 2));
    
    if (isNew) {
      console.log('[MQTT] ✓ Auto-Setup: mqtt-client config created in', CONFIG_PATH);
    }
  }
  
  return config.skills.entries[skillKey];
}

// Run auto-setup on import (only once per process)
let _autoSetupCalled = false;
if (!_autoSetupCalled) {
  _autoSetupCalled = true;
  // Run async in background, but don't let errors propagate
  autoSetupConfig().catch(() => {});
}

module.exports = { MqttClient, generateUniqueClientId, autoSetupConfig, loadOpenClawConfig };