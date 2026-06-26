# Code Review Examples (v2)

This document provides comprehensive examples demonstrating the optimized code review process.

---

## Example 1: Security Vulnerability Review

### Code Under Review
```python
# src/api/users.py
from flask import request, jsonify
import sqlite3

@app.route('/api/users/<user_id>', methods=['GET'])
def get_user(user_id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    query = f"SELECT * FROM users WHERE id = {user_id}"
    cursor.execute(query)
    user = cursor.fetchone()
    conn.close()
    return jsonify(user)
```

### Review Output

```markdown
## Review Summary

**PR**: User API endpoint
**Files Changed**: 1 file, 12 lines added
**Risk Level**:Public API, Database access)

---

### Critical Issues

1. **SQL Injection Vulnerability** - `src/api/users.py:9`
   - **Problem**: User input directly interpolated into SQL query via f-string
   - **Impact**: Attacker can extract, modify, or delete any data in the database
   - **Exploit Example**: `GET /api/users/1 OR 1=1--` returns all users
   - **Suggestion**: 
     ```python
     # Current (VULNERABLE)
     query = f"SELECT * FROM users WHERE id = {user_id}"
     cursor.execute(query)
     
     # Fixed (SAFE)
     cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
     ```
   - **Reference**: CWE-89, OWASP A03:2021

2. **No Input Validation** - `src/api/users.py:7`
   - **Problem**: user_id not validated before use
   - **Impact**: Type confusion, potential SQL injection even with parameterized queries
   - **Suggestion**: 
     ```python
     try:
         user_id = int(user_id)
     except ValueError:
         return jsonify({"error": "Invalid user ID"}), 400
     ```

3. **Resource Leak** - `src/api/users.py:8-12`
   - **Problem**: Connection not closed if exception occurs
   - **Impact**: Connection pool exhaustion under load
   - **Suggestion**: 
     ```python
     try:
         conn = sqlite3.connect('database.db')
         cursor = conn.cursor()
         cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
         user = cursor.fetchone()
         return jsonify(user)
     finally:
         conn.close()
     ```

4. **No Authentication/Authorization** - `src/api/users.py:6`
   - **Problem**: Endpoint publicly accessible without auth
   - **Impact**: Any user can access any other user's data
   - **Suggestion**: Add authentication middleware and ownership check

5. **Sensitive Data Exposure** - `src/api/users.py:11`
   - **Problem**: Returns all columns including password hash, email, etc.
   - **Impact**: PII leakage, credential exposure
   - **Suggestion**: Select only necessary fields
     ```python
     cursor.execute("SELECT id, name, email FROM users WHERE id = ?", (user_id,))
     ```

---

### Recommendation

**Status**: Rejected - Critical security issues

This endpoint has multiple critical security vulnerabilities that must be addressed before deployment. Please review the issues above and consider implementing proper authentication, input validation, and parameterized queries.

---

### Positive Notes

- Clean endpoint structure
- Proper use of Flask routing
```

---

## Example 2: Performance Issue Review

### Code Under Review
```javascript
// src/services/AnalyticsService.js
class AnalyticsService {
  async getMonthlyReport(userId, year) {
    const months = [];
    
    for (let month = 1; month <= 12; month++) {
      const transactions = await db.transactions.find({
        userId,
        date: {
          $gte: new Date(year, month - 1, 1),
          $lt: new Date(year, month, 1)
        }
      });
      
      const total = transactions.reduce((sum, t) => sum + t.amount, 0);
      const categories = {};
      
      for (const transaction of transactions) {
        if (!categories[transaction.category]) {
          categories[transaction.category] = 0;
        }
        categories[transaction.category] += transaction.amount;
      }
      
      months.push({
        month,
        total,
        categories: Object.entries(categories).map(([name, amount]) => ({ name, amount }))
      });
    }
    
    return months;
  }
}
```

### Review Output

