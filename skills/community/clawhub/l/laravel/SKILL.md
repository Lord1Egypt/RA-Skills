---
name: Laravel
slug: laravel
version: 1.0.1
description: Build robust Laravel apps avoiding Eloquent traps, queue failures, and auth pitfalls.
metadata: {"clawdbot":{"emoji":"🔴","requires":{"bins":["php","composer"]},"os":["linux","darwin","win32"]}}
---

## Quick Reference

| Topic | File |
|-------|------|
| N+1 queries, eager loading, accessors, observers | `eloquent.md` |
| Validation, middleware order, dependency injection | `controllers.md` |
| Job serialization, retries, failed jobs | `queues.md` |
| Guards, policies, gates, Sanctum tokens | `auth.md` |
| XSS escaping, components, slots | `blade.md` |
| Commands, scheduling, tinker | `artisan.md` |

## Critical Rules

- Eager load relationships — `with('posts')` not lazy `->posts` in loop (N+1)
- `preventLazyLoading()` in dev AppServiceProvider — crashes on N+1, catches early
- `env()` only in config files — returns null after `config:cache`
- `$fillable` whitelist fields — `$guarded = []` allows mass assignment attacks
- `find()` returns null — use `findOrFail()` to avoid null checks
- Job properties serialize models as ID — re-fetched on process, may be stale/deleted
- `route:cache` requires controller routes — closures break cached routes
- `DB::transaction()` doesn't catch `exit`/timeout — only exceptions roll back
- `RefreshDatabase` uses transactions — faster than `DatabaseMigrations`
- `{!! $html !!}` skips escaping — XSS vector, use `{{ }}` by default
- Middleware order matters — earlier middleware wraps later execution
- `required` validation passes empty string — use `required|filled` for content
- `firstOrCreate` persists immediately — `firstOrNew` returns unsaved model
- Route model binding uses `id` — override `getRouteKeyName()` for slug
