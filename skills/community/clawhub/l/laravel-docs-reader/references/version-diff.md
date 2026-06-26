# Laravel Version Diff (10 / 11 / 12)

## Overview

This document highlights the key differences between Laravel 10, 11, and 12.

---

## Authentication

| Feature | Laravel 10 | Laravel 11 | Laravel 12 |
|---------|-----------|-----------|-----------|
| Auth Scaffolding | `laravel new --auth` (built-in) | Removed | Use Breeze |
| Recommended Auth | `laravel/breeze` | `laravel/breeze` | `laravel/breeze` (minimal) |
| API Auth | Sanctum (separate) | Sanctum | First-party |
| Session Guard | `config/auth.php` | `config/auth.php` | Still needed |
| Login Rate Limit | `Auth::attempt()` throttled | Kernel throttling | Rate limiter |

**Laravel 11+ Migration**: Run `composer require laravel/breeze && php artisan breeze:install`

---

## Routing

| Feature | Laravel 10 | Laravel 11 | Laravel 12 |
|---------|-----------|-----------|-----------|
| Route Files | `routes/web.php`, `routes/api.php` | `routes/web.php`, `routes/api.php` | Same |
| Route Registration | `RouteServiceProvider` (boot) | `bootstrap/app.php` | `bootstrap/app.php` |
| Route Config (views) | `Route::view()` in routes | `Route::view()` in routes | Same |
| Rate Limiting | `throttle` middleware in Kernel | `throttle:60,1` middleware | Rate limiter API |

**Laravel 11+**: Rate limiting now configured in `bootstrap/app.php`:
```php
->withRouting(
    web: __DIR__.'/../routes/web.php',
    api: __DIR__.'/../routes/api.php',
    commands: __DIR__.'/../routes/console.php',
)
->withMiddleware(function (Middleware $m) {
    $m->throttleApi();
})
```

---

## Middleware

| Feature | Laravel 10 | Laravel 11 | Laravel 12 |
|---------|-----------|-----------|-----------|
| Registration | `app/Http/Kernel.php` | `bootstrap/app.php` | `bootstrap/app.php` |
| Middleware Groups | `$middlewareGroups` | `withMiddleware()` | `withMiddleware()` |
| Aliases | `$middlewareAliases` | `->alias()` | `->alias()` |
| Priority | `$middlewarePriority` | No priority (auto) | Same |

**Laravel 11+ Registration**:
```php
// bootstrap/app.php
->withMiddleware(function (Middleware $m) {
    $m->web(append: [CheckAge::class]);
    $m->api(prepend: [JwtAuth::class]);
    $m->alias(['admin' => CheckAdmin::class]);
})
```

---

## Exception Handling

| Feature | Laravel 10 | Laravel 11 | Laravel 12 |
|---------|-----------|-----------|-----------|
| Handler File | `app/Exceptions/Handler.php` | `bootstrap/app.php` (inline) | `bootstrap/app.php` |
| Custom Render | `render($request, $e)` | `render($request, $e)` | Same |
| Custom Report | `report($e)` | `report($e)` | Same |

**Laravel 11+ Handler**:
```php
// bootstrap/app.php
->withExceptions(function (Exceptions $ex) {
    $ex->report(function (Throwable $e) {
        // Custom reporting
    });
    $ex->render(function (NotFoundHttpException $e) {
        return response()->json(['error' => 'Not found'], 404);
    });
})
```

---

## Console / Scheduling

| Feature | Laravel 10 | Laravel 11 | Laravel 12 |
|---------|-----------|-----------|-----------|
| Scheduler Definition | `app/Console/Kernel.php` | `routes/console.php` | `routes/console.php` |
| Kernel (artisan commands) | `app/Console/Kernel.php` | `app/Console/Commands/` (dropped Kernel) | `app/Console/Commands/` |
| Artisan Boot | `boot()` in Kernel | Auto-discovery | Auto-discovery |

**Laravel 11+ Scheduling** (`routes/console.php`):
```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('emails:send')->dailyAt('09:00');
Schedule::job(new ProcessReports)->everyFiveMinutes();
```

---

## Broadcasting

| Feature | Laravel 10 | Laravel 11 | Laravel 12 |
|---------|-----------|-----------|-----------|
| Channels File | `routes/channels.php` | `routes/channels.php` | `routes/channels.php` |
| Channel Registration | `Broadcast::channel()` in channels.php | Same | Same |
| Pusher Config | `config/broadcasting.php` | `config/broadcasting.php` | Same |

---

## Configuration

| Feature | Laravel 10 | Laravel 11 | Laravel 12 |
|---------|-----------|-----------|-----------|
| Config Path | `config/` (40+ files) | `config/` (reduced) | `config/` (minimal) |
| Environment | `.env` | `.env` | `.env` |
| Bootstrap | `bootstrap/app.php` | Streamlined | Further streamlined |
| Service Providers | `config/app.php` providers | Auto-discovery | Auto-discovery |

---

## Database / Migrations

| Feature | Laravel 10 | Laravel 11 | Laravel 12 |
|---------|-----------|-----------|-----------|
| Foreign Keys | `$table->foreignId()` (7+) | Same | Same |
| Soft Deletes | `$table->softDeletes()` | Same | Same |
| Index Naming | Manual or `unique()` | Same | Same |

---

## Deprecated Features in 11+

- `laravel new --auth` (use Breeze)
- `app/Http/Kernel.php` (use `bootstrap/app.php`)
- `app/Console/Kernel.php` for scheduling (use `routes/console.php`)
- `routes/web.php` for API routes (use `routes/api.php`)
- `assertStatus()` in favor of `assertOk()` for redirects

---

## Deprecated Features in 12+

- `@php` directive (use full PHP file includes)
- `Route::matched()` callback
- `assertRedirectedTo()` (use `assertRedirect()` then `getSession()->get()`)

---

## Migration Checklist (10 → 11 → 12)

### 10 → 11
- [ ] Replace `app/Http/Kernel.php` with `bootstrap/app.php` middleware registration
- [ ] Replace `app/Console/Kernel.php` scheduling with `routes/console.php`
- [ ] Move exception handling from `Handler.php` to `bootstrap/app.php`
- [ ] Use Breeze instead of built-in `make:auth`
- [ ] Run `php artisan about` to check new config keys

### 11 → 12
- [ ] Update `laravel/framework` to `^12.0`
- [ ] Run `composer update`
- [ ] Review `php artisan about` for config changes
- [ ] Check for updated deprecation warnings in tests
