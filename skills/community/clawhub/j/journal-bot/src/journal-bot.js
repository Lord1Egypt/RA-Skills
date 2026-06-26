/**
 * JournalBot — Daily Journaling with AI Prompts
 * @author @TheShadowRose
 * @license MIT
 */
const fs = require('fs');
const path = require('path');

const PROMPTS = [
  "What was the highlight of your day?",
  "What was challenging today?",
  "What did you learn today?",
  "Name one thing you're grateful for.",
  "Describe today in three words.",
  "What are you looking forward to?",
  "What would you do differently today?",
  "Who made a positive impact on your day?",
  "What surprised you today?",
  "What's on your mind right now?"
];

class JournalBot {
  constructor(options = {}) {
    this.journalDir = options.journalDir || './journal';
    if (!fs.existsSync(this.journalDir)) fs.mkdirSync(this.journalDir, { recursive: true });
  }

  getPrompt() {
    const idx = Math.floor(Date.now() / 86400000) % PROMPTS.length;
    return PROMPTS[idx];
  }

  addEntry(text, mood) {
    const date = new Date().toISOString().split('T')[0];
    const time = new Date().toLocaleTimeString();
    const file = path.join(this.journalDir, `${date}.md`);
    const entry = `\n## ${time}${mood ? ' | Mood: ' + mood : ''}\n\n${text}\n`;
    if (!fs.existsSync(file)) {
      fs.writeFileSync(file, `# Journal — ${date}\n${entry}`);
    } else {
      fs.appendFileSync(file, entry);
    }
    return { date, time, file, wordCount: text.split(/\s+/).length };
  }

  getEntries(date) {
    const d = date || new Date().toISOString().split('T')[0];
    if (!/^\d{4}-\d{2}-\d{2}$/.test(d)) return null; // Validate date format
    const file = path.join(this.journalDir, `${d}.md`);
    try { return fs.readFileSync(file, 'utf8'); } catch { return null; }
  }

  weeklyStats() {
    const today = new Date();
    let totalWords = 0, daysWritten = 0;
    for (let i = 0; i < 7; i++) {
      const d = new Date(today - i * 86400000).toISOString().split('T')[0];
      const content = this.getEntries(d);
      if (content) { daysWritten++; totalWords += content.split(/\s+/).length; }
    }
    return { daysWritten, totalWords, avgWords: daysWritten ? Math.round(totalWords / daysWritten) : 0 };
  }
}

module.exports = { JournalBot };
