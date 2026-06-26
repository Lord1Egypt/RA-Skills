---
name: privacy-eraser
description: 数字身份守护。帮用户扫描网络上的个人信息，提供最有效的删除方法和平台潜规则，生成投诉模板，设置定期监控。Triggers: "删我信息", "隐私保护", "网上有我的信息", "清理数字足迹", "privacy", "remove my data"
---

# Privacy Eraser 数字身份守护

扫描 → 分析 → 给方案 → 生成投诉 → 监控

---

## 环境要求

### 最佳配置：Mac Mini + OpenClaw
```
用户的 Mac Mini 浏览器已登录各平台账号
↓
AI 通过 node 控制 Mac 上的浏览器
↓
直接自动举报，无需手动操作
```

### 检测环境
```javascript
// 开始前检测
1. 调用 nodes action=status 检查可用节点
2. 如有 Mac 节点，用 browser profile=chrome target=node 控制
3. 无节点则 fallback 到指导模式
```

---

## 使用方式

### 1. 扫描模式
```
用户: 帮我查查网上有没有我的信息

AI 执行:
1. 从 USER.md 读取用户身份信息
2. 搜索百度/Bing（Google 被墙）
3. 只报告有问题的内容
4. 给出最有效的处理方案
```

### 2. 定向模式
```
用户: 帮我删这个 [URL]

AI 执行:
1. 识别平台
2. 查平台潜规则
3. 生成投诉材料
4. 告诉用户最快的提交方式
```

### 3. 监控模式
```
用户: 帮我监控隐私

AI 执行:
1. 设置 cron 每周扫描一次
2. 发现新内容主动通知
```

### 4. 自动举报流程（需要 Mac 节点）
```
用户: 帮我删这个 [URL]

AI 执行:
1. 检测 Mac 节点: nodes action=status
2. 有节点 → 用 browser target=node profile=chrome
3. 导航到目标 URL
4. 识别平台，执行对应自动化:

百度文库:
  - 滚动到版权说明区域
  - 点击"举报"
  - 选择"侵犯隐私"
  - 填写说明
  - 提交

知乎:
  - 点击"举报"按钮
  - 选择"侵犯个人隐私"  
  - 提交

微博:
  - 点击"..."菜单
  - 选择"举报"
  - 选择"泄露隐私"
  - 提交

5. 截图存档
6. 记录到 cases/ 目录
```

---

## 自动化脚本

### 百度文库举报
```
1. browser navigate 到文档页
2. 执行 JS: document.querySelector('.report-click-item').click()
3. 等待举报弹窗
4. 选择举报类型（侵犯隐私）
5. 填写说明："该文档包含本人真实姓名等个人信息，未经本人授权公开，请予删除"
6. 点击提交
7. 截图存档
```

### 知乎举报
```
1. browser navigate 到目标内容页
2. 点击"举报"按钮
3. 选择"侵犯个人隐私"
4. 补充说明
5. 提交
6. 截图存档
```

### 微博举报
```
1. browser navigate 到微博详情页
2. 点击右上角"..."
3. 选择"举报"
4. 选择"泄露个人隐私"
5. 提交
6. 同时私信 @微博客服 加速处理
7. 截图存档
```

### Google 搜索结果移除
```
1. browser navigate 到 google.com/webmasters/tools/legal-removal-request
2. 选择"个人信息"
3. 填写 URL 和说明
4. 提交
5. 截图存档
（无需登录，但需要翻墙）
```

---

## 平台潜规则（实测有效）

### 百度文库
```
❌ 别用: tousu.baidu.com（已废弃，404）
✅ 最快: 手机APP → 右上角"..." → 举报 → 侵犯隐私
✅ 备选: 电脑端文档页底部"版权说明"→ 举报
⏱️ 处理时间: 48小时
💡 技巧: 选"侵犯隐私"比"其他"快
```

### 百度快照
```
✅ 入口: 搜索结果右下角"快照"→"投诉快照"
⚠️ 前提: 原页面必须已删除，否则快照删不掉
⏱️ 处理时间: 1-3天
```

### 百度搜索结果
```
✅ 入口: help.baidu.com/webmaster/add
✅ 选择: 个人信息保护
⏱️ 处理时间: 3-7天
```

### 知乎
```
❌ 别用: 普通"举报"按钮（慢）
✅ 最快: zhihu.com/terms/complaint → 个人信息保护
💡 技巧: 附上身份证明处理更快
⏱️ 处理时间: 3-5天
⚠️ 潜规则: 大V内容难删，匿名回答容易删
```

