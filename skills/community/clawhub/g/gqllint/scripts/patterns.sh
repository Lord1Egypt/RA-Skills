#!/usr/bin/env bash
# GQLLint -- GraphQL Anti-Pattern & Security Definitions
# 90 patterns across 6 categories, 15 patterns each.
#
# Format per line:
#   REGEX|SEVERITY|CHECK_ID|DESCRIPTION|RECOMMENDATION
#
# Severity levels:
#   critical -- Immediate security or performance risk
#   high     -- Significant GraphQL problem requiring prompt attention
#   medium   -- Moderate concern that should be addressed in current sprint
#   low      -- Best practice suggestion or informational finding
#
# IMPORTANT: All regexes use POSIX ERE syntax (grep -E compatible).
# - Use [[:space:]] instead of \s
# - Use [[:alnum:]] instead of \w
# - NEVER use pipe (|) for alternation inside regex -- it conflicts with
#   the field delimiter. Use separate patterns or character classes instead.
# - Use \b-free alternatives where boundary assertions are unavailable
#
# Categories:
#   QD (Query Depth & Complexity) -- 15 patterns (QD-001 to QD-015)
#   RN (Resolver N+1)            -- 15 patterns (RN-001 to RN-015)
#   OF (Over/Under Fetching)     -- 15 patterns (OF-001 to OF-015)
#   RL (Rate Limiting & Auth)    -- 15 patterns (RL-001 to RL-015)
#   SD (Schema Design)           -- 15 patterns (SD-001 to SD-015)
#   CQ (Client Query Safety)     -- 15 patterns (CQ-001 to CQ-015)

set -euo pipefail

# ============================================================================
# 1. QUERY DEPTH & COMPLEXITY (QD-001 through QD-015)
#    Detects unbounded query depth, no max complexity limit, deeply nested
#    fragments, recursive fragment spreads, no query cost analysis,
#    introspection enabled in production.
# ============================================================================

declare -a GQLLINT_QD_PATTERNS=()

GQLLINT_QD_PATTERNS+=(
  # QD-001: Introspection enabled in production configuration
  'introspection[[:space:]]*:[[:space:]]*true|critical|QD-001|GraphQL introspection enabled (exposes full schema in production)|Disable introspection in production: introspection: process.env.NODE_ENV !== "production"'

  # QD-002: No depthLimit configured on GraphQL server
  'createServer\([[:space:]]*\{[^}]*\}[[:space:]]*\)|high|QD-002|GraphQL server created without depthLimit configuration|Add depthLimit middleware: depthLimit(10) to prevent deeply nested query attacks'

  # QD-003: No query complexity limit configured
  'ApolloServer\([[:space:]]*\{[^}]*validationRules|medium|QD-003|ApolloServer without query complexity validation rule|Add createComplexityRule({ maximumComplexity: 1000 }) to validationRules array'

  # QD-004: Deeply nested fragment definition (4+ levels)
  'fragment[[:space:]][[:alnum:]]+[[:space:]]on[[:space:]][[:alnum:]]+[[:space:]]*\{[^}]*\{[^}]*\{[^}]*\{|high|QD-004|Deeply nested GraphQL fragment (4+ levels deep)|Flatten fragment nesting to reduce query depth; split into smaller focused fragments'

  # QD-005: Fragment spread inside fragment (recursive risk)
  'fragment[[:space:]][[:alnum:]]+[[:space:]]on[[:space:]][[:alnum:]]+[[:space:]]*\{[^}]*\.\.\.[[:alnum:]]|high|QD-005|Fragment spread inside fragment definition (potential recursion)|Avoid fragment-within-fragment patterns to prevent recursive query depth escalation'

  # QD-006: No queryComplexity or costAnalysis plugin
  'new[[:space:]]ApolloServer\([[:space:]]*\{[^}]*plugins[[:space:]]*:[[:space:]]*\[|low|QD-006|ApolloServer plugins array without query cost analysis plugin|Add a query cost analysis plugin to reject expensive queries before execution'

  # QD-007: Nested mutation with unbounded depth
  'type[[:space:]]Mutation[[:space:]]*\{[^}]*:[[:space:]]*\[[[:alnum:]]+\]|medium|QD-007|Mutation returning a list type without depth restriction|Limit mutation response nesting and add depthLimit to prevent deep traversal on mutations'

  # QD-008: Schema allows self-referential types without depth guard
  'type[[:space:]][[:alnum:]]+[[:space:]]*\{[^}]*:[[:space:]]*\[?[[:alnum:]]+\]?[^}]*\}|low|QD-008|Type definition with potential self-referential field|Review self-referential types for unbounded depth; add @complexity directives or depth limits'

  # QD-009: Subscription without depth limiting
  'type[[:space:]]Subscription[[:space:]]*\{|medium|QD-009|Subscription type defined without visible depth limiting|Apply depthLimit to subscriptions to prevent deeply nested real-time data leaks'

  # QD-010: No maxDepth in graphql-shield or similar
  'allow[[:space:]]*\([[:space:]]*\)|medium|QD-010|GraphQL shield allow() rule without depth constraint|Add depth check to permission rules: and(isAuthenticated, maxDepth(5))'

  # QD-011: enableIntrospection set to true explicitly
  'enableIntrospection[[:space:]]*:[[:space:]]*true|critical|QD-011|enableIntrospection explicitly set to true|Set enableIntrospection to false in production to hide schema from attackers'

  # QD-012: Query nesting exceeds 3 curly brace levels in string
  'query[[:space:]][[:alnum:]]*[[:space:]]*\{[^}]*\{[^}]*\{[^}]*\{|high|QD-012|Query string with 4+ nesting levels detected|Reduce query depth; flatten nested selections or use separate queries'

  # QD-013: No validation rules array on server config
  'graphqlHTTP\([[:space:]]*\{[^}]*schema|medium|QD-013|graphqlHTTP middleware without validationRules configuration|Add validationRules with depthLimit and costAnalysis to graphqlHTTP options'

  # QD-014: Relay-style connection without first/last limit
  'connection[[:space:]]*\([^)]*\)[[:space:]]*\{[^}]*edges|low|QD-014|Relay connection pattern without visible first/last argument limit|Enforce max first/last arguments on connections (e.g., max 100) to bound result size'

  # QD-015: No query timeout or execution time limit
  'execute\([[:space:]]*schema|low|QD-015|GraphQL execute() call without timeout or abort signal|Add execution timeout to prevent long-running queries from consuming server resources'
)

