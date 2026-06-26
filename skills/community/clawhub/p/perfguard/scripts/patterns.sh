#!/usr/bin/env bash
# PerfGuard -- Performance Anti-Pattern Detection Patterns
# Each pattern: REGEX | SEVERITY | CHECK_ID | DESCRIPTION | RECOMMENDATION
#
# Categories: DATABASE, JAVASCRIPT, PYTHON, GENERAL
# Severities: critical, high, medium, low
# Patterns are grep -E compatible (extended regex)

set -euo pipefail

# ═══════════════════════════════════════════════════════════════════════════════
# DATABASE / ORM PATTERNS
# ═══════════════════════════════════════════════════════════════════════════════

# ─── N+1 Query Detection ────────────────────────────────────────────────────
# Detect patterns where queries are executed inside loops

DB_NPLUS1_PATTERNS=(
  'for\s+.*\bin\b.*\.all\(\)|critical|DB_NPLUS1_LOOP_QUERY|N+1 query: iterating over queryset inside a loop -- each iteration triggers a query|Use select_related() or prefetch_related() to eager-load related objects'
  'for\s+.*\bin\b.*\.objects\.|critical|DB_NPLUS1_OBJECTS|N+1 query: Django ORM query inside loop -- triggers a database hit per iteration|Fetch all needed data in a single queryset with select_related/prefetch_related'
  'for\s+.*\bin\b.*\.query\(|critical|DB_NPLUS1_RAW_QUERY|N+1 query: raw query executed inside a loop|Batch queries outside the loop or use a single JOIN query'
  '\.each\s*do.*\.find\(|critical|DB_NPLUS1_RAILS_FIND|N+1 query: Rails .find() inside .each loop|Use .includes() or .eager_load() to preload associations'
  '\.each\s*do.*\.where\(|critical|DB_NPLUS1_RAILS_WHERE|N+1 query: Rails .where() inside .each loop|Batch the query outside the loop using .includes() or .pluck()'
  '\.forEach.*await.*find|critical|DB_NPLUS1_JS_FOREACH|N+1 query: await find/query inside forEach loop|Collect IDs and use a single query with $in or WHERE IN'
  'for\s*\(.*await.*\.find|critical|DB_NPLUS1_JS_FOR|N+1 query: await database call inside for loop|Use Promise.all() with batched queries or a single bulk query'
  'for\s*\(.*\.execute\(|critical|DB_NPLUS1_EXECUTE|N+1 query: execute() called inside a for loop|Batch queries or use executemany() for bulk operations'
)

# ─── SELECT * Patterns ──────────────────────────────────────────────────────

DB_SELECT_STAR_PATTERNS=(
  'SELECT\s+\*\s+FROM|high|DB_SELECT_STAR|SELECT * fetches all columns -- wastes bandwidth and memory|Select only the columns you need: SELECT col1, col2 FROM table'
  '\.all\(\)\s*$|high|DB_ORM_ALL|Fetching all records without filtering or limiting|Add .filter(), .limit(), or select specific fields with .values()/only()'
  'Model\.find\(\s*\)|high|DB_FIND_ALL|Fetching all records without conditions|Add conditions: Model.find({ where: { ... } }) or use pagination'
  'findAll\(\s*\)|high|DB_FINDALL_NO_FILTER|findAll() without filters retrieves entire table|Add where clause and limit: findAll({ where: {...}, limit: 100 })'
)

# ─── Missing Eager Loading ──────────────────────────────────────────────────

DB_EAGER_LOADING_PATTERNS=(
  '\.objects\.filter\(.*__.*\)|critical|DB_DJANGO_NO_SELECT_RELATED|Django queryset traverses relation without select_related() -- causes N+1|Add .select_related() or .prefetch_related() for related object lookups'
  'ForeignKey\(|medium|DB_DJANGO_FK_HINT|ForeignKey detected -- ensure related querysets use select_related()|Use .select_related("field") when accessing this ForeignKey in queries'
  'has_many\s|medium|DB_RAILS_HAS_MANY_HINT|Rails has_many association -- ensure queries use .includes()|Use .includes(:association) when loading related records in bulk'
  'belongs_to\s|medium|DB_RAILS_BELONGS_TO_HINT|Rails belongs_to association -- ensure queries use .includes()|Use .includes(:association) to prevent N+1 on parent lookups'
  '@ManyToOne|medium|DB_JPA_MANY_TO_ONE|JPA @ManyToOne without fetch strategy -- defaults to EAGER which may cause unexpected queries|Set fetch = FetchType.LAZY and use JOIN FETCH in JPQL when needed'
  '@OneToMany|medium|DB_JPA_ONE_TO_MANY|JPA @OneToMany without @BatchSize -- risks N+1 on collection access|Add @BatchSize(size=25) or use JOIN FETCH in your JPQL query'
  'createQueryBuilder\(|medium|DB_TYPEORM_QB_HINT|TypeORM QueryBuilder -- ensure joins are used for related entities|Use .leftJoinAndSelect() to eager-load relations in a single query'
)

