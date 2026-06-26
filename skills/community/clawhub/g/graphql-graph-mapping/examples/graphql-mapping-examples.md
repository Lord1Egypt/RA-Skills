# GraphQL Graph Mapping - Examples

Real-world examples demonstrating GraphQL-to-graph database translation across multiple domains.

---

## Example 1: Social Network Domain

Map social network relationships via GraphQL to graph database queries.

### GraphQL Schema

```graphql
type User {
  id: ID!
  username: String!
  email: String
  bio: String
  followers: [User!]!
  following: [User!]!
  posts: [Post!]!
}

type Post {
  id: ID!
  title: String!
  content: String!
  author: User!
  likedBy: [User!]!
  comments: [Comment!]!
}

type Comment {
  id: ID!
  content: String!
  author: User!
  post: Post!
}

type Query {
  user(id: ID!): User
  userByUsername(username: String!): User
  feed(userId: ID!, limit: Int): [Post!]!
}
```

### Input GraphQL Query

```graphql
{
  user(id: "user123") {
    username
    email
    followers(limit: 5) {
      username
      email
    }
    posts(limit: 3) {
      title
      content
      likedBy {
        username
      }
    }
  }
}
```

### Neo4j Cypher Translation

```cypher
MATCH (u:User {id: "user123"})
RETURN u.username, u.email,
       [(f)-[:FOLLOWS]->(u) | {username: f.username, email: f.email}][0..5] AS followers,
       [(u)-[:POSTED]->(p:Post) | {
         title: p.title,
         content: p.content,
         likedBy: [(l:User)-[:LIKES]->(p) | {username: l.username}]
       }][0..3] AS posts
```

### Gremlin Translation

```gremlin
g.V().has("User","id","user123")
  .project("username","email","followers","posts")
  .by("username")
  .by("email")
  .by(in("FOLLOWS").limit(5).values("username","email").fold())
  .by(out("POSTED").limit(3).project("title","content","likedBy")
    .by("title")
    .by("content")
    .by(in("LIKES").values("username").fold())
    .fold())
```

### SPARQL Translation

```sparql
PREFIX ex: <http://example.org/>

SELECT ?username ?email ?followerUsername ?postTitle ?postContent ?likerUsername
WHERE {
  ex:user123 ex:username ?username ;
             ex:email ?email .
  
  ?follower ex:follows ex:user123 ;
            ex:username ?followerUsername .
  
  ex:user123 ex:posted ?post .
  ?post ex:title ?postTitle ;
        ex:content ?postContent .
  
  ?liker ex:likes ?post ;
         ex:username ?likerUsername .
}
LIMIT 100
```

### Expected JSON Response

```json
{
  "data": {
    "user": {
      "username": "alice_wonder",
      "email": "alice@example.com",
      "followers": [
        {
          "username": "bob_builder",
          "email": "bob@example.com"
        },
        {
          "username": "carol_dev",
          "email": "carol@example.com"
        }
      ],
      "posts": [
        {
          "title": "My First Post",
          "content": "Hello, social network!",
          "likedBy": [
            {
              "username": "bob_builder"
            },
            {
              "username": "dave_analyst"
            }
          ]
        }
      ]
    }
  }
}
```

---

## Example 2: E-Commerce Knowledge Graph

Map product relationships and recommendations through GraphQL.

### GraphQL Schema

```graphql
type Product {
  id: ID!
  name: String!
  description: String
  price: Float!
  category: Category!
  supplier: Supplier!
  relatedProducts: [Product!]!
  reviews: [Review!]!
  inventory: Int!
}

type Category {
  id: ID!
  name: String!
  products(limit: Int): [Product!]!
}

type Supplier {
  id: ID!
  name: String!
  products: [Product!]!
}

type Review {
  id: ID!
  rating: Int!
  content: String!
  reviewer: User!
  product: Product!
}

type User {
  id: ID!
  username: String!
  reviews: [Review!]!
}

type Query {
  product(id: ID!): Product
  category(id: ID!): Category
  recommendations(productId: ID!, limit: Int): [Product!]!
}
```

### Input GraphQL Query

```graphql
{
  product(id: "prod_001") {
    name
    price
    category {
      name
      products(limit: 5) {
        name
        price
      }
    }
    supplier {
      name
    }
    relatedProducts(limit: 3) {
      name
      price
    }
    reviews(limit: 5) {
      rating
      content
      reviewer {
        username
      }
    }
  }
}
```

### Neo4j Cypher Translation

