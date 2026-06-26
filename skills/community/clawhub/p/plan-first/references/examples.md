# Plan First - Detailed Examples

## Example 1: Full-Stack Feature Implementation

**Task:** "Add a comment system to our blog platform"

```markdown
## Task
Implement a comment system for the blog that allows users to leave comments on posts, with threading support and moderation.

## Plan

### Step 1: [DESIGN] Design database schema
**Dependencies:** None
**Approach:**
- Design comments table: id, post_id, parent_id (for threading), author_id, content, created_at, is_approved
- Consider indexes for post_id and parent_id queries
- Plan soft delete vs hard delete
**Verification:** 
- Schema documented
- Index plan reviewed
**Files:** docs/schema/comments.sql

### Step 2: [SETUP] Create database migration
**Dependencies:** Step 1
**Approach:**
- Write Alembic/SQLAlchemy migration
- Create models.py with Comment class
- Add relationships to Post and User models
**Verification:**
- Migration runs successfully
- Can query comments via ORM
**Files:** migrations/007_add_comments.py, models/comments.py

### Step 3: [API] Create backend endpoints
**Dependencies:** Step 2
**Approach:**
- POST /api/posts/{id}/comments - create comment
- GET /api/posts/{id}/comments - list comments (with threading)
- PATCH /api/comments/{id} - edit own comment
- DELETE /api/comments/{id} - soft delete
**Verification:**
- All endpoints return correct JSON
- Threading structure properly nested
**Files:** routes/comments.py, schemas/comments.py

### Step 4: [AUTH] Add permission checks
**Dependencies:** Step 3
**Approach:**
- Require authentication for creating comments
- Users can only edit/delete own comments
- Admins can moderate (approve/delete any)
**Verification:**
- Unauthorized requests return 401/403
- Users can't modify others' comments
**Files:** routes/comments.py, middleware/permissions.py

### Step 5: [FRONTEND] Build comment UI components
**Dependencies:** Step 3 (API contract known)
**Approach:**
- Comment component (display single comment)
- CommentList component (threaded display)
- CommentForm component (create/edit)
- CommentModeration component (admin)
**Verification:**
- Components render correctly with mock data
- Threading displays properly
**Files:** frontend/src/components/comments/*.jsx

### Step 6: [FRONTEND] Integrate with API
**Dependencies:** Steps 4, 5
**Approach:**
- Create API client functions
- Connect components to endpoints
- Handle loading states
- Handle errors gracefully
**Verification:**
- Can create comment and see it appear
- Threading works end-to-end
**Files:** frontend/src/api/comments.js, frontend/src/components/comments/*.jsx

### Step 7: [MODERATION] Add moderation queue
**Dependencies:** Step 4
**Approach:**
- New comments start as "pending"
- Admin dashboard for moderation
- Email notifications for new comments
- Auto-approve trusted users
**Verification:**
- Pending comments don't appear publicly
- Moderation actions work
**Files:** routes/admin.py, templates/admin/moderation.html

### Step 8: [TESTING] Backend tests
**Dependencies:** Steps 3, 4, 7
**Approach:**
- Unit tests for models
- Integration tests for endpoints
- Permission tests
- Threading logic tests
**Verification:**
- pytest tests/ -v passes 100%
**Files:** tests/test_comments.py

### Step 9: [TESTING] Frontend tests
**Dependencies:** Steps 5, 6
**Approach:**
- Component unit tests
- Integration tests with mocked API
- E2E tests for comment flow
**Verification:**
- npm test passes
- Critical user flows tested
**Files:** frontend/src/components/comments/*.test.jsx

### Step 10: [DEPLOY] Deploy to staging
**Dependencies:** Steps 1-9
**Approach:**
- Run migrations on staging DB
- Deploy backend
- Deploy frontend
- Verify full flow manually
**Verification:**
- Feature works in staging environment
**Files:** N/A

## Risk Analysis
**Blockers:**
- Database migration might be slow on large tables
- Threading query performance needs optimization
**Mitigation:**
- Test migration on copy of production data first
- Add query plan analysis for threading queries

## Rollback Plan
**If fails at migration (Step 2):**
- Can rollback migration
- No impact on existing functionality
**If API has issues (Step 3+):**
- Feature flag to disable
- Revert to previous commit
**If performance issues discovered:**
- Can denormalize threading structure
- Add caching layer
```

