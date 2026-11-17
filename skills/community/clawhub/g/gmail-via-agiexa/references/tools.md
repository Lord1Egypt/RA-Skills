# Gmail tools via Agiexa (61)

Preview only - these become available to the agent after Agiexa launches (November 2026) and the merchant connects Gmail and turns the tools on. They cannot be called today.

Interactive explorer: https://agiexa.com/integrations/gmail

| Tool | What it does |
| --- | --- |
| `GMAIL_BATCH_MODIFY_MESSAGES` | Modify labels on multiple Gmail messages in one efficient API call |
| `GMAIL_CREATE_EMAIL_DRAFT` | Creates a Gmail email draft |
| `GMAIL_CREATE_FILTER` | Tool to create a new Gmail filter with specified criteria and actions |
| `GMAIL_CREATE_LABEL` | Creates a new label with a unique name in the specified user's Gmail account |
| `GMAIL_CREATE_PROMPT_POST` | Send a one-shot prompt to the Sanity Content Agent |
| `GMAIL_DELETE_DRAFT` | Permanently deletes a specific Gmail draft using its ID with no recovery possible; verify the correct `draft_id` and obtain explicit user confirmation |
| `GMAIL_DELETE_FILTER` | Tool to permanently delete a Gmail filter by its ID |
| `GMAIL_DELETE_LABEL` | Permanently DELETES a user-created Gmail label from the account (not from a message) |
| `GMAIL_DELETE_MESSAGE` | Permanently deletes a specific email message by its ID from a Gmail mailbox; for `user_id`, use 'me' for the authenticated user or an email address to |
| `GMAIL_DELETE_THREAD` | Tool to immediately and permanently delete a specified thread and all its messages |
| `GMAIL_FETCH_EMAILS` | Fetches a list of email messages from a Gmail account, supporting filtering, pagination, and optional full content retrieval |
| `GMAIL_FETCH_MESSAGE_BY_MESSAGE_ID` | Fetches a specific email message by its ID, provided the `message_id` exists and is accessible to the authenticated `user_id` |
| `GMAIL_FETCH_MESSAGE_BY_THREAD_ID` | Retrieves messages from a Gmail thread using its `thread_id`, where the thread must be accessible by the specified `user_id` |
| `GMAIL_GET_ATTACHMENT` | Retrieves a specific attachment by ID from a message in a user's Gmail mailbox, requiring valid message and attachment IDs |
| `GMAIL_GET_AUTO_FORWARDING` | Tool to get the auto-forwarding setting for the specified account |
| `GMAIL_GET_CONTACTS` | Fetches contacts (connections) for the authenticated Google account, allowing selection of specific data fields and pagination |
| `GMAIL_GET_DRAFT` | Retrieves a single Gmail draft by its ID |
| `GMAIL_GET_FILTER` | Tool to retrieve a specific Gmail filter by its ID |
| `GMAIL_GET_LABEL` | Gets details for a specified Gmail label |
| `GMAIL_GET_LANGUAGE_SETTINGS` | Tool to retrieve the language settings for a Gmail user |
| `GMAIL_GET_PEOPLE` | Retrieves either a specific person's details (using `resource_name`) or lists 'Other Contacts' (if `other_contacts` is true), with `person_fields` spe |
| `GMAIL_GET_VACATION_SETTINGS` | Tool to retrieve vacation responder settings for a Gmail user |
| `GMAIL_IMPORT_MESSAGE` | Tool to import a message into the user's mailbox with standard email delivery scanning and classification |
| `GMAIL_INSERT_MESSAGE` | Tool to insert a message into the user's mailbox similar to IMAP APPEND |
| `GMAIL_LIST_CSE_IDENTITIES` | Tool to list client-side encrypted identities for an authenticated user |
| `GMAIL_LIST_CSE_KEYPAIRS` | Tool to list client-side encryption key pairs for an authenticated user |
| `GMAIL_LIST_FILTERS` | Tool to list all Gmail filters (rules) in the mailbox |
| `GMAIL_LIST_FORWARDING_ADDRESSES` | Tool to list all forwarding addresses for the specified Gmail account |
| `GMAIL_LIST_HISTORY` | Tool to list Gmail mailbox change history since a known startHistoryId |
| `GMAIL_LIST_LABELS` | Retrieves all system and user-created labels for a Gmail account in a single unpaginated response |
| `GMAIL_LIST_SEND_AS` | Lists the send-as aliases for a Gmail account, including the primary address and custom 'from' aliases |
| `GMAIL_LIST_SMIME_INFO` | Lists S/MIME configs for the specified send-as alias |
| `GMAIL_LIST_THREADS` | Retrieves a list of email threads from a Gmail account, identified by `user_id` (email address or 'me'), supporting filtering and pagination |
| `GMAIL_MODIFY_THREAD_LABELS` | Adds or removes specified existing label IDs from a Gmail thread, affecting all its messages; ensure the thread ID is valid |
| `GMAIL_MOVE_THREAD_TO_TRASH` | Moves the specified thread to the trash |
| `GMAIL_MOVE_TO_TRASH` | Moves an existing, non-deleted email message to the trash for the specified user |
| `GMAIL_PATCH_LABEL` | Patches the specified user-created label |
| `GMAIL_PATCH_SEND_AS` | Tool to patch the specified send-as alias for a Gmail user |
| `GMAIL_SEARCH_PEOPLE` | Searches contacts by matching the query against names, nicknames, emails, phone numbers, and organizations, optionally including 'Other Contacts' |
| `GMAIL_SEND_EMAIL` | Sends an email via Gmail API using the authenticated user's Google profile display name |
| `GMAIL_SETTINGS_GET_IMAP` | Retrieves the IMAP settings for a Gmail user account, including whether IMAP is enabled, auto-expunge behavior, expunge behavior, and maximum folder s |
| `GMAIL_SETTINGS_GET_POP` | Tool to retrieve POP settings for a Gmail account |
| `GMAIL_SETTINGS_SEND_AS_GET` | Tool to retrieve a specific send-as alias configuration for a Gmail user |
| `GMAIL_STOP_WATCH` | Tool to stop receiving push notifications for a Gmail mailbox |
| `GMAIL_UNTRASH_MESSAGE` | Tool to remove a message from trash in Gmail |
| `GMAIL_UNTRASH_THREAD` | Tool to remove a thread from trash in Gmail |
| `GMAIL_UPDATE_DRAFT` | Updates (replaces) an existing Gmail draft's content in-place by draft ID |
| `GMAIL_UPDATE_IMAP_SETTINGS` | Tool to update IMAP settings for a Gmail account |
| `GMAIL_UPDATE_LABEL` | Tool to update the properties of an existing Gmail label |
| `GMAIL_UPDATE_LANGUAGE_SETTINGS` | Tool to update the language settings for a Gmail user |
| `GMAIL_UPDATE_POP_SETTINGS` | Tool to update POP settings for a Gmail account |
| `GMAIL_UPDATE_SEND_AS` | Tool to update a send-as alias for a Gmail user |
| `GMAIL_UPDATE_USER_ATTRIBUTES_VALUES` | Update user attribute values for a resource |
| `GMAIL_UPDATE_VACATION_SETTINGS` | Tool to update vacation responder settings for a Gmail user |
| `GMAIL_ADD_LABEL_TO_EMAIL` | Adds and/or removes specified Gmail labels for a message; ensure `message_id` and all `label_ids` are valid (use 'listLabels' for custom label IDs) |
| `GMAIL_BATCH_DELETE_MESSAGES` | Tool to permanently delete multiple Gmail messages in bulk, bypassing Trash with no recovery possible |
| `GMAIL_FORWARD_MESSAGE` | Forward an existing Gmail message to specified recipients, preserving original body and attachments |
| `GMAIL_GET_PROFILE` | Retrieves Gmail profile information (email address, aggregate messagesTotal/threadsTotal, historyId) for a user |
| `GMAIL_LIST_DRAFTS` | Retrieves a paginated list of email drafts from a user's Gmail account |
| `GMAIL_REPLY_TO_THREAD` | Sends a reply within a specific Gmail thread using the original thread's subject; do not provide a custom subject as it will start a new conversation |
| `GMAIL_SEND_DRAFT` | Sends an existing draft email AS-IS to recipients already defined within the draft |