# ─── Unbounded Queries ──────────────────────────────────────────────────────

DB_UNBOUNDED_PATTERNS=(
  'SELECT[[:space:]].*FROM[[:space:]]|high|DB_UNBOUNDED_SELECT|SQL query without LIMIT clause -- may return millions of rows|Add LIMIT clause: SELECT ... FROM table LIMIT 100'
  '\.find\(\{[^}]*\}\)\s*$|high|DB_UNBOUNDED_FIND|Database find() without limit -- may return entire collection|Add .limit() or pagination: .find({}).limit(100).skip(offset)'
  '\.objects\.all\(\)\s*$|high|DB_DJANGO_UNBOUNDED|Django queryset .all() without slicing or limit|Use slicing [:100] or .iterator() for large querysets'
  '\.fetchall\(\)|high|DB_FETCHALL|fetchall() loads entire result set into memory|Use fetchmany(size) or iterate with fetchone() for large results'
  '\.to_list\(\)|high|DB_MONGO_TO_LIST|MongoDB .to_list() loads entire cursor into memory|Use async for to iterate, or pass a length limit to to_list()'
)

# ─── SQL String Concatenation ───────────────────────────────────────────────

DB_SQL_CONCAT_PATTERNS=(
  '\+\s*["\x27].*SELECT|critical|DB_SQL_CONCAT_SELECT|String concatenation in SQL query -- SQL injection risk and prevents query plan caching|Use parameterized queries: cursor.execute("SELECT ... WHERE id = %s", (id,))'
  'f["\x27].*SELECT.*FROM|critical|DB_SQL_FSTRING|Python f-string in SQL -- prevents plan caching and risks injection|Use parameterized queries instead of f-strings in SQL'
  '\$\{.*\}.*SELECT|critical|DB_SQL_TEMPLATE_LIT|Template literal in SQL query -- prevents plan caching|Use parameterized queries: db.query("SELECT ... WHERE id = $1", [id])'
  '\.format\(.*SELECT|critical|DB_SQL_FORMAT|String .format() in SQL query -- prevents plan caching|Use parameterized queries instead of .format() for SQL'
  '\.raw\s*\(\s*f["\x27]|critical|DB_ORM_RAW_FSTRING|ORM raw() with f-string interpolation|Use parameterized raw queries: Model.objects.raw("... WHERE id = %s", [id])'
)

# ─── Sequential / Unbatched Queries ─────────────────────────────────────────

DB_SEQUENTIAL_PATTERNS=(
  '\.save\(\).*\n.*\.save\(\)|medium|DB_SEQUENTIAL_SAVES|Multiple sequential .save() calls -- each triggers a database round-trip|Use bulk_create(), bulk_update(), or a transaction for batch operations'
  'INSERT INTO.*\n.*INSERT INTO|medium|DB_SEQUENTIAL_INSERTS|Multiple sequential INSERT statements|Use a single INSERT with multiple VALUES or bulk insert API'
  'UPDATE.*\n.*UPDATE.*SET|medium|DB_SEQUENTIAL_UPDATES|Multiple sequential UPDATE statements|Combine into a single UPDATE or use bulk update operations'
)

# ═══════════════════════════════════════════════════════════════════════════════
# JAVASCRIPT / TYPESCRIPT PATTERNS
# ═══════════════════════════════════════════════════════════════════════════════

# ─── Await in Loop ──────────────────────────────────────────────────────────