---

## Example 2: Research and Documentation

**Task:** "Create migration guide from v1 to v2 API"

```markdown
## Task
Write comprehensive documentation for customers migrating from API v1 to v2, including breaking changes, new features, and code examples.

## Plan

### Step 1: [ANALYSIS] Audit v1 vs v2 differences
**Dependencies:** None
**Approach:**
- Review v1 API endpoints and responses
- Review v2 API specification
- Document every endpoint change
- Identify breaking vs non-breaking changes
- Note deprecations
**Verification:**
- Complete list of all differences
- Categorized by severity
**Files:** analysis/v1_v2_comparison.md

### Step 2: [RESEARCH] Survey existing customer usage
**Dependencies:** Step 1
**Approach:**
- Check which v1 endpoints are most used
- Identify common integration patterns
- Look at support tickets for migration pain points
- Interview 3-5 key customers
**Verification:**
- Data on top 10 used endpoints
- 3 customer interviews completed
**Files:** research/customer_usage_report.md

### Step 3: [DRAFT] Write breaking changes section
**Dependencies:** Steps 1, 2
**Approach:**
- List each breaking change
- Explain why it changed
- Provide before/after code examples
- Include migration strategy for each
**Verification:**
- Each breaking change has code examples
- Reviewed by engineering team
**Files:** docs/migration/breaking_changes.md

### Step 4: [DRAFT] Write new features section
**Dependencies:** Step 1
**Approach:**
- Document all new v2 features
- Explain benefits over v1
- Provide usage examples
- Include best practices
**Verification:**
- All new features documented
- Examples compile/run
**Files:** docs/migration/new_features.md

### Step 5: [DRAFT] Create side-by-side comparison
**Dependencies:** Steps 3, 4
**Approach:**
- Table format: v1 code | v2 code
- Cover authentication, common operations
- Include notes on key differences
**Verification:**
- All v1 patterns have v2 equivalents
- Code examples tested
**Files:** docs/migration/cheat_sheet.md

### Step 6: [DRAFT] Write step-by-step migration guide
**Dependencies:** Steps 3, 4, 5
**Approach:**
- Phase 1: Preparation (audit, testing)
- Phase 2: Parallel running
- Phase 3: Cutover
- Phase 4: Cleanup
- Include timeline estimates
**Verification:**
- Steps are sequential and clear
- Timeline is realistic
**Files:** docs/migration/step_by_step.md

### Step 7: [CREATE] Build migration helper tool
**Dependencies:** Step 1
**Approach:**
- CLI tool to check v1 usage
- Auto-suggest v2 equivalents
- Validate v2 implementation
**Verification:**
- Tool runs on sample codebase
- Suggestions are accurate
**Files:** tools/api-migration-checker/

### Step 8: [REVIEW] Technical review
**Dependencies:** Steps 3, 4, 5, 6, 7
**Approach:**
- Engineering team reviews for accuracy
- Developer advocate reviews for clarity
- PM reviews for completeness
**Verification:**
- All feedback addressed
- Sign-off from reviewers
**Files:** [review comments in PR]

### Step 9: [PUBLISH] Package and release
**Dependencies:** Step 8
**Approach:**
- Convert to final format (PDF + web)
- Add to documentation site
- Create announcement blog post
- Update API reference docs
**Verification:**
- All links work
- Search indexing complete
**Files:** docs/migration/, blog/migration-guide.md

### Step 10: [SUPPORT] Prepare support materials
**Dependencies:** Step 9
**Approach:**
- FAQ from anticipated questions
- Troubleshooting guide
- Office hours schedule
- Direct support escalation path
**Verification:**
- Support team trained
- Materials reviewed by support lead
**Files:** docs/migration/faq.md

## Risk Analysis
**Blockers:**
- v2 spec might change during writing
- Engineering too busy to review
**Mitigation:**
- Lock spec version before Step 3
- Schedule review time in advance

## Rollback Plan
**If v2 launch delayed:**
- Version docs for specific v2 beta
- Mark as "upcoming" instead of "current"
- Keep iterating
```

---

## Example 3: Data Migration

**Task:** "Migrate user data from legacy system to new platform"