### 微博
```
✅ 方法: 举报 + 同时私信 @微博客服（双管齐下）
💡 技巧: 只举报不私信，处理很慢
⏱️ 处理时间: 2-7天
⚠️ 潜规则: 蓝V发的难删，转发多的几乎删不掉
```

### 政府网站
```
⚠️ 现实: 基本不会删
✅ 替代方案: 删搜索引擎快照，让它搜不到
📝 如果非要试: 联系信息公开办公室，引用《个人信息保护法》第47条
```

### Google
```
✅ 入口: google.com/webmasters/tools/legal-removal-request
✅ 选择: 个人信息 → 具体类型
⏱️ 处理时间: 1-2周
💡 国内访问需翻墙
```

### 微信公众号
```
✅ APP内: 文章底部 → "投诉" → 选择"侵犯隐私"
✅ PC端: 文章页右上角 "..." → 投诉
✅ 专用通道: https://weixin110.qq.com (隐私侵权)
⏱️ 处理时间: 3-7天（普通），1-3天（有证据）
💡 技巧: 律师函/公证书 → 快很多
💡 技巧: 侵权投诉比"其他"处理优先级高
⚠️ 潜规则: 普通用户投诉排队慢，已过原创的文章更难删
```

### 小红书
```
✅ APP内: 笔记右上角 "..." → 举报 → "涉及隐私"
✅ 创作者中心: https://creator.xiaohongshu.com
✅ 邮箱: jubao@xiaohongshu.com（侵权投诉）
⏱️ 处理时间: 24-72小时
💡 技巧: "人身攻击"比"隐私泄露"更快处理
💡 技巧: 多人举报会加速
⚠️ 潜规则: KOL/大V 的内容基本删不掉，素人笔记举报成功率高
```

### 抖音
```
✅ APP内: 视频右下角 "..." → 举报 → "侵犯隐私"
✅ 创作者中心: https://creator.douyin.com
✅ 侵权投诉: https://www.douyin.com/draft/copyright/complaint
⏱️ 处理时间: 1-7天
💡 技巧: "未经同意拍摄"成功率较高
💡 技巧: 私信博主协商删除是最快路径
⚠️ 潜规则: 视频比图文难删，播放量高的内容几乎删不掉
```

---

## 模板

### 中国平台
- `templates/baidu_removal.md` - 百度系
- `templates/zhihu_report.md` - 知乎
- `templates/weibo_report.md` - 微博
- `templates/weixin_report.md` - 微信公众号
- `templates/cyberspace_report.md` - 网信办举报

### 国际平台
- `templates/google_removal.md` - Google
- `templates/gdpr_request.md` - GDPR（欧洲）
- `templates/dmca_takedown.md` - DMCA（美国）

### 通用
- `templates/generic_privacy.md` - 通用隐私投诉
- `templates/legal_warning_cn.md` - 律师函模板

---

## 优先级判断

| 内容类型 | 紧急度 | 处理方式 |
|---------|--------|---------|
| 手机号/身份证 | 🔴 立即 | 直接举报，不协商 |
| 住址/工作单位 | 🟡 24h内 | 举报 |
| 真名+学校 | 🟡 48h内 | 举报或协商 |
| 仅姓名提及 | 🟢 可选 | 看情况，可忽略 |

---

## 监控设置

用户要求监控时，创建 cron:
```json
{
  "schedule": { "kind": "cron", "expr": "0 9 * * 1", "tz": "Asia/Shanghai" },
  "payload": { "kind": "systemEvent", "text": "隐私监控: 搜索用户姓名，检查是否有新的个人信息泄露，如有则通知用户" },
  "sessionTarget": "main"
}
```

---

## 节点浏览器控制

### 检查可用节点
```
nodes action=status
→ 查看是否有 Mac 节点在线
```

### 使用节点浏览器
```
browser action=open target=node profile=chrome targetUrl="https://..."
browser action=snapshot target=node
browser action=act target=node request={...}
```

### 为什么用节点浏览器？
```
1. 用户的 Mac 浏览器已登录各平台
2. 不需要用户手动提供 Cookie
3. 完全自动化，用户无感知
4. 支持所有需要登录的平台
```

---

## 参考资料

- `references/platforms.md` - 各平台举报入口汇总
- `references/legal_basis.md` - 法律依据（个保法、网安法等）
