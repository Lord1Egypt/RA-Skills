/**
 * Exporter - Export agent events to various formats
 *
 * Supports JSON, CSV, and Markdown export.
 */
class Exporter {
  /**
   * Export events to JSON string
   * @param {Array} events - Events to export
   * @param {Object} options - Export options
   * @param {boolean} options.pretty - Pretty-print JSON (default: true)
   * @returns {string} - JSON string
   */
  static toJSON(events, options = {}) {
    const pretty = options.pretty !== false;
    return JSON.stringify(events, null, pretty ? 2 : 0);
  }

  /**
   * Export events to CSV string
   * @param {Array} events - Events to export
   * @param {Object} options - Export options
   * @param {string[]} options.columns - Columns to include (default: auto-detect)
   * @param {string} options.delimiter - Column delimiter (default: ',')
   * @returns {string} - CSV string
   */
  static toCSV(events, options = {}) {
    if (!events || events.length === 0) return '';

    const delimiter = options.delimiter || ',';

    // Determine columns - use provided or auto-detect from all events
    const columns = options.columns || Exporter._detectColumns(events);

    // Build header row
    const header = columns.map(c => Exporter._escapeCSV(c)).join(delimiter);

    // Build data rows
    const rows = events.map(event => {
      return columns.map(col => {
        const value = Exporter._getNestedValue(event, col);
        return Exporter._escapeCSV(Exporter._formatValue(value));
      }).join(delimiter);
    });

    return [header, ...rows].join('\n');
  }

  /**
   * Export events to Markdown table
   * @param {Array} events - Events to export
   * @param {Object} options - Export options
   * @param {string[]} options.columns - Columns to include (default: auto-detect core fields)
   * @param {string} options.title - Optional title for the report
   * @returns {string} - Markdown string
   */
  static toMarkdown(events, options = {}) {
    if (!events || events.length === 0) return options.title ? `# ${options.title}\n\nNo events found.\n` : 'No events found.\n';

    const columns = options.columns || ['id', 'type', 'agentId', 'action', 'timestamp'];
    const lines = [];

    if (options.title) {
      lines.push(`# ${options.title}`, '');
    }

    lines.push(`**Total Events:** ${events.length}`, '');

    // Table header
    lines.push('| ' + columns.map(c => c).join(' | ') + ' |');
    lines.push('| ' + columns.map(() => '---').join(' | ') + ' |');

    // Table rows
    for (const event of events) {
      const row = columns.map(col => {
        const value = Exporter._getNestedValue(event, col);
        const formatted = Exporter._formatValue(value);
        // Escape pipes in markdown
        return formatted.replace(/\|/g, '\\|');
      });
      lines.push('| ' + row.join(' | ') + ' |');
    }

    lines.push('');
    return lines.join('\n');
  }

  /**
   * Auto-detect columns from event data
   * @param {Array} events - Events to inspect
   * @returns {string[]} - Column names
   */
  static _detectColumns(events) {
    const columnSet = new Set();
    // Prioritize common fields first
    const priorityFields = ['id', 'type', 'agentId', 'action', 'timestamp', 'category', 'severity'];
    for (const field of priorityFields) {
      columnSet.add(field);
    }

    for (const event of events) {
      for (const key of Object.keys(event)) {
        columnSet.add(key);
      }
    }
    return Array.from(columnSet);
  }

  /**
   * Get a possibly nested value from an object
   * @param {Object} obj
   * @param {string} path - Dot-separated path
   * @returns {*}
   */
  static _getNestedValue(obj, path) {
    const parts = path.split('.');
    let current = obj;
    for (const part of parts) {
      if (current === null || current === undefined) return '';
      current = current[part];
    }
    return current;
  }

  /**
   * Format a value for text output
   * @param {*} value
   * @returns {string}
   */
  static _formatValue(value) {
    if (value === null || value === undefined) return '';
    if (typeof value === 'object') return JSON.stringify(value);
    return String(value);
  }

  /**
   * Escape a value for CSV
   * @param {string} value
   * @returns {string}
   */
  static _escapeCSV(value) {
    if (value === null || value === undefined) return '';
    const str = String(value);
    if (str.includes(',') || str.includes('"') || str.includes('\n')) {
      return '"' + str.replace(/"/g, '""') + '"';
    }
    return str;
  }
}

module.exports = { Exporter };
