# Graph Path Reasoning - Real-World Examples

Comprehensive examples of path reasoning analysis across different domains, demonstrating how to find and analyze connections between entities.

## 1. Social Network - Connection Paths

### Scenario
A user wants to understand how they are connected to another user in a social network through mutual connections.

### Graph Schema

**Nodes:**
- Alice, Bob, Charlie, Diana, Eve, Frank (Person nodes)
- TechCorp, StartupAI (Company nodes)

**Relationships:**
```
Alice --FOLLOWS--> Bob (confidence: 0.9)
Bob --FOLLOWS--> Charlie (confidence: 0.85)
Charlie --WORKS_AT--> TechCorp (confidence: 0.95)
Alice --KNOWS--> Diana (confidence: 0.8)
Diana --WORKS_AT--> TechCorp (confidence: 0.95)
TechCorp --PARTNER_OF--> StartupAI (confidence: 0.7)
Frank --FOUNDER_OF--> StartupAI (confidence: 0.99)
Eve --FOLLOWS--> Frank (confidence: 0.88)
```

### Analysis Queries

#### Query 1: Direct vs. Indirect Connections
**Question:** "How is Alice connected to Frank?"

**Analysis:**
```
find_shortest_path(source="Alice", target="Frank")

Path 1: Alice → Eve (direct via mutual connection)? NO
Path 2: Alice → Bob → Charlie → TechCorp → StartupAI → Frank
  Distance: 5 hops
  Confidence: 0.9 * 0.85 * 0.95 * 0.7 * 0.99 = 0.5596

Path 3: Alice → Diana → TechCorp → StartupAI → Frank
  Distance: 4 hops
  Confidence: 0.8 * 0.95 * 0.7 * 0.99 = 0.5292

Shortest: Path 3 (4 hops)
Strongest: Path 3 (confidence 0.5292)
```

**Result:**
```json
{
  "source": "Alice",
  "target": "Frank",
  "shortest_path": ["Alice", "Diana", "TechCorp", "StartupAI", "Frank"],
  "distance": 4,
  "confidence": 0.5292,
  "path_explanation": "Alice knows Diana. Diana works at TechCorp. TechCorp partners with StartupAI. Frank founded StartupAI.",
  "relationship_types": ["knows", "works_at", "partner_of", "founder_of"]
}
```

#### Query 2: Find All Connection Paths
**Question:** "Show me all ways Alice is connected to TechCorp"

**Analysis:**
```
find_all_paths(source="Alice", target="TechCorp", max_length=5)

Path 1: Alice → Bob → Charlie → TechCorp (3 hops)
  Distance: 3, Confidence: 0.9 * 0.85 * 0.95 = 0.7268

Path 2: Alice → Diana → TechCorp (2 hops)
  Distance: 2, Confidence: 0.8 * 0.95 = 0.76
  
Path 3: Alice → Bob → Charlie → TechCorp → (via mutual paths)
```

**Result:**
```json
{
  "source": "Alice",
  "target": "TechCorp",
  "total_paths": 2,
  "paths_ranked_by_distance": [
    {
      "path": ["Alice", "Diana", "TechCorp"],
      "distance": 2,
      "confidence": 0.76,
      "relationship_types": ["knows", "works_at"]
    },
    {
      "path": ["Alice", "Bob", "Charlie", "TechCorp"],
      "distance": 3,
      "confidence": 0.7268,
      "relationship_types": ["follows", "follows", "works_at"]
    }
  ],
  "diversity": "2 independent paths"
}
```

---

## 2. E-Commerce Network - Supply Chain Paths

### Scenario
A retailer wants to understand how they are connected to raw material suppliers through the supply chain.

### Graph Schema

**Entities:**
- Retailers: MegaStore, ShopMart
- Distributors: RegionalDist, NationalDist
- Manufacturers: ApplianceCorp, ElectronicsMfg
- Suppliers: MetalSupply, ComponentSource

