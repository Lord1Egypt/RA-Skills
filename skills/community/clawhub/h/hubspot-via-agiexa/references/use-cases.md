# HubSpot use cases via Agiexa

Example prompts a merchant will be able to give their agent after Agiexa launches (November 2026). They are illustrations of future use - do not run them today.

More examples and live demos: https://agiexa.com/integrations/hubspot

## Prioritize High-Value Sales Opportunities

Review open deals, recent activities, and next steps to identify opportunities that deserve immediate attention.

- Apps: HubSpot, Gmail, Shopify
- Tools: `HUBSPOT_SEARCH_DEALS`, `HUBSPOT_LIST_DEAL_ACTIVITIES`, `HUBSPOT_GET_DEALS`

> Analyze my open HubSpot deals and prioritize them based on deal value, current stage, expected close date, recent activity, and available engagement history. Identify deals that may be stalled, have no recorded next step, or require follow-up. Review associated contacts, companies, tasks, and activities where available. Use relevant Gmail conversations and Shopify business context when accessible, but do not assume a prospect is ready to buy without supporting evidence. Explain why each deal is prioritized and recommend a concrete next action. Present a ranked table with deal value, stage, last activity, outstanding questions, and suggested follow-up.

## Organize New Leads Automatically

Use new-contact events to validate records, identify potential duplicates, and prepare qualified leads for follow-up.

- Apps: HubSpot
- Tools: `HUBSPOT_SEARCH_CONTACTS_BY_CRITERIA`, `HUBSPOT_UPSERT_CONTACTS`, `HUBSPOT_CREATE_TASK`

> Help me configure a workflow for newly created HubSpot contacts. When a new contact is created, validate the available contact fields, check for existing records using reliable identifiers, and identify missing information. Review available company details and lead-source properties where accessible. Apply only approved lifecycle or qualification rules, and create a follow-up task when the contact meets the defined criteria. Avoid creating duplicate contacts, inventing missing information, or associating a contact with a deal without evidence of a sales opportunity. Show the proposed workflow conditions and actions before enabling it.

## Track Deal Stage Changes

React to deal-stage changes by reviewing associated information and identifying the appropriate next sales action.

- Apps: HubSpot
- Tools: `HUBSPOT_GET_DEAL`, `HUBSPOT_LIST_DEAL_ACTIVITIES`, `HUBSPOT_UPDATE_DEAL`

> Help me monitor HubSpot deal-stage changes. When a deal changes stage, retrieve its relevant properties, associated contact and company records, and recent activities where available. Determine which next steps are appropriate for the new stage based on my existing sales process. For example, a proposal-stage deal may need a quotation follow-up, while a negotiation-stage deal may need clarification of requirements. Identify missing information and prepare a task or follow-up draft when appropriate. Do not assume a deal is won or lost beyond its recorded stage, and do not send emails or change deal properties without approval.

## Prepare Personalized Sales Follow-Ups

Use CRM history and related email conversations to draft relevant, context-aware messages for prospects and customers.

- Apps: HubSpot, Gmail
- Tools: `HUBSPOT_READ_CONTACT`, `HUBSPOT_LIST_DEAL_ACTIVITIES`, `HUBSPOT_CREATE_TASK`

> Review selected HubSpot contacts and deals and identify opportunities that need a follow-up. Retrieve the associated company information, deal stage, recent CRM activities, and relevant Gmail correspondence where available. Draft a personalized email that accurately reflects the actual conversation and proposes a useful next step. Avoid repeating questions already answered or claiming that a quotation, meeting, or commitment exists unless the records support it. Include a suggested subject line, email body, related deal, and recommended follow-up date. Save or send messages only when the requested workflow supports it and I have approved the intended action.

## Connect Shopify Customers With CRM Records

Enrich sales and customer records with relevant Shopify order information when reliable matching is available.

- Apps: HubSpot, Shopify
- Tools: `HUBSPOT_SEARCH_CONTACTS_BY_CRITERIA`, `HUBSPOT_CREATE_OBJECT_ASSOCIATION`, `HUBSPOT_UPDATE_CONTACT`

> Help me connect Shopify customer and order information with the appropriate HubSpot contact and company records. Match records using reliable identifiers such as verified email addresses or explicit customer IDs when available. Summarize relevant order history, purchase frequency, order value, and recent product interests only when supported by the connected data. Identify unmatched records and potential duplicates for review. Do not assume every Shopify customer is a sales lead or that every order represents a separate customer. Preserve existing CRM data and show proposed updates and associations before applying them.

