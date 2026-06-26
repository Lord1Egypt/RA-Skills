# Integration Guide

> **Safe third-party integrations and system connections**
> Priority: MEDIUM | Category: Operations

## Overview

Each integration is a potential failure point and security risk. This guide provides safe patterns for connecting OpenClaw to external services.

## Integration Philosophy

```yaml
principles:
  one_at_a_time:
    reason: "Isolate failures, understand each integration"
    rule: "Never add multiple integrations simultaneously"

  test_before_trust:
    reason: "Verify behavior in isolation"
    rule: "Always test integration in controlled environment"

  minimal_permissions:
    reason: "Reduce blast radius of compromise"
    rule: "Request minimum necessary permissions"

  fail_closed:
    reason: "Prevent unauthorized access if integration fails"
    rule: "Deny by default, allow explicitly"
```

## Pre-Integration Checklist

```yaml
before_integrating:
  necessity:
    - [ ] "Integration is necessary for core functionality"
    - [ ] "No existing alternative available"
    - [ ] "Value outweighs complexity and risk"

  security:
    - [ ] "Service is reputable and maintained"
    - [ ] "Authentication method is secure"
    - [ ] "Data handling policies reviewed"
    - [ ] "Privacy implications understood"

  reliability:
    - [ ] "Service has good uptime record"
    - [ ] "Fallback strategy exists"
    - [ ] "Rate limits understood"
    - [ ] "SLA is acceptable"

  support:
    - [ ] "Documentation is comprehensive"
    - [ ] "Support channels exist"
    - [ ] "Community is active (if open source)"
```

## Integration Template

### Step 1: Planning

```markdown
# Integration Plan: [Service Name]

## Overview
**Service**: [Name and URL]
**Purpose**: [What this integration enables]
**Priority**: [critical | high | medium | low]

## Authentication
**Method**: [API key | OAuth | etc]
**Storage**: [Environment variables | Vault | etc]
**Rotation**: [Frequency]

## Permissions Required
- [Permission 1] - [Why needed]
- [Permission 2] - [Why needed]

## Data Flow
**Request**: [What we send]
**Response**: [What we receive]
**Frequency**: [How often]

## Failure Mode
**What happens if service is down**: [Impact]
**Fallback strategy**: [Alternative approach]
**Retry behavior**: [How to handle failures]

## Security Considerations
- [Consideration 1]
- [Consideration 2]

## Testing Plan
1. [Test case 1]
2. [Test case 2]

## Rollback Plan
[How to disable/remove integration]
```

### Step 2: Implementation

```yaml
implementation_phase:
  isolate:
    - "Create dedicated module/file for integration"
    - "No integration logic mixed with core logic"
    - "Clear interface abstraction"

  example_structure:
    file: "integrations/[service-name].js"
    content:
      - "Authentication handling"
      - "Request/response wrapping"
      - "Error handling"
      - "Retry logic"
      - "Rate limiting"

  abstraction_layer:
    purpose: "Easy to swap implementations"
    example: |
      # Don't use service directly in business logic
      # Use abstraction layer

      class NotificationService:
          def send(self, message):
              # Can swap email, slack, sms, etc
              pass
```

### Step 3: Testing

```yaml
testing_phases:
  unit_tests:
    - "Test integration module in isolation"
    - "Mock external service responses"
    - "Test error scenarios"

  integration_tests:
    - "Test against test environment of service"
    - "Test all API methods used"
    - "Test rate limiting"
    - "Test error handling"

  manual_tests:
    - "Verify authentication works"
    - "Test real requests"
    - "Verify error handling"
    - "Test fallback behavior"
```

### Step 4: Monitoring

```yaml
monitoring_setup:
  metrics:
    - "Request count"
    - "Success/failure rate"
    - "Response time"
    - "Rate limit utilization"

  alerting:
    - "High failure rate"
    - "Slow response times"
    - "Near rate limit"
    - "Authentication failures"

  logging:
    - "All requests (sanitized)"
    - "All errors"
    - "Rate limit events"
```

## Common Integration Patterns

### 1. Webhook Receivers

```yaml
pattern: "Receive data from external service"
security:
  - "Verify webhook signature"
  - "Validate source IP"
  - "Rate limit per source"
  - "Sanitize all input"

implementation:
  verification: |
    # Verify webhook signature
    signature = request.headers['X-Webhook-Signature']
    expected = hmac.sign(WEBHOOK_SECRET, payload)

    if signature != expected:
        return 403

  processing: |
    # Queue for async processing
    queue.push(WebhookJob(payload))

    # Return immediately
    return 202
```

### 2. API Clients

```yaml
pattern: "Make requests to external service"
security:
  - "Store credentials securely"
  - "Use HTTPS only"
  - "Implement rate limiting"
  - "Retry with exponential backoff"

implementation:
  authentication: |
    # Get credentials from secure storage
    api_key = secrets.get('SERVICE_API_KEY')

  request: |
    # Make request with timeout
    response = http.post(
      url,
      headers={'Authorization': f'Bearer {api_key}'},
      timeout=30,
      retry=3
    )

  error_handling: |
    # Handle errors gracefully
    if response.status == 429:
      # Rate limited - wait and retry
      wait(retry_after)
    elif response.status >= 500:
      # Server error - retry with backoff
      retry_with_backoff()
```

