# Skill Distill — 通用化检查清单

发布前逐项确认。全部 PASS 才可 `clawhub publish`。

## 1. 路径参数化
- [ ] 无硬编码绝对路径（系统用户目录、临时目录等）
- [ ] 无硬编码 IP 地址
- [ ] 路径通过参数或环境变量传入

## 2. 敏感信息清除
- [ ] 无 API key / token（sk-、ghp_、xoxb-、AKIA 等）
- [ ] 无 password/secret 赋值
- [ ] 无 .env 文件含真实值
- [ ] 无本地用户名引用

## 3. 依赖声明完整性
- [ ] 外部命令依赖已在 SKILL.md 或 README 中声明
- [ ] 无隐式依赖（脚本中调用但未声明的工具）
- [ ] 如有 package.json / requirements.txt，已包含且干净

## 4. 目录结构规范性
- [ ] SKILL.md 在根目录
- [ ] 脚本在 scripts/
- [ ] 参考资料在 references/
- [ ] 无 .git 目录
- [ ] 无 node_modules 目录
- [ ] 无超大文件（>1MB）

## 5. SKILL.md 质量
- [ ] frontmatter 包含 name 和 description
- [ ] Frontmatter (name, description) must be English-only — no CJK characters
- [ ] description 写清触发场景
- [ ] 工作流步骤完整可执行

## 6. 版本与元数据
- [ ] 如有版本号，已设置合理初始值
- [ ] 无调试/开发阶段残留（console.log、print debug 等）