# ============================================================================
# 2. RESOLVER N+1 (RN-001 through RN-015)
#    Detects database call inside resolver loop, no DataLoader usage,
#    sequential awaits in list resolver, missing batching, individual
#    fetch per array item.
# ============================================================================

declare -a GQLLINT_RN_PATTERNS=()

GQLLINT_RN_PATTERNS+=(
  # RN-001: Database find call inside forEach or map with await (N+1)
  '\.map\([[:space:]]*async[[:space:]]*\([^)]*\)[[:space:]]*=>[^}]*\.find\(|critical|RN-001|Async map with database find() call inside (N+1 query pattern)|Use DataLoader to batch database lookups instead of fetching inside map/forEach loops'

  # RN-002: Resolver with for loop containing await (sequential DB calls)
  'async[[:space:]]*\([^)]*\)[[:space:]]*\{[^}]*for[[:space:]]*\([^)]*\)[[:space:]]*\{[^}]*await|high|RN-002|Resolver with sequential await inside for loop (N+1 risk)|Replace loop-based awaits with Promise.all() or DataLoader for parallel batched fetching'

  # RN-003: forEach with await inside resolver context
  '\.forEach\([[:space:]]*async[[:space:]]*\([^)]*\)[[:space:]]*=>[^}]*await|high|RN-003|forEach with async/await in resolver (sequential execution, N+1)|Replace forEach+await with Promise.all(items.map(...)) or DataLoader batching'

  # RN-004: Individual findById inside loop
  'findById\([[:space:]]*[[:alnum:]]+\[|critical|RN-004|findById() called with array index (N+1 individual lookups)|Batch IDs with DataLoader or use find({ _id: { $in: ids } }) for single query'

  # RN-005: No DataLoader import or require in resolver file
  'resolve[[:space:]]*\([[:space:]]*parent|low|RN-005|Resolver function without DataLoader import in scope|Import and use DataLoader for any resolver that fetches related data from a data source'

  # RN-006: Prisma findMany inside a resolver map
  'prisma\.[[:alnum:]]+\.findUnique\([^)]*\)|medium|RN-006|Prisma findUnique() call in resolver (potential N+1 without batching)|Use Prisma batch queries or DataLoader to avoid N+1 when resolving lists of related entities'

  # RN-007: SQL SELECT inside a loop construct
  'SELECT[[:space:]].*FROM[[:space:]].*WHERE[[:space:]].*=[[:space:]]*\$|medium|RN-007|SQL SELECT with parameterized WHERE inside potential loop context|Batch SQL queries with IN clause or use DataLoader to avoid per-item SELECT statements'

  # RN-008: ORM get() or load() inside iteration
  '\.get\([[:space:]]*[[:alnum:]]+\[[[:alnum:]]+\]|high|RN-008|ORM get() called with array index variable (N+1 pattern)|Batch load with getMany() or use DataLoader to coalesce individual lookups'

  # RN-009: Nested resolver fetching parent data again
  'parent\.[[:alnum:]]+[[:space:]]*\?[[:space:]]*parent\.[[:alnum:]]+|low|RN-009|Nested resolver re-accessing parent fields (potential redundant fetch)|Pass resolved parent data down instead of re-fetching; use DataLoader for related lookups'

  # RN-010: Promise.all wrapping individual queries without batching
  'Promise\.all\([[:space:]]*[[:alnum:]]+\.map\([^)]*findOne|high|RN-010|Promise.all with individual findOne() calls (parallel N+1)|Replace parallel individual queries with a single batched query using find() with $in operator'

  # RN-011: Multiple sequential await calls in single resolver
  'await[[:space:]][[:alnum:]]+\.[[:alnum:]]+\([^)]*\)[[:space:]]*;[[:space:]]*await[[:space:]][[:alnum:]]+\.|medium|RN-011|Multiple sequential await calls in resolver (waterfall pattern)|Parallelize independent data fetches with Promise.all() to reduce resolver latency'

  # RN-012: TypeORM find inside resolver loop
  '\.find\([[:space:]]*\{[[:space:]]*where[[:space:]]*:[[:space:]]*\{[[:space:]]*[[:alnum:]]+[[:space:]]*:[[:space:]]*[[:alnum:]]+\.|medium|RN-012|TypeORM find() with dynamic where clause in resolver (N+1 risk)|Use TypeORM relations or DataLoader to batch lookups by related entity IDs'

  # RN-013: GraphQL field resolver making HTTP call per item
  'fetch\([[:space:]]*["`\x27].*\$\{[[:alnum:]]+\.id\}|high|RN-013|HTTP fetch with interpolated ID in resolver (N+1 HTTP calls)|Batch HTTP requests or use DataLoader to coalesce per-item API calls'

  # RN-014: Mongoose populate inside a loop
  '\.populate\([[:space:]]*["\x27][[:alnum:]]+["\x27][[:space:]]*\)|medium|RN-014|Mongoose populate() call (potential N+1 if called per document)|Use populate on the query level or DataLoader for batched population of related documents'

  # RN-015: No batch loading utility in project
  'Resolver\(\)[[:space:]]*\{|low|RN-015|Resolver class without visible batch loading or DataLoader setup|Establish DataLoader instances per request context to batch and cache resolver data fetches'
)

