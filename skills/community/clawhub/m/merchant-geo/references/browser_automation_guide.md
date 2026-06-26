# 浏览器自动化发布指南

本文档详细说明如何使用 `agent-browser` 工具自动化发布内容到各自媒体平台。

---

## 工具基础命令

```bash
# 启动浏览器（如需要）
agent-browser install  # 首次安装Chrome

# 打开网页
agent-browser open <url>

# 获取页面元素（用于交互）
agent-browser snapshot -i

# 点击元素
agent-browser click "@e1"  # @e1 是元素引用号
agent-browser click "text=发布"

# 输入文本
agent-browser fill "#title" "文章标题"
agent-browser type "[contenteditable]" "正文内容"

# 上传文件
agent-browser upload "[上传按钮]" "C:/path/to/image.jpg"

# 截图
agent-browser screenshot

# 关闭浏览器
agent-browser close
```

---

## 发布前准备

### 1. 商家准备工作

商家需要在浏览器中提前登录各平台账号：
- 建议使用 **Chrome** 或 **Edge** 浏览器
- 勾选"记住密码"，避免每次发布都需要登录
- 确保浏览器能正常访问各平台后台

### 2. 识别页面元素

发布前先用 `snapshot -i` 获取页面元素：

```bash
agent-browser open https://baijiahao.baidu.com/
agent-browser snapshot -i
```

会返回类似这样的元素列表：
```
@e1  [button]  "登录"
@e2  [input]   placeholder="请输入标题"
@e3  [div]     contenteditable
@e4  [button]  "发布"
```

然后根据引用号进行操作。

---

## 各平台详细发布流程

### 1. 百家号（百度SEO核心）

**后台地址**：https://baijiahao.baidu.com/

**完整流程**：
```bash
# 打开百家号后台
agent-browser open https://baijiahao.baidu.com/

# 如果需要登录，等待用户操作
# agent-browser snapshot -i  # 查看登录状态

# 点击发布文章
agent-browser click "text=发布文章"

# 等待编辑页面加载
agent-browser wait 2000

# 获取编辑页面元素
agent-browser snapshot -i

# 输入标题（根据实际元素调整选择器）
agent-browser fill "[title-input-selector]" "深圳光明区马田烟酒老店，专注品质20年"

# 输入正文
agent-browser type "[content-editor]" "【正文内容...】"

# 添加标签
agent-browser click "text=添加标签"
agent-browser type "[tag-input]" "深圳烟酒"
agent-browser press Enter

# 上传封面图（如有）
agent-browser click "[上传封面]"
# 注：文件上传需手动选择，或使用 upload 命令

# 点击发布
agent-browser click "text=发布"

# 截图确认
agent-browser screenshot

# 关闭
agent-browser close
```

**注意事项**：
- 百家号对图片有大小限制（单张<5MB）
- 正文编辑器可能是 contenteditable div，需用 `type` 命令
- 发布后截图确认发布成功

---

### 2. 头条号（字节SEO核心）

**后台地址**：https://mp.toutiao.com/

**完整流程**：
```bash
agent-browser open https://mp.toutiao.com/
agent-browser click "text=发头条"
agent-browser wait 2000
agent-browser snapshot -i

# 标题
agent-browser fill "[title-selector]" "[标题]"

# 正文
agent-browser type "[content-selector]" "[正文]"

# 标签
agent-browser click "text=添加标签"
agent-browser type "[tag-selector]" "深圳"
agent-browser press Enter

# 分类
agent-browser click "[category-selector]"

# 发布
agent-browser click "text=发布"
agent-browser screenshot
```

---

### 3. 知乎（权威内容）

**后台地址**：https://www.zhihu.com/creator/create-article

**完整流程**：
```bash
agent-browser open https://www.zhihu.com/creator/create-article
agent-browser wait 2000
agent-browser snapshot -i

# 标题
agent-browser fill "[title-input]" "[标题]"

# 正文
agent-browser type "[article-editor]" "[正文]"

# 添加话题
agent-browser click "[topic-button]"
agent-browser type "[topic-input]" "深圳烟酒"
agent-browser click "[搜索结果]"

# 发布
agent-browser click "text=发布文章"
agent-browser screenshot
```

---

### 4. 小红书（种草转化）

**后台地址**：https://creator.xiaohongshu.com/

**完整流程**：
```bash
agent-browser open https://creator.xiaohongshu.com/
agent-browser wait 2000

# 上传图片/封面
agent-browser click "[上传图片按钮]"
agent-browser upload "[file-input]" "C:/images/cover.jpg"

# 等待图片上传
agent-browser wait 3000

# 标题
agent-browser fill "[title-input]" "[标题]"

# 正文
agent-browser type "[content-editor]" "[正文]"

# 话题标签
agent-browser type "[tag-input]" "#深圳探店"
agent-browser type "[tag-input]" "#烟酒"

# 地点标签
agent-browser click "[location-button]"
agent-browser click "[深圳]"

# 发布
agent-browser click "text=发布"
agent-browser screenshot
```

