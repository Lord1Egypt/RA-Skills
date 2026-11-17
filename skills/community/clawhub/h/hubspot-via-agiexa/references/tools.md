# HubSpot tools via Agiexa (262)

Preview only - these become available to the agent after Agiexa launches (November 2026) and the merchant connects HubSpot and turns the tools on. They cannot be called today.

Interactive explorer: https://agiexa.com/integrations/hubspot

| Tool | What it does |
| --- | --- |
| `HUBSPOT_ADD_ASSET_ASSOCIATION` | Associates an existing asset ('FORM', 'OBJECT_LIST', or 'EXTERNAL_WEB_URL') with a specified HubSpot marketing campaign |
| `HUBSPOT_ADD_TOKEN_TO_EVENT_TEMPLATE` | Adds a new custom data token to an existing event template for a specified HubSpot application, optionally populating a CRM object property if objectP |
| `HUBSPOT_ARCHIVE_BATCH_OF_FEEDBACK_SUBMISSIONS` | Asynchronously archives a batch of HubSpot feedback submissions using their unique IDs, which must correspond to valid and existing submissions; the o |
| `HUBSPOT_ARCHIVE_BATCH_OF_LINE_ITEMS` | Archives a batch of existing line items by their unique IDs in HubSpot CRM; this operation is irreversible via the API |
| `HUBSPOT_ARCHIVE_BATCH_OF_OBJECTS` | Archives a batch of existing, non-archived CRM objects of a specified `objectType` by their IDs, effectively hiding them from active use |
| `HUBSPOT_ARCHIVE_BATCH_OF_PROPERTIES` | Archives a batch of properties by their internal names for a specified HubSpot CRM object type; this operation is idempotent and safe to retry |
| `HUBSPOT_ARCHIVE_BATCH_OF_QUOTES` | Archives a batch of existing quotes by their IDs, removing them from active views while keeping them accessible in your HubSpot account for viewing, d |
| `HUBSPOT_ARCHIVE_COMPANIES` | Archives multiple HubSpot companies by their IDs |
| `HUBSPOT_ARCHIVE_COMPANY` | Archives an existing company in HubSpot CRM by its `companyId`, moving it to a recycling bin from which it can be restored, rather than permanently de |
| `HUBSPOT_ARCHIVE_CONTACT` | Archives a HubSpot contact by its ID |
| `HUBSPOT_ARCHIVE_CONTACTS` | Archives multiple HubSpot contacts by their IDs |
| `HUBSPOT_ARCHIVE_CRM_OBJECT_BY_ID` | Archives a specific HubSpot CRM object by its type and ID, moving it to the recycling bin; this action is irreversible via the API but objects can oft |
| `HUBSPOT_ARCHIVE_DEALS` | Archives multiple HubSpot deals by their IDs |
| `HUBSPOT_ARCHIVE_EMAIL` | Archives the HubSpot email specified by `emailId` by moving it to the recycling bin, making it inaccessible unless restored |
| `HUBSPOT_ARCHIVE_EMAILS` | Archives multiple HubSpot emails by their IDs |
| `HUBSPOT_ARCHIVE_FEEDBACK_SUBMISSION` | Archives an existing, non-archived Feedback Submission in HubSpot CRM by its ID, moving it to the recycling bin (not permanently deleting it) |
| `HUBSPOT_ARCHIVE_LINE_ITEM` | Archives a specific HubSpot line item by its ID, moving it to a recoverable state |
| `HUBSPOT_ARCHIVE_PRODUCT` | Archives a HubSpot product by its ID |
| `HUBSPOT_ARCHIVE_PRODUCTS` | Archives multiple HubSpot products by their IDs |
| `HUBSPOT_ARCHIVE_PROPERTY_BY_OBJECT_TYPE_AND_NAME` | Archives a specified CRM property by its object type and name, moving it to the recycling bin; note that some default HubSpot properties cannot be arc |
| `HUBSPOT_ARCHIVE_PROPERTY_GROUP` | Archives a HubSpot property group, making it inactive and hidden (not permanently deleted, allowing potential restoration) with immediate effect on it |
| `HUBSPOT_RETRIEVE_OWNERS` | Retrieves a list of all owners in the HubSpot CRM, including their ID, first name, last name, email, and user ID |
| `HUBSPOT_ARCHIVE_QUOTE` | Archives a HubSpot Quote object by ID, moving it to the recycling bin where it can be restored within 90 days |
| `HUBSPOT_ARCHIVE_TICKET` | Archives a HubSpot ticket by its ID |
| `HUBSPOT_ARCHIVE_TICKETS` | Archives multiple HubSpot tickets by their IDs |
| `HUBSPOT_AUDIT_PIPELINE_CHANGES` | Retrieves a reverse chronological audit log of all changes for a specific, existing HubSpot CRM pipeline, which is identified by its `pipelineId` and |
| `HUBSPOT_BATCH_READ_COMPANIES_BY_PROPERTIES` | Batch-retrieves up to 100 HubSpot company records by their IDs in a single request |
| `HUBSPOT_BATCH_UPDATE_QUOTES` | Updates multiple existing HubSpot quotes in a batch; each quote is identified by its object ID or a custom unique property (via `idProperty`), and onl |
| `HUBSPOT_CANCEL_IMPORT` | Cancels an active HubSpot data import job using its `importId`; this action is irreversible, and any data already processed will remain |
| `HUBSPOT_CLONE_MARKETING_EMAIL` | Duplicates an existing HubSpot marketing email, identified by its `id`, into a new draft; an optional `cloneName` can be assigned to this new email co |
| `HUBSPOT_CONFIGURE_CALLING_EXTENSION_SETTINGS` | Configures or updates settings for a HubSpot app's calling extension, including its name, UI URL, iframe dimensions, `isReady` status, and `supportsCu |
| `HUBSPOT_CREATE_AB_TEST_VARIATION` | Creates a new A/B test variation for an existing HubSpot marketing email, using its `contentId`; the new variation is created as a draft that can be e |
| `HUBSPOT_CREATE_AND_RETURN_A_NEW_PROPERTY_GROUP` | Creates a new, empty property group for a specified CRM object type in HubSpot, requiring a unique group name for that object type; properties must be |
| `HUBSPOT_CREATE_A_NEW_MARKETING_EMAIL` | Creates a new marketing email in HubSpot, allowing comprehensive configuration of content, recipients, sender details, A/B testing, scheduling, web ve |
| `HUBSPOT_CREATE_ASSOCIATION` | Creates a new custom association definition (schema) for a custom object in HubSpot, specifying how this object type can relate to another object type |
| `HUBSPOT_CREATE_BATCH_OF_FEEDBACK_SUBMISSIONS` | Creates a batch of feedback submissions in HubSpot, ideal for bulk imports; all property names, `associationTypeId`s, and association `to_id`s must re |
| `HUBSPOT_CREATE_BATCH_OF_OBJECTS` | Creates multiple CRM objects of a specified `objectType` (e.g., contacts, companies, deals) in a single batch operation, where each object can have it |
| `HUBSPOT_CREATE_BATCH_OF_PROPERTIES` | Efficiently creates multiple CRM properties in a single batch for a specified HubSpot object type (e.g., 'contacts', 'companies', custom object ID), i |
| `HUBSPOT_CREATE_BATCH_OF_QUOTES` | Creates multiple HubSpot CRM quotes in a batch, ideal for bulk operations; provide meaningful quote details in `inputs` as property requirements can v |
| `HUBSPOT_CREATE_CAMPAIGN` | Creates a new HubSpot campaign |
| `HUBSPOT_CREATE_CAMPAIGNS` | Creates multiple HubSpot campaigns by calling the single campaign creation endpoint for each campaign |
| `HUBSPOT_CREATE_COMPANIES` | Creates multiple new HubSpot companies in a single batch operation |
| `HUBSPOT_CREATE_COMPANY` | Creates a new HubSpot company |
| `HUBSPOT_CREATE_CONTACT` | Creates a new HubSpot contact |
| `HUBSPOT_CREATE_CONTACT_FROM_NL` | Creates a new contact in HubSpot from a natural language description |
| `HUBSPOT_CREATE_CONTACTS` | Creates multiple new HubSpot contacts in a single batch operation |
| `HUBSPOT_CREATE_CRM_OBJECT_FROM_NL` | Creates a new CRM object (contact, deal, company, ticket, or custom object) in HubSpot from a natural language description |
| `HUBSPOT_CREATE_CRM_OBJECT_WITH_PROPERTIES` | Creates a new HubSpot CRM object (e.g., contact, company, custom object) with specified `properties` (using valid internal names) and `associations` ( |
| `HUBSPOT_CREATE_DEAL` | Creates a new HubSpot deal |
| `HUBSPOT_CREATE_DEAL_FROM_NL` | Creates a new deal in HubSpot from a natural language description |
| `HUBSPOT_CREATE_DEALS` | Creates multiple deals in HubSpot CRM; ensure any associated object IDs, deal stages, and pipeline IDs specified are valid and exist within the HubSpo |
| `HUBSPOT_CREATE_EMAIL` | Creates a new HubSpot email engagement record |
| `HUBSPOT_CREATE_EMAILS` | Creates multiple HubSpot emails in a single batch operation |
| `HUBSPOT_CREATE_ENGAGEMENT` | Create a legacy EMAIL, CALL, MEETING, TASK, or NOTE engagement with optional CRM associations, attachments, and type-specific metadata |
| `HUBSPOT_CREATE_EVENT_TEMPLATE_FOR_APP` | Creates a new event template for a HubSpot app, defining structure, custom properties (tokens), and appearance (Markdown with Handlebars) of custom ti |
| `HUBSPOT_CREATE_FEEDBACK_SUBMISSION` | Creates a new HubSpot feedback submission to record customer feedback (e.g., survey responses, support interactions), optionally associating it with C |
| `HUBSPOT_CREATE_LINE_ITEM` | Creates a new HubSpot line item |
| `HUBSPOT_CREATE_LINE_ITEMS` | Creates multiple HubSpot line items in a single batch operation |
| `HUBSPOT_CREATE_LIST` | Create a HubSpot CRM list with manual, snapshot, or dynamic membership rules |
| `HUBSPOT_GET_MARKETING_EMAIL_DRAFT` | Retrieves the draft version of a marketing email by its `emailId`; if no draft exists, returns the published version |
| `HUBSPOT_CREATE_MEETING` | Creates a new meeting engagement in HubSpot CRM |
| `HUBSPOT_CREATE_NOTE` | Creates a new HubSpot CRM note |
| `HUBSPOT_CREATE_OBJECT_ASSOCIATION` | Tool to create or label an association between two CRM records using HubSpot Associations v4 API |
| `HUBSPOT_CREATE_OBJECT_SCHEMA` | Creates a new custom object schema in HubSpot CRM with unique naming for schema and properties, defined display/required/searchable properties within |
| `HUBSPOT_CREATE_OR_UPDATE_DRAFT_VERSION` | Creates or updates the draft version of a marketing email identified by `emailId`; if no draft exists, a new one is created from the current live vers |
| `HUBSPOT_CREATE_PIPELINE` | Creates a new HubSpot pipeline for a specified CRM `objectType` (e.g., 'deals', 'tickets'), requiring the pipeline `label` be unique for that `objectT |
| `HUBSPOT_CREATE_PIPELINE_STAGE` | Creates a new stage in a specified HubSpot CRM pipeline for a given object type, such as 'deals' or 'tickets' |
| `HUBSPOT_CREATE_PRODUCT` | Creates a new HubSpot product |
| `HUBSPOT_CREATE_PRODUCTS` | Creates multiple HubSpot products in a single batch operation |
| `HUBSPOT_CREATE_PROPERTY_FOR_SPECIFIED_OBJECT_TYPE` | Creates a new custom property for a specified HubSpot CRM object type; ensure `groupName` refers to an existing property group for the `objectType` |
| `HUBSPOT_CREATE_QUOTE_OBJECT` | Creates a new quote object in HubSpot CRM with specified properties and associations |
| `HUBSPOT_CREATE_TASK` | Creates a new CRM task record |
| `HUBSPOT_CREATE_TICKET` | Creates a new HubSpot ticket |
| `HUBSPOT_CREATE_TICKETS` | Creates multiple HubSpot tickets in a batch, each with its own properties and associations; `inputs` list must not be empty, each item needs `properti |
| `HUBSPOT_CREATE_TIMELINE_EVENT` | Creates an immutable custom timeline event on a CRM object's record using a specified, existing event template (identified by `eventTemplateId`), opti |
| `HUBSPOT_CREATE_TIMELINE_EVENTS_BATCH` | Creates multiple immutable timeline events in a batch, ideal for bulk data imports or real-time synchronizations, using a valid event template; may up |
| `HUBSPOT_GET_MARKETING_EMAIL_REVISION` | Retrieves a specific, previously saved revision of a marketing email using its unique email ID and revision ID |
| `HUBSPOT_CREATE_WORKFLOW` | Creates a new HubSpot workflow to automate processes; ensure `enrollmentCriteria` and `actions` use properties relevant to the specified `objectTypeId |
| `HUBSPOT_DELETE_CALL` | Permanently deletes a HubSpot call record by its ID |
| `HUBSPOT_DELETE_CALLING_EXTENSION_SETTINGS` | Permanently deletes the settings for a calling extension app, specified by its `appId`, rendering it unusable for all connected HubSpot accounts; this |
| `HUBSPOT_DELETE_CAMPAIGN` | Permanently deletes a marketing campaign from HubSpot using its `campaignGuid`; returns a 204 No Content status even if the campaign does not exist |
| `HUBSPOT_DELETE_CAMPAIGNS_BATCH` | Archives a batch of up to 50 marketing campaigns, hiding them from active views rather than permanently deleting them |
| `HUBSPOT_DELETE_COMPANY_GDPR` | Permanently deletes a company (identified by objectId) and its associated data from HubSpot for GDPR compliance; this action is irreversible and requi |
| `HUBSPOT_DELETE_CONTACT_GDPR` | Irreversibly erases a HubSpot contact and associated data per a GDPR request; if an email is given for a non-existent contact, it's blocklisted |
| `HUBSPOT_DELETE_DEAL_GDPR` | Archives a HubSpot deal by its ID |
| `HUBSPOT_DELETE_LINE_ITEMS_GDPR` | Permanently deletes a specified line item and its associated content for GDPR compliance; this action is irreversible and cannot be undone |
| `HUBSPOT_DELETE_MARKETING_EMAIL` | Permanently deletes a marketing email from your HubSpot account |
| `HUBSPOT_DELETE_MEETING` | Permanently deletes (archives) a HubSpot meeting by its ID, moving it to the recycling bin where it can be restored within 90 days |
| `HUBSPOT_DELETE_NOTE` | Archives a HubSpot note by its ID, removing it from active view |
| `HUBSPOT_DELETE_PIPELINE` | Permanently deletes a HubSpot pipeline and all its stages by `pipelineId` and `objectType`; this is irreversible, so use validation flags to avoid err |
| `HUBSPOT_DELETE_PIPELINE_STAGE` | Permanently deletes a specific pipeline stage for an `objectType` (e.g., 'deals', 'tickets') that supports pipelines; this operation is irreversible, |
| `HUBSPOT_DELETE_SCHEMA` | Deletes a HubSpot custom object schema by `objectType` |
| `HUBSPOT_DELETE_TASK` | Archives a HubSpot task by its ID, removing it from active task lists |
| `HUBSPOT_DELETE_TIMELINE_EVENT_TEMPLATE` | Permanently and irreversibly deletes a specific timeline event template, identified by its `eventTemplateId`, from the application `appId` |
| `HUBSPOT_DELETE_VIDEO_CONFERENCING_APP_SETTINGS` | Irreversibly deletes all settings for a video conferencing application identified by its `appId` in HubSpot, removing its configuration and preventing |
| `HUBSPOT_DELETE_WORKFLOW` | Permanently deletes a HubSpot workflow by its ID; deleted workflows cannot be restored via the API and the ID must exist |
| `HUBSPOT_ENROLL_CONTACT_IN_WORKFLOW` | Enrolls a contact, identified by email, in a HubSpot workflow |
| `HUBSPOT_FETCH_IMPORT_ERROR_DETAILS` | Fetches a paginated list of read-only error details for a specific HubSpot CRM import, requiring a valid `importId` for a processed import |
| `HUBSPOT_FETCH_RECORDING_SETTINGS` | Fetches call recording settings for a specified, existing HubSpot calling extension app |
| `HUBSPOT_FETCH_REVENUE` | Fetches a revenue attribution report for a specified, existing marketing campaign, optionally using a specific attribution model and date range; if bo |
| `HUBSPOT_GET_AB_EMAIL_VARIATION` | Retrieves the alternate variation of a specified A/B marketing email; the `emailId` must identify an email currently in an A/B test |
| `HUBSPOT_GET_ACCOUNT_INFO` | Gets current HubSpot account info (email, hubId, user details) using access-token lookup |
| `HUBSPOT_GET_ACTIVE_IMPORTS_LIST` | Retrieves a list of currently active import jobs in HubSpot for monitoring ongoing data operations |
| `HUBSPOT_GET_AGGREGATED_STATISTIC_INTERVALS` | Retrieves aggregated statistics for marketing emails (e.g., send counts), grouped by specified time intervals within a defined time range |
| `HUBSPOT_GET_AGGREGATED_STATISTICS` | Retrieves aggregated statistics for marketing emails, optionally within an ISO8601 formatted time range, by email IDs, or specific email properties |
| `HUBSPOT_GET_ALL_MARKETING_EMAILS_FOR_A_HUBSPOT_ACCOUNT` | Fetches a list of marketing emails from a HubSpot account, with options for filtering, sorting, pagination, and including performance statistics |
| `HUBSPOT_GET_BLOG_POST` | Retrieves one HubSpot CMS blog post by post ID |
| `HUBSPOT_GET_CAMPAIGN` | Retrieves a HubSpot campaign by its ID |
| `HUBSPOT_GET_CAMPAIGN_METRICS` | Retrieves key attribution metrics for an existing marketing campaign, identified by its `campaignGuid`, within an optional date range |
| `HUBSPOT_GET_CAMPAIGNS` | Retrieves multiple HubSpot campaigns |
| `HUBSPOT_GET_COMPANY` | Retrieves a HubSpot company by its ID |
| `HUBSPOT_GET_CONTACT_IDS` | Fetches a list of contact IDs for a specific HubSpot campaign based on interaction type |
| `HUBSPOT_GET_CRM_LIST` | Retrieves a HubSpot CRM list by its ILS list ID |
| `HUBSPOT_GET_DEAL` | Retrieves a HubSpot deal by its ID |
| `HUBSPOT_GET_DEALS` | Retrieves multiple HubSpot deals by their IDs in a single batch request |
| `HUBSPOT_GET_EMAILS` | Retrieves multiple HubSpot email engagement records by their IDs in a single batch request |
| `HUBSPOT_GET_ENGAGEMENT` | Retrieve one legacy aggregate engagement by its engagement ID |
| `HUBSPOT_GET_EVENT_TEMPLATE` | Retrieves detailed information about a specific event template for a given application in HubSpot's CRM timeline |
| `HUBSPOT_GET_IMPORT_RECORD_INFORMATION` | Retrieves a comprehensive summary of a specific HubSpot CRM import record by its `importId`, including status, progress, updates, results, and errors; |
| `HUBSPOT_GET_MARKETING_EMAIL_REVISIONS` | Retrieves a paginated list of all historical versions (including full state like content, settings, metadata) for a specified, existing marketing emai |
| `HUBSPOT_GET_PIPELINE_BY_ID` | Retrieves a specific pipeline by its ID and CRM object type, detailing its stages and properties |
| `HUBSPOT_GET_PIPELINE_STAGE_AUDIT` | Retrieves a reverse chronological list of all mutations (changes) for a specific pipeline stage, including CREATE and UPDATE events with timestamps an |
| `HUBSPOT_GET_PRODUCT` | Retrieves a HubSpot product by its ID |
| `HUBSPOT_GET_PRODUCTS` | Retrieves multiple HubSpot products by their IDs |
| `HUBSPOT_GET_QUOTE` | Retrieves a specific HubSpot quote by its unique identifier |
| `HUBSPOT_GET_RECORD_LIST_MEMBERSHIPS` | Return the HubSpot lists that contain one CRM record |
| `HUBSPOT_GET_SEGMENT_MEMBERS` | Tool to retrieve segment (list) members ordered by join timestamp |
| `HUBSPOT_GET_THE_DETAILS_OF_A_SPECIFIED_MARKETING_EMAIL` | Retrieves detailed information for a specific marketing email in HubSpot using its unique email ID, optionally including performance statistics and sp |
| `HUBSPOT_GET_TICKET` | Retrieves a HubSpot ticket by its ID |
| `HUBSPOT_GET_TICKETS` | Retrieves multiple HubSpot tickets by their IDs |
| `HUBSPOT_GET_WORKFLOW_BY_ID` | Retrieves comprehensive details for an existing HubSpot workflow by its unique ID; unsupported actions are designated 'UNSUPPORTED_ACTION' in the resp |
| `HUBSPOT_GET_WORKFLOW_REVISION` | Retrieves a specific historical revision of a HubSpot workflow |
| `HUBSPOT_GET_WORKFLOWS` | Retrieves a list of workflow summaries (ID, name, type, status) from HubSpot, using the 'limit' parameter for pagination |
| `HUBSPOT_LIST_ASSETS` | Lists assets of a specific `assetType` for a given HubSpot marketing `campaignGuid`, optionally including performance metrics for a date range |
| `HUBSPOT_LIST_ASSOCIATION_TYPES` | Lists all valid association types between two specified HubSpot CRM object types |
| `HUBSPOT_LIST_AUDIT_LOGS` | Lists Enterprise-only HubSpot account audit logs with optional filters and pagination |
| `HUBSPOT_LIST_CALL_DISPOSITIONS` | Return HubSpot call disposition IDs and labels |
| `HUBSPOT_LIST_COMPANIES` | Retrieves a paginated list of HubSpot companies |
| `HUBSPOT_LIST_COMPANY_ACTIVITIES` | List all activity/engagement associations from a company to a specified activity type (calls, emails, meetings, notes, or tasks) |
| `HUBSPOT_LIST_COMPANY_CALLS` | Lists all calls associated with a specific HubSpot company |
| `HUBSPOT_LIST_COMPANY_MEETINGS` | List all meetings associated with a specific company in HubSpot |
| `HUBSPOT_LIST_CONTACT_NOTES` | List all notes associated with a specific HubSpot contact |
| `HUBSPOT_LIST_CONTACT_PROPERTIES` | Lists all contact properties in your HubSpot account, including custom properties you've created |
| `HUBSPOT_LIST_CONTACTS` | Retrieves a paginated list of HubSpot contacts |
| `HUBSPOT_LIST_CONTACT_TASKS` | List all tasks associated with a specific contact |
| `HUBSPOT_LIST_CONVERSATION_THREADS` | Lists HubSpot conversation threads with filtering and forward pagination |
| `HUBSPOT_LIST_DEAL_ACTIVITIES` | Retrieves activities (notes, calls, emails, meetings, tasks) associated with a specific HubSpot deal |
| `HUBSPOT_LIST_DEAL_MEETINGS` | List all meetings associated with a specific deal in HubSpot |
| `HUBSPOT_LIST_DEALS` | Retrieves a paginated list of HubSpot deals |
| `HUBSPOT_LIST_EMAIL_EVENTS` | Lists one page of HubSpot marketing email events; continue with `offset` only while `hasMore` is true |
| `HUBSPOT_LIST_EMAILS` | Retrieves a paginated list of HubSpot emails, allowing selection of specific properties (with or without history), associated object IDs, and filterin |
| `HUBSPOT_LIST_EVENT_TEMPLATES` | Retrieves all event templates associated with a valid `appId` for an existing application in HubSpot's CRM Timeline |
| `HUBSPOT_LIST_FEEDBACK_SUBMISSIONS` | Retrieves a paginated list of feedback submissions from HubSpot, allowing specification of properties (including history), associated object IDs, and |
| `HUBSPOT_LIST_GRANTED_SCOPES` | Tool to introspect the current OAuth access token and return its granted scopes and metadata |
| `HUBSPOT_LIST_OBJECT_ASSOCIATIONS` | List all associations from a single CRM record to a specified target object type |
| `HUBSPOT_LIST_PRODUCTS` | Retrieves a paginated list of HubSpot products |
| `HUBSPOT_LIST_QUOTES` | Retrieves a paginated list of quotes, allowing selection of specific properties, property history, associated object IDs, and filtering by archived st |
| `HUBSPOT_LIST_RECENTLY_MODIFIED_ENGAGEMENTS` | Lists one page of engagements from HubSpot's last-30-days or 10,000-most-recently-updated feed |
| `HUBSPOT_LIST_SEQUENCES` | Lists automation sequences for a specific HubSpot user |
| `HUBSPOT_LIST_SITE_PAGES` | Return one cursor-controlled page of HubSpot website pages |
| `HUBSPOT_LIST_TICKETS` | Retrieves a paginated list of HubSpot tickets |
| `HUBSPOT_MERGE_COMPANIES` | Merges two existing company records of the same type in HubSpot CRM, where `objectIdToMerge` is absorbed into `primaryObjectId`; this operation is irr |
| `HUBSPOT_MERGE_CONTACTS` | Merges two HubSpot contacts into one |
| `HUBSPOT_MERGE_DEALS` | Merges two HubSpot deals into one |
| `HUBSPOT_MERGE_EMAILS` | Merges two HubSpot emails into one |
| `HUBSPOT_MERGE_FEEDBACK_SUBMISSIONS` | Merges two existing feedback submissions by ID, primarily for consolidating duplicates or related feedback; this operation is irreversible, and `prima |
| `HUBSPOT_MERGE_LINE_ITEMS` | Merges two line items, `objectIdToMerge` into `primaryObjectId`, which must be of the same type; `objectIdToMerge` is absorbed and the operation is ir |
| `HUBSPOT_MERGE_OBJECTS` | Merges two distinct HubSpot CRM objects of the same `objectType`, consolidating data into `primaryObjectId` (which is preserved) and deleting `objectI |
| `HUBSPOT_MERGE_PRODUCTS` | Merges two HubSpot products into one |
| `HUBSPOT_MERGE_QUOTES` | Merges two distinct quotes of the same type by consolidating `objectIdToMerge` into `primaryObjectId` (e.g., for combining information or updating ter |
| `HUBSPOT_MERGE_TICKETS` | Merges two HubSpot tickets into one |
| `HUBSPOT_PARTIALLY_UPDATE_CRM_OBJECT_BY_ID` | Partially updates specified properties of a CRM object (e.g., contact, company, deal) identified by its type and ID, or optionally by a unique propert |
| `HUBSPOT_PERMANENTLY_DELETE_CONTACT_VIA_GDPR` | Permanently deletes a HubSpot contact and all its associated data for GDPR compliance, identifying the contact by its ID or another unique property |
| `HUBSPOT_PUBLISH_MARKETING_EMAIL` | Publishes or sends a specified HubSpot marketing email that is valid and ready for sending; requires Marketing Hub Enterprise or the transactional ema |
| `HUBSPOT_READ_A_CRM_PROPERTY_BY_NAME` | Reads a specific CRM property definition for a given HubSpot object type by its internal name |
| `HUBSPOT_READ_ALL_PROPERTIES_FOR_OBJECT_TYPE` | Retrieves definitions and metadata (not actual values) for properties of a specified HubSpot CRM object type (e.g., 'contacts', 'companies', 'deals', |
| `HUBSPOT_READ_APAGE_OF_OBJECTS_BY_TYPE` | Retrieves a paginated list of objects for a specified and valid HubSpot CRM object type (e.g., 'contacts', 'companies', 'deals', or custom ID) |
| `HUBSPOT_READ_ASSOCIATIONS_BATCH` | Tool to batch-read CRM associations (e.g., deals→contacts, deals→companies) for up to 1,000 source record IDs in one request |
| `HUBSPOT_READ_BATCH_CRM_OBJECT_PROPERTIES` | Retrieves property definitions (metadata) for a batch of CRM object properties for a specified object type |
| `HUBSPOT_READ_BATCH_FEEDBACK_SUBMISSIONS_BY_ID_OR_PROPERTY` | Retrieves up to 100 feedback submissions in a batch using their IDs or a specified unique `idProperty`, optionally including specified properties and |
| `HUBSPOT_READ_BATCH_OF_CRM_OBJECTS_BY_ID_OR_PROPERTY_VALUES` | Reads a batch of CRM objects of a specified `objectType` using their HubSpot IDs or unique property values from the `inputs` list, allowing retrieval |
| `HUBSPOT_READ_BATCH_OF_LINE_ITEMS_BY_ID_OR_PROPERTY_VALUES` | Retrieves a batch of HubSpot CRM line items by their IDs, or optionally by values of a custom unique property defined in `idProperty` |
| `HUBSPOT_READ_BATCH_OF_QUOTES_BY_PROPERTY_VALUES` | Efficiently retrieves a batch of HubSpot CRM quotes by their IDs (or a specified unique property), optionally including archived quotes, specific prop |
| `HUBSPOT_READ_BUDGET` | Fetches detailed budget (total, spent, remaining) and spend information for a marketing campaign, including an 'order' field for sequencing budget/spe |
| `HUBSPOT_READ_CONTACT` | Retrieves a HubSpot contact by its ID |
| `HUBSPOT_READ_CONTACTS` | Batch read multiple HubSpot contacts by their IDs or custom identifier property |
| `HUBSPOT_READ_CRM_OBJECT_BY_ID` | Retrieves a specific CRM object (e.g., contact, company, deal, ticket) by its ID or a unique property, optionally including specific properties, histo |
| `HUBSPOT_READ_EMAIL` | Call this to retrieve an existing HubSpot email by its `emailId` or an alternative unique `idProperty` |
| `HUBSPOT_READ_FEEDBACK_SUBMISSION_BY_ID` | Reads a HubSpot feedback submission by its ID, optionally using a custom unique 'idProperty', and allows specifying properties to return including his |
| `HUBSPOT_READ_PROPERTY_GROUP` | Retrieves metadata for a specific property group of a given CRM object type, detailing its structure and attributes, but not the actual property value |
| `HUBSPOT_RETRIEVE_OWNER_BY_ID_OR_USER_ID` | Retrieves a specific HubSpot CRM owner by their ID, with options to specify ID type (owner or user) and to include archived records |
| `HUBSPOT_READ_PROPERTY_GROUPS_FOR_OBJECT_TYPE` | Retrieves all property groups in a single call for a specified HubSpot CRM object type (e.g., 'contacts', 'companies'), returning only the groups them |
| `HUBSPOT_REMOVE_ASSET_ASSOCIATION` | Disassociates an asset from a HubSpot marketing campaign |
| `HUBSPOT_REMOVE_ASSOCIATION` | Tool to remove all associations between two CRM records using the v4 associations endpoint |
| `HUBSPOT_REMOVE_ASSOCIATION_FROM_SCHEMA` | Permanently removes a specified association definition (type) from a HubSpot object's schema, preventing future creations of this association type wit |
| `HUBSPOT_REMOVE_DEAL` | Removes a HubSpot deal by its ID |
| `HUBSPOT_REMOVE_TOKEN_FROM_EVENT_TEMPLATE` | Removes a token from a HubSpot event template, preventing its inclusion in new events created from that template |
| `HUBSPOT_RENDER_EVENT_DETAIL_TEMPLATE` | Renders detailed information for a specific HubSpot CRM timeline event using a predefined event template, ignoring `extraData` references in the templ |
| `HUBSPOT_RENDER_EVENT_HEADER_OR_DETAIL_AS_HTML` | Renders an event's header or detail template as HTML for a specified event on the HubSpot CRM timeline, using a given event template ID and event ID |
| `HUBSPOT_REPLACE_ALL_PROPERTIES_OF_PIPELINE` | Overwrites an entire CRM pipeline (specified by `objectType` and `pipelineId`) and all its stages with a new definition, returning the updated pipelin |
| `HUBSPOT_REPLACE_PIPELINE_STAGE_PROPERTIES` | Replaces all properties of a specified pipeline stage; the new `label` must be unique within the pipeline, and if `objectType` is 'deals', the `metada |
| `HUBSPOT_RESET_DRAFT` | Resets a marketing email's draft to its currently published (live) version, discarding all unpublished changes; the email must have a live version to |
| `HUBSPOT_RESTORE_EMAIL_REVISION` | Restores a specific revision of a marketing email to a DRAFT state, overwriting any existing draft |
| `HUBSPOT_RESTORE_MARKETING_EMAIL_REVISION` | Restores a specific, existing, non-active revision of a marketing email to become the new live version for that email |
| `HUBSPOT_RETRIEVE_ALL_OBJECT_SCHEMAS` | Retrieves all object schema definitions (not data records) for a HubSpot account, supporting retrieval of either active or archived schemas |
| `HUBSPOT_RETRIEVE_ALL_PIPELINES_FOR_SPECIFIED_OBJECT_TYPE` | Retrieves all pipelines in HubSpot for a specified CRM object type, such as deals or tickets |
| `HUBSPOT_RETRIEVE_CALLING_SETTINGS_FOR_APP` | Retrieves the read-only calling extension settings for a specific HubSpot app; the app must exist and have calling extensions configured |
| `HUBSPOT_RETRIEVE_LINE_ITEM_BY_ID` | Retrieves a HubSpot CRM line item by its ID or a specified unique property (`idProperty`) |
| `HUBSPOT_RETRIEVE_LINE_ITEMS` | Fetches a paginated list of HubSpot CRM line items, allowing selection of specific properties (including history), associated object IDs, and filterin |
| `HUBSPOT_RETRIEVE_OBJECT_SCHEMA` | Fetches the detailed schema definition for a specified, existing standard or custom HubSpot CRM object type; this action is read-only and does not cre |
| `HUBSPOT_RETRIEVE_PAGE_OF_CRM_OWNERS` | Retrieves a paginated list of CRM owners from HubSpot, optionally filtering by email or archived status |
| `HUBSPOT_RETRIEVE_PIPELINE_STAGE_BY_ID` | Fetches detailed properties and metadata (e.g., label, display order, custom properties) for a specific stage within a HubSpot CRM pipeline, identifie |
| `HUBSPOT_RETRIEVE_PIPELINE_STAGES` | Fetches all stages for a specified HubSpot CRM object type and pipeline ID |
| `HUBSPOT_RETRIEVE_TIMELINE_EVENT_BY_IDS` | Retrieves a specific HubSpot CRM timeline event by its application ID, event template ID, and event ID, returning event details including timestamp, t |
| `HUBSPOT_RETRIEVE_VIDEO_CONFERENCE_SETTINGS_BY_ID` | Retrieves video conference application settings, such as webhook URLs and user/account management configurations, for a specified `appId` |
| `HUBSPOT_SEARCH_CAMPAIGNS` | Searches for HubSpot campaigns |
| `HUBSPOT_SEARCH_COMPANIES` | Searches for HubSpot companies using flexible criteria and filters |
| `HUBSPOT_SEARCH_CONTACTS_BY_CRITERIA` | Searches for HubSpot contacts using a text query, specific filter criteria (filters in a group are ANDed, groups are ORed), sorting, and pagination to |
| `HUBSPOT_SEARCH_CRM_OBJECTS_BY_CRITERIA` | Searches HubSpot CRM objects (e.g., 'contacts', 'companies') by `objectType` using complex criteria including filters, sorting, and pagination; proper |
| `HUBSPOT_SEARCH_DEALS` | Searches for HubSpot deals using flexible criteria and filters |
| `HUBSPOT_SEARCH_EMAILS` | Searches for HubSpot emails using flexible criteria and filters |
| `HUBSPOT_SEARCH_FEEDBACK_SUBMISSIONS` | Searches for feedback submissions in HubSpot CRM using text query, filter groups, sorting, and pagination, returning specified properties |
| `HUBSPOT_SEARCH_LINE_ITEMS_BY_CRITERIA` | Searches HubSpot line items using criteria including filters, sorting, and pagination; `after` must be a valid cursor from a previous response, and `s |
| `HUBSPOT_SEARCH_PRODUCTS` | Searches for HubSpot products using flexible criteria and filters |
| `HUBSPOT_SEARCH_QUOTES_BY_CRITERIA` | Searches HubSpot CRM quotes using a text query, complex filter criteria, sorting, and pagination |
| `HUBSPOT_SEARCH_TICKETS` | Searches for HubSpot tickets using flexible criteria and filters |
| `HUBSPOT_SET_CALL_RECORDING_SETTINGS` | Configures the URL (`urlToRetrieveAuthedRecording`) that HubSpot uses to retrieve call recordings for a specified third-party calling app (`appId`) |
| `HUBSPOT_START_IMPORT` | Call this action to start an asynchronous data import into HubSpot CRM using uploaded files and a detailed `importRequest` JSON configuration, ensurin |
| `HUBSPOT_UPDATE_A_MARKETING_EMAIL` | Updates properties of an existing marketing email identified by its `emailId`; unspecified fields retain their current values |
| `HUBSPOT_UPDATE_BATCH_FEEDBACK_SUBMISSIONS` | Updates a batch of HubSpot feedback submissions; property keys must be existing internal HubSpot names and values must be correctly formatted strings |
| `HUBSPOT_UPDATE_BATCH_OF_OBJECTS_BY_IDOR_PROPERTY_VALUES` | Performs a batch update on a valid `objectType` where properties are writeable and any `idProperty` used is designated unique; updates can be partial |
| `HUBSPOT_UPDATE_CALLING_APP_RECORDING_SETTINGS` | Updates the recording settings, such as the URL for retrieving authenticated recordings, for a specific calling extension app identified by its `appId |
| `HUBSPOT_UPDATE_CALLING_EXTENSION_SETTINGS` | Updates settings (e.g., display name, UI URL/dimensions, feature flags) for an existing calling extension app, identified by `appId` |
| `HUBSPOT_UPDATE_CAMPAIGN` | Partially updates specific, writable properties of an existing HubSpot marketing campaign identified by `campaignGuid`; an empty string value in `prop |
| `HUBSPOT_UPDATE_CAMPAIGNS` | Updates properties for up to 50 existing HubSpot marketing campaigns in a single batch operation |
| `HUBSPOT_UPDATE_COMPANIES` | Updates multiple HubSpot companies in a single batch operation |
| `HUBSPOT_UPDATE_COMPANY` | Updates properties for an existing HubSpot company |
| `HUBSPOT_UPDATE_CONTACT` | Updates properties for an existing HubSpot contact |
| `HUBSPOT_UPDATE_CONTACTS` | Updates multiple HubSpot contacts in a single batch operation |
| `HUBSPOT_UPDATE_CRM_PROPERTY` | Updates attributes of an existing HubSpot CRM property, identified by its `objectType` and `propertyName`; only provided fields are modified, and chan |
| `HUBSPOT_UPDATE_DEAL` | Updates properties for an existing HubSpot deal |
| `HUBSPOT_UPDATE_DEALS` | Updates multiple HubSpot deals in a single batch operation |
| `HUBSPOT_UPDATE_EMAIL` | Partially updates properties of an existing HubSpot email object, identified by `emailId` (as internal ID or custom unique property value if `idProper |
| `HUBSPOT_UPDATE_EMAILS` | Updates multiple HubSpot emails in a single batch operation |
| `HUBSPOT_UPDATE_EVENT_TEMPLATE` | Updates an existing HubSpot event template's name, display templates, and tokens; providing `tokens` replaces the entire existing list, and the `id` i |
| `HUBSPOT_UPDATE_FEEDBACK_SUBMISSION` | Partially updates writable properties of an existing HubSpot Feedback Submission, identified by its `feedbackSubmissionId` (which can be an internal o |
| `HUBSPOT_UPDATE_LINE_ITEM` | Partially updates specified properties of an existing HubSpot Line Item, identified by `lineItemId` (as HubSpot object ID or value of `idProperty` if |
| `HUBSPOT_UPDATE_LINE_ITEMS` | Updates a batch of existing HubSpot CRM line items in a single operation, identifying each by its primary ID or a unique `idProperty` (which must be a |
| `HUBSPOT_UPDATE_OBJECT_SCHEMA` | Updates an existing custom object schema's metadata in HubSpot, such as its description, labels, display properties, required properties, searchable p |
| `HUBSPOT_UPDATE_PIPELINE` | Partially updates a CRM pipeline's label, display order, or restores an archived pipeline by setting `archived` to `false` |
| `HUBSPOT_UPDATE_PIPELINE_STAGE` | Partially updates a HubSpot CRM pipeline stage identified by `objectType`, `pipelineId`, and `stageId`, requiring `metadata` in the request; unspecifi |
| `HUBSPOT_UPDATE_PRODUCT` | Updates properties for an existing HubSpot product |
| `HUBSPOT_UPDATE_PRODUCTS` | Updates multiple HubSpot products in a single batch operation |
| `HUBSPOT_UPDATE_PROPERTY_GROUP` | Partially updates a property group's `displayOrder` or `label` for a specified CRM `objectType` in HubSpot |
| `HUBSPOT_UPDATE_QUOTE` | Performs a partial update on an existing HubSpot quote's specified properties, identifying the quote by `quoteId` (either its internal ID or a custom |
| `HUBSPOT_UPDATE_TICKET` | Updates properties for an existing HubSpot ticket |
| `HUBSPOT_UPDATE_TICKETS` | Updates multiple HubSpot tickets in a single batch operation |
| `HUBSPOT_UPDATE_TOKEN_ON_EVENT_TEMPLATE` | Updates the label or options of an existing token within a specified HubSpot CRM event template; token name and data type remain unchanged |
| `HUBSPOT_UPDATE_VIDEO_CONFERENCE_APP_SETTINGS` | Updates webhook URLs (for creating/updating/deleting meetings, fetching accounts, verifying users) for a video conference application specified by `ap |
| `HUBSPOT_UPDATE_WORKFLOW` | Fully replace an existing Automation v4 workflow at its current revision |
| `HUBSPOT_UPSERT_CONTACTS` | Creates or updates as many as 100 HubSpot contacts by unique property value |
| `HUBSPOT_WHO_AM_I` | Return the connected HubSpot account (portal id, domain) |
