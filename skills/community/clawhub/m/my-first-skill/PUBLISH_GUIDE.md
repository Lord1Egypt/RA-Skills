# ClawHub技能发布指南

## 📋 发布前准备

### 1. 检查技能完整性
确保以下文件都存在：
```
my-first-skill/
├── SKILL.md          # ✅ 必须
├── README.md         # ✅ 必须  
├── package.json      # ✅ 必须
├── config.json       # ✅ 推荐
├── references/       # ✅ 推荐
└── scripts/          # ✅ 推荐
```

### 2. 更新版本号
在 `package.json` 中更新版本号：
```json
{
  "version": "1.0.0"  # 更新为适当版本
}
```

### 3. 更新作者信息
在 `package.json` 和 `SKILL.md` 中更新作者信息：
```json
{
  "author": "你的名字 <你的邮箱@example.com>",
  "repository": {
    "url": "https://github.com/你的用户名/my-first-skill.git"
  }
}
```

### 4. 运行测试
```bash
cd /root/.openclaw/my-first-skill
python3 scripts/test_skill.py
```

## 🚀 发布到ClawHub

### 方法一：使用clawhub CLI（推荐）

#### 1. 安装clawhub CLI
```bash
# 如果还没有安装
npm install -g clawhub
# 或
pnpm add -g clawhub
```

#### 2. 登录ClawHub
```bash
clawhub login
# 按照提示输入用户名和密码
```

#### 3. 发布技能
```bash
cd /root/.openclaw/my-first-skill
clawhub publish
```

#### 4. 填写发布信息
发布时会提示输入：
- **技能名称**: my-first-skill（建议保持与目录名一致）
- **显示名称**: 招标项目分析技能
- **描述**: 简要描述技能功能
- **版本**: 1.0.0
- **标签**: openclaw, skill, bid, analysis, database
- **分类**: business（商务类）

### 方法二：通过GitHub发布

#### 1. 创建GitHub仓库
```bash
# 初始化Git仓库
cd /root/.openclaw/my-first-skill
git init
git add .
git commit -m "初始提交: 招标项目分析技能 v1.0.0"

# 创建GitHub仓库（在GitHub网站操作）
# 然后添加远程仓库
git remote add origin https://github.com/你的用户名/my-first-skill.git
git branch -M main
git push -u origin main
```

#### 2. 在ClawHub网站发布
1. 访问 https://clawhub.com
2. 点击 "发布技能"
3. 填写技能信息
4. 输入GitHub仓库URL
5. 提交审核

## 🔧 发布后操作

### 1. 验证发布
```bash
# 搜索你的技能
clawhub search my-first-skill

# 查看技能详情
clawhub info my-first-skill
```

### 2. 安装测试
```bash
# 从ClawHub安装
clawhub install my-first-skill

# 或指定版本
clawhub install my-first-skill@1.0.0
```

### 3. 使用技能
```bash
# 在OpenClaw中使用
openclaw skill my-first-skill analyze --file 招标文件.xlsx
```

## 📝 技能元数据规范

### package.json 关键字段
```json
{
  "name": "my-first-skill",                    // 技能ID，必须小写、无空格
  "version": "1.0.0",                         // 语义化版本号
  "description": "技能描述",                   // 简短描述
  "keywords": ["openclaw", "skill", "bid"],   // 搜索关键词
  "author": "作者 <邮箱>",                     // 作者信息
  "license": "MIT",                           // 许可证
  
  "openclaw": {
    "skill": true,                            // 必须为true
    "category": "business",                   // 分类：business/tools/entertainment等
    "triggers": ["招标", "分析", "数据库"],    // 触发关键词
    "requirements": ["mysql-server", "python3"], // 系统要求
    "install": "pip install pandas mysql-connector-python" // 安装命令
  }
}
```

### SKILL.md 规范
- **技能描述**: 清晰说明技能功能
- **适用场景**: 何时使用该技能
- **技能功能**: 详细功能列表
- **使用方法**: 具体使用示例
- **技术依赖**: 需要的软件/库
- **配置文件**: 配置说明
- **示例对话**: 展示交互过程
- **注意事项**: 重要提示
- **更新日志**: 版本历史
- **作者信息**: 联系方式
- **许可证**: 使用许可

## 🐛 常见问题

### Q1: 发布时提示"技能名称已存在"
A: 修改技能名称，确保唯一性

### Q2: 审核不通过
A: 检查：
- 技能描述是否清晰
- 代码是否有安全问题
- 依赖是否明确
- 许可证是否合适

### Q3: 用户安装后无法使用
A: 检查：
- 依赖是否自动安装
- 配置文件是否正确
- 错误提示信息是否友好

### Q4: 如何更新技能
A: 
```bash
# 更新版本号
# 提交更改
git add .
git commit -m "更新: v1.0.1"
git push

# 重新发布
clawhub publish
```

## 📈 技能优化建议

### 1. 用户体验
- 添加详细的错误提示
- 提供使用示例
- 添加进度显示
- 支持多种输入格式

### 2. 代码质量
- 添加单元测试
- 编写文档注释
- 处理边界情况
- 优化性能

### 3. 功能扩展
- 添加更多分析功能
- 支持导出多种格式
- 添加定时任务
- 集成通知功能

### 4. 社区支持
- 创建GitHub Issues模板
- 编写贡献指南
- 添加变更日志
- 响应问题反馈

## 🔒 安全注意事项

### 1. 数据库安全
- 不要硬编码密码
- 使用环境变量
- 限制数据库权限
- 定期备份数据

### 2. 文件安全
- 验证文件类型
- 限制文件大小
- 清理临时文件
- 防止路径遍历

### 3. 代码安全
- 避免命令注入
- 验证用户输入
- 使用参数化查询
- 处理异常情况

## 🌟 成功案例参考

查看ClawHub上的热门技能，学习最佳实践：
```bash
# 查看热门技能
clawhub list --sort downloads

# 查看技能详情
clawhub info 技能名称
```

## 📞 支持与帮助

### 官方资源
- ClawHub文档: https://docs.clawhub.com
- OpenClaw文档: https://docs.openclaw.ai
- GitHub仓库: https://github.com/openclaw/openclaw
- Discord社区: https://discord.gg/clawd

### 问题反馈
1. 在GitHub创建Issue
2. 在Discord社区提问
3. 邮件联系: support@clawhub.com

### 贡献指南
欢迎提交Pull Request改进技能：
1. Fork仓库
2. 创建功能分支
3. 提交更改
4. 创建Pull Request

---

**最后更新**: 2026年3月24日  
**技能状态**: 准备发布  
**测试状态**: ✅ 通过  
**文档状态**: ✅ 完整  

祝你的技能发布成功！🎉