/**
 * DebugConsole - Interactive time-travel debugger for AI agent execution
 *
 * Provides step-through debugging of agent event traces with
 * variable inspection and tool call analysis.
 */
class DebugConsole {
  /**
   * @param {Array} events - Chronologically sorted events to debug
   */
  constructor(events = []) {
    this.events = [...events].sort(
      (a, b) => new Date(a.timestamp) - new Date(b.timestamp)
    );
    this.cursor = -1; // Before first event
  }

  /**
   * Get total number of events in the trace
   * @returns {number}
   */
  get length() {
    return this.events.length;
  }

  /**
   * Get current cursor position
   * @returns {number}
   */
  get position() {
    return this.cursor;
  }

  /**
   * Step forward one event
   * @returns {Object|null} - The next event, or null if at end
   */
  stepForward() {
    if (this.cursor >= this.events.length - 1) return null;
    this.cursor++;
    return this.current();
  }

  /**
   * Step backward one event
   * @returns {Object|null} - The previous event, or null if at beginning
   */
  stepBackward() {
    if (this.cursor <= 0) return null;
    this.cursor--;
    return this.current();
  }

  /**
   * Jump to a specific position
   * @param {number} index - Position to jump to
   * @returns {Object|null} - The event at that position
   */
  jumpTo(index) {
    if (index < 0 || index >= this.events.length) return null;
    this.cursor = index;
    return this.current();
  }

  /**
   * Jump to the first event
   * @returns {Object|null}
   */
  jumpToStart() {
    return this.jumpTo(0);
  }

  /**
   * Jump to the last event
   * @returns {Object|null}
   */
  jumpToEnd() {
    return this.jumpTo(this.events.length - 1);
  }

  /**
   * Get the current event without moving
   * @returns {Object|null}
   */
  current() {
    if (this.cursor < 0 || this.cursor >= this.events.length) return null;
    return this.events[this.cursor];
  }

  /**
   * Inspect the current event with detailed breakdown
   * @returns {Object|null} - Detailed inspection of the current event
   */
  inspect() {
    const event = this.current();
    if (!event) return null;

    const inspection = {
      position: `${this.cursor + 1}/${this.events.length}`,
      event: { ...event },
      timing: {
        timestamp: event.timestamp,
        durationMs: event.durationMs || null,
      },
      context: {},
    };

    // Add type-specific inspection details
    if (event.type === 'tool-call') {
      inspection.toolCall = {
        toolName: event.toolName || event.tool || null,
        input: event.toolInput || event.input || null,
        output: event.toolOutput || event.output || null,
        success: event.success !== undefined ? event.success : null,
        cost: event.cost || null,
      };
    }

    if (event.type === 'agent-thought') {
      inspection.thought = {
        content: event.thought || event.message || null,
        context: event.context || null,
        confidence: event.confidence || null,
      };
    }

    if (event.type === 'agent-decision') {
      inspection.decision = {
        decision: event.decision || null,
        confidence: event.confidence || null,
        alternatives: event.alternativesConsidered || null,
        reasoning: event.reasoning || null,
      };
    }

    if (event.type === 'agent-error') {
      inspection.error = {
        errorType: event.errorType || null,
        message: event.errorMessage || event.message || null,
        severity: event.severity || null,
        recovered: event.recovered || false,
      };
    }

    // Show surrounding context
    if (this.cursor > 0) {
      inspection.context.previousEvent = {
        type: this.events[this.cursor - 1].type,
        timestamp: this.events[this.cursor - 1].timestamp,
      };
    }
    if (this.cursor < this.events.length - 1) {
      inspection.context.nextEvent = {
        type: this.events[this.cursor + 1].type,
        timestamp: this.events[this.cursor + 1].timestamp,
      };
    }

    return inspection;
  }

  /**
   * Search for events matching criteria within the trace
   * @param {Object} criteria - Search criteria
   * @param {string} criteria.type - Event type to find
   * @param {string} criteria.agentId - Agent ID to find
   * @param {string} criteria.text - Text to search for in event values
   * @returns {Array<{index: number, event: Object}>} - Matching events with their positions
   */
  search(criteria = {}) {
    const results = [];

    for (let i = 0; i < this.events.length; i++) {
      const event = this.events[i];
      let matches = true;

      if (criteria.type && event.type !== criteria.type) matches = false;
      if (criteria.agentId && event.agentId !== criteria.agentId) matches = false;
      if (criteria.text) {
        const eventStr = JSON.stringify(event).toLowerCase();
        if (!eventStr.includes(criteria.text.toLowerCase())) matches = false;
      }

      if (matches) {
        results.push({ index: i, event });
      }
    }

    return results;
  }

  /**
   * Get a summary of the entire trace
   * @returns {Object} - Trace summary
   */
  summary() {
    if (this.events.length === 0) {
      return { totalEvents: 0, eventTypes: {}, agents: [], duration: null };
    }

    const eventTypes = {};
    const agents = new Set();
    let totalCost = 0;
    let totalDuration = 0;
    let errorCount = 0;

    for (const event of this.events) {
      // Count event types
      eventTypes[event.type] = (eventTypes[event.type] || 0) + 1;

      // Collect unique agents
      if (event.agentId) agents.add(event.agentId);

      // Sum costs
      if (event.cost) totalCost += event.cost;

      // Sum durations
      if (event.durationMs) totalDuration += event.durationMs;

      // Count errors
      if (event.type === 'agent-error') errorCount++;
    }

    const firstTimestamp = this.events[0].timestamp;
    const lastTimestamp = this.events[this.events.length - 1].timestamp;
    const wallClockMs = new Date(lastTimestamp) - new Date(firstTimestamp);

    return {
      totalEvents: this.events.length,
      eventTypes,
      agents: Array.from(agents),
      errorCount,
      totalCost: Math.round(totalCost * 10000) / 10000,
      totalDurationMs: totalDuration,
      wallClockMs,
      timeRange: {
        start: firstTimestamp,
        end: lastTimestamp,
      },
    };
  }

  /**
   * Get all tool calls from the trace
   * @returns {Array} - Tool call events
   */
  getToolCalls() {
    return this.events.filter(e => e.type === 'tool-call');
  }

  /**
   * Get all errors from the trace
   * @returns {Array} - Error events
   */
  getErrors() {
    return this.events.filter(e => e.type === 'agent-error');
  }

  /**
   * Get all decisions from the trace
   * @returns {Array} - Decision events
   */
  getDecisions() {
    return this.events.filter(e => e.type === 'agent-decision');
  }
}

module.exports = { DebugConsole };
