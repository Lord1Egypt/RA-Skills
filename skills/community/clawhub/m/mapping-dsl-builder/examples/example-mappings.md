# Mapping DSL Examples

Complete examples of mapping DSL generation for different domains and data sources.

## Example 1: Relational Database to RDF Mapping

### Source Database Schema

```sql
CREATE TABLE person (
  person_id INT PRIMARY KEY,
  first_name VARCHAR(100),
  last_name VARCHAR(100),
  email VARCHAR(100),
  birth_date DATE,
  company_id INT,
  FOREIGN KEY (company_id) REFERENCES company(company_id)
);

CREATE TABLE company (
  company_id INT PRIMARY KEY,
  company_name VARCHAR(255),
  industry VARCHAR(100),
  founded_year INT
);

CREATE TABLE employment (
  employment_id INT PRIMARY KEY,
  person_id INT,
  company_id INT,
  job_title VARCHAR(100),
  start_date DATE,
  salary DECIMAL(10, 2),
  FOREIGN KEY (person_id) REFERENCES person(person_id),
  FOREIGN KEY (company_id) REFERENCES company(company_id)
);
```

### Generated Mapping DSL

```yaml
mapping: PersonCompanyMapping
version: 1.0
description: Map person and company tables to RDF triples

source:
  type: database
  connection: postgresql://localhost:5432/company_db
  dialect: postgresql

entities:
  - mapping_id: PersonMapping
    table: person
    entity_type: http://xmlns.com/foaf/0.1/Person
    identifier:
      column: person_id
      datatype: http://www.w3.org/2001/XMLSchema#integer
    uri_template: "http://example.org/person/{person_id}"
    
    properties:
      - source_column: first_name
        predicate: http://xmlns.com/foaf/0.1/givenName
        datatype: xsd:string
      - source_column: last_name
        predicate: http://xmlns.com/foaf/0.1/familyName
        datatype: xsd:string
      - source_column: email
        predicate: http://xmlns.com/foaf/0.1/mbox
        datatype: xsd:string
      - source_column: birth_date
        predicate: http://xmlns.com/foaf/0.1/birthday
        datatype: xsd:date
    
    relationships:
      - name: WORKS_FOR
        source_column: company_id
        target_mapping: CompanyMapping
        predicate: http://schema.org/worksFor
        cardinality: "*..1"

  - mapping_id: CompanyMapping
    table: company
    entity_type: http://schema.org/Organization
    identifier:
      column: company_id
      datatype: http://www.w3.org/2001/XMLSchema#integer
    uri_template: "http://example.org/company/{company_id}"
    
    properties:
      - source_column: company_name
        predicate: http://schema.org/name
        datatype: xsd:string
      - source_column: industry
        predicate: http://schema.org/industry
        datatype: xsd:string
      - source_column: founded_year
        predicate: http://schema.org/foundingDate
        datatype: xsd:gYear
        transformation: "year_format"

  - mapping_id: EmploymentMapping
    table: employment
    entity_type: http://example.org/Employment
    identifier:
      column: employment_id
      datatype: http://www.w3.org/2001/XMLSchema#integer
    uri_template: "http://example.org/employment/{employment_id}"
    
    properties:
      - source_column: job_title
        predicate: http://schema.org/jobTitle
      - source_column: start_date
        predicate: http://schema.org/startDate
        datatype: xsd:date
      - source_column: salary
        predicate: http://example.org/salary
        datatype: xsd:decimal
    
    relationships:
      - name: HAS_EMPLOYEE
        source_column: person_id
        target_mapping: PersonMapping
        predicate: http://example.org/hasEmployee
      - name: FOR_COMPANY
        source_column: company_id
        target_mapping: CompanyMapping
        predicate: http://example.org/forCompany
```

### Generated R2RML

