---
name: mongodb-admin
description: Comprehensive MongoDB administration including connection management, backup/restore operations, performance analysis, index management, user administration, and replica set configuration. Supports both mongosh and legacy mongo shell commands.
---

# MongoDB Admin

Complete MongoDB administration toolkit for database management, performance optimization, backup/restore operations, and replica set management. Covers both local and remote MongoDB instances.

## Prerequisites

- MongoDB installed (server and/or client tools)
- `mongosh` (MongoDB Shell) or legacy `mongo` client
- `mongodump` and `mongorestore` utilities
- Appropriate database permissions
- Network access to target MongoDB instance

## Usage

### Connection Management

**Basic connection:**
```bash
# Local instance
mongosh

# Remote instance
mongosh "mongodb://localhost:27017/mydb"
mongosh "mongodb://user:pass@host:27017/mydb"

# With authentication
mongosh --host localhost --port 27017 --username admin --password --authenticationDatabase admin

# SSL/TLS connection
mongosh "mongodb://host:27017/mydb?ssl=true"
```

**Connection string examples:**
```bash
# Local development
mongosh "mongodb://localhost:27017/clawd_memory_db"

# Remote with auth
mongosh "mongodb://dbuser:password@10.0.0.100:27017/production_db?authSource=admin"

# Replica set
mongosh "mongodb://node1:27017,node2:27017,node3:27017/mydb?replicaSet=rs0"

# MongoDB Atlas
mongosh "mongodb+srv://username:password@cluster0.abcde.mongodb.net/mydb"
```

### Database Operations

**Database management:**
```javascript
// List databases
show dbs

// Switch to database
use mydb

// Drop database
db.dropDatabase()

// Database stats
db.stats()
db.runCommand({dbStats: 1, scale: 1024*1024}) // MB scale
```

**Collection operations:**
```javascript
// List collections
show collections

// Create collection
db.createCollection("users")
db.createCollection("logs", {capped: true, size: 10000000, max: 1000})

// Drop collection
db.users.drop()

// Collection stats
db.users.stats()
```

### Backup and Restore

**Using mongodump/mongorestore:**

```bash
# Backup entire database
mongodump --host localhost:27017 --db mydb --out /backup/$(date +%Y%m%d)

# Backup with authentication
mongodump --host localhost:27017 --username admin --password --authenticationDatabase admin --db mydb --out /backup/

# Backup specific collection
mongodump --host localhost:27017 --db mydb --collection users --out /backup/

# Compressed backup
mongodump --host localhost:27017 --db mydb --gzip --out /backup/

# Restore database
mongorestore --host localhost:27017 --db mydb /backup/mydb

# Restore with different name
mongorestore --host localhost:27017 --db newdb /backup/mydb

# Restore specific collection
mongorestore --host localhost:27017 --db mydb --collection users /backup/mydb/users.bson
```

**Automated backup script:**
```bash
#!/bin/bash
# mongodb-backup.sh

DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/var/backups/mongodb"
DB_NAME="clawd_memory_db"

echo "Starting MongoDB backup: $DATE"

# Create backup directory
mkdir -p $BACKUP_DIR/$DATE

# Perform backup
mongodump --host localhost:27017 --db $DB_NAME --gzip --out $BACKUP_DIR/$DATE

# Check if backup successful
if [ $? -eq 0 ]; then
    echo "✅ Backup completed: $BACKUP_DIR/$DATE"
    
    # Create symlink to latest
    ln -sfn $BACKUP_DIR/$DATE $BACKUP_DIR/latest
    
    # Cleanup old backups (keep 7 days)
    find $BACKUP_DIR -type d -name "2*" -mtime +7 -exec rm -rf {} \;
else
    echo "❌ Backup failed!"
    exit 1
fi
```

### Performance Analysis

**Query performance:**
```javascript
// Enable profiling
db.setProfilingLevel(2) // profile all operations
db.setProfilingLevel(1, {slowms: 100}) // profile slow queries only

// View slow queries
db.system.profile.find().limit(5).sort({ts: -1}).pretty()

// Find slow queries
db.system.profile.find({millis: {$gt: 100}}).sort({ts: -1}).pretty()

// Disable profiling
db.setProfilingLevel(0)
```

**Server status and metrics:**
```javascript
// Server status
db.serverStatus()

// Current operations
db.currentOp()

// Kill long-running operation
db.killOp(opid)

// Database statistics
db.stats()

// Collection statistics
db.users.stats()
```

**Connection monitoring:**
```javascript
// Current connections
db.serverStatus().connections

// Active connections
db.runCommand({connPoolStats: 1})

// List current sessions
db.aggregate([{$listSessions: {}}])
```

### Index Management

