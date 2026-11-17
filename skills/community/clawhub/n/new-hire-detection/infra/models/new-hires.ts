import { defineModel } from "@cargo-ai/cdk";

import { salesNavigator } from "../connectors/sales-navigator";
import { modelsFolder } from "../folders";

// One market slice as a Sales Navigator people search. Every value is a
// PLACEHOLDER for the operator's market: the titles they sell to, the
// industries, the headcount band and the regions. Derive them from the ICP in
// the context repo when it exists; ask for them only when it does not.
//
// Facet ids are LinkedIn's, not labels. Headcount uses letters (B 1-10,
// C 11-50, D 51-200, E 201-500, F 501-1,000, G 1,001-5,000, H 5,001-10,000,
// I 10,001+). Industry and region ids come from the integration's
// autocompletes, never from memory: a wrong id is silently ignored and the
// search widens to the whole market.
//
// The three job-change filters are not part of the market and must not be
// edited away (see SKILL.md, "What should not change"):
// RECENTLY_CHANGED_JOBS, under a year at the company, and under a year in the
// position. Together they drop internal promotions, which look like a job
// change and are not one.
const search = {
  titles: [
    "VP Sales",
    "Head of Sales",
    "Chief Revenue Officer",
    "VP Revenue Operations",
    "Head of Revenue Operations",
    "Director of Revenue Operations",
    "Head of Growth",
  ],
  excludedTitleWords: [
    "intern",
    "interim",
    "fractional",
    "assistant",
    "recruiter",
    "student",
  ],
  headcounts: [
    { id: "D", text: "51-200" },
    { id: "E", text: "201-500" },
  ],
  industries: [{ id: "4", text: "Software Development" }],
  regions: [{ id: "103644278", text: "United States" }],
};

// Sales Navigator reads its query as a nested list in which every free-text
// value is encoded once and the whole query is encoded again. A single
// encoding pass loads an empty search page, and the extractor then returns
// nothing while reporting success.
const encodeText = (value: string) =>
  encodeURIComponent(value).replace(
    /[!'()*]/g,
    (char) => "%" + char.charCodeAt(0).toString(16).toUpperCase(),
  );

type Facet = { id?: string; text: string; excluded?: boolean };

const facet = (type: string, values: Facet[]) =>
  `(type:${type},values:List(${values
    .map(
      (value) =>
        "(" +
        (value.id === undefined ? "" : `id:${value.id},`) +
        `text:${encodeText(value.text)},selectionType:${
          value.excluded === true ? "EXCLUDED" : "INCLUDED"
        })`,
    )
    .join(",")}))`;

const searchUrl = (filters: string[]) =>
  "https://www.linkedin.com/sales/search/people?query=" +
  encodeURIComponent(`(filters:List(${filters.join(",")}))`)
    .replace(/%3A/g, ":")
    .replace(/%2C/g, ",") +
  "&viewAllFilters=true";

const newHireSearchUrl = searchUrl([
  facet("RECENTLY_CHANGED_JOBS", [{ id: "RPC", text: "Changed jobs" }]),
  facet("YEARS_AT_CURRENT_COMPANY", [{ id: "1", text: "Less than 1 year" }]),
  facet("YEARS_IN_CURRENT_POSITION", [{ id: "1", text: "Less than 1 year" }]),
  facet("COMPANY_HEADCOUNT", search.headcounts),
  facet("INDUSTRY", search.industries),
  facet("REGION", search.regions),
  facet("CURRENT_TITLE", [
    { text: search.titles.map((title) => `"${title}"`).join(" OR ") },
    ...search.excludedTitleWords.map((text) => ({ text, excluded: true })),
  ]),
]);

// One row per person who just took one of the titles above somewhere in the
// market, keyed by `linkedin_profile_id`. The play reacts to rows ADDED here,
// so a person is posted once, the first sync they appear in.
//
// Ships as the pilot: `limit: 10` and no schedule. Opening up raises `limit`
// to the approved value and adds the cadence (references/run.md in the skill).
// `limit` is per URL, and 2,500 is Sales Navigator's own ceiling for one
// search. Count the search before raising it (`searchPersonMetrics`, see
// references/search.md in the skill). Above 2,500, split it by a facet (one
// URL per region or per headcount band) and list every URL in `urls`; a single
// URL over the cap returns its first 2,500 and the rest of the market is never
// seen.
//
// THE SCHEDULE RE-BUYS THE SEARCH. `fetchLeadSearch` is not incremental:
// every sync extracts and bills every lead the search returns, including the
// ones already sitting in this model. "Changed jobs" covers roughly the last
// 90 days, so a sync every two weeks re-pays for most of the previous sync to
// find the people who are new. That is the price of being systematic; the
// cadence is the dial (see "What you can change"). The default, added when
// opening up, is the 1st and the 15th at 06:00 UTC:
//   schedule: { type: "cron", cron: "0 6 1,15 * *" },
//
// If you deploy with a schedule and later delete the line, that does NOT clear
// the live cron: the deploy engine omits a silent field and the platform keeps
// what it has. Clear it at runtime instead:
//   cargo-ai storage model update --uuid <modelUuid> --schedule null
export const newHires = defineModel("new_hires", {
  connector: salesNavigator,
  extractSlug: "fetchLeadSearch",
  description:
    "People who just took a target role anywhere in the market, from a Sales Navigator job-change search. Each new row is qualified and, when it fits the ICP, posted to Slack by the new-hire play.",
  folder: modelsFolder,
  config: {
    urls: [newHireSearchUrl],
    limit: 10,
  },
});
