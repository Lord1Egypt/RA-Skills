package com.paytm.demo.config;

import java.io.InputStream;
import java.net.URLEncoder;
import java.nio.charset.StandardCharsets;
import java.util.Properties;

/**
 * Paytm merchant configuration.
 *
 * Defaults point to Production PG; set PAYTM_PG_DOMAIN or PAYTM_ENVIRONMENT=staging to change.
 * No QA credentials are embedded; MID + merchant key must be provided via env/system properties.
 */
public final class PaytmMerchantConfig {

  private PaytmMerchantConfig() {
  }

  private static final Properties APP_PROPS = loadApplicationProperties();

  private static Properties loadApplicationProperties() {
    Properties p = new Properties();
    try (InputStream in = PaytmMerchantConfig.class.getClassLoader().getResourceAsStream("application.properties")) {
      if (in != null) {
        p.load(in);
      }
    } catch (Exception ignored) {
      // Optional; env vars / system properties can be used instead.
    }
    return p;
  }

  private static String fromProps(String... keys) {
    for (String k : keys) {
      String v = APP_PROPS.getProperty(k);
      if (v != null && !v.trim().isEmpty()) {
        return v.trim();
      }
    }
    return null;
  }

  public static final String CHANNEL_ID = "WEB";

  /**
   * Per-MID websiteName. Override with system property {@code paytm.website.name},
   * env {@code PAYTM_WEBSITE_NAME}, or {@code application.properties}.
   * Defaults mirror {@link #pgDomain()}: "WEBSTAGING" for staging, "DEFAULT" for production.
   */
  public static String websiteName() {
    String fromSys = System.getProperty("paytm.website.name");
    if (fromSys != null && !fromSys.isEmpty()) {
      return fromSys.trim();
    }
    String fromEnv = System.getenv("PAYTM_WEBSITE_NAME");
    if (fromEnv != null && !fromEnv.isEmpty()) {
      return fromEnv.trim();
    }
    String fromProps = fromProps("PAYTM_WEBSITE_NAME", "paytm.website.name");
    if (fromProps != null) {
      return fromProps;
    }
    return isProduction() ? "DEFAULT" : "WEBSTAGING";
  }

  private static boolean isProduction() {
    String env = System.getenv("PAYTM_ENVIRONMENT");
    if (env == null || env.isEmpty()) {
      env = System.getProperty("paytm.environment", "staging");
    }
    return env.trim().equalsIgnoreCase("production");
  }

  /** @deprecated Use {@link #websiteName()}; kept for backwards-compat in legacy services. */
  @Deprecated
  public static final String WEBSITE_NAME = "WEBSTAGING";

  public static final String PROD_PG_DOMAIN = "https://secure.paytmpayments.com";
  public static final String STAGING_PG_DOMAIN = "https://securestage.paytmpayments.com";

  /**
   * Merchant MID.
   * Override with system property {@code paytm.mid} or env {@code PAYTM_MID}.
   */
  public static String mid() {
    String fromSys = System.getProperty("paytm.mid");
    if (fromSys != null && !fromSys.isEmpty()) {
      return fromSys.trim();
    }
    String fromEnv = System.getenv("PAYTM_MID");
    if (fromEnv != null && !fromEnv.isEmpty()) {
      return fromEnv.trim();
    }
    String fromProps = fromProps("PAYTM_MID", "paytm.mid");
    if (fromProps != null) {
      return fromProps;
    }
    throw new IllegalStateException("Missing MID. Set PAYTM_MID or -Dpaytm.mid");
  }

  /**
   * Merchant key (required for checksum generation/verification).
   * Override with system property {@code paytm.merchant.key} or env {@code PAYTM_MERCHANT_KEY}.
   */
  public static String merchantKey() {
    String fromSys = System.getProperty("paytm.merchant.key");
    if (fromSys != null && !fromSys.isEmpty()) {
      return fromSys.trim();
    }
    String fromEnv = System.getenv("PAYTM_MERCHANT_KEY");
    if (fromEnv != null && !fromEnv.isEmpty()) {
      return fromEnv.trim();
    }
    String fromProps = fromProps("PAYTM_MERCHANT_KEY", "paytm.merchant.key");
    if (fromProps != null) {
      return fromProps;
    }
    throw new IllegalStateException("Missing merchant key. Set PAYTM_MERCHANT_KEY or -Dpaytm.merchant.key");
  }

  /**
   * Full callback URL that Paytm will call after payment attempt.
   * Override with system property {@code paytm.callback.url} or env {@code PAYTM_CALLBACK_URL}.
   */
  public static String callbackUrl() {
    return callbackUrl(null);
  }

  /**
   * Per-request override of the callback URL. If {@code requestBaseUrl} is non-null
   * (e.g. derived from the inbound HTTP request), it wins over the static config -
   * matches the Node/Python backends' {@code serverBaseUrl} parameter.
   */
  public static String callbackUrl(String requestBaseUrl) {
    String fromSys = System.getProperty("paytm.callback.url");
    if (fromSys != null && !fromSys.isEmpty()) {
      return fromSys.trim();
    }
    String fromEnv = System.getenv("PAYTM_CALLBACK_URL");
    if (fromEnv != null && !fromEnv.isEmpty()) {
      return fromEnv.trim();
    }
    String fromProps = fromProps("PAYTM_CALLBACK_URL", "paytm.callback.url");
    if (fromProps != null) {
      return fromProps;
    }
    String base = (requestBaseUrl != null && !requestBaseUrl.trim().isEmpty())
        ? trimTrailingSlash(requestBaseUrl) : callbackBaseUrl();
    return base + "/paytm/callback";
  }

