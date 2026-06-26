# Graph Rule Engine - Real-World Examples

Comprehensive examples of rule-based reasoning applied to knowledge graphs across different domains.

## 1. Organizational Hierarchy - Manager Inference

### Scenario
Derive manager relationships transitively to understand reporting chains.

### Graph Schema

**Nodes:**
- Alice, Bob, Charlie, Diana, Eve (employees)
- CEO, VP_Engineering, Manager (roles)

**Relationships:**
```
Alice --REPORTS_TO--> Bob
Bob --REPORTS_TO--> Charlie
Charlie --REPORTS_TO--> Diana
Diana --REPORTS_TO--> CEO
```

### Rule: Transitive Manager Chain

**Rule Definition:**
```
Rule Name: manager_chain_inference
Type: derivation
Priority: 100

Condition (IF):
  MATCH (emp1:Employee)-[:REPORTS_TO]->(mgr1:Employee)
  MATCH (mgr1)-[:REPORTS_TO]->(mgr2:Employee)
  WHERE emp1 != mgr2

Inference (THEN):
  CREATE (emp1)-[:REPORTS_INDIRECTLY_TO]->(mgr2)

Constraints:
  Cycle Detection: true
  Max Depth: 10
  Materialization: true
```

### Execution Results

```json
{
  "rule_name": "manager_chain_inference",
  "matches_found": 6,
  "inferred_relationships": [
    {"source": "Alice", "target": "Charlie", "type": "REPORTS_INDIRECTLY_TO", "depth": 2},
    {"source": "Alice", "target": "Diana", "type": "REPORTS_INDIRECTLY_TO", "depth": 3},
    {"source": "Alice", "target": "CEO", "type": "REPORTS_INDIRECTLY_TO", "depth": 4},
    {"source": "Bob", "target": "Diana", "type": "REPORTS_INDIRECTLY_TO", "depth": 2},
    {"source": "Bob", "target": "CEO", "type": "REPORTS_INDIRECTLY_TO", "depth": 3},
    {"source": "Charlie", "target": "CEO", "type": "REPORTS_INDIRECTLY_TO", "depth": 2}
  ],
  "inference_time_ms": 45,
  "fixpoint_iterations": 3
}
```

---

## 2. Fraud Detection - Transaction Cycles

### Scenario
Detect fraudulent circular transfer patterns indicating money laundering.

### Graph Schema

**Nodes:**
- Account_A, Account_B, Account_C, Account_D (bank accounts)

**Relationships:**
```
Account_A --TRANSFERRED_TO--> Account_B
Account_B --TRANSFERRED_TO--> Account_C
Account_C --TRANSFERRED_TO--> Account_D
Account_D --TRANSFERRED_TO--> Account_A
```

### Rule: Circular Transfer Detection

**Rule Definition:**
```
Rule Name: circular_transfer_detection
Type: constraint
Priority: 200
Severity: HIGH

Condition (IF):
  MATCH (a:Account)-[:TRANSFERRED_TO]->(b:Account)
  MATCH (b)-[:TRANSFERRED_TO]->(c:Account)
  MATCH (c)-[:TRANSFERRED_TO]->(d:Account)
  MATCH (d)-[:TRANSFERRED_TO]->(a)
  WHERE NOT EXISTS (a)-[:LEGITIMATE_CYCLE]->(a)

Inference (THEN):
  Flag(SuspiciousTransferCycle, 
    accounts=[a, b, c, d], 
    risk_level=HIGH,
    confidence=0.95)

Constraints:
  Check Whitelist: legitimate_transfers
  Min Transfer Amount: $1000
```

### Execution Results

```json
{
  "rule_name": "circular_transfer_detection",
  "matches_found": 1,
  "violations_flagged": [
    {
      "violation_id": "FraudAlert_001",
      "type": "SuspiciousTransferCycle",
      "accounts_involved": ["Account_A", "Account_B", "Account_C", "Account_D"],
      "risk_level": "HIGH",
      "confidence": 0.95,
      "total_amount": 45000,
      "cycle_detected": true,
      "recommendation": "Block transactions and investigate"
    }
  ],
  "validation_time_ms": 120
}
```

---

## 3. E-Commerce - Product Recommendations

### Scenario
Generate product recommendations using collaborative filtering rules.

### Graph Schema

**Entities:**
- Users: User1, User2, User3, User4
- Products: Laptop, Monitor, Mouse, Keyboard
- Categories: Electronics, Accessories

