# Troubleshooting

## 401 Unauthorized

- `NOTION_API_KEY` is missing, expired, or wrong
- The CLI is using a different token than the shell environment

## 403 Forbidden

- The integration lacks the required read or write capability
- OAuth token scope does not cover the requested operation

## 404 Not Found

- The database or page is not shared with the integration
- A `database_id` was used where `data_source_id` is required
- The page ID was copied incorrectly

## Wrong Row Updated

- The match was based on title only
- There were duplicate titles in the same time window
- Property names were assumed instead of retrieved

## Calendar View Looks Wrong

- The database view is pointed at a different date property
- All-day versus timed values were mixed
- The timezone used in the API payload does not match the user's expectation

## Performance Problems

- Query windows are too broad
- Too many heavy properties are being returned
- The database schema should be trimmed or queried with narrower filters
