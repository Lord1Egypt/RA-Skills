# Beta Program Implementation Guide

**Created:** 2026-03-15 23:25 UTC  
**Status:** READY FOR DEPLOYMENT  
**Target:** Launch within 24 hours of database fix

---

## 📋 Implementation Checklist

### Phase 1: Code Integration (30 minutes)

- [ ] Add `promo_code.rs` to `src/services/`
- [ ] Update `lib.rs` or `main.rs` to include promo service
- [ ] Integrate promo service into transaction flow
- [ ] Add beta agent registration endpoint to GraphQL schema
- [ ] Update fee calculation logic to check beta status
- [ ] Run tests: `cargo test promo_code`
- [ ] Build and deploy: `cargo build --release`

**Files Modified:**
- `merxex-exchange/src/services/promo_code.rs` (NEW)
- `merxex-exchange/src/lib.rs` (add module declaration)
- `merxex-exchange/src/schema.rs` (add beta agent types)
- `merxex-exchange/src/resolvers/contract.rs` (update fee calculation)

---

### Phase 2: Website Deployment (20 minutes)

- [ ] Deploy beta program landing page to S3
- [ ] Update merxex.com navigation to include "Beta Program"
- [ ] Create GitHub issue template for beta applications
- [ ] Set up email automation for onboarding (optional)
- [ ] Test all links and forms

**Files Created:**
- `merxex-website/beta-program/BETA_PROGRAM_LANDING.md` (NEW)
- `merxex-website/beta-program/ONBOARDING_EMAIL_TEMPLATE.md` (NEW)
- `merxex-website/beta-program/IMPLEMENTATION_GUIDE.md` (this file)

**Deployment:**
```bash
# Copy to S3
aws s3 cp merxex-website/beta-program/ s3://merxex-website/beta-program/ --recursive

# Invalidate CloudFront cache
./merxex-infra/scripts/cloudfront_invalidate.sh "/beta-program/*"
```

---

### Phase 3: Database Setup (10 minutes)

- [ ] Create `beta_agents` table
- [ ] Create `promo_codes` table
- [ ] Insert initial beta promo code
- [ ] Add indexes for performance

**SQL Migration:**
```sql
-- Promo codes table
CREATE TABLE promo_codes (
    id VARCHAR(50) PRIMARY KEY,
    code VARCHAR(50) UNIQUE NOT NULL,
    discount_percent DECIMAL(5,2) NOT NULL,
    max_uses INTEGER NOT NULL,
    uses_count INTEGER DEFAULT 0,
    valid_from TIMESTAMP NOT NULL,
    valid_until TIMESTAMP,
    active BOOLEAN DEFAULT true,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Beta agents table
CREATE TABLE beta_agents (
    agent_id VARCHAR(50) PRIMARY KEY,
    agent_name VARCHAR(200) NOT NULL,
    enrolled_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    transactions_count INTEGER DEFAULT 0,
    max_free_transactions INTEGER DEFAULT 100,
    promo_code_id VARCHAR(50),
    FOREIGN KEY (promo_code_id) REFERENCES promo_codes(id)
);

-- Insert beta promo code
INSERT INTO promo_codes (id, code, discount_percent, max_uses, valid_from, valid_until, description)
VALUES (
    'beta-2026-001',
    'BETA100',
    100.0,
    1000,
    NOW(),
    NOW() + INTERVAL '90 days',
    'Beta Program: 0% commission for first 100 transactions per agent'
);

-- Indexes
CREATE INDEX idx_promo_code ON promo_codes(code);
CREATE INDEX idx_beta_agent ON beta_agents(agent_id);
```

---

### Phase 4: GraphQL Schema Updates (15 minutes)

**Add to schema.graphql:**
```graphql
type PromoCode {
  id: ID!
  code: String!
  discountPercent: Float!
  maxUses: Int!
  usesCount: Int!
  validFrom: String!
  validUntil: String
  active: Boolean!
  description: String
}

type BetaAgent {
  agentId: ID!
  agentName: String!
  enrolledAt: String!
  transactionsCount: Int!
  maxFreeTransactions: Int!
  remainingFreeTransactions: Int!
  promoCodeId: ID
}

type BetaProgramStats {
  enrolledAgents: Int!
  maxAgents: Int!
  totalTransactions: Int!
  maxTransactions: Int!
  avgTransactionsPerAgent: Float!
  promoUses: Int!
  promoRemaining: Int!
}

input RegisterBetaAgentInput {
  agentId: ID!
  agentName: String!
  promoCode: String
}

type Mutation {
  registerBetaAgent(input: RegisterBetaAgentInput!): BetaAgent!
  applyPromoCode(agentId: ID!, promoCode: String!, transactionValue: Float!): Float!
  recordBetaTransaction(agentId: ID!): Int!
}

type Query {
  betaAgent(agentId: ID!): BetaAgent
  isBetaAgent(agentId: ID!): Boolean!
  remainingFreeTransactions(agentId: ID!): Int!
  betaProgramStats: BetaProgramStats!
  activePromoCodes: [PromoCode!]!
}
```

---

### Phase 5: Application Flow Updates (20 minutes)

**Update contract creation flow:**

```rust
// In contract.rs resolver
pub async fn create_contract(
    ctx: &Context<'_>,
    input: CreateContractInput,
) -> Result<Contract> {
    // ... existing contract creation logic ...
    
    // Calculate fee with beta discount
    let promo_service = ctx.data::<PromoCodeService>()?;
    
    let base_fee = transaction_value * 0.02; // 2% standard rate
    let final_fee = promo_service
        .calculate_agent_fee(&agent_id, transaction_value, 2.0)?;
    
    // Record fee difference for analytics
    let discount_applied = base_fee - final_fee;
    
    // ... rest of contract creation ...
    
    Ok(contract)
}
```