# ============================================================================
# 3. OVER/UNDER FETCHING (OF-001 through OF-015)
#    Detects selecting all fields (*), returning full objects when only ID
#    needed, no field-level selection, fetching unused relations, no
#    pagination on list fields.
# ============================================================================

declare -a GQLLINT_OF_PATTERNS=()

GQLLINT_OF_PATTERNS+=(
  # OF-001: SELECT * in resolver or data layer
  'SELECT[[:space:]]\*[[:space:]]FROM|critical|OF-001|SELECT * in GraphQL data layer (over-fetching all columns)|Select only the fields requested in the GraphQL query using info.fieldNodes or projections'

  # OF-002: No pagination arguments on list field
  'type[[:space:]]Query[[:space:]]*\{[^}]*:[[:space:]]*\[[[:alnum:]]+\]|high|OF-002|Query returning bare list type without pagination arguments (first/after/limit)|Add pagination arguments (first, after, limit, offset) to all list-returning query fields'

  # OF-003: Returning full object when only ID is needed
  'return[[:space:]][[:alnum:]]+;[[:space:]]*.*//.*full[[:space:]]object|low|OF-003|Returning full entity object where subset of fields would suffice|Return only requested fields using GraphQL info object or DTO projections'

  # OF-004: No field selection in ORM query
  '\.findAll\([[:space:]]*\{[[:space:]]*where|medium|OF-004|ORM findAll() without field selection attributes|Add attributes/select to ORM queries: findAll({ where: ..., attributes: [...] }) to avoid over-fetching'

  # OF-005: Fetching relations eagerly without being requested
  'relations[[:space:]]*:[[:space:]]*\[|medium|OF-005|Eager loading relations in resolver without checking requested fields|Use info argument to conditionally load relations only when they are requested in the query'

  # OF-006: No limit on database query from resolver
  '\.find\([[:space:]]*\{[[:space:]]*\}[[:space:]]*\)|high|OF-006|Database find() with empty filter and no limit (fetches entire collection)|Add limit/take to database queries and enforce maximum page size in resolvers'

  # OF-007: REST endpoint called from resolver returning full payload
  'fetch\([[:space:]]*["`\x27].*api.*["`\x27][[:space:]]*\)|medium|OF-007|REST API fetch in resolver without field filtering (potential over-fetching)|Transform REST response to return only GraphQL-requested fields; use projections or DTOs'

  # OF-008: Include all nested associations
  'include[[:space:]]*:[[:space:]]*\[[[:space:]]*\{[[:space:]]*all[[:space:]]*:[[:space:]]*true|high|OF-008|ORM include with all:true flag (eagerly loads every association)|Specify explicit include associations based on GraphQL query info to avoid loading unused data'

  # OF-009: No field-level resolver for computed fields
  'type[[:space:]][[:alnum:]]+[[:space:]]*\{[^}]*[[:alnum:]]+[[:space:]]*:[[:space:]]*String[^}]*\}|low|OF-009|Type with String fields that may benefit from field-level resolvers|Consider field-level resolvers for expensive computed fields to enable lazy loading'

  # OF-010: Returning entire array without pagination metadata
  'return[[:space:]]\{[[:space:]]*data[[:space:]]*:[[:space:]]*results[[:space:]]*\}|low|OF-010|Returning result array without pagination metadata (totalCount, hasNextPage)|Include pagination metadata (totalCount, pageInfo, hasNextPage) in list responses'

  # OF-011: GraphQL query requesting all possible fields
  'query[[:space:]]*\{[^}]*\{[^}]*[[:alnum:]]+[[:space:]]*[[:alnum:]]+[[:space:]]*[[:alnum:]]+[[:space:]]*[[:alnum:]]+[[:space:]]*[[:alnum:]]+[[:space:]]*[[:alnum:]]+|medium|OF-011|GraphQL query selecting many fields (possible over-fetching)|Request only the fields your component needs; use fragments to share common field selections'

  # OF-012: Model.toJSON() returning all fields to GraphQL
  '\.toJSON\(\)|medium|OF-012|Model toJSON() used in resolver (exposes all model fields to GraphQL)|Map model to a DTO or use field resolvers to control which data is exposed through GraphQL'

  # OF-013: No cursor-based pagination on connection type
  'type[[:space:]][[:alnum:]]+Connection[[:space:]]*\{[^}]*edges|low|OF-013|Connection type without cursor-based pagination implementation|Implement cursor-based pagination (after/before/first/last) for efficient list traversal'

  # OF-014: Fetching deeply nested relations in single query
  'populate\([[:space:]]*["\x27][[:alnum:]]+\.[[:alnum:]]+\.[[:alnum:]]+|high|OF-014|Deep nested populate (3+ levels) causing over-fetching|Limit populate depth and use DataLoader or separate queries for deep relations'

  # OF-015: No maxResults or pageSize enforcement
  'args\.[[:alnum:]]*[Ll]imit|low|OF-015|Limit argument used without visible max enforcement|Enforce a maximum page size: Math.min(args.limit, MAX_PAGE_SIZE) to prevent huge result sets'
)

