---
name: naming-forge
version: 1.0.0
description: >
  Solves the hardest problem in computer science: naming things. Uses
  linguistic principles, codebase conventions, and semantic analysis to
  generate precise, consistent, discoverable names for variables, functions,
  types, files, routes, database tables, and everything else that needs
  a name. Because 'temp2_final_v3' is not a name — it's a cry for help.
author: J. DeVere Cooley
category: everyday-tools
tags:
  - naming
  - conventions
  - readability
  - linguistics
metadata:
  openclaw:
    emoji: "⚒️"
    os: ["darwin", "linux", "win32"]
    cost: free
    requires_api: false
    tags:
      - zero-dependency
      - everyday
      - code-quality
---

# Naming Forge

> "There are only two hard things in Computer Science: cache invalidation and naming things." — Phil Karlton

## What It Does

You need to name a function. It takes a list of orders, filters out cancelled ones, groups them by customer, and returns the totals. You stare at the cursor. `processOrders`? Too vague. `filterAndGroupAndSummarizeOrdersByCustomerExcludingCancelled`? Too long. `getOrderSummary`? Misleading — it does more than "get."

Naming Forge generates names that are **precise** (says what it does), **consistent** (matches your codebase's conventions), **discoverable** (other developers can guess what to search for), and **proportional** (name length matches scope importance).

## The Five Laws of Good Names

### Law 1: A Name Should Be a Contract
The name is a promise. `calculateTotal` promises it calculates and returns a total. If it also sends an email, the name is a lie.

```
BAD:  updateUser()          — does it update the DB? The UI? Both? What fields?
GOOD: saveUserProfile()     — saves the user's profile (to persistent storage)
GOOD: refreshUserDisplay()  — updates what the user sees on screen
```

### Law 2: Scope Determines Length
Small scope → short name. Large scope → descriptive name. A loop variable can be `i`. A public API method should not be.

| Scope | Name Length | Example |
|---|---|---|
| Loop variable (3 lines) | 1-2 chars | `i`, `ch`, `tx` |
| Local variable (10-20 lines) | 1 word | `total`, `users`, `query` |
| Private method (module scope) | 1-2 words | `parseInput`, `buildQuery` |
| Public method (cross-module) | 2-3 words | `calculateOrderTotal`, `validateAddress` |
| Exported constant (global) | 2-4 words | `MAX_RETRY_ATTEMPTS`, `DEFAULT_TIMEOUT_MS` |

### Law 3: Verbs for Actions, Nouns for Things
Functions do things → verbs. Variables hold things → nouns. Types describe things → nouns/adjectives.

```
FUNCTIONS (verb-first):
├── get/fetch/load    → retrieves data (getSessions, fetchUser, loadConfig)
├── set/update/save   → modifies data (setTheme, updateProfile, saveOrder)
├── create/build/make → constructs new things (createUser, buildQuery, makeHandler)
├── delete/remove     → eliminates things (deleteAccount, removeItem)
├── is/has/can/should → returns boolean (isValid, hasPermission, canEdit)
├── parse/format/transform → converts between formats (parseJSON, formatDate)
├── validate/check/verify → confirms correctness (validateEmail, checkStatus)
└── handle/process/on → responds to events (handleClick, processPayment, onSubmit)

VARIABLES (noun/adjective):
├── Collections: plural nouns (users, orders, activeConnections)
├── Singles: singular nouns (user, order, currentConnection)
├── Booleans: is/has/can prefix (isLoading, hasErrors, canSubmit)
├── Counts: noun + Count (retryCount, errorCount, userCount)
└── Maps/Indices: noun + By + Key (userById, ordersByDate)
```

### Law 4: Consistency Beats Cleverness
If your codebase says `fetchUser`, don't introduce `retrieveUser`. If it says `isValid`, don't introduce `checkValidity`. Match what exists.

```
CODEBASE AUDIT:
├── Existing pattern: fetch* for API calls → USE fetchOrders, NOT getOrders
├── Existing pattern: *Service for modules → USE PaymentService, NOT PaymentManager
├── Existing pattern: on* for handlers → USE onSubmit, NOT handleSubmit
└── Existing pattern: is* for booleans → USE isActive, NOT active or checkActive
```

### Law 5: Avoid Semantic Noise
Words that add length without adding meaning: `data`, `info`, `item`, `thing`, `object`, `value`, `manager`, `handler`, `processor`, `helper`, `utils`.

```
BAD:  userData, userInfo, userObject  → just "user"
BAD:  orderItem  → just "order" (unless distinguishing from order summary)
BAD:  StringHelper, DateUtils  → what do they actually do? Be specific.
GOOD: formatDate, parseCSV, slugify  → specific actions
```

## The Forge Process

```
INPUT: What does this thing do? (natural language description)
CONTEXT: What part of the codebase is this in?

Phase 1: SEMANTIC EXTRACTION
├── Extract the core action or concept from the description
├── Identify: Is this a function, variable, type, file, or route?
├── Identify: What's the scope? (local, module, public, global)
└── Identify: What domain vocabulary applies? (business terms, tech terms)

Phase 2: CONVENTION SCAN
├── Scan existing codebase for naming patterns:
│   ├── Verb preferences (get vs. fetch vs. load vs. retrieve)
│   ├── Noun preferences (User vs. Account vs. Profile)
│   ├── Casing convention (camelCase, snake_case, PascalCase, kebab-case)
│   ├── Prefix/suffix patterns (is*, *Service, *Controller, I* for interfaces)
│   └── Domain vocabulary already in use
├── Identify the dominant convention for this type of name
└── Flag any existing inconsistencies

Phase 3: CANDIDATE GENERATION
├── Generate 3-5 candidates following conventions
├── For each candidate, evaluate:
│   ├── Precision: Does the name accurately describe the thing?
│   ├── Consistency: Does it match existing patterns?
│   ├── Discoverability: Could a teammate guess this name?
│   ├── Proportionality: Is the length right for the scope?
│   └── Uniqueness: Does it conflict with any existing name?
├── Rank candidates by composite score
└── Flag tradeoffs between candidates

Phase 4: RECOMMENDATION
├── Top recommendation with rationale
├── Runner-up alternatives
├── Names to AVOID (and why)
└── If renaming: migration impact (how many references to update)
```

## Domain-Specific Naming

### API Routes / Endpoints

```
PATTERN: /resource/action or RESTful convention

GOOD:
├── GET    /users              → list users
├── GET    /users/:id          → get specific user
├── POST   /users              → create user
├── PUT    /users/:id          → replace user
├── PATCH  /users/:id          → partial update
├── DELETE /users/:id          → delete user
├── POST   /users/:id/verify   → action on user (verb as sub-resource)

BAD:
├── GET /getUsers              → verb in path (GET already implies "get")
├── POST /createNewUser        → redundant (POST already implies "create")
├── GET /user_list             → inconsistent casing, use /users
└── POST /doUserVerification   → too verbose, use /users/:id/verify
```

### Database Tables / Columns

```
TABLES:
├── Plural nouns: users, orders, payments (not user, order, payment)
├── Join tables: user_roles, order_items (alphabetical or parent_child)
├── Consistent casing: snake_case for SQL, camelCase for NoSQL (match your ORM)

COLUMNS:
├── Foreign keys: user_id, order_id (table_singular + _id)
├── Booleans: is_active, has_verified, can_edit (prefix with state verb)
├── Timestamps: created_at, updated_at, deleted_at (past_participle + _at)
├── Counts: login_count, retry_count (noun + _count)
└── Status: order_status, payment_state (entity + _status/_state)
```

### CSS Classes

```
PATTERN: BEM (block__element--modifier) or utility classes

GOOD:
├── .card__header--highlighted
├── .nav__link--active
├── .form__input--error
└── .btn--primary, .btn--disabled

BAD:
├── .redButton        → visual, not semantic
├── .leftSidebar      → positional, not semantic
├── .big              → relative to what?
└── .myComponent      → "my" adds nothing
```

### Environment Variables

```
PATTERN: SCREAMING_SNAKE_CASE, grouped by service

GOOD:
├── DATABASE_URL, DATABASE_POOL_SIZE
├── REDIS_HOST, REDIS_PORT, REDIS_PASSWORD
├── SMTP_HOST, SMTP_PORT, SMTP_FROM_ADDRESS
├── APP_SECRET_KEY, APP_DEBUG, APP_LOG_LEVEL

BAD:
├── db, DB             → too short, too ambiguous
├── databaseUrl        → wrong casing for env vars
├── MY_APP_SETTING     → "MY" adds nothing
└── ENABLE_FEATURE_X   → what feature? be specific
```

## Output Format

```
╔══════════════════════════════════════════════════════════════╗
║                      NAMING FORGE                           ║
║  Input: "function that takes a list of orders, filters      ║
║  out cancelled ones, groups by customer, returns totals"    ║
║  Scope: Public method in OrderService                       ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  RECOMMENDATION: summarizeActiveOrdersByCustomer             ║
║  ├── Precise: "summarize" = aggregate, "active" = not        ║
║  │   cancelled, "by customer" = grouping key                 ║
║  ├── Convention match: codebase uses *ByField pattern ✓      ║
║  ├── Discoverable: searching "order" + "customer" finds it ✓ ║
║  └── Proportional: 5 words for a public cross-module method ✓║
║                                                              ║
║  ALTERNATIVES:                                               ║
║  ├── getCustomerOrderTotals — shorter but loses "active"     ║
║  ├── aggregateOrdersByCustomer — "aggregate" is less common  ║
║  │   in this codebase (0 uses vs 12 uses of "summarize")     ║
║  └── calculateCustomerOrderSummary — "calculate" implies     ║
║      math; this is more filter + group                       ║
║                                                              ║
║  AVOID:                                                      ║
║  ├── processOrders — "process" is meaningless                ║
║  ├── getOrderData — "data" is noise                          ║
║  └── doOrderStuff — please                                   ║
╚══════════════════════════════════════════════════════════════╝
```

## When to Invoke

- When you're staring at a cursor trying to name something
- When you're about to name something `temp`, `data`, `result`, or `thing`
- When refactoring and you realize names no longer match behavior
- When reviewing code with misleading names
- When starting a new module and setting naming conventions
- When naming database tables, API endpoints, or environment variables

## Why It Matters

Names are the **primary documentation** of a codebase. Developers read names thousands of times a day. A precise name eliminates the need to read the implementation. A misleading name causes more damage than no name at all.

You'll spend 10 minutes agonizing over a name, or you'll spend 10 hours explaining what `processData` actually does. The Forge is faster than either.

Zero external dependencies. Zero API calls. Pure linguistic and codebase analysis.
