import { defineTool, defineWorkflow } from "@cargo-ai/cdk";
import { z } from "zod";

import { linkedin } from "../connectors/linkedin";
import { slack } from "../connectors/slack";
import { toolsFolder } from "../folders";
import { gtmAccounts } from "../models/gtm-accounts";
import { gtmContacts } from "../models/gtm-contacts";
import { slackChannelId } from "../settings";

// PLACEHOLDER: the qualification rules, taken from the ICP in context/. They
// read LinkedIn's company data: `employee_count` is a number (use it, not
// `employee_range`, which can disagree with it), and `hq_country` is an ISO
// 3166 alpha-2 code ("US", "GB"). Confirm both with one live call on a known
// customer before deploying.
const icpMinEmployees = 50;
const icpMaxEmployees = 5000;
const icpCountries = ["US", "GB", "FR", "DE"];

// PLACEHOLDER: the scheduling page a qualified visitor is sent to.
const bookingUrl = "https://cal.com/example/demo";

// A demo form asks for a work email: the domain is how the company is found.
// Accepting these is the `accept-personal-email` variation.
const freeMailDomains = [
  "gmail.com",
  "googlemail.com",
  "yahoo.com",
  "hotmail.com",
  "outlook.com",
  "live.com",
  "icloud.com",
  "me.com",
  "aol.com",
  "proton.me",
  "protonmail.com",
  "gmx.com",
  "yandex.com",
];

// One submission from the website's form, in the order a request is cheapest
// to refuse:
//
//   personal email  -> refused on the page, nothing paid, nothing written
//   known domain    -> company from LinkedIn, the ICP rules, the account and
//                      the contact in the shared GTM models, one Slack post,
//                      and the booking link on the page when it qualifies
//
// The company is enriched, never the person: the person told us who they are.
// The answer is the run's output: the site submits in async mode and shows it
// when the run finishes.
const inboundSubmission = defineWorkflow(
  "inbound_form",
  {
    // The form's fields are this schema: the SDK renders and validates them.
    // `utm_*`, `page_url` and `referrer` arrive as hidden values.
    input: z.object({
      email: z.string().email().describe("Work email"),
      first_name: z.string().describe("First name"),
      last_name: z.string().describe("Last name"),
      message: z.string().optional().describe("What would you like to see?"),
      consent: z
        .boolean()
        .optional()
        .describe("I agree to receive product news by email"),
      utm_source: z.string().optional(),
      utm_medium: z.string().optional(),
      utm_campaign: z.string().optional(),
      page_url: z.string().optional(),
      referrer: z.string().optional(),
    }),
    output: z.object({
      status: z.enum(["qualified", "not_qualified", "work_email_required"]),
      bookingUrl: z.string().optional(),
    }),
    uses: { linkedin, slack },
    imports: {
      gtmAccounts,
      gtmContacts,
      freeMailDomains,
      icpMinEmployees,
      icpMaxEmployees,
      icpCountries,
      bookingUrl,
      slackChannelId,
    },
  },
  ({ input, uses, model }) => {
    const domain = input.email
      .toLowerCase()
      .slice(input.email.indexOf("@") + 1);

    // Refused before any paid call or write: the page asks again.
    if (freeMailDomains.includes(domain)) {
      return { status: "work_email_required" as const };
    }

    const company = uses.linkedin.enrichCompanyFromDomain({ domain: domain });
    const qualified =
      company.employee_count >= icpMinEmployees &&
      company.employee_count <= icpMaxEmployees &&
      icpCountries.includes(company.hq_country);

    const accounts = model.upsert({
      modelUuid: gtmAccounts.uuid,
      matchingColumnSlug: "website",
      matchingValue: domain,
      mappings: [
        { columnSlug: "website", value: domain },
        { columnSlug: "name", value: company.company_name },
        { columnSlug: "number_of_employees", value: company.employee_count },
        { columnSlug: "billing_country", value: company.hq_country },
        { columnSlug: "linkedin_url", value: company.linkedin_url },
        { columnSlug: "description", value: company.description },
      ],
    });

    model.upsert({
      modelUuid: gtmContacts.uuid,
      matchingColumnSlug: "email",
      matchingValue: input.email,
      mappings: [
        { columnSlug: "email", value: input.email },
        { columnSlug: "first_name", value: input.first_name },
        { columnSlug: "last_name", value: input.last_name },
        {
          columnSlug: "name",
          value: `${input.first_name} ${input.last_name}`,
        },
        { columnSlug: "account_id", value: accounts[0].id },
        { columnSlug: "lead_source", value: "website" },
      ],
      customMappings: [
        {
          columnSlug: "inbound_status",
          value: company.company_name
            ? qualified
              ? "qualified"
              : "not_qualified"
            : "unknown_company",
        },
        { columnSlug: "inbound_message", value: input.message },
        { columnSlug: "inbound_page_url", value: input.page_url },
        { columnSlug: "utm_source", value: input.utm_source },
        { columnSlug: "utm_campaign", value: input.utm_campaign },
        { columnSlug: "marketing_consent", value: input.consent },
      ],
    });

    uses.slack.postMessage({
      channelId: slackChannelId,
      format: "markdown",
      disableUnfurling: true,
      body: `*New inbound${qualified ? ", qualified" : ""}* from ${input.first_name} ${input.last_name} at ${company.company_name ? company.company_name : domain} (${domain})\n${company.employee_count} employees, ${company.hq_country}\n${input.message}\n\nPage: ${input.page_url}`,
    });

    if (qualified) {
      return { status: "qualified" as const, bookingUrl: bookingUrl };
    }

    return { status: "not_qualified" as const };
  },
);

// The public form is this tool's entry point: the website submits to it, and
// each submission runs the workflow above. The tool has to be published for
// the form to accept submissions; a deploy publishes it.
//
// Spam: the SDK's honeypot and render timestamp, the server's per-IP rate
// limit, and `minFillMillis`, counted from when the form became usable (the
// site loads the SDK once the page has hydrated). A CAPTCHA is the `turnstile` variation;
// its secret goes through `env()`, never into this file.
export const inboundForm = defineTool("inbound_form", {
  folder: toolsFolder,
  workflow: inboundSubmission,
  name: "Inbound form",
  description:
    "The website's demo form: qualifies each submission against the ICP, lands it in the GTM accounts and contacts, posts it to Slack, and answers with a booking link or a thank-you.",
  publicForm: {
    isEnabled: true,
    // PLACEHOLDER: the site's canonical origin, exactly (no trailing slash).
    // Every other origin is refused with 403.
    allowedOrigins: ["https://www.example.com"],
    spam: {
      captchaProvider: null,
      captchaSiteKey: null,
      captchaSecret: null,
      minFillMillis: 3000,
    },
    presentation: null,
  },
});
