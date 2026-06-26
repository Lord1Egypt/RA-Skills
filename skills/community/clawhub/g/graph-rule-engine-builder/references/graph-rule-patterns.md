# Graph Rule Engine - Design Patterns & Execution Strategies

Comprehensive collection of rule patterns, execution strategies, and optimization techniques for knowledge graph reasoning.

## Rule Pattern Catalog

### Pattern 1: Transitive Closure via Fixpoint Iteration

Iteratively apply rules until no new inferences are derived.

**Use Case:** Hierarchies, organizational chains, geographic nesting

**Implementation:**
```python
def execute_transitive_rule(graph, rule):
    """
    Execute rule to fixpoint (until no new inferences).
    
    Args:
        graph: Knowledge graph
        rule: Rule with condition and inference
    
    Returns:
        Set of inferred relationships
    """
    inferred = set()
    iteration = 0
    max_iterations = 1000
    
    while iteration < max_iterations:
        iteration += 1
        matches = find_pattern_matches(graph, rule['condition'])
        
        new_inferences = 0
        for match in matches:
            inference = apply_inference(match, rule['inference'])
            
            if inference not in inferred:
                inferred.add(inference)
                graph.add_edge(inference)
                new_inferences += 1
        
        if new_inferences == 0:
            break  # Fixpoint reached
    
    return {
        'inferred': inferred,
        'iterations': iteration,
        'fixpoint_reached': iteration < max_iterations
    }


# Example:
result = execute_transitive_rule(graph, {
    'condition': '(a)-[REPORTS_TO]->(b) AND (b)-[REPORTS_TO]->(c)',
    'inference': '(a)-[REPORTS_INDIRECTLY_TO]->(c)'
})
```

**Complexity:** O(N * E) where N = iterations to fixpoint  
**Best For:** Deriving all consequences, complete materialization

---

### Pattern 2: Co-occurrence Inference

Derive relationships between entities that share common connections.

**Use Case:** Recommendations, collaborative filtering, similarity

**Implementation:**
```python
def co_occurrence_rule(graph, relationship_type):
    """
    Infer that entities are related if they connect to same node.
    
    IF (a)-[rel]->(c)<-[rel]-(b)
    THEN (a)-[COOCCUR_WITH]->(b)
    """
    inferred = set()
    
    # Find all nodes with incoming relationships
    for node_c in graph.nodes():
        # Find all nodes connecting to node_c
        incoming = graph.get_incoming_edges(node_c, relationship_type)
        
        # Create pairwise relationships
        incoming_nodes = [edge['source'] for edge in incoming]
        
        for i in range(len(incoming_nodes)):
            for j in range(i + 1, len(incoming_nodes)):
                node_a = incoming_nodes[i]
                node_b = incoming_nodes[j]
                
                if node_a != node_b:
                    edge = {
                        'source': node_a,
                        'target': node_b,
                        'type': 'COOCCUR_WITH',
                        'shared_connection': node_c
                    }
                    inferred.add((node_a, node_b))
                    graph.add_edge(edge)
    
    return inferred


# Example: Product recommendations
# IF User1 --PURCHASED--> Product AND User2 --PURCHASED--> Product
# THEN User1 --RECOMMENDATION--> Product (via User2)
```

**Complexity:** O(V * E²)  
**Best For:** Collaborative systems, relationship discovery

---

### Pattern 3: Property-Based Conditional Rules

Apply rules based on entity properties and constraints.

**Use Case:** Classification, segmentation, compliance

**Implementation:**
```python
def property_conditional_rule(graph, rule):
    """
    Apply rules conditionally based on entity properties.
    
    Rule format:
    {
      'conditions': [
        {'property': 'age', 'operator': '>=', 'value': 65},
        {'property': 'status', 'operator': '==', 'value': 'Active'}
      ],
      'then': {
        'add_relationship': ('ELIGIBLE_FOR', 'SeniorBenefits'),
        'set_property': {'priority': 'high'}
      }
    }
    """
    inferred = []
    
    for node in graph.nodes():
        node_data = graph.get_node(node)
        
        # Check all conditions
        conditions_met = True
        for condition in rule['conditions']:
            prop = condition['property']
            operator = condition['operator']
            value = condition['value']
            
            node_value = node_data.get(prop)
            
            if operator == '>=':
                if not (node_value >= value):
                    conditions_met = False
            elif operator == '==':
                if not (node_value == value):
                    conditions_met = False
            elif operator == '<=':
                if not (node_value <= value):
                    conditions_met = False
            elif operator == 'NOT EXISTS':
                if prop in node_data:
                    conditions_met = False
        
        # Apply inference if conditions met
        if conditions_met:
            # Add relationships
            if 'add_relationship' in rule['then']:
                rel_type, target = rule['then']['add_relationship']
                graph.add_edge({
                    'source': node,
                    'target': target,
                    'type': rel_type
                })
                inferred.append((node, rel_type, target))
            
            # Set properties
            if 'set_property' in rule['then']:
                for prop, value in rule['then']['set_property'].items():
                    graph.set_node_property(node, prop, value)
    
    return inferred


# Example: Senior citizen classification
rule = {
    'conditions': [
        {'property': 'age', 'operator': '>=', 'value': 65}
    ],
    'then': {
        'add_relationship': ('ELIGIBLE_FOR', 'SeniorBenefits'),
        'set_property': {'age_group': 'senior', 'priority': 'high'}
    }
}
```

