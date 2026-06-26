package com.paytm.demo.web;

import java.time.Duration;
import java.time.Instant;
import java.util.LinkedHashMap;
import java.util.Map;
import org.springframework.stereotype.Component;

/**
 * Minimal in-process idempotency cache for the reference create endpoints.
 *
 * <p>PRODUCTION NOTE: in-memory and per-process - fine for the demo, NOT for a
 * real merchant deployment. Replace with Redis / a DB row keyed on the
 * idempotency key before going live.
 */
@Component
public class IdempotencyCache {

  private static final Duration TTL = Duration.ofHours(24);
  private static final int MAX_ENTRIES = 10_000;

  // LinkedHashMap with access-order = LRU; we still time-evict on read.
  private final Map<String, Entry> cache = new LinkedHashMap<>(16, 0.75f, true) {
    @Override protected boolean removeEldestEntry(Map.Entry<String, Entry> eldest) {
      return size() > MAX_ENTRIES;
    }
  };

  public synchronized Entry get(String key) {
    if (key == null || key.isEmpty()) return null;
    Entry e = cache.get(key);
    if (e == null) return null;
    if (Duration.between(e.createdAt, Instant.now()).compareTo(TTL) > 0) {
      cache.remove(key);
      return null;
    }
    return e;
  }

  public synchronized void put(String key, int status, Object body) {
    if (key == null || key.isEmpty()) return;
    cache.put(key, new Entry(status, body, Instant.now()));
  }

  /**
   * Read the idempotency key from the {@code Idempotency-Key} header (preferred)
   * or {@code idempotencyKey} on the request body.
   */
  public static String readKey(String headerValue, Object bodyKey) {
    if (headerValue != null && !headerValue.trim().isEmpty()) return headerValue.trim();
    if (bodyKey instanceof String s && !s.trim().isEmpty()) return s.trim();
    return null;
  }

  public static final class Entry {
    public final int status;
    public final Object body;
    public final Instant createdAt;

    Entry(int status, Object body, Instant createdAt) {
      this.status = status;
      this.body = body;
      this.createdAt = createdAt;
    }
  }
}
