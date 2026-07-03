# Problem Diagnosis Decision Tree (Problem Diagnosis Decision Tree)

> Instructions: When a client describes a vague problem ("the system is slow" / "IT costs are too high" / "data is unusable"), use this decision tree to quickly find root cause direction and corresponding solution path. Don't jump directly from problem to solution.

---

## Decision Tree Overview

```
Client says: "[vague problem]"
    │
    ├── Can the problem be quantified?
    │   ├── Yes → Enter [Quantified Diagnosis Path]
    │   └── No → First do [Problem Clarification] (using 5W1H)
    │
    ├── What is the essence of the problem? (MECE Five-Dimensional Decomposition) → See classification tree below
    │
    └── Quickly locate → Enter corresponding workflow
```

---

## Category 1: "The system is too slow" / "Performance is poor"

```
"The system is too slow"
    │
    ├── When is it slow?
    │   ├── Always slow → 
    │   │   ├── Everyone slow? → Infrastructure/Architecture issue → workflow 02-03 (IT Diagnosis)
    │   │   └── Some people slow? → Network/Region/Permission issue
    │   │
    │   └── Sometimes slow (intermittent) →
    │       ├── Slow during peak? → Insufficient capacity → Scale up or architecture optimization
    │       ├── Specific operations slow? → Specific API/Query/Database → Locate to specific code
    │       └── Randomly slow? → External dependencies/GC/Resource contention → Observability investigation
    │
    ├── Where is it slow?
    │   ├── Frontend rendering slow? → Frontend performance optimization (Reduce Bundle/Lazy loading)
    │   ├── API response slow? → Backend logic/Database query/Dependent services
    │   ├── Database query slow? → Index/Query optimization/Data volume
    │   └── Network transmission slow? → CDN/Bandwidth/Data compression
    │
    └── Compared to what is it "slow"?
        ├── Slower than last year? → Data volume growth/User growth/Technical debt accumulation
        ├── Slower than competitors? → Architecture gap/Technology selection gap
        └── Slower than expected? → Requirements vs actual/Benchmark testing
```

---

## Category 2: "IT costs are too high"

```
"IT costs are too high"
    │
    ├── Which type of cost is high?
    │   ├── Too many people? → Organization diagnosis → workflow 02-03
    │   │   ├── Reasonable headcount but low efficiency? → Automation/Tools/Processes
    │   │   └── Outsourcing ratio too high? → Insourcing/Vendor renegotiation
    │   │
    │   ├── Infrastructure/Cloud costs? → FinOps assessment → workflow 05-03
    │   │   ├── No tags/Don't know where money is spent? → Phase 1: Inform
    │   │   ├── Know where but don't know how to optimize? → Phase 2: Optimize
    │   │   └── Optimized but still expensive? → Architecture optimization/Vendor renegotiation
    │   │
    │   ├── Software licenses? → License audit + optimization
    │   │   ├── Any idle licenses? → Reclaim
    │   │   ├── Premium features unused? → Downgrade
    │   │   └── Contract expiring soon? → Renegotiate
    │   │
    │   ├── Projects/Vendors? → Vendor management → workflow 07-02
    │   │   ├── Vendor quotes inflated? → Benchmark comparison + negotiation
    │   │   ├── Change request costs out of control? → Change management process
    │   │   └── SLA premium but poor service? → Downgrade SLA or switch vendors
    │   │
    │   └── Don't know which type—all high? → Comprehensive IT cost diagnosis → workflow 05-01
    │
    ├── Compared to what is it "high"?
    │   ├── Higher than last year? → Growth reasonableness (User/Business growth?)
    │   ├── Higher than industry benchmark? → Benchmarking analysis → references/benchmark-data-and-industry-metrics.md
    │   └── Higher than budget? → Budget execution issues/Hidden costs
    │
    └── What is the context?
        ├── IT investment increased but business value didn't? → ROI issue → workflow 05-02
        ├── IT investment increase is strategic need (digital transformation)? → Ensure business case exists
        └── IT investment reduction (cost pressure)? → Cost optimization → workflow 05-03
```

