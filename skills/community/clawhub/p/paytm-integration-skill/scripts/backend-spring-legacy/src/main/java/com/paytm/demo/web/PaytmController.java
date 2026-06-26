package com.paytm.demo.web;

import com.paytm.demo.service.PaytmDynamicQrService;
import com.paytm.demo.service.PaytmInitiateTransactionService;
import com.paytm.demo.service.PaytmInitiateTransactionService.InitiateResult;
import com.paytm.demo.service.PaytmOrderStatusService;
import com.paytm.demo.service.PaytmPaymentLinkService;
import com.paytm.demo.service.PaytmSubscriptionService;
import java.util.Collections;
import java.util.LinkedHashMap;
import java.util.Map;
import java.util.concurrent.Callable;
import javax.servlet.http.HttpServletRequest;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestHeader;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.ResponseBody;

@Controller
@RequestMapping("/paytm")
public class PaytmController {

  private final PaytmInitiateTransactionService initiateService;
  private final PaytmOrderStatusService orderStatusService;
  private final PaytmSubscriptionService subscriptionService;
  private final PaytmPaymentLinkService linkService;
  private final PaytmDynamicQrService qrService;
  private final IdempotencyCache idempotency;

  public PaytmController(PaytmInitiateTransactionService initiateService,
                         PaytmOrderStatusService orderStatusService,
                         PaytmSubscriptionService subscriptionService,
                         PaytmPaymentLinkService linkService,
                         PaytmDynamicQrService qrService,
                         IdempotencyCache idempotency) {
    this.initiateService = initiateService;
    this.orderStatusService = orderStatusService;
    this.subscriptionService = subscriptionService;
    this.linkService = linkService;
    this.qrService = qrService;
    this.idempotency = idempotency;
  }

  /**
   * Wraps a create-handler with Idempotency-Key support so double-clicks don't
   * produce two Paytm orders. Cache key is the Idempotency-Key header (preferred)
   * or {@code idempotencyKey} on the request body.
   */
  @SuppressWarnings("unchecked")
  private ResponseEntity<Object> withIdempotency(String key, Callable<Object> handler) {
    if (key != null && !key.isEmpty()) {
      IdempotencyCache.Entry cached = idempotency.get(key);
      if (cached != null) {
        return ResponseEntity.status(cached.status)
            .header("Idempotent-Replayed", "true")
            .body(cached.body);
      }
    }
    try {
      Object body = handler.call();
      if (key != null && !key.isEmpty()) idempotency.put(key, 200, body);
      return ResponseEntity.ok(body);
    } catch (PaytmUpstreamException e) {
      Map<String, Object> err = new LinkedHashMap<>();
      err.put("error", true);
      err.put("code", e.code);
      err.put("message", e.getMessage());
      if (e.orderId != null) err.put("orderId", e.orderId);
      if (e.paytm != null) err.put("paytm", e.paytm);
      int s = e.httpStatus.value();
      // Cache definitive 4xx only - never 5xx so retries can succeed.
      if (key != null && !key.isEmpty() && s >= 400 && s < 500) idempotency.put(key, s, err);
      return ResponseEntity.status(s).body(err);
    } catch (Exception e) {
      throw new IllegalStateException(e.getMessage(), e);
    }
  }

  // -- New product endpoints (Subscription / Payment Link / Dynamic QR) -----

  @PostMapping(value = "/create-subscription", consumes = MediaType.APPLICATION_JSON_VALUE, produces = MediaType.APPLICATION_JSON_VALUE)
  @ResponseBody
  public ResponseEntity<Object> createSubscription(
      @RequestHeader(value = "Idempotency-Key", required = false) String idemKey,
      @RequestBody(required = false) PaytmSubscriptionService.CreateRequest req) {
    final PaytmSubscriptionService.CreateRequest body = (req != null) ? req : new PaytmSubscriptionService.CreateRequest();
    return withIdempotency(idemKey, () -> subscriptionService.create(body));
  }

  @PostMapping(value = "/create-link", consumes = MediaType.APPLICATION_JSON_VALUE, produces = MediaType.APPLICATION_JSON_VALUE)
  @ResponseBody
  public ResponseEntity<Object> createLink(
      @RequestHeader(value = "Idempotency-Key", required = false) String idemKey,
      @RequestBody(required = false) PaytmPaymentLinkService.CreateRequest req) {
    final PaytmPaymentLinkService.CreateRequest body = (req != null) ? req : new PaytmPaymentLinkService.CreateRequest();
    return withIdempotency(idemKey, () -> linkService.create(body));
  }

  @PostMapping(value = "/create-qr", consumes = MediaType.APPLICATION_JSON_VALUE, produces = MediaType.APPLICATION_JSON_VALUE)
  @ResponseBody
  public ResponseEntity<Object> createQr(
      @RequestHeader(value = "Idempotency-Key", required = false) String idemKey,
      @RequestBody(required = false) PaytmDynamicQrService.CreateRequest req) {
    final PaytmDynamicQrService.CreateRequest body = (req != null) ? req : new PaytmDynamicQrService.CreateRequest();
    return withIdempotency(idemKey, () -> qrService.create(body));
  }

