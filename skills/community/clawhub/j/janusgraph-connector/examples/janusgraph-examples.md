# JanusGraph Examples

This file contains 5 complete, production-ready examples of JanusGraph usage across different domains. Each example demonstrates real-world scenarios with full Gremlin queries and Python implementation.

---

## Table of Contents

1. [Social Network Graph](#1-social-network-graph)
2. [E-Commerce Knowledge Graph](#2-e-commerce-knowledge-graph)
3. [Knowledge Base Graph](#3-knowledge-base-graph)
4. [Organizational Hierarchy](#4-organizational-hierarchy)
5. [Research Paper Citation Network](#5-research-paper-citation-network)

---

## 1. Social Network Graph

### Domain Description

A social network graph modeling users, their relationships, and interactions. Demonstrates:
- User relationships (FOLLOWS, FRIENDS_WITH)
- Finding mutual connections
- Computing social distance
- Identifying influencers
- Recommendation generation

### Data Model

**Vertices:**
- `User` - Person node with properties: name, age, email, joined_date, location

**Edges:**
- `FOLLOWS` - One-way following relationship (from → to)
- `FRIENDS_WITH` - Mutual friendship (bidirectional)
- `COMMENTED_ON` - User comments on post

**Properties:**
- Edges may have timestamps, interaction counts

### Schema Creation (Gremlin)

```gremlin
// Create User vertices
g.addV("User").property("name", "Alice").property("age", 28).property("email", "alice@example.com").property("location", "New York")
g.addV("User").property("name", "Bob").property("age", 32).property("email", "bob@example.com").property("location", "San Francisco")
g.addV("User").property("name", "Charlie").property("age", 25).property("email", "charlie@example.com").property("location", "Boston")
g.addV("User").property("name", "Diana").property("age", 30).property("email", "diana@example.com").property("location", "New York")
g.addV("User").property("name", "Eve").property("age", 26).property("email", "eve@example.com").property("location", "Austin")

// Create FOLLOWS relationships
g.V().has("User", "name", "Alice").addE("FOLLOWS").to(g.V().has("User", "name", "Bob"))
g.V().has("User", "name", "Bob").addE("FOLLOWS").to(g.V().has("User", "name", "Charlie"))
g.V().has("User", "name", "Charlie").addE("FOLLOWS").to(g.V().has("User", "name", "Alice"))
g.V().has("User", "name", "Diana").addE("FOLLOWS").to(g.V().has("User", "name", "Alice"))
g.V().has("User", "name", "Diana").addE("FOLLOWS").to(g.V().has("User", "name", "Eve"))
```

### Example Queries

#### Query 1: Get Alice's followers
```gremlin
g.V().has("User", "name", "Alice")
  .in("FOLLOWS")
  .values("name")
```

**Output:**
```
Diana
Charlie
```

#### Query 2: Find mutual friends between Alice and Bob
```gremlin
g.V().has("User", "name", "Alice")
  .out("FOLLOWS")
  .where(out("FOLLOWS").has("name", "Bob"))
  .values("name")
```

#### Query 3: Find influencers (users with most followers)
```gremlin
g.V().hasLabel("User")
  .in("FOLLOWS")
  .count()
  .order()
  .limit(5)
```

#### Query 4: Calculate shortest path from Alice to Charlie
```gremlin
g.V().has("User", "name", "Alice")
  .repeat(out("FOLLOWS"))
  .until(has("name", "Charlie"))
  .path()
  .limit(1)
```

#### Query 5: Get recommendations for Alice (friends of friends)
```gremlin
g.V().has("User", "name", "Alice")
  .out("FOLLOWS")
  .out("FOLLOWS")
  .dedup()
  .where(neq(Alice))
  .values("name")
```

### Python Implementation

```python
from janusgraph_connector import JanusGraphConnector, ConnectionConfig

# Setup
config = ConnectionConfig(host="localhost", port=8182)
connector = JanusGraphConnector()
connector.connect(config)

# Get followers of a user
def get_followers(username):
    query = f"""
    g.V().has("User", "name", "{username}")
      .in("FOLLOWS")
      .values("name")
    """
    result = connector.execute_query(query)
    return result.records

# Find recommendations
def get_recommendations(username):
    query = f"""
    g.V().has("User", "name", "{username}")
      .out("FOLLOWS")
      .out("FOLLOWS")
      .dedup()
      .values("name")
    """
    result = connector.execute_query(query)
    return result.records

# Get users by location
def get_users_by_location(location):
    query = f"""
    g.V().hasLabel("User").has("location", "{location}")
      .values("name")
    """
    result = connector.execute_query(query)
    return result.records

# Usage
followers = get_followers("Alice")
print(f"Followers: {followers}")

recommendations = get_recommendations("Alice")
print(f"Recommendations: {recommendations}")

users_nyc = get_users_by_location("New York")
print(f"Users in NYC: {users_nyc}")

connector.close()
```

---

## 2. E-Commerce Knowledge Graph

### Domain Description

An e-commerce graph modeling products, categories, suppliers, and customer interactions. Demonstrates:
- Product categorization and hierarchy
- Supplier relationships
- Customer purchase history
- Inventory management
- Recommendation based on co-purchases

### Data Model

**Vertices:**
- `Product` - Product with: id, name, price, stock_level
- `Category` - Product category with: name, description
- `Supplier` - Supplier company with: name, country, rating
- `Customer` - Customer with: name, email, account_created

**Edges:**
- `IN_CATEGORY` - Product belongs to category
- `SUPPLIED_BY` - Product supplied by supplier
- `PURCHASED` - Customer purchased product (with date, quantity, price properties)
- `SIMILAR_TO` - Product similarity relationship
- `VARIANT_OF` - Product variants

### Schema Creation

```gremlin
// Create Products
g.addV("Product").property("id", "P001").property("name", "Laptop").property("price", 999.99).property("stock_level", 50)
g.addV("Product").property("id", "P002").property("name", "Mouse").property("price", 29.99).property("stock_level", 500)
g.addV("Product").property("id", "P003").property("name", "Keyboard").property("price", 79.99).property("stock_level", 200)

// Create Categories
g.addV("Category").property("name", "Electronics").property("description", "Electronic devices")
g.addV("Category").property("name", "Accessories").property("description", "Computer accessories")

// Create Suppliers
g.addV("Supplier").property("name", "Tech Corp").property("country", "USA").property("rating", 4.8)
g.addV("Supplier").property("name", "Global Supply").property("country", "China").property("rating", 4.5)

// Create Customers
g.addV("Customer").property("name", "John Doe").property("email", "john@example.com")
g.addV("Customer").property("name", "Jane Smith").property("email", "jane@example.com")

// Create IN_CATEGORY edges
g.V().has("Product", "name", "Laptop").addE("IN_CATEGORY").to(g.V().has("Category", "name", "Electronics"))
g.V().has("Product", "name", "Mouse").addE("IN_CATEGORY").to(g.V().has("Category", "name", "Accessories"))

// Create SUPPLIED_BY edges
g.V().has("Product", "name", "Laptop").addE("SUPPLIED_BY").to(g.V().has("Supplier", "name", "Tech Corp"))
g.V().has("Product", "name", "Mouse").addE("SUPPLIED_BY").to(g.V().has("Supplier", "name", "Global Supply"))

// Create PURCHASED edges
g.V().has("Customer", "name", "John Doe").addE("PURCHASED").to(g.V().has("Product", "name", "Laptop")).property("date", "2024-01-15").property("quantity", 1).property("price", 999.99)
```

### Example Queries

#### Query 1: Get all products in a category
```gremlin
g.V().has("Category", "name", "Electronics")
  .in("IN_CATEGORY")
  .values("name", "price")
```

#### Query 2: Find products supplied by a specific supplier
```gremlin
g.V().has("Supplier", "name", "Tech Corp")
  .in("SUPPLIED_BY")
  .values("name", "price")
```

#### Query 3: Get purchase history of a customer
```gremlin
g.V().has("Customer", "name", "John Doe")
  .out("PURCHASED")
  .as("product")
  .select("product")
  .values("name", "price")
```

#### Query 4: Find co-purchased products
```gremlin
g.V().has("Product", "name", "Laptop")
  .in("PURCHASED")
  .out("PURCHASED")
  .dedup()
  .where(neq(Laptop))
  .values("name")
```

#### Query 5: Get low stock products
```gremlin
g.V().hasLabel("Product")
  .has("stock_level", lt(100))
  .values("id", "name", "stock_level")
```

### Python Implementation

```python
from janusgraph_connector import JanusGraphConnector, ConnectionConfig

config = ConnectionConfig(host="localhost", port=8182)
connector = JanusGraphConnector()
connector.connect(config)

def get_category_products(category_name):
    query = f"""
    g.V().has("Category", "name", "{category_name}")
      .in("IN_CATEGORY")
      .values("name", "price")
    """
    return connector.execute_query(query).records

def get_customer_purchase_history(customer_name):
    query = f"""
    g.V().has("Customer", "name", "{customer_name}")
      .out("PURCHASED")
      .values("name")
    """
    return connector.execute_query(query).records

def get_co_purchased_products(product_name):
    query = f"""
    g.V().has("Product", "name", "{product_name}")
      .in("PURCHASED")
      .out("PURCHASED")
      .dedup()
      .values("name")
    """
    return connector.execute_query(query).records

def get_low_stock_alerts(threshold=100):
    query = f"""
    g.V().hasLabel("Product")
      .has("stock_level", lt({threshold}))
      .valueMap()
    """
    return connector.execute_query(query).records

# Usage
electronics = get_category_products("Electronics")
print(f"Electronics: {electronics}")

history = get_customer_purchase_history("John Doe")
print(f"Purchase History: {history}")

recommendations = get_co_purchased_products("Laptop")
print(f"Often bought with Laptop: {recommendations}")

low_stock = get_low_stock_alerts(100)
print(f"Low stock: {low_stock}")

connector.close()
```

---

## 3. Knowledge Base Graph

### Domain Description

A documentation/knowledge base graph with topics, prerequisites, and learning paths. Demonstrates:
- Topic hierarchies
- Prerequisite chains
- Learning path generation
- Dependency resolution
- Progress tracking

### Data Model

**Vertices:**
- `Topic` - Learning topic with: name, description, difficulty, estimated_hours
- `Resource` - Learning resource with: title, url, type (video, article, course)
- `User` - Learner with: name, email

**Edges:**
- `HAS_PREREQUISITE` - Topic prerequisite relationship
- `COVERS` - Resource covers topic
- `COMPLETED_BY` - User completed topic (with date, score)

### Schema Creation

```gremlin
// Create Topics
g.addV("Topic").property("name", "Python Basics").property("difficulty", 1).property("estimated_hours", 10)
g.addV("Topic").property("name", "Data Structures").property("difficulty", 2).property("estimated_hours", 20)
g.addV("Topic").property("name", "Algorithms").property("difficulty", 3).property("estimated_hours", 25)
g.addV("Topic").property("name", "Graph Theory").property("difficulty", 4).property("estimated_hours", 30)

// Create Resources
g.addV("Resource").property("title", "Python for Beginners").property("url", "https://example.com/python").property("type", "video")
g.addV("Resource").property("title", "Data Structures Handbook").property("url", "https://example.com/ds").property("type", "article")

// Create Prerequisites
g.V().has("Topic", "name", "Data Structures").addE("HAS_PREREQUISITE").to(g.V().has("Topic", "name", "Python Basics"))
g.V().has("Topic", "name", "Algorithms").addE("HAS_PREREQUISITE").to(g.V().has("Topic", "name", "Data Structures"))
g.V().has("Topic", "name", "Graph Theory").addE("HAS_PREREQUISITE").to(g.V().has("Topic", "name", "Algorithms"))

// Map Resources to Topics
g.V().has("Resource", "title", "Python for Beginners").addE("COVERS").to(g.V().has("Topic", "name", "Python Basics"))
```

### Example Queries

#### Query 1: Get prerequisites for a topic
```gremlin
g.V().has("Topic", "name", "Algorithms")
  .repeat(out("HAS_PREREQUISITE")).until(not(out("HAS_PREREQUISITE")))
  .values("name")
```

#### Query 2: Find learning path from Topic A to Topic B
```gremlin
g.V().has("Topic", "name", "Python Basics")
  .repeat(out("HAS_PREREQUISITE")).times(3)
  .values("name")
```

#### Query 3: Get resources for a topic
```gremlin
g.V().has("Topic", "name", "Python Basics")
  .in("COVERS")
  .values("title", "url", "type")
```

#### Query 4: Get recommended next topics
```gremlin
g.V().has("Topic", "name", "Python Basics")
  .in("HAS_PREREQUISITE")
  .values("name")
```

### Python Implementation

```python
from janusgraph_connector import JanusGraphConnector, ConnectionConfig

config = ConnectionConfig(host="localhost", port=8182)
connector = JanusGraphConnector()
connector.connect(config)

def get_prerequisites(topic_name):
    query = f"""
    g.V().has("Topic", "name", "{topic_name}")
      .repeat(out("HAS_PREREQUISITE"))
      .until(not(out("HAS_PREREQUISITE")))
      .values("name")
    """
    return connector.execute_query(query).records

def get_learning_path(start_topic):
    query = f"""
    g.V().has("Topic", "name", "{start_topic}")
      .in("HAS_PREREQUISITE")
      .values("name")
    """
    return connector.execute_query(query).records

def get_resources_for_topic(topic_name):
    query = f"""
    g.V().has("Topic", "name", "{topic_name}")
      .in("COVERS")
      .values("title", "url", "type")
    """
    return connector.execute_query(query).records

# Usage
prereqs = get_prerequisites("Algorithms")
print(f"Prerequisites: {prereqs}")

path = get_learning_path("Python Basics")
print(f"Next topics: {path}")

resources = get_resources_for_topic("Python Basics")
print(f"Resources: {resources}")

connector.close()
```

---

## 4. Organizational Hierarchy

### Domain Description

An organizational structure graph modeling employees, departments, and management relationships. Demonstrates:
- Org hierarchy traversal
- Chain of command queries
- Department structure
- Reporting relationships

### Data Model

**Vertices:**
- `Employee` - Employee with: id, name, email, job_title, salary
- `Department` - Department with: name, budget
- `Office` - Office location with: city, country

**Edges:**
- `WORKS_IN` - Employee works in department
- `REPORTS_TO` - Employee reports to manager
- `MANAGES` - Manager manages department
- `LOCATED_IN` - Department located in office

### Schema Creation

```gremlin
// Create Employees
g.addV("Employee").property("id", "E001").property("name", "CEO").property("job_title", "Chief Executive Officer")
g.addV("Employee").property("id", "E002").property("name", "VP Engineering").property("job_title", "VP Engineering")
g.addV("Employee").property("id", "E003").property("name", "Engineering Manager").property("job_title", "Manager")
g.addV("Employee").property("id", "E004").property("name", "Developer 1").property("job_title", "Software Engineer")

// Create Departments
g.addV("Department").property("name", "Engineering").property("budget", 5000000)

// Create Offices
g.addV("Office").property("city", "San Francisco").property("country", "USA")

// Create relationships
g.V().has("Employee", "name", "VP Engineering").addE("REPORTS_TO").to(g.V().has("Employee", "name", "CEO"))
g.V().has("Employee", "name", "Engineering Manager").addE("REPORTS_TO").to(g.V().has("Employee", "name", "VP Engineering"))
g.V().has("Employee", "name", "Developer 1").addE("REPORTS_TO").to(g.V().has("Employee", "name", "Engineering Manager"))
```

### Example Queries

#### Query 1: Get chain of command for an employee
```gremlin
g.V().has("Employee", "name", "Developer 1")
  .repeat(out("REPORTS_TO")).until(not(out("REPORTS_TO")))
  .values("name", "job_title")
```

#### Query 2: Get direct reports of a manager
```gremlin
g.V().has("Employee", "name", "VP Engineering")
  .in("REPORTS_TO")
  .values("name", "job_title")
```

#### Query 3: Get org structure (all levels)
```gremlin
g.V().has("Employee", "name", "CEO")
  .repeat(in("REPORTS_TO")).times(5)
  .path()
```

### Python Implementation

```python
from janusgraph_connector import JanusGraphConnector, ConnectionConfig

config = ConnectionConfig(host="localhost", port=8182)
connector = JanusGraphConnector()
connector.connect(config)

def get_chain_of_command(employee_name):
    query = f"""
    g.V().has("Employee", "name", "{employee_name}")
      .repeat(out("REPORTS_TO"))
      .until(not(out("REPORTS_TO")))
      .values("name", "job_title")
    """
    return connector.execute_query(query).records

def get_direct_reports(manager_name):
    query = f"""
    g.V().has("Employee", "name", "{manager_name}")
      .in("REPORTS_TO")
      .values("name", "job_title")
    """
    return connector.execute_query(query).records

# Usage
command_chain = get_chain_of_command("Developer 1")
print(f"Chain of command: {command_chain}")

reports = get_direct_reports("VP Engineering")
print(f"Direct reports: {reports}")

connector.close()
```

---

## 5. Research Paper Citation Network

### Domain Description

A research network graph modeling papers, authors, citations, and research topics. Demonstrates:
- Citation networks
- Co-authorship relationships
- Research trajectory analysis
- Topic similarity

### Data Model

**Vertices:**
- `Paper` - Research paper with: id, title, year, venue
- `Author` - Researcher with: id, name, email, affiliation
- `Topic` - Research topic with: name
- `Venue` - Conference/Journal with: name, rank

**Edges:**
- `AUTHORED_BY` - Paper written by author
- `CITES` - Paper cites another paper (with count property)
- `RESEARCHES` - Author researches topic
- `PUBLISHED_IN` - Paper published in venue

### Schema Creation

```gremlin
// Create Papers
g.addV("Paper").property("id", "P001").property("title", "Graph Databases for KGs").property("year", 2020).property("venue", "SIGMOD")
g.addV("Paper").property("id", "P002").property("title", "Distributed Graph Processing").property("year", 2019).property("venue", "VLDB")

// Create Authors
g.addV("Author").property("id", "A001").property("name", "Alice Researcher").property("affiliation", "MIT")
g.addV("Author").property("id", "A002").property("name", "Bob Scholar").property("affiliation", "Stanford")

// Create Topics
g.addV("Topic").property("name", "Graph Databases")
g.addV("Topic").property("name", "Knowledge Graphs")

// Create relationships
g.V().has("Paper", "title", "Graph Databases for KGs").addE("AUTHORED_BY").to(g.V().has("Author", "name", "Alice Researcher"))
g.V().has("Paper", "id", "P001").addE("CITES").to(g.V().has("Paper", "id", "P002")).property("count", 3)
g.V().has("Author", "name", "Alice Researcher").addE("RESEARCHES").to(g.V().has("Topic", "name", "Graph Databases"))
```

### Example Queries

#### Query 1: Get all papers by an author
```gremlin
g.V().has("Author", "name", "Alice Researcher")
  .in("AUTHORED_BY")
  .values("title", "year")
```

#### Query 2: Get citation count for a paper
```gremlin
g.V().has("Paper", "title", "Graph Databases for KGs")
  .in("CITES")
  .count()
```

#### Query 3: Find papers citing a specific paper
```gremlin
g.V().has("Paper", "title", "Graph Databases for KGs")
  .in("CITES")
  .values("title", "year")
```

#### Query 4: Get co-authors
```gremlin
g.V().has("Author", "name", "Alice Researcher")
  .in("AUTHORED_BY")
  .out("AUTHORED_BY")
  .dedup()
  .where(neq(Alice))
  .values("name")
```

#### Query 5: Get research trajectory of an author
```gremlin
g.V().has("Author", "name", "Alice Researcher")
  .in("AUTHORED_BY")
  .order().by("year")
  .values("title", "year")
```

### Python Implementation

```python
from janusgraph_connector import JanusGraphConnector, ConnectionConfig

config = ConnectionConfig(host="localhost", port=8182)
connector = JanusGraphConnector()
connector.connect(config)

def get_author_papers(author_name):
    query = f"""
    g.V().has("Author", "name", "{author_name}")
      .in("AUTHORED_BY")
      .order().by("year", desc)
      .values("title", "year")
    """
    return connector.execute_query(query).records

def get_paper_citations(paper_title):
    query = f"""
    g.V().has("Paper", "title", "{paper_title}")
      .in("CITES")
      .count()
    """
    return connector.execute_query(query).records

def get_citing_papers(paper_title):
    query = f"""
    g.V().has("Paper", "title", "{paper_title}")
      .in("CITES")
      .values("title", "year")
    """
    return connector.execute_query(query).records

def get_coauthors(author_name):
    query = f"""
    g.V().has("Author", "name", "{author_name}")
      .in("AUTHORED_BY")
      .out("AUTHORED_BY")
      .dedup()
      .values("name")
    """
    return connector.execute_query(query).records

# Usage
papers = get_author_papers("Alice Researcher")
print(f"Papers by Alice: {papers}")

citations = get_paper_citations("Graph Databases for KGs")
print(f"Citation count: {citations}")

citing = get_citing_papers("Graph Databases for KGs")
print(f"Papers citing: {citing}")

coauthors = get_coauthors("Alice Researcher")
print(f"Co-authors: {coauthors}")

connector.close()
```

---

## Summary

These 5 examples demonstrate:

✅ **Social Network** - Relationship analysis and recommendation  
✅ **E-Commerce** - Product catalog and purchase patterns  
✅ **Knowledge Base** - Learning paths and prerequisites  
✅ **Organization** - Hierarchy and reporting structures  
✅ **Research Network** - Citation analysis and collaboration  

Each example includes:
- Complete data model definition
- Schema creation queries
- 4-5 representative queries
- Full Python implementation with helper functions

All examples follow best practices:
- Proper vertex/edge labeling
- Meaningful property names
- Efficient traversals
- Real-world scenarios

---

**Last Updated:** April 12, 2026  
**JanusGraph Version:** 0.6.0+  
**Gremlin Version:** 3.6.0+

