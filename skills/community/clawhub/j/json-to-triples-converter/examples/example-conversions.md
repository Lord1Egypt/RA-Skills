# JSON to Triples Conversion Examples

Complete examples of JSON-to-triples conversions in different domains.

## Example 1: Person and Organization JSON

### Input JSON

```json
{
  "person": {
    "id": "alice_001",
    "name": "Alice Johnson",
    "age": 30,
    "email": "alice@example.com",
    "phone": "+1-555-0001",
    "organization": {
      "id": "org_acme",
      "name": "Acme Corporation",
      "industry": "Technology",
      "founded": "2000"
    },
    "position": "Senior Software Engineer",
    "startDate": "2020-01-15"
  }
}
```

### Generated RDF Triples (Turtle)

```turtle
@prefix ex: <http://example.org/> .
@prefix foaf: <http://xmlns.com/foaf/0.1/> .
@prefix schema: <http://schema.org/> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

ex:person_alice_001 a foaf:Person ;
  foaf:name "Alice Johnson" ;
  foaf:age "30"^^xsd:integer ;
  foaf:mbox <mailto:alice@example.com> ;
  foaf:phone "+1-555-0001" ;
  schema:jobTitle "Senior Software Engineer" ;
  schema:startDate "2020-01-15"^^xsd:date ;
  schema:worksFor ex:organization_acme ;
  foaf:made ex:person_alice_001 .

ex:organization_acme a schema:Organization ;
  foaf:name "Acme Corporation" ;
  schema:industry "Technology" ;
  schema:foundingDate "2000"^^xsd:gYear .
```

### Generated JSON-LD

```json
{
  "@context": {
    "@vocab": "http://schema.org/",
    "foaf": "http://xmlns.com/foaf/0.1/"
  },
  "@graph": [
    {
      "@type": "Person",
      "@id": "http://example.org/person_alice_001",
      "foaf:name": "Alice Johnson",
      "foaf:age": 30,
      "email": "alice@example.com",
      "foaf:phone": "+1-555-0001",
      "jobTitle": "Senior Software Engineer",
      "startDate": "2020-01-15",
      "worksFor": {
        "@id": "http://example.org/organization_acme"
      }
    },
    {
      "@type": "Organization",
      "@id": "http://example.org/organization_acme",
      "name": "Acme Corporation",
      "industry": "Technology",
      "foundingDate": "2000"
    }
  ]
}
```

---

## Example 2: Product Catalog JSON

### Input JSON

```json
{
  "products": [
    {
      "sku": "LAPTOP-001",
      "name": "ProBook 15",
      "price": 999.99,
      "currency": "USD",
      "category": "Electronics",
      "subcategory": "Computers",
      "manufacturer": {
        "id": "mfg_techcorp",
        "name": "TechCorp Inc"
      },
      "specifications": {
        "processor": "Intel i7",
        "ram": "16GB",
        "storage": "512GB SSD"
      },
      "ratings": {
        "average": 4.5,
        "count": 128
      }
    }
  ]
}
```

### Generated N-Triples

```
<http://example.org/product_laptop_001> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://schema.org/Product> .
<http://example.org/product_laptop_001> <http://schema.org/sku> "LAPTOP-001" .
<http://example.org/product_laptop_001> <http://schema.org/name> "ProBook 15" .
<http://example.org/product_laptop_001> <http://schema.org/price> "999.99"^^<http://www.w3.org/2001/XMLSchema#decimal> .
<http://example.org/product_laptop_001> <http://schema.org/priceCurrency> "USD" .
<http://example.org/product_laptop_001> <http://schema.org/category> "Electronics" .
<http://example.org/product_laptop_001> <http://schema.org/manufacturer> <http://example.org/manufacturer_techcorp> .
<http://example.org/product_laptop_001> <http://schema.org/processorType> "Intel i7" .
<http://example.org/product_laptop_001> <http://example.org/ram> "16GB" .
<http://example.org/product_laptop_001> <http://example.org/storage> "512GB SSD" .
<http://example.org/product_laptop_001> <http://schema.org/aggregateRating> <http://example.org/rating_laptop_001> .
<http://example.org/rating_laptop_001> <http://schema.org/ratingValue> "4.5"^^<http://www.w3.org/2001/XMLSchema#decimal> .
<http://example.org/rating_laptop_001> <http://schema.org/reviewCount> "128"^^<http://www.w3.org/2001/XMLSchema#integer> .
<http://example.org/manufacturer_techcorp> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://schema.org/Organization> .
<http://example.org/manufacturer_techcorp> <http://schema.org/name> "TechCorp Inc" .
```

---

## Example 3: Scientific Paper JSON

### Input JSON

```json
{
  "paper": {
    "id": "arxiv_2024_001",
    "title": "Knowledge Graphs and Semantic Web",
    "authors": [
      {
        "name": "Dr. Alice Chen",
        "affiliation": "MIT",
        "orcid": "0000-0001-2345-6789"
      },
      {
        "name": "Dr. Bob Kumar",
        "affiliation": "Stanford",
        "orcid": "0000-0002-3456-7890"
      }
    ],
    "published": "2024-04-09",
    "venue": {
      "name": "ACM Conference on Knowledge Graphs",
      "year": 2024,
      "location": "San Francisco"
    },
    "abstract": "This paper explores...",
    "keywords": ["knowledge graphs", "semantic web", "ontology"],
    "citationCount": 42,
    "doi": "10.1234/example"
  }
}
```

### Generated RDF (Turtle)

