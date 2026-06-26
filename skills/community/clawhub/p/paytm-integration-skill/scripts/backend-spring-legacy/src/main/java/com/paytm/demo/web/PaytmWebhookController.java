package com.paytm.demo.web;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.paytm.demo.config.PaytmMerchantConfig;
import com.paytm.pg.merchant.PaytmChecksum;
import java.io.BufferedReader;
import java.nio.charset.StandardCharsets;
import java.time.Instant;
import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.Collections;
import java.util.Deque;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.concurrent.ConcurrentHashMap;
import javax.servlet.http.HttpServletRequest;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.ResponseBody;

/**
 * Paytm S2S webhook receiver.
 *
 * Contract:
 *  1. Read raw body bytes (we read from the servlet input stream verbatim).
 *  2. Extract head.signature; verify against the body bytes Paytm signed.
 *     Re-serializing here would change key order / whitespace and break the
 *     signature - use the bytes Paytm sent.
 *  3. Idempotency check on (orderId, status) - Paytm retries at-least-once.
 *  4. Persist event for audit (here, in-memory ring buffer).
 *  5. Apply state transition (here, a stub log - replace with your DB write).
 *  6. Return 200 fast. Heavy lifting goes to a queue.
 */
@Controller
public class PaytmWebhookController {

  private static final ObjectMapper MAPPER = new ObjectMapper();

  // (orderId|status) - at-least-once dedup. Replace with Redis in production.
  private final Set<String> seen = ConcurrentHashMap.newKeySet();

  // Bounded ring buffer of recent webhook events for in-process audit / debugging.
  // Matches the 200-event cap in the Node + Python backends.
  private static final int EVENT_LOG_MAX = 200;
  private final Deque<LoggedEvent> eventLog = new ArrayDeque<>(EVENT_LOG_MAX);

  /** Snapshot the most-recent events (newest first). */
  public synchronized List<LoggedEvent> recentEvents() {
    List<LoggedEvent> out = new ArrayList<>(eventLog);
    Collections.reverse(out);
    return out;
  }

  private synchronized void rememberEvent(JsonNode parsed) {
    if (eventLog.size() >= EVENT_LOG_MAX) eventLog.removeFirst();
    eventLog.addLast(new LoggedEvent(Instant.now(), parsed));
  }

  /** Audit-log entry shape - timestamp + parsed payload. */
  public static final class LoggedEvent {
    public final Instant at;
    public final JsonNode payload;

    LoggedEvent(Instant at, JsonNode payload) {
      this.at = at;
      this.payload = payload;
    }
  }

  @PostMapping(value = "/paytm/webhook", consumes = MediaType.APPLICATION_JSON_VALUE,
               produces = MediaType.APPLICATION_JSON_VALUE)
  @ResponseBody
  public ResponseEntity<Map<String, Object>> webhook(HttpServletRequest request) {
    String rawBody = readRawBody(request);
    JsonNode parsed;
    try {
      parsed = MAPPER.readTree(rawBody == null ? "{}" : rawBody);
    } catch (Exception e) {
      return error(400, "invalid JSON: " + e.getMessage());
    }

    String signature = parsed.path("head").path("signature").asText("");
    if (signature.isEmpty()) {
      return error(401, "missing head.signature");
    }

    // Verify the signed body bytes (NOT a re-serialization).
    String bodyBytes = extractBodyBytes(rawBody);
    if (bodyBytes == null) {
      bodyBytes = parsed.path("body").toString();    // best-effort fallback
    }
    boolean ok;
    try {
      ok = PaytmChecksum.verifySignature(bodyBytes,
          PaytmMerchantConfig.merchantKey(), signature);
    } catch (Exception e) {
      ok = false;
    }
    if (!ok) {
      return error(401, "invalid signature");
    }

    // Persist for audit BEFORE dedup so duplicates are visible in the log.
    rememberEvent(parsed);

    String orderId = parsed.path("body").path("orderId").asText("unknown");
    String status = parsed.path("body").path("status").asText(
        parsed.path("body").path("STATUS").asText("unknown"));
    String dedupKey = orderId + "|" + status;
    if (!seen.add(dedupKey)) {
      Map<String, Object> body = new LinkedHashMap<>();
      body.put("ok", true);
      body.put("dedup", true);
      body.put("orderId", orderId);
      body.put("status", status);
      return ResponseEntity.ok(body);
    }
    if (seen.size() > 50_000) seen.clear();          // crude wrap; Redis has TTLs in real life

    fulfillOrder(orderId, status, parsed);

    Map<String, Object> body = new LinkedHashMap<>();
    body.put("ok", true);
    body.put("orderId", orderId);
    body.put("status", status);
    return ResponseEntity.ok(body);
  }

  // -- helpers ---------------------------------------------------------------

  private static String readRawBody(HttpServletRequest request) {
    try (BufferedReader r = request.getReader()) {
      StringBuilder sb = new StringBuilder();
      char[] buf = new char[4096];
      int n;
      while ((n = r.read(buf)) > 0) sb.append(buf, 0, n);
      return sb.toString();
    } catch (Exception e) {
      return null;
    }
  }

  /**
   * Substring of the raw body that corresponds to "body": {...}. Paytm signs
   * those bytes verbatim - re-serializing would change key order / whitespace.
   */
  static String extractBodyBytes(String raw) {
    if (raw == null) return null;
    int idx = raw.indexOf("\"body\"");
    if (idx < 0) return null;
    int colon = raw.indexOf(':', idx);
    if (colon < 0) return null;
    int start = -1;
    for (int i = colon + 1; i < raw.length(); i++) {
      char c = raw.charAt(i);
      if (Character.isWhitespace(c)) continue;
      if (c == '{') { start = i; break; }
      return null;
    }
    if (start < 0) return null;
    int depth = 0;
    boolean inString = false, escape = false;
    for (int i = start; i < raw.length(); i++) {
      char c = raw.charAt(i);
      if (escape) { escape = false; continue; }
      if (c == '\\') { escape = true; continue; }
      if (c == '"') { inString = !inString; continue; }
      if (inString) continue;
      if (c == '{') depth++;
      else if (c == '}') {
        depth--;
        if (depth == 0) return raw.substring(start, i + 1);
      }
    }
    return null;
  }

  /** Replace with your real DB write / queue push. Keep it fast - webhook timeout is 10s. */
  private void fulfillOrder(String orderId, String status, JsonNode parsed) {
    System.out.println("[paytm webhook] fulfill stub orderId=" + orderId
        + " status=" + status + " mid=" + parsed.path("body").path("mid").asText("?"));
  }

  private static ResponseEntity<Map<String, Object>> error(int status, String msg) {
    Map<String, Object> body = new LinkedHashMap<>();
    body.put("ok", false);
    body.put("error", msg);
    return ResponseEntity.status(status).body(body);
  }
}
