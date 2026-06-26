/**
 * OpenClawInstrumentation - Automatic instrumentation hooks for OpenClaw integration
 *
 * When LobsterOps is installed as an OpenClaw skill, this module provides
 * automatic capture of agent events by hooking into OpenClaw's event system.
 */
class OpenClawInstrumentation {
  /**
   * @param {Object} lobsterOps - LobsterOps instance
   * @param {Object} options - Instrumentation options
   * @param {boolean} options.captureToolCalls - Capture tool call events (default: true)
   * @param {boolean} options.captureSpawns - Capture agent spawn events (default: true)
   * @param {boolean} options.captureLifecycle - Capture lifecycle events (default: true)
   * @param {boolean} options.captureReasoningTraces - Capture reasoning/thought events (default: true)
   * @param {boolean} options.captureFileChanges - Capture file system changes (default: false)
   * @param {boolean} options.captureGitOps - Capture git operations (default: false)
   */
  constructor(lobsterOps, options = {}) {
    this.ops = lobsterOps;
    this.options = {
      captureToolCalls: options.captureToolCalls !== false,
      captureSpawns: options.captureSpawns !== false,
      captureLifecycle: options.captureLifecycle !== false,
      captureReasoningTraces: options.captureReasoningTraces !== false,
      captureFileChanges: options.captureFileChanges === true,
      captureGitOps: options.captureGitOps === true,
    };
    this.active = false;
    this._hooks = [];
  }

  /**
   * Activate instrumentation by attaching to OpenClaw's event system
   * @param {Object} openClawContext - OpenClaw runtime context (if available)
   */
  activate(openClawContext = null) {
    this.active = true;
    this.context = openClawContext;

    // If OpenClaw context is provided, hook into its event emitters
    if (openClawContext && typeof openClawContext.on === 'function') {
      this._attachHooks(openClawContext);
    }
  }

  /**
   * Deactivate instrumentation and remove hooks
   */
  deactivate() {
    this.active = false;
    for (const unhook of this._hooks) {
      try { unhook(); } catch (e) { /* ignore */ }
    }
    this._hooks = [];
  }

  /**
   * Manually instrument a tool call (for use when auto-hooks aren't available)
   * @param {Object} toolCall - Tool call details
   * @returns {Promise<string>} - Event ID
   */
  async instrumentToolCall(toolCall) {
    if (!this.active || !this.options.captureToolCalls) return null;

    return this.ops.logToolCall({
      agentId: toolCall.agentId || 'openclaw-agent',
      toolName: toolCall.toolName || toolCall.name,
      toolInput: toolCall.input,
      toolOutput: toolCall.output,
      durationMs: toolCall.durationMs,
      success: toolCall.success,
      cost: toolCall.cost,
      sessionId: toolCall.sessionId,
    });
  }

  /**
   * Manually instrument a spawn event
   * @param {Object} spawnInfo - Spawn details
   * @returns {Promise<string>} - Event ID
   */
  async instrumentSpawn(spawnInfo) {
    if (!this.active || !this.options.captureSpawns) return null;

    return this.ops.logSpawning({
      parentAgentId: spawnInfo.parentId || 'openclaw-agent',
      childAgentId: spawnInfo.childId,
      childAgentType: spawnInfo.type,
      task: spawnInfo.task,
      spawnReason: spawnInfo.reason,
      sessionId: spawnInfo.sessionId,
    });
  }

  /**
   * Manually instrument a lifecycle event
   * @param {Object} lifecycle - Lifecycle details
   * @returns {Promise<string>} - Event ID
   */
  async instrumentLifecycle(lifecycle) {
    if (!this.active || !this.options.captureLifecycle) return null;

    return this.ops.logLifecycle({
      agentId: lifecycle.agentId || 'openclaw-agent',
      action: lifecycle.action,
      status: lifecycle.status,
      sessionId: lifecycle.sessionId,
      version: lifecycle.version,
      environment: lifecycle.environment,
    });
  }

  /**
   * Manually instrument a reasoning/thought event
   * @param {Object} thought - Thought details
   * @returns {Promise<string>} - Event ID
   */
  async instrumentThought(thought) {
    if (!this.active || !this.options.captureReasoningTraces) return null;

    return this.ops.logThought({
      agentId: thought.agentId || 'openclaw-agent',
      thought: thought.content || thought.thought,
      context: thought.context,
      confidence: thought.confidence,
      sessionId: thought.sessionId,
    });
  }

  /**
   * Manually instrument a file change event
   * @param {Object} fileChange - File change details
   * @returns {Promise<string>} - Event ID
   */
  async instrumentFileChange(fileChange) {
    if (!this.active || !this.options.captureFileChanges) return null;

    return this.ops.logEvent({
      type: 'file-change',
      agentId: fileChange.agentId || 'openclaw-agent',
      action: fileChange.action, // 'create', 'modify', 'delete'
      filePath: fileChange.path,
      linesChanged: fileChange.linesChanged,
      sessionId: fileChange.sessionId,
    });
  }

  /**
   * Manually instrument a git operation
   * @param {Object} gitOp - Git operation details
   * @returns {Promise<string>} - Event ID
   */
  async instrumentGitOp(gitOp) {
    if (!this.active || !this.options.captureGitOps) return null;

    return this.ops.logEvent({
      type: 'git-operation',
      agentId: gitOp.agentId || 'openclaw-agent',
      action: gitOp.action, // 'commit', 'push', 'branch', 'merge'
      details: gitOp.details,
      sessionId: gitOp.sessionId,
    });
  }

  /**
   * Check if instrumentation is active
   * @returns {boolean}
   */
  isActive() {
    return this.active;
  }

  /**
   * Create a pre-configured instrumentation from OpenClaw config
   * @param {Object} lobsterOps - LobsterOps instance
   * @param {Object} config - OpenClaw config object
   * @returns {OpenClawInstrumentation}
   */
  static fromConfig(lobsterOps, config = {}) {
    return new OpenClawInstrumentation(lobsterOps, {
      captureToolCalls: config.captureToolCalls !== false,
      captureSpawns: config.captureSpawns !== false,
      captureLifecycle: config.captureLifecycle !== false,
      captureReasoningTraces: config.captureReasoningTraces !== false,
      captureFileChanges: config.captureFileChanges === true,
      captureGitOps: config.captureGitOps === true,
    });
  }

  // --- Private methods ---

  _attachHooks(emitter) {
    const hookEvent = (eventName, handler) => {
      emitter.on(eventName, handler);
      this._hooks.push(() => emitter.removeListener(eventName, handler));
    };

    if (this.options.captureToolCalls) {
      hookEvent('tool:call', (data) => this.instrumentToolCall(data));
    }

    if (this.options.captureSpawns) {
      hookEvent('agent:spawn', (data) => this.instrumentSpawn(data));
    }

    if (this.options.captureLifecycle) {
      hookEvent('agent:start', (data) => this.instrumentLifecycle({ ...data, action: 'start' }));
      hookEvent('agent:stop', (data) => this.instrumentLifecycle({ ...data, action: 'stop' }));
    }

    if (this.options.captureReasoningTraces) {
      hookEvent('agent:thought', (data) => this.instrumentThought(data));
    }

    if (this.options.captureFileChanges) {
      hookEvent('file:change', (data) => this.instrumentFileChange(data));
    }

    if (this.options.captureGitOps) {
      hookEvent('git:operation', (data) => this.instrumentGitOp(data));
    }
  }
}

module.exports = { OpenClawInstrumentation };
