package com.paytm.demo.service;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.paytm.demo.config.PaytmMerchantConfig;
import com.paytm.demo.web.PaytmUpstreamException;
import com.paytm.pg.merchant.PaytmChecksum;
import java.math.BigDecimal;
import java.math.RoundingMode;
import java.security.SecureRandom;
import java.time.ZoneId;
import java.time.ZonedDateTime;
import java.time.format.DateTimeFormatter;
import java.util.LinkedHashMap;
import java.util.Map;
import org.json.JSONObject;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestClientResponseException;
import org.springframework.web.client.RestTemplate;

/**
 * Create Payment Link - POST /link/create.
 *
 * Doc: https://www.paytmpayments.com/docs/api/create-link-api
 *
 * Defaults & gotchas baked in (matching Node + Python):
 *  - head requires tokenType "AES" + timestamp (Unix epoch SECONDS as string)
 *  - linkType: "FIXED" by default (GENERIC ignores amount)
 *  - amount is a JSON number, NOT a string
 *  - linkName: alphanumerics ONLY (no spaces) - some MIDs reject space here.
 *    Sanitize via sanitizeLinkName() below.
 *  - linkDescription: alphanumerics + spaces. Sanitize via sanitizeDescription().
 *    Both fields must be >= 3 chars.
 *  - customer details nested under customerContact (not top-level)
 *  - expiryDate format DD/MM/YYYY HH:MM:SS (most MIDs)
 */
@Service
public class PaytmPaymentLinkService {

  private static final ObjectMapper MAPPER = new ObjectMapper();
  private static final SecureRandom RANDOM = new SecureRandom();
  private static final ZoneId IST = ZoneId.of("Asia/Kolkata");
  private static final DateTimeFormatter EXPIRY_FMT =
      DateTimeFormatter.ofPattern("dd/MM/yyyy HH:mm:ss");

  private final RestTemplate restTemplate;

  public PaytmPaymentLinkService(RestTemplate restTemplate) {
    this.restTemplate = restTemplate;
  }

  public CreateResult create(CreateRequest req) throws Exception {
    return create(req, null);
  }

  /**
   * Overload that accepts a per-request {@code requestBaseUrl} for callback derivation -
   * matches the {@code serverBaseUrl} parameter on Node/Python.
   */
  public CreateResult create(CreateRequest req, String requestBaseUrl) throws Exception {
    String orderId = (req.orderId != null && !req.orderId.trim().isEmpty())
        ? req.orderId.trim() : "LNK_" + randomHex();

    JSONObject customerContact = new JSONObject();
    if (notEmpty(req.customerName)) customerContact.put("customerName", req.customerName.trim());
    if (notEmpty(req.customerEmail)) customerContact.put("customerEmail", req.customerEmail.trim());
    if (notEmpty(req.customerMobile)) customerContact.put("customerMobile", req.customerMobile.trim());
    if (notEmpty(req.customerId)) customerContact.put("customerId", req.customerId.trim());

    JSONObject body = new JSONObject();
    body.put("mid", PaytmMerchantConfig.mid());
    body.put("linkType", "FIXED");
    body.put("linkName", sanitizeLinkName(req.linkName, "Invoice"));
    body.put("linkDescription", sanitizeDescription(req.linkDescription, "Invoice payment"));
    body.put("amount", normalizeAmountAsNumber(req.amount));
    body.put("sendSms", req.sendSms != null ? req.sendSms : Boolean.TRUE);
    body.put("sendEmail", req.sendEmail != null ? req.sendEmail : Boolean.TRUE);
    body.put("customerContact", customerContact);
    body.put("expiryDate", notEmpty(req.expiryDate) ? req.expiryDate.trim() : oneYearFromNowExpiry());
    body.put("orderId", orderId);
    body.put("callbackUrl", notEmpty(req.callbackUrl) ? req.callbackUrl.trim()
        : PaytmMerchantConfig.callbackUrl(requestBaseUrl));
    if (notEmpty(req.merchantUniqueReference)) {
      body.put("merchantUniqueReference", req.merchantUniqueReference.trim());
    }


    String checksum = PaytmChecksum.generateSignature(body.toString(), PaytmMerchantConfig.merchantKey());
    JSONObject head = new JSONObject();
    head.put("tokenType", "AES");
    head.put("signature", checksum);
    head.put("timestamp", String.valueOf(System.currentTimeMillis() / 1000));

    JSONObject paytmParams = new JSONObject();
    paytmParams.put("body", body);
    paytmParams.put("head", head);

    HttpHeaders headers = new HttpHeaders();
    headers.setContentType(MediaType.APPLICATION_JSON);
    HttpEntity<String> entity = new HttpEntity<>(paytmParams.toString(), headers);

    String responseBody;
    try {
      ResponseEntity<String> response = restTemplate.postForEntity(
          PaytmMerchantConfig.linkCreateUrl(), entity, String.class);
      responseBody = response.getBody();
    } catch (RestClientResponseException e) {
      throw upstream("LINK_HTTP_ERROR",
          "link/create failed (HTTP " + e.getRawStatusCode() + ")",
          orderId, e.getResponseBodyAsString());
    }

    JsonNode root = MAPPER.readTree(responseBody);
    JsonNode info = root.path("body").path("resultInfo");
    String status = info.path("resultStatus").asText("");
    if (!status.isEmpty() && !"SUCCESS".equals(status) && !"S".equals(status)) {
      throw upstream("LINK_FAILED",
          info.path("resultMsg").asText("link/create failed"), orderId, responseBody);
    }

    JsonNode bodyResp = root.path("body");
    // Read defensively - current Paytm returns linkId; older docs LinkID.
    long linkId = bodyResp.path("linkId").asLong(bodyResp.path("LinkID").asLong(0L));

    return new CreateResult(
        orderId,
        linkId,
        bodyResp.path("shortUrl").asText(null),
        bodyResp.path("longUrl").asText(null),
        bodyResp.path("linkStatus").asText("ACTIVE"),
        body.getDouble("amount"),
        PaytmMerchantConfig.mid());
  }