**Complexity:** O(V * C) where C = condition checks  
**Best For:** Segmentation, classification, compliance rules

---

### Pattern 4: Anomaly/Fraud Detection

Detect suspicious patterns and flag them.

**Use Case:** Fraud detection, compliance monitoring, quality control

**Implementation:**
```python
def anomaly_detection_rule(graph, pattern, severity_level='HIGH'):
    """
    Detect and flag anomalous patterns in graph.
    
    Patterns:
    - Circular transfers
    - Unusual access patterns
    - Duplicate edges
    - Constraint violations
    """
    anomalies = []
    
    if pattern == 'circular_transfer':
        # Find cycles in transfers
        for node in graph.nodes():
            cycles = find_cycles_from_node(graph, node)
            for cycle in cycles:
                if len(cycle) >= 3:  # At least 3-node cycle
                    anomalies.append({
                        'type': 'CircularTransfer',
                        'cycle': cycle,
                        'severity': severity_level,
                        'confidence': 0.95,
                        'action': 'Flag for investigation'
                    })
    
    elif pattern == 'constraint_violation':
        # Check for constraint violations
        for edge in graph.edges():
            if violates_constraints(edge, graph):
                anomalies.append({
                    'type': 'ConstraintViolation',
                    'edge': edge,
                    'severity': severity_level,
                    'violation': get_violation_details(edge)
                })
    
    elif pattern == 'unusual_activity':
        # Detect unusual activity patterns
        for node in graph.nodes():
            activity_score = compute_activity_score(node, graph)
            if activity_score > threshold:
                anomalies.append({
                    'type': 'UnusualActivity',
                    'node': node,
                    'score': activity_score,
                    'severity': severity_level
                })
    
    return anomalies


def find_cycles_from_node(graph, start_node, max_length=10):
    """Find all cycles starting and ending at start_node."""
    cycles = []
    
    def dfs(current, path, visited):
        if len(path) > max_length:
            return
        
        for neighbor in graph.get_neighbors(current):
            if neighbor == start_node and len(path) >= 3:
                cycles.append(path[:])
            elif neighbor not in visited and neighbor != start_node:
                visited.add(neighbor)
                path.append(neighbor)
                dfs(neighbor, path, visited)
                path.pop()
                visited.remove(neighbor)
    
    dfs(start_node, [start_node], {start_node})
    return cycles


# Example: Fraud detection
anomalies = anomaly_detection_rule(graph, 'circular_transfer', severity_level='HIGH')
for anomaly in anomalies:
    print(f"Alert: {anomaly['type']} detected in cycle {anomaly['cycle']}")
```

**Complexity:** O(V * (V + E))  
**Best For:** Real-time monitoring, compliance

---

### Pattern 5: Aggregation & Metrics Computation

Compute aggregate metrics from graph patterns.

**Use Case:** Analytics, KPIs, summarization

