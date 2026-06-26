# 企业微信API配置指南

## 🔧 配置步骤

### 1. 获取企业微信应用配置信息

1. 登录企业微信管理后台：https://work.weixin.qq.com
2. 进入"应用管理" → "应用"
3. 选择你的应用（如果没有，需要先创建应用）
4. 记录以下信息：
   - **企业ID (CorpID)**: 企业微信的唯一标识
   - **应用Secret**: 应用的密钥
   - **Webhook URL**: 回调地址URL
   - **智能表格ID**: 如果需要使用智能表格功能

### 2. 配置回调地址

#### 回调地址要求：
- 必须使用HTTPS协议
- 域名必须已备案
- 域名必须添加到企业微信可信域名列表
- 回调地址必须可以正常访问

#### 配置步骤：
1. 在企业微信应用管理后台，进入"企业微信插件"
2. 点击"设置回调模式"
3. 填写回调服务器地址（例如：`https://your-domain.com/webhook`）
4. 添加回调域名到可信域名列表

### 3. 更新配置文件

修改 `config.json` 中的企业微信配置部分：

```json
"wechatWork": {
  "webhookUrl": "https://your-domain.com/webhook",
  "smartTableId": "xxxxx",
  "departmentId": "1",
  "apiToken": "your_access_token_here",
  "corpId": "your_corp_id",
  "corpSecret": "your_corp_secret",
  "token": "your_token",
  "encodingAESKey": "your_encoding_aes_key"
}
```

## 🔍 常见问题排查

### 问题1：回调地址请求不通过

**可能原因：**
1. 回调地址不在可信域名列表中
2. 回调地址无法正常访问
3. 使用了HTTP而非HTTPS
4. 证书问题

**解决方案：**
```bash
# 测试回调地址是否可访问
curl -I https://your-domain.com/webhook

# 检查证书
openssl s_client -connect your-domain.com:443 -servername your-domain.com
```

### 问题2：API调用失败

**可能原因：**
1. Access Token过期
2. 参数格式错误
3. 权限不足

**解决方案：**
```javascript
// 测试获取Access Token
const wechatAPI = new WeChatWorkAPI(config);
const token = await wechatAPI.getAccessToken(config.wechatWork.corpId, config.wechatWork.corpSecret);
console.log('Access Token:', token);
```

### 问题3：智能表格记录失败

**可能原因：**
1. 智能表格ID错误
2. 数据格式不符合要求
3. API权限不足

**解决方案：**
1. 确认智能表格ID正确
2. 检查数据字段是否匹配表格列名
3. 确认应用有智能表格写入权限

## 🧪 测试脚本

创建测试文件 `test-wechat.js`：

```javascript
const WeChatWorkAPI = require('./wechat-api');
const config = require('./config.json');

const wechatAPI = new WeChatWorkAPI(config.wechatWork);

async function testWeChat() {
  try {
    // 测试发送文本消息
    await wechatAPI.sendText('测试消息：药学系统招标信息收集系统已启动');
    console.log('文本消息发送成功');
    
    // 测试发送Markdown消息
    const markdown = `
## 📋 测试通知

**系统名称**: 药学系统招标信息收集系统
**状态**: 运行正常
**时间**: ${new Date().toLocaleString()}

---
*此为测试消息*
    `;
    
    await wechatAPI.sendMarkdown(markdown);
    console.log('Markdown消息发送成功');
    
    // 测试智能表格记录
    if (config.wechatWork.smartTableId) {
      const testData = {
        '测试项目': '测试记录',
        '测试时间': new Date().toLocaleString(),
        '状态': '成功'
      };
      
      await wechatAPI.recordToSmartTable(testData);
      console.log('智能表格记录成功');
    }
    
  } catch (error) {
    console.error('测试失败:', error.message);
  }
}

testWeChat();
```

运行测试：
```bash
node test-wechat.js
```

## 📋 智能表格字段建议

在创建智能表格时，建议包含以下字段：

| 字段名 | 类型 | 说明 |
|--------|------|------|
| 项目名称 | 文本 | 招标项目名称 |
| 招标单位 | 文本 | 招标单位名称 |
| 预算金额 | 数字 | 项目预算金额 |
| 购标截止日期 | 日期 | 购买标书的截止日期 |
| 开标日期 | 日期 | 开标日期 |
| 涉及产品范围 | 文本 | 相关产品范围 |
| 对应负责销售 | 人员 | 负责的销售人员 |
| 项目状态 | 单选 | 项目状态（待评估/建议投标/不建议投标） |
| 创建时间 | 日期 | 记录创建时间 |

## 🔒 安全注意事项

1. **保护敏感信息**：不要将Secret、Token等敏感信息提交到代码仓库
2. **定期更新Token**：Access Token有效期为2小时，需要定期更新
3. **HTTPS配置**：确保回调地址使用HTTPS，并配置正确的证书
4. **IP白名单**：如果可能，将企业微信服务器IP添加到防火墙白名单

## 📞 技术支持

如果遇到问题，可以：
1. 查看企业微信官方文档：https://developer.work.weixin.qq.com
2. 检查企业微信应用配置是否正确
3. 确认网络连接和服务器状态
4. 查看详细错误日志进行排查