```markdown
## Task
Migrate 100,000 user records from legacy PostgreSQL database to new MongoDB-based platform, including validation and rollback capability.

## Plan

### Step 1: [ANALYSIS] Analyze legacy schema
**Dependencies:** None
**Approach:**
- Document all tables: users, profiles, preferences
- Map field types and constraints
- Identify orphaned records
- Check for duplicates
- Note encrypted fields
**Verification:**
- Complete schema documentation
- Row counts per table
**Files:** analysis/legacy_schema.md

### Step 2: [DESIGN] Design target schema
**Dependencies:** Step 1
**Approach:**
- Design MongoDB collections
- Map legacy fields to new structure
- Handle field merging/splitting
- Plan for indexes
- Document transformations needed
**Verification:**
- Schema approved by data architect
- Query patterns supported
**Files:** design/new_schema.json

### Step 3: [SETUP] Create migration environment
**Dependencies:** Step 2
**Approach:**
- Set up isolated migration database
- Create read replica of legacy (if possible)
- Set up target environment
- Configure monitoring/logging
**Verification:**
- Can connect to both databases
- Monitoring dashboards working
**Files:** infra/migration_env.tf

### Step 4: [IMPLEMENTATION] Write ETL scripts
**Dependencies:** Step 3
**Approach:**
- Extract from PostgreSQL in batches
- Transform data (format conversions)
- Load to MongoDB with upsert
- Handle errors per batch
- Log all operations
**Verification:**
- Test run on 1000 records
- Logs complete and accurate
**Files:** scripts/migrate_users.py

### Step 5: [VALIDATION] Build validation suite
**Dependencies:** Step 4
**Approach:**
- Count records match
- Spot-check data integrity
- Verify relationships intact
- Check constraint compliance
- Performance benchmarks
**Verification:**
- All validations pass on test data
**Files:** scripts/validate_migration.py

### Step 6: [DRY-RUN] Execute full dry run
**Dependencies:** Steps 4, 5
**Approach:**
- Run migration on production-like data
- Full validation
- Performance timing
- Document any issues
**Verification:**
- 100% record count match
- < 1% validation errors (investigate)
- Migration completes in < 4 hours
**Files:** reports/dry_run_results.md

### Step 7: [OPTIMIZE] Optimize based on dry run
**Dependencies:** Step 6
**Approach:**
- Fix any data transformation bugs
- Tune batch sizes
- Optimize slow queries
- Add parallelization if needed
**Verification:**
- Re-run dry run validates fixes
**Files:** scripts/migrate_users_v2.py

### Step 8: [PREPARE] Production migration setup
**Dependencies:** Step 7
**Approach:**
- Schedule maintenance window
- Notify users
- Prepare rollback scripts
- Set up real-time monitoring
- Brief on-call team
**Verification:**
- Rollback tested on staging
- Monitoring alerts configured
**Files:** runbooks/production_migration.md

### Step 9: [EXECUTE] Run production migration
**Dependencies:** Step 8
**Approach:**
- Start maintenance window
- Run migration (with live monitoring)
- Validate continuously
- Generate reports
- Close maintenance window
**Verification:**
- All records migrated
- Validation 100% pass
- No errors in logs
**Files:** [live execution]

### Step 10: [VERIFY] Post-migration verification
**Dependencies:** Step 9
**Approach:**
- Application smoke tests
- User acceptance spot checks
- Performance monitoring
- Support ticket monitoring
- Keep legacy on standby for 48h
**Verification:**
- No critical issues for 48 hours
- Support tickets normal levels
**Files:** reports/post_migration.md

### Step 11: [CLEANUP] Legacy decommission
**Dependencies:** Step 10
**Approach:**
- Archive legacy data
- Update documentation
- Remove legacy code paths
- Decommission legacy database
**Verification:**
- Archive accessible
- No code references to legacy
**Files:** [cleanup tasks]

## Risk Analysis
**Blockers:**
- Data corruption during migration
- Migration takes longer than maintenance window
- Validation fails on critical records
**Mitigation:**
- Extensive dry runs
- Rollback tested and ready
- Can migrate in phases if needed

## Rollback Plan
**If migration fails:**
1. Stop migration script
2. Restore application to use legacy DB
3. Investigate and fix
4. Schedule retry
**If data issues discovered post-migration:**
- Have rollback script to restore legacy
- Can re-run specific record fixes
```

