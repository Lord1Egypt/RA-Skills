/**
 * Dynamics365Client — unit tests with fetch mocks
 *
 * Mock behaviour matches official Dataverse Web API docs (v9.2):
 *
 *  POST   → 204 No Content | OData-EntityId header contains record URI
 *  PATCH  → 204 No Content | no body; If-Match: * sent by client
 *  GET    → 200 OK         | { value: T[] }  (empty: { value: [] })
 *
 * Docs:
 *  Create: https://learn.microsoft.com/en-us/power-apps/developer/data-platform/webapi/create-entity-web-api
 *  Update: https://learn.microsoft.com/en-us/power-apps/developer/data-platform/webapi/update-delete-entities-using-web-api
 *  Query:  https://learn.microsoft.com/en-us/power-apps/developer/data-platform/webapi/query/overview
 */

import { Dynamics365Client } from "../src/client.js";

// ─── Mock helpers ────────────────────────────────────────────────────────────

const ORG_URI = "https://contoso.crm.dynamics.com";
const API_BASE = `${ORG_URI}/api/data/v9.2`;
const TOKEN = "mock-bearer-token";

/**
 * Simulate a successful POST response (204 No Content + OData-EntityId header).
 * Matches: https://learn.microsoft.com/en-us/power-apps/developer/data-platform/webapi/create-entity-web-api#basic-create
 */
function mockPost204(entitySet: string, guid: string): Response {
  return new Response(null, {
    status: 204,
    headers: {
      "OData-Version": "4.0",
      "OData-EntityId": `${API_BASE}/${entitySet}(${guid})`,
    },
  });
}

/**
 * Simulate a successful PATCH response (204 No Content, no body).
 * Matches: https://learn.microsoft.com/en-us/power-apps/developer/data-platform/webapi/update-delete-entities-using-web-api#basic-update
 */
function mockPatch204(): Response {
  return new Response(null, {
    status: 204,
    headers: { "OData-Version": "4.0" },
  });
}

/**
 * Simulate a GET query response (200 OK, { value: T[] }).
 * Matches: https://learn.microsoft.com/en-us/power-apps/developer/data-platform/webapi/query/overview#retrieve-data
 */
function mockGet200<T>(records: T[]): Response {
  return new Response(
    JSON.stringify({
      "@odata.context": `${API_BASE}/$metadata#entity/$entity`,
      value: records,
    }),
    {
      status: 200,
      headers: {
        "Content-Type": "application/json",
        "OData-Version": "4.0",
      },
    },
  );
}

/** Simulate an API error response */
function mockError(status: number, message: string): Response {
  return new Response(
    JSON.stringify({ error: { code: String(status), message } }),
    {
      status,
      headers: { "Content-Type": "application/json" },
    },
  );
}

// ─── Test setup ──────────────────────────────────────────────────────────────

let client: Dynamics365Client;

beforeEach(() => {
  client = new Dynamics365Client(ORG_URI, TOKEN);
  global.fetch = jest.fn();
});

afterEach(() => {
  jest.resetAllMocks();
});

// ─── Opportunity ─────────────────────────────────────────────────────────────

