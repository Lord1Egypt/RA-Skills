/**
 * openclaw-dynamics-365 — Dataverse Web API Client
 *
 * Implements CRUD operations for the five core CRM entities:
 * Opportunity, Lead, Contact, Account, Task
 *
 * API reference: https://learn.microsoft.com/en-us/power-apps/developer/data-platform/webapi/overview
 * API version: v9.2 (latest stable as of 2026)
 *
 * HTTP behaviour per official docs:
 *  POST   → 204 No Content  | record ID in `OData-EntityId` response header
 *  PATCH  → 204 No Content  | no body; requires `If-Match: *` to prevent accidental upsert
 *  GET    → 200 OK          | body: { value: T[] }  (empty: { value: [] })
 */

import type {
  D365Account,
  D365Contact,
  D365Lead,
  D365Opportunity,
  D365Task,
  UpsertResult,
} from "./types.js";

const API_VERSION = "v9.2";

export class Dynamics365Client {
  private readonly baseUrl: string;
  private readonly headers: Record<string, string>;

  /**
   * @param instanceUrl  e.g. https://contoso.crm.dynamics.com
   * @param accessToken  Bearer token from Azure AD OAuth flow
   */
  constructor(instanceUrl: string, accessToken: string) {
    const origin = instanceUrl.replace(/\/$/, "");
    this.baseUrl = `${origin}/api/data/${API_VERSION}`;
    this.headers = {
      Authorization: `Bearer ${accessToken}`,
      "Content-Type": "application/json",
      Accept: "application/json",
      "OData-MaxVersion": "4.0",
      "OData-Version": "4.0",
    };
  }

  // ─── Opportunities ──────────────────────────────────────────────────────────

  /**
   * Find an Opportunity by exact name match.
   *
   * GET /opportunities?$select=opportunityid&$filter=name eq 'X'&$top=1
   * Response: 200 OK — { value: [{ opportunityid: "guid" }] } or { value: [] }
   */
  async searchOpportunity(name: string): Promise<string | null> {
    const filter = `name eq '${escapeSingleQuotes(name)}'`;
    const resp = await fetch(
      `${this.baseUrl}/opportunities?$select=opportunityid&$filter=${encodeURIComponent(filter)}&$top=1`,
      { headers: this.headers },
    );
    if (!resp.ok) return null;
    const data = (await resp.json()) as { value: Array<{ opportunityid: string }> };
    return data.value[0]?.opportunityid ?? null;
  }

  /**
   * Create or update an Opportunity.
   *
   * Create → POST /opportunities
   *   Response: 204 No Content
   *   ID extracted from OData-EntityId header: .../opportunities(guid)
   *
   * Update → PATCH /opportunities({id})
   *   Response: 204 No Content
   *   If-Match: * prevents accidental creation via upsert
   */
  async upsertOpportunity(payload: D365Opportunity): Promise<UpsertResult> {
    const existingId =
      payload.opportunityid ?? (await this.searchOpportunity(payload.name));

    const { opportunityid: _id, ...fields } = payload;

    if (existingId) {
      const resp = await fetch(
        `${this.baseUrl}/opportunities(${existingId})`,
        {
          method: "PATCH",
          headers: { ...this.headers, "If-Match": "*" },
          body: JSON.stringify(fields),
        },
      );
      if (!resp.ok) {
        throw new Error(`Opportunity PATCH failed: ${resp.status} ${await resp.text()}`);
      }
      return { id: existingId, created: false };
    }

    const resp = await fetch(`${this.baseUrl}/opportunities`, {
      method: "POST",
      headers: this.headers,
      body: JSON.stringify(fields),
    });
    if (!resp.ok) {
      throw new Error(`Opportunity POST failed: ${resp.status} ${await resp.text()}`);
    }
    return { id: extractGuid(resp.headers.get("OData-EntityId") ?? ""), created: true };
  }

  // ─── Leads ──────────────────────────────────────────────────────────────────

