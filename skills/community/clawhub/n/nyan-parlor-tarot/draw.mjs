#!/usr/bin/env node
// Offline tarot draw: N distinct cards from the 78-card Rider–Waite–Smith deck, crypto-random.
// Usage: node draw.mjs [count=3] [--upright]
import { randomInt } from 'node:crypto';

const MAJOR = ['The Fool', 'The Magician', 'The High Priestess', 'The Empress', 'The Emperor', 'The Hierophant', 'The Lovers', 'The Chariot', 'Strength', 'The Hermit', 'Wheel of Fortune', 'Justice', 'The Hanged Man', 'Death', 'Temperance', 'The Devil', 'The Tower', 'The Star', 'The Moon', 'The Sun', 'Judgement', 'The World'];
const RANKS = ['Ace', 'Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Page', 'Knight', 'Queen', 'King'];
const SUITS = ['Wands', 'Cups', 'Swords', 'Pentacles'];
const DECK = [...MAJOR, ...SUITS.flatMap((s) => RANKS.map((r) => `${r} of ${s}`))];
const slug = (name) => name.toLowerCase().replace(/\s+/g, '-');

const count = Math.min(Math.max(parseInt(process.argv[2] ?? '3', 10) || 3, 1), 10);
const upright = process.argv.includes('--upright');
const pool = [...DECK];
for (let i = 0; i < count; i++) {
  const j = i + randomInt(pool.length - i);
  [pool[i], pool[j]] = [pool[j], pool[i]];
  const reversed = !upright && randomInt(2) === 1;
  console.log(`${i + 1}. ${pool[i]}${reversed ? ' (reversed)' : ''}  https://www.tarotoper.com/en/tarot-card-meanings/${slug(pool[i])}`);
}
