# Ontology-Based Inference - Design Patterns & Strategies

Comprehensive collection of ontology inference patterns, algorithms, and optimization techniques.

## Inference Patterns

### Pattern 1: Subclass Hierarchy Closure

Compute transitive closure of subclass relationships for class membership inference.

**Use Case:** Determining all classes an individual belongs to

**Implementation:**
```python
def compute_class_hierarchy(individual, explicit_type, subclass_relationships):
    """
    Compute all classes individual belongs to through subclass inheritance.
    
    Algorithm:
    1. Start with explicit type
    2. Add all parent classes via subclass relationships
    3. Repeat until no new classes found
    """
    inferred_classes = {explicit_type}
    queue = [explicit_type]
    
    while queue:
        current_class = queue.pop(0)
        
        # Find all parents of current class
        if current_class in subclass_relationships:
            for parent_class in subclass_relationships[current_class]:
                if parent_class not in inferred_classes:
                    inferred_classes.add(parent_class)
                    queue.append(parent_class)
    
    return inferred_classes


# Example:
subclass_hierarchy = {
    'Smartphone': ['MobilePhone'],
    'MobilePhone': ['Electronics'],
    'Electronics': ['PhysicalProduct'],
    'PhysicalProduct': ['Product']
}

classes = compute_class_hierarchy('iPhone14', 'Smartphone', subclass_hierarchy)
# Returns: {'Smartphone', 'MobilePhone', 'Electronics', 'PhysicalProduct', 'Product'}
```

**Complexity:** O(C * P) where C = classes, P = parent relationships  
**Best For:** Materializing full class hierarchies

---

### Pattern 2: Property Domain & Range Inference

Infer types based on property usage constraints.

**Use Case:** Type discovery from domain/range constraints

**Implementation:**
```python
def apply_domain_range_inference(subject, predicate, obj, ontology):
    """
    Infer types of subject and object from property constraints.
    
    Domain: If property P has domain D, and S P O, then S:D
    Range: If property P has range R, and S P O, then O:R
    """
    inferred_types = {}
    
    if predicate in ontology['properties']:
        prop_def = ontology['properties'][predicate]
        
        # Domain inference
        if 'domain' in prop_def:
            inferred_types[subject] = prop_def['domain']
        
        # Range inference
        if 'range' in prop_def:
            inferred_types[obj] = prop_def['range']
    
    return inferred_types


# Example:
ontology = {
    'properties': {
        'hasOwner': {
            'domain': 'Vehicle',
            'range': 'Person'
        }
    }
}

# Fact: john_car hasOwner jane
inferred = apply_domain_range_inference('john_car', 'hasOwner', 'jane', ontology)
# Returns: {'john_car': 'Vehicle', 'jane': 'Person'}
```

**Complexity:** O(P) where P = properties  
**Best For:** Type discovery and validation

---

### Pattern 3: Property Inheritance Through Hierarchy

Propagate properties through class hierarchies.

**Use Case:** Property applicability based on class membership

**Implementation:**
```python
def inherit_properties_down_hierarchy(class_obj, class_properties, subclasses):
    """
    Inherit properties from parent to child classes.
    
    If class A has property P, and B is subclass of A,
    then B inherits property P.
    """
    all_properties = {}
    visited = set()
    
    def traverse(current_class):
        if current_class in visited:
            return
        visited.add(current_class)
        
        # Collect properties of current class
        if current_class in class_properties:
            all_properties.update(class_properties[current_class])
        
        # Traverse parent classes
        if current_class in subclasses:
            for parent in subclasses[current_class]:
                traverse(parent)
    
    traverse(class_obj)
    return all_properties


# Example:
class_properties = {
    'Vehicle': {'hasEngine': 'Engine', 'hasWheels': 'Wheel'},
    'Car': {'hasSeats': 'Seat'},
    'ElectricCar': {'hasBattery': 'Battery'}
}

subclasses = {
    'Car': ['Vehicle'],
    'ElectricCar': ['Car'],
    'Vehicle': []
}

props = inherit_properties_down_hierarchy('ElectricCar', class_properties, subclasses)
# Returns: {
#   'hasBattery': 'Battery',
#   'hasSeats': 'Seat',
#   'hasEngine': 'Engine',
#   'hasWheels': 'Wheel'
# }
```