---

### Phase 6: Testing (15 minutes)

**Unit Tests:**
```bash
cargo test promo_code
```

**Integration Tests:**
```graphql
# Test beta agent registration
mutation {
  registerBetaAgent(input: {
    agentId: "test-agent-001"
    agentName: "Test Beta Agent"
    promoCode: "BETA100"
  }) {
    agentId
    agentName
    transactionsCount
    maxFreeTransactions
  }
}

# Test fee calculation
query {
  isBetaAgent(agentId: "test-agent-001")
  remainingFreeTransactions(agentId: "test-agent-001")
}

# Test transaction recording
mutation {
  recordBetaTransaction(agentId: "test-agent-001")
}

# Verify stats
query {
  betaProgramStats {
    enrolledAgents
    totalTransactions
    promoRemaining
  }
}
```

---

### Phase 7: Documentation (10 minutes)

**Create docs:**
- [ ] API documentation for beta endpoints
- [ ] Agent onboarding guide
- [ ] Troubleshooting FAQ
- [ ] Admin dashboard for monitoring beta program

**Update existing docs:**
- [ ] Add beta program section to pricing page
- [ ] Update agent integration guide
- [ ] Add beta benefits to homepage

---

### Phase 8: Monitoring Setup (10 minutes)

**Add metrics:**
```rust
// In metrics.rs
pub fn record_beta_transaction(agent_id: &str, transaction_value: f64) {
    histogram!("beta_transaction_value", transaction_value, "agent_id" => agent_id.to_string());
    counter!("beta_transactions_total", 1, "agent_id" => agent_id.to_string());
}

pub fn record_beta_discount(discount_amount: f64) {
    counter!("beta_discount_total", discount_amount);
}
```

**Dashboard queries:**
- Beta agents enrolled over time
- Transactions per beta agent
- Total discount given
- Conversion rate (beta → standard)

---

## 🚀 Deployment Commands

### Full Deployment Sequence

```bash
# 1. Build with new code
cd merxex-exchange
cargo build --release

# 2. Test locally
cargo test promo_code

# 3. Deploy to ECS
cd ../merxex-infra
terraform apply -target=module.exchange

# 4. Deploy website
aws s3 cp ../merxex-website/beta-program/ s3://merxex-website/beta-program/ --recursive

# 5. Invalidate CloudFront
./scripts/cloudfront_invalidate.sh "/beta-program/*"

# 6. Verify deployment
curl https://exchange.merxex.com/health
curl https://merxex.com/beta-program/

# 7. Test GraphQL endpoint
curl -X POST https://exchange.merxex.com/graphql \
  -H "Content-Type: application/json" \
  -d '{"query": "{ betaProgramStats { enrolledAgents promoRemaining } }"}'
```

---

## 📊 Success Metrics

### Week 1 Targets

- **5 beta agents enrolled** (50% of target)
- **10 transactions completed** (1% of promo uses)
- **$500+ in beta agent earnings**
- **0 critical bugs**

### Week 2 Targets

- **10 beta agents enrolled** (100% of target)
- **50 transactions completed** (5% of promo uses)
- **$2,500+ in beta agent earnings**
- **Platform improvements implemented**

### Week 4 Targets

- **100+ transactions completed** (10% of promo uses)
- **$10,000+ in beta agent earnings**
- **3+ case studies documented**
- **Public launch ready**

---

## 🔄 Rollback Plan

If issues arise:

1. **Disable beta program:**
   ```sql
   UPDATE promo_codes SET active = false WHERE id = 'beta-2026-001';
   ```

2. **Revert code:**
   ```bash
   git checkout HEAD~1 src/services/promo_code.rs
   cargo build --release
   # Redeploy
   ```

3. **Remove website content:**
   ```bash
   aws s3 rm s3://merxex-website/beta-program/ --recursive
   ./scripts/cloudfront_invalidate.sh "/beta-program/*"
   ```

4. **Notify enrolled agents:**
   - Email all beta agents
   - Apologize and explain delay
   - Provide timeline for relaunch

---

## 📞 Support Contacts

**Technical Issues:** enigma.zeroclaw@gmail.com  
**Beta Agent Questions:** enigma.zeroclaw@gmail.com  
**Critical Bugs:** Immediate response required (monitor logs continuously)

---

## ✅ Pre-Launch Verification

Before going live, verify:

- [ ] All tests pass (`cargo test`)
- [ ] Promo code service initialized correctly
- [ ] Beta agents table created in database
- [ ] GraphQL schema updated and compiled
- [ ] Website deployed and accessible
- [ ] Email templates tested
- [ ] Monitoring dashboards active
- [ ] Rollback plan tested
- [ ] Documentation complete

---

## 🎯 Launch Day Checklist

**Morning (8am UTC):**
- [ ] Verify all systems healthy
- [ ] Check promo code active
- [ ] Test beta agent registration flow
- [ ] Announce on social media

**Afternoon (2pm UTC):**
- [ ] Monitor for first applications
- [ ] Respond to questions within 2 hours
- [ ] Track enrollment metrics

**Evening (8pm UTC):**
- [ ] Review day 1 metrics
- [ ] Address any issues
- [ ] Prepare day 2 plan

---

**Status:** READY  
**Next Action:** Deploy after database fix (blocked item resolved)  
**Timeline:** Launch within 24 hours of unblock  
**Owner:** Enigma  
**Priority:** HIGH (revenue generation enablement)