# ============================================================================
# 4. RATE LIMITING & AUTH (RL-001 through RL-015)
#    Detects no auth check in resolver, missing rate limiting on mutations,
#    no query complexity throttling, open introspection, no persisted
#    queries enforcement.
# ============================================================================

declare -a GQLLINT_RL_PATTERNS=()

GQLLINT_RL_PATTERNS+=(
  # RL-001: Mutation resolver without auth/authentication check
  'Mutation[[:space:]]*:[[:space:]]*\{[^}]*resolve[[:space:]]*:[[:space:]]*async|critical|RL-001|Mutation resolver without visible authentication check|Add authentication middleware or @auth directive to all mutation resolvers'

  # RL-002: No rate limiting middleware on GraphQL endpoint
  'app\.[a-z]+\([[:space:]]*["\x27]/graphql["\x27]|high|RL-002|GraphQL endpoint registered without rate limiting middleware|Add rate limiting middleware (express-rate-limit, graphql-rate-limit) before the GraphQL endpoint'

  # RL-003: No persisted queries enforcement
  'new[[:space:]]ApolloServer\([[:space:]]*\{[^}]*schema|medium|RL-003|ApolloServer without persistedQueries configuration|Enable persistedQueries to prevent arbitrary query execution in production'

  # RL-004: Missing @auth directive on schema definition
  'type[[:space:]]Query[[:space:]]*\{[^}]*\([^)]*\)[[:space:]]*:[[:space:]]*[[:alnum:]]|medium|RL-004|Query field without @auth or @authenticated directive|Add authorization directives to query fields that return sensitive data'

  # RL-005: No CORS configuration on GraphQL endpoint
  'graphqlHTTP\([[:space:]]*\{[^}]*schema[[:space:]]*:|medium|RL-005|GraphQL HTTP middleware without CORS configuration|Configure CORS with specific allowed origins instead of wildcard for GraphQL endpoint'

  # RL-006: Anonymous query allowed without rate limit
  'context[[:space:]]*:[[:space:]]*\([[:space:]]*\{[[:space:]]*req[[:space:]]*\}[[:space:]]*\)[[:space:]]*=>|low|RL-006|GraphQL context factory without rate limiting or throttle logic|Add per-IP or per-user rate limiting in the context factory to throttle anonymous requests'

  # RL-007: No query complexity cost limit
  'maxComplexity|low|RL-007|maxComplexity configuration present but verify threshold is appropriate|Ensure maxComplexity threshold matches your server capacity; typical values: 500-2000'

  # RL-008: Subscription without authentication guard
  'type[[:space:]]Subscription[[:space:]]*\{[^}]*\([^)]*\)[[:space:]]*:|high|RL-008|Subscription field without authentication guard|Require authentication on subscriptions to prevent unauthorized real-time data access'

  # RL-009: No API key validation in context
  'context[[:space:]]*:[[:space:]]*\(\)[[:space:]]*=>[[:space:]]*\(\{|medium|RL-009|GraphQL context returning empty object (no auth/API key validation)|Validate authentication tokens or API keys in the context factory before resolver execution'

  # RL-010: Mutation without CSRF protection
  'app\.post\([[:space:]]*["\x27]/graphql["\x27]|medium|RL-010|GraphQL POST endpoint without CSRF protection middleware|Add CSRF token validation middleware for GraphQL mutations to prevent cross-site request forgery'

  # RL-011: No query allowlisting for production
  'playground[[:space:]]*:[[:space:]]*true|high|RL-011|GraphQL Playground enabled (should be disabled in production)|Disable GraphQL Playground in production; use playground: process.env.NODE_ENV === "development"'

  # RL-012: Missing helmet or security headers on GraphQL route
  'express\(\)[[:space:]]*;[^;]*app\.[a-z]+\([[:space:]]*["\x27]/graphql|low|RL-012|Express app with GraphQL route but no visible security header middleware|Add helmet() middleware before GraphQL route for security headers (CSP, HSTS, etc.)'

  # RL-013: No depth limit combined with auth check
  'depthLimit\([[:space:]]*[0-9]+[[:space:]]*\)|low|RL-013|depthLimit configured but verify it is combined with authentication|Combine depthLimit with per-user complexity budgets for authenticated rate limiting'

  # RL-014: Open subscription websocket without auth
  'subscriptions[[:space:]]*:[[:space:]]*\{[^}]*path[[:space:]]*:|high|RL-014|WebSocket subscription path configured without onConnect auth handler|Add onConnect handler to validate auth tokens on WebSocket subscription connections'

  # RL-015: No request size limit on GraphQL endpoint
  'bodyParser\.json\([[:space:]]*\)|medium|RL-015|Body parser without size limit on GraphQL endpoint|Set request body size limit: bodyParser.json({ limit: "100kb" }) to prevent oversized queries'
)

