# Version Detection Logic

## Overview

When this skill runs against a Laravel project, it auto-detects the Laravel version using the following priority:

## Detection Priority

### 1. composer.json (Recommended)

```json
{
  "require": {
    "laravel/framework": "^12.0"
  }
}
```

Detection logic:
```php
$composer = file_get_contents('composer.json');
$data = json_decode($composer, true);
$laravelVersion = $data['require']['laravel/framework'] ?? null;
// Extract major version: "^12.0" → 12
preg_match('/\^?(\d+)/', $laravelVersion, $m);
$major = (int) $m[1]; // e.g. 12
```

### 2. artisan --version

```bash
$ php artisan --version
Laravel Framework 11.x.x
```

Detection logic:
```php
$output = shell_exec('php artisan --version');
preg_match('/Laravel Framework (\d+)/', $output, $m);
$major = (int) ($m[1] ?? 12);
```

### 3. Application.php VERSION constant

```php
// vendor/laravel/framework/src/Illuminate/Foundation/Application.php
const VERSION = '12.0.0';
```

Detection logic:
```php
$appFile = 'vendor/laravel/framework/src/Illuminate/Foundation/Application.php';
$content = file_get_contents($appFile);
preg_match('/const VERSION = \'(\d+)/', $content, $m);
$major = (int) ($m[1] ?? 12);
```

---

## CLI Usage

```bash
# Detect current project
php laradoc.php version

# Detect specific path
php laradoc.php version /path/to/project

# Show default
php laradoc.php current
```

---

## Version Mapping

| Composer Version | Artisan Output | Detected Major |
|-----------------|---------------|----------------|
| `^12.0` | Laravel Framework 12.x | 12 |
| `^11.0` | Laravel Framework 11.x | 11 |
| `^10.0` | Laravel Framework 10.x | 10 |

---

## Agent Behavior

When the agent processes a request:

1. Run `version_detect()` on the project root
2. If detected ≠ default (12), add a note to the response:
   > "Note: Your project uses Laravel {detected}, but this default is Laravel 12. Some features shown may differ."
3. All code examples use the detected version's syntax

---

## Fallback

If no Laravel project is found (e.g. running in an empty directory):
- Default to **Laravel 12**
- No version warning shown