### 3. Authentication Providers

```yaml
pattern: "Use external service for authentication"
security:
  - "Validate tokens"
  - "Check token expiration"
  - "Handle revocation"
  - "Secure token storage"

implementation:
  validation: |
    # Always validate tokens
    def validate_token(token):
      # Check signature
      # Check expiration
      # Check issuer
      # Check revocation status
      return valid

  refresh: |
    # Handle token refresh
    if token.expired:
      new_token = refresh_token(token)
      if not new_token:
        raise AuthenticationError()
```

## Integration Examples

### Example 1: Email Service Integration

```yaml
service: "SendGrid"
purpose: "Send notifications"

plan:
  authentication:
    method: "API Key"
    storage: "Environment variable: SENDGRID_API_KEY"

  permissions:
    - "Send emails" - "Required for notifications"
    - "View email status" - "For monitoring"

  data_flow:
    request: "Recipient, subject, body"
    response: "Message ID, status"
    frequency: "As needed"

  failure_mode:
    if_down: "Queue emails, retry later"
    fallback: "Log to file for manual review"
    retry: "Exponential backoff, max 3 attempts"

security:
  - "API key stored as secret"
  - "Rate limiting applied"
  - "Input validation on recipients"
  - "Sanitize HTML content"

testing:
  - "Send test email"
  - "Test invalid recipient"
  - "Test rate limit handling"
  - "Test authentication failure"

monitoring:
  - "Emails sent per hour"
  - "Success rate"
  - "Error types"
  - "Response times"

rollback:
  - "Disable email notifications"
  - "Use fallback logging"
  - "Remove API key"
```

### Example 2: Calendar Integration

```yaml
service: "Google Calendar API"
purpose: "Schedule reminders"

plan:
  authentication:
    method: "OAuth 2.0"
    storage: "Encrypted token storage"
    rotation: "Token auto-refresh"

  permissions:
    - "Read calendar" - "Check availability"
    - "Create events" - "Add reminders"
    - NOT: "Delete events" - "Not needed"
    - NOT: "Share calendar" - "Not needed"

  data_flow:
    request: "Event title, time, attendees"
    response: "Event ID, confirmation"
    frequency: "User initiated"

  failure_mode:
    if_down: "Queue event, retry"
    fallback: "Log reminder, add manually"
    retry: "Linear backoff, max 5 attempts"

security:
  - "OAuth tokens encrypted"
  - "Scope limited to calendar only"
  - "Rate limiting applied"
  - "No calendar data logged"

testing:
  - "Create test event"
  - "Check availability"
  - "Test conflict handling"
  - "Test authentication refresh"

monitoring:
  - "Events created"
  - "API call count"
  - "Token refresh status"
  - "Error rates"

rollback:
  - "Disable calendar integration"
  - "Use email reminders instead"
  - "Revoke OAuth tokens"
```

## Integration Rollback Protocol

```yaml
when_to_rollback:
  immediate:
    - "Security breach detected"
    - "Data leak suspected"
    - "Service abused credentials"

  planned:
    - "Integration causing instability"
    - "Better alternative found"
    - "Integration no longer needed"

rollback_steps:
  1: "Disable integration in configuration"
  2: "Verify fallback is working"
  3: "Revoke/rotate credentials"
  4: "Clean up integration code (if permanent)"
  5: "Update documentation"
  6: "Notify stakeholders"
```

## Integration Review Checklist

### Post-Integration Review

```yaml
after_integration:
  functionality:
    - [ ] "Integration works as expected"
    - [ ] "Error handling is robust"
    - [ ] "Fallback mechanism works"
    - [ ] "Performance is acceptable"

  security:
    - [ ] "Credentials stored securely"
    - [ ] "Permissions are minimal"
    - [ ] "Data is sanitized"
    - [ ] "Rate limiting in place"

  reliability:
    - [ ] "Monitoring configured"
    - [ ] "Alerts configured"
    - [ ] "Logging in place"
    - [ ] "Failures handled gracefully"

  documentation:
    - [ ] "Integration documented"
    - [ ] "Troubleshooting guide written"
    - [ ] "Rollback procedure documented"
    - [ ] "Dependencies listed"
```

## Common Pitfalls

### ❌ Integration Without Testing

```yaml
mistake: "Add integration and ship to production"
risk: "Breaks production, hard to debug"
fix: "Always test in isolation first"
```

### ❌ Over-Broad Permissions

```yaml
mistake: "Request all permissions 'just in case'"
risk: "Security vulnerability, compliance issue"
fix: "Request minimum necessary permissions"
```

### ❌ No Fallback Strategy

```yaml
mistake: "Assume service is always available"
risk: "System breaks when service is down"
fix: "Always have fallback behavior"
```

### ❌ Ignoring Rate Limits

```yaml
mistake: "Make unlimited requests to API"
risk: "Get rate-limited, integration fails"
fix: "Implement rate limiting and retry logic"
```

### ❌ Logging Sensitive Data

```yaml
mistake: "Log API responses containing sensitive data"
risk: "Data leak through logs"
fix: "Sanitize all logged data"
```

## Key Takeaway

**Each integration is a contract with external dependencies.** Plan carefully, implement defensively, and always have an exit strategy.

---

**Related Skills**: `security-hardening.md`, `error-recovery.md`, `scope-control.md`