```markdown
## Performance Review

**PR**: Monthly analytics report generation
**Files Changed**: 1 file, 35 lines added
**Focus**: Performance Analysis

---

### Performance Impact Assessment

| Metric | Current | Estimated | Issue |
|--------|---------|-----------|-------|
| Database Queries | 12 (sequential) | 12 | N+1 pattern |
| Response Time | ~600-1200ms | High | Sequential async |
| Memory Usage | O(n) per month | Moderate | Loading all transactions |

---

### Critical Issues

1. **N+1 Query Pattern** - `src/services/AnalyticsService.js:6-12`
   - **Problem**: 12 sequential database queries (one per month)
   - **Impact**: High latency, especially with network overhead
   - **Optimization**: 
     ```javascript
     // Current (SLOW - 12 queries)
     for (let month = 1; month <= 12; month++) {
       const transactions = await db.transactions.find({...});
     }
     
     // Optimized (FAST - 1 query)
     const allTransactions = await db.transactions.find({
       userId,
       date: {
         $gte: new Date(year, 0, 1),
         $lt: new Date(year + 1, 0, 1)
       }
     });
     
     // Then group by month in memory
     const byMonth = groupBy(allTransactions, t => t.date.getMonth() + 1);
     ```
   - **Expected Improvement**: 10-20x faster

2. **Inefficient Aggregation** - `src/services/AnalyticsService.js:14-20`
   - **Problem**: Manual iteration instead of database aggregation
   - **Impact**: Transfers unnecessary data, CPU overhead in application
   - **Optimization**: Use MongoDB aggregation pipeline
     ```javascript
     const report = await db.transactions.aggregate([
       { $match: { userId, date: { $gte: startDate, $lt: endDate } } },
       { $group: {
         _id: { month: { $month: "$date" }, category: "$category" },
         total: { $sum: "$amount" },
         count: { $sum: 1 }
       }}
     ]);
     ```
   - **Expected Improvement**: 5-10x less data transfer, faster processing

---

### Warnings

1. **No Caching** - Consider caching monthly reports
   - **Recommendation**: Add Redis caching with 1-hour TTL for completed months
   - **Impact**: Near-instant response for repeated requests

2. **No Pagination for Large Datasets**
   - **Recommendation**: If users have 100k+ transactions, consider streaming or pagination

---

### Positive Notes

- Clean class structure
- Good use of async/await
- Proper date boundary calculations

---

### Verdict

**Performance Impact**: Negative - Will not scale

Request changes to use aggregation pipeline and reduce database queries. The current implementation will become a bottleneck as data grows.
```

---

## Example 3: Rust Code Review (Memory Safety)

### Code Under Review
```rust
// src/cache.rs
use std::collections::HashMap;

pub struct Cache {
    data: HashMap<String, Vec<u8>>,
}

impl Cache {
    pub fn new() -> Self {
        Cache {
            data: HashMap::new(),
        }
    }
    
    pub fn get(&self, key: &str) -> Option<Vec<u8>> {
        self.data.get(key).cloned()
    }
    
    pub fn set(&mut self, key: String, value: Vec<u8>) {
        self.data.insert(key, value);
    }
    
    pub fn get_or_compute<F>(&self, key: &str, compute: F) -> Vec<u8>
    where
        F: FnOnce() -> Vec<u8>,
    {
        match self.get(key) {
            Some(value) => value,
            None => {
                let value = compute();
                // BUG: Can't mutate self here because &self is immutable
                value
            }
        }
    }
}
```

### Review Output

```markdown
## Review Summary

**PR**: In-memory cache implementation
**Files Changed**: 1 file, 38 lines added
**Risk Level**: Medium

---

### Critical Issues

1. **Compilation Error** - `src/cache.rs:28-35`
   - **Problem**: `get_or_compute` cannot mutate cache due to immutable `&self`
   - **Impact**: Code won't compile
   - **Suggestion**: 
     ```rust
     // Option 1: Use interior mutability with Mutex/RwLock
     use std::sync::{Mutex, RwLock};
     
     pub struct Cache {
         data: RwLock<HashMap<String, Vec<u8>>>,
     }
     
     // Option 2: Change signature to take &mut self
     pub fn get_or_compute<F>(&mut self, key: &str, compute: F) -> Vec<u8>
     where
         F: FnOnce() -> Vec<u8>,
     {
         if let Some(value) = self.get(key) {
             return value;
         }
         let value = compute();
         self.set(key.to_string(), value.clone());
         value
     }
     ```

---

### Warnings

1. **Unbounded Memory Growth** - `src/cache.rs:21`
   - **Problem**: Cache never evicts entries, will grow indefinitely
   - **Impact**: Out of memory in long-running applications
   - **Recommendation**: Use `lru` crate or implement TTL/size-based eviction
     ```rust
     use lru::LruCache;
     use std::num::NonZeroUsize;
     
     pub struct Cache {
         data: LruCache<String, Vec<u8>>,
     }
     
     impl Cache {
         pub fn new(capacity: usize) -> Self {
             Cache {
                 data: LruCache::new(NonZeroUsize::new(capacity).unwrap()),
             }
         }
     }
     ```

2. **Inefficient Cloning** - `src/cache.rs:14`
   - **Problem**: `cloned()` copies entire `Vec<u8>` on every get
   - **Impact**: Unnecessary memory allocations for large values
   - **Recommendation**: Consider returning reference with proper lifetime, or use `Arc<Vec<u8>>` for shared ownership

---

### Suggestions

1. **Add Cache Statistics**
   - Track hit/miss rates for monitoring
   - Consider using `metrics` crate

2. **Thread Safety**
   - If used across threads, wrap in `Arc<Mutex<Cache>>` or use `DashMap`

---

### Positive Notes

- Clean API design
- Good use of generics and traits
- Type-safe interface

---

### Recommendation

**Status**: Request changes - Won't compile as-is

Please fix the compilation error and consider the memory growth issue before merging.
```