**Supply Chain Relationships:**
```
MegaStore --BUYS_FROM--> RegionalDist (lead_time: 2 days, cost: 0.85)
ShopMart --BUYS_FROM--> NationalDist (lead_time: 1 day, cost: 0.9)
RegionalDist --SOURCES_FROM--> ApplianceCorp (lead_time: 5 days, cost: 0.8)
NationalDist --SOURCES_FROM--> ElectronicsMfg (lead_time: 3 days, cost: 0.85)
ApplianceCorp --DEPENDS_ON--> MetalSupply (lead_time: 7 days, cost: 0.75)
ElectronicsMfg --DEPENDS_ON--> ComponentSource (lead_time: 10 days, cost: 0.7)
MetalSupply --SHARES_SUPPLIER--> ComponentSource (lead_time: 0, cost: 1.0)
```

### Analysis Queries

#### Query: Critical Path Analysis
**Question:** "What is the longest lead time path from MegaStore to raw materials?"

**Analysis:**
```
find_all_paths(source="MegaStore", target=["MetalSupply", "ComponentSource"])

Path 1: MegaStore → RegionalDist → ApplianceCorp → MetalSupply
  Total lead time: 2 + 5 + 7 = 14 days
  Cost factor: 0.85 * 0.8 * 0.75 = 0.51

Path 2: MegaStore → RegionalDist → ApplianceCorp → MetalSupply → ComponentSource
  Total lead time: 2 + 5 + 7 + 0 = 14 days
  Cost factor: 0.85 * 0.8 * 0.75 * 1.0 = 0.51
```

**Result:**
```json
{
  "source": "MegaStore",
  "targets": ["MetalSupply", "ComponentSource"],
  "critical_path": ["MegaStore", "RegionalDist", "ApplianceCorp", "MetalSupply"],
  "total_lead_time_days": 14,
  "bottleneck": "ApplianceCorp → MetalSupply (7 days)",
  "cost_factor": 0.51,
  "recommendation": "Establish alternative suppliers to reduce lead time"
}
```

---

## 3. Fraud Investigation - Money Laundering Detection

### Scenario
Financial investigators track suspicious money flows between accounts to identify money laundering schemes.

### Graph Schema

**Account Types:**
- Personal: Account_A, Account_B, Account_C, Account_D
- Business: Company_X, Company_Y, Company_Z
- Shell: ShellCorp_1, ShellCorp_2

**Transaction Relationships:**
```
Account_A --TRANSFERRED_TO--> Account_B (amount: $10k, time_delay: 0)
Account_B --TRANSFERRED_TO--> Company_X (amount: $10k, time_delay: 1 hour)
Company_X --TRANSFERRED_TO--> ShellCorp_1 (amount: $9.8k, time_delay: 2 hours)
ShellCorp_1 --TRANSFERRED_TO--> Account_C (amount: $9.5k, time_delay: 3 hours)
Account_C --TRANSFERRED_TO--> Company_Y (amount: $9.2k, time_delay: 1 day)
Company_Y --TRANSFERRED_TO--> ShellCorp_2 (amount: $8.9k, time_delay: 1 day)
ShellCorp_2 --TRANSFERRED_TO--> Account_D (amount: $8.5k, time_delay: 2 days)
```

### Analysis Query

**Question:** "Trace the money flow from Account_A to Account_D"

**Analysis:**
```
find_all_paths(source="Account_A", target="Account_D", max_length=10)

Detected path: Account_A → Account_B → Company_X → ShellCorp_1 → Account_C → Company_Y → ShellCorp_2 → Account_D

Suspicious patterns:
- Multiple intermediary transfers (7 hops)
- Progressive amount reduction ($10k → $8.5k = 15% loss)
- Passes through shell corporations (ShellCorp_1, ShellCorp_2)
- Total time span: 3+ days (concealment indicator)
```

**Result:**
```json
{
  "source": "Account_A",
  "target": "Account_D",
  "path": ["Account_A", "Account_B", "Company_X", "ShellCorp_1", "Account_C", "Company_Y", "ShellCorp_2", "Account_D"],
  "path_length": 8,
  "initial_amount": 10000,
  "final_amount": 8500,
  "loss_percentage": 15,
  "total_time_span_hours": 72,
  "risk_score": 0.92,
  "suspicious_indicators": [
    "Multiple shell corporation intermediaries",
    "Sequential transfers suggest deliberate obfuscation",
    "Significant amount reduction",
    "Extended time span for simple transfer"
  ],
  "recommendation": "Flag for investigation - pattern consistent with money laundering"
}
```

---

## 4. Recommendation System - Product Discovery

### Scenario
E-commerce platform uses path reasoning to recommend products based on user-product-category connections.

