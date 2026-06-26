/**
 * AlertManager - Customizable alerting and anomaly detection for agent events
 *
 * Supports rule-based alerts for cost spikes, repeated failures,
 * unusual behavior patterns, and custom thresholds.
 */
class AlertManager {
  constructor() {
    this.rules = [];
    this.alerts = [];
    this.listeners = [];
  }

  /**
   * Add an alert rule
   * @param {Object} rule - Alert rule definition
   * @param {string} rule.name - Rule name
   * @param {string} rule.type - Rule type: 'threshold', 'frequency', 'pattern', 'absence'
   * @param {Object} rule.condition - Condition configuration (depends on type)
   * @param {string} rule.severity - Alert severity: 'low', 'medium', 'high', 'critical'
   * @param {string} rule.message - Alert message template
   * @returns {string} - Rule ID
   */
  addRule(rule) {
    const ruleId = `rule-${Date.now()}-${Math.random().toString(36).substr(2, 6)}`;
    this.rules.push({
      id: ruleId,
      ...rule,
      enabled: rule.enabled !== false,
      createdAt: new Date().toISOString(),
    });
    return ruleId;
  }

  /**
   * Remove a rule by ID
   * @param {string} ruleId
   * @returns {boolean}
   */
  removeRule(ruleId) {
    const idx = this.rules.findIndex(r => r.id === ruleId);
    if (idx === -1) return false;
    this.rules.splice(idx, 1);
    return true;
  }

  /**
   * Register a listener for alerts
   * @param {Function} callback - Called with (alert) when an alert fires
   */
  onAlert(callback) {
    this.listeners.push(callback);
  }

  /**
   * Evaluate a single event against all rules
   * @param {Object} event - The event to evaluate
   * @param {Object} context - Additional context (recent events, stats, etc.)
   * @returns {Array} - Alerts triggered
   */
  evaluate(event, context = {}) {
    const triggered = [];

    for (const rule of this.rules) {
      if (!rule.enabled) continue;

      let fired = false;

      switch (rule.type) {
        case 'threshold':
          fired = this._evaluateThreshold(event, rule);
          break;
        case 'frequency':
          fired = this._evaluateFrequency(event, rule, context);
          break;
        case 'pattern':
          fired = this._evaluatePattern(event, rule);
          break;
        case 'absence':
          fired = this._evaluateAbsence(event, rule, context);
          break;
        default:
          break;
      }

      if (fired) {
        const alert = {
          id: `alert-${Date.now()}-${Math.random().toString(36).substr(2, 6)}`,
          ruleId: rule.id,
          ruleName: rule.name,
          severity: rule.severity || 'medium',
          message: this._renderMessage(rule.message, event),
          event: { id: event.id, type: event.type, timestamp: event.timestamp },
          triggeredAt: new Date().toISOString(),
        };

        this.alerts.push(alert);
        triggered.push(alert);

        // Notify listeners
        for (const listener of this.listeners) {
          try {
            listener(alert);
          } catch (e) {
            // Don't let listener errors break alert processing
          }
        }
      }
    }

    return triggered;
  }

  /**
   * Evaluate events in bulk and return all triggered alerts
   * @param {Array} events - Events to evaluate
   * @returns {Array} - All triggered alerts
   */
  evaluateAll(events) {
    const allAlerts = [];
    const recentEvents = [];

    for (const event of events) {
      recentEvents.push(event);
      const context = { recentEvents: [...recentEvents] };
      const triggered = this.evaluate(event, context);
      allAlerts.push(...triggered);
    }

    return allAlerts;
  }

  /**
   * Get all fired alerts
   * @param {Object} filter - Optional filter
   * @param {string} filter.severity - Filter by severity
   * @param {string} filter.ruleId - Filter by rule ID
   * @returns {Array}
   */
  getAlerts(filter = {}) {
    let result = [...this.alerts];

    if (filter.severity) {
      result = result.filter(a => a.severity === filter.severity);
    }
    if (filter.ruleId) {
      result = result.filter(a => a.ruleId === filter.ruleId);
    }

    return result;
  }

  /**
   * Clear all alerts
   */
  clearAlerts() {
    this.alerts = [];
  }

  /**
   * Get all registered rules
   * @returns {Array}
   */
  getRules() {
    return [...this.rules];
  }

  // --- Private evaluation methods ---

  _evaluateThreshold(event, rule) {
    const { field, operator, value } = rule.condition;
    const eventValue = this._getField(event, field);

    if (eventValue === undefined || eventValue === null) return false;

    switch (operator) {
      case '>': return eventValue > value;
      case '>=': return eventValue >= value;
      case '<': return eventValue < value;
      case '<=': return eventValue <= value;
      case '==': return eventValue === value;
      case '!=': return eventValue !== value;
      default: return false;
    }
  }

  _evaluateFrequency(event, rule, context) {
    const { eventType, windowMs, maxCount } = rule.condition;

    // Only trigger on matching event types
    if (eventType && event.type !== eventType) return false;

    const recentEvents = context.recentEvents || [];
    const windowStart = new Date(Date.now() - (windowMs || 60000));

    const count = recentEvents.filter(e => {
      if (eventType && e.type !== eventType) return false;
      return new Date(e.timestamp) >= windowStart;
    }).length;

    return count >= (maxCount || 5);
  }

  _evaluatePattern(event, rule) {
    const { eventType, field, regex } = rule.condition;

    if (eventType && event.type !== eventType) return false;

    if (field && regex) {
      const value = this._getField(event, field);
      if (typeof value === 'string') {
        return new RegExp(regex).test(value);
      }
    }

    return false;
  }

  _evaluateAbsence(event, rule, context) {
    const { expectedType, windowMs } = rule.condition;
    const recentEvents = context.recentEvents || [];
    const windowStart = new Date(Date.now() - (windowMs || 300000));

    const found = recentEvents.some(e =>
      e.type === expectedType && new Date(e.timestamp) >= windowStart
    );

    // Alert fires if the expected type is NOT found
    return !found && recentEvents.length > 0;
  }

  _getField(obj, path) {
    const parts = path.split('.');
    let current = obj;
    for (const part of parts) {
      if (current === null || current === undefined) return undefined;
      current = current[part];
    }
    return current;
  }

  _renderMessage(template, event) {
    if (!template) return `Alert triggered for event ${event.type}`;
    return template
      .replace(/\{type\}/g, event.type || '')
      .replace(/\{agentId\}/g, event.agentId || '')
      .replace(/\{timestamp\}/g, event.timestamp || '')
      .replace(/\{id\}/g, event.id || '');
  }
}

module.exports = { AlertManager };
