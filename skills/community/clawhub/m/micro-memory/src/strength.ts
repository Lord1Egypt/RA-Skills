// Micro Memory - Strength System

import { Memory, Strength } from './types';
import { formatTimestamp, daysBetween, getStrengthLevel } from './utils';

// Decay rates per day for each level
const DECAY_RATES: Record<string, number> = {
  critical: 5,
  weak: 3,
  stable: 1,
  strong: 0.5,
  permanent: 0.1,
};

// Reinforce boost multipliers
const BOOST_MULTIPLIERS: Record<number, number> = {
  1: 1.2,
  2: 1.5,
  3: 2.0,
};

export function calculateDecay(memory: Memory): number {
  const now = new Date();
  const lastReinforced = new Date(memory.strength.lastReinforced.replace(' ', 'T'));
  const days = daysBetween(lastReinforced, now);
  const rate = DECAY_RATES[memory.strength.level] || 1;
  return Math.min(days * rate, memory.strength.score);
}

export function updateStrength(memory: Memory): Strength {
  const decay = calculateDecay(memory);
  const newScore = Math.max(0, memory.strength.score - decay);
  const level = getStrengthLevel(newScore) as Strength['level'];
  
  return {
    level,
    score: Math.round(newScore),
    lastReinforced: memory.strength.lastReinforced,
  };
}

export function reinforce(memory: Memory, boost: number = 1): Strength {
  const multiplier = BOOST_MULTIPLIERS[boost] || 1.2;
  const newScore = Math.min(100, memory.strength.score * multiplier + 10);
  const level = getStrengthLevel(newScore) as Strength['level'];
  
  return {
    level,
    score: Math.round(newScore),
    lastReinforced: formatTimestamp(),
  };
}

export function getStrengthEmoji(level: string): string {
  const emojis: Record<string, string> = {
    permanent: '💎',
    strong: '💪',
    stable: '📊',
    weak: '⚠️',
    critical: '🔴',
  };
  return emojis[level] || '❓';
}

export function getDecayWarning(memory: Memory): string | null {
  const decay = calculateDecay(memory);
  if (decay > 20) {
    return `⚠️ 记忆即将衰减 ${decay.toFixed(0)} 点，建议复习！`;
  }
  if (memory.strength.level === 'critical') {
    return '🔴 记忆处于临界状态，急需复习！';
  }
  return null;
}

export function getOptimalReviewInterval(level: string): number {
  const intervals: Record<string, number> = {
    critical: 1,
    weak: 3,
    stable: 7,
    strong: 14,
    permanent: 30,
  };
  return intervals[level] || 7;
}
