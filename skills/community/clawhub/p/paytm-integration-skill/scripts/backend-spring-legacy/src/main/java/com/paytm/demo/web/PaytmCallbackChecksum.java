package com.paytm.demo.web;

import com.paytm.demo.config.PaytmMerchantConfig;
import com.paytm.pg.merchant.PaytmChecksum;
import java.util.TreeMap;
import javax.servlet.http.HttpServletRequest;

/**
 * Validates CHECKSUMHASH on Paytm callback / redirect payloads (form parameters).
 * See "Receive & Validate Callback Response":
 * https://www.paytmpayments.com/docs/jscheckout-verify-payment
 */
public final class PaytmCallbackChecksum {

  private PaytmCallbackChecksum() {
  }

  public static boolean verify(HttpServletRequest request) {
    String checksum = firstParam(request, "CHECKSUMHASH");
    if (checksum == null || checksum.isEmpty()) {
      return false;
    }
    TreeMap<String, String> params = new TreeMap<>();
    request.getParameterMap().forEach((name, values) -> {
      if (values == null || values.length == 0) {
        return;
      }
      if ("CHECKSUMHASH".equalsIgnoreCase(name)) {
        return;
      }
      params.put(name, values[0]);
    });
    try {
      return PaytmChecksum.verifySignature(params, PaytmMerchantConfig.merchantKey(), checksum);
    } catch (Exception e) {
      return false;
    }
  }

  private static String firstParam(HttpServletRequest request, String name) {
    String v = request.getParameter(name);
    if (v != null) {
      return v;
    }
    return request.getParameter(name.toLowerCase());
  }
}