**Creating indexes:**
```javascript
// Single field index
db.users.createIndex({email: 1})

// Compound index
db.users.createIndex({email: 1, createdAt: -1})

// Text search index
db.articles.createIndex({title: "text", content: "text"})

// Partial index
db.users.createIndex({email: 1}, {partialFilterExpression: {active: true}})

// TTL index (auto-expire documents)
db.sessions.createIndex({expireAt: 1}, {expireAfterSeconds: 0})

// Background index creation
db.users.createIndex({email: 1}, {background: true})
```

**Index analysis:**
```javascript
// List indexes
db.users.getIndexes()

// Index usage statistics
db.users.aggregate([{$indexStats: {}}])

// Explain query execution
db.users.find({email: "test@example.com"}).explain("executionStats")

// Drop index
db.users.dropIndex({email: 1})
db.users.dropIndex("email_1")
```

### User Management

**Database users:**
```javascript
// Create admin user
db.createUser({
  user: "admin",
  pwd: "securepassword",
  roles: [{role: "userAdminAnyDatabase", db: "admin"}]
})

// Create database-specific user
db.createUser({
  user: "appuser",
  pwd: "apppassword",
  roles: [
    {role: "readWrite", db: "mydb"},
    {role: "read", db: "analytics"}
  ]
})

// Update user
db.updateUser("appuser", {
  roles: [{role: "dbOwner", db: "mydb"}]
})

// Change password
db.changeUserPassword("appuser", "newpassword")

// List users
db.getUsers()

// Drop user
db.dropUser("appuser")
```

**Custom roles:**
```javascript
// Create custom role
db.createRole({
  role: "dataAnalyst",
  privileges: [
    {resource: {db: "analytics", collection: ""}, actions: ["find", "listIndexes"]},
    {resource: {db: "logs", collection: ""}, actions: ["find"]}
  ],
  roles: []
})

// Grant role to user
db.grantRolesToUser("analyst", ["dataAnalyst"])
```

### Replica Set Management

**Initialize replica set:**
```javascript
// Initialize replica set
rs.initiate({
  _id: "rs0",
  members: [
    {_id: 0, host: "mongo1:27017"},
    {_id: 1, host: "mongo2:27017"},
    {_id: 2, host: "mongo3:27017"}
  ]
})
```

**Replica set operations:**
```javascript
// Check replica set status
rs.status()

// Check configuration
rs.conf()

// Add member
rs.add("mongo4:27017")

// Remove member
rs.remove("mongo4:27017")

// Step down primary
rs.stepDown()

// Force reconfiguration
rs.reconfig(config, {force: true})
```

### Data Import/Export

**JSON import/export:**
```bash
# Export collection to JSON
mongoexport --host localhost:27017 --db mydb --collection users --out users.json

# Export with query
mongoexport --host localhost:27017 --db mydb --collection users --query '{"active": true}' --out active_users.json

# Import JSON
mongoimport --host localhost:27017 --db mydb --collection users --file users.json

# Import CSV
mongoimport --host localhost:27017 --db mydb --collection users --type csv --headerline --file users.csv
```

### Maintenance Tasks

**Database maintenance:**
```javascript
// Compact collection
db.users.compact()

// Repair database
db.repairDatabase()

// Validate collection
db.users.validate()

// Re-index collection
db.users.reIndex()
```

**Cleanup operations:**
```bash
# Clean up orphaned data
mongosh --eval "db.runCommand({cleanupOrphaned: 'mydb.users'})"

# Compact all collections
mongosh mydb --eval "db.runCommand({compact: 'users', force: true})"
```

### Monitoring Scripts

**Health check script:**
```bash
#!/bin/bash
# mongodb-health.sh

echo "MongoDB Health Check - $(date)"
echo "=================================="

# Check if MongoDB is running
if ! pgrep mongod > /dev/null; then
    echo "❌ MongoDB is not running"
    exit 1
fi

# Check connection
mongosh --eval "db.adminCommand('ping')" > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "✅ MongoDB connection: OK"
else
    echo "❌ MongoDB connection: FAILED"
    exit 1
fi

# Check disk space
DISK_USAGE=$(df -h /var/lib/mongodb | tail -1 | awk '{print $5}' | sed 's/%//')
if [ $DISK_USAGE -gt 80 ]; then
    echo "⚠️ Disk usage: ${DISK_USAGE}% (High)"
else
    echo "✅ Disk usage: ${DISK_USAGE}%"
fi

# Check memory usage
MEMORY_USAGE=$(mongosh --quiet --eval "JSON.stringify(db.serverStatus().mem)" | jq '.resident')
echo "📊 Memory usage: ${MEMORY_USAGE}MB"

# Check active connections
CONNECTIONS=$(mongosh --quiet --eval "db.serverStatus().connections.current")
echo "🔌 Active connections: $CONNECTIONS"

echo "Health check completed."
```

This skill provides comprehensive MongoDB administration capabilities for both development and production environments.