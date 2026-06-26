# Code Review Guidelines

**A comprehensive guide for AI agents performing code reviews**, organized by priority and impact.

---

## Table of Contents

### Security — **CRITICAL**
1. [SQL Injection Prevention](#sql-injection-prevention)
2. [XSS Prevention](#xss-prevention)

### Performance — **HIGH**
3. [Avoid N+1 Query Problem](#avoid-n-1-query-problem)

### Correctness — **HIGH**
4. [Proper Error Handling](#proper-error-handling)

### Maintainability — **MEDIUM**
5. [Use Meaningful Variable Names](#use-meaningful-variable-names)
6. [Add Type Hints](#add-type-hints)

### Test Coverage — **HIGH**
7. [Go Test Coverage Analysis](#go-test-coverage-analysis)

### Team Effectiveness - **HIGH**
8. [Team Effectiveness Metrics](#team-effectiveness-metrics.md)

---

## Security

### SQL Injection Prevention

**Impact: CRITICAL** | **Category: security** | **Tags:** sql, security, injection, database, go

Never construct SQL queries with string concatenation or f-strings. Always use parameterized queries to prevent SQL injection attacks.

#### Why This Matters

SQL injection is one of the most common and dangerous web vulnerabilities. Attackers can:
- Access unauthorized data
- Modify or delete database records
- Execute admin operations on the database
- In some cases, issue commands to the OS

#### ❌ Incorrect

```go
func getUser(userID string) (*User, error) {
    // 危险：字符串拼接SQL
    query := fmt.Sprintf("SELECT * FROM users WHERE id = %s", userID)
    row := db.QueryRow(query)
    // ...
}

// Vulnerable to: getUser("1' OR '1'='1")
// Returns all users!
```

#### ✅ Correct

```go
	import (
		"database/sql"
		"fmt"
	)

	type User struct {
		ID   string
		Name string
	}

	func getUser(userID string) (*User, error) {
		// 安全：参数化查询（Go 标准库占位符风格）
		query := "SELECT id, name FROM users WHERE id = ?"
		row := db.QueryRow(query, userID)
		
		var u User
		if err := row.Scan(&u.ID, &u.Name); err != nil {
			if err == sql.ErrNoRows {
				return nil, fmt.Errorf("user %s not found", userID)
			}
			return nil, fmt.Errorf("failed to query user: %w", err)
		}
		return &u, nil
	}
```

[➡️ Full details: security-sql-injection.md](rules/security-sql-injection.md)

---

### XSS Prevention

**Impact: CRITICAL** | **Category: security** | **Tags:**  xss, security, html, go, template

Never insert unsanitized user input directly into HTML responses. Always use Go's html/template package (auto-escapes by default) or explicit escaping for raw HTML.

#### ❌ Incorrect

```go
// 危险：直接拼接用户输入到HTML
func handleUserProfile(w http.ResponseWriter, r *http.Request) {
    username := r.URL.Query().Get("username")
    w.Write([]byte(fmt.Sprintf("<h1>Hello %s</h1>", username)))
}
// 恶意输入示例：?username=<script>stealCookies()</script>
```

#### ✅ Correct

```go
import (
    "html/template"
    "net/http"
    "html"
)

// 方案1：使用html/template（推荐，自动转义）
var profileTpl = template.Must(template.New("profile").Parse(`
    <h1>Hello {{.Username}}</h1>
`))

func handleUserProfile(w http.ResponseWriter, r *http.Request) {
    username := r.URL.Query().Get("username")
    if err := profileTpl.Execute(w, map[string]string{"Username": username}); err != nil {
        http.Error(w, err.Error(), http.StatusInternalServerError)
        return
    }
}

// 方案2：手动转义（仅当必须拼接HTML时）
func handleRawHTML(w http.ResponseWriter, r *http.Request) {
    userInput := r.URL.Query().Get("content")
    safeInput := html.EscapeString(userInput)
    w.Write([]byte(fmt.Sprintf("<div>%s</div>", safeInput)))
}
```

[➡️ Full details: security-xss-prevention.md](rules/security-xss-prevention.md)

---

## Performance

### Avoid N+1 Query Problem

**Impact: HIGH** | **Category: performance** | **Tags:** database, performance, orm, go, sql

The N+1 query problem occurs when code executes 1 query to fetch a list, then N additional queries to fetch related data for each item. Use JOIN queries or batch fetching in Go to avoid this.

#### ❌ Incorrect

```go
// 101 queries for 100 posts!
func listPosts() ([]Post, error) {
    // 1 query to get all posts
    rows, err := db.Query("SELECT id, title, author_id FROM posts")
    if err != nil {
        return nil, err
    }
    defer rows.Close()

    var posts []Post
    for rows.Next() {
        var p Post
        if err := rows.Scan(&p.ID, &p.Title, &p.AuthorID); err != nil {
            return nil, err
        }
        // N queries to get author for each post
        author, err := getAuthor(p.AuthorID) // 每次循环执行SQL查询
        if err != nil {
            return nil, err
        }
        p.Author = author
        posts = append(posts, p)
    }
    return posts, nil
}
```

#### ✅ Correct

```go
type Post struct {
    ID     string
    Title  string
    Author Author
}

type Author struct {
    ID   string
    Name string
}

// 1 query with JOIN (无N+1问题)
func listPosts() ([]Post, error) {
    query := `
        SELECT p.id, p.title, p.author_id, a.id, a.name 
        FROM posts p
        JOIN authors a ON p.author_id = a.id
    `
    rows, err := db.Query(query)
    if err != nil {
        return nil, err
    }
    defer rows.Close()

    var posts []Post
    for rows.Next() {
        var p Post
        var authorID, authorName string
        if err := rows.Scan(&p.ID, &p.Title, &authorID, &p.Author.ID, &p.Author.Name); err != nil {
            return nil, err
        }
        posts = append(posts, p)
    }
    return posts, nil
}
```

[➡️ Full details: performance-n-plus-one.md](rules/performance-n-plus-one.md)

---

## Correctness

### Proper Error Handling

**Impact: HIGH** | **Category: correctness** | **Tags:**  errors, exceptions, reliability, go

Always handle errors explicitly in Go (no "bare" error ignores). Use error wrapping (%w) for context, and never ignore errors with _ unless intentionally justified.

#### ❌ Incorrect

```go
// 危险：忽略错误 + 无上下文的错误返回
func loadConfig(path string) (*Config, error) {
    data, _ := os.ReadFile(path) // 忽略读取错误
    var cfg Config
    if err := json.Unmarshal(data, &cfg); err != nil {
        return nil, errors.New("config parse failed") // 无具体上下文
    }
    return &cfg, nil
}
```

#### ✅ Correct

```go
	import (
		"encoding/json"
		"errors"
		"fmt"
		"os"
	)

	type Config struct {
		Port int `json:"port"`
	}

	func loadConfig(path string) (*Config, error) {
		data, err := os.ReadFile(path)
		if err != nil {
			if os.IsNotExist(err) {
				return getDefaultConfig(), fmt.Errorf("config file %s not found, using defaults: %w", path, err)
			}
			return nil, fmt.Errorf("failed to read config file %s: %w", path, err)
		}

		var cfg Config
		if err := json.Unmarshal(data, &cfg); err != nil {
			return nil, fmt.Errorf("invalid JSON in config file %s: %w", path, err)
		}
		return &cfg, nil
	}

	func getDefaultConfig() *Config {
		return &Config{Port: 8080}
	}
```

[➡️ Full details: correctness-error-handling.md](rules/correctness-error-handling.md)

---

## Maintainability

### Use Meaningful Variable Names

**Impact: MEDIUM** | **Category: maintainability** | **Tags:** naming, readability, code-quality, go

Choose descriptive, intention-revealing names (follow Go idioms). Avoid single letters (except loop counters like i, j), abbreviations, and generic names.

#### ❌ Incorrect

```go
// 模糊的命名，无法体现语义
func calc(x, y float64, z int) float64 {
    t := x * float64(z)
    r := t + y
    return r
}
```

#### ✅ Correct

```go
// 语义化命名，符合Go命名规范（小写开头，简洁且明确）
func calculateTotalPrice(unitPrice float64, tax float64, quantity int) float64 {
    subtotal := unitPrice * float64(quantity)
    total := subtotal + (subtotal * tax)
    return total
}
```

[➡️ Full details: maintainability-naming.md](rules/maintainability-naming.md)

---

### Add Type Hints

**Impact: MEDIUM** | **Category: maintainability** | **Tags:** types, go , type-safety

Leverage Go's strong typing system: use custom types for domain-specific values, avoid empty interfaces (interface{}) where possible, and define clear function signatures.

#### ❌ Incorrect

```go
// 弱类型：使用空接口，丢失类型信息
func processData(data interface{}) interface{} {
    // 需要大量类型断言，易出错
    return data
}
```

#### ✅ Correct

```go
// 强类型：自定义类型 + 明确签名
type UserID string
type OrderAmount float64

type Order struct {
    ID     string
    UserID UserID
    Amount OrderAmount
}

func calculateOrderTotal(orders []Order) OrderAmount {
    var total OrderAmount
    for _, o := range orders {
        total += o.Amount
    }
    return total
}

// 明确的输入输出类型，无空接口
func getOrderByID(orderID string) (*Order, error) {
    // 业务逻辑
    return &Order{ID: orderID}, nil
}
```

[➡️ Full details: maintainability-type-hints.md](rules/maintainability-type-hints.md)

---

## Test Coverage

### Go Test Coverage Analysis

** Impact: HIGH | Category: testing | Tags: go, test, coverage, unit-test **

Analyze Go test coverage data generated by the command:


```go
go test "./..." \
    -v \
    -coverprofile="coverage.out" \
    -covermode=count \
    -gcflags=-l \
    -json > test-report.json
```
Parse coverage.out (coverage data) and test-report.json (test execution logs) to generate module-level coverage reports.

### Coverage Metrics to Analyze


1.** Line Coverage **: Percentage of code lines executed by tests (core metric)

2.** Function Coverage **: Percentage of functions with at least one test

3.** Branch Coverage **: Percentage of code branches (if/else, switch) covered (via covermode=count)

4.** Module-Level Breakdown **: Coverage per package/module (e.g., api/, service/, utils/)


** Coverage Risk Levels **


| Risk Level | Line Coverage | Action |
|-------|-------------|--------|
| **CRITICAL** | < 60% | Block merge, require additional tests |
| **HIGH** | 60% - 79% | Fix before merge, focus on core logic coverage |
| **MEDIUM** | 80% - 89% | Accept with TODO to improve edge case coverage |
| **LOW** | ≥ 90% | Accept, optional minor improvements |


** Required Output: Module-Level Coverage Table **


| Module/Package | Line Coverage	| Function Coverage |	Branch Coverage | Risk Level	| Uncovered Core Functions|
|-----|-------|--------|-------|------|------|
| api/ | 85% | 88% | 79% | Medium | handleLogin() |,| handleOrder() |
| service/ | 58% | 60% | 55% | Critical | calculateTotal() |,| validateUser() |
| utils/ | 92% | 95% | 90% | Low | None |
| database/ | 75% | 78% | 70% | High | connectDB(),migrate() |


** Test Failure Analysis (from test-report.json)


Extract and summarize test failures from the JSON log:

- Failed test names + package
- Error messages + stack traces
- Suggestions to fix failing tests


## Quick Reference

### Review Checklist

**Security (CRITICAL - review first)**
- [ ] No SQL injection (parameterized queries only)
- [ ] No XSS (html/template auto-escaping used)
- [ ] Secrets not hardcoded (use environment variables via os.Getenv)
- [ ] Proper authentication middleware for HTTP endpoints

**Performance (HIGH)**
- [ ] No N+1 SQL queries (JOINs used where needed)
- [ ] No unnecessary allocations (avoid fmt.Sprintf in hot paths)
- [ ] Efficient use of sync.Pool for frequent object creation
- [ ] No blocking operations in HTTP handler goroutines

**Correctness (HIGH)** - [ ] Proper error handling
- [ ] Proper error handling (no ignored errors, wrapped with context)
- [ ] Edge cases handled (nil checks, empty slices, boundary values)
- [ ] Input validation (use go-playground/validator for struct validation)
- [ ] No race conditions (proper sync primitives or channel usage)

**Maintainability (MEDIUM)**
- [ ] Clear variable/function names (Go idioms)
- [ ] Strong type safety (no unnecessary interface{})
- [ ] Code is DRY (reusable functions/packages)
- [ ] Functions follow single responsibility principle

**Testing**
- [ ] Test coverage per module meets thresholds
- [ ] Tests cover normal/error/edge cases
- [ ] Table-driven tests used for multiple input scenarios
- [ ] Mocks for external dependencies (use testify/mock)

---

## Severity Levels

| Level | Description | Examples | Action |
|-------|-------------|----------|--------|
| **CRITICAL** | Security vulnerabilities, data loss risks | SQL injection, XSS, hardcoded secrets | Block merge, fix immediately |
| **HIGH** | Performance issues, correctness bugs | N+1 queries, race conditions, < 60% coverage | Fix before merge |
| **MEDIUM** | Maintainability, code quality | Poor naming, unnecessary interface{}, 80-89% coverage | Fix or accept with TODO |
| **LOW** | Style preferences, minor improvements | Formatting, unused imports, ≥90% coverage | Optional |

---

## Review Output Format

When performing reviews, structure as:

```markdown
## Security Issues (X found)

### CRITICAL: SQL Injection in `get_user()`
**File:** `database/user.go:12`
**Issue:** User input interpolated directly into SQL query with fmt.Sprintf
**Fix:**  Use parameterized query with ? placeholder:
```go
  query := "SELECT id, name FROM users WHERE id = ?"
  row := db.QueryRow(query, userID)
```

## Performance Issues (X found)

### HIGH: N+1 Query in `list_posts()`

**File:** `service/post.go:25`

**Issue:**  Fetching author in loop (1+N queries)

**Fix:** Use JOIN query to fetch posts and authors in one query:

```go
  query := `SELECT p.id, p.title, a.id, a.name FROM posts p JOIN authors a ON p.author_id = a.id`
```
## Test Coverage Analysis

### Module-Level Coverage

| Module/Package | Line Coverage	| Function Coverage |	Branch Coverage | Risk Level	| Uncovered Core Functions|
|-----|-------|--------|-------|------|------|
| api/ | 85% | 88% | 79% | Medium | handleLogin() |,| handleOrder() |
| service/ | 58% | 60% | 55% | Critical | calculateTotal() |,| validateUser() |
| utils/ | 92% | 95% | 90% | Low | None |

### Test Failures
 ** TestCalculateTotal (package: service) **
  Error: expected 100.0, got 90.0
  Fix: Update test case to account for tax calculation logic

## Summary
- 🔴 CRITICAL: 1
- 🟠 HIGH: 1
- 🟡 MEDIUM: 3
- ⚪ LOW: 2

**Recommendation:** Address CRITICAL and HIGH issues before merging.Prioritize increasing service/ package coverage to ≥80% and fixing N+1 query problem.
```

---

## References

- Individual rule files in `rules/` directory
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Go Code Review Comments](https://github.com/golang/go/wiki/CodeReviewComments)
- [Go Testing Best Practices](https://go.dev/doc/testing)
- [Go Coverage Documentation](https://go.dev/blog/cover)
