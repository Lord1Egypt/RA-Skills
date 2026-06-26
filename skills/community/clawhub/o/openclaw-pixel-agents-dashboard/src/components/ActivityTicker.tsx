/**
 * ActivityTicker — Scrolling news ticker showing recent agent activity.
 * Shows events like "🥧 Earl: Reading SOUL.md", "🔧 Larry: Writing App.tsx"
 */

import { useEffect, useRef, useState } from 'react';

interface TickerEntry {
  id: number;
  text: string;
  timestamp: number;
}

interface ActivityTickerProps {
  /** Ref that parent updates when new events arrive */
  eventsRef: React.RefObject<TickerEntry[]>;
}

const MAX_ENTRIES = 30;
const ENTRY_LIFETIME_MS = 5 * 60_000; // 5 minutes

export function ActivityTicker({ eventsRef }: ActivityTickerProps) {
  const [, setTick] = useState(0);
  const scrollRef = useRef<HTMLDivElement>(null);

  // Re-render periodically to pick up new events
  useEffect(() => {
    const timer = setInterval(() => setTick(n => n + 1), 1000);
    return () => clearInterval(timer);
  }, []);

  // Auto-scroll to the right (newest)
  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollLeft = scrollRef.current.scrollWidth;
    }
  });

  const now = Date.now();
  const entries = (eventsRef.current || []).filter(
    e => now - e.timestamp < ENTRY_LIFETIME_MS
  ).slice(-MAX_ENTRIES);

  if (entries.length === 0) return null;

  return (
    <div
      style={{
        position: 'absolute',
        bottom: 30, // above the bottom toolbar
        left: 0,
        right: 0,
        zIndex: 45,
        pointerEvents: 'none',
      }}
    >
      <div
        ref={scrollRef}
        style={{
          display: 'flex',
          gap: 24,
          padding: '4px 12px',
          background: 'rgba(10, 10, 20, 0.75)',
          borderTop: '1px solid rgba(255,255,255,0.08)',
          overflowX: 'hidden',
          whiteSpace: 'nowrap',
          fontFamily: 'monospace',
          fontSize: '11px',
          color: 'rgba(255,255,255,0.5)',
        }}
      >
        {entries.map(entry => {
          const age = now - entry.timestamp;
          const opacity = age > 3 * 60_000 ? 0.3 : age > 60_000 ? 0.5 : 0.8;
          return (
            <span key={entry.id} style={{ opacity, flexShrink: 0 }}>
              {entry.text}
            </span>
          );
        })}
      </div>
    </div>
  );
}

/** Push a new event to the ticker entries array */
let nextId = 0;
export function pushTickerEvent(
  entries: TickerEntry[],
  text: string,
): TickerEntry[] {
  const entry: TickerEntry = {
    id: nextId++,
    text,
    timestamp: Date.now(),
  };
  const result = [...entries, entry];
  // Keep within max
  if (result.length > MAX_ENTRIES * 2) {
    return result.slice(-MAX_ENTRIES);
  }
  return result;
}