```cypher
MATCH (p:Product {id: "prod_001"})
MATCH (p)-[:IN_CATEGORY]->(cat:Category)
MATCH (p)-[:SUPPLIED_BY]->(sup:Supplier)
OPTIONAL MATCH (p)-[:RELATED_TO]->(related:Product)
OPTIONAL MATCH (p)<-[:REVIEWS]-(review:Review)<-[:WROTE]-(user:User)

WITH p, cat, sup, review, user, related
RETURN p.name, p.price,
       {name: cat.name,
        products: [(cat)-[:HAS_PRODUCT]->(cp:Product) | {name: cp.name, price: cp.price}][0..5]
       } AS category,
       {name: sup.name} AS supplier,
       [related | {name: related.name, price: related.price}][0..3] AS relatedProducts,
       [review | {rating: review.rating, content: review.content, reviewer: {username: user.username}}][0..5] AS reviews
```

### Gremlin Translation

```gremlin
g.V().has("Product","id","prod_001")
  .project("name","price","category","supplier","relatedProducts","reviews")
  .by("name")
  .by("price")
  .by(out("IN_CATEGORY").project("name","products")
    .by("name")
    .by(out("HAS_PRODUCT").limit(5).values("name","price").fold())
    .fold())
  .by(out("SUPPLIED_BY").values("name").fold())
  .by(out("RELATED_TO").limit(3).values("name","price").fold())
  .by(in("REVIEWS").in("WROTE").limit(5).project("rating","content","reviewer")
    .by("rating")
    .by("content")
    .by(values("username").fold())
    .fold())
```

### Result Mapping

```json
{
  "data": {
    "product": {
      "name": "Wireless Headphones",
      "price": 79.99,
      "category": {
        "name": "Audio Equipment",
        "products": [
          {
            "name": "USB-C Cable",
            "price": 12.99
          },
          {
            "name": "Portable Speaker",
            "price": 49.99
          }
        ]
      },
      "supplier": {
        "name": "TechCorp Industries"
      },
      "relatedProducts": [
        {
          "name": "Phone Case",
          "price": 19.99
        },
        {
          "name": "Screen Protector",
          "price": 9.99
        }
      ],
      "reviews": [
        {
          "rating": 5,
          "content": "Excellent sound quality!",
          "reviewer": {
            "username": "happy_customer_42"
          }
        }
      ]
    }
  }
}
```

---

## Example 3: Research Publication Knowledge Graph

Map academic relationships and citations through GraphQL.

### GraphQL Schema

```graphql
type Researcher {
  id: ID!
  name: String!
  email: String
  affiliation: Organization!
  papers: [Paper!]!
  collaborators: [Researcher!]!
  citations: Int!
}

type Paper {
  id: ID!
  title: String!
  abstract: String
  authors: [Researcher!]!
  publishedIn: Venue!
  year: Int!
  citedBy: [Paper!]!
  cites: [Paper!]!
  keywords: [String!]!
}

type Organization {
  id: ID!
  name: String!
  researchers: [Researcher!]!
}

type Venue {
  id: ID!
  name: String!
  papers: [Paper!]!
}

type Query {
  researcher(id: ID!): Researcher
  paper(id: ID!): Paper
  searchPapers(keyword: String!): [Paper!]!
}
```

### Input GraphQL Query

```graphql
{
  researcher(id: "res_001") {
    name
    email
    affiliation {
      name
      researchers(limit: 10) {
        name
      }
    }
    papers(limit: 5) {
      title
      year
      publishedIn {
        name
      }
      citedBy(limit: 3) {
        title
        year
      }
    }
    collaborators(limit: 5) {
      name
      affiliation {
        name
      }
    }
  }
}
```

### Neo4j Cypher Translation

```cypher
MATCH (r:Researcher {id: "res_001"})
MATCH (r)-[:AFFILIATED_WITH]->(org:Organization)
OPTIONAL MATCH (r)-[:AUTHORED]->(paper:Paper)-[:PUBLISHED_IN]->(venue:Venue)
OPTIONAL MATCH (citingPaper:Paper)-[:CITES]->(paper)
OPTIONAL MATCH (r)-[:COLLABORATES_WITH]->(collab:Researcher)-[:AFFILIATED_WITH]->(collabOrg:Organization)

WITH r, org, paper, venue, citingPaper, collab, collabOrg
RETURN r.name, r.email,
       {name: org.name,
        researchers: [(org)-[:HAS_RESEARCHER]->(re:Researcher) | {name: re.name}][0..10]
       } AS affiliation,
       [paper | {
         title: paper.title,
         year: paper.year,
         publishedIn: {name: venue.name},
         citedBy: [(cp:Paper)-[:CITES]->(paper) | {title: cp.title, year: cp.year}][0..3]
       }][0..5] AS papers,
       [collab | {
         name: collab.name,
         affiliation: {name: collabOrg.name}
       }][0..5] AS collaborators
```

### Gremlin Translation