  /**
   * Reconcile a Payment Link via {@code /link/fetchTransaction}. Use this for
   * Payment Link flows instead of {@code /v3/order/status}; the response wraps
   * each payer's order under {@code body.orders[]}.
   */
  @PostMapping(value = "/link-transactions", consumes = MediaType.APPLICATION_JSON_VALUE, produces = MediaType.APPLICATION_JSON_VALUE)
  @ResponseBody
  public ResponseEntity<PaytmPaymentLinkService.FetchTransactionsResult> linkTransactions(
      @RequestBody(required = false) PaytmPaymentLinkService.FetchTransactionsRequest req) throws Exception {
    if (req == null) req = new PaytmPaymentLinkService.FetchTransactionsRequest();
    return ResponseEntity.ok(linkService.fetchTransactions(req));
  }

  /**
   * initiateTransaction → txnToken (JSON for the HTML demo).
   */
  @PostMapping(value = "/create-order", consumes = MediaType.APPLICATION_JSON_VALUE, produces = MediaType.APPLICATION_JSON_VALUE)
  @ResponseBody
  public ResponseEntity<Object> createOrder(
      @RequestHeader(value = "Idempotency-Key", required = false) String idemKey,
      @RequestBody(required = false) Map<String, String> body) {
    final Map<String, String> safe = body != null ? body : Collections.emptyMap();
    return withIdempotency(idemKey, () -> {
      InitiateResult r = initiateService.initiate(
          safe.get("amount"), safe.get("custId"),
          safe.get("mobile"), safe.get("email"),
          safe.get("orderId"));
      Map<String, Object> out = new LinkedHashMap<>();
      out.put("orderId", r.orderId);
      out.put("txnToken", r.txnToken);
      out.put("amount", r.amount);
      out.put("mid", r.mid);
      out.put("tokenType", "TXN_TOKEN");
      return out;
    });
  }

  /**
   * Transaction Status API (server-side verification) - recommended in JS Checkout docs before fulfilling orders.
   *
   * @see <a href="https://www.paytmpayments.com/docs/jscheckout-verify-payment">Verify Payment Status</a>
   */
  @PostMapping(value = "/order-status", consumes = MediaType.APPLICATION_JSON_VALUE, produces = MediaType.APPLICATION_JSON_VALUE)
  @ResponseBody
  public ResponseEntity<String> orderStatus(@RequestBody Map<String, String> body) throws Exception {
    Map<String, String> safe = body != null ? body : Collections.emptyMap();
    String orderId = safe.get("orderId");
    if (orderId == null || orderId.isEmpty()) {
      return ResponseEntity.badRequest().body("{\"error\":\"orderId required\"}");
    }
    String json = orderStatusService.fetchOrderStatusJson(orderId);
    return ResponseEntity.ok().contentType(MediaType.APPLICATION_JSON).body(json);
  }

  /**
   * Paytm browser redirect / POST callback after payment attempt.
   */
  @PostMapping(value = "/callback", consumes = MediaType.APPLICATION_FORM_URLENCODED_VALUE)
  public ResponseEntity<String> callbackForm(HttpServletRequest request) {
    return callbackView(request);
  }

  @GetMapping("/callback")
  public ResponseEntity<String> callbackGet(HttpServletRequest request) {
    return callbackView(request);
  }

  private ResponseEntity<String> callbackView(HttpServletRequest request) {
    boolean checksumOk = PaytmCallbackChecksum.verify(request);
    StringBuilder b = new StringBuilder();
    b.append("<!DOCTYPE html><html><head><meta charset=\"UTF-8\"><title>Paytm callback</title></head><body>");
    b.append("<h1>Paytm callback</h1>");
    b.append("<p><strong>CHECKSUMHASH validation:</strong> ");
    b.append(checksumOk ? "OK (signature verified)" : "FAILED or CHECKSUMHASH missing - do not treat as paid");
    b.append("</p>");
    b.append("<p>Per <a href=\"https://www.paytmpayments.com/docs/jscheckout-verify-payment\">Verify Payment Status</a>, ");
    b.append("also call Transaction Status API (or webhook) before confirming the order.</p>");
    b.append("<pre>");
    // Paytm posts callback fields directly from the user's browser, so EVERY value
    // is untrusted input. HTML-escape before rendering or you've shipped reflected XSS.
    request.getParameterMap().forEach((k, v) ->
        b.append(escapeHtml(k)).append("=").append(escapeHtml(String.join(",", v))).append('\n'));
    b.append("</pre></body></html>");
    return ResponseEntity.ok().contentType(MediaType.TEXT_HTML).body(b.toString());
  }

  private static String escapeHtml(String s) {
    if (s == null) return "";
    StringBuilder out = new StringBuilder(s.length());
    for (int i = 0; i < s.length(); i++) {
      char c = s.charAt(i);
      switch (c) {
        case '&': out.append("&amp;"); break;
        case '<': out.append("&lt;"); break;
        case '>': out.append("&gt;"); break;
        case '"': out.append("&quot;"); break;
        case '\'': out.append("&#39;"); break;
        default: out.append(c);
      }
    }
    return out.toString();
  }
}
