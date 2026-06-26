# Property Graph Schema Examples

Complete Neo4j-style property graph schemas for different domains.

## Example 1: University Domain

### Domain Description

```
A university contains students, professors, courses, and departments.
Students enroll in courses. Professors teach courses.
Departments manage professors and courses.
Courses have prerequisites. Professors have research areas.
```

### Schema Design

```
NODE LABELS
├── Student
│   ├── student_id: String (UNIQUE)
│   ├── name: String
│   ├── email: String
│   └── enrollment_year: Integer
├── Professor
│   ├── professor_id: String (UNIQUE)
│   ├── name: String
│   ├── email: String
│   └── research_area: String
├── Course
│   ├── course_code: String (UNIQUE)
│   ├── title: String
│   ├── credits: Integer
│   └── description: String
└── Department
    ├── dept_id: String (UNIQUE)
    ├── name: String
    ├── budget: Float
    └── chair: String

RELATIONSHIPS
├── (Student)-[:ENROLLED_IN {semester, grade}]->(Course)
├── (Professor)-[:TEACHES {semester}]->(Course)
├── (Professor)-[:WORKS_IN]->(Department)
├── (Department)-[:OFFERS]->(Course)
├── (Course)-[:REQUIRES]->(Course)
└── (Department)-[:HAS_CHAIR]->(Professor)

CONSTRAINTS & INDEXES
├── CREATE CONSTRAINT student_id UNIQUE on (s:Student) REQUIRE s.student_id
├── CREATE CONSTRAINT professor_id UNIQUE on (p:Professor) REQUIRE p.professor_id
├── CREATE CONSTRAINT course_code UNIQUE on (c:Course) REQUIRE c.course_code
├── CREATE CONSTRAINT dept_id UNIQUE on (d:Department) REQUIRE d.dept_id
├── CREATE INDEX ON (s:Student)(name)
├── CREATE INDEX ON (p:Professor)(research_area)
└── CREATE INDEX ON (c:Course)(title)
```

### Cypher Implementation

```cypher
-- Create nodes
CREATE (s:Student {student_id: "S001", name: "Alice", email: "alice@uni.edu", enrollment_year: 2024})
CREATE (p:Professor {professor_id: "P001", name: "Dr. Smith", email: "smith@uni.edu", research_area: "AI"})
CREATE (c:Course {course_code: "CS101", title: "Intro to CS", credits: 3})
CREATE (d:Department {dept_id: "D001", name: "Computer Science", budget: 100000.0})

-- Create relationships
CREATE (s)-[:ENROLLED_IN {semester: "Fall2024", grade: "A"}]->(c)
CREATE (p)-[:TEACHES {semester: "Fall2024"}]->(c)
CREATE (p)-[:WORKS_IN]->(d)
CREATE (d)-[:OFFERS]->(c)

-- Query example
MATCH (s:Student)-[:ENROLLED_IN {semester: "Fall2024"}]->(c:Course)<-[:TEACHES]-(p:Professor)
RETURN s.name, c.title, p.name;
```

---

## Example 2: E-Commerce Domain

### Domain Description

```
An e-commerce platform has customers, products, orders, and categories.
Customers place orders. Orders contain products.
Products belong to categories. Customers write reviews.
Suppliers provide products. Orders have order items.
```

### Schema Design

```
NODE LABELS
├── Customer
│   ├── customer_id: String (UNIQUE)
│   ├── name: String
│   ├── email: String (UNIQUE)
│   ├── phone: String
│   └── registration_date: Date
├── Product
│   ├── product_id: String (UNIQUE)
│   ├── name: String
│   ├── price: Float
│   ├── sku: String (UNIQUE)
│   └── description: String
├── Order
│   ├── order_id: String (UNIQUE)
│   ├── order_date: Date
│   ├── total_amount: Float
│   ├── status: String
│   └── shipping_address: String
├── OrderItem
│   ├── order_item_id: String (UNIQUE)
│   ├── quantity: Integer
│   ├── unit_price: Float
│   └── subtotal: Float
├── Category
│   ├── category_id: String (UNIQUE)
│   ├── name: String
│   └── description: String
├── Review
│   ├── review_id: String (UNIQUE)
│   ├── rating: Integer
│   ├── text: String
│   └── review_date: Date
└── Supplier
    ├── supplier_id: String (UNIQUE)
    ├── name: String
    ├── contact: String
    └── rating: Float

RELATIONSHIPS
├── (Customer)-[:PLACES]->(Order)
├── (Order)-[:CONTAINS {qty, price}]->(OrderItem)
├── (OrderItem)-[:OF_PRODUCT]->(Product)
├── (Product)-[:BELONGS_TO]->(Category)
├── (Customer)-[:WROTE]->(Review)
├── (Review)-[:REVIEWS]->(Product)
├── (Supplier)-[:PROVIDES]->(Product)
└── (Customer)-[:PURCHASED]->(Product)

CONSTRAINTS & INDEXES
├── CREATE CONSTRAINT customer_id UNIQUE on (c:Customer) REQUIRE c.customer_id
├── CREATE CONSTRAINT email UNIQUE on (c:Customer) REQUIRE c.email
├── CREATE CONSTRAINT product_id UNIQUE on (p:Product) REQUIRE p.product_id
├── CREATE CONSTRAINT order_id UNIQUE on (o:Order) REQUIRE o.order_id
├── CREATE INDEX ON (p:Product)(name)
├── CREATE INDEX ON (p:Product)(price)
└── CREATE INDEX ON (o:Order)(order_date)
```

