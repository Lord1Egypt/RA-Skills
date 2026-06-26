---
name: mongodb-query
description: "Query MongoDB databases for debugging and troubleshooting. Use when user needs to: (1) List all databases, (2) List collections in a database, (3) Execute MongoDB queries, (4) Check MongoDB connection and health. Automatically handles IP address or Kubernetes service name for connection. REQUIRES: --uri parameter with MongoDB connection string. Accepts parameters like --uri, --list-dbs, --db, --list-collections, --collection, --query, --namespace."
---

# MongoDB Query

Query MongoDB with automatic connection handling (direct IP or Kubernetes port-forward).

## Prerequisites

**Dependencies:**
- Python 3.6+
- `pymongo` package: `pip install pymongo`
- `kubectl` (only needed if connecting to Kubernetes service via port-forward)

**The agent MUST ask user for MongoDB connection information before using this skill.**

Required information:

1. **MongoDB Connection String** (required): Full connection URI including credentials
   - Example: `mongodb://root:password@172.16.79.249:27017/?authSource=admin&replicaSet=rs0`
   - Example for K8s: `mongodb://root:password@mongodb.mongodb.svc.cluster.local:27017/?authSource=admin`

2. **Kubernetes Namespace** (optional): Only needed if the MongoDB address is a Kubernetes service name

**Recommendation**: Save connection info to project's `TOOLS.md` for future reference:

```markdown
### MongoDB

- mongo_conn_str: mongodb://user:pass@host:port/?options
- mongo_namespace: (optional - only if K8s service name)
```

## Connection Mode

The script automatically detects connection type based on the host in connection URI:

| Address Type | Connection Method |
|--------------|-------------------|
| IP address (e.g., `172.16.79.249:27017`) | Direct connection |
| K8s Service (e.g., `mongodb.mongodb.svc.cluster.local:27017`) | kubectl port-forward |

## Usage

```bash
# List all databases
python scripts/query_mongo.py --uri "mongodb://user:pass@host:27017/?authSource=admin" --list-dbs

# List collections in a database
python scripts/query_mongo.py --uri "mongodb://user:pass@host:27017/?authSource=admin" --db <database> --list-collections

# Execute a query
python scripts/query_mongo.py --uri "mongodb://user:pass@host:27017/?authSource=admin" --db <database> --collection <name> --query '{"status": "active"}'

# For K8s service names, specify namespace
python scripts/query_mongo.py --uri "mongodb://user:pass@svc.ns.svc.cluster.local:27017/?authSource=admin" --list-dbs --namespace mongodb
```

## Parameters

| Parameter | Description | Required |
|-----------|-------------|----------|
| `--uri` | MongoDB connection string | **Yes** |
| `--list-dbs` | List all databases | No |
| `--db <name>` | Database name | For collection/query operations |
| `--list-collections` | List all collections in database | No |
| `--collection <name>` | Collection name | For query operations |
| `--query <json>` | MongoDB query in JSON format | No |
| `--namespace <ns>` | Kubernetes namespace (required if host is a K8s service name) | Conditional |
| `--limit <n>` | Limit number of results (default: 10) | No |
| `--json` | Output raw JSON | No |

## Examples

```bash
# List all databases
python scripts/query_mongo.py --uri "mongodb://root:pass@172.16.79.249:27017/?authSource=admin" --list-dbs

# Find active users
python scripts/query_mongo.py --uri "mongodb://root:pass@172.16.79.249:27017/?authSource=admin" --db production --collection users --query '{"status": "active"}'

# Query by ObjectId
python scripts/query_mongo.py --uri "mongodb://root:pass@172.16.79.249:27017/?authSource=admin" --db production --collection users --query '{"_id": {"$oid": "507f1f77bcf86cd799439011"}}'

# Limit results
python scripts/query_mongo.py --uri "mongodb://root:pass@172.16.79.249:27017/?authSource=admin" --db production --collection logs --query '{"level": "ERROR"}' --limit 20

# K8s service mode
python scripts/query_mongo.py --uri "mongodb://root:pass@mongodb.mongodb.svc.cluster.local:27017/?authSource=admin" --db production --collection users --query '{}' --namespace mongodb
```

## Output

- List operations: Returns database/collection names
- Query operations: Returns matching documents in formatted or JSON format