describe("upsertOpportunity", () => {
  const OPP_GUID = "aabbccdd-0000-0000-0000-000000000001";

  it("creates a new opportunity when none exists (POST → 204, ID from OData-EntityId)", async () => {
    (global.fetch as jest.Mock)
      .mockResolvedValueOnce(mockGet200([]))                     // search: no match
      .mockResolvedValueOnce(mockPost204("opportunities", OPP_GUID)); // POST

    const result = await client.upsertOpportunity({ name: "Deal TechNova Q2" });

    expect(result).toEqual({ id: OPP_GUID, created: true });

    const [searchCall, postCall] = (global.fetch as jest.Mock).mock.calls;
    expect(searchCall[0]).toContain("/opportunities?$select=opportunityid&$filter=");
    expect(searchCall[0]).toContain(encodeURIComponent("name eq 'Deal TechNova Q2'"));
    expect(postCall[1].method).toBe("POST");
    expect(JSON.parse(postCall[1].body as string).name).toBe("Deal TechNova Q2");
  });

  it("updates an existing opportunity when found (PATCH → 204, If-Match: *)", async () => {
    (global.fetch as jest.Mock)
      .mockResolvedValueOnce(mockGet200([{ opportunityid: OPP_GUID }])) // search: found
      .mockResolvedValueOnce(mockPatch204());                            // PATCH

    const result = await client.upsertOpportunity({
      name: "Deal TechNova Q2",
      estimatedvalue: 75000,
      stepname: "Propose",
    });

    expect(result).toEqual({ id: OPP_GUID, created: false });

    const [, patchCall] = (global.fetch as jest.Mock).mock.calls;
    expect(patchCall[0]).toContain(`/opportunities(${OPP_GUID})`);
    expect(patchCall[1].method).toBe("PATCH");
    expect(patchCall[1].headers["If-Match"]).toBe("*");
    const body = JSON.parse(patchCall[1].body as string);
    expect(body.estimatedvalue).toBe(75000);
    expect(body.stepname).toBe("Propose");
    expect(body.opportunityid).toBeUndefined(); // never sent in body
  });

  it("skips search when opportunityid is provided explicitly", async () => {
    (global.fetch as jest.Mock).mockResolvedValueOnce(mockPatch204());

    const result = await client.upsertOpportunity({
      opportunityid: OPP_GUID,
      name: "Deal TechNova Q2",
    });

    expect(result).toEqual({ id: OPP_GUID, created: false });
    expect(global.fetch).toHaveBeenCalledTimes(1); // only PATCH, no search
  });

  it("escapes single quotes in opportunity name for OData $filter", async () => {
    (global.fetch as jest.Mock)
      .mockResolvedValueOnce(mockGet200([]))
      .mockResolvedValueOnce(mockPost204("opportunities", OPP_GUID));

    await client.upsertOpportunity({ name: "O'Brien & Co" });

    const [searchCall] = (global.fetch as jest.Mock).mock.calls;
    expect(searchCall[0]).toContain(encodeURIComponent("name eq 'O''Brien & Co'"));
  });

  it("throws on POST error with status and body", async () => {
    (global.fetch as jest.Mock)
      .mockResolvedValueOnce(mockGet200([]))
      .mockResolvedValueOnce(mockError(401, "Unauthorized"));

    await expect(
      client.upsertOpportunity({ name: "Deal X" }),
    ).rejects.toThrow("Opportunity POST failed: 401");
  });

  it("throws on PATCH error", async () => {
    (global.fetch as jest.Mock)
      .mockResolvedValueOnce(mockGet200([{ opportunityid: OPP_GUID }]))
      .mockResolvedValueOnce(mockError(412, "Precondition Failed"));

    await expect(
      client.upsertOpportunity({ name: "Deal X" }),
    ).rejects.toThrow("Opportunity PATCH failed: 412");
  });
});

// ─── Lead ─────────────────────────────────────────────────────────────────────

describe("upsertLead", () => {
  const LEAD_GUID = "aabbccdd-0000-0000-0000-000000000002";

  it("creates a new lead when not found by email", async () => {
    (global.fetch as jest.Mock)
      .mockResolvedValueOnce(mockGet200([]))
      .mockResolvedValueOnce(mockPost204("leads", LEAD_GUID));

    const result = await client.upsertLead({
      fullname: "João Silva",
      emailaddress1: "joao@techno.com",
      companyname: "TechNova",
    });

    expect(result).toEqual({ id: LEAD_GUID, created: true });

    const [searchCall] = (global.fetch as jest.Mock).mock.calls;
    // Email is preferred over fullname as search key
    expect(searchCall[0]).toContain(
      encodeURIComponent("fullname eq 'joao@techno.com' or emailaddress1 eq 'joao@techno.com'"),
    );
  });

  it("searches by fullname when email is absent", async () => {
    (global.fetch as jest.Mock)
      .mockResolvedValueOnce(mockGet200([]))
      .mockResolvedValueOnce(mockPost204("leads", LEAD_GUID));

    await client.upsertLead({ fullname: "Maria Santos" });

    const [searchCall] = (global.fetch as jest.Mock).mock.calls;
    expect(searchCall[0]).toContain(encodeURIComponent("fullname eq 'Maria Santos'"));
  });

  it("updates existing lead found by name (PATCH → 204)", async () => {
    (global.fetch as jest.Mock)
      .mockResolvedValueOnce(mockGet200([{ leadid: LEAD_GUID }]))
      .mockResolvedValueOnce(mockPatch204());

    const result = await client.upsertLead({
      fullname: "Maria Santos",
      jobtitle: "CEO",
    });

    expect(result).toEqual({ id: LEAD_GUID, created: false });

    const [, patchCall] = (global.fetch as jest.Mock).mock.calls;
    expect(patchCall[1].headers["If-Match"]).toBe("*");
    expect(JSON.parse(patchCall[1].body as string).jobtitle).toBe("CEO");
  });

  it("skips search when neither name nor email provided", async () => {
    (global.fetch as jest.Mock).mockResolvedValueOnce(
      mockPost204("leads", LEAD_GUID),
    );

    await client.upsertLead({ telephone1: "+55 11 99999-0000" });

    expect(global.fetch).toHaveBeenCalledTimes(1); // no search call
  });
});

