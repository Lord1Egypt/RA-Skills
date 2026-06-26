/**
 * HabitTracker — Conversational Habit Tracking
 * @author @TheShadowRose
 * @license MIT
 */
const fs = require('fs');

class HabitTracker {
  constructor(options = {}) {
    this.dataFile = options.dataFile || './habits-data.json';
    this.habits = options.habits || [];
    this.entries = this._load();
  }

  log(habitName, value = true, date) {
    if (['__proto__', 'constructor', 'prototype'].includes(habitName)) return { error: 'Invalid habit name' };
    const d = date || new Date().toISOString().split('T')[0];
    if (!this.entries[d]) this.entries[d] = Object.create(null);
    this.entries[d][habitName] = value;
    this._save();
    const streak = this.getStreak(habitName);
    return { habit: habitName, date: d, value, streak, message: `Logged ${habitName}. Streak: ${streak} days.` };
  }

  getStreak(habitName) {
    let streak = 0;
    const d = new Date();
    for (let i = 0; i < 365; i++) {
      const key = d.toISOString().split('T')[0];
      if (this.entries[key] && this.entries[key][habitName]) streak++;
      else break;
      d.setDate(d.getDate() - 1);
    }
    return streak;
  }

  weeklyReport() {
    const today = new Date();
    const days = [];
    for (let i = 6; i >= 0; i--) {
      days.push(new Date(today - i * 86400000).toISOString().split('T')[0]);
    }
    const report = {};
    for (const habit of this.habits) {
      const name = habit.name || habit;
      const completed = days.filter(d => this.entries[d] && this.entries[d][name]).length;
      report[name] = { completed, total: 7, percent: Math.round(completed / 7 * 100), streak: this.getStreak(name) };
    }
    return report;
  }

  checkIn() {
    const today = new Date().toISOString().split('T')[0];
    const done = this.entries[today] || {};
    const missing = this.habits.filter(h => !done[h.name || h]).map(h => h.name || h);
    return { date: today, completed: Object.keys(done), missing };
  }

  _load() { try { return JSON.parse(fs.readFileSync(this.dataFile, 'utf8')); } catch { return {}; } }
  _save() { try { fs.writeFileSync(this.dataFile, JSON.stringify(this.entries, null, 2)); } catch {} }
}

module.exports = { HabitTracker };