---

## Category 3: "Data is unusable" / "Poor data quality"

```
"Data is unusable"
    │
    ├── What kind of "unusable"?
    │   ├── Can't find data? → Data assets not discoverable → workflow 03-05 (Data Strategy)
    │   │   └── Need Data Catalog + Metadata Management
    │   │
    │   ├── Found but don't know what it means? → Data dictionary/Metadata missing
    │   │
    │   ├── Data inaccurate? → Data quality issues
    │   │   ├── Which data is inaccurate? → List
    │   │   ├── Reasons for inaccuracy? → 
    │   │   │   ├── Wrong at source? → Entry/Collection issues
    │   │   │   ├── Different data across systems? → Master data inconsistency → MDM
    │   │   │   ├── Data outdated? → Timeliness issues
    │   │   │   └── Processing errors? → ETL/Calculation logic errors
    │   │   └── Enter data quality improvement process → workflow 03-05
    │   │
    │   ├── Data in different places/not interconnected? → Data silos
    │   │   └── Data integration/Data platform architecture → workflow 03-05
    │   │
    │   └── Have data but don't know how to use it (analytics/AI)? → Data analytics capability → workflow 03-05
    │
    └── Who is complaining?
        ├── Business personnel (need data for decisions) → Self-service analytics/Data democratization
        ├── Data scientists (need data to train models) → Data readiness + Feature engineering
        └── Regulatory/Compliance (data non-compliant) → Data governance + Compliance
```

---

## Category 4: "Digital/IT doesn't support the business"

```
"IT doesn't support the business"
    │
    ├── What does this mean?
    │   ├── IT response too slow? (2 months for a report)
    │   │   ├── Too many requirements? → Requirement prioritization + Product-oriented operation
    │   │   ├── IT capacity insufficient? → Resources/Efficiency/Outsourcing
    │   │   └── Process too cumbersome? → Agile transformation/DevOps
    │   │
    │   ├── IT builds things the business doesn't need? (Built but no one uses)
    │   │   ├── Requirements not aligned? → Product management/BA capability
    │   │   ├── Communication issues? → IT-Business collaboration mechanism
    │   │   └── No early business involvement? → Involve business from the start
    │   │
    │   ├── IT doesn't understand the business? 
    │   │   └── IT organization design issue → workflow 06-02 (IT Organization Design)
    │   │
    │   ├── IT technology too old, can't keep up with business needs?
    │   │   └── Architecture modernization → workflow 03-03 (Enterprise Architecture)
    │   │
    │   └── IT strategic direction misaligned with business direction?
    │       └── IT strategy realignment → workflow 03-01 (IT Strategy Planning)
    │
    └── Is this perception or fact?
        ├── Perception (but widespread) → Need objective diagnosis (workflow 02-03) to find real gaps
        └── Fact (data-supported) → Understand root cause before developing solution
```

---

## Category 5: "Security concerns" / "Afraid of incidents"

```
"We lack confidence in our security"
    │
    ├── Why lack confidence?
    │   ├── Had incidents? → What type?
    │   │   ├── Data breach → Data security + DLP
    │   │   ├── Ransomware → Backup + Endpoint security + Security awareness
    │   │   ├── Phishing succeeded → Security awareness training + Phishing tests
    │   │   └── Insider threat → Permission management + Audit
    │   │
    │   ├── No incidents but feel unsafe?
    │   │   ├── Don't know what vulnerabilities exist? → Penetration testing + Vulnerability scanning
    │   │   ├── Compliance requirements tightened? → Classified Protection/ISO27001/SOC2
    │   │   ├── Saw peers have incidents? → Risk assessment + Benchmarking
    │   │   └── Regulator inspection coming? → Compliance assessment → workflow 03-06
    │   │
    │   ├── Vendor/Third-party risk?
    │   │   └── Supply chain security → workflow 03-06
    │   │
    │   └── OT (Industrial Control) security? (Manufacturing/Energy)
    │       └── OT/IT security convergence → workflow 03-06
    │
    └── Enter security strategy workflow → workflow 03-06
```

