# Google Calendar tools via Agiexa (47)

Preview only - these become available to the agent after Agiexa launches (November 2026) and the merchant connects Google Calendar and turns the tools on. They cannot be called today.

Interactive explorer: https://agiexa.com/integrations/google-calendar

| Tool | What it does |
| --- | --- |
| `GOOGLECALENDAR_ACL_DELETE` | Deletes an access control rule from a Google Calendar |
| `GOOGLECALENDAR_ACL_GET` | Retrieves a specific access control rule for a calendar |
| `GOOGLECALENDAR_ACL_INSERT` | Creates an access control rule for a calendar |
| `GOOGLECALENDAR_ACL_LIST` | Retrieves the list of access control rules (ACLs) for a specified calendar, providing the necessary 'rule_id' values required for updating specific AC |
| `GOOGLECALENDAR_ACL_PATCH` | Updates an existing access control rule for a calendar using patch semantics (partial update) |
| `GOOGLECALENDAR_ACL_UPDATE` | Updates an access control rule for the specified calendar |
| `GOOGLECALENDAR_ACL_WATCH` | Tool to watch for changes to ACL resources |
| `GOOGLECALENDAR_BATCH_EVENTS` | Execute up to 1000 event mutations (create/patch/delete) in one Google Calendar HTTP batch request with per-item status/results |
| `GOOGLECALENDAR_CALENDAR_LIST_DELETE` | Tool to remove a calendar from the user's calendar list |
| `GOOGLECALENDAR_CALENDAR_LIST_GET` | Retrieves metadata for a SINGLE specific calendar from the user's calendar list by its calendar ID |
| `GOOGLECALENDAR_CALENDAR_LIST_INSERT` | Inserts an existing calendar into the user's calendar list, making it visible in the UI |
| `GOOGLECALENDAR_CALENDAR_LIST_PATCH` | Updates an existing calendar on the user's calendar list using patch semantics |
| `GOOGLECALENDAR_CALENDAR_LIST_UPDATE` | Updates a calendar list entry's display/subscription settings (color, visibility, reminders, selection) for the authenticated user — does not modify t |
| `GOOGLECALENDAR_CALENDAR_LIST_WATCH` | Watch for changes to CalendarList resources using push notifications |
| `GOOGLECALENDAR_CALENDARS_DELETE` | Deletes a secondary calendar that you own or have delete permissions on |
| `GOOGLECALENDAR_CALENDARS_UPDATE` | Full PUT-style update that overwrites all calendar metadata fields; unspecified optional fields are cleared |
| `GOOGLECALENDAR_CHANNELS_STOP` | Tool to stop watching resources through a notification channel |
| `GOOGLECALENDAR_CLEAR_CALENDAR` | Clears a primary calendar by deleting all events from it |
| `GOOGLECALENDAR_COLORS_GET` | Returns the color definitions for calendars and events |
| `GOOGLECALENDAR_CREATE_CALENDAR` | Creates a new secondary Google Calendar with the specified title and optional settings |
| `GOOGLECALENDAR_CREATE_EVENT` | Creates an event in a selected calendar using start_datetime and either end_datetime or duration fields |
| `GOOGLECALENDAR_DELETE_EVENT` | Deletes a specified event by `event_id` from a Google Calendar (`calendar_id`); idempotent — a 404 for an already-deleted event is a no-op |
| `GOOGLECALENDAR_DUPLICATE_CALENDAR` | Creates a new, empty Google Calendar with the specified title (summary) |
| `GOOGLECALENDAR_EVENTS_GET` | Retrieves a SINGLE event by its unique event_id (REQUIRED) |
| `GOOGLECALENDAR_EVENTS_IMPORT` | Tool to import an event as a private copy to a calendar |
| `GOOGLECALENDAR_EVENTS_INSTANCES` | Returns instances of the specified recurring event |
| `GOOGLECALENDAR_EVENTS_LIST` | Lists or incrementally synchronizes events from one calendar, defaulting to the connected user's primary calendar |
| `GOOGLECALENDAR_EVENTS_LIST_ALL_CALENDARS` | Return a unified event list across all calendars in the user's calendar list for a given time range |
| `GOOGLECALENDAR_EVENTS_MOVE` | Moves an event to another calendar, i.e., changes an event's organizer |
| `GOOGLECALENDAR_EVENTS_WATCH` | Watch for changes to Events resources |
| `GOOGLECALENDAR_FIND_EVENT` | Finds events in a specified Google Calendar using text query, time ranges (event start/end, last modification), and event types |
| `GOOGLECALENDAR_FIND_FREE_SLOTS` | Finds both free and busy time slots in Google Calendars for specified calendars within a defined time range |
| `GOOGLECALENDAR_FREE_BUSY_QUERY` | Queries raw busy intervals for one or more calendars or groups over an exact time range |
| `GOOGLECALENDAR_GET_CALENDAR` | Gets canonical metadata for one Google Calendar, defaulting to the authenticated user's primary calendar |
| `GOOGLECALENDAR_GET_CURRENT_DATE_TIME` | Gets the current date and time, allowing for a specific timezone offset |
| `GOOGLECALENDAR_GET_CURRENT_USER` | Identifies the Google user connected to Calendar from the primary calendar resource |
| `GOOGLECALENDAR_LIST_BUILDINGS` | Lists all buildings for a Google Workspace customer account with full details including addresses, coordinates, and floor names |
| `GOOGLECALENDAR_LIST_CALENDAR_RESOURCES` | Retrieves calendar resources (such as conference rooms) from a Google Workspace domain using the Admin SDK Directory API |
| `GOOGLECALENDAR_LIST_CALENDARS` | Lists calendars accessible through the connected user's CalendarList, returning IDs and user-specific metadata such as access role, color, visibility, |
| `GOOGLECALENDAR_PATCH_CALENDAR` | Partially updates (PATCHes) an existing Google Calendar, modifying only the fields provided |
| `GOOGLECALENDAR_PATCH_EVENT` | Update specified fields of an existing event in a Google Calendar using patch semantics (array fields like `attendees` are fully replaced if provided) |
| `GOOGLECALENDAR_QUICK_ADD` | Parses natural language text to quickly create a basic Google Calendar event with its title, date, and time, suitable for simple scheduling; does not |
| `GOOGLECALENDAR_REMOVE_ATTENDEE` | Removes an attendee from a specified event in a Google Calendar; the calendar and event must exist |
| `GOOGLECALENDAR_SETTINGS_GET` | Tool to return a single user setting for the authenticated user |
| `GOOGLECALENDAR_SETTINGS_LIST` | Returns all user settings for the authenticated user |
| `GOOGLECALENDAR_SETTINGS_WATCH` | Watch for changes to Settings resources |
| `GOOGLECALENDAR_UPDATE_EVENT` | Updates an existing event in Google Calendar |
