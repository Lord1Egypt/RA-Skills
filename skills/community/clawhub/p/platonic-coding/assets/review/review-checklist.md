# Spec-to-Code Review Checklist

Use this checklist to systematically verify code implementation against specifications.

## Pre-Review

- [ ] Locate and read all relevant specifications
- [ ] Understand specification requirements and constraints
- [ ] Identify testable criteria from specs
- [ ] Determine review scope and boundaries
- [ ] Note spec version and last update date

## Spec Coverage

- [ ] All specified features are implemented
- [ ] All specified APIs/interfaces are present
- [ ] All specified data structures exist
- [ ] All specified behaviors are coded
- [ ] All specified constraints are enforced
- [ ] All specified error cases are handled

## Functional Consistency

- [ ] Implementation matches spec descriptions
- [ ] Function/method signatures match specs
- [ ] Input parameters match specifications
- [ ] Return values match specifications
- [ ] Side effects match specifications
- [ ] Workflows follow specified sequences

## Data Consistency

- [ ] Data models match spec definitions
- [ ] Field names match spec terminology
- [ ] Data types match specifications
- [ ] Validation rules match specs
- [ ] Default values match specifications
- [ ] Relationships/associations match specs

## API/Interface Consistency

**For Web APIs (Backend):**
- [ ] Endpoints match spec paths
- [ ] HTTP methods match specifications
- [ ] Request formats match specs
- [ ] Response formats match specs
- [ ] Status codes match specifications
- [ ] Headers match specifications

**For Libraries/Modules:**
- [ ] Public interfaces match specs
- [ ] Function signatures match specs
- [ ] Parameter types match specifications
- [ ] Return types match specifications

**For System Components:**
- [ ] Component interfaces match architecture specs
- [ ] Communication protocols match specs
- [ ] Message formats match specifications

## Business Logic Consistency

- [ ] Business rules implemented per specs
- [ ] Calculations match specified algorithms
- [ ] Workflows match specified processes
- [ ] State transitions match specifications
- [ ] Validation logic matches specs
- [ ] Authorization rules match specifications

## Error Handling Consistency

- [ ] Error conditions match specs
- [ ] Error messages match specifications
- [ ] Error codes match specifications
- [ ] Fallback behaviors match specs
- [ ] Retry logic matches specifications (if specified)
- [ ] Timeout handling matches specs (if specified)

## Performance Requirements

- [ ] Response time meets spec requirements
- [ ] Throughput meets specifications
- [ ] Resource usage within spec limits
- [ ] Scalability requirements addressed
- [ ] Concurrency handling per specs
- [ ] Rate limiting matches specifications (if specified)

## Security Requirements

**General:**
- [ ] Authentication matches spec requirements
- [ ] Authorization matches specifications
- [ ] Data encryption per specs (if specified)
- [ ] Sensitive data handling per specs

**Web/API Specific:**
- [ ] Input validation per specs
- [ ] SQL injection prevention (if database access)
- [ ] XSS prevention (if web-facing)
- [ ] CSRF protection (if web-facing)

**System/Backend Specific:**
- [ ] Access controls per specs
- [ ] Credential management per specs
- [ ] Network security per specs (if applicable)
- [ ] Audit logging per specs (if specified)

## Configuration & Deployment

- [ ] Configuration options match specs
- [ ] Environment variables per specs
- [ ] Deployment requirements per specs
- [ ] Dependencies match specifications
- [ ] Version requirements per specs

## Integration Points

- [ ] External service integration per specs
- [ ] Database integration per specs
- [ ] Message queue usage per specs (if applicable)
- [ ] File system usage per specs (if applicable)
- [ ] Network protocols per specs

## Testing Against Specs

- [ ] Test cases cover specified requirements
- [ ] Test scenarios match spec examples
- [ ] Edge cases from specs are tested
- [ ] Performance tests per spec requirements
- [ ] Integration tests per spec requirements

## Documentation Alignment

- [ ] Code comments reference specs where needed
- [ ] API documentation matches specs
- [ ] README reflects spec requirements
- [ ] Migration guides per specs (if breaking changes)

## Gap Analysis

- [ ] No specified features are missing
- [ ] No undocumented features in code
- [ ] No deprecated features per old specs
- [ ] All spec requirements have code
- [ ] All code features have spec coverage

## Cross-Reference Validation

- [ ] Spec dependencies are implemented
- [ ] Referenced specs are implemented
- [ ] Spec version matches implementation
- [ ] No implementation of superseded specs

## Final Verification

- [ ] Full checklist reviewed
- [ ] All inconsistencies documented
- [ ] All gaps identified
- [ ] Severity assigned to each finding
- [ ] Report generated (no code changes by default)

## Severity Classification

Rate inconsistencies by impact:

- **Critical** 🔴 - Spec violation with data loss/security/breaking impact
- **High** 🟠 - Major feature missing or incorrect per spec
- **Medium** 🟡 - Partial implementation or minor spec deviation
- **Low** 🟢 - Minor inconsistency or undocumented feature

## Report Components

Ensure your review includes:
- ✅ Features fully implemented per spec
- ⚠️ Features partially implemented
- ❌ Features missing from implementation
- ⚡ Features inconsistent with spec
- 🔍 Features needing clarification
- 📝 Undocumented features in code
