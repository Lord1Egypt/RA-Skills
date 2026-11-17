# Add the CRM

The template ends at a Slack post and needs no CRM. Two variations add one,
and they are offered, not assumed: inspect the authenticated connectors, and
when a CRM is connected, say what each adds and what it costs before writing
either.

| Variation     | What it adds                                                                                                | What it costs                                                                                                                          |
| ------------- | ----------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------- |
| `crm_lookup`  | One read-only line on the Slack post: already in the CRM or not, its stage, and its owner                   | A CRM connector and one lookup per qualified person. Nothing is written                                                                |
| `crm_routing` | The CRM becomes the destination: account, contact and an owner's task, routed on what the CRM already holds | Owner IDs, a CSM field, association types and a LinkedIn field to resolve; an email lookup per person; the CRM writes are irreversible |

Both match on the domain and the LinkedIn profile in every stored form (the
lookup script below), never on one exact form: a known account read as new is
a duplicate, and on `crm_routing` a known person read as a stranger is one too.

HubSpot is the worked example for both. Salesforce and Attio change the
connector, the lookups, the routing signal, the contact key and the task
together, following the sections at the end.

## The connector and the lookup script

Add `infra/connectors/crm.ts`:

```ts
import { defineConnector } from "@cargo-ai/cdk";

// Binds the workspace's DEFAULT HubSpot connector rather than creating one:
// authorize it once (`cargo-ai project add connector/hubspot`) and this
// declaration resolves to it.
export const crm = defineConnector("crm", {
  integration: "hubspot",
  default: true,
});
```

and `infra/scripts/lookup.ts`, called after the company enrichment and read by
the domain guard (`if (!lookup.domain)`) in place of `company.domain`:

```ts
// What the account and person lookups search for: the enriched domain and the
// Sales Navigator profile, in every form a CRM could have stored them. A CRM
// lookup matches stored text, not normalized text, so one exact form misses the
// account stored as `www.` and the contact stored without a trailing slash, and
// the play then creates a duplicate of each.
//
// The same normalization as crm-deduplication (`scripts/contacts/identity.ts`,
// `scripts/accounts/account.ts`), so a record this play writes reads as the
// same record to the deduplication audit.

import { defineScript } from "@cargo-ai/cdk";

export const prepareLookups = defineScript(
  ({
    domain,
    linkedinProfileUrl,
  }: {
    domain: string | undefined;
    linkedinProfileUrl: string;
  }) => {
    const bareDomain = normalizeDomain(domain);
    return {
      // The domain guard reads this rather than the enrichment's raw value,
      // so a domain of `https://` alone stops the run too.
      domain: bareDomain,
      domainVariants: domainVariants(bareDomain),
      linkedinUrlVariants: linkedinUrlVariants(linkedinProfileUrl),
    };
  },
);

/** A property as text, with `""` and absence read as the same thing. */
const asText = (value: unknown): string | undefined => {
  if (value === null || value === undefined) {
    return undefined;
  }

  const text = String(value).trim();
  return text === "" ? undefined : text;
};