  /**
   * PG domain / host for Paytm APIs + CheckoutJS loader.
   * Defaults to Production {@code https://secure.paytmpayments.com}. Override via {@code paytm.pg.domain} /
   * {@code PAYTM_PG_DOMAIN} or set {@code PAYTM_ENVIRONMENT=staging}.
   */
  public static String pgDomain() {
    String fromSys = System.getProperty("paytm.pg.domain");
    if (fromSys != null && !fromSys.isEmpty()) {
      return trimTrailingSlash(fromSys);
    }
    String fromEnv = System.getenv("PAYTM_PG_DOMAIN");
    if (fromEnv != null && !fromEnv.isEmpty()) {
      return trimTrailingSlash(fromEnv);
    }
    String fromProps = fromProps("PAYTM_PG_DOMAIN", "paytm.pg.domain");
    if (fromProps != null) {
      return trimTrailingSlash(fromProps);
    }
    // Defaults to staging unless PAYTM_ENVIRONMENT explicitly set to "production".
    return isProduction() ? PROD_PG_DOMAIN : STAGING_PG_DOMAIN;
  }

  /**
   * CheckoutJS loader URL for the configured MID (QA: {@code pgp-qa12} only).
   *
   * @see <a href="https://www.paytmpayments.com/docs/jscheckout-invoke-payment">Invoke Payment Page</a>
   */
  public static String checkoutJsLoaderUrl() {
    return pgDomain() + "/merchantpgpui/checkoutjs/merchants/"
        + URLEncoder.encode(mid(), StandardCharsets.UTF_8) + ".js";
  }

  /**
   * Subscription create endpoint. Differs between staging (no /theia prefix) and production.
   */
  public static String subscriptionCreateUrl() {
    String base = pgDomain();
    return isProduction() ? base + "/theia/api/v1/subscription/create" : base + "/subscription/create";
  }

  public static String linkCreateUrl() {
    return pgDomain() + "/link/create";
  }

  public static String linkFetchTransactionUrl() {
    return pgDomain() + "/link/fetchTransaction";
  }

  public static String qrCreateUrl() {
    return pgDomain() + "/paymentservices/qr/create";
  }

  /**
   * clientId is per-merchant - issued by Paytm during onboarding. "C11" works for most
   * single-merchant-key setups. Override via env {@code PAYTM_CLIENT_ID} or system property
   * {@code paytm.client.id}.
   */
  public static String clientId() {
    String fromSys = System.getProperty("paytm.client.id");
    if (fromSys != null && !fromSys.isEmpty()) {
      return fromSys.trim();
    }
    String fromEnv = System.getenv("PAYTM_CLIENT_ID");
    if (fromEnv != null && !fromEnv.isEmpty()) {
      return fromEnv.trim();
    }
    String fromProps = fromProps("PAYTM_CLIENT_ID", "paytm.client.id");
    if (fromProps != null) {
      return fromProps;
    }
    return "C11";
  }

  /**
   * Transaction Status API on the same PG host as {@link #pgDomain()} ({@code /v3/order/status}).
   * Override with {@code paytm.status.api.url} or env {@code PAYTM_STATUS_API_URL} for other environments
   * (e.g. {@code https://securestage.paytmpayments.com/v3/order/status} per Paytm docs).
   *
   * @see <a href="https://www.paytmpayments.com/docs/jscheckout-verify-payment">Verify Payment Status</a>
   */
  public static String transactionStatusApiUrl() {
    String fromSys = System.getProperty("paytm.status.api.url");
    if (fromSys != null && !fromSys.isEmpty()) {
      return fromSys.trim();
    }
    String fromEnv = System.getenv("PAYTM_STATUS_API_URL");
    if (fromEnv != null && !fromEnv.isEmpty()) {
      return fromEnv.trim();
    }
    return pgDomain() + "/v3/order/status";
  }

  /**
   * Public base URL of this WAR (no trailing slash), used in callbackUrl.
   * Override with system property {@code paytm.callback.base} or env {@code PAYTM_CALLBACK_BASE}.
   */
  public static String callbackBaseUrl() {
    String fromSys = System.getProperty("paytm.callback.base");
    if (fromSys != null && !fromSys.isEmpty()) {
      return trimTrailingSlash(fromSys);
    }
    String fromEnv = System.getenv("PAYTM_CALLBACK_BASE");
    if (fromEnv != null && !fromEnv.isEmpty()) {
      return trimTrailingSlash(fromEnv);
    }
    return "http://localhost:8080/paytm-backend";
  }

  private static String trimTrailingSlash(String u) {
    if (u.endsWith("/")) {
      return u.substring(0, u.length() - 1);
    }
    return u;
  }
}