**Complexity:** O(C * P) where C = classes, P = properties  
**Best For:** Property applicability determination

---

### Pattern 4: Inverse Property Application

Generate inverse triples for symmetric/inverse properties.

**Use Case:** Bidirectional relationship materialization

**Implementation:**
```python
def apply_inverse_property(subject, predicate, obj, inverse_property_map):
    """
    Apply inverse property rule.
    
    IF (S P O) and P inverse_of Q
    THEN (O Q S)
    """
    inverse_triples = []
    
    if predicate in inverse_property_map:
        inverse_pred = inverse_property_map[predicate]
        inverse_triples.append((obj, inverse_pred, subject))
    
    return inverse_triples


# Example:
inverse_map = {
    'parent': 'hasChild',
    'hasChild': 'parent',
    'spouse': 'spouse',  # symmetric
    'hasOwner': 'owns'
}

# Fact: Alice parent Bob
inverses = apply_inverse_property('Alice', 'parent', 'Bob', inverse_map)
# Returns: [('Bob', 'hasChild', 'Alice')]
```

**Complexity:** O(1) per triple  
**Best For:** Materializing bidirectional relationships

---

### Pattern 5: Transitive Property Closure

Compute transitive closure for transitive properties.

**Use Case:** Chain relationships (ancestor, partOf, reportsTo)

**Implementation:**
```python
def compute_transitive_closure(entity, predicate, relationships, transitive_predicates):
    """
    Compute transitive closure for transitive properties.
    
    IF P is transitive, and (S P M) and (M P O)
    THEN (S P O)
    """
    if predicate not in transitive_predicates:
        return []
    
    reachable = set()
    queue = [(entity, neighbor) for neighbor in relationships.get((entity, predicate), [])]
    
    while queue:
        source, target = queue.pop(0)
        
        if (source, target) not in reachable:
            reachable.add((source, target))
            
            # Continue chain
            for next_target in relationships.get((target, predicate), []):
                queue.append((source, next_target))
    
    return list(reachable)


# Example:
relationships = {
    ('Alice', 'ancestor'): ['Bob'],
    ('Bob', 'ancestor'): ['Charlie'],
    ('Charlie', 'ancestor'): ['David']
}

transitive_predicates = {'ancestor', 'partOf', 'reportsTo'}

closure = compute_transitive_closure('Alice', 'ancestor', relationships, transitive_predicates)
# Returns: [('Alice', 'Bob'), ('Alice', 'Charlie'), ('Alice', 'David')]
```

**Complexity:** O(V + E) using BFS  
**Best For:** Chain relationship materialization

---

### Pattern 6: Symmetric Property Inference

Handle symmetric properties (bidirectional).

**Use Case:** Symmetric relationships like "knows", "married_to"

**Implementation:**
```python
def apply_symmetric_property(subject, predicate, obj, symmetric_predicates):
    """
    Apply symmetric property rule.
    
    IF P is symmetric and (S P O)
    THEN (O P S)
    """
    symmetric_triples = []
    
    if predicate in symmetric_predicates:
        symmetric_triples.append((obj, predicate, subject))
    
    return symmetric_triples


# Example:
symmetric_predicates = {'knows', 'married_to', 'sibling', 'colleague'}

# Fact: Alice knows Bob
symmetric = apply_symmetric_property('Alice', 'knows', 'Bob', symmetric_predicates)
# Returns: [('Bob', 'knows', 'Alice')]
```

**Complexity:** O(1)  
**Best For:** Bidirectional relationship inference

---

