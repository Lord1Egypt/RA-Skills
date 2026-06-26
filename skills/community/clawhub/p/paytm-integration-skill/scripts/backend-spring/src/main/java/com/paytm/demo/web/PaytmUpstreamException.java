package com.paytm.demo.web;

import java.util.Map;
import org.springframework.http.HttpStatus;

public class PaytmUpstreamException extends RuntimeException {
  public final HttpStatus httpStatus;
  public final String code;
  public final String orderId;
  public final Map<String, Object> paytm;

  public PaytmUpstreamException(HttpStatus httpStatus, String code, String message, String orderId, Map<String, Object> paytm) {
    super(message);
    this.httpStatus = httpStatus;
    this.code = code;
    this.orderId = orderId;
    this.paytm = paytm;
  }
}