**Relationships:**
```
User1 --PURCHASED--> Laptop (price: $1200)
User1 --PURCHASED--> Monitor (price: $300)
User2 --PURCHASED--> Laptop (price: $1200)
User2 --PURCHASED--> Keyboard (price: $100)
User3 --PURCHASED--> Monitor (price: $300)
Product --BELONGS_TO--> Category
```

### Rule: Collaborative Filtering

**Rule Definition:**
```
Rule Name: product_recommendation_cf
Type: derivation
Priority: 150

Condition (IF):
  MATCH (user1:User)-[:PURCHASED]->(prod1:Product)
  MATCH (user2:User)-[:PURCHASED]->(prod1:Product)
  MATCH (user2)-[:PURCHASED]->(prod2:Product)
  WHERE user1 != user2
  AND NOT EXISTS (user1)-[:PURCHASED]->(prod2)
  AND NOT EXISTS (user1)-[:NOT_INTERESTED_IN]->(prod2)

Inference (THEN):
  CREATE (user1)-[:RECOMMENDATION]->(prod2)
  SET recommendation.source="collaborative_filtering"
  SET recommendation.confidence=0.85

Constraints:
  Min Common Products: 1
  Max Recommendations: 5 per user
```

### Execution Results

```json
{
  "rule_name": "product_recommendation_cf",
  "matches_found": 3,
  "recommendations_generated": [
    {
      "user": "User1",
      "recommended_product": "Keyboard",
      "reason": "User2 bought Laptop and Keyboard",
      "confidence": 0.85,
      "estimated_price": 100,
      "category": "Accessories"
    },
    {
      "user": "User1",
      "recommended_product": "Monitor",
      "reason": "Already purchased",
      "confidence": 1.0,
      "skip_reason": "duplicate"
    },
    {
      "user": "User3",
      "recommended_product": "Laptop",
      "reason": "User1 bought Monitor and Laptop",
      "confidence": 0.85,
      "estimated_price": 1200,
      "category": "Electronics"
    }
  ],
  "inference_time_ms": 89
}
```

---

## 4. Knowledge Base - Geographic Inference

### Scenario
Derive comprehensive geographic relationships from partial data.

### Graph Schema

**Locations:**
- Paris, Lyon (cities in France)
- London (city in UK)
- France, UK (countries)
- Europe (continent)

**Relationships:**
```
Paris --LOCATED_IN--> France
Lyon --LOCATED_IN--> France
London --LOCATED_IN--> UK
France --LOCATED_IN--> Europe
UK --LOCATED_IN--> Europe
```

### Rule: Geographic Transitive Closure

**Rule Definition:**
```
Rule Name: geographic_hierarchy_closure
Type: derivation
Priority: 100

Condition (IF):
  MATCH (place1)-[:LOCATED_IN]->(place2)
  MATCH (place2)-[:LOCATED_IN]->(place3)
  WHERE place1 != place3

Inference (THEN):
  CREATE (place1)-[:LOCATED_IN_REGION]->(place3)

Constraints:
  Max Levels: 5
  Cycle Detection: true
```

### Execution Results

```json
{
  "rule_name": "geographic_hierarchy_closure",
  "matches_found": 4,
  "inferred_relationships": [
    {
      "source": "Paris",
      "target": "Europe",
      "type": "LOCATED_IN_REGION",
      "path_length": 2
    },
    {
      "source": "Lyon",
      "target": "Europe",
      "type": "LOCATED_IN_REGION",
      "path_length": 2
    },
    {
      "source": "London",
      "target": "Europe",
      "type": "LOCATED_IN_REGION",
      "path_length": 2
    }
  ],
  "hierarchy_depth": 3,
  "total_inferred": 3
}
```

---

## 5. Compliance - Age-Based Classification

### Scenario
Classify users based on age to enforce compliance rules.

### Graph Schema

**Users:**
- User_Alice (born: 1990)
- User_Bob (born: 2005)
- User_Carol (born: 1960)

**Relationships:**
```
User_Alice --DOB--> 1990
User_Bob --DOB--> 2005
User_Carol --DOB--> 1960
```

### Rule: Age-Based Compliance Rules

**Rule Definition:**
```
Rule Name: age_based_classification
Type: conditional
Priority: 120

Condition (IF):
  MATCH (user:User)-[:DOB]->(year:Integer)
  WHERE (current_year - year) >= 18
  AND (current_year - year) < 65

Inference (THEN):
  CREATE (user)-[:COMPLIANCE_STATUS]->(Eligible)
  CREATE (user)-[:AGE_CATEGORY]->(Adult)

Condition (IF):
  MATCH (user:User)-[:DOB]->(year:Integer)
  WHERE (current_year - year) >= 65

Inference (THEN):
  CREATE (user)-[:COMPLIANCE_STATUS]->(Senior)
  CREATE (user)-[:AGE_CATEGORY]->(Senior)
  CREATE (user)-[:ELIGIBLE_FOR]->(SeniorBenefits)

Constraints:
  Must Pass Validation: true
```

