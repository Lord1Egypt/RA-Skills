import { defineConnector } from "@cargo-ai/cdk";

// Enrichment for the company. A Sales Navigator lead carries a company URL,
// not a domain, and the CRM lookup needs a domain: `enrichCompany` turns one
// into the other and brings the firmographics the qualifier reads.
export const linkedin = defineConnector("linkedin", {
  integration: "linkedin",
  default: true,
});