### Pattern 7: Subproperty Inference

Apply subproperty relationships.

**Use Case:** Property specialization (son ⊆ child)

**Implementation:**
```python
def apply_subproperty_rule(subject, predicate, obj, subproperty_hierarchy):
    """
    Apply subproperty inheritance.
    
    IF P subproperty_of Q and (S P O)
    THEN (S Q O)
    """
    inferred_triples = []
    
    # Find all parent properties
    queue = [predicate]
    processed = set()
    
    while queue:
        current_prop = queue.pop(0)
        
        if current_prop not in processed:
            processed.add(current_prop)
            
            if current_prop in subproperty_hierarchy:
                for parent_prop in subproperty_hierarchy[current_prop]:
                    inferred_triples.append((subject, parent_prop, obj))
                    queue.append(parent_prop)
    
    return inferred_triples


# Example:
subproperty_hierarchy = {
    'son': ['child'],
    'daughter': ['child'],
    'child': ['descendant'],
    'grandchild': ['descendant']
}

# Fact: Alice son Bob
inferred = apply_subproperty_rule('Alice', 'son', 'Bob', subproperty_hierarchy)
# Returns: [('Alice', 'child', 'Bob'), ('Alice', 'descendant', 'Bob')]
```

**Complexity:** O(P * D) where P = properties, D = depth  
**Best For:** Property hierarchy inference

---

### Pattern 8: Cardinality Constraints

Validate cardinality constraints during inference.

**Use Case:** Constraint checking and validation

**Implementation:**
```python
def check_cardinality_constraint(subject, predicate, cardinality_constraints):
    """
    Check if adding triple violates cardinality constraints.
    
    Cardinality: (1=1, 0..1=optional, 1..*=many)
    """
    if predicate not in cardinality_constraints:
        return True  # No constraint
    
    constraint = cardinality_constraints[predicate]
    current_count = get_value_count(subject, predicate)  # hypothetical
    max_allowed = constraint.get('max', float('inf'))
    
    return current_count < max_allowed


# Example:
cardinality_constraints = {
    'hasSpouse': {'min': 0, 'max': 1},  # At most 1 spouse
    'hasParent': {'min': 2, 'max': 2},  # Exactly 2 parents
    'hasChild': {'min': 0, 'max': float('inf')}  # Any number
}
```

**Complexity:** O(1) lookup  
**Best For:** Data quality and consistency validation

---

## Execution Strategies

### Strategy 1: Forward Chaining Materialization

Eagerly derive all inferences upfront.

```python
def forward_chaining_materialization(ontology, individuals, rules):
    """
    Apply all rules to completion (fixpoint).
    
    Algorithm:
    1. Load ontology and individuals
    2. Repeat until no new facts:
       a. For each rule:
          - Find matches
          - Generate inferences
          - Add new facts
    3. Return materialized facts
    """
    inferred = set()
    iteration = 0
    max_iterations = 1000
    
    while iteration < max_iterations:
        iteration += 1
        new_inferences = 0
        
        for rule in rules:
            matches = find_rule_matches(rule, ontology, individuals, inferred)
            
            for match in matches:
                new_fact = apply_rule_inference(rule, match)
                if new_fact not in inferred:
                    inferred.add(new_fact)
                    new_inferences += 1
        
        if new_inferences == 0:
            break  # Fixpoint reached
    
    return inferred
```

**Pros:** Complete, deterministic, fast queries  
**Cons:** High upfront cost, storage  
**Best For:** OLAP, offline reasoning, complete materialization

---

### Strategy 2: Backward Chaining Resolution

Query-driven inference.