---

### 5. 抖音（流量爆发）

**后台地址**：https://creator.douyin.com/

**完整流程**：
```bash
agent-browser open https://creator.douyin.com/
agent-browser wait 2000

# 上传视频
agent-browser click "[上传视频]"
agent-browser upload "[file-input]" "C:/videos/intro.mp4"

# 等待上传完成
agent-browser wait 5000

# 描述/文案
agent-browser fill "[desc-input]" "[视频描述文案...]"

# 话题标签
agent-browser type "[tag-input]" "#深圳烟酒"
agent-browser type "[tag-input]" "#探店"

# 封面（可选）
agent-browser click "[设置封面]"

# 发布
agent-browser click "text=发布"
agent-browser screenshot
```

**注意**：视频上传必须手动选择文件，自动化只负责文案部分。

---

### 6. 搜狐号（搜狗SEO）

**后台地址**：https://mp.sohu.com/

**完整流程**：
```bash
agent-browser open https://mp.sohu.com/
agent-browser wait 2000
agent-browser click "text=发布文章"
agent-browser snapshot -i

# 标题
agent-browser fill "[title-selector]" "[标题]"

# 正文
agent-browser type "[content-editor]" "[正文]"

# 来源
agent-browser fill "[source-selector]" "[企业名称]"

# 发布
agent-browser click "text=发布"
agent-browser screenshot
```

---

### 7. 网易号（网易搜索）

**后台地址**：https://mp.163.com/

**完整流程**：
```bash
agent-browser open https://mp.163.com/
agent-browser wait 2000
agent-browser click "text=发布文章"
agent-browser snapshot -i

# 标题
agent-browser fill "[title-selector]" "[标题]"

# 正文
agent-browser type "[content-editor]" "[正文]"

# 分类
agent-browser click "[category-selector]"

# 发布
agent-browser click "text=发布"
agent-browser screenshot
```

---

### 8. 快手（下沉市场）

**后台地址**：https://cp.kuaishou.com/

**完整流程**：
```bash
agent-browser open https://cp.kuaishou.com/
agent-browser wait 2000

# 上传作品
agent-browser click "[上传作品]"
agent-browser upload "[file-input]" "C:/videos/kuaishou.mp4"

# 等待上传
agent-browser wait 5000

# 描述文案
agent-browser fill "[desc-input]" "[文案...]"

# 话题标签
agent-browser type "[tag-input]" "#老铁"
agent-browser type "[tag-input]" "#深圳"

# 发布
agent-browser click "text=发布"
agent-browser screenshot
```

---

## 批量发布工作流

对于需要发布到多个平台的情况，建议按以下顺序：

```bash
# 1. 百家号
agent-browser open https://baijiahao.baidu.com/
# ... 发布流程
agent-browser close

# 2. 头条号
agent-browser open https://mp.toutiao.com/
# ... 发布流程
agent-browser close

# 3. 知乎
agent-browser open https://www.zhihu.com/creator/create-article
# ... 发布流程
agent-browser close

# ... 以此类推
```

---

## 常见问题处理

### 1. 需要登录怎么办？

遇到登录页面时，暂停自动化，让用户手动登录：

```bash
agent-browser open https://baijiahao.baidu.com/
# 等待用户扫码/输入密码
agent-browser snapshot -i  # 确认已登录
# 继续自动化流程
```

### 2. 找不到元素怎么办？

使用 `find` 命令查找元素：

```bash
agent-browser find text "发布" click
agent-browser find role button click --name "发布"
agent-browser find placeholder "请输入标题" fill "标题内容"
```

### 3. 上传文件失败？

Windows下路径需要使用正斜杠或转义：

```bash
# 正确
agent-browser upload "[input]" "C:/Users/admin/Pictures/image.jpg"

# 或者
agent-browser upload "[input]" "C:\\Users\\admin\\Pictures\\image.jpg"
```

### 4. 页面加载慢？

添加等待：

```bash
agent-browser wait 3000  # 等待3秒
# 或等待特定元素出现
agent-browser wait "[loading-spinner]"  # 等待加载动画消失
```

---

## 安全与隐私建议

1. **账号安全**：建议使用专门的工作账号，避免使用老板的私人账号
2. **验证码处理**：遇到验证码时暂停自动化，人工处理
3. **发布频率**：避免短时间内大量发布，可能触发平台风控
4. **内容审核**：发布前检查内容是否符合平台规范