// ─── Contact ──────────────────────────────────────────────────────────────────

describe("upsertContact", () => {
  const CONTACT_GUID = "aabbccdd-0000-0000-0000-000000000003";

  it("creates a new contact (POST → 204)", async () => {
    (global.fetch as jest.Mock)
      .mockResolvedValueOnce(mockGet200([]))
      .mockResolvedValueOnce(mockPost204("contacts", CONTACT_GUID));

    const result = await client.upsertContact({
      fullname: "Ana Lima",
      emailaddress1: "ana@corp.com",
    });

    expect(result).toEqual({ id: CONTACT_GUID, created: true });
  });

  it("updates existing contact (PATCH → 204, If-Match: *)", async () => {
    (global.fetch as jest.Mock)
      .mockResolvedValueOnce(mockGet200([{ contactid: CONTACT_GUID }]))
      .mockResolvedValueOnce(mockPatch204());

    const result = await client.upsertContact({
      fullname: "Ana Lima",
      jobtitle: "CTO",
      "parentcustomerid_account@odata.bind": "/accounts(acc-001)",
    });

    expect(result).toEqual({ id: CONTACT_GUID, created: false });

    const [, patchCall] = (global.fetch as jest.Mock).mock.calls;
    expect(patchCall[0]).toContain(`/contacts(${CONTACT_GUID})`);
    const body = JSON.parse(patchCall[1].body as string);
    expect(body["parentcustomerid_account@odata.bind"]).toBe("/accounts(acc-001)");
  });

  it("returns null from searchContact on API error", async () => {
    (global.fetch as jest.Mock).mockResolvedValueOnce(mockError(403, "Forbidden"));

    const id = await client.searchContact("Ana Lima");
    expect(id).toBeNull();
  });
});

// ─── Account ──────────────────────────────────────────────────────────────────

describe("upsertAccount", () => {
  const ACCOUNT_GUID = "aabbccdd-0000-0000-0000-000000000004";

  it("creates a new account (POST → 204)", async () => {
    (global.fetch as jest.Mock)
      .mockResolvedValueOnce(mockGet200([]))
      .mockResolvedValueOnce(mockPost204("accounts", ACCOUNT_GUID));

    const result = await client.upsertAccount({ name: "TechNova Ltda" });

    expect(result).toEqual({ id: ACCOUNT_GUID, created: true });

    const [, postCall] = (global.fetch as jest.Mock).mock.calls;
    expect(postCall[0]).toContain("/accounts");
    expect(postCall[1].method).toBe("POST");
  });

  it("updates existing account (PATCH → 204)", async () => {
    (global.fetch as jest.Mock)
      .mockResolvedValueOnce(mockGet200([{ accountid: ACCOUNT_GUID }]))
      .mockResolvedValueOnce(mockPatch204());

    const result = await client.upsertAccount({
      name: "TechNova Ltda",
      websiteurl: "https://techno.com",
    });

    expect(result).toEqual({ id: ACCOUNT_GUID, created: false });

    const [, patchCall] = (global.fetch as jest.Mock).mock.calls;
    expect(patchCall[1].headers["If-Match"]).toBe("*");
  });

  it("uses provided accountid directly without search", async () => {
    (global.fetch as jest.Mock).mockResolvedValueOnce(mockPatch204());

    const result = await client.upsertAccount({
      accountid: ACCOUNT_GUID,
      name: "TechNova Ltda",
    });

    expect(result).toEqual({ id: ACCOUNT_GUID, created: false });
    expect(global.fetch).toHaveBeenCalledTimes(1);
  });
});