JS_ASYNC_PATTERNS=(
  'for\s*\(.*await\s|critical|JS_AWAIT_IN_FOR|await inside for loop -- runs async operations sequentially instead of in parallel|Collect promises and use Promise.all(): const results = await Promise.all(items.map(fn))'
  'for\s+.*of.*await\s|critical|JS_AWAIT_IN_FOR_OF|await inside for...of loop -- sequential async operations|Use Promise.all() with .map() for parallel execution'
  '\.forEach\(.*await\s|critical|JS_AWAIT_IN_FOREACH|await inside forEach -- forEach does not await promises, causing silent failures|Use for...of with await, or Promise.all() with .map()'
  'while\s*\(.*await\s|high|JS_AWAIT_IN_WHILE|await inside while loop -- sequential async, may cause long blocking|Consider batching or streaming approach instead of sequential awaits'
)

# ─── Missing Promise.all ────────────────────────────────────────────────────

JS_PROMISE_PATTERNS=(
  'await\s+\w+\(.*\)\s*;\s*\n\s*await\s+\w+\(|high|JS_SEQUENTIAL_AWAIT|Multiple sequential awaits that may be independent|If operations are independent, use Promise.all([op1(), op2()]) for parallel execution'
  'await\s+fetch\(.*\)\s*;\s*\n\s*await\s+fetch\(|high|JS_SEQUENTIAL_FETCH|Multiple sequential fetch calls|Use Promise.all() to fetch in parallel: await Promise.all([fetch(url1), fetch(url2)])'
)

# ─── Sync File I/O ──────────────────────────────────────────────────────────

JS_SYNC_IO_PATTERNS=(
  'readFileSync\s*\(|high|JS_SYNC_READ|readFileSync blocks the event loop -- stalls all concurrent requests|Use fs.promises.readFile() or fs.readFile() with callback'
  'writeFileSync\s*\(|high|JS_SYNC_WRITE|writeFileSync blocks the event loop|Use fs.promises.writeFile() or fs.writeFile() with callback'
  'appendFileSync\s*\(|high|JS_SYNC_APPEND|appendFileSync blocks the event loop|Use fs.promises.appendFile() for non-blocking file append'
  'mkdirSync\s*\(|medium|JS_SYNC_MKDIR|mkdirSync blocks the event loop|Use fs.promises.mkdir() for non-blocking directory creation'
  'existsSync\s*\(|medium|JS_SYNC_EXISTS|existsSync blocks the event loop|Use fs.promises.access() or fs.promises.stat() for non-blocking checks'
  'readdirSync\s*\(|medium|JS_SYNC_READDIR|readdirSync blocks the event loop|Use fs.promises.readdir() for non-blocking directory listing'
)

# ─── JSON Clone / Inefficient Serialization ─────────────────────────────────

JS_SERIALIZATION_PATTERNS=(
  'JSON\.parse\s*\(\s*JSON\.stringify\s*\(|medium|JS_JSON_CLONE|JSON.parse(JSON.stringify()) for deep clone is slow and drops functions/dates/undefined|Use structuredClone(), lodash.cloneDeep(), or a dedicated clone library'
  'JSON\.stringify\(.*\)\s*\.length|medium|JS_STRINGIFY_LENGTH|Stringifying entire object just to check size is wasteful|Use sizeof or object-sizeof package for memory estimation'
)

# ─── Unbounded Array Operations ─────────────────────────────────────────────

JS_ARRAY_PATTERNS=(
  '\.map\s*\(\s*async|high|JS_ASYNC_MAP_NO_AWAIT|async callback in .map() without Promise.all -- promises created but not awaited|Wrap in Promise.all(): await Promise.all(items.map(async (item) => ...))'
  '\.filter\(.*\)\.map\(.*\)\.filter\(|medium|JS_CHAINED_ARRAY_OPS|Multiple chained array operations -- iterates the array multiple times|Use .reduce() or a single loop to combine filter+map operations'
)

# ─── Memory Leaks ───────────────────────────────────────────────────────────

JS_MEMORY_PATTERNS=(
  'addEventListener\s*\(|high|JS_EVENT_NO_CLEANUP|addEventListener without corresponding removeEventListener -- potential memory leak|Store listener reference and call removeEventListener in cleanup/unmount'
  'setInterval\s*\(|high|JS_INTERVAL_NO_CLEAR|setInterval without clearInterval -- runs indefinitely and leaks memory|Store interval ID and call clearInterval in cleanup: const id = setInterval(...); clearInterval(id)'
  'new\s+EventEmitter|medium|JS_EMITTER_LEAK|EventEmitter without setMaxListeners or removeListener -- potential memory leak|Call .setMaxListeners() and .removeListener() in cleanup paths'
)