```turtle
@prefix rr: <http://www.w3.org/ns/r2rml#> .
@prefix foaf: <http://xmlns.com/foaf/0.1/> .
@prefix schema: <http://schema.org/> .
@prefix ex: <http://example.org/> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

ex:PersonMapping a rr:TriplesMap ;
  rr:logicalTable [ rr:tableName "person" ] ;
  rr:subjectMap [
    rr:template "http://example.org/person/{person_id}" ;
    rr:class foaf:Person
  ] ;
  rr:predicateObjectMap [
    rr:predicate foaf:givenName ;
    rr:objectMap [ rr:column "first_name" ]
  ] ;
  rr:predicateObjectMap [
    rr:predicate foaf:familyName ;
    rr:objectMap [ rr:column "last_name" ]
  ] ;
  rr:predicateObjectMap [
    rr:predicate schema:worksFor ;
    rr:objectMap [
      rr:parentTriplesMap ex:CompanyMapping ;
      rr:joinCondition [ rr:child "company_id" ; rr:parent "company_id" ]
    ]
  ] .

ex:CompanyMapping a rr:TriplesMap ;
  rr:logicalTable [ rr:tableName "company" ] ;
  rr:subjectMap [
    rr:template "http://example.org/company/{company_id}" ;
    rr:class schema:Organization
  ] ;
  rr:predicateObjectMap [
    rr:predicate schema:name ;
    rr:objectMap [ rr:column "company_name" ]
  ] ;
  rr:predicateObjectMap [
    rr:predicate schema:industry ;
    rr:objectMap [ rr:column "industry" ]
  ] .
```

---

## Example 2: CSV File Mapping

### Input CSV File (employees.csv)

```csv
employee_id,employee_name,department,manager_id,salary,hire_date
E001,Alice Johnson,Engineering,M001,100000,2020-01-15
E002,Bob Smith,Sales,M002,75000,2021-03-20
E003,Carol Davis,Engineering,M001,95000,2020-06-10
E004,David Wilson,HR,M003,80000,2022-01-05
```

### Generated Mapping DSL

```yaml
mapping: EmployeeCSVMapping
version: 1.0

source:
  type: csv
  file: data/employees.csv
  delimiter: ","
  encoding: utf-8
  header_row: 1
  skip_blank_rows: true

entity:
  mapping_id: EmployeeMapping
  entity_type: http://xmlns.com/foaf/0.1/Person
  identifier:
    column: employee_id
    datatype: xsd:string
  uri_template: "http://example.org/employee/{employee_id}"

properties:
  - source_column: employee_name
    predicate: http://xmlns.com/foaf/0.1/name
    datatype: xsd:string
  - source_column: department
    predicate: http://example.org/department
    datatype: xsd:string
  - source_column: salary
    predicate: http://example.org/salary
    datatype: xsd:decimal
  - source_column: hire_date
    predicate: http://schema.org/startDate
    datatype: xsd:date

relationships:
  - name: REPORTS_TO
    source_column: manager_id
    target_mapping: ManagerMapping
    target_entity_type: http://xmlns.com/foaf/0.1/Person
    target_uri_template: "http://example.org/manager/{manager_id}"
    predicate: http://example.org/reportsTo
    cardinality: "*..1"
```

---

## Example 3: JSON API Response Mapping

### Input JSON API Response

```json
{
  "items": [
    {
      "id": "product_001",
      "name": "Laptop",
      "description": "High-performance laptop",
      "price": 999.99,
      "currency": "USD",
      "category": {
        "id": "cat_001",
        "name": "Electronics"
      },
      "manufacturer": {
        "id": "mfg_001",
        "name": "TechCorp"
      },
      "reviews": [
        {
          "reviewer": "user_123",
          "rating": 5,
          "comment": "Excellent product"
        }
      ]
    }
  ]
}
```

### Generated Mapping DSL

```yaml
mapping: ProductAPIMapping
version: 1.0

source:
  type: json
  location: https://api.example.com/products
  path: $.items[*]
  authentication: bearer_token
  
entities:
  - mapping_id: ProductMapping
    jsonpath: $.
    entity_type: http://schema.org/Product
    identifier:
      jsonpath: $.id
      datatype: xsd:string
    uri_template: "http://example.org/product/{id}"
    
    properties:
      - source_jsonpath: $.name
        predicate: http://schema.org/name
        datatype: xsd:string
      - source_jsonpath: $.description
        predicate: http://schema.org/description
        datatype: xsd:string
      - source_jsonpath: $.price
        predicate: http://schema.org/price
        datatype: xsd:decimal
      - source_jsonpath: $.currency
        predicate: http://schema.org/priceCurrency
        datatype: xsd:string
    
    relationships:
      - name: HAS_CATEGORY
        source_jsonpath: $.category.id
        target_mapping: CategoryMapping
        predicate: http://schema.org/category
        
      - name: MANUFACTURED_BY
        source_jsonpath: $.manufacturer.id
        target_mapping: ManufacturerMapping
        predicate: http://schema.org/manufacturer
      
      - name: HAS_REVIEW
        source_jsonpath: $.reviews[*].id
        target_mapping: ReviewMapping
        predicate: http://schema.org/review

  - mapping_id: CategoryMapping
    jsonpath: $.category
    entity_type: http://schema.org/Category
    identifier:
      jsonpath: $.id
      datatype: xsd:string
    uri_template: "http://example.org/category/{id}"
    
    properties:
      - source_jsonpath: $.name
        predicate: http://schema.org/name

  - mapping_id: ManufacturerMapping
    jsonpath: $.manufacturer
    entity_type: http://schema.org/Organization
    identifier:
      jsonpath: $.id
      datatype: xsd:string
    uri_template: "http://example.org/manufacturer/{id}"
    
    properties:
      - source_jsonpath: $.name
        predicate: http://schema.org/name
```