---

## Example 4: Positive Review (Well-Written Code)

### Code Under Review
```typescript
// src/services/EmailService.ts
import { injectable } from 'inversify';
import nodemailer from 'nodemailer';
import { Logger } from '../utils/Logger';

interface EmailOptions {
  to: string;
  subject: string;
  body: string;
  attachments?: Array<{ filename: string; content: Buffer }>;
}

@injectable()
export class EmailService {
  private transporter: nodemailer.Transporter;
  private readonly logger: Logger;

  constructor(logger: Logger) {
    this.logger = logger;
    this.transporter = nodemailer.createTransport({
      host: process.env.SMTP_HOST,
      port: parseInt(process.env.SMTP_PORT || '587'),
      secure: false,
      auth: {
        user: process.env.SMTP_USER,
        pass: process.env.SMTP_PASS,
      },
    });
  }

  async send(options: EmailOptions): Promise<void> {
    this.validateEmailOptions(options);

    try {
      await this.transporter.sendMail({
        from: process.env.EMAIL_FROM,
        to: options.to,
        subject: options.subject,
        html: options.body,
        attachments: options.attachments,
      });

      this.logger.info('Email sent', { to: options.to, subject: options.subject });
    } catch (error) {
      this.logger.error('Failed to send email', {
        error: error instanceof Error ? error.message : 'Unknown error',
        to: options.to,
      });
      throw new Error(`Failed to send email: ${error}`);
    }
  }

  private validateEmailOptions(options: EmailOptions): void {
    if (!options.to || !options.subject || !options.body) {
      throw new Error('Missing required email fields');
    }

    if (!this.isValidEmail(options.to)) {
      throw new Error('Invalid email address');
    }
  }

  private isValidEmail(email: string): boolean {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
  }
}
```

### Review Output

```markdown
## Review Summary

**PR**: Email service implementation
**Files Changed**: 1 file, 72 lines added
**Risk Level**: Low

---

### Issues Found

None identified.

---

### Positive Notes

- **Excellent Type Safety**: Comprehensive TypeScript interfaces and proper type annotations
- **Dependency Injection**: Clean use of Inversify for testability
- **Error Handling**: Proper try-catch with contextual logging
- **Input Validation**: Validates email options before sending
- **Observability**: Structured logging with relevant context
- **Configuration**: Environment variables for all configuration
- **Single Responsibility**: Focused, well-encapsulated class
- **Documentation**: Clear interface definitions

---

### Minor Suggestions (Optional)

1. Consider adding rate limiting for bulk email scenarios
2. Could add retry logic with exponential backoff for transient SMTP failures
3. Email validation regex could be more comprehensive (consider `validator` package)

---

### Recommendation

**Status**: Approved

Well-written, production-ready code. No changes required.
```

---

## Example 5: Architecture Review (Microservice Communication)

### Code Under Review
```go
// cmd/api/main.go
package main

import (
    "context"
    "net/http"
    "time"
    
    "github.com/company/orderservice/internal/handler"
    "github.com/company/orderservice/internal/service"
    "github.com/company/orderservice/pkg/inventory"
    "github.com/company/orderservice/pkg/payment"
)

func main() {
    inventoryClient := inventory.NewClient("http://inventory-service:8080")
    paymentClient := payment.NewClient("http://payment-service:8080")
    
    orderService := service.NewOrderService(inventoryClient, paymentClient)
    handler := handler.NewOrderHandler(orderService)
    
    http.HandleFunc("/orders", handler.CreateOrder)
    http.ListenAndServe(":8080", nil)
}

// internal/service/order.go
func (s *OrderService) CreateOrder(ctx context.Context, req CreateOrderRequest) error {
    // 1. Check inventory
    inventoryResp, err := s.inventoryClient.CheckStock(ctx, req.Items)
    if err != nil {
        return err
    }
    
    // 2. Process payment
    paymentResp, err := s.paymentClient.Charge(ctx, req.PaymentInfo)
    if err != nil {
        return err
    }
    
    // 3. Create order in database
    order := Order{
        Items: req.Items,
        PaymentID: paymentResp.ID,
        Status: "created",
    }
    return s.db.CreateOrder(ctx, order)
}
```

