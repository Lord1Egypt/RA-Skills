# Contributing to Layered Memory

感谢您考虑为 Layered Memory 技能做贡献！

## 如何贡献

### 报告 Bug
1. 在 GitHub Issues 中搜索是否已存在相关问题
2. 如果没有，创建新 Issue，包含：
   - 复现步骤
   - 预期行为
   - 实际行为
   - 环境信息（OpenClaw 版本、Node 版本）

### 提交 Pull Request
1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

### 开发规范
- 遵循现有代码风格
- 添加测试覆盖新功能
- 更新文档（README, CHANGELOG）
- 确保 `npm test` 通过

### 运行测试
```bash
npm test
```

### 性能基准测试
```bash
npm run benchmark
```

## 版本管理
- 主版本：不兼容的 API 修改
- 次版本：向下兼容的功能新增
- 修订版本：向下兼容的问题修复

## 行为准则
- 尊重所有贡献者
- 接受建设性反馈
- 聚焦于技术讨论

---
