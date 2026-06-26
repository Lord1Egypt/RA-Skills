# Real E2E Test Templates

## Table of Contents

- [Philosophy](#philosophy)
- [1. Environment Preparation Script Template](#1-environment-preparation-script-template)
  - [Service Startup Sequence](#service-startup-sequence)
  - [Health Check Patterns](#health-check-patterns)
  - [System Boot Validation](#system-boot-validation)
- [2. HTTP API Real E2E Test Template](#2-http-api-real-e2e-test-template)
  - [Setup](#setup)
  - [Test Patterns](#test-patterns)
  - [Cleanup](#cleanup)
- [3. CLI Tool Real E2E Test Template](#3-cli-tool-real-e2e-test-template)
- [4. Browser Automation Real E2E Test Template](#4-browser-automation-real-e2e-test-template)
- [5. Mock Decision Guide](#5-mock-decision-guide)
- [6. Cleanup Strategy](#6-cleanup-strategy)

---

## Philosophy

These templates follow the **"real execution first"** principle. The default is to start real services and make real requests. Mock/stub is only used for uncontrollable external dependencies (third-party APIs, paid services).

---

## 1. Environment Preparation Script Template

A generic template for preparing the test environment before running E2E tests.

### Service Startup Sequence

```
# Environment Preparation Template

# 1. Check prerequisites
check_prerequisites():
    verify tool installed: runtime (node/python/java)
    verify tool installed: package manager (npm/pip/mvn)
    verify tool installed: docker (if needed)
    verify tool installed: database client (if needed)

# 2. Start dependency services (in order)
start_dependencies():
    # Start database
    start_service "database" using:
        - docker: docker compose up -d db
        - or native: systemctl start postgresql
    wait_for_health "database" using:
        - tcp: host:port
        - or http: GET /health
        - or cli: pg_isready -h localhost -p 5432

    # Start cache (if needed)
    start_service "cache" using:
        - docker: docker compose up -d redis
    wait_for_health "cache" using: tcp localhost:6379

    # Start message queue (if needed)
    start_service "queue" using:
        - docker: docker compose up -d rabbitmq
    wait_for_health "queue" using: tcp localhost:5672

# 3. Run database migrations/seeds
prepare_data():
    run migrations: project_migration_command
    seed test data: project_seed_command
    verify seed: query validation_table

# 4. Start the target service
start_target_service():
    start using: project_start_command (e.g., npm run dev, uvicorn app:app)
    wait_for_health "target" using:
        - http: GET http://localhost:PORT/health
    record: actual_port, actual_host

# 5. Verify full stack is ready
verify_ready():
    health_check all services
    if any service unhealthy:
        report blocker
        suggest downgrade realism level
```

### Health Check Patterns

```
# TCP check
wait_for_tcp(host, port, timeout=30):
    retry every 1s until timeout:
        try connect to host:port
        if connected: return ready
    return timeout

# HTTP check
wait_for_http(url, timeout=30):
    retry every 2s until timeout:
        response = GET url
        if response.status == 200: return ready
    return timeout

# CLI check
wait_for_cli(command, expected_output, timeout=30):
    retry every 2s until timeout:
        output = run command
        if expected_output in output: return ready
    return timeout
```

### System Boot Validation

Before running any tests, verify the system itself is deliverable. A system that can't boot from a clean state isn't shippable -- no matter how many unit tests pass.

```
# System Boot Validation

validate_system_boot():
    # 1. Clean start (no cached state)
    stop all services if running
    clear any cached artifacts (node_modules/.cache, __pycache__, build output)

    # 2. Start from scratch
    start target service using production-equivalent command
    capture startup logs

    # 3. Verify health
    health = GET http://localhost:PORT/health
    assert health.status == 200
    assert health.body.status == "healthy"  # if structured

    # 4. Check logs for errors
    errors = filter startup_logs for level >= ERROR
    assert errors is empty
    warnings = filter startup_logs for level == WARN
    if warnings:
        log "warnings during boot:" + warnings  # not blocking, but flagged

    # 5. Verify basic connectivity to each dependency
    for each dependency in [database, cache, queue, external_api]:
        probe = dependency.ping()
        assert probe.success

    # 6. Smoke test: one real external request
    smoke = GET base_url + "/"  # or any known-safe endpoint
    assert smoke.status in [200, 301, 302]  # alive, not crashing
```

**Why this matters:** Tests passing internally while the system fails to boot is the most common delivery failure. Boot validation catches missing environment variables, broken Docker configs, incompatible dependency versions, and misconfigured services before any test logic runs.

---

## 2. HTTP API Real E2E Test Template

A template for testing HTTP APIs with real requests.

### Setup

```
# Setup (once per test suite)
setup_suite():
    load environment config
    get base_url from config or service discovery
    get auth_token (if needed):
        - real login: POST /auth/login with test credentials
        - or API key from environment variable
    store auth_token for reuse
```

### Test Patterns

#### CRUD Operation

```
test "create and retrieve resource":
    # 1. Create
    create_response = POST base_url + "/api/resource"
        headers: { Authorization: auth_token, Content-Type: "application/json" }
        body: { name: "test-item", value: 42 }
    assert create_response.status == 201
    assert create_response.body.id exists
    assert create_response.body.name == "test-item"
    resource_id = create_response.body.id

    # 2. Retrieve
    get_response = GET base_url + "/api/resource/" + resource_id
        headers: { Authorization: auth_token }
    assert get_response.status == 200
    assert get_response.body.name == "test-item"
    assert get_response.body.value == 42

    # 3. Update
    update_response = PUT base_url + "/api/resource/" + resource_id
        headers: { Authorization: auth_token, Content-Type: "application/json" }
        body: { name: "updated-item", value: 99 }
    assert update_response.status == 200
    assert update_response.body.name == "updated-item"

    # 4. Delete
    delete_response = DELETE base_url + "/api/resource/" + resource_id
        headers: { Authorization: auth_token }
    assert delete_response.status == 204

    # 5. Verify deleted
    get_after_delete = GET base_url + "/api/resource/" + resource_id
        headers: { Authorization: auth_token }
    assert get_after_delete.status == 404
```

#### Error Handling

```
test "invalid input returns validation error":
    response = POST base_url + "/api/resource"
        headers: { Authorization: auth_token, Content-Type: "application/json" }
        body: { name: "", value: -1 }  # invalid: empty name, negative value
    assert response.status == 422
    assert response.body.errors exists
    assert "name" in response.body.errors  # field-level error
```

#### Auth/Permission

```
test "unauthenticated request returns 401":
    response = GET base_url + "/api/resource/123"
        # no auth header
    assert response.status == 401
```

#### Response Schema Validation

```
test "list endpoint returns correct schema":
    response = GET base_url + "/api/resource?page=1&limit=10"
        headers: { Authorization: auth_token }
    assert response.status == 200
    assert response.body.items is array
    assert response.body.total is integer
    assert response.body.page == 1
    assert len(response.body.items) <= 10
```

### Cleanup

```
# Cleanup (once per test suite)
cleanup_suite():
    delete all test-created resources (or use rollback)
    optionally reset database state
```

---

## 3. CLI Tool Real E2E Test Template

```
# CLI Tool E2E Test Template

# Setup
setup_suite():
    verify CLI installed: cli_command --version
    create temp directory for test artifacts
    set test config if needed

# Test pattern: Basic command execution
test "cli processes valid input correctly":
    output = run "cli_command process --input test_file.txt --output result.txt"
    assert exit_code == 0
    assert "success" in output
    assert file_exists("result.txt")

# Test pattern: Error handling
test "cli reports error for missing input":
    output = run "cli_command process --input nonexistent.txt"
    assert exit_code != 0
    assert "error" in output or "not found" in output

# Test pattern: Help and version
test "cli shows help":
    output = run "cli_command --help"
    assert exit_code == 0
    assert "usage" in output.lower()

# Test pattern: Piped input
test "cli reads from stdin":
    output = echo "test data" | run "cli_command process --stdin"
    assert exit_code == 0
    assert expected_result in output

# Test pattern: Config file
test "cli uses config file":
    write temp config: { "option": "value" }
    output = run "cli_command process --config temp_config.json"
    assert exit_code == 0
    assert "value" in output

# Cleanup
cleanup_suite():
    remove temp directory and test artifacts
```

---

## 4. Browser Automation Real E2E Test Template

```
# Browser E2E Test Template (conceptual, for Playwright/Puppeteer/Cypress patterns)

# Setup
setup_suite():
    launch browser (headless for CI, headed for local debug)
    set viewport size
    set base_url

# Test pattern: User flow
test "user can complete registration flow":
    # Navigate
    page.goto base_url + "/register"
    assert page.title contains "Register"

    # Fill form
    page.fill "#email" "test@example.com"
    page.fill "#password" "SecurePass123!"
    page.fill "#confirm-password" "SecurePass123!"
    page.click "#terms-checkbox"

    # Submit
    page.click "button[type=submit]"

    # Verify success
    wait_for_navigation base_url + "/dashboard"
    assert page.title contains "Dashboard"
    assert page.text contains "Welcome"

# Test pattern: Form validation
test "registration form shows inline errors":
    page.goto base_url + "/register"
    page.click "button[type=submit]"  # submit empty form

    assert page.element("#email-error").text is not empty
    assert page.element("#password-error").text is not empty

    page.fill "#email" "invalid-email"
    assert page.element("#email-error").text contains "valid email"

# Test pattern: API interaction
test "page loads data from API":
    page.goto base_url + "/dashboard"
    wait_for_selector ".data-loaded"

    # Verify API was called and data rendered
    assert page.element(".data-row").count > 0
    assert page.element(".data-row:first-child .name").text is not empty

# Test pattern: Error state
test "page handles API error gracefully":
    # Block API to simulate error
    page.route base_url + "/api/data" -> respond 500

    page.goto base_url + "/dashboard"
    assert page.element(".error-message").text contains "something went wrong"

# Cleanup
cleanup_suite():
    close browser
    clear cookies/storage
```

---

## 5. Mock Decision Guide

When to mock in E2E tests (minimal guidance -- the skill defaults to real):

| Scenario | Decision | Reason |
|----------|----------|--------|
| Internal database | Run real | Core integration point |
| Internal microservice | Run real | Contract verification |
| Third-party API (paid) | Mock/stub | Uncontrollable, no test sandbox |
| Third-party API (free tier) | Run real if rate limits allow | Prefer real |
| Email service (SendGrid etc.) | Mock | External, side effect |
| File storage (S3 etc.) | Mock or use local equivalent | External service |
| Authentication provider | Use test accounts if available | Prefer real |

---

## 6. Cleanup Strategy

```
# Cleanup patterns

# Per-test cleanup
cleanup_per_test():
    delete created resources via API
    or use database transaction rollback
    or delete from database directly

# Per-suite cleanup
cleanup_per_suite():
    drop test database and recreate
    or run project's test cleanup command
    or delete all resources created during test run

# Always cleanup even on failure
cleanup_on_failure():
    use try/finally pattern
    register cleanup in teardown hook
    log what was cleaned up (or what failed to clean)
```
