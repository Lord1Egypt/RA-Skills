# 📱 ios-self-improve

**iOS 开发者自改进技能** - 依赖 developer-self-improve-core 安全闭环

---

## ⚠️ 重要：安装顺序

**必须先安装核心技能：**

```bash
# 1. 先安装核心技能
clawhub install developer-self-improve-core

# 2. 再安装 iOS 技能
clawhub install ios-self-improve
```

**为什么？**
- 此技能是平台扩展，需要核心技能提供基础功能
- 核心技能提供：规则生成、记忆管理、平台配置
- 此技能提供：iOS 专属自检、iOS 规则模板

---

## 🎯 功能

### iOS 专属自检

- ✅ 崩溃风险检测（数组越界、空指针、循环引用）
- ✅ 导航栏配置检查
- ✅ Info.plist 隐私权限检查
- ✅ AutoLayout 约束检查
- ✅ SwiftUI 生命周期检查
- ✅ 异步代码检查
- ✅ 沙盒读写检查
- ✅ 代码风格检查
- ✅ 暗黑模式适配检查
- ✅ 应用生命周期检查

### 平台隔离

- 仅在 `platform=ios` 或 `platform=multi-platform` 时激活
- 其他平台自动禁用，避免冲突

---

## 🔐 安全特性

### 只读操作

- ✅ 仅读取配置文件
- ✅ 不修改任何文件
- ✅ 不执行外部代码
- ✅ 无网络访问

### 人类终审

- ✅ 所有规则变更需用户确认
- ✅ AI 只提议，不自动写入
- ✅ 所有操作可追溯、可回滚

### 依赖透明

- ✅ 依赖在 `.clawhub.json` 中声明
- ✅ 依赖关系在文档中说明
- ✅ 依赖代码可审计（开源）

---

## 📋 依赖说明

**依赖：** developer-self-improve-core

**用途：**
1. 规则草案生成
2. 规则确认工作流
3. 平台配置管理

**信任模型：**
- 同一作者（lijiujiu）
- 相同安全标准
- 只读访问配置
- 开源可审计

详见：`TRUST_MODEL.md`

---

## 🚀 使用

### 初始化

```bash
./scripts/ios-self-improve.sh init
```

### iOS 自检

```bash
./scripts/ios-self-improve.sh self-check "代码内容"
```

### 示例

```bash
# 检查循环引用
./scripts/ios-self-improve.sh self-check "self.completionHandler = { self.updateUI() }"

# 输出：
# 🔴 发现崩溃风险：
# ⚠️  闭包内使用 self 未加 [weak self]
```

---

## 📖 文档

- [SKILL.md](SKILL.md) - 完整技能说明
- [SECURITY.md](SECURITY.md) - 安全信息
- [TRUST_MODEL.md](TRUST_MODEL.md) - 依赖信任模型
- [DEPENDENCY_EXPLANATION.md](DEPENDENCY_EXPLANATION.md) - 依赖说明
- [SUBMISSION_NOTE.md](SUBMISSION_NOTE.md) - ClawHub 提交说明

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

**作者：** lijiujiu  
**许可证：** MIT

---

## 📄 许可证

MIT License
