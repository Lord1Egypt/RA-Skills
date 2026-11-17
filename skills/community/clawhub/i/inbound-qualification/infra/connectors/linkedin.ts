import { defineConnector } from "@cargo-ai/cdk";

// LinkedIn company data on Cargo's credits. `enrichCompanyFromDomain` turns
// the submitter's email domain into a company: its name, headcount,
// headquarters country and industries, which the qualification rules read.
// Binds the workspace's default connection, so there is nothing to configure.
export const linkedin = defineConnector("linkedin", {
  integration: "linkedin",
  default: true,
});