---

## Example 4: Complex Multi-Table Mapping

### Mapping Configuration

```yaml
mapping: UniversityMapping
version: 1.0
description: Map university database to RDF knowledge graph

source:
  type: database
  connection: mysql://localhost/university

entities:
  # Student Mapping
  - mapping_id: StudentMapping
    table: students
    entity_type: http://example.org/Student
    identifier:
      column: student_id
    uri_template: "http://example.org/student/{student_id}"
    properties:
      - source_column: first_name
        predicate: foaf:givenName
      - source_column: last_name
        predicate: foaf:familyName
      - source_column: email
        predicate: foaf:mbox
      - source_column: enrollment_date
        predicate: schema:startDate
        datatype: xsd:date
    relationships:
      - name: ENROLLED_IN
        source_column: degree_program_id
        target_mapping: DegreeMapping
        predicate: ex:enrolledIn
      - name: ADVISED_BY
        source_column: advisor_id
        target_mapping: ProfessorMapping
        predicate: ex:advisedBy

  # Professor Mapping
  - mapping_id: ProfessorMapping
    table: professors
    entity_type: http://example.org/Professor
    identifier:
      column: professor_id
    uri_template: "http://example.org/professor/{professor_id}"
    properties:
      - source_column: name
        predicate: foaf:name
      - source_column: email
        predicate: foaf:mbox
      - source_column: office
        predicate: ex:office
    relationships:
      - name: TEACHES
        source_column: department_id
        target_mapping: DepartmentMapping
        predicate: ex:partOf

  # Course Mapping
  - mapping_id: CourseMapping
    table: courses
    entity_type: http://schema.org/Course
    identifier:
      column: course_id
    uri_template: "http://example.org/course/{course_id}"
    properties:
      - source_column: course_name
        predicate: schema:name
      - source_column: description
        predicate: schema:description
      - source_column: credit_hours
        predicate: ex:creditHours
        datatype: xsd:integer
    relationships:
      - name: OFFERED_BY
        source_column: department_id
        target_mapping: DepartmentMapping
        predicate: ex:offeredBy

  # Degree Program Mapping
  - mapping_id: DegreeMapping
    table: degree_programs
    entity_type: http://schema.org/EducationalOccupationalCredential
    identifier:
      column: degree_id
    uri_template: "http://example.org/degree/{degree_id}"
    properties:
      - source_column: degree_name
        predicate: schema:name
      - source_column: duration_years
        predicate: ex:duration
        datatype: xsd:integer

  # Department Mapping
  - mapping_id: DepartmentMapping
    table: departments
    entity_type: http://schema.org/Organization
    identifier:
      column: department_id
    uri_template: "http://example.org/department/{department_id}"
    properties:
      - source_column: department_name
        predicate: schema:name
      - source_column: building
        predicate: ex:location
```

---

## Mapping Statistics

| Example | Source | Entities | Properties | Relationships | Output Formats |
|---------|--------|----------|-----------|----------------|----------------|
| Database | SQL | 3 (Person, Company, Employment) | 12 | 5 | DSL, R2RML |
| CSV | File | 1 (Employee) | 5 | 1 | DSL |
| JSON API | HTTP | 4 (Product, Category, Manufacturer, Review) | 8 | 3 | DSL |
| University | SQL | 5 (Student, Professor, Course, Degree, Dept) | 16 | 6 | DSL |

---

See [mapping-patterns.md](../references/mapping-patterns.md) for detailed mapping DSL design patterns.