// ─── Task ─────────────────────────────────────────────────────────────────────

describe("createTask", () => {
  const TASK_GUID = "aabbccdd-0000-0000-0000-000000000005";

  it("creates a task and returns activityid from OData-EntityId header", async () => {
    (global.fetch as jest.Mock).mockResolvedValueOnce(
      mockPost204("tasks", TASK_GUID),
    );

    const id = await client.createTask({
      subject: "Follow-up call with TechNova",
      prioritycode: 2,
      scheduledend: "2026-05-01T10:00:00Z",
    });

    expect(id).toBe(TASK_GUID);

    const [call] = (global.fetch as jest.Mock).mock.calls;
    expect(call[0]).toContain("/tasks");
    expect(call[1].method).toBe("POST");
    const body = JSON.parse(call[1].body as string);
    expect(body.subject).toBe("Follow-up call with TechNova");
    expect(body.prioritycode).toBe(2);
    expect(body.activityid).toBeUndefined(); // never sent
  });

  it("creates a task linked to an opportunity via odata.bind", async () => {
    (global.fetch as jest.Mock).mockResolvedValueOnce(
      mockPost204("tasks", TASK_GUID),
    );

    await client.createTask({
      subject: "Send proposal",
      "regardingobjectid_opportunity_task@odata.bind":
        Dynamics365Client.bindRef("opportunities", "opp-guid-001"),
    });

    const body = JSON.parse(
      (global.fetch as jest.Mock).mock.calls[0][1].body as string,
    );
    expect(body["regardingobjectid_opportunity_task@odata.bind"]).toBe(
      "/opportunities(opp-guid-001)",
    );
  });

  it("throws on POST error", async () => {
    (global.fetch as jest.Mock).mockResolvedValueOnce(
      mockError(400, "Bad Request"),
    );

    await expect(
      client.createTask({ subject: "Test Task" }),
    ).rejects.toThrow("Task POST failed: 400");
  });
});

// ─── Static utilities ────────────────────────────────────────────────────────

describe("Dynamics365Client.recordUrl", () => {
  it("builds a correct deep link URL for an opportunity", () => {
    const url = Dynamics365Client.recordUrl(ORG_URI, "opportunity", "opp-001");
    expect(url).toBe(
      `${ORG_URI}/main.aspx?etn=opportunity&id=opp-001&pagetype=entityrecord`,
    );
  });

  it("strips trailing slash from instanceUrl", () => {
    const url = Dynamics365Client.recordUrl(`${ORG_URI}/`, "lead", "lead-001");
    expect(url).toBe(
      `${ORG_URI}/main.aspx?etn=lead&id=lead-001&pagetype=entityrecord`,
    );
  });
});

describe("Dynamics365Client.bindRef", () => {
  it("formats an OData binding reference correctly", () => {
    expect(Dynamics365Client.bindRef("accounts", "acc-guid-001")).toBe(
      "/accounts(acc-guid-001)",
    );
    expect(Dynamics365Client.bindRef("opportunities", "opp-001")).toBe(
      "/opportunities(opp-001)",
    );
  });
});

// ─── Request headers ─────────────────────────────────────────────────────────

describe("request headers", () => {
  it("sends required OData headers on every request", async () => {
    (global.fetch as jest.Mock).mockResolvedValue(mockGet200([]));

    await client.searchOpportunity("Test");

    const [, init] = (global.fetch as jest.Mock).mock.calls[0];
    expect(init.headers["Authorization"]).toBe(`Bearer ${TOKEN}`);
    expect(init.headers["OData-MaxVersion"]).toBe("4.0");
    expect(init.headers["OData-Version"]).toBe("4.0");
    expect(init.headers["Accept"]).toBe("application/json");
  });

  it("includes If-Match: * on all PATCH requests", async () => {
    const GUID = "aabbccdd-0000-0000-0000-000000000099";
    (global.fetch as jest.Mock)
      .mockResolvedValueOnce(mockGet200([{ opportunityid: GUID }]))
      .mockResolvedValueOnce(mockPatch204());

    await client.upsertOpportunity({ name: "Test" });

    const patchCall = (global.fetch as jest.Mock).mock.calls[1];
    expect(patchCall[1].headers["If-Match"]).toBe("*");
  });
});
