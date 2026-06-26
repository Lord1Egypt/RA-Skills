# Hermes 系统版本管理

## 📋 版本管理策略

### 版本号规范
采用 [语义化版本](https://semver.org/lang/zh-CN/) 2.0.0 规范：`主版本号.次版本号.修订号`

- **主版本号 (MAJOR)**: 不兼容的 API 修改
- **次版本号 (MINOR)**: 向下兼容的功能性新增
- **修订号 (PATCH)**: 向下兼容的问题修正

**预发布版本**: `主版本号.次版本号.修订号-预发布标识.构建号`
- 示例: `1.0.0-alpha.1`, `1.0.0-beta.2`, `1.0.0-rc.1`

**构建元数据**: `主版本号.次版本号.修订号+构建元数据`
- 示例: `1.0.0+20240423.093000`, `1.0.0+sha.7c6d634`

### 版本生命周期

```
开发阶段 (Development)
    ↓
Alpha 测试 (内部测试)
    ↓
Beta 测试 (公开测试)  
    ↓
发布候选 (Release Candidate)
    ↓
正式发布 (Stable Release)
    ↓
维护阶段 (Maintenance)
    ↓
终止支持 (End of Life)
```

### 版本支持策略

| 版本系列 | 状态 | 开始日期 | 结束支持 | 安全更新 | 功能更新 |
|----------|------|----------|----------|----------|----------|
| 2.x.x | 规划中 | - | - | - | - |
| 1.x.x | 开发中 | 2026-04-22 | 2026-10-22 | ✅ | ✅ |
| 1.0.x | 稳定版 | 2026-04-23 | 2026-07-23 | ✅ | ⚠️ 仅关键 |
| 0.x.x | 实验版 | - | - | ❌ | ❌ |

## 🏷️ 版本标签

### Git 标签规范
```bash
# 正式版本
git tag -a v1.0.0 -m "Release v1.0.0: Initial release"

# 预发布版本
git tag -a v1.0.0-rc.1 -m "Release Candidate v1.0.0-rc.1"

# 带构建元数据
git tag -a v1.0.0+build.123 -m "Build 123"
```

### 分支策略
```
main (保护分支)
    ↑
release/v1.0.x (发布分支)
    ↑
develop (开发分支)
    ↑
feature/* (功能分支)
bugfix/* (修复分支)
hotfix/* (热修复分支)
```

## 📦 发布流程

### 阶段1: 发布准备 (1-2天)
```bash
# 1. 更新版本号
echo "1.0.0" > VERSION

# 2. 更新变更日志
vim CHANGELOG.md

# 3. 更新依赖
pip freeze > requirements.txt

# 4. 运行完整测试
./scripts/test-all.sh

# 5. 构建发布包
./scripts/build-release.sh
```

### 阶段2: Alpha 发布 (内部测试)
```bash
# 创建 Alpha 标签
git tag -a v1.0.0-alpha.1 -m "Alpha release v1.0.0-alpha.1"

# 推送到仓库
git push origin v1.0.0-alpha.1

# 创建 GitHub Release
gh release create v1.0.0-alpha.1 \
  --title "Hermes System v1.0.0 Alpha 1" \
  --notes-file CHANGELOG.md \
  --prerelease \
  dist/hermes-system-1.0.0-alpha.1.tar.gz
```

### 阶段3: Beta 发布 (公开测试)
```bash
# 创建 Beta 标签
git tag -a v1.0.0-beta.1 -m "Beta release v1.0.0-beta.1"

# 推送到仓库
git push origin v1.0.0-beta.1

# 创建 GitHub Release
gh release create v1.0.0-beta.1 \
  --title "Hermes System v1.0.0 Beta 1" \
  --notes-file CHANGELOG.md \
  --prerelease \
  dist/hermes-system-1.0.0-beta.1.tar.gz
```

### 阶段4: 发布候选 (RC)
```bash
# 创建 RC 标签
git tag -a v1.0.0-rc.1 -m "Release Candidate v1.0.0-rc.1"

# 推送到仓库
git push origin v1.0.0-rc.1

# 创建 GitHub Release
gh release create v1.0.0-rc.1 \
  --title "Hermes System v1.0.0 Release Candidate 1" \
  --notes-file CHANGELOG.md \
  --prerelease \
  dist/hermes-system-1.0.0-rc.1.tar.gz
```

### 阶段5: 正式发布
```bash
# 创建正式版本标签
git tag -a v1.0.0 -m "Release v1.0.0"

# 推送到仓库
git push origin v1.0.0

# 创建 GitHub Release
gh release create v1.0.0 \
  --title "Hermes System v1.0.0" \
  --notes-file CHANGELOG.md \
  dist/hermes-system-1.0.0.tar.gz

# 合并到主分支
git checkout main
git merge --no-ff release/v1.0.0
git push origin main
```

### 阶段6: 发布后维护
```bash
# 创建维护分支
git checkout -b maintenance/v1.0.x

# 应用热修复
git checkout -b hotfix/critical-bug
# ... 修复代码 ...
git checkout maintenance/v1.0.x
git merge --no-ff hotfix/critical-bug

# 发布补丁版本
git tag -a v1.0.1 -m "Patch release v1.0.1"
git push origin v1.0.1
```

## 📝 变更日志规范

### 文件结构
```
CHANGELOG.md
├── [版本号] - YYYY-MM-DD
│   ├### 新增
│   ├### 变更
│   ├### 修复
│   └### 移除
└── [版本号] - YYYY-MM-DD
    └── ...
```

### 变更类型
- **新增 (Added)**: 新功能
- **变更 (Changed)**: 现有功能变更
- **弃用 (Deprecated)**: 即将移除的功能
- **移除 (Removed)**: 已移除的功能
- **修复 (Fixed)**: bug 修复
- **安全 (Security)**: 安全相关更新

### 示例
```markdown
## [1.0.0] - 2026-04-23

### 新增
- 记忆系统: 跨会话记忆持久化
- Skill生成系统: 任务轨迹分析 → Skill候选生成
- 兼容性层: 与 OpenClaw 现有体系集成
- 性能监控: 健康度评分和性能基准

### 变更
- 重构记忆管理器接口，提高性能
- 优化 Skill 模板生成算法

### 修复
- 修复记忆预取中的中文分词问题
- 修复配置热更新不生效的问题

### 已知问题
- 嵌入模型 API 在某些环境下不可用
- 大规模记忆文件加载可能较慢
```

## 🔄 版本升级指南

### 自动升级
```bash
# 检查可用升级
./bin/hermes-check-updates

# 执行升级
./bin/hermes-upgrade

# 指定版本升级
./bin/hermes-upgrade --version 1.1.0
```

### 手动升级步骤

#### 从 0.x 升级到 1.0.0
```bash
# 1. 备份数据
./scripts/backup.sh --full

# 2. 停止服务
./bin/hermes-stop

# 3. 下载新版本
wget https://github.com/your-org/hermes-system/releases/download/v1.0.0/hermes-system-1.0.0.tar.gz

# 4. 解压
tar -xzf hermes-system-1.0.0.tar.gz
cd hermes-system-1.0.0

# 5. 运行迁移脚本
./bin/hermes-migrate --from 0.9.0 --to 1.0.0

# 6. 更新配置
cp config/hermes.yaml.example config/hermes.yaml
# 编辑配置，应用新功能

# 7. 启动服务
./bin/hermes-start

# 8. 验证升级
./bin/hermes-validate-upgrade
```

#### 从 1.0.x 升级到 1.1.0
```bash
# 1. 查看升级说明
cat docs/UPGRADE_1.1.0.md

# 2. 备份配置
cp config/hermes.yaml config/hermes.yaml.backup

# 3. 执行标准升级流程
./bin/hermes-upgrade --version 1.1.0

# 4. 合并配置变更
# 手动合并 config/hermes.yaml 和 config/hermes.yaml.new
```

### 降级流程
```bash
# 1. 停止服务
./bin/hermes-stop

# 2. 备份当前版本
./scripts/backup.sh --version=$(cat VERSION)

# 3. 下载旧版本
wget https://github.com/your-org/hermes-system/releases/download/v1.0.0/hermes-system-1.0.0.tar.gz

# 4. 恢复数据
./bin/hermes-restore --backup=backups/20240423_093000

# 5. 启动旧版本
./bin/hermes-start
```

## 📊 版本兼容性矩阵

### Hermes 与 OpenClaw 兼容性
| Hermes 版本 | OpenClaw 版本 | 状态 | 备注 |
|-------------|---------------|------|------|
| 1.0.x | 2026.4.15+ | ✅ 完全兼容 | 推荐组合 |
| 1.0.x | 2026.4.1-2026.4.14 | ⚠️ 部分兼容 | 某些功能受限 |
| 1.0.x | < 2026.4.1 | ❌ 不兼容 | 需要升级 OpenClaw |
| 0.9.x | 2026.3.x | ⚠️ 部分兼容 | 已弃用 |

### Python 版本兼容性
| Hermes 版本 | Python 3.9 | Python 3.10 | Python 3.11 | Python 3.12 |
|-------------|------------|-------------|-------------|-------------|
| 1.0.x | ✅ | ✅ | ✅ | ⚠️ 测试中 |
| 0.9.x | ✅ | ✅ | ⚠️ | ❌ |

### 操作系统兼容性
| Hermes 版本 | macOS | Linux | Windows (WSL) | Windows (原生) |
|-------------|-------|-------|---------------|----------------|
| 1.0.x | ✅ | ✅ | ✅ | ⚠️ 测试中 |
| 0.9.x | ✅ | ✅ | ⚠️ | ❌ |

## 🛡️ 安全更新策略

### 安全响应流程
1. **报告接收** - 通过安全邮箱接收漏洞报告
2. **评估分类** - 评估漏洞严重程度 (CVSS 评分)
3. **修复开发** - 开发安全补丁
4. **测试验证** - 验证修复不影响功能
5. **发布更新** - 发布安全更新版本
6. **公告发布** - 发布安全公告

### 安全版本支持
- **关键安全更新**: 所有受支持版本
- **重要安全更新**: 当前版本和上一个版本
- **一般安全更新**: 仅当前版本

### 安全公告格式
```markdown
## 安全公告: HERMES-SA-2026-001

**影响版本**: 1.0.0 - 1.0.2
**修复版本**: 1.0.3
**严重程度**: 高 (CVSS: 7.5)
**CVE 编号**: CVE-2026-XXXXX

### 描述
记忆系统存在授权绕过漏洞...

### 影响
攻击者可能... 

### 解决方案
升级到版本 1.0.3 或应用补丁...

### 致谢
感谢 [报告者] 报告此漏洞
```

## 📈 版本指标监控

### 发布质量指标
- **测试覆盖率**: ≥ 80%
- **代码重复率**: ≤ 5%
- **技术债务比率**: ≤ 10%
- **缺陷密度**: ≤ 0.5 缺陷/KLOC

### 版本健康指标
- **采用率**: 新版本用户占比
- **升级成功率**: 成功升级用户占比
- **回滚率**: 升级后回滚用户占比
- **用户满意度**: NPS 评分

### 监控仪表板
```bash
# 生成版本报告
./bin/hermes-version-report --format=json --output=version_report.json

# 包含指标:
# - 版本分布
# - 升级成功率
# - 缺陷统计
# - 性能对比
```

## 🔧 工具与自动化

### 版本管理工具
```bash
# 版本检查
./bin/hermes-version

# 升级检查
./bin/hermes-check-updates

# 自动升级
./bin/hermes-auto-upgrade --schedule="weekly"

# 版本清理
./bin/hermes-cleanup-versions --keep=5
```

### CI/CD 集成
```yaml
# .github/workflows/release.yml
name: Release

on:
  push:
    tags:
      - 'v*'

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.9'
          
      - name: Install dependencies
        run: pip install -r requirements.txt
        
      - name: Run tests
        run: ./scripts/test-all.sh
        
      - name: Build package
        run: ./scripts/build-release.sh
        
      - name: Create Release
        uses: softprops/action-gh-release@v1
        with:
          files: dist/*
```

## 📚 文档版本管理

### 文档版本化
```
docs/
├── v1.0/          # 版本 1.0 文档
│   ├── README.md
│   ├── INSTALL.md
│   └── API.md
├── v1.1/          # 版本 1.1 文档
│   └── ...
└── latest/        # 最新版本文档 (符号链接)
    └── -> v1.0/
```

### 文档更新流程
1. **新功能文档**: 随功能开发编写
2. **API 文档**: 随 API 变更更新
3. **用户指南**: 版本发布前更新
4. **迁移指南**: 不兼容变更时编写

## 🎯 版本发布检查清单

### 发布前检查
- [ ] 所有测试通过
- [ ] 文档完整且准确
- [ ] 变更日志已更新
- [ ] 版本号已更新
- [ ] 依赖已更新
- [ ] 构建脚本工作正常
- [ ] 发布说明已编写

### 发布中检查
- [ ] 标签已创建并推送
- [ ] 发布包已构建
- [ ] GitHub Release 已创建
- [ ] 下载链接有效
- [ ] 签名验证通过

### 发布后检查
- [ ] 公告已发布
- [ ] 用户已通知
- [ ] 监控已就绪
- [ ] 支持团队已培训
- [ ] 回滚计划已准备

## 📞 版本支持

### 支持渠道
- **社区支持**: GitHub Discussions
- **问题报告**: GitHub Issues
- **安全报告**: security@example.com
- **商业支持**: support@example.com

### 支持时效
- **关键问题**: 24小时内响应
- **重要问题**: 3个工作日内响应
- **一般问题**: 7个工作日内响应
- **功能请求**: 下一个版本规划

### 终止支持流程
1. **公告**: 提前6个月发布终止支持公告
2. **迁移**: 提供迁移指南和支持
3. **归档**: 代码归档到只读仓库
4. **通知**: 最终终止支持通知

---

**版本管理文档版本**: 1.0  
**最后更新**: 2026-04-23 09:58  
**适用版本**: Hermes System 1.0.0+