# ============================================================================
# 5. SCHEMA DESIGN (SD-001 through SD-015)
#    Detects non-nullable fields without defaults, missing input validation
#    types, god queries (100+ fields), no deprecation annotations,
#    inconsistent naming conventions.
# ============================================================================

declare -a GQLLINT_SD_PATTERNS=()

GQLLINT_SD_PATTERNS+=(
  # SD-001: Non-nullable field without default value in input type
  'input[[:space:]][[:alnum:]]+[[:space:]]*\{[^}]*:[[:space:]]*[[:alnum:]]+![^}]*\}|medium|SD-001|Input type with non-nullable field (may lack default value)|Provide default values for non-nullable input fields or make them nullable with validation'

  # SD-002: No @deprecated directive on old fields
  'type[[:space:]][[:alnum:]]+[[:space:]]*\{[^}]*[[:alnum:]]+[[:space:]]*:[[:space:]]*String|low|SD-002|Type fields without @deprecated directives on legacy fields|Add @deprecated(reason: "Use newField instead") to fields being phased out'

  # SD-003: Query type with many fields (god query object)
  'type[[:space:]]Query[[:space:]]*\{|medium|SD-003|Query type defined (verify it does not exceed 50+ root fields)|Keep Query type focused; split into domain-specific types using extend type Query'

  # SD-004: Mutation accepting raw scalar arguments instead of input type
  'Mutation[[:space:]]*\{[^}]*\([[:space:]]*[[:alnum:]]+[[:space:]]*:[[:space:]]*String|high|SD-004|Mutation using raw scalar arguments instead of dedicated input type|Use input types for mutations: createUser(input: CreateUserInput!) for better validation and evolution'

  # SD-005: Enum type with single value
  'enum[[:space:]][[:alnum:]]+[[:space:]]*\{[[:space:]]*[[:alnum:]]+[[:space:]]*\}|low|SD-005|Enum type with single value (unnecessary enum)|Remove single-value enums or add meaningful variants; single-value enums add complexity without benefit'

  # SD-006: No description on type definition
  'type[[:space:]][[:alnum:]]+[[:space:]]*\{|low|SD-006|Type definition without preceding description comment|Add descriptions to types using triple-quote strings for self-documenting GraphQL schemas'

  # SD-007: Field returning generic JSON/Object scalar
  ':[[:space:]]*JSON[^[:alnum:]]|high|SD-007|Field returning generic JSON scalar type (loses GraphQL type safety)|Replace JSON scalar with a properly typed GraphQL object to preserve type safety and validation'

  # SD-008: ID field not using ID scalar type
  '[[:alnum:]]*[Ii]d[[:space:]]*:[[:space:]]*String|medium|SD-008|ID-like field using String type instead of ID scalar|Use the ID scalar type for identifier fields to enable proper caching and normalization'

  # SD-009: Inconsistent naming (snake_case in GraphQL schema)
  '[[:space:]][a-z]+_[a-z]+[[:space:]]*:[[:space:]]*[[:alnum:]]|medium|SD-009|Snake_case field name in GraphQL schema (convention is camelCase)|Use camelCase for GraphQL field names; reserve snake_case for database columns'

  # SD-010: No error union type for mutations
  'type[[:space:]][[:alnum:]]*Payload[[:space:]]*\{[^}]*[[:alnum:]]+[[:space:]]*:[[:space:]]*[[:alnum:]]+!|low|SD-010|Mutation payload type without error union for structured error handling|Use union types for mutation results: union CreateUserResult = User or CreateUserError'

  # SD-011: Missing createdAt/updatedAt timestamp fields
  'type[[:space:]][[:alnum:]]+[[:space:]]*\{[^}]*id[[:space:]]*:[[:space:]]*ID|low|SD-011|Entity type with ID field but no visible timestamp fields|Add createdAt and updatedAt DateTime fields to entity types for audit trails'

  # SD-012: Float used for monetary values
  '[[:alnum:]]*[Pp]rice[[:space:]]*:[[:space:]]*Float|high|SD-012|Float type used for monetary/price field (floating point precision issues)|Use Int (cents), String, or custom Money scalar for monetary values to avoid precision errors'

  # SD-013: No custom scalar for email or URL fields
  '[[:alnum:]]*[Ee]mail[[:space:]]*:[[:space:]]*String|low|SD-013|Email field using plain String type instead of custom scalar|Use a custom Email scalar with built-in validation for email fields in the schema'

  # SD-014: Deeply nested input type (3+ levels)
  'input[[:space:]][[:alnum:]]+[[:space:]]*\{[^}]*:[[:space:]][[:alnum:]]+Input|medium|SD-014|Input type containing nested input type references (complexity risk)|Flatten deeply nested input types to simplify validation and reduce mutation complexity'

  # SD-015: No interface or union types in schema
  'type[[:space:]]Query[[:space:]]*\{.*type[[:space:]]Mutation|low|SD-015|Schema without interface or union types (may lack polymorphism)|Use interfaces for shared fields (Node, Timestamped) and unions for polymorphic returns'
)

