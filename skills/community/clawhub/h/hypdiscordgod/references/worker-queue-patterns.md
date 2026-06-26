# Worker and Queue Patterns

Use this reference when webhooks or APIs should enqueue work for Discord-side processing.

## Preferred Flow

1. API receives webhook
2. API validates auth/signature
3. API persists job record
4. Worker polls or consumes queued jobs
5. Worker performs Discord-side action
6. Worker marks success/failure with retry metadata

## Good Uses

- webhook-triggered announcements
- moderation sync tasks
- external platform events that should not block HTTP responses

## Safe Rules

- make jobs idempotent where possible
- persist attempt count and last error
- cap retries or dead-letter failed jobs
- keep provider-specific payload normalization separate from job execution
