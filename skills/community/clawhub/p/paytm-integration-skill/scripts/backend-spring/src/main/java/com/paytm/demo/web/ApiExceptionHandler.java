package com.paytm.demo.web;

import java.util.LinkedHashMap;
import java.util.Map;
import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.RestControllerAdvice;

@RestControllerAdvice
public class ApiExceptionHandler {

  @ExceptionHandler(IllegalArgumentException.class)
  public ResponseEntity<Map<String, Object>> badRequest(IllegalArgumentException e) {
    return jsonError(HttpStatus.BAD_REQUEST, "BAD_REQUEST", e.getMessage());
  }

  @ExceptionHandler(PaytmUpstreamException.class)
  public ResponseEntity<Map<String, Object>> upstream(PaytmUpstreamException e) {
    Map<String, Object> out = new LinkedHashMap<>();
    out.put("error", true);
    out.put("code", e.code);
    out.put("message", e.getMessage());
    out.put("orderId", e.orderId);
    if (e.paytm != null && !e.paytm.isEmpty()) {
      out.put("paytm", e.paytm);
    }
    return ResponseEntity.status(e.httpStatus).contentType(MediaType.APPLICATION_JSON).body(out);
  }

  @ExceptionHandler(Exception.class)
  public ResponseEntity<Map<String, Object>> internal(Exception e) {
    // Do not leak stack traces to clients. Log server-side if needed.
    return jsonError(HttpStatus.INTERNAL_SERVER_ERROR, "INTERNAL_ERROR",
        "Something went wrong while processing the request. Please retry or check server logs.");
  }

  private static ResponseEntity<Map<String, Object>> jsonError(HttpStatus status, String code, String message) {
    Map<String, Object> out = new LinkedHashMap<>();
    out.put("error", true);
    out.put("code", code);
    out.put("message", message);
    return ResponseEntity.status(status).contentType(MediaType.APPLICATION_JSON).body(out);
  }
}