### Graph Schema

**Entities:**
- Users: User1, User2, User3
- Products: Laptop, Monitor, Mouse, Keyboard
- Categories: Electronics, Computer_Accessories
- Brands: TechBrand, AccessoryBrand

**Relationships:**
```
User1 --VIEWED--> Laptop (confidence: 1.0)
User1 --PURCHASED--> Monitor (confidence: 0.95)
Laptop --BELONGS_TO--> Electronics (confidence: 0.99)
Monitor --BELONGS_TO--> Electronics (confidence: 0.99)
Mouse --BELONGS_TO--> Computer_Accessories (confidence: 0.98)
Electronics --RELATED_TO--> Computer_Accessories (confidence: 0.8)
Keyboard --BELONGS_TO--> Computer_Accessories (confidence: 0.98)
User2 --PURCHASED--> Keyboard (confidence: 0.92)
User2 --SIMILAR_TO--> User1 (confidence: 0.75)
```

### Analysis Query

**Question:** "What products should we recommend to User1?"

**Analysis:**
```
find_all_paths(source="User1", target="Product", max_length=3)

Existing interests:
- User1 → Viewed → Laptop
- User1 → Purchased → Monitor

Recommendation paths:
1. User1 → (via Electronics category) → Mouse
   Path: User1 → Purchased → Monitor → Belongs_To → Electronics → Related_To → Computer_Accessories → Contains → Mouse
   Distance: 6 hops
   Confidence: 0.95 * 0.99 * 0.8 * 0.98 = 0.7465
   Reasoning: "Monitor you bought is in Electronics, which relates to Computer Accessories, where Mouse is categorized"

2. User1 → (via similar user) → Keyboard
   Path: User1 → Similar_To → User2 → Purchased → Keyboard
   Distance: 3 hops
   Confidence: 0.75 * 0.92 = 0.69
   Reasoning: "Similar users purchased Keyboard"
```

**Result:**
```json
{
  "user": "User1",
  "recommendations": [
    {
      "product": "Mouse",
      "recommendation_path": "Related products to your Monitor purchase",
      "confidence": 0.7465,
      "reasoning": "Complements your Monitor - both in Computer Accessories ecosystem"
    },
    {
      "product": "Keyboard",
      "recommendation_path": "Popular among similar users",
      "confidence": 0.69,
      "reasoning": "Users with similar preferences purchased Keyboard"
    }
  ],
  "total_recommendations": 2
}
```

---

## 5. Knowledge Base Navigation - Learning Paths

### Scenario
Educational platform helps students discover learning paths by understanding how topics are related.

### Graph Schema

**Topics:**
- Fundamentals: Programming_Basics, Data_Structures, Algorithms
- Intermediate: OOP, Databases, Web_Development
- Advanced: Machine_Learning, Distributed_Systems, Security

**Relationships:**
```
Student --COMPLETED--> Programming_Basics (confidence: 1.0)
Programming_Basics --PREREQUISITE_FOR--> OOP (confidence: 0.95)
Programming_Basics --PREREQUISITE_FOR--> Data_Structures (confidence: 0.98)
Data_Structures --PREREQUISITE_FOR--> Algorithms (confidence: 0.9)
Algorithms --PREREQUISITE_FOR--> Machine_Learning (confidence: 0.85)
OOP --PREREQUISITE_FOR--> Web_Development (confidence: 0.8)
Web_Development --PREREQUISITE_FOR--> Distributed_Systems (confidence: 0.75)
Algorithms --PREREQUISITE_FOR--> Distributed_Systems (confidence: 0.7)
```

### Analysis Query

**Question:** "What learning path leads to Machine Learning from what I've completed?"

**Analysis:**
```
find_shortest_path(source="Programming_Basics", target="Machine_Learning")

Path: Programming_Basics → Data_Structures → Algorithms → Machine_Learning
  Distance: 3 hops
  Cumulative confidence: 0.98 * 0.9 * 0.85 = 0.7497
  Recommended order: Strict sequence required

Alternative paths:
- Programming_Basics → (many hops via OOP/Web Dev) → (cannot reach ML)
```

