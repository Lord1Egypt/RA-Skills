# 政策合规与动态学习

> 自动追踪 Apple 开发者政策变更，预警合规风险，生成合规报告。

## 政策监控器

### 监控来源
- https://developer.apple.com/news/
- https://developer.apple.com/cn/news/

### 关键政策领域

| 领域 | 说明 | 影响程度 |
|------|------|----------|
| AI/ML框架使用 | 条款3.3.11，规范AI及机器学习技术使用 | 🔴 高 |
| 敏感内容分析(Sensitive Content) | 条款3.3.3(N)，明确分析框架使用要求 | 🟡 中 |
| 未成年保护 | 审核指南1.2.1(a)，年龄分级和限制机制 | 🔴 高 |
| 出口合规 | 条款3.1，ITSAppUsesNonExemptEncryption声明 | 🟡 中 |
| 隐私标签与数据披露 | 审核指南更新，必须准确声明数据收集 | 🟡 中 |
| 4.3低质应用清理 | 禁止提交与现有内容高度相似的应用 | 🔴 高 |
| API废弃通知 | 如ImageCreator在iOS 27废弃 | 🟡 中 |

### 合规检查命令

首次构建前，调用 `scripts/policy_monitor.py`（若已实现）检查当前项目合规性，或手动检查以下项目：

1. ✅ Info.plist 包含 `ITSAppUsesNonExemptEncryption = false`
2. ✅ 隐私标签（PrivacyInfo.xcprivacy）已配置
3. ✅ 应用未使用废弃 API
4. ✅ 未使用 emoji 作为功能图标
5. ✅ 深色模式适配完成
6. ✅ 应用差异化度 ≥ 70%（避免4.3条款风险）
7. ✅ 未成年保护机制（若应用面向儿童）

### 常见政策变更响应

- **AI/ML 新条款**：确保任何 AI 生成内容明确标识，用户可控制 AI 功能开关
- **4.3 条款收紧**：为每个上架应用准备差异化说明文档
- **API 废弃**：在 Xcode 中查看废弃警告，按 deadline 迁移
- **隐私标签变更**：每次更新审核指南时重新检查 PrivacyInfo.xcprivacy
