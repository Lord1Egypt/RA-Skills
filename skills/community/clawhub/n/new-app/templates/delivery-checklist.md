# Internal App Delivery Checklist

## Documentation

- [ ] Requirements summary is written and approved
- [ ] Architecture proposal is documented and confirmed
- [ ] English docs are updated
- [ ] Chinese docs are updated
- [ ] Runtime configuration is documented

## Implementation

- [ ] Frontend structure is established
- [ ] Backend structure is established
- [ ] Core domain models are implemented
- [ ] Core workflows are implemented end to end
- [ ] Auth integration is complete or explicitly deferred
- [ ] Database strategy is implemented
- [ ] Storage strategy is implemented or stubbed intentionally

## Operations

- [ ] Local startup steps are documented
- [ ] Dev tasks or commands exist for common operations
- [ ] Migrations are in place if shared or production databases are involved
- [ ] Diagnostics or health checks exist for critical runtime dependencies

## Validation

- [ ] Frontend build passes
- [ ] Backend sanity checks pass
- [ ] Representative workflows were manually verified
- [ ] Auth flow was validated if applicable
- [ ] Database or migration state was validated if applicable

## Handoff

- [ ] Known risks and follow-up items are listed
- [ ] Next steps are clear
- [ ] The delivered scope matches the agreed MVP
