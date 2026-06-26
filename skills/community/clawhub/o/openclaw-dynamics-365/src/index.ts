/**
 * openclaw-dynamics-365
 * Microsoft Dynamics 365 CRM integration skill for OpenClaw
 *
 * @example
 * import { Dynamics365Client, exchangeCodeForTokens } from "openclaw-dynamics-365";
 */

export { Dynamics365Client } from "./client.js";
export {
  getAuthorizationUrl,
  exchangeCodeForTokens,
  refreshAccessToken,
  isTokenExpired,
} from "./oauth.js";
export type {
  Dynamics365Config,
  OAuthTokens,
  D365Opportunity,
  D365Lead,
  D365Contact,
  D365Account,
  D365Task,
  UpsertResult,
} from "./types.js";
