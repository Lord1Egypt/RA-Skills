# 拼多多客服助手 (pinduoduo-cs-assistant)

🛒 **拼多多商家客服自动化助手** - 基于 OpenClaw browser 工具实现 RPA 自动化，7x24 小时智能客服值守

## ✨ 核心功能

### 1. 浏览器自动化登录
- 自动打开拼多多商家后台
- 扫码登录/账号密码登录
- Session 持久化（避免重复登录）
- 多店铺账号切换

### 2. 智能消息读取
- 实时监听买家咨询消息（5 秒轮询）
- 未读消息自动提醒
- 消息内容提取（文本/图片/订单信息）
- 买家历史订单查询

### 3. 智能回复生成
- 基于上下文自动生成回复
- 话术库匹配（售前/售后/物流/退换货）
- 个性化回复（带买家昵称、订单信息）
- 表情包/图片自动匹配

### 4. 快捷回复发送
- 一键发送常用话术
- 自定义话术模板
- 批量回复（促销活动时）
- 发送记录追踪

### 5. 售后订单处理
- 退款申请自动读取
- 退换货工单处理
- 物流异常预警
- 差评预警与挽回

## 🚀 快速开始

### 安装依赖

```bash
cd pinduoduo-cs-assistant
npm install
```

### 登录商家后台

```bash
# 方式 1：开发模式（ts-node）
npm run dev login

# 方式 2：生产模式（编译后）
npm run build
npm start login
```

### 监听消息

```bash
# 监听 1 小时（3600 秒）
npm run dev listen --duration 3600

# 监听 8 小时（工作日）
npm run dev listen --duration 28800
```

### 查看未读消息

```bash
npm run dev messages
```

### 智能回复

```bash
npm run dev reply --conversation-id "会话 ID"
```

### 管理话术库

```bash
# 查看所有话术
npm run dev templates --list

# 查看特定分类话术
npm run dev templates --list --category "售前"
```

## 📚 话术库分类

### 售前咨询
- 库存查询
- 发货时间
- 优惠活动
- 产品材质/质量

### 物流查询
- 物流跟踪
- 快递催促
- 快递指定

### 售后处理
- 退货退款
- 质量问题
- 差评处理
- 发票申请

## 🔧 配置说明

### 环境变量

创建 `.env` 文件：

```bash
# 拼多多商家后台 URL
PDD_URL=https://mms.pinduoduo.com

# 消息检查间隔（毫秒）
CHECK_INTERVAL=5000

# Session 超时时间（毫秒，默认 24 小时）
SESSION_TIMEOUT=86400000

# 是否自动回复（true/false）
AUTO_REPLY=false

# 自动回复延迟（毫秒）
AUTO_REPLY_DELAY=3000
```

### 自定义话术

编辑 `src/index.ts` 中的 `TEMPLATES` 对象：

```typescript
const TEMPLATES = {
  售前: [
    {
      keywords: ['有货吗', '还有货', '库存'],
      response: '亲，这款商品目前有现货的哦~'
    }
  ],
  // 添加更多分类和话术...
}
```

## 📊 使用示例

### 场景 1：日常客服值守

```bash
# 早上 9 点开始监听
npm run dev listen --duration 28800  # 8 小时
```

### 场景 2：促销活动期间

```bash
# 双 11 期间，监听 12 小时
npm run dev listen --duration 43200

# 查看实时消息
npm run dev messages
```

### 场景 3：售后处理

```bash
# 查看待处理售后
npm run dev after-sales --pending

# 处理退款申请
npm run dev refund --order-id "PDD20260403001" --action approve
```

## 🛡️ 安全与合规

**严格遵守：**
- ✅ 仅人工触发操作
- ✅ 通过拼多多官方商家后台
- ✅ 不存储买家敏感信息
- ✅ 合理请求频率，避免风控

**不会执行：**
- ❌ 自动发送骚扰消息
- ❌ 批量刷单/刷好评
- ❌ 抓取非公开数据
- ❌ 绕过平台风控

## 📈 数据看板

### 实时统计
- 今日接待买家数
- 平均响应时间
- 消息回复率
- 转化率（咨询→下单）

### 查看统计

```bash
# 今日数据
npm run dev stats --today

# 本周数据
npm run dev stats --week

# 本月数据
npm run dev stats --month
```

## 🔌 扩展集成

### 飞书集成（计划中）
- 买家咨询消息推送到飞书群
- 售后工单自动创建飞书任务
- 数据报表自动同步飞书多维表格

### 微信通知（计划中）
- 重要买家消息微信提醒
- 售后预警微信推送

### AI 智能回复（计划中）
- 接入大模型生成个性化回复
- 自动学习历史优质回复话术
- 情感分析（识别买家情绪）

## 🐛 常见问题

### Q1: 登录失败怎么办？
**A:** 
1. 检查网络连接
2. 尝试手动扫码登录
3. Session 过期需重新登录
4. 清除浏览器缓存

### Q2: 消息监听不工作？
**A:**
1. 确认浏览器保持打开状态
2. 确认客服工作台页面处于激活状态
3. 检查网络是否正常
4. 查看控制台错误日志

### Q3: 话术匹配不准确？
**A:**
1. 优化话术库关键词
2. 添加更多同义词和变体
3. 根据实际对话调整回复内容

### Q4: 被平台风控限制？
**A:**
1. 降低请求频率（增加 CHECK_INTERVAL）
2. 避免短时间内大量操作
3. 人工介入处理敏感操作
4. 使用真实用户行为模式

## 📝 开发指南

### 项目结构

```
pinduoduo-cs-assistant/
├── src/
│   └── index.ts          # 主入口
├── scripts/
│   ├── config.json       # 配置文件
│   └── templates.json    # 话术库
├── tests/
│   └── index.test.ts     # 单元测试
├── references/
│   └── api-docs.md       # API 文档
├── assets/
│   └── icons/            # 图标资源
├── package.json
├── tsconfig.json
├── skill.json
└── README.md
```

### 添加新功能

1. 在 `src/index.ts` 添加新函数
2. 在 `main()` 函数添加新命令
3. 更新 `skill.json` 的 commands 列表
4. 编写单元测试
5. 更新文档

### 测试

```bash
# 运行单元测试
npm test

# 运行特定测试
npm test -- --testNamePattern="登录测试"
```

## 📦 发布到 ClawHub

```bash
# 登录 ClawHub
claw login --token <your-token>

# 进入项目目录
cd pinduoduo-cs-assistant

# 发布
claw skill publish

# 验证发布
claw skill my
```

## 📄 License

MIT License

## 👥 作者

OpenClaw Skill Master

## 🙏 致谢

- OpenClaw 团队
- ClawHub 社区
- 拼多多开放平台

---

**🛒 拼多多客服自动化助手 — 7x24 小时智能值守，提升客服效率**
