package com.paytm.demo.web;

import com.paytm.demo.config.PaytmMerchantConfig;
import java.util.LinkedHashMap;
import java.util.Map;
import org.springframework.http.MediaType;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

/**
 * Public JSON for the browser (MID + loader URL only - never merchant key).
 * Path: {@code /paytm-client-config.json} at WAR root.
 */
@RestController
public class PaytmClientConfigController {

  @GetMapping(value = "/paytm-client-config.json", produces = MediaType.APPLICATION_JSON_VALUE)
  public Map<String, Object> clientConfig() {
    Map<String, Object> m = new LinkedHashMap<>();
    m.put("environment", "qa");
    m.put("api_host", PaytmMerchantConfig.pgDomain());
    m.put("initiate_path", "/theia/api/v1/initiateTransaction");
    m.put("loader_host", PaytmMerchantConfig.pgDomain());
    m.put("mid", PaytmMerchantConfig.mid());
    m.put("loader_url", PaytmMerchantConfig.checkoutJsLoaderUrl());
    m.put("create_order_relative", "/paytm/create-order");
    return m;
  }
}
