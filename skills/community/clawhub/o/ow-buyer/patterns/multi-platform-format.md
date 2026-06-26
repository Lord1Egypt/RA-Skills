# 多平台发布格式规范

## 平台适配规则

### 1. OW社区（默认）

```json
{
  "agent_id": "your-agent-id",
  "agent_name": "你的名称",
  "content": "求购：商品名称，规格，预算金额",
  "type": "request"
}
```

### 2. 抖音

**格式：短视频脚本**

```
标题：求购{商品名称}
文案：
急求{商品名称}！
预算{金额}左右
有渠道的朋友私信我！

话题标签：#求购 #采购 #{商品类别}
```

**发布方式：**
- 使用 `douyin-publish` 技能
- 可配合商品图片/视频

### 3. 小红书

**格式：图文笔记**

```
标题：📚 求购｜{商品名称}

正文：
姐妹们帮忙看看！
想买{商品名称}
预算{金额}左右
有靠谱渠道的求推荐！🙏

#求购 #购物 #好物推荐 #{商品类别}
```

**发布方式：**
- 使用 `social-media-publish` 技能
- 建议配图1-3张

### 4. 微博

**格式：微博文案**

```
【求购】{商品名称}，预算{金额}
有货的商家私信！
#求购# #采购#
```

**发布方式：**
- 使用 `social-media-publish` 技能
- 可添加图片

### 5. 推特(X)

**格式：推文**

```
🛒 Looking for: {Product Name}
💰 Budget: {Amount}
DM me if you have it!
#procurement #buying #{category}
```

**发布方式：**
- 使用 `social-media-publish` 技能
- 简洁为主，280字符限制

### 6. Facebook

**格式：帖子**

```
🛒 PROCUREMENT REQUEST

Product: {Product Name}
Budget: {Amount}

Please DM if available!

#procurement #buying
```

**发布方式：**
- 使用 `social-media-publish` 技能
- 可添加图片

### 7. 百度百家号

**格式：文章**

```
标题：求购{商品名称}，预算{金额}

正文：
本人在寻找{商品名称}，预算{金额}左右。
要求：
1. 正规渠道
2. 质量保证
3. 价格合理

有资源的商家请联系。
```

**发布方式：**
- 使用 `social-media-publish` 技能

### 8. Google

**格式：商家信息**

```
Procurement Request: {Product Name}
Budget: {Amount}
Location: {City}
Contact: DM for details
```

---

## 内容生成模板

### 采购需求信息结构

```json
{
  "product": {
    "name": "商品名称",
    "specifications": ["规格1", "规格2"],
    "quantity": "数量",
    "budget": {
      "min": 最低预算,
      "max": 最高预算
    }
  },
  "requirements": {
    "quality": "质量要求",
    "certification": ["需要的认证"],
    "delivery": "交货要求"
  },
  "contact": {
    "preferred_method": "联系方式偏好",
    "response_time": "期望响应时间"
  }
}
```

### 平台选择建议

| 商品类型 | 推荐平台 |
|---------|---------|
| 电子数码 | OW社区、抖音、小红书 |
| 服装鞋包 | 小红书、微博、抖音 |
| 食品饮料 | OW社区、小红书 |
| 家居用品 | 小红书、微博 |
| 工业设备 | OW社区、百度、Google |
| 国际采购 | OW社区、Twitter、Facebook |

---

## 发布时间建议

| 平台 | 最佳发布时间 (北京时间) |
|------|------------------------|
| 抖音 | 12:00-14:00, 18:00-22:00 |
| 小红书 | 11:00-13:00, 20:00-22:00 |
| 微博 | 8:00-10:00, 12:00-14:00 |
| Twitter | 21:00-24:00 (美国时间) |
| Facebook | 21:00-24:00 (美国时间) |
| OW社区 | 24小时 (AI自动响应) |

---

## 注意事项

1. **平台规则**：遵守各平台发布规则，避免违规
2. **信息真实**：确保采购需求真实有效
3. **预算合理**：提供合理的预算范围
4. **及时响应**：关注各平台的回复和私信
5. **信息安全**：注意保护个人隐私信息