### Review Output

```markdown
## Architecture Review

**PR**: Order service implementation
**Scope**: Microservice communication, distributed transaction
**Risk Level**:Financial transactions)

---

### Architectural Assessment

| Criterion | Rating | Notes |
|-----------|--------|-------|
| Cohesion | ✅ Good | Clear separation of concerns |
| Coupling | Concern | Tight coupling to external services |
| Extensibility | ✅ Good | Easy to add new handlers |
| Testability | ✅ Good | Dependency injection used |
| Operability |❌ | No circuit breakers, retries, or observability |

---

### Critical Issues

1. **Distributed Transaction Problem** - `internal/service/order.go:14-28`
   - **Problem**: Three-phase operation without compensation (inventory → payment → order)
   - **Impact**: Money charged but order not created if DB fails (or vice versa)
   - **Severity**: inconsistency, financial impact
   - **Recommendation**: Implement Saga pattern or use outbox pattern
     ```go
     func (s *OrderService) CreateOrder(ctx context.Context, req CreateOrderRequest) error {
         // Phase 1: Reserve inventory (not deduct)
         if err := s.inventoryClient.Reserve(ctx, req.Items); err != nil {
             return err
         }
         defer s.inventoryClient.Release(ctx, req.Items) // Compensation
         
         // Phase 2: Create order first (idempotent)
         order := Order{Items: req.Items, Status: "pending_payment"}
         if err := s.db.CreateOrder(ctx, order); err != nil {
             return err
         }
         
         // Phase 3: Process payment
         paymentResp, err := s.paymentClient.Charge(ctx, req.PaymentInfo)
         if err != nil {
             return err // Inventory will be released by defer
         }
         
         // Phase 4: Confirm order
         return s.db.UpdateOrderStatus(ctx, order.ID, "confirmed", paymentResp.ID)
     }
     ```

2. **No Circuit Breakers** - `cmd/api/main.go:16-17`
   - **Problem**: Direct HTTP calls without failure isolation
   - **Impact**: Cascading failures if downstream services are down
   - **Recommendation**: Use circuit breaker pattern
     ```go
     import "github.com/sony/gobreaker"
     
     cb := gobreaker.NewCircuitBreaker(gobreaker.Settings{
         Name:        "inventory-service",
         MaxRequests: 3,
         Timeout:     30 * time.Second,
     })
     
     // Wrap calls with circuit breaker
     result, err := cb.Execute(func() (interface{}, error) {
         return inventoryClient.CheckStock(ctx, req.Items)
     })
     ```

3. **No Retries** - `internal/service/order.go`
   - **Problem**: Transient failures cause immediate order failure
   - **Impact**: Poor user experience, lost sales
   - **Recommendation**: Add retry with exponential backoff for idempotent operations

---

### Warnings

1. **No Timeout Configuration** - `cmd/api/main.go:16-17`
   - HTTP clients should have timeouts configured
   - Default is no timeout (can hang indefinitely)

2. **No Request Tracing**
   - Add correlation IDs for distributed tracing
   - Pass trace context to downstream services

3. **No Health Checks**
   - Implement `/health` and `/ready` endpoints

---

### Dependencies

**External Service Dependencies**:
- `inventory-service`: Critical, no fallback
- `payment-service`: Critical, no fallback

**Recommendation**: Implement graceful degradation (queue orders for later processing if services are temporarily unavailable)

---

### Verdict

**Architecture**: Needs redesign - Distributed transaction issues

The current implementation has critical data consistency risks. Please implement compensation logic and circuit breakers before proceeding. Consider using a message queue for eventual consistency.
```

---

## Quick Reference: Review Patterns

| Pattern | What to Look For | Severity |
|---------|-----------------|----------|
| SQL Injection | String interpolation in queries |
| N+1 Queries | Loop with database calls | |
| Missing Auth | Public endpoints without checks |
| Resource Leaks | Unclosed connections/files | |
| No Error Handling | Swallowed exceptions | |
| Hardcoded Secrets | API keys in code |
| Race Conditions | Shared mutable state |
| No Input Validation | Trusting user input | |
| Missing Tests | Untested critical paths | |
| Magic Numbers | Unexplained constants |💡
