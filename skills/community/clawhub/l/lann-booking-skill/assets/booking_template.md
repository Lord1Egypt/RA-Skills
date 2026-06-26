# 预约确认消息模板

## 成功预约模板

```markdown
✅ 预约成功！

📋 预约详情
━━━━━━━━━━━━━━━━━━━━━━━
• 预约 ID：{bookingId}
• 门店：{storeName}
• 地址：{storeAddress}
• 电话：{storeTelephone}
• 服务：{serviceName}
• 时间：{startTime} - {endTime}
• 人数：{count} 人

🚇 交通指引
━━━━━━━━━━━━━━━━━━━━━━━
{trafficInfo}

💡 温馨提示
━━━━━━━━━━━━━━━━━━━━━━━
• 请提前 10 分钟到店
• 如需取消或改期，请至少提前 1 小时联系门店
• 祝您享受愉快的按摩体验！✨
```

**变量说明**：
- `{bookingId}`: 预约唯一标识符
- `{storeName}`: 门店名称
- `{storeAddress}`: 门店地址
- `{storeTelephone}`: 门店电话
- `{serviceName}`: 服务名称
- `{startTime}`: 预约开始时间（格式化后）
- `{endTime}`: 预约结束时间（格式化后）
- `{count}`: 预约人数
- `{trafficInfo}`: 交通指引

---

## 失败预约模板

### 参数校验失败

```markdown
❌ 预约失败

⚠️ 错误原因：{errorMessage}

📝 请检查以下信息：
• 手机号：请输入正确的 11 位中国大陆手机号
• 门店名称：请使用完整的门店名称
• 服务名称：请使用完整的服务项目名称
• 人数范围：1-20 人
• 预约时间：必须晚于当前时间，使用 ISO 8601 格式

💡 需要帮助？可以问我"有哪些门店"或"有哪些服务"
```

### 门店不存在

```markdown
❌ 未找到匹配的门店

🏪 您输入的门店："{userInput}"

📍 可用的门店列表：
{storeList}

💡 提示：请提供完整的门店名称，或告诉我您所在的城市/区域
```

### 服务不存在

```markdown
❌ 未找到匹配的服务项目

💆 您输入的服务："{userInput}"

📋 可用的服务列表：
{serviceList}

💡 提示：请提供完整的服务名称，或描述您的需求（如"缓解肩颈疲劳"）
```

### 时间冲突

```markdown
❌ 该时段已被预约

🕐 冲突时间：{requestedTime}
🏪 门店：{storeName}

💡 建议：
• 选择其他时间段
• 尝试相邻的门店
• 联系门店咨询可用时间：{storeTelephone}
```

### 服务器错误

```markdown
❌ 预约服务暂时不可用

⚠️ 错误信息：{errorMessage}

🔄 请稍后重试，或直接联系门店：
• 门店：{storeName}
• 电话：{storeTelephone}

💡 提示：如遇网络问题，请检查您的网络连接
```

---

## 信息确认模板

在提交预约前，向用户确认所有信息：

```markdown
📝 请确认预约信息

━━━━━━━━━━━━━━━━━━━━━━━
👤 手机号：{mobileMasked}
🏪 门店：{storeName}
   地址：{storeAddress}
💆 服务：{serviceName}
   时长：{serviceDuration}
👥 人数：{count} 人
🕐 时间：{formattedTime}
━━━━━━━━━━━━━━━━━━━━━━━

✅ 确认无误，提交预约
✏️ 修改信息
❌ 取消预约

请回复"确认"或"提交"以完成预约
```

**变量说明**：
- `{mobileMasked}`: 脱敏后的手机号（如：138****5678）
- `{serviceDuration}`: 服务时长（从服务名称中提取或计算）
- `{formattedTime}`: 友好格式的时间（如：2024年1月15日 14:00）

---

## 查询结果模板

### 门店列表

```markdown
🏪 蘭泰式按摩门店列表

{cityFilter}共找到 {count} 家门店：

{storeItems}

💡 提示：告诉我您想预约的门店名称，或询问具体门店的详细信息
```

**单个门店项格式**：
```
{n}. {storeName}
   📍 {address}
   📞 {telephone}
   🚇 {trafficHint}
```