## Detect and Resolve CRM Duplicates

Identify duplicate contacts, companies, and deals while preserving important relationship and activity history.

- Apps: HubSpot
- Tools: `HUBSPOT_SEARCH_COMPANIES`, `HUBSPOT_MERGE_CONTACTS`, `HUBSPOT_MERGE_COMPANIES`

> Audit my HubSpot CRM for potential duplicate contacts, companies, and deals. Use reliable identifiers such as email addresses, company domains, and unique deal references where available. For each suspected duplicate, show the candidate records, matching evidence, differing properties, and associated activities or relationships that could be affected. Separate strong matches from uncertain similarities. Recommend which record should be retained and which should be merged, if appropriate. Do not merge or archive records automatically, and never permanently delete data as part of this review. Present a review table and request approval for each proposed merge.

## Manage Marketing Campaign Performance

Connect campaign activity with CRM contacts, deals, and revenue attribution to assess marketing effectiveness.

- Apps: HubSpot, Shopify, Google Ads
- Tools: `HUBSPOT_GET_CAMPAIGNS`, `HUBSPOT_GET_CAMPAIGN_METRICS`, `HUBSPOT_FETCH_REVENUE`

> Analyze my HubSpot marketing campaigns for the selected date range. Retrieve available campaign metrics, associated assets, email performance statistics, and revenue attribution information. Identify campaigns generating engagement, creating relevant contact activity, or contributing to associated deals where supported. Compare performance using clearly defined metrics and the available attribution model. If Shopify orders or Google Ads results are available through connected integrations, compare them only when the data can be matched reliably. Highlight underperforming campaigns and promising opportunities without assuming that correlation proves causation. Present the findings in tables and recommend the next steps. Do not publish emails or change live campaigns without approval.

## Automate Sales Tasks and Reminders

Turn missing next steps and qualified deal activity into structured follow-up tasks.

- Apps: HubSpot
- Tools: `HUBSPOT_LIST_DEAL_ACTIVITIES`, `HUBSPOT_CREATE_TASK`, `HUBSPOT_SEARCH_DEALS`

> Review my HubSpot deals and associated activities to identify opportunities that need a documented next step. Find deals without upcoming tasks, overdue follow-ups where dates are available, and recently changed deals that may require action. Recommend a task title, description, associated contact or company, due date, and priority for each case. Use my existing sales process and avoid creating duplicate tasks for work that is already scheduled. Where supported, create approved tasks and associate them with the correct CRM records. Do not invent deadlines or modify deal stages automatically.

## Improve the Sales Pipeline Structure

Review pipeline stages and deal data to identify process gaps, inconsistent records, and opportunities to improve sales visibility.

- Apps: HubSpot
- Tools: `HUBSPOT_RETRIEVE_ALL_PIPELINES_FOR_SPECIFIED_OBJECT_TYPE`, `HUBSPOT_RETRIEVE_PIPELINE_STAGES`, `HUBSPOT_AUDIT_PIPELINE_CHANGES`

> Review my HubSpot deal pipelines, stages, stage properties, and available pipeline change history. Identify stages with unclear progression criteria, deals missing important fields, and records that may be stalled or incorrectly categorized. Summarize the number and total value of deals in each stage where the required data is available. Recommend clearer stage definitions, required information, and next-step criteria. Distinguish observed pipeline data from suggestions for process improvement. Do not replace pipelines, delete stages, or change existing stage definitions without approval. Present a concise pipeline audit and a prioritized improvement plan.

## Generate a Weekly CRM Performance Report

Summarize leads, deals, follow-ups, campaign performance, and sales pipeline changes in one actionable report.

- Apps: HubSpot, Gmail, Shopify
- Tools: `HUBSPOT_LIST_DEALS`, `HUBSPOT_LIST_CONTACTS`, `HUBSPOT_GET_CAMPAIGNS`

> Prepare a weekly HubSpot CRM report for the selected period. Include newly created contacts, open deals, deals by stage, total pipeline value, upcoming close dates, overdue tasks where available, and deal-stage changes. Identify the most important follow-ups and deals without a clear next step. Include relevant campaign performance and revenue attribution metrics where accessible. Where Shopify and Gmail data are connected, use verified order information and relevant correspondence to add context to sales opportunities. Do not invent conversion rates, revenue attribution, or missing activity dates. Present metric cards, concise tables, key risks, and three prioritized actions for the coming week.
