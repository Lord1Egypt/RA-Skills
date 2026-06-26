package com.paytm.demo.service;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.paytm.demo.config.PaytmMerchantConfig;
import com.paytm.demo.web.PaytmUpstreamException;
import com.paytm.pg.merchant.PaytmChecksum;
import java.math.BigDecimal;
import java.math.RoundingMode;
import java.security.SecureRandom;
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
 * Create Dynamic QR - POST /paymentservices/qr/create.
 *
 * Doc: https://www.paytmpayments.com/docs/api/create-qr-code-api
 *
 * Defaults & gotchas baked in (matching Node + Python):
 *  - posId is REQUIRED (Paytm returns 400 without it)
 *  - amount must be a STRING with two decimals
 *  - head requires clientId + version + signature
 *  - Response `image` is RAW base64 - we prepend `data:image/png;base64,` here so
 *    the frontend can drop it straight into <img src>.
 */
@Service
public class PaytmDynamicQrService {

  private static final ObjectMapper MAPPER = new ObjectMapper();
  private static final SecureRandom RANDOM = new SecureRandom();

  private final RestTemplate restTemplate;

  public PaytmDynamicQrService(RestTemplate restTemplate) {
    this.restTemplate = restTemplate;
  }

  public CreateResult create(CreateRequest req) throws Exception {
    if (req.posId == null || req.posId.trim().isEmpty()) {
      throw new IllegalArgumentException(
          "posId is required for QR creation (Paytm returns 400 without it)");
    }
    String orderId = (req.orderId != null && !req.orderId.trim().isEmpty())
        ? req.orderId.trim() : "QR_" + randomHex();

    JSONObject body = new JSONObject();
    body.put("mid", PaytmMerchantConfig.mid());
    body.put("orderId", orderId);
    body.put("amount", normalizeAmount(req.amount));
    body.put("businessType", "UPI_QR_CODE");
    body.put("posId", req.posId.trim());
    body.put("imageRequired", req.imageRequired == null ? Boolean.TRUE : req.imageRequired);
    if (req.displayName != null && !req.displayName.trim().isEmpty()) {
      String trimmed = req.displayName.trim();
      body.put("displayName", trimmed.length() > 30 ? trimmed.substring(0, 30) : trimmed);
    }
    if (req.expiryDate != null && !req.expiryDate.trim().isEmpty()) {
      body.put("expiryDate", req.expiryDate.trim());
    }

    String checksum = PaytmChecksum.generateSignature(body.toString(), PaytmMerchantConfig.merchantKey());
    JSONObject head = new JSONObject();
    head.put("clientId", PaytmMerchantConfig.clientId());
    head.put("version", "v1");
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
          PaytmMerchantConfig.qrCreateUrl(), entity, String.class);
      responseBody = response.getBody();
    } catch (RestClientResponseException e) {
      throw upstream("QR_HTTP_ERROR",
          "qr/create failed (HTTP " + e.getRawStatusCode() + ")",
          orderId, e.getResponseBodyAsString());
    }

    JsonNode root = MAPPER.readTree(responseBody);
    JsonNode info = root.path("body").path("resultInfo");
    String status = info.path("resultStatus").asText("");
    if (!status.isEmpty() && !"SUCCESS".equals(status) && !"S".equals(status)) {
      throw upstream("QR_FAILED",
          info.path("resultMsg").asText("qr/create failed"), orderId, responseBody);
    }

    JsonNode bodyResp = root.path("body");
    String rawImage = bodyResp.path("image").asText(null);
    String image = (rawImage != null && !rawImage.isEmpty())
        ? "data:image/png;base64," + rawImage : null;

    return new CreateResult(
        orderId,
        bodyResp.path("qrCodeId").asText(null),
        bodyResp.path("qrData").asText(null),
        image,
        PaytmMerchantConfig.mid());
  }

  // -- helpers ---------------------------------------------------------------

  private static String normalizeAmount(String amount) {
    BigDecimal v;
    try {
      v = new BigDecimal((amount == null ? "1.00" : amount).trim()).setScale(2, RoundingMode.HALF_UP);
    } catch (Exception e) {
      v = new BigDecimal("1.00");
    }
    if (v.signum() <= 0) v = new BigDecimal("1.00");
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
    public String amount;
    public String posId;          // REQUIRED - Paytm 400s without it
    public String displayName;
    public String expiryDate;
    public Boolean imageRequired;
    public String orderId;        // optional
  }

  public static final class CreateResult {
    public final String orderId;
    public final String qrCodeId;
    public final String qrData;
    public final String image;     // already wrapped with `data:image/png;base64,` prefix
    public final String mid;

    public CreateResult(String orderId, String qrCodeId, String qrData, String image, String mid) {
      this.orderId = orderId;
      this.qrCodeId = qrCodeId;
      this.qrData = qrData;
      this.image = image;
      this.mid = mid;
    }
  }
}