/** A domain as its bare host: no scheme, `www.`, path, port or trailing dot. */
const normalizeDomain = (value: unknown): string | undefined => {
  const domain = asText(value)
    ?.toLowerCase()
    .replace(/^(?:https?:\/\/)?(?:www\.)?/, "")
    .replace(/[/?#][\s\S]*$/, "")
    .replace(/:\d+$/, "")
    .replace(/\.$/, "");
  return domain === "" ? undefined : domain;
};

/** The forms a CRM could hold for one company's domain. */
const domainVariants = (domain: string | undefined): string[] => {
  if (domain === undefined) {
    return [];
  }

  return [
    domain,
    `www.${domain}`,
    `https://${domain}`,
    `https://www.${domain}`,
  ];
};

/** The forms a CRM could hold for one LinkedIn profile. */
const linkedinUrlVariants = (value: unknown): string[] => {
  const handle = asText(value)
    ?.toLowerCase()
    .replace(/^(?:https?:\/\/)?(?:[\w-]+\.)?linkedin\.com\/in\//, "")
    .replace(/[?#].*$/, "")
    .replace(/\/+$/, "");
  if (handle === undefined || handle === "") {
    return [];
  }

  return [
    `https://linkedin.com/in/${handle}`,
    `https://linkedin.com/in/${handle}/`,
    `https://www.linkedin.com/in/${handle}`,
    `https://www.linkedin.com/in/${handle}/`,
  ];
};
```

Each variant is its own `findRecords` criterion, as in crm-deduplication's
contact search: criteria are OR'd and empty values are skipped.

Then update the contract's connector inventory to include `connector:crm`, and
add the assertions the variation below names.

## `crm_lookup`: one read-only line on the post

After the gate, before the post, look the account up and say what was found:

```ts
const accounts = uses.crm.findRecords({
  objectType: "companies",
  criterias: [
    { propertyName: "domain", value: lookup.domainVariants[0] },
    { propertyName: "domain", value: lookup.domainVariants[1] },
    { propertyName: "domain", value: lookup.domainVariants[2] },
    { propertyName: "domain", value: lookup.domainVariants[3] },
  ],
});
```

and append to the post's body:

```ts
`\n\nCRM: ${accounts.length > 0 ? `in HubSpot, ${accounts[0].properties.lifecyclestage}, owner ${accounts[0].properties.hubspot_owner_id}` : "not in HubSpot"}`;
```

Nothing else changes. Add to the contract: every CRM node is a `findRecords`
or `searchRecords`, and none is a write.

Customers and accounts with an open deal are qualified by definition. If the
team wants them posted even when the qualifier would decline them, move the
lookup before the qualifier and skip it when the account is found; say that
the qualifier then no longer sees them.

## `crm_routing`: the CRM as the destination

The CRM replaces Slack as where the hand-off lands, and the same job-change
event means different things depending on what it already holds:

| The account is…                | What the play does                                                                                  |
| ------------------------------ | --------------------------------------------------------------------------------------------------- |
| Not in the CRM                 | Qualifies it. If it fits: creates the account, the contact, and a task for the named owner          |
| In the CRM, open deal          | Adds the contact and a HIGH task for the owner: a new decision-maker mid-deal                       |
| A customer                     | Adds the contact and a HIGH task for the CSM to welcome them (the account owner when no CSM is set) |
| Any other stage, lead included | Adds the contact to the account. No task, no allocation                                             |

**One contact per person.** Before the routes split, the person is looked up
across the CRM by LinkedIn identity. Already a contact on this account: the run
stops before paying for an email. A contact at another company: they moved, and
that record is moved to the new account rather than duplicated. A mover's email
on file is their previous employer's, so it is replaced by the new one or
cleared, never carried over. Whether the team wants one contact per person or
one per company is asked.

What it asks for, on top of the template's inputs:

| Input               | Kind    | How it is answered                                                                                                                                                                                    |
| ------------------- | ------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `crm`               | derived | Inspect the authenticated connectors. If more than one CRM is connected, ask which one is the system of record                                                                                        |
| `new_account_owner` | asked   | Pick from the CRM's live owner list (HubSpot owners, Salesforce users, Attio members)                                                                                                                 |
| `person_dedupe`     | asked   | One contact per person (default: a mover's record is moved) or a new contact per company                                                                                                              |
| `csm_owner_field`   | derived | The company property holding the CSM as an owner, from the live schema. Ask only when none is obvious                                                                                                 |
| `routing_signal`    | derived | HubSpot: confirm `lifecyclestage` is populated on companies. Salesforce: the opportunities. Attio: the deal stage or a status attribute                                                               |
| `contact_key`       | derived | The contact field holding a LinkedIn URL. Use the one the project's other cookbooks use (crm-deduplication reads `linkedin_url`); check the stored shape is one of the four forms the lookup searches |
| `find_email_tool`   | derived | Instantiate Cargo's native Find Email tool, confirm its live inputs and output path, and replace `REPLACE-WITH-FIND-EMAIL-TOOL-UUID`                                                                  |

What holds once it is in:

- the qualifier runs on the new-account route only, and its verdict gates every
  write on it
- the person is looked up before anything is written, and a contact on the same
  account stops the run
- every task names an owner and is attached to the account and the contact.
  HubSpot cannot attach at insert, so the association nodes stay
- lookups never use `soqlQuery`

Contract assertions to add: the qualifier sits before any CRM write, every
contact write keys on the person lookup first, no contact write carries the
found person's email, three tasks (new account, open deal, customer) each
followed on HubSpot by its company association, and no task on the
known-account route.

The worked HubSpot play, replacing `infra/plays/route-new-hires.ts`. Keep the
Slack post on the routes that raise a task if the team wants both.

```ts
import { definePlay, defineWorkflow, toolRef } from "@cargo-ai/cdk";
import { z } from "zod";

import { icpQualifier } from "../agents/icp-qualifier";
import { crm } from "../connectors/crm";
import { linkedin } from "../connectors/linkedin";
import { playsFolder } from "../folders";
import { newHires } from "../models/new-hires";
import { prepareLookups } from "../scripts/lookup";

// Instantiate Cargo's native Find Email tool, confirm that it accepts these
// inputs, and replace this value with its deployed tool UUID. Confirm the
// release output path before deployment; this example expects `email`.
const findEmail = toolRef<{ email?: string }>(
  "REPLACE-WITH-FIND-EMAIL-TOOL-UUID",
);

// PLACEHOLDER: the HubSpot owner ID that receives accounts this play creates.
// A new account has no owner until someone is named, and a task with no owner
// lands in nobody's queue. Resolve it from the live owner list; never guess.
const newAccountOwnerId = "PLACEHOLDER_NEW_ACCOUNT_OWNER_ID";

// PLACEHOLDER: the company property that holds the customer's CSM, as a
// HubSpot owner. HubSpot has no standard one; find the portal's custom field
// in the live company schema. The customer task goes to that person, and to
// the account owner when the field is empty or the portal has none.
const csmOwnerProperty = "PLACEHOLDER_CSM_OWNER_PROPERTY";

// HubSpot's task-to-company and task-to-contact association types. A task
// cannot be associated when it is created (`insertRecord` takes mappings
// only), so each task is followed by explicit associations, or it surfaces in
// a task list detached from the account a rep would open.
const taskToCompany = "HUBSPOT_DEFINED:192";
const taskToContact = "HUBSPOT_DEFINED:204";

// One person who just took a target role. The same event means different
// things depending on what the CRM already holds, and the routes below are
// the play:
//
//   not in the CRM      -> qualify, then create the account, the contact and
//                          a task for the new account's owner
//   open opportunity    -> a new decision-maker mid-deal: tell the owner now
//   customer            -> a new stakeholder who did not choose you: the CSM
//                          welcomes them before they form a view
//   any other stage     -> add the contact to the account, nothing else. No
//   (lead, MQL, SQL…)      task and no allocation: the account already has
//                          whatever motion owns it
//
// One contact per person. The person is looked up across the whole CRM by
// their LinkedIn identity before anything is written. Found on the very
// account they just joined: not news, the run stops. Found anywhere else:
// they moved, and that record is updated onto the new account instead of a
// second contact being created. Ends at the CRM write: nothing is sent.
const routeNewHire = defineWorkflow(
  "route_new_hire",
  {
    // The `fetchLeadSearch` columns this workflow reads. Confirm them against
    // the live model after the first sync (`cargo-ai storage column list`).
    input: z.object({
      linkedin_profile_url: z.string(),
      sales_navigator_company_url: z.string(),
      first_name: z.string().optional(),
      last_name: z.string().optional(),
      job_title: z.string().optional(),
      company_name: z.string().optional(),
      tenure_length: z.string().optional(),
    }),
    output: z.object({
      route: z.enum([
        "no_domain",
        "new_account",
        "open_opportunity",
        "customer",
        "known_account",
      ]),
      status: z.enum([
        "written",
        "not_icp",
        "contact_already_on_account",
        "skipped",
      ]),
      rationale: z.string().optional(),
    }),
    uses: { crm, linkedin, findEmail, icpQualifier },
    imports: {
      newAccountOwnerId,
      csmOwnerProperty,
      taskToCompany,
      taskToContact,
    },
  },
  ({ input, uses }) => {
    // The lead carries a company URL, not a domain, and the CRM is matched on
    // the domain. Enrich first, match second.
    const company = uses.linkedin.enrichCompany({
      linkedinUrl: input.sales_navigator_company_url,
    });

    // Every form the CRM could hold the domain and the profile in. Both
    // lookups below are exact, so searching one form reads a known account as
    // new and a known person as a stranger, and the play duplicates both.
    const lookup = prepareLookups({
      domain: company.domain,
      linkedinProfileUrl: input.linkedin_profile_url,
    });

    // The domain guard. An empty domain matches nothing in HubSpot and
    // everything in a `contains` lookup on other CRMs; either way the route
    // would be wrong, so the run stops here.
    if (!lookup.domain) {
      return { route: "no_domain" as const, status: "skipped" as const };
    }

    // The account, by domain, in each stored form. Several accounts sharing a
    // domain is a duplicate for crm-deduplication; the first one is routed.
    const accounts = uses.crm.findRecords({
      objectType: "companies",
      criterias: [
        { propertyName: "domain", value: lookup.domainVariants[0] },
        { propertyName: "domain", value: lookup.domainVariants[1] },
        { propertyName: "domain", value: lookup.domainVariants[2] },
        { propertyName: "domain", value: lookup.domainVariants[3] },
      ],
    });

    // The person, anywhere in the CRM, by LinkedIn identity in each stored
    // form. Criteria are OR'd and empty values skipped. Add the portal's
    // LinkedIn ID property as a second criterion when it has one; never match
    // on the full name alone, which finds namesakes.
    const people = uses.crm.findRecords({
      objectType: "contacts",
      criterias: [
        {
          propertyName: "hs_linkedin_url",
          value: lookup.linkedinUrlVariants[0],
        },
        {
          propertyName: "hs_linkedin_url",
          value: lookup.linkedinUrlVariants[1],
        },
        {
          propertyName: "hs_linkedin_url",
          value: lookup.linkedinUrlVariants[2],
        },
        {
          propertyName: "hs_linkedin_url",
          value: lookup.linkedinUrlVariants[3],
        },
      ],
    });

    if (accounts.length === 0) {
      // New account: the only route that pays for a qualification, and the
      // only one that gates. A company the ICP rejects never reaches the CRM.
      const verdict = uses.icpQualifier({
        prompt: `Qualify ${company.company_name} (${company.domain}) against the ICP. ${input.first_name} ${input.last_name} just joined as ${input.job_title}. Company object: ${JSON.stringify(company)}`,
      });

      if (!verdict.answer.is_icp) {
        return {
          route: "new_account" as const,
          status: "not_icp" as const,
          rationale: verdict.answer.rationale,
        };
      }

      const created = uses.crm.upsertRecords({
        objectType: "companies",
        matchingPropertyName: "domain",
        matchingValue: lookup.domain,
        mappings: [
          { propertyName: "name", value: company.company_name },
          { propertyName: "website", value: company.website },
          {
            propertyName: "linkedin_company_page",
            value: company.linkedin_url,
          },
          {
            propertyName: "numberofemployees",
            value: company.employee_count,
          },
          { propertyName: "lifecyclestage", value: "lead" },
          { propertyName: "hubspot_owner_id", value: newAccountOwnerId },
        ],
      });

      const found = uses.findEmail({
        linkedin_url: input.linkedin_profile_url,
        first_name: input.first_name,
        last_name: input.last_name,
      });

      // A known person is moved, not duplicated: matched on their record ID.
      // Otherwise keyed on the email when one was found, so the contact
      // dedupes against one the team created by hand, and on the LinkedIn URL
      // when not. A mover's email on file is their previous employer's, so it
      // is replaced by the new one or cleared, never carried to this account.
      const contact = uses.crm.upsertRecords({
        objectType: "contacts",
        matchingPropertyName:
          people.length > 0
            ? "hs_object_id"
            : found.email
              ? "email"
              : "hs_linkedin_url",
        matchingValue:
          people.length > 0
            ? people[0].id
            : found.email
              ? found.email
              : input.linkedin_profile_url,
        mappings: [
          {
            propertyName: "email",
            value: found.email ? found.email : "",
          },
          { propertyName: "firstname", value: input.first_name },
          { propertyName: "lastname", value: input.last_name },
          { propertyName: "jobtitle", value: input.job_title },
          {
            propertyName: "hs_linkedin_url",
            value: input.linkedin_profile_url,
          },
          { propertyName: "associatedcompanyid", value: created[0].id },
        ],
      });

      const task = uses.crm.insertRecord({
        objectType: "tasks",
        mappings: [
          {
            propertyName: "hs_task_subject",
            value: `New ${input.job_title} at ${company.company_name}, a new ${verdict.answer.fit_tier} account`,
          },
          {
            propertyName: "hs_task_body",
            value: `${input.first_name} ${input.last_name} just joined ${company.company_name} as ${input.job_title} (${input.tenure_length}). The account was not in the CRM; it was created because it qualified.${people.length > 0 ? " They were already in the CRM as a contact at another company, and the record was moved here." : ""}\n\nICP: ${verdict.answer.fit_tier}, ${verdict.answer.fit_score}/100, ${verdict.answer.confidence} confidence. ${verdict.answer.rationale}\n\nLinkedIn: ${input.linkedin_profile_url}`,
          },
          { propertyName: "hs_task_status", value: "NOT_STARTED" },
          { propertyName: "hs_task_priority", value: "MEDIUM" },
          { propertyName: "hs_task_type", value: "TODO" },
          { propertyName: "hs_timestamp", value: new Date() },
          { propertyName: "hubspot_owner_id", value: newAccountOwnerId },
        ],
      });

      uses.crm.createAssociation(
        {
          fromObjectType: "tasks",
          fromObjectId: task[0].id,
          toObjectType: "companies",
          toObjectId: created[0].id,
          associationTypeId: taskToCompany,
        },
        { continueOnFailure: true },
      );
      uses.crm.createAssociation(
        {
          fromObjectType: "tasks",
          fromObjectId: task[0].id,
          toObjectType: "contacts",
          toObjectId: contact[0].id,
          associationTypeId: taskToContact,
        },
        { continueOnFailure: true },
      );

      return {
        route: "new_account" as const,
        status: "written" as const,
        rationale: verdict.answer.rationale,
      };
    }

    // The account is in the CRM. Its lifecycle stage is the routing signal in
    // HubSpot; confirm it is actually maintained before trusting it (see
    // references/crm-adaptation.md for routing on deals instead).
    const stage = accounts[0].properties.lifecyclestage;
    const route =
      stage === "opportunity"
        ? ("open_opportunity" as const)
        : stage === "customer"
          ? ("customer" as const)
          : ("known_account" as const);

    // Already a contact on this very account: not news. Stop before paying
    // for an email. Found on another account, they moved: carry on, and the
    // write below moves that record here.
    if (
      people.length > 0 &&
      people[0].properties.associatedcompanyid === accounts[0].id
    ) {
      return { route, status: "contact_already_on_account" as const };
    }

    const found = uses.findEmail({
      linkedin_url: input.linkedin_profile_url,
      first_name: input.first_name,
      last_name: input.last_name,
    });

    const contact = uses.crm.upsertRecords({
      objectType: "contacts",
      matchingPropertyName:
        people.length > 0
          ? "hs_object_id"
          : found.email
            ? "email"
            : "hs_linkedin_url",
      matchingValue:
        people.length > 0
          ? people[0].id
          : found.email
            ? found.email
            : input.linkedin_profile_url,
      mappings: [
        {
          propertyName: "email",
          value: found.email ? found.email : "",
        },
        { propertyName: "firstname", value: input.first_name },
        { propertyName: "lastname", value: input.last_name },
        { propertyName: "jobtitle", value: input.job_title },
        { propertyName: "hs_linkedin_url", value: input.linkedin_profile_url },
        { propertyName: "associatedcompanyid", value: accounts[0].id },
      ],
    });

    // The routes differ in who is told and why. Each task sits on both the
    // account and the contact.
    if (stage === "opportunity") {
      // The highest-urgency route and the one most CRMs miss: a new
      // decision-maker landed mid-deal. The owner hears it today.
      const task = uses.crm.insertRecord({
        objectType: "tasks",
        mappings: [
          {
            propertyName: "hs_task_subject",
            value: `New decision-maker mid-deal: ${input.first_name} ${input.last_name}, ${input.job_title} at ${company.company_name}`,
          },
          {
            propertyName: "hs_task_body",
            value: `${input.first_name} ${input.last_name} just joined ${company.company_name} as ${input.job_title} (${input.tenure_length}), and the account has an open deal.${people.length > 0 ? " They were already in the CRM as a contact at another company, and the record was moved here." : " They were not in the CRM before today."} Multi-thread now: a new decision-maker either unblocks the deal or restarts it.\n\nLinkedIn: ${input.linkedin_profile_url}`,
          },
          { propertyName: "hs_task_status", value: "NOT_STARTED" },
          { propertyName: "hs_task_priority", value: "HIGH" },
          { propertyName: "hs_task_type", value: "TODO" },
          { propertyName: "hs_timestamp", value: new Date() },
          {
            propertyName: "hubspot_owner_id",
            value: accounts[0].properties.hubspot_owner_id,
          },
        ],
      });
      uses.crm.createAssociation(
        {
          fromObjectType: "tasks",
          fromObjectId: task[0].id,
          toObjectType: "companies",
          toObjectId: accounts[0].id,
          associationTypeId: taskToCompany,
        },
        { continueOnFailure: true },
      );
      uses.crm.createAssociation(
        {
          fromObjectType: "tasks",
          fromObjectId: task[0].id,
          toObjectType: "contacts",
          toObjectId: contact[0].id,
          associationTypeId: taskToContact,
        },
        { continueOnFailure: true },
      );
      return { route: "open_opportunity" as const, status: "written" as const };
    } else if (stage === "customer") {
      // A new leader inside a customer is a churn risk before it is an
      // expansion: they did not choose you. The CSM welcomes them before they
      // form a view; the account owner when no CSM is set.
      const task = uses.crm.insertRecord({
        objectType: "tasks",
        mappings: [
          {
            propertyName: "hs_task_subject",
            value: `New ${input.job_title} at customer ${company.company_name}: welcome them before they form a view`,
          },
          {
            propertyName: "hs_task_body",
            value: `${input.first_name} ${input.last_name} just joined ${company.company_name} as ${input.job_title} (${input.tenure_length}).${people.length > 0 ? " They were already in the CRM as a contact at another company, and the record was moved here." : ""} This is a customer, and a new leader arrives with opinions about the tools they used before. Welcome them and walk them through what the team already runs this week, before the renewal becomes their decision instead of the team's.\n\nLinkedIn: ${input.linkedin_profile_url}`,
          },
          { propertyName: "hs_task_status", value: "NOT_STARTED" },
          { propertyName: "hs_task_priority", value: "HIGH" },
          { propertyName: "hs_task_type", value: "TODO" },
          { propertyName: "hs_timestamp", value: new Date() },
          {
            propertyName: "hubspot_owner_id",
            value: accounts[0].properties[csmOwnerProperty]
              ? accounts[0].properties[csmOwnerProperty]
              : accounts[0].properties.hubspot_owner_id,
          },
        ],
      });
      uses.crm.createAssociation(
        {
          fromObjectType: "tasks",
          fromObjectId: task[0].id,
          toObjectType: "companies",
          toObjectId: accounts[0].id,
          associationTypeId: taskToCompany,
        },
        { continueOnFailure: true },
      );
      uses.crm.createAssociation(
        {
          fromObjectType: "tasks",
          fromObjectId: task[0].id,
          toObjectType: "contacts",
          toObjectId: contact[0].id,
          associationTypeId: taskToContact,
        },
        { continueOnFailure: true },
      );
      return { route: "customer" as const, status: "written" as const };
    } else {
      // Any other stage, lead included: the contact is on the account and
      // that is the whole job. No task, no allocation.
      return { route: "known_account" as const, status: "written" as const };
    }
  },
);

// Routes every person the search adds. There is no filter: the search URL
// already IS the audience, and a segment that restated it would be a drift
// trap.
//
// `changeKinds: ["added"]` is what makes a person routed once. The model
// re-extracts the whole search on every sync, and only people who were not in
// it before create a run. Drop it and every sync re-routes the whole search,
// paying for the enrichment and the email again and raising duplicate tasks.
//
// Cron, not watch or realtime: `fetchLeadSearch` is a fetch-mode extractor,
// so realtime and watch both fail at deploy with integrationNotCompatible.
// Hourly, because the model syncs on its own schedule and a new row should not
// wait a day for its run; ticks with nothing added create nothing.
//
// Ships disabled. Enabling is the last yes after the pilot of ten, not an
// input. Enable, then execute once: `changeKinds: ["added"]` does not
// backfill rows that landed while the play was off.
export const routeNewHires = definePlay("route_new_hires", {
  description:
    "Routes each person who just took a target role into the CRM by what the CRM already holds: qualify and create, alert the deal owner, have the CSM welcome them at a customer, or add them to a known account.",
  folder: playsFolder,
  model: newHires,
  workflow: routeNewHire,
  isEnabled: false,
  runCreationRule: "noConcurrency",
  changeKinds: ["added"],
  schedule: { type: "cron", cron: "20 * * * *" },
});
```

## Salesforce

**Every lookup is `findRecords` or `searchRecords`. Never `soqlQuery`.** Both
take a structured filter that Cargo validates against the object's fields and
turns into a query itself, so a field that does not exist fails loudly at
design time instead of returning nothing at run time, and the lookup stays
readable in the canvas. A hand-written SOQL string escapes neither: a
misspelled field or an unquoted domain becomes a run that looks successful and
routed every person down the wrong branch.

- `findRecords` takes `criterias` (`[{propertyName, value}]`, exact match, OR
  across criterias, empty values skipped). Use it for exact keys: a contact by
  its LinkedIn field, an account by an exact domain field when the org has one.
- `searchRecords` takes the same `filter` shape as HubSpot's and supports
  `contains`, `is`, `isNot`, numeric and null operators. Use it when the match
  is not exact, such as `Website contains <domain>`.

### The account lookup

Salesforce has no domain field by default; `Website` holds a URL in whatever
form a rep typed it. Match on it with `contains`:

```ts
const accounts = uses.crm.searchRecords({
  objectType: "Account",
  limit: 1,
  filter: {
    conjonction: "or",
    groups: [
      {
        conjonction: "and",
        conditions: [
          {
            propertyName: "Website",
            operator: "contains",
            values: [lookup.domain],
          },
        ],
      },
    ],
  },
});
```

The domain guard before this lookup is not optional on Salesforce: an empty
domain makes `contains` match every account in the org, and the first one wins.
`contains` also over-matches a short domain inside a longer one (`acme.com` in
`notacme.com`), so check the pilot's matches by eye.

If the org keeps a clean custom domain field, prefer
`findRecords({ objectType: "Account", criterias: [{ propertyName: "<Domain__c>", value: lookup.domainVariants }] })`.

### The routing signal: opportunities, not `Account.Type`

`Account.Type` is frequently empty in real orgs, and a switch built on it
routes nothing. Count the values before trusting it (`listObjectFields`, then a
`searchRecords` on `Account` filtered `Type isNotNull` with a small `limit`).
The dependable signal is the opportunities themselves:

```ts
const deals = uses.crm.searchRecords({
  objectType: "Opportunity",
  limit: 50,
  filter: {
    conjonction: "or",
    groups: [
      {
        conjonction: "and",
        conditions: [
          {
            propertyName: "AccountId",
            operator: "is",
            values: [accounts[0].Id],
          },
        ],
      },
    ],
  },
});
```

Then route on what came back:

- open opportunity: `deals.some((deal) => !deal.IsClosed)`
- customer: `deals.some((deal) => deal.IsWon)`
- known account, no open deal: neither

### Contacts

Salesforce has no LinkedIn field by default. Find the org's custom field
(often `LinkedIn_URL__c`, but it varies) with `listObjectFields` on `Contact`,
and if there is none, ask before creating one: it is the key that stops the
next sync from creating the same person twice.

- person lookup, before the routes split: `findRecords({ objectType: "Contact", criterias: [{ propertyName: "<LinkedIn field>", value: lookup.linkedinUrlVariants[0] }, …] })`, one criterion per variant
- same-account stop: the found contact's `AccountId` equals the account's `Id`
- write: `upsertRecords` on `Contact`, matching `Id` when the person was found
  (a mover is moved, not duplicated), else `Email` when the email was found,
  else the LinkedIn field, with `AccountId` set to the account
- new account: `upsertRecords` on `Account` matching `Website`, with `OwnerId`
  set to the owner the operator named

### Tasks

Salesforce tasks attach at insert, so the HubSpot play's two `createAssociation`
nodes go away. `insertRecord` on `Task` with:

| Field          | Value                                                                                                                                      |
| -------------- | ------------------------------------------------------------------------------------------------------------------------------------------ |
| `Subject`      | the route's subject line                                                                                                                   |
| `Description`  | the route's body                                                                                                                           |
| `WhoId`        | the contact's `Id`                                                                                                                         |
| `WhatId`       | the open opportunity's `Id` on that route, the account's `Id` on others                                                                    |
| `OwnerId`      | the opportunity's `OwnerId` on that route; on customers the account's CSM field (often a custom user lookup), else the account's `OwnerId` |
| `Status`       | `Not Started`                                                                                                                              |
| `Priority`     | `High` or `Normal`                                                                                                                         |
| `ActivityDate` | today                                                                                                                                      |

On the open-opportunity route the task sits on the deal and goes to the deal
owner, which is where a rep working that deal will see it.

## Attio

Attio has `findRecords`, `searchRecords`, `upsertRecords`, `insertRecord` and
`createNote`, and no task action.

- the account lookup: `findRecords` on `companies` with criteria on `domains`
- the routing signal: Attio has no lifecycle stage; read the deal records
  linked to the company (the `deals` object and its stage attribute, whose
  names vary per workspace) or a company status attribute the team maintains
- contacts: `people`, found by the LinkedIn attribute before the routes split,
  and moved by updating their company relationship when they sit on another one
- the task: there is no task write, so the owner is told with `createNote` on
  the company record (title and markdown body from the route), or through the
  team's Slack connector. Say which one before deploying: a note on the record
  is visible, but nobody is notified of it

## After adapting

From this skill's folder:

```sh
node --import tsx evals/contract.mjs
```

Then from the project root: `cargo-ai project types && cargo-ai project check && cargo-ai project plan`. In
the pilot, take one record through each route the variation adds, with the CRM record links in the
report.