  /**
   * Fetch transactions for a Payment Link - POST /link/fetchTransaction.
   * Doc: https://www.paytmpayments.com/docs/api/fetch-transaction-link-api
   *
   * <p>USE THIS for Payment Link reconciliation, NOT /v3/order/status. Returns
   * a {@link FetchTransactionsResult} with {@code orders} as a list (may be
   * empty when no payments yet - Paytm's 404 / "Data Not Found" is normalised
   * to an empty list so callers can treat all valid responses uniformly).
   */
  public FetchTransactionsResult fetchTransactions(FetchTransactionsRequest req) throws Exception {
    if (req == null || req.linkId == null) {
      throw new IllegalArgumentException("linkId is required");
    }

    JSONObject body = new JSONObject();
    body.put("mid", PaytmMerchantConfig.mid());
    body.put("linkId", req.linkId.longValue());
    body.put("pageNo", req.pageNo != null ? req.pageNo : 1);
    body.put("pageSize", req.pageSize != null ? req.pageSize : 10);
    body.put("fetchAllTxns", req.fetchAllTxns != null ? req.fetchAllTxns : Boolean.TRUE);

    String checksum = PaytmChecksum.generateSignature(body.toString(), PaytmMerchantConfig.merchantKey());
    JSONObject head = new JSONObject();
    head.put("tokenType", "AES");
    head.put("signature", checksum);

    JSONObject paytmParams = new JSONObject();
    paytmParams.put("body", body);
    paytmParams.put("head", head);

    HttpHeaders headers = new HttpHeaders();
    headers.setContentType(MediaType.APPLICATION_JSON);
    HttpEntity<String> entity = new HttpEntity<>(paytmParams.toString(), headers);

    String responseBody;
    try {
      ResponseEntity<String> response = restTemplate.postForEntity(
          PaytmMerchantConfig.linkFetchTransactionUrl(), entity, String.class);
      responseBody = response.getBody();
    } catch (RestClientResponseException e) {
      throw upstream("LINK_FETCH_TXN_HTTP_ERROR",
          "link/fetchTransaction failed (HTTP " + e.getRawStatusCode() + ")",
          String.valueOf(req.linkId), e.getResponseBodyAsString());
    }

    JsonNode root = MAPPER.readTree(responseBody);
    JsonNode info = root.path("body").path("resultInfo");
    String code = info.path("resultCode").asText("");
    String msg = info.path("resultMessage").asText(info.path("resultMsg").asText(""));
    String status = info.path("resultStatus").asText("");

    if ("404".equals(code) || msg.toLowerCase().contains("not found")) {
      return new FetchTransactionsResult(req.linkId, new java.util.ArrayList<>(),
          code, status.isEmpty() ? "FAILED" : status, msg);
    }
    if (!status.isEmpty() && !"SUCCESS".equals(status) && !"S".equals(status)) {
      throw upstream("LINK_FETCH_TXN_FAILED",
          msg.isEmpty() ? "link/fetchTransaction failed" : msg,
          String.valueOf(req.linkId), responseBody);
    }

    java.util.List<JsonNode> orders = new java.util.ArrayList<>();
    JsonNode arr = root.path("body").path("orders");
    if (arr.isArray()) arr.forEach(orders::add);
    return new FetchTransactionsResult(req.linkId, orders, code, status, msg);
  }