### 服务列表

```markdown
💆 蘭泰式按摩服务项目

{categoryFilter}共找到 {count} 项服务：

{serviceItems}

💡 提示：告诉我您想预约的服务名称，或描述您的需求
```

**单个服务项格式**：
```
{n}. {serviceName}
   📝 {description}
```

---

## 推荐模板

### 根据需求推荐服务

```markdown
💡 根据您的"{userNeed}"需求，推荐以下服务：

{recommendedServices}

🏆 最受欢迎：{topService}
   ⏱ 时长：{duration}
   📝 {description}

💬 需要了解更多详情吗？或者有其他偏好？
```

### 就近推荐门店

```markdown
📍 离您最近的门店：

{nearestStore}
   📍 {address}
   📞 {telephone}
   🚇 {trafficHint}
   📏 距离：约 {distance} 公里

🏪 附近还有其他门店：
{nearbyStores}

💬 需要我帮您预约这家门店吗？
```

---

## 取消政策模板

```markdown
📋 取消与改期政策

━━━━━━━━━━━━━━━━━━━━━━━

⏰ 取消时限
• 请至少提前 1 小时联系门店取消预约
• 超过取消时限可能无法退款

📞 联系方式
• 直接拨打门店电话：{storeTelephone}
• 提供预约 ID：{bookingId}

🔄 改期流程
• 同样需提前 1 小时联系门店
• 根据门店可用时间重新安排

💡 温馨提示
• 建议准时到店，以免延误服务
• 如有特殊情况，请及时与门店沟通
```

---

## 常见问题模板

```markdown
❓ 常见问题

Q: 如何取消预约？
A: 请至少提前 1 小时拨打门店电话 {storeTelephone}，提供预约 ID {bookingId}。

Q: 可以修改预约时间吗？
A: 可以，请提前 1 小时联系门店，根据可用时间重新安排。

Q: 最多可以预约多少人？
A: 单次预约最多 20 人。如需更多人，请分批预约或联系门店。

Q: 需要提前多久预约？
A: 建议至少提前 2 小时预约，以确保有可用时段。

Q: 营业时间是什么时候？
A: 各门店营业时间可能不同，请咨询具体门店：{storeTelephone}

Q: 如何找到门店？
A: 门店地址：{storeAddress}
   交通指引：{trafficHint}
```

---

## 使用示例

### Python 渲染示例

```python
def render_booking_confirmation(booking_data):
    """渲染预约确认消息"""
    template = open("assets/booking_template.md", "r").read()

    # 提取成功模板
    success_template = template.split("## 成功预约模板")[1].split("##")[0]

    # 替换变量
    message = success_template.format(
        bookingId=booking_data["bookingId"],
        storeName=booking_data["storeInfo"]["name"],
        storeAddress=booking_data["storeInfo"]["address"],
        storeTelephone=booking_data["storeInfo"]["telephone"],
        serviceName=booking_data["serviceInfo"]["name"],
        startTime=format_time(booking_data["startTime"]),
        endTime=format_time(booking_data["endTime"]),
        count=booking_data.get("count", 1),
        trafficInfo=booking_data["storeInfo"].get("traffic", "暂无")
    )

    return message
```

### JavaScript 渲染示例

```javascript
function renderBookingConfirmation(bookingData) {
    const template = require('fs').readFileSync('assets/booking_template.md', 'utf8');

    // 提取成功模板
    const successTemplate = template.split('## 成功预约模板')[1].split('##')[0];

    // 替换变量
    const message = successTemplate
        .replace('{bookingId}', bookingData.bookingId)
        .replace('{storeName}', bookingData.storeInfo.name)
        .replace('{storeAddress}', bookingData.storeInfo.address)
        .replace('{storeTelephone}', bookingData.storeInfo.telephone)
        .replace('{serviceName}', bookingData.serviceInfo.name)
        .replace('{startTime}', formatTime(bookingData.startTime))
        .replace('{endTime}', formatTime(bookingData.endTime))
        .replace('{count}', bookingData.count || 1)
        .replace('{trafficInfo}', bookingData.storeInfo.traffic || '暂无');

    return message;
}
```