**Implementation:**
```python
def aggregation_rule(graph, aggregation_spec):
    """
    Compute and store aggregate metrics.
    
    Spec format:
    {
      'source_pattern': '(emp:Employee)-[:WORKS_AT]->(company:Company)',
      'aggregation': 'count',
      'group_by': 'company',
      'target_property': 'employee_count'
    }
    """
    results = {}
    
    # Find all matches of pattern
    matches = find_pattern_matches(graph, aggregation_spec['source_pattern'])
    
    # Group matches
    groups = {}
    for match in matches:
        group_key = match[aggregation_spec['group_by']]
        if group_key not in groups:
            groups[group_key] = []
        groups[group_key].append(match)
    
    # Apply aggregation
    for group_key, group_matches in groups.items():
        if aggregation_spec['aggregation'] == 'count':
            result = len(group_matches)
        elif aggregation_spec['aggregation'] == 'sum':
            result = sum(m.get('value', 0) for m in group_matches)
        elif aggregation_spec['aggregation'] == 'avg':
            values = [m.get('value', 0) for m in group_matches]
            result = sum(values) / len(values) if values else 0
        elif aggregation_spec['aggregation'] == 'min':
            result = min(m.get('value', 0) for m in group_matches)
        elif aggregation_spec['aggregation'] == 'max':
            result = max(m.get('value', 0) for m in group_matches)
        
        # Store result
        graph.set_node_property(
            group_key,
            aggregation_spec['target_property'],
            result
        )
        
        results[group_key] = result
    
    return results


# Example: Count employees per company
spec = {
    'source_pattern': '(emp:Employee)-[:WORKS_AT]->(company:Company)',
    'aggregation': 'count',
    'group_by': 'company',
    'target_property': 'employee_count'
}

employee_counts = aggregation_rule(graph, spec)
# Returns: {'TechCorp': 45, 'FinanceInc': 32, 'RetailCo': 120}
```

**Complexity:** O(matches * log(groups))  
**Best For:** KPI computation, analytics

---

## Rule Execution Strategies

### Strategy 1: Forward Chaining (Eager Inference)

Apply all rules to derive all possible inferences.

```python
def forward_chaining_engine(graph, rules):
    """
    Execute forward chaining: derive all possible inferences.
    
    Algorithm:
    1. Working Memory = initial facts from graph
    2. While new facts can be derived:
       a. For each rule:
          - Find pattern matches in working memory
          - Apply inference to add new facts
       b. Add new facts to working memory
    3. Return materialized facts
    """
    materialized = set()
    changed = True
    iteration = 0
    
    while changed and iteration < MAX_ITERATIONS:
        iteration += 1
        changed = False
        
        for rule in rules:
            # Find matches
            matches = find_pattern_matches(graph, rule['condition'])
            
            for match in matches:
                # Apply inference
                new_fact = apply_inference(match, rule['inference'])
                
                if new_fact not in materialized:
                    materialized.add(new_fact)
                    graph.add_edge(new_fact)
                    changed = True
    
    return {
        'materialized_facts': materialized,
        'iterations': iteration,
        'complete': iteration < MAX_ITERATIONS
    }
```

**Pros:** Complete, explicit inferences, fast queries  
**Cons:** Storage cost, update latency, preprocessing time  
**Best For:** OLAP, data warehouses, complete materialization

---

### Strategy 2: Backward Chaining (Lazy Inference)

Derive inferences only when queried.

```python
def backward_chaining_engine(graph, rules, query):
    """
    Execute backward chaining: derive on-demand.
    
    Algorithm:
    1. Goal = query
    2. If goal exists in graph, return it
    3. If not, find rules that could derive goal
    4. Recursively prove rule conditions (subgoals)
    5. Return proof chain
    """
    def prove(goal, depth=0, visited=None):
        if visited is None:
            visited = set()
        
        if depth > MAX_DEPTH:
            return None
        
        goal_tuple = tuple(sorted(goal.items()))
        if goal_tuple in visited:
            return None  # Avoid infinite recursion
        
        visited.add(goal_tuple)
        
        # Check if goal exists in graph
        if graph.has_edge(goal):
            return {'proven': True, 'source': 'graph', 'path': [goal]}
        
        # Try to derive goal from rules
        for rule in rules:
            if rule['inference'] matches goal:
                # Try to prove rule conditions
                conditions = parse_conditions(rule['condition'])
                
                for condition in conditions:
                    proof = prove(condition, depth + 1, visited)
                    if proof:
                        return {
                            'proven': True,
                            'source': 'rule',
                            'rule_name': rule['name'],
                            'conditions': conditions,
                            'proof_path': [goal] + proof.get('path', [])
                        }
        
        return None
    
    return prove(query)
```

**Pros:** Memory efficient, always current, lazy evaluation  
**Cons:** Query latency, repeated computation, complex proofs  
**Best For:** OLTP, query-driven systems, on-demand inference

---

### Strategy 3: Incremental Inference

Update inferences incrementally on data changes.