```turtle
@prefix ex: <http://example.org/> .
@prefix dblp: <http://dblp.org/> .
@prefix foaf: <http://xmlns.com/foaf/0.1/> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix bibo: <http://purl.org/ontology/bibo/> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

ex:paper_arxiv_2024_001 a bibo:AcademicArticle ;
  dcterms:title "Knowledge Graphs and Semantic Web" ;
  dcterms:creator ex:author_alice_chen, ex:author_bob_kumar ;
  dcterms:issued "2024-04-09"^^xsd:date ;
  dcterms:description "This paper explores..." ;
  bibo:doi "10.1234/example" ;
  ex:citedBy ex:paper_arxiv_2024_001 ;
  ex:citationCount "42"^^xsd:integer ;
  dcterms:issued ex:venue_acm_2024 ;
  ex:hasKeyword "knowledge graphs", "semantic web", "ontology" .

ex:author_alice_chen a foaf:Person ;
  foaf:name "Dr. Alice Chen" ;
  foaf:workplaceHomepage <http://mit.edu> ;
  foaf:givenName "Alice" ;
  foaf:familyName "Chen" .

ex:author_bob_kumar a foaf:Person ;
  foaf:name "Dr. Bob Kumar" ;
  foaf:workplaceHomepage <http://stanford.edu> ;
  foaf:givenName "Bob" ;
  foaf:familyName "Kumar" .

ex:venue_acm_2024 a ex:Conference ;
  foaf:name "ACM Conference on Knowledge Graphs" ;
  ex:year "2024"^^xsd:gYear ;
  foaf:based_near "San Francisco" .
```

---

## Example 4: Social Media Profile JSON

### Input JSON

```json
{
  "user": {
    "id": "user_12345",
    "username": "alice_dev",
    "displayName": "Alice Developer",
    "bio": "Software engineer interested in graphs",
    "profileImage": "https://example.com/alice.jpg",
    "followers": 5000,
    "following": 250,
    "location": {
      "city": "San Francisco",
      "country": "USA"
    },
    "socialLinks": [
      {
        "platform": "GitHub",
        "url": "https://github.com/alice_dev"
      },
      {
        "platform": "LinkedIn",
        "url": "https://linkedin.com/in/alice_dev"
      }
    ],
    "recentPosts": [
      {
        "id": "post_001",
        "content": "Just released my new graph library!",
        "timestamp": "2024-04-09T10:30:00Z",
        "likes": 150,
        "comments": 23
      }
    ]
  }
}
```

### Generated Graph JSON

```json
{
  "nodes": [
    {
      "id": "user_alice_dev",
      "type": "User",
      "properties": {
        "username": "alice_dev",
        "displayName": "Alice Developer",
        "bio": "Software engineer interested in graphs",
        "followers": 5000,
        "following": 250
      }
    },
    {
      "id": "location_sf",
      "type": "Location",
      "properties": {
        "city": "San Francisco",
        "country": "USA"
      }
    },
    {
      "id": "social_github",
      "type": "SocialProfile",
      "properties": {
        "platform": "GitHub",
        "url": "https://github.com/alice_dev"
      }
    },
    {
      "id": "post_001",
      "type": "Post",
      "properties": {
        "content": "Just released my new graph library!",
        "timestamp": "2024-04-09T10:30:00Z",
        "likes": 150,
        "comments": 23
      }
    }
  ],
  "edges": [
    {
      "source": "user_alice_dev",
      "target": "location_sf",
      "type": "located_in"
    },
    {
      "source": "user_alice_dev",
      "target": "social_github",
      "type": "has_social_profile"
    },
    {
      "source": "user_alice_dev",
      "target": "post_001",
      "type": "created"
    }
  ]
}
```

---

## Example 5: Multilingual Content JSON

### Input JSON

```json
{
  "resource": {
    "id": "book_001",
    "titles": {
      "en": "The Art of Graphs",
      "fr": "L'Art des Graphes",
      "es": "El Arte de los Gráficos"
    },
    "descriptions": {
      "en": "A comprehensive guide to graph theory",
      "fr": "Un guide complet de la théorie des graphes",
      "es": "Una guía completa de la teoría de gráficos"
    },
    "author": {
      "name": "John Smith",
      "country": "UK"
    }
  }
}
```

### Generated RDF with Language Tags

```turtle
@prefix ex: <http://example.org/> .
@prefix foaf: <http://xmlns.com/foaf/0.1/> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix dbo: <http://dbpedia.org/ontology/> .

ex:book_001 a dbo:Book ;
  rdfs:label "The Art of Graphs"@en ;
  rdfs:label "L'Art des Graphes"@fr ;
  rdfs:label "El Arte de los Gráficos"@es ;
  rdfs:comment "A comprehensive guide to graph theory"@en ;
  rdfs:comment "Un guide complet de la théorie des graphes"@fr ;
  rdfs:comment "Una guía completa de la teoría de gráficos"@es ;
  dbo:author ex:author_john_smith .

ex:author_john_smith a foaf:Person ;
  foaf:name "John Smith" ;
  foaf:based_near "UK" .
```

---

## Conversion Statistics

| Example | Input Size | Triple Count | Output Formats | Entities |
|---------|-----------|--------------|----------------|----------|
| Person/Org | 250 bytes | 12 triples | Turtle, JSON-LD | 2 |
| Products | 350 bytes | 15 triples | N-Triples | 3 |
| Paper | 600 bytes | 24 triples | Turtle | 5 |
| Social | 500 bytes | 18 triples | Graph JSON | 4 |
| Multilingual | 280 bytes | 8 triples | Turtle | 2 |

---

See [conversion-patterns.md](../references/conversion-patterns.md) for detailed JSON-to-triples conversion design patterns.