# ─── React Performance ──────────────────────────────────────────────────────

JS_REACT_PATTERNS=(
  'import\s+_\s+from\s+["\x27]lodash["\x27]|high|JS_LODASH_FULL|Importing entire lodash bundle (~70KB min) instead of specific functions|Import specific functions: import debounce from "lodash/debounce"'
  'import\s+\{.*\}\s+from\s+["\x27]lodash["\x27]|high|JS_LODASH_NAMED|Named imports from lodash still pull entire bundle without babel plugin|Use lodash-es or import from "lodash/functionName" for tree-shaking'
  'import\s+moment\s+from|medium|JS_MOMENT_IMPORT|moment.js is 300KB+ and mutable -- consider lighter alternatives|Use date-fns, dayjs, or native Intl/Temporal APIs instead'
)

# ─── Missing Pagination ────────────────────────────────────────────────────

JS_PAGINATION_PATTERNS=(
  'res\.json\s*\(\s*await.*\.find\(|high|JS_NO_PAGINATION|API response returns all query results without pagination|Add limit/offset or cursor-based pagination: .find().limit(20).skip(page*20)'
  'res\.send\s*\(\s*await.*\.findAll|high|JS_NO_PAGINATION_FINDALL|API response returns findAll() without pagination|Add limit and offset: .findAll({ limit: 20, offset: page * 20 })'
  'return.*\.find\(\s*\)|high|JS_RETURN_FIND_ALL|Returning all documents without pagination|Add pagination parameters: .find().limit(pageSize).skip(page * pageSize)'
)

# ─── Console in Production ──────────────────────────────────────────────────

JS_CONSOLE_PATTERNS=(
  'console\.log\s*\(|low|JS_CONSOLE_LOG|console.log left in code -- adds overhead and leaks info in production|Remove console.log or use a structured logger (winston, pino) with log levels'
  'console\.dir\s*\(|low|JS_CONSOLE_DIR|console.dir in code -- serializes entire objects for output|Remove console.dir or use a structured logger with appropriate levels'
  'console\.table\s*\(|low|JS_CONSOLE_TABLE|console.table in code -- expensive serialization for debug output|Remove console.table or gate behind a debug flag'
)

# ═══════════════════════════════════════════════════════════════════════════════
# PYTHON PATTERNS
# ═══════════════════════════════════════════════════════════════════════════════

# ─── Import / Module Patterns ───────────────────────────────────────────────

PY_IMPORT_PATTERNS=(
  'def\s+\w+\(.*\):\s*\n\s+import\s+(pandas|numpy|tensorflow|torch|scipy|sklearn|matplotlib)|medium|PY_HEAVY_IMPORT_IN_FUNC|Heavy module imported inside function -- re-imported on every call|Move heavy imports (pandas, numpy, etc.) to module level for one-time loading'
  'import\s+\*\s+from|medium|PY_WILDCARD_IMPORT|Wildcard import pulls entire module namespace into scope|Import only what you need: from module import specific_function'
)

# ─── String / Memory Patterns ───────────────────────────────────────────────

PY_STRING_PATTERNS=(
  'for\s+.*:\s*\n\s+\w+\s*\+=\s*["\x27]|medium|PY_STRING_CONCAT_LOOP|String concatenation with += in loop -- O(n^2) time complexity|Collect strings in a list and use "".join(parts) after the loop'
  'for\s+.*:\s*\n\s+\w+\s*=\s*\w+\s*\+\s*["\x27]|medium|PY_STRING_PLUS_LOOP|String + concatenation in loop -- creates new string each iteration|Use list append and "".join() for O(n) string building'
)

# ─── List vs Generator ──────────────────────────────────────────────────────