### Cypher Queries

```cypher
-- Find products in a category
MATCH (c:Category {name: "Electronics"})<-[:BELONGS_TO]-(p:Product)
RETURN p.name, p.price
ORDER BY p.price DESC;

-- Find orders by customer
MATCH (cust:Customer {name: "Alice"})-[:PLACES]->(o:Order)
RETURN o.order_id, o.order_date, o.total_amount;

-- Get products in an order
MATCH (o:Order {order_id: "O001"})-[:CONTAINS]->(oi:OrderItem)-[:OF_PRODUCT]->(p:Product)
RETURN p.name, oi.quantity, oi.unit_price;
```

---

## Example 3: Social Network Domain

### Domain Description

```
Users follow each other. Users post content.
Posts can have comments. Users like posts and comments.
Users belong to groups. Content is tagged with topics.
```

### Schema Design

```
NODE LABELS
├── User
│   ├── user_id: String (UNIQUE)
│   ├── username: String (UNIQUE)
│   ├── email: String (UNIQUE)
│   ├── bio: String
│   └── joined_date: Date
├── Post
│   ├── post_id: String (UNIQUE)
│   ├── content: String
│   ├── created_date: Date
│   ├── likes_count: Integer
│   └── is_public: Boolean
├── Comment
│   ├── comment_id: String (UNIQUE)
│   ├── content: String
│   ├── created_date: Date
│   └── likes_count: Integer
├── Group
│   ├── group_id: String (UNIQUE)
│   ├── name: String
│   ├── description: String
│   └── created_date: Date
└── Topic
    ├── topic_id: String (UNIQUE)
    ├── name: String
    └── description: String

RELATIONSHIPS
├── (User)-[:FOLLOWS]->(User)
├── (User)-[:CREATED]->(Post)
├── (Post)-[:HAS_COMMENT]->(Comment)
├── (User)-[:COMMENTED_ON]->(Post)
├── (User)-[:LIKED]->(Post)
├── (User)-[:LIKED_COMMENT]->(Comment)
├── (User)-[:MEMBER_OF]->(Group)
├── (Post)-[:TAGGED_WITH]->(Topic)
├── (User)-[:INTERESTED_IN]->(Topic)
└── (Group)-[:ABOUT]->(Topic)

CONSTRAINTS & INDEXES
├── CREATE CONSTRAINT user_id UNIQUE on (u:User) REQUIRE u.user_id
├── CREATE CONSTRAINT username UNIQUE on (u:User) REQUIRE u.username
├── CREATE CONSTRAINT email UNIQUE on (u:User) REQUIRE u.email
├── CREATE CONSTRAINT post_id UNIQUE on (p:Post) REQUIRE p.post_id
├── CREATE INDEX ON (u:User)(username)
├── CREATE INDEX ON (p:Post)(created_date)
└── CREATE INDEX ON (t:Topic)(name)
```

### Cypher Queries

```cypher
-- Find user's timeline (posts from followed users)
MATCH (u:User {username: "alice"})-[:FOLLOWS]->(f:User)-[:CREATED]->(p:Post)
RETURN f.username, p.content, p.created_date
ORDER BY p.created_date DESC;

-- Find trending topics
MATCH (t:Topic)<-[:TAGGED_WITH]-(p:Post)-[:LIKED]-(u:User)
RETURN t.name, COUNT(u) as likes
ORDER BY likes DESC
LIMIT 10;

-- Find posts liked by followed users
MATCH (u:User {username: "alice"})-[:FOLLOWS]->(f:User)
MATCH (f)-[:LIKED]->(p:Post)
RETURN p.content, p.likes_count;
```

---

## Schema Comparison

| Aspect | University | E-Commerce | Social |
|--------|-----------|-----------|--------|
| **Node Labels** | 4 | 7 | 5 |
| **Relationships** | 6 | 8 | 9 |
| **Total Properties** | 15 | 30 | 20 |
| **Constraints** | 4 | 4 | 3 |
| **Indexes** | 3 | 3 | 3 |
| **Complexity** | Medium | High | High |

---

See [schema-patterns.md](../references/schema-patterns.md) for design patterns and best practices.