# ============================================================================
# 6. CLIENT QUERY SAFETY (CQ-001 through CQ-015)
#    Detects string-concatenated queries, no query variables for user input,
#    missing error handling on GraphQL response, no retry on network
#    failure, caching without cache keys.
# ============================================================================

declare -a GQLLINT_CQ_PATTERNS=()

GQLLINT_CQ_PATTERNS+=(
  # CQ-001: Template literal injection in GraphQL query string
  'gql`[^`]*\$\{[^}]+\}[^`]*`|critical|CQ-001|Template literal interpolation inside gql tag (query injection risk)|Use GraphQL variables ($var) instead of string interpolation in gql tagged templates'

  # CQ-002: String concatenation building GraphQL query
  '["\x27]query[[:space:]]*\{["\x27][[:space:]]*\+|critical|CQ-002|String concatenation used to build GraphQL query (injection vulnerability)|Use parameterized GraphQL variables instead of string concatenation for dynamic values'

  # CQ-003: No error handling on GraphQL response
  '\.then\([[:space:]]*\([[:space:]]*[[:alnum:]]+[[:space:]]*\)[[:space:]]*=>[[:space:]]*[[:alnum:]]+\.data|high|CQ-003|GraphQL response accessed without checking errors array|Always check response.errors before accessing response.data in GraphQL clients'

  # CQ-004: Missing error field destructuring from GraphQL response
  'const[[:space:]]\{[[:space:]]*data[[:space:]]*\}[[:space:]]*=[[:space:]]*await|high|CQ-004|Destructuring only data from GraphQL response (ignoring errors)|Destructure both data and errors: const { data, errors } = await graphqlRequest(...)'

  # CQ-005: No retry logic on GraphQL network request
  'fetch\([[:space:]]*[[:alnum:]]*[Gg]raphql[[:alnum:]]*|medium|CQ-005|GraphQL fetch call without visible retry or error recovery logic|Add retry logic with exponential backoff for transient network failures on GraphQL requests'

  # CQ-006: User input directly interpolated into query
  'query.*\$\{req\.|critical|CQ-006|Request parameter directly interpolated into GraphQL query string|Never interpolate user input into queries; use GraphQL variables with proper type definitions'

  # CQ-007: No loading/error state management in query hook
  'useQuery\([[:space:]]*[[:alnum:]_]+[[:space:]]*\)[[:space:]]*;|medium|CQ-007|useQuery hook without destructuring loading and error states|Destructure loading and error: const { data, loading, error } = useQuery(QUERY)'

  # CQ-008: Cache policy not set on client query
  'useQuery\([[:space:]]*[[:alnum:]_]+[[:space:]]*\)|low|CQ-008|useQuery without explicit fetchPolicy configuration|Set fetchPolicy explicitly (cache-first, network-only, etc.) based on data freshness requirements'

  # CQ-009: No AbortController or cancellation on GraphQL request
  'fetch\([[:space:]]*["\x27].*graphql|low|CQ-009|GraphQL fetch without AbortController for request cancellation|Use AbortController to cancel in-flight GraphQL requests on component unmount or navigation'

  # CQ-010: Hardcoded GraphQL endpoint URL
  'fetch\([[:space:]]*["\x27]https*://[^"\x27]*graphql["\x27]|medium|CQ-010|Hardcoded GraphQL endpoint URL in client code|Use environment variables for GraphQL endpoint URL to support different environments'

  # CQ-011: No query deduplication in Apollo Client
  'new[[:space:]]ApolloClient\([[:space:]]*\{[^}]*link[[:space:]]*:|low|CQ-011|ApolloClient without queryDeduplication configuration|Enable queryDeduplication: true on ApolloClient to prevent duplicate in-flight requests'

  # CQ-012: Missing optimistic response on mutation
  'useMutation\([[:space:]]*[[:alnum:]_]+[[:space:]]*\)|low|CQ-012|useMutation without optimistic response configuration|Add optimisticResponse to mutations for instant UI feedback while awaiting server response'

  # CQ-013: GraphQL client without default error policy
  'new[[:space:]]ApolloClient\([[:space:]]*\{[^}]*cache[[:space:]]*:|medium|CQ-013|ApolloClient without defaultOptions error policy|Configure defaultOptions.query.errorPolicy and mutate.errorPolicy on ApolloClient'

  # CQ-014: No type generation from schema (missing codegen)
  'gql`[[:space:]]*query[[:space:]][[:alnum:]]+|low|CQ-014|GraphQL queries defined without visible type generation setup|Use graphql-codegen to generate TypeScript types from your schema for type-safe queries'

  # CQ-015: Mutation without refetchQueries or cache update
  'useMutation\([[:space:]]*[[:alnum:]_]+[[:space:]]*,[[:space:]]*\{|medium|CQ-015|useMutation with options but verify refetchQueries or cache update is configured|Add refetchQueries or update function to mutations to keep the Apollo cache consistent'
)