```python
def incremental_inference_engine(graph, rules):
    """
    Update inferences incrementally on data modification.
    
    On INSERT edge:
      - Find rules affected by new edge
      - Re-execute only affected rules
      - Derive only new consequences
    
    On DELETE edge:
      - Remove derived facts dependent on edge
      - Update materialized views
    """
    def on_insert_edge(edge):
        affected_rules = find_affected_rules(rules, edge)
        
        new_inferences = []
        for rule in affected_rules:
            # Check if rule condition matches with new edge
            if matches_rule_condition(edge, rule):
                # Derive consequence
                inference = apply_inference(edge, rule['inference'])
                new_inferences.append(inference)
                graph.add_edge(inference)
        
        return new_inferences
    
    def on_delete_edge(edge):
        # Find inferences that depend on this edge
        dependent = find_dependent_inferences(edge, graph)
        
        for dep_inference in dependent:
            # Remove derived fact
            graph.delete_edge(dep_inference)
            
            # Recursively remove cascading inferences
            on_delete_edge(dep_inference)
    
    return {
        'on_insert': on_insert_edge,
        'on_delete': on_delete_edge
    }
```

**Pros:** Minimal computation, near real-time, efficient updates  
**Cons:** Complex dependency tracking, cascading updates  
**Best For:** Real-time systems, continuous inference

---

## Rule Optimization Techniques

### Technique 1: Indexing for Pattern Matching

```python
def create_rule_indexes(graph, rules):
    """
    Create indexes to accelerate pattern matching.
    
    Strategies:
    - Index by relationship type
    - Index by source node
    - Index by properties
    """
    indexes = {}
    
    for rule in rules:
        # Extract pattern elements
        pattern = rule['condition']
        
        # Create index keys
        if 'WORKS_AT' in pattern:
            if 'works_at_index' not in indexes:
                indexes['works_at_index'] = defaultdict(list)
            
            # Build index
            for edge in graph.edges():
                if edge['type'] == 'WORKS_AT':
                    source = edge['source']
                    indexes['works_at_index'][source].append(edge)
    
    return indexes
```

---

### Technique 2: Rule Prioritization

```python
def prioritize_rules(rules):
    """
    Order rules by cost and impact for efficient execution.
    
    Cost factors:
    - Pattern complexity (simpler = lower cost)
    - Number of conditions (fewer = lower cost)
    - Selectivity (high selectivity = lower cost)
    
    Impact factors:
    - Number of inferences
    - Downstream consequences
    """
    def compute_priority(rule):
        cost = 1.0
        
        # Increase cost for complex patterns
        if '*' in rule['condition']:  # Variable-length paths
            cost *= 10
        
        # Increase cost for multiple conditions
        condition_count = rule['condition'].count('AND')
        cost *= (condition_count + 1)
        
        # Reduce cost for high-selectivity conditions
        if 'WHERE' in rule['condition']:
            cost *= 0.5
        
        # Impact priority (higher = more important)
        impact = 100 if rule['type'] == 'derivation' else 50
        
        # Final priority
        priority = impact / cost
        
        return priority
    
    # Sort by priority descending
    return sorted(rules, key=compute_priority, reverse=True)
```

---

## Rule Validation & Testing

### Pattern 1: Rule Consistency Checking

```python
def check_rule_consistency(rules):
    """Validate rules for logical consistency."""
    issues = []
    
    # Check for circular dependencies
    rule_deps = build_rule_dependency_graph(rules)
    cycles = find_cycles(rule_deps)
    if cycles:
        issues.append(f"Circular rule dependencies: {cycles}")
    
    # Check for conflicting inferences
    for i, rule1 in enumerate(rules):
        for rule2 in rules[i+1:]:
            if infers_conflicting(rule1, rule2):
                issues.append(f"Rules {rule1['name']} and {rule2['name']} may conflict")
    
    return issues


def test_rule(graph, rule, test_cases):
    """Test rule on sample data."""
    results = []
    
    for test_case in test_cases:
        # Apply rule
        inferences = execute_rule(graph, rule)
        
        # Check expected results
        expected = test_case['expected']
        actual = inferences
        
        passed = expected == actual
        results.append({
            'test': test_case['name'],
            'passed': passed,
            'expected': expected,
            'actual': actual
        })
    
    return results
```

---

## Summary

| Pattern | Use Case | Complexity | Best For |
|---------|----------|-----------|----------|
| 1. Transitive | Hierarchies | O(N*E) | Chains, closure |
| 2. Co-occurrence | Recommendations | O(V*E²) | Collaboration |
| 3. Conditional | Classification | O(V*C) | Segmentation |
| 4. Anomaly | Fraud detection | O(V*(V+E)) | Monitoring |
| 5. Aggregation | Analytics | O(matches) | Metrics |

| Strategy | Execution | Memory | Query Latency | Best For |
|----------|-----------|--------|---------------|----------|
| Forward Chaining | Eager | High | Low | OLAP |
| Backward Chaining | Lazy | Low | High | OLTP |
| Incremental | On-demand | Medium | Medium | Real-time |


