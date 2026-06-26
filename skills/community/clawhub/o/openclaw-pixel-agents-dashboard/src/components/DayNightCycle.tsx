/**
 * DayNightCycle — Applies a color overlay based on real Phoenix time.
 *
 * Phases:
 * - Night   (10 PM - 5 AM): Dark blue overlay, desk lamp glow simulation
 * - Dawn    (5 AM - 7 AM):  Warm golden brightening
 * - Day     (7 AM - 5 PM):  No overlay (full bright)
 * - Dusk    (5 PM - 7 PM):  Warm orange darkening
 * - Evening (7 PM - 10 PM): Cool blue-ish dim
 *
 * Phoenix is America/Phoenix (MST year-round, no DST).
 */

import { useEffect, useState } from 'react';

interface TimePhase {
  overlay: string;   // CSS background for the overlay div
  opacity: number;   // Overlay opacity
  label: string;     // For debug
}

function getPhoenixHour(): number {
  // Get current hour in Phoenix timezone
  const now = new Date();
  const phoenixTime = new Date(now.toLocaleString('en-US', { timeZone: 'America/Phoenix' }));
  return phoenixTime.getHours() + phoenixTime.getMinutes() / 60;
}

function getPhase(hour: number): TimePhase {
  // Night: 22-5
  if (hour >= 22 || hour < 5) {
    return {
      overlay: 'rgba(10, 15, 40, 1)',
      opacity: 0.45,
      label: 'night',
    };
  }
  // Dawn: 5-7
  if (hour >= 5 && hour < 7) {
    const progress = (hour - 5) / 2; // 0 to 1
    const nightOpacity = 0.45 * (1 - progress);
    return {
      overlay: `rgba(${Math.round(40 + 60 * progress)}, ${Math.round(30 + 30 * progress)}, ${Math.round(40 - 20 * progress)}, 1)`,
      opacity: Math.max(0.05, nightOpacity),
      label: 'dawn',
    };
  }
  // Day: 7-17
  if (hour >= 7 && hour < 17) {
    return {
      overlay: 'transparent',
      opacity: 0,
      label: 'day',
    };
  }
  // Dusk: 17-19
  if (hour >= 17 && hour < 19) {
    const progress = (hour - 17) / 2; // 0 to 1
    return {
      overlay: `rgba(${Math.round(80 - 40 * progress)}, ${Math.round(40 - 10 * progress)}, ${Math.round(20 + 10 * progress)}, 1)`,
      opacity: 0.05 + 0.15 * progress,
      label: 'dusk',
    };
  }
  // Evening: 19-22
  const progress = (hour - 19) / 3; // 0 to 1
  return {
    overlay: `rgba(${Math.round(20 - 10 * progress)}, ${Math.round(20 - 5 * progress)}, ${Math.round(40 + 0 * progress)}, 1)`,
    opacity: 0.2 + 0.25 * progress,
    label: 'evening',
  };
}

export function DayNightCycle() {
  const [phase, setPhase] = useState<TimePhase>(() => getPhase(getPhoenixHour()));

  useEffect(() => {
    // Update every 60 seconds
    const timer = setInterval(() => {
      setPhase(getPhase(getPhoenixHour()));
    }, 60_000);
    return () => clearInterval(timer);
  }, []);

  if (phase.opacity === 0) return null;

  return (
    <div
      style={{
        position: 'absolute',
        inset: 0,
        background: phase.overlay,
        opacity: phase.opacity,
        pointerEvents: 'none',
        zIndex: 35, // Below vignette (40), above canvas
        mixBlendMode: 'multiply',
        transition: 'opacity 30s ease, background 30s ease',
      }}
    />
  );
}

/** Get a time label for display (e.g. in debug view) */
export function getTimeLabel(): string {
  const hour = getPhoenixHour();
  const phase = getPhase(hour);
  const h = Math.floor(hour);
  const m = Math.floor((hour - h) * 60);
  return `${h.toString().padStart(2, '0')}:${m.toString().padStart(2, '0')} MST (${phase.label})`;
}
