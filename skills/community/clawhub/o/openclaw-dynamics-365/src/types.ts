/**
 * openclaw-dynamics-365
 * TypeScript types for Microsoft Dynamics 365 Dataverse Web API
 */

/** Credentials for an Azure AD App Registration (multi-tenant recommended) */
export interface Dynamics365Config {
  /** Azure AD Application (client) ID */
  clientId: string;
  /** Azure AD Client Secret */
  clientSecret: string;
  /**
   * Azure AD Tenant ID.
   * Use "common" for multi-tenant apps (recommended),
   * or a specific tenant GUID for single-tenant.
   */
  tenantId: string;
  /**
   * Dynamics 365 instance URL.
   * Format: https://{org}.crm.dynamics.com
   * e.g.  https://contoso.crm.dynamics.com
   */
  instanceUrl: string;
}

/** OAuth 2.0 tokens returned after authorization */
export interface OAuthTokens {
  accessToken: string;
  refreshToken: string;
  /** Unix timestamp (ms) when the access token expires */
  expiresAt: number;
  /** Dynamics 365 instance URL associated with these tokens */
  instanceUrl: string;
}

// ─── Dataverse Entity Types ──────────────────────────────────────────────────

/**
 * Dynamics 365 Opportunity
 * Entity set: /opportunities
 */
export interface D365Opportunity {
  /** Existing record ID — set to trigger PATCH instead of POST */
  opportunityid?: string;
  /** Opportunity name (required) */
  name: string;
  /** Estimated revenue in base currency */
  estimatedvalue?: number;
  /**
   * Sales stage / pipeline step name.
   * Common values: "Qualify", "Develop", "Propose", "Close"
   */
  stepname?: string;
  /** Expected close date (ISO 8601: YYYY-MM-DD) */
  actualclosedate?: string;
  /** Notes / description */
  description?: string;
  /**
   * Link to a parent Account via OData binding.
   * Format: /accounts({accountid})
   */
  "parentaccountid@odata.bind"?: string;
}

/**
 * Dynamics 365 Lead
 * Entity set: /leads
 */
export interface D365Lead {
  /** Existing record ID */
  leadid?: string;
  /** Full name (auto-populated from first + last name if not set) */
  fullname?: string;
  firstName?: string;
  lastName?: string;
  /** Primary email address */
  emailaddress1?: string;
  /** Job title */
  jobtitle?: string;
  /** Company name */
  companyname?: string;
  /** Primary phone number */
  telephone1?: string;
  /** Notes / description */
  description?: string;
}

/**
 * Dynamics 365 Contact
 * Entity set: /contacts
 */
export interface D365Contact {
  /** Existing record ID */
  contactid?: string;
  fullname?: string;
  firstName?: string;
  lastName?: string;
  emailaddress1?: string;
  jobtitle?: string;
  telephone1?: string;
  description?: string;
  /**
   * Link to parent Account via OData binding.
   * Format: /accounts({accountid})
   */
  "parentcustomerid_account@odata.bind"?: string;
}

/**
 * Dynamics 365 Account
 * Entity set: /accounts
 */
export interface D365Account {
  /** Existing record ID */
  accountid?: string;
  /** Account / company name (required) */
  name: string;
  emailaddress1?: string;
  telephone1?: string;
  websiteurl?: string;
  description?: string;
}

/**
 * Dynamics 365 Task (Activity)
 * Entity set: /tasks
 */
export interface D365Task {
  /** Existing record ID */
  activityid?: string;
  /** Task subject / title (required) */
  subject: string;
  description?: string;
  /** Due date-time (ISO 8601) */
  scheduledend?: string;
  /**
   * Priority:
   * 0 = Low | 1 = Normal (default) | 2 = High
   */
  prioritycode?: 0 | 1 | 2;
  /** Link to related Opportunity */
  "regardingobjectid_opportunity_task@odata.bind"?: string;
  /** Link to related Contact */
  "regardingobjectid_contact_task@odata.bind"?: string;
  /** Link to related Account */
  "regardingobjectid_account_task@odata.bind"?: string;
}

/** Result returned by upsert operations */
export interface UpsertResult {
  /** Record GUID in Dataverse */
  id: string;
  /** true = record was created; false = existing record was updated */
  created: boolean;
}