  /**
   * Find a Lead by full name or primary email address.
   *
   * GET /leads?$select=leadid&$filter=fullname eq 'X' or emailaddress1 eq 'X'&$top=1
   * Response: 200 OK — { value: [{ leadid: "guid" }] } or { value: [] }
   */
  async searchLead(query: string): Promise<string | null> {
    const escaped = escapeSingleQuotes(query);
    const filter = `fullname eq '${escaped}' or emailaddress1 eq '${escaped}'`;
    const resp = await fetch(
      `${this.baseUrl}/leads?$select=leadid&$filter=${encodeURIComponent(filter)}&$top=1`,
      { headers: this.headers },
    );
    if (!resp.ok) return null;
    const data = (await resp.json()) as { value: Array<{ leadid: string }> };
    return data.value[0]?.leadid ?? null;
  }

  /**
   * Create or update a Lead.
   * Searches by email (preferred) or full name before creating.
   */
  async upsertLead(payload: D365Lead): Promise<UpsertResult> {
    const searchKey = payload.emailaddress1 ?? payload.fullname ?? "";
    const existingId =
      payload.leadid ?? (searchKey ? await this.searchLead(searchKey) : null);

    const { leadid: _id, ...fields } = payload;

    if (existingId) {
      const resp = await fetch(`${this.baseUrl}/leads(${existingId})`, {
        method: "PATCH",
        headers: { ...this.headers, "If-Match": "*" },
        body: JSON.stringify(fields),
      });
      if (!resp.ok) {
        throw new Error(`Lead PATCH failed: ${resp.status} ${await resp.text()}`);
      }
      return { id: existingId, created: false };
    }

    const resp = await fetch(`${this.baseUrl}/leads`, {
      method: "POST",
      headers: this.headers,
      body: JSON.stringify(fields),
    });
    if (!resp.ok) {
      throw new Error(`Lead POST failed: ${resp.status} ${await resp.text()}`);
    }
    return { id: extractGuid(resp.headers.get("OData-EntityId") ?? ""), created: true };
  }

  // ─── Contacts ───────────────────────────────────────────────────────────────

  /**
   * Find a Contact by full name or primary email address.
   *
   * GET /contacts?$select=contactid&$filter=fullname eq 'X' or emailaddress1 eq 'X'&$top=1
   */
  async searchContact(query: string): Promise<string | null> {
    const escaped = escapeSingleQuotes(query);
    const filter = `fullname eq '${escaped}' or emailaddress1 eq '${escaped}'`;
    const resp = await fetch(
      `${this.baseUrl}/contacts?$select=contactid&$filter=${encodeURIComponent(filter)}&$top=1`,
      { headers: this.headers },
    );
    if (!resp.ok) return null;
    const data = (await resp.json()) as { value: Array<{ contactid: string }> };
    return data.value[0]?.contactid ?? null;
  }

  /** Create or update a Contact. */
  async upsertContact(payload: D365Contact): Promise<UpsertResult> {
    const searchKey = payload.emailaddress1 ?? payload.fullname ?? "";
    const existingId =
      payload.contactid ??
      (searchKey ? await this.searchContact(searchKey) : null);

    const { contactid: _id, ...fields } = payload;

    if (existingId) {
      const resp = await fetch(`${this.baseUrl}/contacts(${existingId})`, {
        method: "PATCH",
        headers: { ...this.headers, "If-Match": "*" },
        body: JSON.stringify(fields),
      });
      if (!resp.ok) {
        throw new Error(`Contact PATCH failed: ${resp.status} ${await resp.text()}`);
      }
      return { id: existingId, created: false };
    }

    const resp = await fetch(`${this.baseUrl}/contacts`, {
      method: "POST",
      headers: this.headers,
      body: JSON.stringify(fields),
    });
    if (!resp.ok) {
      throw new Error(`Contact POST failed: ${resp.status} ${await resp.text()}`);
    }
    return { id: extractGuid(resp.headers.get("OData-EntityId") ?? ""), created: true };
  }

  // ─── Accounts ───────────────────────────────────────────────────────────────