```python
def backward_chaining(query, ontology, rules):
    """
    Prove query through backward chaining.
    
    Algorithm:
    1. Check if query fact exists
    2. If not, find rules that conclude query
    3. Recursively prove rule conditions
    4. Return proof or failure
    """
    def prove(goal, depth=0, visited=None):
        if visited is None:
            visited = set()
        
        if depth > MAX_DEPTH:
            return None
        
        # Check explicit facts
        if fact_exists(goal):
            return {'proven': True, 'source': 'explicit'}
        
        # Try rules
        for rule in rules:
            if rule_concludes(rule, goal):
                conditions = get_rule_conditions(rule)
                
                for condition in conditions:
                    proof = prove(condition, depth + 1, visited)
                    if proof:
                        return {
                            'proven': True,
                            'source': 'rule',
                            'conditions': conditions
                        }
        
        return None
    
    return prove(query)
```

**Pros:** Memory efficient, on-demand  
**Cons:** Query latency, repeated computation  
**Best For:** OLTP, large graphs

---

### Strategy 3: Hybrid Approach

Combine materialization with backward chaining.

```python
def hybrid_inference(ontology, individuals, rules):
    """
    Hybrid: Forward chain core rules, backward chain derived rules.
    """
    # Forward chain high-impact rules
    core_rules = [r for r in rules if r['priority'] > 80]
    materialized = forward_chaining_materialization(ontology, individuals, core_rules)
    
    # Backward chain remaining rules
    derived_rules = [r for r in rules if r['priority'] <= 80]
    
    return {
        'materialized': materialized,
        'rules_for_backward': derived_rules
    }
```

**Pros:** Balanced cost/benefit  
**Cons:** Complexity  
**Best For:** Mixed workloads

---

## Optimization Techniques

### Technique 1: Rule Indexing

Index rules for efficient pattern matching.

```python
def index_rules_by_predicate(rules):
    """
    Index rules by predicates they match.
    """
    index = {}
    
    for rule in rules:
        predicates = extract_predicates(rule['condition'])
        
        for pred in predicates:
            if pred not in index:
                index[pred] = []
            index[pred].append(rule)
    
    return index
```

---

### Technique 2: Incremental Inference

Update inferences only on data changes.

```python
def incremental_inference_on_insert(new_fact, ontology, rules):
    """
    Update inferences incrementally when new fact added.
    """
    affected_inferences = []
    
    # Find rules affected by new fact
    affected_rules = find_affected_rules(new_fact, rules)
    
    for rule in affected_rules:
        new_inferences = apply_rule(rule, ontology)
        affected_inferences.extend(new_inferences)
    
    return affected_inferences
```

---

### Technique 3: Fixpoint Detection

Stop iteration when no new inferences.

```python
def detect_fixpoint(previous_facts, current_facts):
    """
    Check if fixpoint reached (no new facts).
    """
    return len(current_facts - previous_facts) == 0
```

---

## Performance Optimization

### Caching Strategies
```python
class OntologyInferenceCache:
    def __init__(self):
        self.class_hierarchy_cache = {}
        self.property_cache = {}
    
    def get_class_hierarchy(self, class_id):
        if class_id not in self.class_hierarchy_cache:
            self.class_hierarchy_cache[class_id] = compute_hierarchy(class_id)
        return self.class_hierarchy_cache[class_id]
    
    def invalidate(self):
        self.class_hierarchy_cache.clear()
        self.property_cache.clear()
```

---

## Summary

| Pattern | Use Case | Complexity |
|---------|----------|-----------|
| 1. Subclass Closure | Class hierarchy | O(C*P) |
| 2. Domain/Range | Type inference | O(P) |
| 3. Property Inherit. | Applicability | O(C*P) |
| 4. Inverse Property | Bidirectional | O(1) |
| 5. Transitive | Chain relations | O(V+E) |
| 6. Symmetric | Symmetric rels | O(1) |
| 7. Subproperty | Property spec | O(P*D) |
| 8. Cardinality | Validation | O(1) |

| Strategy | Cost | Speed | Best For |
|----------|------|-------|----------|
| Forward | High | Fast | OLAP |
| Backward | Low | Slow | OLTP |
| Hybrid | Medium | Medium | Mixed |