```gremlin
g.V().has("Researcher","id","res_001")
  .project("name","email","affiliation","papers","collaborators")
  .by("name")
  .by("email")
  .by(out("AFFILIATED_WITH").project("name","researchers")
    .by("name")
    .by(in("AFFILIATED_WITH").limit(10).values("name").fold())
    .fold())
  .by(out("AUTHORED").limit(5).project("title","year","publishedIn","citedBy")
    .by("title")
    .by("year")
    .by(out("PUBLISHED_IN").values("name").fold())
    .by(in("CITES").limit(3).project("title","year")
      .by("title")
      .by("year")
      .fold())
    .fold())
  .by(out("COLLABORATES_WITH").limit(5).project("name","affiliation")
    .by("name")
    .by(out("AFFILIATED_WITH").values("name").fold())
    .fold())
```

### Result Mapping

```json
{
  "data": {
    "researcher": {
      "name": "Dr. Jane Smith",
      "email": "jane.smith@university.edu",
      "affiliation": {
        "name": "MIT Computer Science",
        "researchers": [
          {
            "name": "Dr. John Doe"
          },
          {
            "name": "Dr. Alice Johnson"
          }
        ]
      },
      "papers": [
        {
          "title": "Advanced Graph Neural Networks",
          "year": 2023,
          "publishedIn": {
            "name": "NeurIPS 2023"
          },
          "citedBy": [
            {
              "title": "Graph Transformers for Knowledge Graphs",
              "year": 2024
            }
          ]
        }
      ],
      "collaborators": [
        {
          "name": "Dr. Bob Wilson",
          "affiliation": {
            "name": "Stanford AI Lab"
          }
        }
      ]
    }
  }
}
```

---

## Example 4: Corporate Knowledge Graph

Map organizational structure and relationships via GraphQL.

### GraphQL Schema

```graphql
type Company {
  id: ID!
  name: String!
  industry: String!
  employees(limit: Int): [Employee!]!
  departments: [Department!]!
  subsidiaries: [Company!]!
}

type Department {
  id: ID!
  name: String!
  manager: Employee!
  employees: [Employee!]!
  projects: [Project!]!
}

type Employee {
  id: ID!
  name: String!
  email: String!
  department: Department!
  manager: Employee
  directReports(limit: Int): [Employee!]!
  projects: [Project!]!
  skills: [Skill!]!
}

type Project {
  id: ID!
  name: String!
  department: Department!
  teamMembers: [Employee!]!
  status: String!
}

type Skill {
  id: ID!
  name: String!
  employees: [Employee!]!
}

type Query {
  employee(id: ID!): Employee
  department(id: ID!): Department
}
```

### Input GraphQL Query

```graphql
{
  employee(id: "emp_001") {
    name
    email
    department {
      name
      manager {
        name
      }
    }
    directReports(limit: 3) {
      name
      email
      department {
        name
      }
    }
    projects(limit: 5) {
      name
      status
    }
    skills {
      name
    }
  }
}
```

### Neo4j Cypher Translation

```cypher
MATCH (e:Employee {id: "emp_001"})
MATCH (e)-[:WORKS_IN]->(dept:Department)
MATCH (dept)-[:MANAGED_BY]->(deptMgr:Employee)
OPTIONAL MATCH (e)-[:MANAGES]->(report:Employee)-[:WORKS_IN]->(reportDept:Department)
OPTIONAL MATCH (e)-[:WORKS_ON]->(proj:Project)
OPTIONAL MATCH (e)-[:HAS_SKILL]->(skill:Skill)

RETURN e.name, e.email,
       {name: dept.name,
        manager: {name: deptMgr.name}
       } AS department,
       [report | {
         name: report.name,
         email: report.email,
         department: {name: reportDept.name}
       }][0..3] AS directReports,
       [proj | {name: proj.name, status: proj.status}][0..5] AS projects,
       [skill | {name: skill.name}] AS skills
```

### Result Mapping

```json
{
  "data": {
    "employee": {
      "name": "Alice Manager",
      "email": "alice@company.com",
      "department": {
        "name": "Engineering",
        "manager": {
          "name": "Chief Engineer"
        }
      },
      "directReports": [
        {
          "name": "Bob Developer",
          "email": "bob@company.com",
          "department": {
            "name": "Engineering"
          }
        },
        {
          "name": "Carol Analyst",
          "email": "carol@company.com",
          "department": {
            "name": "Data Analytics"
          }
        }
      ],
      "projects": [
        {
          "name": "GraphDB Migration",
          "status": "In Progress"
        },
        {
          "name": "API Enhancement",
          "status": "Planning"
        }
      ],
      "skills": [
        {
          "name": "Neo4j"
        },
        {
          "name": "Team Leadership"
        },
        {
          "name": "GraphQL"
        }
      ]
    }
  }
}
```

