---
name: mongodb-skill
description: MongoDB 文档数据库管理技能。通过自然语言查询、管理 MongoDB，支持文档查询、聚合操作、索引管理、地理空间查询等功能。当用户提到 MongoDB、NoSQL、文档数据库时使用此技能。
---

# MongoDB Skill - 灵活的文档数据库管理

通过自然语言，轻松管理 MongoDB，利用其强大的文档操作能力！

---

## 🎯 功能特点

### 核心能力
- **🔍 灵活查询** - 自然语言描述，自动生成查询语句
- **📊 聚合分析** - 复杂的数据聚合和统计分析
- **📑 文档操作** - 嵌套文档、数组操作
- **🌍 地理查询** - 地理空间查询和距离计算
- **📈 索引管理** - 复合索引、文本索引、地理索引
- **💾 备份恢复** - mongodump/mongrestore 完整方案

---

## 📋 使用场景

### 查询场景
- "查询年龄大于 25 岁的用户"
- "查找包含特定标签的文章"
- "按字段分组统计"

### 聚合分析场景
- "统计每个分类的文章数量"
- "计算用户的平均订单金额"
- "时间序列数据分析"

### 文档操作场景
- "向用户文档中添加一个 address 字段"
- "更新数组中的元素"
- "删除嵌套字段"

### 地理查询场景
- "查询距离我 5 公里内的商家"
- "查找特定区域内的地点"

---

## 🔧 前置条件

### 1. 安装 MongoDB 客户端

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install mongodb-clients
```

**macOS:**
```bash
brew install mongodb-community-shell
```

**Python 客户端（推荐）:**
```bash
pip install pymongo
```

### 2. 连接 MongoDB

**使用 mongosh:**
```bash
mongosh "mongodb://localhost:27017/your_database"
```

**使用连接字符串：**
```
mongodb://username:password@localhost:27017/database
```

---

## 💻 常用操作

### 基础查询

```javascript
// 查询年龄大于 25 的用户
db.users.find({ age: { $gt: 25 } })

// 模糊查询（正则表达式）
db.articles.find({ title: { $regex: /人工智能/i } })

// 数组字段查询（包含特定值）
db.products.find({ tags: "electronics" })

// 多条件查询
db.users.find({
  age: { $gte: 18, $lte: 35 },
  status: "active"
})

// 指定返回字段
db.users.find(
  { age: { $gt: 25 } },
  { name: 1, email: 1, _id: 0 }
)
```

### 聚合操作

```javascript
// 统计每个分类的文章数量
db.articles.aggregate([
  { $group: { 
      _id: "$category", 
      count: { $sum: 1 } 
    } 
  },
  { $sort: { count: -1 } }
])

// 计算用户的平均订单金额
db.orders.aggregate([
  { $match: { status: "completed" } },
  { $group: { 
      _id: "$user_id", 
      total_spent: { $sum: "$amount" },
      order_count: { $sum: 1 }
    } 
  },
  { $addFields: {
      avg_order: { $divide: ["$total_spent", "$order_count"] }
    }
  },
  { $sort: { total_spent: -1 } }
])

// 时间序列分析（按天统计）
db.orders.aggregate([
  {
    $group: {
      _id: {
        $dateToString: {
          format: "%Y-%m-%d",
          date: "$created_at"
        }
      },
      total_amount: { $sum: "$amount" },
      count: { $sum: 1 }
    }
  },
  { $sort: { _id: 1 } }
])

// 复杂聚合（多表 JOIN）
db.orders.aggregate([
  {
    $lookup: {
      from: "users",
      localField: "user_id",
      foreignField: "_id",
      as: "user_info"
    }
  },
  { $unwind: "$user_info" },
  {
    $project: {
      order_id: "$_id",
      amount: 1,
      user_name: "$user_info.name",
      user_email: "$user_info.email"
    }
  }
])
```

### 文档更新

```javascript
// 更新单个文档
db.users.updateOne(
  { _id: ObjectId("123") },
  { $set: { last_login: new Date() } }
)

// 批量更新
db.users.updateMany(
  { status: "inactive" },
  { $set: { archived: true } }
)

// 添加字段
db.users.updateMany(
  {},
  { $set: { created_at: new Date() } }
)

// 数组操作（添加元素）
db.products.updateOne(
  { _id: ObjectId("123") },
  { $push: { tags: "new_tag" } }
)

// 数组操作（删除元素）
db.products.updateOne(
  { _id: ObjectId("123") },
  { $pull: { tags: "old_tag" } }
)

// 嵌套文档更新
db.users.updateOne(
  { _id: ObjectId("123") },
  { $set: { "profile.address": "新地址" } }
)

// 数组元素更新
db.orders.updateOne(
  { _id: ObjectId("123"), "items.product_id": ObjectId("456") },
  { $set: { "items.$.quantity": 10 } }
)
```

### 数组操作

```javascript
// 查询数组包含特定值
db.posts.find({ tags: "javascript" })

// 查询数组包含多个值中的任意一个
db.posts.find({ tags: { $in: ["javascript", "python"] } })

// 查询数组包含所有指定值
db.posts.find({ tags: { $all: ["javascript", "mongodb"] } })

// 查询数组长度
db.posts.find({ tags: { $size: 3 } })

// 查询数组的第 N 个元素
db.posts.find({ "tags.0": "javascript" })
```

### 地理空间查询

```javascript
// 创建地理索引
db.places.createIndex({ location: "2dsphere" })

// 查询距离某点 5 公里内的地点
db.places.find({
  location: {
    $near: {
      $geometry: {
        type: "Point",
        coordinates: [116.4074, 39.9042]  // [经度, 纬度]
      },
      $maxDistance: 5000  // 5 公里
    }
  }
})

