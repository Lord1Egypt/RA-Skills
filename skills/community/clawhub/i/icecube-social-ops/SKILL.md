---
name: icecube-social-ops
description: "🧊 IceCube 社交账号运营中心 — 管理 X/Twitter、小红书账号的登录、发布、互动全流程。需要 Boss 一次性登录授权后，系统自动运营。当用户提到'账号运营'、'社交账号'、'发布内容'、'Twitter 运营'、'小红书运营'时使用。"
metadata:
  openclaw:
    requires:
      skills: ["browser", "xiaohongshu-publish", "social-media-agent"]
---

# 🧊 IceCube 社交账号运营中心

**Boss 授权一次，系统自动运营。**

---

## 一、账号现状

| 平台 | 登录状态 | 发布能力 | 互动能力 |
|------|----------|----------|----------|
| X/Twitter | ❌ 未登录 | 需要 OAuth 或登录 | 需要 OAuth 或登录 |
| 小红书 | ❌ 未登录 | 需要登录创作平台 | 需要登录 |

---

## 二、Boss 需要做的事（一次性）

### X/Twitter 授权

**方式 A：Browser 登录（推荐）**
1. Boss 打开 Chrome，登录 x.com
2. 启用 Chrome 远程调试：
   ```bash
   /Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --remote-debugging-port=9222
   ```
3. IceCube 通过 browser skill 连接已登录的 Chrome
4. 自动发布/互动

**方式 B：Twitter API（可选）**
- 需要 Twitter Developer 账号
- 申请 API Key + API Secret
- 配置 OAuth 2.0

### 小红书授权

**方式：Browser 登录**
1. Boss 打开 Chrome，访问 https://creator.xiaohongshu.com
2. 使用手机小红书扫码登录
3. 保持 Chrome 打开（或保存 cookies）
4. IceCube 通过 browser skill 自动发布

---

## 三、运营流程

### 日常发布流程

```
[凌晨] IceCube 生成内容（日记/教程/分享）
       ↓
[早上] 检查登录状态
       ↓
[定时] 自动发布（X: 9am/3pm/9pm, 小红书: 12:30pm/9:30pm）
       ↓
[全天] 监控互动（评论/点赞/私信）
       ↓
[晚间] 生成运营报告
```

### 发布日程

| 平台 | 时间 | 内容类型 | 频率 |
|------|------|----------|------|
| X/Twitter | 09:00 | AI 行业洞察 | 1 条 |
| X/Twitter | 15:00 | IceCube 进展 | 1 条 |
| X/Twitter | 21:00 | 热点互动 | 1 条 |
| 小红书 | 12:30 | 技术教程/干货 | 1 条 |
| 小红书 | 21:30 | IceCube Diary | 1 条 |

---

## 四、内容来源

### 自动生成

**X/Twitter：**
- AI 行业新闻 → `web_fetch` → 评论观点
- IceCube Diary → 截取片段 → 发布
- 热点话题 → `web_search` → 参与讨论

**小红书：**
- `icecube-diary` → 完整日记
- `icecube-content-factory` → 教程内容
- 用户问题 → 解答 → 干货分享

### 内容审批（可选）

**默认：自动发布**
- 内容质量检查（无敏感词、格式正确）
- 自动发布

**可选：Boss 审批**
- 生成内容后发送给 Boss
- Boss 确认后发布
- 适合初期运营

---

## 五、互动策略

### X/Twitter 互动

**主动互动：**
- 关注相关账号（AI、OpenClaw、开发者）
- 回复热门推文（有价值观点）
- 转发有价值内容 + 评论

**被动互动：**
- 回复评论（24 小时内）
- 感谢点赞/转发
- 处理私信

### 小红书互动

**评论回复：**
- 技术问题 → 详细解答
- 合作意向 → 引导私信
- 简单感谢 → 礼貌回复

**私信处理：**
- 常见问题 → 自动回复模板
- 服务需求 → 记录并通知 Boss
- 合作机会 → 记录并通知 Boss

---

## 六、数据追踪

### memory/social-ops/YYYY-MM-DD.md

```markdown
# 社交运营日报 — YYYY-MM-DD

## X/Twitter
- 发布：3 条
- 曝光：XXX
- 互动：XX 点赞 / XX 转发 / XX 评论
- 新粉丝：+X
- 热门内容：[内容摘要]

## 小红书
- 发布：2 条
- 浏览：XXX
- 互动：XX 点赞 / XX 收藏 / XX 评论
- 新粉丝：+X
- 热门内容：[内容摘要]

## 转化
- 私信咨询：X 条
- 服务需求：X 条
- 知识星球引流：X 人

## 问题
- [任何需要 Boss 处理的问题]
```

---

## 七、风险控制

### 发布限制

| 平台 | 每日上限 | 安全间隔 |
|------|----------|----------|
| X/Twitter | 5 条 | 45 秒+ |
| 小红书 | 3 条 | 2 小时+ |

### 敏感词过滤

- 政治敏感词
- 广告敏感词
- 平台禁用词

### 异常处理

- 发布失败 → 记录日志 → 重试 1 次
- 登录失效 → 通知 Boss → 等待重新登录
- 限流 → 暂停发布 → 等待恢复

---

## 八、启动清单

### Boss 操作

- [ ] 打开 Chrome，登录 x.com
- [ ] 启用 Chrome 远程调试（端口 9222）
- [ ] 登录小红书创作平台
- [ ] 确认两个平台都保持登录状态
- [ ] 告诉 IceCube "可以开始运营了"

### IceCube 操作

- [ ] 验证 X/Twitter 登录状态
- [ ] 验证小红书登录状态
- [ ] 生成首发内容
- [ ] 开始自动运营

---

## 九、命令参考

### 检查登录状态

```bash
# 检查 Chrome 远程调试是否运行
curl -s http://localhost:9222/json/version

# 如果返回 JSON，Chrome 调试可用
```

### 手动发布测试

**X/Twitter：**
```
1. browser open → x.com/compose/post
2. 确认页面加载
3. 输入测试内容
4. 发布
```

**小红书：**
```
1. browser open → creator.xiaohongshu.com/publish/publish
2. 确认已登录
3. 输入测试内容
4. 发布
```

---

## 十、预期成果

### 第 1 周

- 发布：X 21 条 + 小红书 14 条
- 粉丝：X +50 + 小红书 +100
- 内容品牌确立

### 第 1 月

- 发布：X 90 条 + 小红书 60 条
- 粉丝：X +200 + 小红书 +500
- 收入转化：¥500-2000

### 第 3 月

- 发布：持续
- 粉丝：X +1000 + 小红书 +2000
- 收入转化：¥5000-20000

---

## License

MIT — Use freely.

---

*Boss 授权一次，系统自动运营。*

---

## ⚠️ 当前状态

**需要 Boss 操作：**
1. 登录 X/Twitter（Chrome 远程调试）
2. 登录小红书创作平台

**完成后告诉 IceCube：** "账号已登录，开始运营"