package com.paytm.demo.service;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.paytm.demo.config.PaytmMerchantConfig;
import com.paytm.demo.web.PaytmUpstreamException;
import com.paytm.pg.merchant.PaytmChecksum;
import java.math.BigDecimal;
import java.math.RoundingMode;
import java.security.SecureRandom;
import java.time.LocalDate;
import java.time.ZoneId;
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
import org.springframework.web.util.UriComponentsBuilder;

/**
 * Native Create Subscription - POST /subscription/create.
 *
 * Doc: https://www.paytmpayments.com/docs/api/initiate-subscription-api
 *
 * Defaults baked in (matching Node + Python):
 *  - subscriptionPaymentMode: "UNKNOWN"  (Paytm renders all enabled rails)
 *  - txnAmount.value: ">= 2.00"          (CC/DC mandates require > Rs.1)
 *  - subscriptionGraceDays: "3"          (CC/DC max)
 *  - subscriptionStartDate: today (IST)
 *  - subscriptionEnableRetry: "0"        (retry off; subscriptionRetryCount omitted)
 */
@Service
public class PaytmSubscriptionService {

  private static final ObjectMapper MAPPER = new ObjectMapper();
  private static final SecureRandom RANDOM = new SecureRandom();
  private static final ZoneId IST = ZoneId.of("Asia/Kolkata");
  private static final DateTimeFormatter ISO = DateTimeFormatter.ofPattern("yyyy-MM-dd");

  private final RestTemplate restTemplate;

  public PaytmSubscriptionService(RestTemplate restTemplate) {
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
        ? req.orderId.trim() : "SUB_" + randomHex();
    String traceId = "TRC_" + randomHex();
    String start = (req.startDate != null && !req.startDate.trim().isEmpty())
        ? req.startDate.trim() : LocalDate.now(IST).format(ISO);
    String expiry = (req.expiryDate != null && !req.expiryDate.trim().isEmpty())
        ? req.expiryDate.trim() : LocalDate.parse(start, ISO).plusYears(1).format(ISO);
    String amountType = (req.amountType != null && !req.amountType.isEmpty()) ? req.amountType : "FIX";
    String paymentMode = (req.paymentMode != null && !req.paymentMode.isEmpty()) ? req.paymentMode : "UNKNOWN";

    JSONObject userInfo = new JSONObject();
    userInfo.put("custId", sanitizeCustId(req.custId));
    if (notEmpty(req.mobile)) userInfo.put("mobile", req.mobile.trim());
    if (notEmpty(req.email)) userInfo.put("email", req.email.trim());
    if (notEmpty(req.firstName)) userInfo.put("firstName", req.firstName.trim());
    if (notEmpty(req.lastName)) userInfo.put("lastName", req.lastName.trim());

    JSONObject txnAmount = new JSONObject();
    txnAmount.put("value", normalizeAmount(req.amount, new BigDecimal("2.00")));
    txnAmount.put("currency", "INR");

    JSONObject body = new JSONObject();
    body.put("requestType", "NATIVE_SUBSCRIPTION");
    body.put("mid", PaytmMerchantConfig.mid());
    body.put("orderId", orderId);
    body.put("websiteName", PaytmMerchantConfig.websiteName());
    body.put("txnAmount", txnAmount);
    body.put("subscriptionPaymentMode", paymentMode);
    body.put("subscriptionAmountType", amountType);
    body.put("subscriptionFrequency", req.frequency != null ? req.frequency : "1");
    body.put("subscriptionFrequencyUnit", req.frequencyUnit != null ? req.frequencyUnit : "MONTH");
    body.put("subscriptionStartDate", start);
    body.put("subscriptionExpiryDate", expiry);
    body.put("subscriptionGraceDays", req.graceDays != null ? req.graceDays : "3");
    body.put("subscriptionEnableRetry", "0");
    body.put("userInfo", userInfo);
    body.put("callbackUrl", PaytmMerchantConfig.callbackUrl(requestBaseUrl));

    if ("VARIABLE".equals(amountType)) {
      if (req.maxAmount == null) {
        throw new IllegalArgumentException("subscriptionMaxAmount required for VARIABLE amount type");
      }
      body.put("subscriptionMaxAmount", normalizeAmount(req.maxAmount, BigDecimal.ZERO));
    } else if (req.maxAmount != null) {
      body.put("subscriptionMaxAmount", normalizeAmount(req.maxAmount, BigDecimal.ZERO));
    }
    if (notEmpty(req.renewalAmount)) {
      body.put("renewalAmount", normalizeAmount(req.renewalAmount, BigDecimal.ZERO));
    }
    if ("BANK_MANDATE".equals(paymentMode)) {
      body.put("mandateType", req.mandateType != null ? req.mandateType : "E_MANDATE");
    }


    String checksum = PaytmChecksum.generateSignature(body.toString(), PaytmMerchantConfig.merchantKey());
    JSONObject head = new JSONObject();
    head.put("clientId", PaytmMerchantConfig.clientId());
    head.put("channelId", "WEB");
    head.put("version", "v1");
    head.put("requestTimestamp", String.valueOf(System.currentTimeMillis()));
    head.put("signature", checksum);

    JSONObject paytmParams = new JSONObject();
    paytmParams.put("body", body);
    paytmParams.put("head", head);

    String url = UriComponentsBuilder.fromHttpUrl(PaytmMerchantConfig.subscriptionCreateUrl())
        .queryParam("mid", PaytmMerchantConfig.mid())
        .queryParam("orderId", orderId)
        .queryParam("traceId", traceId)
        .toUriString();

    HttpHeaders headers = new HttpHeaders();
    headers.setContentType(MediaType.APPLICATION_JSON);
    HttpEntity<String> entity = new HttpEntity<>(paytmParams.toString(), headers);

    ResponseEntity<String> response;
    String responseBody;
    try {
      response = restTemplate.postForEntity(url, entity, String.class);
      responseBody = response.getBody();
    } catch (RestClientResponseException e) {
      throw upstream("SUBSCRIPTION_HTTP_ERROR",
          "subscription/create failed (HTTP " + e.getRawStatusCode() + ")",
          orderId, e.getResponseBodyAsString());
    }

    JsonNode root = MAPPER.readTree(responseBody);
    JsonNode info = root.path("body").path("resultInfo");
    if (!"S".equals(info.path("resultStatus").asText(""))) {
      throw upstream("SUBSCRIPTION_FAILED",
          info.path("resultMsg").asText("subscription/create failed"),
          orderId, responseBody);
    }
    String txnToken = root.path("body").path("txnToken").asText(null);
    String subscriptionId = root.path("body").path("subscriptionId").asText(null);
    return new CreateResult(orderId, traceId, txnToken, subscriptionId,
        body.getJSONObject("txnAmount").getString("value"),
        PaytmMerchantConfig.mid());
  }