# ============================================================================
# Utility Functions
# ============================================================================

# Get total pattern count across all categories
gqllint_pattern_count() {
  local count=0
  count=$((count + ${#GQLLINT_QD_PATTERNS[@]}))
  count=$((count + ${#GQLLINT_RN_PATTERNS[@]}))
  count=$((count + ${#GQLLINT_OF_PATTERNS[@]}))
  count=$((count + ${#GQLLINT_RL_PATTERNS[@]}))
  count=$((count + ${#GQLLINT_SD_PATTERNS[@]}))
  count=$((count + ${#GQLLINT_CQ_PATTERNS[@]}))
  echo "$count"
}

# Get pattern count for a specific category
gqllint_category_count() {
  local category="$1"
  local patterns_name
  patterns_name=$(get_gqllint_patterns_for_category "$category")
  if [[ -z "$patterns_name" ]]; then
    echo 0
    return
  fi
  local -n _ref="$patterns_name"
  echo "${#_ref[@]}"
}

# Get patterns array name for a category
get_gqllint_patterns_for_category() {
  local category="$1"
  case "$category" in
    QD|qd) echo "GQLLINT_QD_PATTERNS" ;;
    RN|rn) echo "GQLLINT_RN_PATTERNS" ;;
    OF|of) echo "GQLLINT_OF_PATTERNS" ;;
    RL|rl) echo "GQLLINT_RL_PATTERNS" ;;
    SD|sd) echo "GQLLINT_SD_PATTERNS" ;;
    CQ|cq) echo "GQLLINT_CQ_PATTERNS" ;;
    *)     echo "" ;;
  esac
}

# Get the human-readable label for a category
get_gqllint_category_label() {
  local category="$1"
  case "$category" in
    QD|qd) echo "Query Depth & Complexity" ;;
    RN|rn) echo "Resolver N+1" ;;
    OF|of) echo "Over/Under Fetching" ;;
    RL|rl) echo "Rate Limiting & Auth" ;;
    SD|sd) echo "Schema Design" ;;
    CQ|cq) echo "Client Query Safety" ;;
    *)     echo "$category" ;;
  esac
}

# All category codes for iteration
get_all_gqllint_categories() {
  echo "QD RN OF RL SD CQ"
}

# Get categories available for a given tier level
# free=0 -> QD, RN (30 patterns)
# pro=1  -> QD, RN, OF, RL (60 patterns)
# team=2 -> all 6 (90 patterns)
# enterprise=3 -> all 6 (90 patterns)
get_gqllint_categories_for_tier() {
  local tier_level="${1:-0}"
  if [[ "$tier_level" -ge 2 ]]; then
    echo "QD RN OF RL SD CQ"
  elif [[ "$tier_level" -ge 1 ]]; then
    echo "QD RN OF RL"
  else
    echo "QD RN"
  fi
}

# Severity to numeric points for scoring
severity_to_points() {
  case "$1" in
    critical) echo 25 ;;
    high)     echo 15 ;;
    medium)   echo 8 ;;
    low)      echo 3 ;;
    *)        echo 0 ;;
  esac
}

# List patterns by category
gqllint_list_patterns() {
  local filter_category="${1:-all}"

  if [[ "$filter_category" == "all" ]]; then
    for cat in QD RN OF RL SD CQ; do
      gqllint_list_patterns "$cat"
    done
    return
  fi

  local patterns_name
  patterns_name=$(get_gqllint_patterns_for_category "$filter_category")
  if [[ -z "$patterns_name" ]]; then
    echo "Unknown category: $filter_category"
    return 1
  fi

  local -n _patterns_ref="$patterns_name"
  local label
  label=$(get_gqllint_category_label "$filter_category")

  echo "  ${label} (${filter_category}):"
  for entry in "${_patterns_ref[@]}"; do
    IFS='|' read -r regex severity check_id description recommendation <<< "$entry"
    printf "    %-8s %-10s %s\n" "$check_id" "$severity" "$description"
  done
  echo ""
}

# Validate that a category code is valid
is_valid_gqllint_category() {
  local category="$1"
  case "$category" in
    QD|qd|RN|rn|OF|of|RL|rl|SD|sd|CQ|cq) return 0 ;;
    *) return 1 ;;
  esac
}