### Execution Results

```json
{
  "rule_name": "age_based_classification",
  "execution_date": "2026-04-12",
  "matches_found": 3,
  "classifications": [
    {
      "user": "User_Alice",
      "age": 36,
      "classification": "Adult",
      "compliance_status": "Eligible",
      "eligible_for": []
    },
    {
      "user": "User_Bob",
      "age": 21,
      "classification": "Adult",
      "compliance_status": "Eligible",
      "eligible_for": []
    },
    {
      "user": "User_Carol",
      "age": 66,
      "classification": "Senior",
      "compliance_status": "Senior",
      "eligible_for": ["SeniorBenefits"]
    }
  ],
  "inference_time_ms": 52
}
```

---

## 6. Data Quality - Validation Rules

### Scenario
Validate data quality and flag inconsistencies.

### Graph Schema

**Entities:**
- Company: TechCorp
- Employee: Alice, Bob
- Department: Engineering

**Relationships:**
```
Alice --WORKS_AT--> TechCorp
Bob --WORKS_AT--> TechCorp
Alice --WORKS_IN--> Engineering
Bob --WORKS_IN--> Engineering

TechCorp --HAS_OFFICE--> SanFrancisco
SanFrancisco --CITY--> USA
```

### Rule: Data Consistency Validation

**Rule Definition:**
```
Rule Name: employee_company_consistency
Type: constraint
Priority: 180

Condition (IF):
  MATCH (emp:Employee)-[:WORKS_AT]->(company:Company)
  MATCH (emp)-[:WORKS_IN]->(dept:Department)
  MATCH (company)-[:HAS_OFFICE]->(office:Office)
  WHERE NOT EXISTS (dept)-[:LOCATED_AT]->(office)

Inference (THEN):
  Flag(DataInconsistency,
    issue="Employee department not located in company office",
    severity=MEDIUM,
    elements=[emp, company, dept, office])

Constraints:
  Ignore Whitelist: remote_workers
```

### Execution Results

```json
{
  "rule_name": "employee_company_consistency",
  "matches_found": 0,
  "inconsistencies_flagged": [],
  "data_quality_score": 1.0,
  "validation_report": {
    "total_validations": 2,
    "passed": 2,
    "failed": 0,
    "warnings": 0
  }
}
```

---

## Common Rule Patterns

### Pattern 1: Transitive Closure
```
IF (a)-[REL]->(b) AND (b)-[REL]->(c)
THEN (a)-[REL_CLOSURE]->(c)
```

Use: Hierarchies, geographic nesting, organizational chains

### Pattern 2: Co-occurrence Inference
```
IF (entity1)-[REL]->(common) AND (entity2)-[REL]->(common)
THEN (entity1)-[RELATED_TO]->(entity2)
```

Use: Recommendations, similarity, collaboration networks

### Pattern 3: Conditional Classification
```
IF (entity.property > threshold)
THEN (entity)-[CLASSIFICATION]->(Category)
```

Use: Segmentation, categorization, compliance

### Pattern 4: Anomaly Detection
```
IF (pattern matches suspicious criteria)
THEN Flag(Anomaly, severity, confidence)
```

Use: Fraud, security, quality monitoring

### Pattern 5: Aggregation & Metrics
```
IF aggregate(count(matches)) > threshold
THEN (entity.metric = computed_value)
```

Use: Analytics, KPIs, summarization

---

## Rule Execution Best Practices

### 1. Rule Testing
```
Before Deployment:
✓ Test on sample data
✓ Validate inferred results
✓ Check for cycles
✓ Measure performance
✓ Verify constraints
```

### 2. Incremental Execution
```
Strategy:
1. Execute simple rules first (fast, high confidence)
2. Build on results with complex rules
3. Validate intermediate results
4. Materialize high-value inferences only
```

### 3. Performance Optimization
```
Techniques:
- Index properties used in rule conditions
- Order rules by cost (cheap first)
- Use priorities to skip unnecessary rules
- Apply incremental updates on data changes
```

### 4. Monitoring & Debugging
```
Track:
- Rule execution time
- Inference counts
- Cycle detection triggers
- Conflict resolution choices
- Materialization status
```

---

**Rule engines are essential for:**
- Automatic knowledge derivation
- Compliance and validation
- Recommendation systems
- Fraud detection
- Data quality management
- Semantic reasoning


