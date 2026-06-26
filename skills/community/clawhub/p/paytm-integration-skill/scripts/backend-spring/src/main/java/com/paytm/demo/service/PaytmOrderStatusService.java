package com.paytm.demo.service;

import com.paytm.demo.config.PaytmMerchantConfig;
import com.paytm.demo.web.PaytmUpstreamException;
import com.paytm.pg.merchant.PaytmChecksum;
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
 * Transaction Status API per Paytm JS Checkout "Verify Payment Status":
 * https://www.paytmpayments.com/docs/jscheckout-verify-payment
 *
 * <p><strong>Head shape gotcha:</strong> {@code /v3/order/status} accepts
 * {@code head: { signature }} ONLY. Do NOT add {@code tokenType: "AES"} or
 * {@code timestamp} - those belong to {@code /link/*} and {@code /refund/*}
 * APIs, not to Transaction Status. Mixing them in returns checksum-mismatch
 * errors that look like a key problem.
 */
@Service
public class PaytmOrderStatusService {

  private final RestTemplate restTemplate;

  public PaytmOrderStatusService(RestTemplate restTemplate) {
    this.restTemplate = restTemplate;
  }

  public String fetchOrderStatusJson(String orderId) throws Exception {
    JSONObject body = new JSONObject();
    body.put("mid", PaytmMerchantConfig.mid());
    body.put("orderId", orderId);

    String checksum = PaytmChecksum.generateSignature(body.toString(), PaytmMerchantConfig.merchantKey());

    JSONObject head = new JSONObject();
    head.put("signature", checksum);

    JSONObject paytmParams = new JSONObject();
    paytmParams.put("body", body);
    paytmParams.put("head", head);

    HttpHeaders headers = new HttpHeaders();
    headers.setContentType(MediaType.APPLICATION_JSON);
    HttpEntity<String> entity = new HttpEntity<>(paytmParams.toString(), headers);

    try {
      ResponseEntity<String> response =
          restTemplate.postForEntity(PaytmMerchantConfig.transactionStatusApiUrl(), entity, String.class);
      return response.getBody();
    } catch (RestClientResponseException e) {
      // Wrap upstream errors so the controller / global exception handler can
      // return a consistent JSON envelope ({error, code, message, orderId, paytm})
      // - matches the Node + Python service shape.
      throw new PaytmUpstreamException(
          HttpStatus.BAD_GATEWAY,
          "STATUS_HTTP_ERROR",
          "order status HTTP " + e.getRawStatusCode() + " - " + e.getResponseBodyAsString(),
          orderId,
          null);
    }
  }
}