PY_GENERATOR_PATTERNS=(
  '\[\s*\w+\s+for\s+\w+\s+in\s+range\s*\(\s*\d{5,}|medium|PY_LARGE_LIST_COMP|Large list comprehension (100K+ items) consumes excessive memory|Use a generator expression: (x for x in range(...)) or process in chunks'
  '\.readlines\(\)|medium|PY_READLINES|.readlines() loads entire file into memory as a list|Iterate the file directly: for line in file: (uses lazy line-by-line reading)'
  '\.read\(\)\s*$|medium|PY_READ_WHOLE_FILE|.read() loads entire file contents into memory|Use chunked reading: for chunk in iter(lambda: f.read(8192), b"") or iterate lines'
)

# ─── Async Anti-Patterns ────────────────────────────────────────────────────

PY_ASYNC_PATTERNS=(
  'time\.sleep\s*\(|critical|PY_SLEEP_IN_ASYNC|time.sleep() blocks the event loop in async code|Use await asyncio.sleep() instead of time.sleep() in async functions'
  'requests\.(get|post|put|delete|patch)\s*\(|high|PY_SYNC_HTTP_IN_ASYNC|Synchronous requests library used -- blocks event loop if called from async code|Use aiohttp or httpx.AsyncClient for non-blocking HTTP in async code'
  'open\s*\(.*\)\s*as\s|high|PY_SYNC_FILE_IN_ASYNC|Synchronous file I/O -- blocks event loop in async context|Use aiofiles: async with aiofiles.open() as f: for non-blocking file I/O'
  'subprocess\.(run|call|check_output)\s*\(|high|PY_SYNC_SUBPROCESS|Synchronous subprocess call blocks the event loop|Use asyncio.create_subprocess_exec() or asyncio.create_subprocess_shell()'
)

# ─── Connection / Resource Patterns ─────────────────────────────────────────

PY_CONNECTION_PATTERNS=(
  'psycopg2\.connect\s*\(|high|PY_NO_CONN_POOL_PG|Direct psycopg2 connection without connection pooling|Use psycopg2.pool.ThreadedConnectionPool or SQLAlchemy connection pool'
  'pymysql\.connect\s*\(|high|PY_NO_CONN_POOL_MYSQL|Direct pymysql connection without connection pooling|Use a connection pool: SQLAlchemy create_engine() or DBUtils.PooledDB'
  'sqlite3\.connect\s*\(|medium|PY_SQLITE_DIRECT|Direct sqlite3 connection -- no pooling or WAL mode|Use SQLAlchemy for connection management or enable WAL mode for concurrency'
  'MongoClient\s*\(|medium|PY_MONGO_NO_POOL_HINT|MongoClient created -- ensure maxPoolSize is configured|Set maxPoolSize in connection string: MongoClient(uri, maxPoolSize=50)'
)

# ─── Regex in Loop ──────────────────────────────────────────────────────────

PY_REGEX_PATTERNS=(
  'for\s+.*:\s*\n\s+.*re\.(search|match|findall|sub)\s*\(|medium|PY_REGEX_IN_LOOP|Regex compiled inside loop -- recompiles pattern on every iteration|Compile regex outside loop: pattern = re.compile(...) then pattern.search()'
  'for\s+.*:\s*\n\s+.*re\.compile\s*\(|medium|PY_RECOMPILE_IN_LOOP|re.compile() inside loop -- compiles same pattern repeatedly|Move re.compile() before the loop and reuse the compiled pattern object'
)

# ═══════════════════════════════════════════════════════════════════════════════
# GENERAL PATTERNS (language-agnostic)
# ═══════════════════════════════════════════════════════════════════════════════

# ─── Retry / Timeout Patterns ───────────────────────────────────────────────

GEN_RETRY_PATTERNS=(
  'while\s*(true|True|\(true\)).*retry|high|GEN_UNBOUNDED_RETRY|Unbounded retry loop without backoff -- can overwhelm downstream services|Add exponential backoff with max retries: sleep(2^attempt * base_delay), max 5 retries'
  'retry.*while\s*(true|True)|high|GEN_RETRY_NO_BACKOFF|Retry loop without exponential backoff|Add exponential backoff and a maximum retry count to prevent infinite loops'
  'for.*retry.*<\s*\d+|medium|GEN_RETRY_NO_DELAY|Retry loop without delay between attempts|Add delay with exponential backoff: Math.min(1000 * 2^attempt, 30000)'
)

# ─── Missing Timeout ────────────────────────────────────────────────────────

