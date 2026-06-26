# Method Dev Agent 发布指南

## 🚀 一键发布

### Windows用户
```bash
双击运行: publish.bat
```

### Mac/Linux用户
```bash
chmod +x publish.sh
./publish.sh
```

## 📋 发布前检查清单

- [ ] GitHub仓库已创建: https://github.com/teagec/t2
- [ ] 已登录ClawHub: `clawhub login`
- [ ] 所有代码已提交到Git
- [ ] skill.json信息完整
- [ ] CLAWHUB_README.md已更新

## 📝 手动发布步骤

如果一键脚本失败，手动执行:

```bash
# 1. 推送代码到GitHub
git add .
git commit -m "v0.1.0 release"
git push origin main

# 2. 发布到ClawHub
clawhub publish . \
  --slug method-dev-agent \
  --name "药品分析色谱方法开发助手" \
  --version 0.1.0 \
  --changelog "MVP: 实验记录、方法库、基础分析、专业版0.03 ETH/月"
```

## 🔗 发布后的链接

- GitHub: https://github.com/teagec/t2
- ClawHub: https://clawhub.ai/teagec/method-dev-agent

## ⚠️ 常见问题

**Q: 提示"Not logged in"**
A: 先运行 `clawhub login` 完成授权

**Q: GitHub推送失败**
A: 检查GitHub仓库是否已创建，是否有推送权限

**Q: ClawHub发布失败**
A: 检查skill.json格式是否正确，必填字段是否完整

## 📞 联系信息

- 作者: Teagee Li
- 邮箱: teagee@qq.com
- GitHub: https://github.com/teagec/t2