// 计算距离
db.places.aggregate([
  {
    $geoNear: {
      near: {
        type: "Point",
        coordinates: [116.4074, 39.9042]
      },
      distanceField: "distance",
      maxDistance: 5000,
      spherical: true
    }
  }
])

// 查询特定区域内的地点
db.places.find({
  location: {
    $geoWithin: {
      $polygon: [
        [116.3, 39.9],
        [116.5, 39.9],
        [116.5, 40.0],
        [116.3, 40.0]
      ]
    }
  }
})
```

### 索引管理

```javascript
// 创建单字段索引
db.users.createIndex({ email: 1 })

// 创建复合索引
db.orders.createIndex({ user_id: 1, created_at: -1 })

// 创建唯一索引
db.users.createIndex({ username: 1 }, { unique: true })

// 创建文本索引（全文搜索）
db.articles.createIndex({ title: "text", content: "text" })

// 全文搜索
db.articles.find(
  { $text: { $search: "人工智能" } },
  { score: { $meta: "textScore" } }
).sort({ score: { $meta: "textScore" } })

// 查看索引
db.users.getIndexes()

// 删除索引
db.users.dropIndex("email_1")
```

---

## 💾 备份恢复

### 备份

**完整备份：**
```bash
mongodump --uri="mongodb://localhost:27017/your_database" \
  --out=backup_$(date +%Y%m%d)
```

**仅备份单个集合：**
```bash
mongodump --uri="mongodb://localhost:27017/your_database" \
  --collection=users --out=backup_users
```

**使用查询条件备份：**
```bash
mongodump --uri="mongodb://localhost:27017/your_database" \
  --query='{ "status": "active" }' --out=backup_active
```

### 恢复

**恢复完整备份：**
```bash
mongorestore --uri="mongodb://localhost:27017/your_database" backup_20260323
```

**恢复单个集合：**
```bash
mongorestore --uri="mongodb://localhost:27017/your_database" \
  backup_20260323/your_database/users.bson
```

---

## 🔍 高级功能

### 文档建模

**嵌入模式：**
```javascript
// 适合 1:N 关系，N 较小
{
  _id: ObjectId("..."),
  title: "文章标题",
  comments: [
    { user_id: ObjectId("..."), content: "评论内容", created_at: Date }
  ]
}
```

**引用模式：**
```javascript
// 适合 N:N 关系或 N 较大
{
  _id: ObjectId("..."),
  title: "文章标题",
  comment_ids: [ObjectId("..."), ObjectId("...")]
}
```

### 事务操作

```javascript
// 使用事务处理多集合操作
session = db.getMongo().startSession()
session.startTransaction()

try {
  db.users.updateOne(
    { _id: user_id },
    { $inc: { balance: -100 } },
    { session }
  )
  
  db.orders.insertOne(
    { user_id, amount: 100, created_at: new Date() },
    { session }
  )
  
  session.commitTransaction()
} catch (error) {
  session.abortTransaction()
  throw error
}
```

### 更改流（Change Streams）

```javascript
// 监听集合的变更
changeStream = db.users.watch()

changeStream.on('change', (next) => {
  console.log(next)
  // 根据 next.operationType 处理不同事件
})
```

---

## ⚡ 性能优化

### 查询优化
1. **创建合适的索引** - 为查询字段创建索引
2. **使用投影** - 只返回需要的字段
3. **限制结果数量** - 使用 `.limit()`
4. **避免 `$where` 查询** - 使用 MongoDB 操作符

### 索引策略
1. **ESR 原则** - Equality, Sort, Range
2. **复合索引顺序** - 查询条件顺序应与索引一致
3. **避免全表扫描** - 为大集合创建索引
4. **定期索引维护** - 使用 `reIndex()`

---

## 🎓 示例对话

### 示例 1：复杂聚合查询
**用户：** "统计每个用户最近的订单金额"

**AI：** "使用聚合管道查询每个用户的订单统计"
```javascript
db.orders.aggregate([
  { $match: { status: "completed" } },
  {
    $group: {
      _id: "$user_id",
      last_order_date: { $max: "$created_at" },
      total_amount: { $sum: "$amount" },
      order_count: { $sum: 1 }
    }
  },
  { $sort: { total_amount: -1 } }
])
```

### 示例 2：地理查询
**用户：** "查询距离天安门 5 公里内的餐厅"

**AI：** "使用地理空间索引查询附近地点"
```javascript
db.places.find({
  type: "restaurant",
  location: {
    $near: {
      $geometry: {
        type: "Point",
        coordinates: [116.3974, 39.9093]  // 天安门坐标
      },
      $maxDistance: 5000
    }
  }
})
```

### 示例 3：文档更新
**用户：** "给所有订单添加一个 processed 字段"

**AI：** "批量更新订单文档"
```javascript
db.orders.updateMany(
  { processed: { $exists: false } },
  { $set: { processed: false } }
)
```

---

## ⚠️ 注意事项

### 数据建模建议
1. **嵌入 vs 引用** - 根据访问频率选择
2. **数组大小限制** - 避免无限增长的数组
3. **文档大小限制** - 单文档最大 16MB
4. **规范化设计** - 重复数据 vs 查询性能

### 安全建议
1. **启用认证** - 配置用户名密码
2. **网络隔离** - 不要暴露到公网
3. **最小权限** - 使用角色基础访问控制
4. **敏感数据加密** - 存储前加密

---

## 📚 参考资料

- [MongoDB 官方文档](https://www.mongodb.com/docs/)
- [MongoDB 查询操作符](https://www.mongodb.com/docs/manual/reference/operator/)
- [MongoDB 聚合管道](https://www.mongodb.com/docs/manual/core/aggregation-pipeline/)

---

**开始使用：** 告诉我你的 MongoDB 操作需求，我会帮你生成相应的查询！🚀
