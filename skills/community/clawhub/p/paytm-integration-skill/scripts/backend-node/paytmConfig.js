export function getPaytmConfig() {
  const PROD_PG_DOMAIN = "https://secure.paytmpayments.com";
  const STAGING_PG_DOMAIN = "https://securestage.paytmpayments.com";
  // Defaults to "staging" so a fresh clone never accidentally points at production.
  const env = (process.env.PAYTM_ENVIRONMENT?.trim() || "staging").toLowerCase();
  const defaultPg = env === "production" ? PROD_PG_DOMAIN : STAGING_PG_DOMAIN;
  const pgDomain = (process.env.PAYTM_PG_DOMAIN?.trim() || defaultPg).replace(/\/+$/, "");

  const mid = process.env.PAYTM_MID?.trim() || "";
  const merchantKey = process.env.PAYTM_MERCHANT_KEY?.trim() || "";
  // Default mirrors PAYTM_ENVIRONMENT - "WEBSTAGING" for staging, "DEFAULT" for prod.
  const websiteName = process.env.PAYTM_WEBSITE_NAME?.trim()
    || (env === "production" ? "DEFAULT" : "WEBSTAGING");
  const callbackBase = (process.env.PAYTM_CALLBACK_BASE?.trim() || "http://localhost:3001").replace(/\/+$/, "");
  // '' unless PAYTM_CALLBACK_URL; actual callback URL = serverBaseUrl + /paytm/callback in paytmService (see create-order)
  const callbackUrl = process.env.PAYTM_CALLBACK_URL?.trim() || "";

  return {
    pgDomain,
    mid,
    merchantKey,
    websiteName,
    callbackBase,
    callbackUrl, // auto-set from serverBaseUrl at runtime when still ''
    initiateTransactionUrl: `${pgDomain}/theia/api/v1/initiateTransaction`,
    orderStatusUrl: process.env.PAYTM_STATUS_API_URL?.trim() || `${pgDomain}/v3/order/status`,
    // Subscription endpoints differ between staging (no /theia prefix) and production.
    subscriptionCreateUrl: env === "production"
      ? `${pgDomain}/theia/api/v1/subscription/create`
      : `${pgDomain}/subscription/create`,
    linkCreateUrl: `${pgDomain}/link/create`,
    linkFetchTransactionUrl: `${pgDomain}/link/fetchTransaction`,
    qrCreateUrl: `${pgDomain}/paymentservices/qr/create`,
    // clientId is per-merchant - issued by Paytm during onboarding. "C11" works for
    // most single-merchant-key setups; override via env if your KAM gave you a different value.
    clientId: process.env.PAYTM_CLIENT_ID?.trim() || "C11",
    checkoutJsLoaderUrl: mid
      ? `${pgDomain}/merchantpgpui/checkoutjs/merchants/${encodeURIComponent(mid)}.js`
      : "",
  };
}
