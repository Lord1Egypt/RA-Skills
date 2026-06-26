/**
 * LogTail — Smart Log Monitor & Analyzer
 * @author @TheShadowRose
 * @license MIT
 */
const fs = require('fs');
const path = require('path');

class LogTail {
  constructor(options = {}) {
    this.files = options.files || [];
    this.filters = options.filters || { ignore: [], highlight: [] };
    // Note: timestamps are set at receive time, not parsed from log lines
    this.buffer = [];
    this.maxBuffer = options.maxBuffer || 10000;
  }

  watch(callback) {
    this.stop(); // Clear any existing watchers
    for (const file of this.files) {
      try {
        let size = fs.statSync(file).size;
        let reading = false;
        const watcher = fs.watchFile(file, { interval: 1000 }, () => {
          if (reading) return; // Prevent overlapping reads
          const newSize = fs.statSync(file).size;
          if (newSize < size) { size = 0; } // Log rotation detected — reset
          if (newSize > size) {
            reading = true;
            const stream = fs.createReadStream(file, { start: size, encoding: 'utf8' });
            let chunk = '';
            stream.on('data', d => chunk += d);
            stream.on('end', () => {
              const lines = chunk.split('\n').filter(l => l.trim());
              for (const line of lines) {
                const entry = this._parse(line);
                if (this._shouldIgnore(entry)) continue;
                this.buffer.push(entry);
                if (this.buffer.length > this.maxBuffer) this.buffer.shift();
                if (callback) callback(entry);
              }
            });
            stream.on('error', () => { reading = false; });
            stream.on('close', () => { reading = false; });
            size = newSize;
          }
        });
        // watcher tracked by fs.watchFile internally
      } catch {}
    }
    return this;
  }

  stop() { for (const f of this.files) fs.unwatchFile(f); }

  async summarize(options = {}) {
    const period = options.period || '1h';
    const ms = this._parsePeriod(period);
    const cutoff = Date.now() - ms;
    const entries = this.buffer.filter(e => e.timestamp >= cutoff);

    const errors = entries.filter(e => e.severity === 'error' || e.severity === 'fatal');
    const warnings = entries.filter(e => e.severity === 'warning');

    // Group errors by message pattern
    const errorGroups = {};
    for (const e of errors) {
      const key = e.message.substring(0, 60);
      errorGroups[key] = (errorGroups[key] || 0) + 1;
    }

    const topErrors = Object.entries(errorGroups)
      .sort((a, b) => b[1] - a[1])
      .slice(0, 5)
      .map(([msg, count]) => ({ message: msg, count }));

    return {
      period,
      total: entries.length,
      errors: errors.length,
      warnings: warnings.length,
      errorRate: entries.length ? (errors.length / entries.length * 100).toFixed(2) + '%' : '0%',
      topErrors,
      summary: errors.length === 0
        ? `✅ Clean — ${entries.length} entries, no errors in last ${period}`
        : `⚠️ ${errors.length} errors in ${entries.length} entries (last ${period})`
    };
  }

  _parse(line) {
    const severity = /\b(error|fatal|critical)\b/i.test(line) ? 'error'
      : /\b(warn|warning)\b/i.test(line) ? 'warning'
      : /\b(info)\b/i.test(line) ? 'info' : 'debug';
    return { timestamp: Date.now(), raw: line, message: line.substring(0, 200), severity };
  }

  _shouldIgnore(entry) {
    return this.filters.ignore.some(pat =>
      entry.raw.toLowerCase().includes(pat.toLowerCase())
    );
  }

  _parsePeriod(p) {
    const m = p.match(/(\d+)([smhd])/);
    if (!m) return 3600000;
    const val = parseInt(m[1]);
    const unit = { s: 1000, m: 60000, h: 3600000, d: 86400000 }[m[2]];
    return val * unit;
  }
}

module.exports = { LogTail };