  /**
   * Find an Account by exact name match.
   *
   * GET /accounts?$select=accountid&$filter=name eq 'X'&$top=1
   */
  async searchAccount(name: string): Promise<string | null> {
    const filter = `name eq '${escapeSingleQuotes(name)}'`;
    const resp = await fetch(
      `${this.baseUrl}/accounts?$select=accountid&$filter=${encodeURIComponent(filter)}&$top=1`,
      { headers: this.headers },
    );
    if (!resp.ok) return null;
    const data = (await resp.json()) as { value: Array<{ accountid: string }> };
    return data.value[0]?.accountid ?? null;
  }

  /** Create or update an Account. */
  async upsertAccount(payload: D365Account): Promise<UpsertResult> {
    const existingId =
      payload.accountid ?? (await this.searchAccount(payload.name));

    const { accountid: _id, ...fields } = payload;

    if (existingId) {
      const resp = await fetch(`${this.baseUrl}/accounts(${existingId})`, {
        method: "PATCH",
        headers: { ...this.headers, "If-Match": "*" },
        body: JSON.stringify(fields),
      });
      if (!resp.ok) {
        throw new Error(`Account PATCH failed: ${resp.status} ${await resp.text()}`);
      }
      return { id: existingId, created: false };
    }

    const resp = await fetch(`${this.baseUrl}/accounts`, {
      method: "POST",
      headers: this.headers,
      body: JSON.stringify(fields),
    });
    if (!resp.ok) {
      throw new Error(`Account POST failed: ${resp.status} ${await resp.text()}`);
    }
    return { id: extractGuid(resp.headers.get("OData-EntityId") ?? ""), created: true };
  }

  // ─── Tasks ────────────────────────────────────────────────────────────────

  /**
   * Create a Task (Activity) record.
   *
   * POST /tasks
   * Response: 204 No Content — ID in OData-EntityId header
   *
   * Link to related records via odata.bind fields:
   *   "regardingobjectid_opportunity_task@odata.bind": "/opportunities(guid)"
   */
  async createTask(payload: D365Task): Promise<string> {
    const { activityid: _id, ...fields } = payload;
    const resp = await fetch(`${this.baseUrl}/tasks`, {
      method: "POST",
      headers: this.headers,
      body: JSON.stringify(fields),
    });
    if (!resp.ok) {
      throw new Error(`Task POST failed: ${resp.status} ${await resp.text()}`);
    }
    return extractGuid(resp.headers.get("OData-EntityId") ?? "");
  }

  // ─── Static utilities ────────────────────────────────────────────────────────

  /**
   * Build a deep link URL to open a Dynamics 365 record in the browser.
   *
   * @param instanceUrl   e.g. https://contoso.crm.dynamics.com
   * @param entityName    Singular entity logical name
   * @param id            Record GUID
   */
  static recordUrl(
    instanceUrl: string,
    entityName: "opportunity" | "lead" | "contact" | "account" | "task",
    id: string,
  ): string {
    const origin = instanceUrl.replace(/\/$/, "");
    return `${origin}/main.aspx?etn=${entityName}&id=${id}&pagetype=entityrecord`;
  }

  /**
   * Build an OData binding reference string for lookup fields.
   *
   * @example
   * Dynamics365Client.bindRef("accounts", accountId)
   * // → "/accounts(abc-123-...)"
   */
  static bindRef(entitySetName: string, id: string): string {
    return `/${entitySetName}(${id})`;
  }
}

// ─── Internal helpers ────────────────────────────────────────────────────────

/**
 * Escape single quotes for OData $filter strings.
 * OData spec: represent a single quote within a string by doubling it.
 * Docs: https://docs.oasis-open.org/odata/odata/v4.0/odata-v4.0-part2-url-conventions.html
 */
function escapeSingleQuotes(value: string): string {
  return value.replace(/'/g, "''");
}

/**
 * Extract GUID from an OData-EntityId header value.
 *
 * Header format: https://org.crm.dynamics.com/api/data/v9.2/accounts(guid)
 * Docs: https://learn.microsoft.com/en-us/power-apps/developer/data-platform/webapi/create-entity-web-api
 */
function extractGuid(entityIdHeader: string): string {
  const match = entityIdHeader.match(/\(([^)]+)\)$/);
  return match?.[1] ?? "";
}