---

## Example 4: Debugging / Investigation

**Task:** "Investigate why API latency spiked last week"

```markdown
## Task
Find root cause of API latency increase from 100ms to 800ms p99 starting March 15th.

## Plan

### Step 1: [DATA] Gather metrics and logs
**Dependencies:** None
**Approach:**
- Pull latency graphs from March 10-20
- Get server resource usage (CPU, memory, I/O)
- Database query performance logs
- Error rates during same period
- Deployment history
**Verification:**
- Have access to all needed data sources
- Data covers relevant time window
**Files:** data/metrics_march10_20.json

### Step 2: [ANALYSIS] Identify correlation points
**Dependencies:** Step 1
**Approach:**
- Mark when latency spike started (March 15)
- Check what changed that day:
  - Code deployments
  - Infrastructure changes
  - Traffic patterns
  - Database migrations
**Verification:**
- Clear timeline of events
**Files:** analysis/timeline.md

### Step 3: [HYPOTHESIS] Form initial hypotheses
**Dependencies:** Step 2
**Approach:**
- H1: Recent deployment introduced regression
- H2: Database query plan changed
- H3: New traffic pattern overwhelming cache
- H4: Infrastructure degradation
**Verification:**
- Each hypothesis is testable
**Files:** analysis/hypotheses.md

### Step 4: [TEST] Test deployment hypothesis
**Dependencies:** Step 3
**Approach:**
- Review commits deployed March 15
- Check for suspicious changes
- Look at performance-related PRs
- Check if rollback correlates with improvement
**Verification:**
- Can identify specific commits
**Files:** analysis/deployment_review.md

### Step 5: [TEST] Test database hypothesis
**Dependencies:** Step 3
**Approach:**
- Identify slow queries during spike period
- Compare query plans before/after March 15
- Check for missing indexes
- Verify table statistics updated
**Verification:**
- EXPLAIN plans for slow queries
**Files:** analysis/query_analysis.md

### Step 6: [TEST] Test traffic pattern hypothesis
**Dependencies:** Step 3
**Approach:**
- Compare request patterns March 10 vs 15
- Check for new high-volume endpoints
- Verify cache hit rates
- Look for request amplification
**Verification:**
- Traffic analysis complete
**Files:** analysis/traffic_analysis.md

### Step 7: [ANALYSIS] Determine root cause
**Dependencies:** Steps 4, 5, 6
**Approach:**
- Compare evidence for each hypothesis
- Identify which hypothesis best explains data
- Document confidence level
- Note contributing factors
**Verification:**
- Can explain why this cause, not others
**Files:** analysis/root_cause.md

### Step 8: [FIX] Implement fix
**Dependencies:** Step 7
**Approach:**
- Code fix / config change / infrastructure fix
- Include tests
- Plan deployment
**Verification:**
- Fix validated in staging
**Files:** [PR with fix]

### Step 9: [VERIFY] Confirm fix in production
**Dependencies:** Step 8
**Approach:**
- Deploy fix
- Monitor latency metrics
- Confirm return to baseline
**Verification:**
- P99 latency back to < 150ms
**Files:** [monitoring dashboard]

### Step 10: [DOCUMENT] Post-mortem
**Dependencies:** Step 9
**Approach:**
- Timeline of incident
- Root cause analysis
- Impact assessment
- Action items to prevent recurrence
**Verification:**
- Shared with team
- Action items assigned
**Files:** docs/post_mortems/2024_03_latency_spike.md

## Risk Analysis
**Blockers:**
- Logs may have been rotated
- Multiple causes might be interacting
**Mitigation:**
- Check backup systems for older logs
- Test hypotheses incrementally

## Rollback Plan
**If investigation stalls:**
- Can implement temporary mitigations (caching, rate limiting)
- Escalate to senior engineers
- Consider infrastructure scaling as band-aid
```

---

## Best Practice Checklist

Before executing any plan, verify:

- [ ] Steps are in logical order
- [ ] Each step has clear verification criteria
- [ ] Dependencies are realistic
- [ ] No step is too large (can be completed in one sitting)
- [ ] Rollback plan exists
- [ ] Risks identified and mitigated
- [ ] Someone else could follow this plan

**If you can't check all boxes, revise the plan.**
