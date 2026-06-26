# Ontology-Based Inference - Real-World Examples

Comprehensive examples of ontology-based reasoning applied to knowledge graphs across different domains.

## 1. Product Taxonomy - E-Commerce Ontology

### Scenario
An e-commerce system maintains a product taxonomy with class hierarchies for categorization and inference.

### Ontology Schema

**Classes:**
```
Product (root)
  ├── PhysicalProduct
  │   ├── Electronics
  │   │   ├── Computer
  │   │   │   ├── Desktop
  │   │   │   ├── Laptop
  │   │   │   │   └── Gaming Laptop
  │   │   │   └── Tablet
  │   │   └── Mobile Phone
  │   │       └── Smartphone
  │   └── Clothing
  │       ├── Apparel
  │       └── Footwear
  └── DigitalProduct
      ├── Software
      └── EBook
```

**Properties:**
```
hasPrice: domain=Product, range=Currency
hasManufacturer: domain=PhysicalProduct, range=Company
hasCompatibility: domain=Electronics, range=OperatingSystem
hasSize: domain=Clothing, range=Size
```

### Ontology Inference Examples

#### Example 1: Class Membership Inference

**Explicit Facts:**
```
iPhone14 rdf:type Smartphone
```

**Applied Rules:**
```
Rule 1 (Subclass): Smartphone ⊆ MobilePhone → iPhone14 rdf:type MobilePhone
Rule 2 (Subclass): MobilePhone ⊆ Electronics → iPhone14 rdf:type Electronics
Rule 3 (Subclass): Electronics ⊆ PhysicalProduct → iPhone14 rdf:type PhysicalProduct
Rule 4 (Subclass): PhysicalProduct ⊆ Product → iPhone14 rdf:type Product
```

**Inferred Facts:**
```
iPhone14 rdf:type [Smartphone, MobilePhone, Electronics, PhysicalProduct, Product]
```

#### Example 2: Property Inheritance

**Explicit Facts:**
```
iPhone14 rdf:type Smartphone
```

**Properties defined in hierarchy:**
```
Product.hasPrice (defined at root)
Electronics.hasCompatibility (defined at Electronics)
```

**Inferred Properties:**
```
iPhone14 can have hasPrice (inherited from Product)
iPhone14 can have hasCompatibility (inherited from Electronics)
```

### Inference Results

```json
{
  "individual": "iPhone14",
  "explicit_class": "Smartphone",
  "inferred_classes": [
    {"class": "MobilePhone", "distance": 1},
    {"class": "Electronics", "distance": 2},
    {"class": "PhysicalProduct", "distance": 3},
    {"class": "Product", "distance": 4}
  ],
  "inherited_properties": [
    {"property": "hasPrice", "source": "Product"},
    {"property": "hasManufacturer", "source": "PhysicalProduct"},
    {"property": "hasCompatibility", "source": "Electronics"}
  ],
  "total_inferences": 7
}
```

---

## 2. Biomedical Ontology - Disease Classification

### Scenario
A biomedical knowledge graph uses disease ontologies (SNOMED CT, ICD-10) for clinical reasoning.

### Ontology Schema

**Classes:**
```
Disease (root)
  ├── InfectiousDisease
  │   ├── ViralDisease
  │   │   ├── Influenza
  │   │   ├── COVID19
  │   │   └── Measles
  │   └── BacterialDisease
  │       ├── Pneumonia
  │       └── Tuberculosis
  └── ChronicDisease
      ├── Diabetes
      ├── HeartDisease
      └── Arthritis
```

**Properties:**
```
hasCause: domain=Disease, range=Pathogen
hasSymptom: domain=Disease, range=Symptom
treatmentWith: domain=Disease, range=Medication
requiredDiagnosis: domain=Disease, range=DiagnosticProcedure
```

### Ontology Inference Examples

#### Example 1: Disease Classification Inference

**Case: Patient diagnosed with COVID-19**

**Explicit:**
```
patient123 hasDisagnosis COVID19
```

**Inferred through hierarchy:**
```
COVID19 rdf:type ViralDisease  (explicit)
ViralDisease rdf:type InfectiousDisease  (subclass)
InfectiousDisease rdf:type Disease  (subclass)

⇒ patient123 hasDisease [COVID19, ViralDisease, InfectiousDisease, Disease]
```

**Property inferences:**
```
COVID19 hasCause Virus  (inherited from ViralDisease)
COVID19 treatmentWith Antivirals  (inherited property domain)
⇒ patient123 treatmentWith Antivirals
```

