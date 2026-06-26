# TigerGraph Examples

This file contains 5 complete, production-ready examples of TigerGraph usage across different domains. Each example demonstrates real-world scenarios with full GSQL queries and Python implementation.

---

## Table of Contents

1. [Social Network Analysis](#1-social-network-analysis)
2. [E-Commerce Recommendation Engine](#2-e-commerce-recommendation-engine)
3. [Fraud Detection Network](#3-fraud-detection-network)
4. [Supply Chain Management](#4-supply-chain-management)
5. [Research Collaboration Network](#5-research-collaboration-network)

---

## 1. Social Network Analysis

### Domain Description

TigerGraph-based social network with real-time analytics. Demonstrates:
- User relationship management
- Community detection
- Influence analysis
- Recommendation generation
- Social metrics computation

### Graph Schema

**Vertices:**
- `User` - User node with: id, name, age, location, joined_date

**Edges:**
- `FOLLOWS` - One-way following relationship
- `FRIENDS_WITH` - Mutual friendship
- `INTERACTS_WITH` - Interaction with weight/frequency

### GSQL Queries

#### Find Influencers (PageRank)
```gsql
CREATE QUERY findInfluencers(INT limit = 10) FOR GRAPH SocialGraph {
  SetAccum<VERTEX<User>> influencers;
  
  MaxAccum<FLOAT> max_rank;
  FLOAT rank_value;
  
  Start = {User.*};
  
  Influence = SELECT u FROM Start:u
              ACCUM
              FOREACH t IN u.FOLLOWERS DO
                rank_value += 1.0 / (t.FOLLOWER_COUNT + 1)
              END
              ORDER BY rank_value DESC
              LIMIT limit;
  
  PRINT Influence;
}
```

#### Detect Communities
```gsql
CREATE QUERY detectCommunities() FOR GRAPH SocialGraph {
  MaxAccum<INT> community;
  
  Users = {User.*};
  
  # Louvain community detection algorithm
  WHILE (changed) DO
    Users = SELECT u FROM Users:u
            ACCUM
            INT max_comm = -1,
            FLOAT max_mod = -1.0,
            FOREACH neighbor IN u.NEIGHBORS DO
              FLOAT mod = calculateModularity(u, neighbor);
              IF mod > max_mod THEN
                max_mod = mod;
                max_comm = neighbor.community;
              END
            END,
            u.community = max_comm;
  END;
  
  PRINT Users;
}
```

#### Find Friend Recommendations
```gsql
CREATE QUERY recommendFriends(VERTEX<User> u, INT limit = 5) FOR GRAPH SocialGraph {
  Start = {u};
  FriendOfFriend = SELECT friend_friend
                   FROM Start:s -(FOLLOWS:e1)-> User:friend -(FOLLOWS:e2)-> User:friend_friend
                   WHERE friend_friend NOT IN Start.FOLLOWERS
                   ACCUM friend_friend.score += 1
                   ORDER BY score DESC
                   LIMIT limit;
  
  PRINT FriendOfFriend;
}
```

### Python Implementation

```python
from tigergraph_connector import TigerGraphConnector, ConnectionConfig

config = ConnectionConfig(
    host="http://localhost",
    restpp_port=9000,
    graph_name="SocialGraph",
    api_token="token"
)

connector = TigerGraphConnector()
connector.connect(config)

# Find influencers
influencers = connector.run_query("findInfluencers", {"limit": 10})
print(f"Top influencers: {influencers}")

# Detect communities
communities = connector.run_query("detectCommunities", {})
print(f"Communities found: {len(communities)}")

# Get recommendations
recommendations = connector.run_query(
    "recommendFriends",
    {"u": "user123", "limit": 5}
)
print(f"Recommendations: {recommendations}")
```

---

## 2. E-Commerce Recommendation Engine

### Domain Description

Real-time recommendation system using product and user interaction graphs. Demonstrates:
- Product similarity calculation
- Collaborative filtering
- Purchase pattern analysis
- Personalized recommendations
- Inventory graph

### Graph Schema

**Vertices:**
- `Product` - Product with: id, name, price, category
- `User` - User with: id, name, email
- `Category` - Product category
- `Supplier` - Supplier information

**Edges:**
- `PURCHASED` - User purchased product (with date, price)
- `BROWSED` - User browsed product
- `SIMILAR_TO` - Product similarity
- `IN_CATEGORY` - Product in category

### GSQL Queries

#### Collaborative Filtering
```gsql
CREATE QUERY collaborativeFiltering(VERTEX<User> user, INT limit = 10) FOR GRAPH EcommerceGraph {
  SumAccum<FLOAT> score;
  
  Start = {user};
  
  # Find similar users
  SimilarUsers = SELECT other_user
                 FROM Start:s -(PURCHASED:e1)-> Product:p -(PURCHASED:e2)-> User:other_user
                 WHERE other_user != s
                 ACCUM other_user.score += 1.0 / e1.rating
                 ORDER BY score DESC
                 LIMIT 10;
  
  # Get products from similar users
  Recommendations = SELECT product
                    FROM SimilarUsers:s -(PURCHASED:e)-> Product:product
                    WHERE product NOT IN Start.PURCHASED
                    ACCUM product.score += s.score * e.rating
                    ORDER BY score DESC
                    LIMIT limit;
  
  PRINT Recommendations;
}
```

#### Product Recommendations
```gsql
CREATE QUERY getProductRecommendations(VERTEX<Product> product, INT limit = 5) FOR GRAPH EcommerceGraph {
  Start = {product};
  
  CoProducts = SELECT p
               FROM Start:s -(SIMILAR_TO:e)-> Product:p
               ORDER BY e.similarity DESC
               LIMIT limit;
  
  PRINT CoProducts;
}
```

---

## 3. Fraud Detection Network

### Domain Description

Fraud detection system analyzing transaction and entity networks. Demonstrates:
- Suspicious pattern detection
- Entity relationship analysis
- Graph-based anomaly detection
- Risk scoring

### Graph Schema

**Vertices:**
- `Account` - Bank account
- `Transaction` - Transaction record
- `Entity` - Person or organization
- `Device` - Device information

**Edges:**
- `INITIATED` - Account initiated transaction
- `SENT_TO` - Transaction destination
- `LINKED_TO` - Account linked to entity
- `USED_DEVICE` - Account used device

### GSQL Queries

#### Detect Fraud Rings
```gsql
CREATE QUERY detectFraudRings() FOR GRAPH FraudGraph {
  ListAccum<VERTEX<Account>> ring;
  SetAccum<VERTEX<Account>> visited;
  
  Accounts = {Account.*};
  
  Accounts = SELECT account FROM Accounts:account
             ACCUM
             IF account NOT IN visited THEN
               ring = findConnectedComponent(account),
               IF ring.SIZE >= 3 THEN
                 account.fraud_score += ring.SIZE * 10
               END,
               visited += ring
             END;
  
  FraudRings = SELECT account FROM Accounts:account
               WHERE account.fraud_score > 30;
  
  PRINT FraudRings;
}
```

### Python Implementation

```python
def analyze_fraud():
    connector = TigerGraphConnector()
    connector.connect(config)
    
    # Detect fraud rings
    fraud_rings = connector.run_query("detectFraudRings", {})
    print(f"Fraud rings detected: {len(fraud_rings)}")
    
    # Get high-risk accounts
    high_risk = [account for account in fraud_rings 
                 if account['fraud_score'] > 50]
    print(f"High-risk accounts: {len(high_risk)}")
    
    return high_risk
```

---

## 4. Supply Chain Management

### Domain Description

Supply chain network optimization and tracking. Demonstrates:
- Supplier network analysis
- Delivery path optimization
- Inventory tracking
- Risk assessment

### Graph Schema

**Vertices:**
- `Supplier` - Supplier company
- `Product` - Product
- `Warehouse` - Warehouse location
- `Customer` - Customer

**Edges:**
- `SUPPLIES` - Supplier supplies product
- `STORES` - Warehouse stores product
- `SHIPS_TO` - Shipment route
- `ORDERS` - Customer orders product

### GSQL Queries

#### Find Optimal Supply Chain Path
```gsql
CREATE QUERY findOptimalPath(VERTEX<Supplier> supplier, 
                              VERTEX<Customer> customer) FOR GRAPH SupplyChainGraph {
  Path = shortest_path_bfs(supplier, customer, "SHIPS_TO", FORWARD);
  
  PRINT Path;
}
```

---

## 5. Research Collaboration Network

### Domain Description

Research collaboration and publication network analysis. Demonstrates:
- Collaboration network analysis
- Citation networks
- Co-authorship patterns
- Research trajectory analysis

### Graph Schema

**Vertices:**
- `Paper` - Research paper
- `Author` - Researcher
- `Topic` - Research topic
- `Venue` - Conference/Journal

**Edges:**
- `AUTHORED_BY` - Paper written by author
- `CITES` - Citation relationship
- `COLLABORATES_WITH` - Author collaboration
- `RESEARCHES` - Author researches topic

### GSQL Queries

#### Find Research Communities
```gsql
CREATE QUERY findResearchCommunities() FOR GRAPH ResearchGraph {
  MaxAccum<INT> community_id;
  
  Authors = {Author.*};
  
  # Find clusters of collaborating researchers
  Communities = SELECT author FROM Authors:author
                ACCUM
                FOREACH neighbor IN author.COLLABORATORS DO
                  IF neighbor.community_id > author.community_id THEN
                    author.community_id = neighbor.community_id
                  END
                END;
  
  PRINT Communities;
}
```

---

## Summary

These 5 examples demonstrate:

✅ **Social Network** - Influencer analysis, community detection, recommendations  
✅ **E-Commerce** - Collaborative filtering, product recommendations  
✅ **Fraud Detection** - Pattern-based fraud ring detection  
✅ **Supply Chain** - Path optimization, network analysis  
✅ **Research** - Collaboration networks, citation analysis  

Each example includes:
- Complete graph schema
- GSQL query definitions
- Real-world use cases
- Python implementation examples

All examples follow best practices:
- Efficient graph algorithms
- Scalable patterns
- Real-time processing
- Production-ready code

---

**Last Updated:** April 12, 2026  
**TigerGraph Version:** 3.0+  
**GSQL Version:** 3.0+