---

## Example 5: Movie/Entertainment Knowledge Graph

Map complex relationships in entertainment industry.

### GraphQL Schema

```graphql
type Movie {
  id: ID!
  title: String!
  releaseYear: Int!
  director: Person!
  actors: [Person!]!
  genre: [Genre!]!
  reviews: [Review!]!
  averageRating: Float
}

type Person {
  id: ID!
  name: String!
  birthYear: Int
  nationality: String
  directedMovies: [Movie!]!
  actedInMovies: [Movie!]!
  collaborators: [Person!]!
}

type Genre {
  id: ID!
  name: String!
  movies(limit: Int): [Movie!]!
}

type Review {
  id: ID!
  rating: Int!
  content: String!
  reviewer: Person!
  movie: Movie!
}

type Query {
  movie(id: ID!): Movie
  person(id: ID!): Person
}
```

### Input GraphQL Query

```graphql
{
  movie(id: "movie_inception") {
    title
    releaseYear
    director {
      name
      directedMovies(limit: 3) {
        title
        releaseYear
      }
    }
    actors(limit: 5) {
      name
      actedInMovies(limit: 2) {
        title
      }
      collaborators(limit: 3) {
        name
      }
    }
    genre {
      name
    }
    reviews(limit: 3) {
      rating
      content
      reviewer {
        name
      }
    }
    averageRating
  }
}
```

### Neo4j Cypher Translation

```cypher
MATCH (m:Movie {id: "movie_inception"})
MATCH (m)-[:DIRECTED_BY]->(director:Person)
OPTIONAL MATCH (director)-[:DIRECTED]->(directedMovie:Movie)
OPTIONAL MATCH (m)-[:STARS]->(actor:Person)
OPTIONAL MATCH (actor)-[:ACTED_IN]->(actorMovie:Movie)
OPTIONAL MATCH (actor)-[:COLLABORATED_WITH]->(collaborator:Person)
OPTIONAL MATCH (m)-[:HAS_GENRE]->(genre:Genre)
OPTIONAL MATCH (m)<-[:REVIEWED_BY]-(review:Review)<-[:WROTE]-(reviewer:Person)

RETURN m.title, m.releaseYear,
       {name: director.name,
        directedMovies: [(director)-[:DIRECTED]->(dm:Movie) | {title: dm.title, releaseYear: dm.releaseYear}][0..3]
       } AS director,
       [actor | {
         name: actor.name,
         actedInMovies: [(actor)-[:ACTED_IN]->(am:Movie) | {title: am.title}][0..2],
         collaborators: [(actor)-[:COLLABORATED_WITH]->(c:Person) | {name: c.name}][0..3]
       }][0..5] AS actors,
       [genre | {name: genre.name}] AS genre,
       [review | {rating: review.rating, content: review.content, reviewer: {name: reviewer.name}}][0..3] AS reviews,
       apoc.math.mean([(m)<-[:REVIEWED_BY]-(r:Review) | r.rating]) AS averageRating
```

### Result Mapping

```json
{
  "data": {
    "movie": {
      "title": "Inception",
      "releaseYear": 2010,
      "director": {
        "name": "Christopher Nolan",
        "directedMovies": [
          {
            "title": "The Dark Knight",
            "releaseYear": 2008
          },
          {
            "title": "Interstellar",
            "releaseYear": 2014
          }
        ]
      },
      "actors": [
        {
          "name": "Leonardo DiCaprio",
          "actedInMovies": [
            {
              "title": "Titanic"
            },
            {
              "title": "The Wolf of Wall Street"
            }
          ],
          "collaborators": [
            {
              "name": "Joseph Gordon-Levitt"
            },
            {
              "name": "Marion Cotillard"
            }
          ]
        }
      ],
      "genre": [
        {
          "name": "Sci-Fi"
        },
        {
          "name": "Thriller"
        }
      ],
      "reviews": [
        {
          "rating": 5,
          "content": "Mind-bending masterpiece!",
          "reviewer": {
            "name": "Movie Critic 1"
          }
        }
      ],
      "averageRating": 4.7
    }
  }
}
```

---

## Key Mapping Principles

### 1. Type Mapping
- GraphQL Object Types → Node Labels
- GraphQL Fields → Node Properties
- GraphQL Relationship Fields → Edge Traversals

### 2. Query Translation
- Root query fields → Starting node match
- Nested fields → Relationship traversals
- Arguments → WHERE clauses / filters

### 3. Result Mapping
- Graph results → GraphQL response shape
- Multiple results → Arrays
- Single results → Object values
- Null handling → missing relationships

### 4. Performance Optimization
- Limit nested query depth
- Use pagination cursors
- Cache frequently accessed patterns
- Index filtered properties

---