#### Example 2: Transitive Property Closure

**Relationships:**
```
Symptom COVID19: Fever
Symptom COVID19: Cough
Fever canLead PneumoniaComplication  (transitive causation)
Cough canLead PneumoniaComplication

⇒ COVID19 canLead PneumoniaComplication  (transitive closure)
```

### Inference Results

```json
{
  "patient": "patient123",
  "diagnosed_disease": "COVID19",
  "disease_hierarchy": [
    "COVID19",
    "ViralDisease",
    "InfectiousDisease",
    "Disease"
  ],
  "inferred_properties": {
    "hasCause": "Virus",
    "symptoms": ["Fever", "Cough", "Fatigue"],
    "treatment": "Antivirals",
    "possible_complications": ["PneumoniaComplication", "LungDamage"],
    "monitoring_required": true
  },
  "clinical_recommendations": [
    "Monitor vital signs",
    "Consider antiviral therapy",
    "Screen for complications"
  ]
}
```

---

## 3. Organization Ontology - Corporate Hierarchy

### Scenario
An organizational ontology manages employee roles, departments, and relationships with inference.

### Ontology Schema

**Classes:**
```
Employee (root)
  ├── Manager
  │   ├── DepartmentHead
  │   │   ├── VP
  │   │   └── C-Level
  │   └── TeamLead
  └── Contributor
      ├── SeniorEngineer
      ├── Engineer
      └── Junior Engineer
```

**Properties:**
```
worksIn: domain=Employee, range=Department
manages: domain=Manager, range=Employee
reportsTo: domain=Employee, range=Manager
hasPermission: domain=Employee, range=Permission
```

### Inference Rules

**Rule 1: Management Hierarchy**
```
IF (A manages B) AND (B manages C)
THEN (A manages C)  [transitive management]
```

**Rule 2: Permission Inheritance**
```
IF (role A subclass_of role B) AND (B hasPermission P)
THEN (A hasPermission P)  [permission inheritance]
```

**Rule 3: Reporting Chain**
```
IF (A reportsTo B) AND (B reportsTo C)
THEN (A reportsTo C)  [reporting chain]
```

### Inference Examples

**Scenario: John is a Senior Engineer**

```
Explicit:
  john rdf:type SeniorEngineer
  john worksIn EngineeringDept
  jane rdf:type DepartmentHead
  jane worksIn EngineeringDept
  jane reportsTo cto

Inferred:
  john rdf:type Engineer  (subclass inference)
  john rdf:type Contributor  (subclass inference)
  john rdf:type Employee  (subclass inference)
  
  john hasPermission CodeReview  (inherited from Engineer)
  john hasPermission MeetingAttendance  (inherited from Employee)
  
  john reportsTo jane  (organizational structure)
  john reportsTo cto  (transitive reporting chain)
```

---

## 4. Location Ontology - Geographic Reasoning

### Scenario
A location ontology with geographic hierarchy and spatial relationships.

### Ontology Schema

**Classes:**
```
Location (root)
  ├── Continent
  │   ├── Europe
  │   │   ├── Country
  │   │   │   ├── France
  │   │   │   │   ├── Region
  │   │   │   │   │   ├── IleDeFrance
  │   │   │   │   │   │   ├── City
  │   │   │   │   │   │   │   └── Paris
  │   │   │   │   │   │   └── Suburb
  │   │   │   ├── Germany
  │   │   │   └── UK
  │   └── Asia
  │       ├── China
  │       └── Japan
  └── Ocean
```

**Transitive Properties:**
```
locatedIn (transitive)
hasLocation (transitive)
partOf (transitive)
```

### Inference Examples

**Fact: Musée du Louvre is located in Paris**

```
Explicit:
  LouvreMuseum locatedIn Paris

Inferred by transitivity:
  Paris locatedIn IleDeFrance
  IleDeFrance locatedIn France
  ⇒ LouvreMuseum locatedIn IleDeFrance  (transitive)
  ⇒ LouvreMuseum locatedIn France  (transitive)
  
  France locatedIn Europe
  ⇒ LouvreMuseum locatedIn Europe  (transitive closure)
```

### Inference Results

```json
{
  "entity": "LouvreMuseum",
  "explicit_location": "Paris",
  "inferred_locations": [
    {"location": "IleDeFrance", "distance": 1},
    {"location": "France", "distance": 2},
    {"location": "Europe", "distance": 3},
    {"location": "Earth", "distance": 4}
  ],
  "hierarchical_path": [
    "LouvreMuseum",
    "Paris",
    "IleDeFrance",
    "France",
    "Europe",
    "Earth"
  ],
  "distance_from_root": 5
}
```