**Result:**
```json
{
  "current_knowledge": "Programming_Basics",
  "target_skill": "Machine_Learning",
  "recommended_path": [
    {
      "step": 1,
      "topic": "Data_Structures",
      "prerequisite_strength": 0.98,
      "estimated_duration_hours": 20
    },
    {
      "step": 2,
      "topic": "Algorithms",
      "prerequisite_strength": 0.9,
      "estimated_duration_hours": 25
    },
    {
      "step": 3,
      "topic": "Machine_Learning",
      "prerequisite_strength": 0.85,
      "estimated_duration_hours": 40
    }
  ],
  "total_path_strength": 0.7497,
  "total_estimated_duration_hours": 85,
  "completion_probability": 0.7497
}
```

---

## 6. Organizational Hierarchy - Authority Paths

### Scenario
A company wants to understand reporting relationships and authorization paths for decision-making.

### Graph Schema

**Organizational Structure:**
- CEO: John
- VPs: Alice (Engineering), Bob (Sales)
- Managers: Charlie (Frontend), Diana (Backend), Eve (Enterprise), Frank (SMB)
- Employees: George, Helen, Ian, Julia

**Relationships:**
```
Alice --REPORTS_TO--> John (authority: 1.0)
Bob --REPORTS_TO--> John (authority: 1.0)
Charlie --REPORTS_TO--> Alice (authority: 0.9)
Diana --REPORTS_TO--> Alice (authority: 0.9)
Eve --REPORTS_TO--> Bob (authority: 0.9)
Frank --REPORTS_TO--> Bob (authority: 0.9)
George --REPORTS_TO--> Charlie (authority: 0.8)
Helen --REPORTS_TO--> Diana (authority: 0.8)
Ian --REPORTS_TO--> Eve (authority: 0.8)
Julia --REPORTS_TO--> Frank (authority: 0.8)
George --PEER_TO--> Helen (authority: 0.5)
```

### Analysis Query

**Question:** "What is the authorization chain for George to approve a decision?"

**Analysis:**
```
find_shortest_path(source="George", target="John", relationship="REPORTS_TO")

Direct path: George → Charlie → Alice → John
  Distance: 3 hops
  Authority chain: 0.8 * 0.9 * 1.0 = 0.72

Alternative (cross-org): George → (via peer Helen?) → Diana → Alice → John
  Distance: 4 hops
  Authority: 0.5 * 0.8 * 0.9 * 1.0 = 0.36 (lower authority)
```

**Result:**
```json
{
  "employee": "George",
  "ceo": "John",
  "authority_path": ["George", "Charlie", "Alice", "John"],
  "path_strength": 0.72,
  "chain_of_command": [
    {
      "level": 1,
      "person": "Charlie",
      "role": "Manager - Frontend",
      "authority": 0.8
    },
    {
      "level": 2,
      "person": "Alice",
      "role": "VP - Engineering",
      "authority": 0.9
    },
    {
      "level": 3,
      "person": "John",
      "role": "CEO",
      "authority": 1.0
    }
  ],
  "approval_required_count": 3,
  "decision_authority": "VP Engineering (Alice) can approve up to $50k"
}
```

---

## Common Path Analysis Patterns

### Pattern 1: Distance-Based Ranking
```python
def rank_paths_by_distance(paths):
    """Prioritize shorter paths."""
    return sorted(paths, key=lambda p: len(p['path']))

# Result: Shortest paths ranked first
```

### Pattern 2: Confidence-Weighted Paths
```python
def rank_paths_by_confidence(paths):
    """Score by cumulative confidence."""
    for path in paths:
        confidence = 1.0
        for edge in path['edges']:
            confidence *= edge.get('confidence', 0.5)
        path['confidence'] = confidence
    return sorted(paths, key=lambda p: p['confidence'], reverse=True)

# Result: Most confident paths first
```

### Pattern 3: Path Diversity
```python
def find_diverse_paths(paths, num_paths=3):
    """Select paths using different edges."""
    selected = []
    used_edges = set()
    
    for path in sorted_paths:
        path_edges = set(path['edge_ids'])
        if not path_edges & used_edges:  # No overlap
            selected.append(path)
            used_edges.update(path_edges)
            if len(selected) == num_paths:
                break
    
    return selected

# Result: Diverse paths with minimal overlap
```

---

**Path reasoning is essential for:**
- Understanding indirect connections
- Recommendation systems
- Fraud detection
- Knowledge base navigation
- Organizational hierarchies
- Supply chain optimization


