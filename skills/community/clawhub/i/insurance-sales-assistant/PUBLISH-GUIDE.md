# 📦 发布 sales-assistant 到 ClawHub

> 状态：⏳ 待登录

---

## 🚀 发布步骤

### 步骤 1：登录 ClawHub

```bash
# 方式 1：浏览器登录（推荐）
clawhub login

# 方式 2：手动输入 Token
clawhub auth token <your-token>
```

**登录流程：**
1. 运行 `clawhub login`
2. 浏览器自动打开
3. 登录 clawhub.com
4. 授权 OpenClaw
5. 返回终端，显示 "Logged in as: xxx"

---

### 步骤 2：验证登录

```bash
clawhub whoami
# 应该显示：Logged in as: <your-username>
```

---

### 步骤 3：发布 Skill

```bash
# 方式 1：从目录发布（推荐）
cd ~/.openclaw/workspace/skills/sales-assistant
clawhub publish .

# 方式 2：从 skill 文件发布
clawhub publish ~/.openclaw/workspace/skills/sales-assistant
```

**发布流程：**
1. 运行发布命令
2. 输入 Skill 信息（如果首次发布）：
   - **Slug**: `sales-assistant`
   - **名称**: `销售行为管理助手`
   - **描述**: `保险代理人销售行为管理助手。自动创建飞书多维表格、文档和表单，包含每日任务推送、暖客池管理、签单追踪、周/月复盘、业绩统计。`
   - **版本**: `1.1.0`
   - **标签**: `sales,insurance,feishu,crm,automation`
   - **是否公开**: `yes`

3. 确认发布信息
4. 等待上传完成
5. 显示发布成功

---

### 步骤 4：验证发布

```bash
# 搜索已发布的 skill
clawhub search sales-assistant

# 查看 skill 详情
clawhub inspect sales-assistant

# 应该显示 skill 元数据和文件列表
```

---

## 📋 发布配置

### 必需文件

- [x] `SKILL.md` - 核心指令
- [x] `README.md` - 使用说明
- [x] `scripts/init.sh` - 初始化脚本
- [x] `templates/` - 模板文件
- [x] `evals/evals.json` - 测试用例

### 可选文件

- [x] `RELEASE-NOTES.md` - 更新日志

---

## 🔧 元数据配置

### 建议配置

```json
{
  "slug": "sales-assistant",
  "name": "销售行为管理助手",
  "description": "保险代理人销售行为管理助手。自动创建飞书多维表格、文档和表单，包含每日任务推送、暖客池管理、签单追踪、周/月复盘、业绩统计。",
  "version": "1.1.0",
  "tags": [
    "sales",
    "insurance",
    "feishu",
    "crm",
    "automation",
    "productivity"
  ],
  "author": "your-username",
  "license": "MIT",
  "visibility": "public",
  "category": "productivity"
}
```

---

## ⚠️ 注意事项

### 发布前检查

- [ ] 确认 `SKILL.md` 不包含硬编码的资源链接
- [ ] 确认 `SKILL.md` 不包含个人隐私信息
- [ ] 确认所有模板文件已完成
- [ ] 确认测试用例通过
- [ ] 确认已登录 ClawHub

### 发布后验证

- [ ] 搜索 skill 可见
- [ ] 安装 skill 正常
- [ ] 自动初始化正常
- [ ] 无错误日志

---

## 🔄 更新 Skill

### 修改后重新发布

```bash
# 1. 修改 skill 文件
cd ~/.openclaw/workspace/skills/sales-assistant
# 编辑 SKILL.md 或其他文件

# 2. 更新版本号
# 编辑 SKILL.md  frontmatter 中的 version

# 3. 重新发布
clawhub publish . --update

# 或
clawhub update sales-assistant
```

---

## 📊 发布统计

发布后可以查看：

```bash
# 查看下载量
clawhub inspect sales-assistant

# 查看评分
clawhub search sales-assistant
```

---

## 🐛 常见问题

### Q1: 发布失败 "Not logged in"

**解决：**
```bash
clawhub login
```

### Q2: 发布失败 "Slug already exists"

**解决：**
```bash
# 更新现有 skill
clawhub publish . --update

# 或使用不同的 slug
clawhub publish . --slug sales-assistant-v2
```

### Q3: 发布后搜索不到

**原因：** 索引延迟（通常 1-5 分钟）

**解决：** 等待几分钟后重试

### Q4: 安装失败 "Skill not found"

**解决：**
```bash
# 确认 slug 正确
clawhub inspect sales-assistant

# 检查网络连接
clawhub search sales
```

---

## 📞 下一步

### 立即发布

```bash
# 1. 登录
clawhub login

# 2. 验证登录
clawhub whoami

# 3. 发布
cd ~/.openclaw/workspace/skills/sales-assistant
clawhub publish .
```

### 发布成功后

1. 分享链接给其他人
2. 编写使用教程
3. 录制演示视频
4. 收集用户反馈

---

**准备就绪！请先登录 ClawHub，然后执行发布命令！** 🚀

```bash
clawhub login
```
