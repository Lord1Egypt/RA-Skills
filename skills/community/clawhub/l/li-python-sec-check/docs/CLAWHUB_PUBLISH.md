# ClawHub 发布指南

## 发布前准备

### 1. 检查文件完整性

确保以下文件存在：

```
Li_python_sec_check/
├── SKILL.md              ✅ 必需
├── README.md             ✅ 必需
├── _meta.json           ✅ 必需
├── package.json         ✅ 推荐
├── LICENSE              ✅ 推荐
├── requirements.txt     ✅ 必需
├── scripts/
│   └── python_sec_check.py  ✅ 必需
├── docs/
│   └── USAGE.md         ✅ 推荐
└── examples/            ✅ 推荐
```

### 2. 更新版本

编辑 `_meta.json` 和 `SKILL.md` 中的版本号：

```json
{
  "version": "2.0.0"
}
```

### 3. 测试技能

```bash
# 运行测试
cd Li_python_sec_check
bash test.sh

# 验证功能
python scripts/python_sec_check.py examples/unsafe-example
```

## 发布到 ClawHub

### 方式 1: 使用 clawhub CLI

```bash
# 安装 clawhub
npm install -g clawhub

# 登录
clawhub login

# 发布技能
cd /root/.openclaw/workspace/skills/Li_python_sec_check
clawhub publish
```

### 方式 2: 手动发布

1. 打包技能
```bash
cd /root/.openclaw/workspace/skills
tar -czf Li_python_sec_check.tar.gz Li_python_sec_check/
```

2. 上传到 ClawHub
   - 访问 https://clawhub.com
   - 创建新技能
   - 上传压缩包
   - 填写元数据

### 方式 3: GitHub 发布

```bash
# 提交到 Git
cd Li_python_sec_check
git add .
git commit -m "Release v2.0.0"
git tag v2.0.0
git push origin main --tags

# 在 ClawHub 中关联 GitHub 仓库
```

## 发布后验证

### 1. 搜索技能

```bash
clawhub search Li_python_sec_check
```

### 2. 安装测试

```bash
# 在新环境中安装
clawhub install Li_python_sec_check

# 验证安装
cd ~/.openclaw/skills/Li_python_sec_check
python scripts/python_sec_check.py --help
```

### 3. 检查页面

访问 ClawHub 技能页面，确认：
- ✅ 描述正确
- ✅ 版本号正确
- ✅ 文档完整
- ✅ 示例代码可运行

## 版本更新

### 更新流程

1. 修改代码
2. 更新 `_meta.json` 版本号
3. 更新 `SKILL.md` 版本号
4. 更新 `CHANGELOG.md`（如有）
5. 提交并打标签
6. 重新发布

### 版本号规范

遵循语义化版本 (SemVer):

- `MAJOR.MINOR.PATCH` (例如：2.0.0)
- MAJOR: 不兼容的变更
- MINOR: 向后兼容的功能
- PATCH: 向后兼容的修复

## 常见问题

### Q: 发布失败？
A: 检查网络连接、认证信息、文件大小

### Q: 技能搜索不到？
A: 等待索引更新（通常 5-10 分钟）

### Q: 如何撤回发布？
A: 联系 ClawHub 管理员或在控制台下架

---

**最后更新**: 2026-03-21  
**版本**: 2.0.0
