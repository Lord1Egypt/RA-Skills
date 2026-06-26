# 📦 Literature Search Workflow - ClawHub 上传指南

**创建时间**: 2026-03-14  
**技能版本**: v1.0.0  
**作者**: academic-assistant

---

## 📋 技能包内容

```
literature-search-workflow/
├── openclaw.skill.json    # 技能配置 (3.0 KB)
├── SKILL.md               # 技能说明 (3.9 KB)
└── scripts/
    └── literature_search.py # 主脚本 (4.3 KB)
```

**总大小**: ~11 KB

---

## 🚀 上传步骤

### 步骤 1: 登录 ClawHub

浏览器已打开，请访问：
```
https://clawhub.ai/cli/auth
```

**登录流程**:
1. 点击浏览器中的链接
2. 使用 ClawHub 账号登录
3. 授权 CLI 访问
4. 登录成功后返回终端

---

### 步骤 2: 验证登录

```bash
clawhub whoami
```

**预期输出**:
```
✅ Logged in as: [你的用户名]
```

---

### 步骤 3: 上传技能

```bash
clawhub publish C:\Users\13600\.openclaw\workspace\skills\literature-search-workflow
```

**预期输出**:
```
📦 Packing skill...
📤 Uploading to ClawHub...
✅ Published successfully!
🔗 Skill URL: https://clawhub.com/skills/literature-search-workflow
```

---

### 步骤 4: 验证上传

访问 ClawHub 技能页面：
```
https://clawhub.com/skills/literature-search-workflow
```

**检查内容**:
- ✅ 技能名称正确
- ✅ 描述完整
- ✅ 版本号正确 (v1.0.0)
- ✅ 作者信息
- ✅ 许可证 (MIT)

---

## 📊 技能信息

### 基本信息

| 项目 | 内容 |
|------|------|
| **技能 ID** | literature-search-workflow |
| **技能名称** | Literature Search Workflow |
| **版本** | v1.0.0 |
| **作者** | academic-assistant |
| **许可证** | MIT |
| **分类** | productivity / research |

---

### 功能特点

- ✅ 6 阶段文献搜索流程
- ✅ 整合多个学术搜索技能
- ✅ 4 种搜索场景
- ✅ 自动触发关键词
- ✅ 结构化输出报告

---

### 触发关键词

```
文献搜索、论文搜索、查找文献、search literature、find papers、量表搜索、文献调研
```

---

### 依赖技能

**必需**:
- tavily-search
- web_fetch
- citation-management

**可选**:
- pubmed-database
- bgpt-paper-search
- openalex-database
- research-lookup

---

## 🎯 使用示例

### 安装后使用

```bash
# 安装技能
clawhub install literature-search-workflow

# 使用技能
python skills/literature-search-workflow/scripts/literature_search.py "主观幸福感量表 validation"
```

### 在 Agent 中配置

编辑 `agents/academic-assistant/agent/config.json`:
```json
{
  "skills": [
    "literature-search-workflow",
    "tavily-search",
    "citation-management",
    ...
  ]
}
```

---

## 📝 搜索场景

### 场景 1: 学术论文搜索

```bash
python literature_search.py "主观幸福感量表 validation" --type academic_paper
```

**输出**: 论文列表 + 引用

---

### 场景 2: 量表工具搜索

```bash
python literature_search.py "SHS scale Chinese validation" --type scale_search
```

**输出**: 量表验证报告

---

### 场景 3: 综述文献搜索

```bash
python literature_search.py "AI psychology review" --type review --max-results 50
```

**输出**: 综述文献列表 (50 篇)

---

### 场景 4: 研究方法搜索

```bash
python literature_search.py "experimental design psychology" --type methodology
```

**输出**: 方法学资源列表

---

## ⚠️ 常见问题

### 问题 1: 登录失败

**错误**: `Error: Not logged in`

**解决**:
```bash
# 重新登录
clawhub login

# 检查登录状态
clawhub whoami
```

---

### 问题 2: 上传失败

**错误**: `Failed to publish skill`

**检查**:
1. 技能配置文件是否正确
2. 文件路径是否正确
3. 网络连接是否正常

**解决**:
```bash
# 验证技能配置
clawhub inspect C:\Users\13600\.openclaw\workspace\skills\literature-search-workflow

# 重新上传
clawhub publish C:\Users\13600\.openclaw\workspace\skills\literature-search-workflow
```

---

### 问题 3: 技能文件缺失

**错误**: `Missing required files`

**必需文件**:
- openclaw.skill.json
- SKILL.md

**检查**:
```bash
Get-ChildItem -Path "C:\Users\13600\.openclaw\workspace\skills\literature-search-workflow" -File
```

---

## 📞 支持资源

### ClawHub 文档

- **官网**: https://clawhub.com/
- **文档**: https://clawhub.com/docs
- **技能市场**: https://clawhub.com/skills

### 社区支持

- **Discord**: https://discord.gg/clawhub
- **GitHub**: https://github.com/clawhub

---

## 📝 上传检查清单

- [x] 技能文件已创建
- [x] 配置文件正确
- [x] 技能说明完整
- [x] 脚本可执行
- [ ] 已登录 ClawHub
- [ ] 上传成功
- [ ] 验证技能页面

---

## 🎉 上传成功后

### 分享技能

```
🔍 Literature Search Workflow Skill 已发布！

📦 技能名称：Literature Search Workflow
🔗 链接：https://clawhub.com/skills/literature-search-workflow
📝 版本：v1.0.0
👤 作者：academic-assistant

功能：标准化文献搜索工作流，整合多个学术搜索技能
```

### 推广建议

1. **ClawHub 社区**: 发布技能介绍帖
2. **社交媒体**: Twitter/X、微信公众号
3. **学术圈**: 实验室群组、学术会议

---

## 📊 技能测试结果

**测试查询**: "主观幸福感量表 validation psychometric 2025"

**测试结果**:
- ✅ 找到 10 篇相关文献
- ✅ 包含 PMC 全文链接
- ✅ 包含量表验证信息
- ✅ 响应时间：3.9 秒

**关键文献**:
1. SHS 中文版验证 (Cheung & Lucas, 2014)
2. PERMA-Profiler 中文版 (2024)
3. 心理健康价值观量表 (2025)

---

**创建时间**: 2026-03-14  
**维护者**: academic-assistant  
**下次更新**: 功能改进时

---

*祝上传顺利！*📦🚀