---

## Category 6: "Want to do AI but don't know how to start"

```
"We want to do AI" / "What can AI help us do"
    │
    ├── Why do you want to do AI?
    │   ├── Boss said to do it (AI tourism) → First do AI literacy + Use case workshop
    │   ├── Competitors are doing it → Competitive analysis + Differentiated AI strategy
    │   ├── Indeed has business problems suitable for AI → ✅ Correct starting point
    │   └── Don't know, just feel we should → Start with AI maturity assessment
    │
    ├── What do you want to solve with AI?
    │   ├── Has clear problem → Enter AI use case evaluation → workflow 03-02
    │   ├── Can't articulate → AI Discovery Workshop
    │   └── "Everything can be done" → Help focus, select 1-2 highest-value scenarios
    │
    ├── Is the data ready?
    │   ├── Has data and quality is good → ✅ Ready to start
    │   ├── Has data but poor quality → Do data governance first → workflow 03-05
    │   ├── No data (scenario needs data that doesn't exist) → First establish data collection
    │   └── Don't know if we have it → Data inventory
    │
    ├── Is technical capability ready?
    │   ├── Has AI/ML team → ✅ 
    │   ├── No team but has cloud platform → Can try cloud AI services (low-code)
    │   ├── Nothing at all → Start with simple scenarios + external support
    │   └── Team wants to learn but doesn't know how → AI literacy training → references/ai-and-business-transformation-framework.md
    │
    └── Enter AI transformation strategy → workflow 03-02
```

---

## Category 7: "Vendor problems"

```
"Vendor problems"
    │
    ├── What problem?
    │   ├── Want to select a vendor but don't know how?
    │   │   └── → workflow 04-02 (RFP Full Process) + 04-03 (Vendor Evaluation)
    │   │
    │   ├── Vendor performance poor?
    │   │   ├── Poor delivery quality? → Vendor performance management → workflow 07-02
    │   │   ├── Delivery delay? → Contract management + Escalation
    │   │   ├── Frequent staff changes? → Contract clause enforcement
    │   │   └── Poor service attitude? → Quarterly Business Review (QBR) + Escalation
    │   │
    │   ├── Vendor fees keep increasing?
    │   │   ├── Reasonable increase (cost increase)? → Negotiate cap
    │   │   ├── Unreasonable increase (lock-in effect)? → Introduce competition/Evaluate alternatives
    │   │   └── Hidden fees keep emerging? → Contract review + Monthly fee review
    │   │
    │   ├── Want to switch vendors?
    │   │   └── → workflow 07-02 (Vendor Exit Management)
    │   │
    │   ├── Vendor being acquired/going bankrupt?
    │   │   └── Immediately conduct risk assessment + Contingency plan + Data backup
    │   │
    │   └── M&A/Due diligence needs technology assessment?
    │       └── → workflow 04-01 (Technology Due Diligence)
```

---

## Usage Process

1. **After hearing the problem**, first map out on the whiteboard/in your mind: "What category does this problem fall into?"
2. **Ask 3-5 clarifying questions** to narrow down the problem scope
3. **Follow the decision tree to find the corresponding deepest node**
4. **Enter the corresponding workflow** and execute step by step
5. **If the problem spans multiple categories** (most real problems are cross-domain), advance in parallel by priority

---

## Key Reminders

- The decision tree is a guide, not iron law — real client problems often have "all 6 of the above"
- Don't give a solution upon hearing the first problem — first ask "Can you give me a specific example?"
- If what the client says doesn't match the decision tree at all — the problem may not have been correctly articulated yet, go back to 5W1H and re-clarify
- The most dangerous is when the client says "system is slow" and you start doing performance optimization — when they actually mean "requirement response is slow" (process issue, not technical issue)