  // -- DTOs (fetch-transactions) ---------------------------------------------

  public static final class FetchTransactionsRequest {
    public Long linkId;
    public Integer pageNo;
    public Integer pageSize;
    public Boolean fetchAllTxns;
  }

  public static final class FetchTransactionsResult {
    public final Long linkId;
    public final java.util.List<JsonNode> orders;
    public final String resultCode;
    public final String resultStatus;
    public final String resultMessage;

    public FetchTransactionsResult(Long linkId, java.util.List<JsonNode> orders,
                                   String resultCode, String resultStatus, String resultMessage) {
      this.linkId = linkId;
      this.orders = orders;
      this.resultCode = resultCode;
      this.resultStatus = resultStatus;
      this.resultMessage = resultMessage;
    }
  }

  // -- helpers ---------------------------------------------------------------

  /** linkDescription: alphanumerics + spaces (per Paytm docs). */
  private static String sanitizeDescription(String s, String fallback) {
    if (s == null) return fallback;
    String cleaned = s.replaceAll("[^A-Za-z0-9 ]", " ").replaceAll("\\s+", " ").trim();
    return cleaned.length() >= 3 ? cleaned : fallback;
  }

  /**
   * linkName: alphanumerics ONLY. Paytm's docs say spaces are allowed but
   * several MIDs reject space as a special character with "link name contains
   * special character". Stripping spaces is the safe cross-MID default.
   */
  private static String sanitizeLinkName(String s, String fallback) {
    if (s == null) return fallback;
    String cleaned = s.replaceAll("[^A-Za-z0-9]", "");
    return cleaned.length() >= 3 ? cleaned : fallback;
  }

  private static String oneYearFromNowExpiry() {
    return ZonedDateTime.now(IST).plusYears(1)
        .withHour(23).withMinute(59).withSecond(59)
        .format(EXPIRY_FMT);
  }

  private static boolean notEmpty(String s) {
    return s != null && !s.trim().isEmpty();
  }

  /** Payment Link API takes amount as a JSON number, two-decimal precision. */
  private static double normalizeAmountAsNumber(String amount) {
    BigDecimal v;
    try {
      v = new BigDecimal((amount == null ? "1.00" : amount).trim()).setScale(2, RoundingMode.HALF_UP);
    } catch (Exception e) {
      v = new BigDecimal("1.00");
    }
    if (v.signum() <= 0) v = new BigDecimal("1.00");
    return v.doubleValue();
  }

  private static String randomHex() {
    byte[] rnd = new byte[10];
    RANDOM.nextBytes(rnd);
    StringBuilder hex = new StringBuilder(20);
    for (byte b : rnd) hex.append(String.format("%02X", b));
    return hex.toString();
  }

  private static PaytmUpstreamException upstream(String code, String message, String orderId, String raw) {
    Map<String, Object> paytm = new LinkedHashMap<>();
    try {
      JsonNode info = MAPPER.readTree(raw == null ? "{}" : raw).path("body").path("resultInfo");
      String s = info.path("resultStatus").asText("");
      String c = info.path("resultCode").asText("");
      String m = info.path("resultMsg").asText("");
      if (!s.isEmpty()) paytm.put("resultStatus", s);
      if (!c.isEmpty()) paytm.put("resultCode", c);
      if (!m.isEmpty()) paytm.put("resultMsg", m);
    } catch (Exception ignored) {}
    return new PaytmUpstreamException(HttpStatus.BAD_GATEWAY, code, message, orderId,
        paytm.isEmpty() ? null : paytm);
  }

  // -- DTOs ------------------------------------------------------------------

  public static final class CreateRequest {
    public String amount;
    public String linkName;
    public String linkDescription;
    public String customerName;
    public String customerEmail;
    public String customerMobile;
    public String customerId;
    public String expiryDate;       // DD/MM/YYYY HH:MM:SS
    public String orderId;          // optional
    public Boolean sendSms;
    public Boolean sendEmail;
    public String callbackUrl;
    public String merchantUniqueReference;
  }

  public static final class CreateResult {
    public final String orderId;
    public final long linkId;
    public final String shortUrl;
    public final String longUrl;
    public final String linkStatus;
    public final double amount;
    public final String mid;

    public CreateResult(String orderId, long linkId, String shortUrl, String longUrl,
                        String linkStatus, double amount, String mid) {
      this.orderId = orderId;
      this.linkId = linkId;
      this.shortUrl = shortUrl;
      this.longUrl = longUrl;
      this.linkStatus = linkStatus;
      this.amount = amount;
      this.mid = mid;
    }
  }
}