---

## 5. Person Ontology - Kinship Relations

### Scenario
A person ontology with kinship relationships and inverse/symmetric properties.

### Ontology Schema

**Properties:**
```
parent: domain=Person, range=Person
  inverse: hasChild
  
sibling: domain=Person, range=Person
  symmetric: true
  
spouse: domain=Person, range=Person
  symmetric: true
  inverse: spouse
  
ancestor: domain=Person, range=Person
  transitive: true
```

### Inference Rules

**Rule 1: Inverse Properties**
```
IF (A parent B)
THEN (B hasChild A)  [inverse]
```

**Rule 2: Sibling Derivation**
```
IF (A parent B) AND (A parent C) AND (B != C)
THEN (B sibling C)  [co-parent relationship]
```

**Rule 3: Transitive Closure**
```
IF (A ancestor B) AND (B ancestor C)
THEN (A ancestor C)  [transitive]
```

### Inference Examples

**Family: Alice (parent of Bob) and Carol**

```
Explicit:
  Alice parent Bob
  Alice parent Carol

Inferred:
  Bob hasChild Alice  (inverse property)
  Carol hasChild Alice  (inverse property)
  
  Bob sibling Carol  (from shared parent)
  Carol sibling Bob  (symmetric property)
```

---

## 6. Software Ontology - Library Dependencies

### Scenario
A software ontology managing library versions, dependencies, and compatibility.

### Ontology Schema

**Classes:**
```
Library (root)
  ├── UILibrary
  │   ├── React
  │   ├── Vue
  │   └── Angular
  └── UtilityLibrary
      ├── DateLibrary
      ├── MathLibrary
      └── ValidationLibrary
```

**Properties:**
```
dependsOn: domain=Library, range=Library (transitive)
compatibleWith: domain=Library, range=Library (symmetric)
requiresVersion: domain=Library, range=Version
```

### Inference Rules

**Rule: Transitive Dependencies**
```
IF (A dependsOn B) AND (B dependsOn C)
THEN (A dependsOn C)  [transitive dependency]
```

### Inference Results

```
Explicit:
  ReactApp dependsOn React
  React dependsOn ReactDOM
  ReactDOM dependsOn CoreJS

Inferred:
  ReactApp dependsOn ReactDOM  (transitive)
  ReactApp dependsOn CoreJS  (transitive)
  (full dependency tree materialized)
```

---

## Common Inference Patterns

### Pattern 1: Hierarchical Closure

```python
# Apply rule iteratively until fixpoint
def hierarchical_closure(individual, start_class, subclass_rules):
    """
    Compute full class hierarchy for individual.
    """
    classes = {start_class}
    queue = {start_class}
    
    while queue:
        current_class = queue.pop()
        for parent_class in subclass_rules.get(current_class, []):
            if parent_class not in classes:
                classes.add(parent_class)
                queue.add(parent_class)
    
    return classes
```

### Pattern 2: Property Inheritance

```python
def inherit_properties(individual, class_hierarchy, property_definitions):
    """
    Collect all properties applicable to individual through hierarchy.
    """
    properties = {}
    
    for cls in class_hierarchy:
        if cls in property_definitions:
            properties.update(property_definitions[cls])
    
    return properties
```

### Pattern 3: Inverse Property Application

```python
def apply_inverse_properties(triple, inverse_rules):
    """
    Generate inverse triples for symmetric/inverse properties.
    """
    (subject, predicate, obj) = triple
    
    if predicate in inverse_rules:
        inverse_pred = inverse_rules[predicate]
        return (obj, inverse_pred, subject)
    
    return None
```

### Pattern 4: Transitive Closure

```python
def transitive_closure(start, relationships, transitive_predicates):
    """
    Compute transitive closure for transitive properties.
    """
    closure = set()
    queue = [(start, neighbor) for neighbor in relationships.get(start, [])]
    
    while queue:
        source, target = queue.pop(0)
        closure.add((source, target))
        
        for next_target in relationships.get(target, []):
            if (source, next_target) not in closure:
                queue.append((source, next_target))
    
    return closure
```

---

**Ontology-based inference is essential for:**
- Semantic web applications
- Biomedical knowledge bases
- Enterprise data governance
- E-commerce taxonomies
- Geographic reasoning
- Organizational hierarchies
- Library management systems