GEN_TIMEOUT_PATTERNS=(
  'fetch\s*\([^)]*\)\s*$|high|GEN_FETCH_NO_TIMEOUT|fetch() without timeout -- can hang indefinitely on slow/down servers|Add AbortController with timeout: const controller = new AbortController(); setTimeout(...)'
  'requests\.(get|post)\s*\([^)]*\)\s*$|high|GEN_REQUESTS_NO_TIMEOUT|requests call without timeout -- can block indefinitely|Add timeout parameter: requests.get(url, timeout=30)'
  'http\.request\s*\(|high|GEN_HTTP_NO_TIMEOUT|HTTP request without explicit timeout|Set timeout option: { timeout: 30000 } or use AbortController'
  'axios\s*\.\s*(get|post|put|delete)\s*\([^)]*\)\s*$|medium|GEN_AXIOS_NO_TIMEOUT|axios call without explicit timeout|Configure timeout: axios.get(url, { timeout: 30000 })'
  'HttpClient|medium|GEN_HTTPCLIENT_TIMEOUT_HINT|HttpClient usage -- ensure connection and read timeouts are configured|Set connectTimeout and readTimeout on the HTTP client instance'
)

# ─── Polling Patterns ───────────────────────────────────────────────────────

GEN_POLLING_PATTERNS=(
  'setInterval\s*\(.*fetch|medium|GEN_POLLING_FETCH|Polling with setInterval+fetch -- wastes bandwidth and battery|Use WebSocket, Server-Sent Events, or webhook callbacks instead of polling'
  'while.*sleep.*request|medium|GEN_POLLING_SLEEP|Sleep-based polling loop -- wastes resources waiting|Use event-driven architecture: webhooks, message queues, or pub/sub'
  'schedule\.every\s*\(\s*\d+\s*\)\s*\.seconds|medium|GEN_POLLING_SCHEDULE|Frequent scheduled polling -- consider event-driven alternatives|Use webhooks or message queues if the data source supports push notifications'
)

# ─── Hardcoded Delays ───────────────────────────────────────────────────────

GEN_DELAY_PATTERNS=(
  'sleep\s*\(\s*\d+\s*\)|low|GEN_HARDCODED_SLEEP|Hardcoded sleep/delay -- may be too long or too short in different environments|Use configurable timeouts or event-based waiting instead of fixed delays'
  'setTimeout\s*\(.*,\s*\d{4,}\s*\)|low|GEN_LONG_TIMEOUT|Long setTimeout (1s+) -- may indicate polling or race condition workaround|Use event listeners, promises, or MutationObserver instead of arbitrary delays'
  'Thread\.sleep\s*\(\s*\d+\s*\)|low|GEN_THREAD_SLEEP|Thread.sleep() with hardcoded delay|Use configurable delay or event-based waiting'
)

# ─── Missing Cache / Memoization ────────────────────────────────────────────

GEN_CACHE_PATTERNS=(
  'def\s+fibonacci\s*\(|medium|GEN_RECURSIVE_NO_MEMO|Recursive function (fibonacci) without memoization -- exponential time complexity|Add @functools.lru_cache or manual memoization for recursive functions'
  'function\s+fibonacci\s*\(|medium|GEN_RECURSIVE_NO_MEMO_JS|Recursive function without memoization|Use a cache Map or lodash.memoize() for recursive functions'
  'def\s+factorial\s*\(|medium|GEN_RECURSIVE_FACTORIAL|Recursive factorial without memoization|Add @functools.lru_cache decorator for memoized recursion'
)

# ─── Large Payload / Streaming ──────────────────────────────────────────────

GEN_PAYLOAD_PATTERNS=(
  'JSON\.stringify\s*\(.*\)\s*$|medium|GEN_LARGE_STRINGIFY|JSON.stringify on potentially large object -- blocks event loop during serialization|Use streaming JSON serialization (JSONStream, fast-json-stringify) for large payloads'
  'json\.dumps\s*\(.*\)\s*$|medium|GEN_LARGE_JSON_DUMPS|json.dumps on potentially large object|Use ijson or orjson for streaming/fast serialization of large data'
  'yaml\.dump\s*\(|medium|GEN_YAML_DUMP|YAML serialization can be very slow for large objects|Use yaml.CSafeLoader/CSafeDumper or consider JSON for large payloads'
)