  // -- helpers ---------------------------------------------------------------

  private static String sanitizeCustId(String s) {
    if (s == null || s.isEmpty()) return "CUST_DEMO";
    return s.replaceAll("[^a-zA-Z0-9_]", "_");
  }

  private static boolean notEmpty(String s) {
    return s != null && !s.trim().isEmpty();
  }

  private static String normalizeAmount(String amount, BigDecimal floor) {
    BigDecimal v;
    try {
      v = new BigDecimal(amount.trim()).setScale(2, RoundingMode.HALF_UP);
    } catch (Exception e) {
      v = floor;
    }
    if (v.compareTo(floor) < 0) v = floor;
    if (v.signum() <= 0) v = floor;
    return v.toPlainString();
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
    public String amount;          // first-debit amount; >= 2.00 for cross-rail safety
    public String renewalAmount;   // optional
    public String custId;
    public String mobile;
    public String email;
    public String firstName;
    public String lastName;
    public String frequency;       // default "1"
    public String frequencyUnit;   // default "MONTH"
    public String amountType;      // FIX | VARIABLE
    public String maxAmount;       // required when VARIABLE
    public String startDate;       // YYYY-MM-DD; defaults to today (IST)
    public String expiryDate;      // YYYY-MM-DD; defaults to start + 1y
    public String graceDays;       // default "3"
    public String paymentMode;     // CC | DC | BANK_MANDATE | UNKNOWN (default)
    public String mandateType;     // E_MANDATE | PAPER_MANDATE - only with BANK_MANDATE
    public String orderId;         // optional caller-supplied
  }

  public static final class CreateResult {
    public final String orderId;
    public final String traceId;
    public final String txnToken;
    public final String subscriptionId;
    public final String amount;
    public final String mid;

    public CreateResult(String orderId, String traceId, String txnToken,
                        String subscriptionId, String amount, String mid) {
      this.orderId = orderId;
      this.traceId = traceId;
      this.txnToken = txnToken;
      this.subscriptionId = subscriptionId;
      this.amount = amount;
      this.mid = mid;
    }
  }
}
