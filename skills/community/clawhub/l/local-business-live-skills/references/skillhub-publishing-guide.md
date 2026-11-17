# SkillHub 发布踩坑记录

## 前置条件

- 已注册 SkillHub 账号
- 已通过 `skillhub login --key skh_xxx` 登录

## SKILL.md 必须字段

```
slug: <唯一标识符>          # 必须，不能重复
displayName: <显示名称>     # 必须，展示在搜索结果中
```

缺少这两个字段 → `Error: SKILL.md 缺少 slug / displayName`

## 发布方式

### 方式1：从目录发布（推荐）
```bash
skillhub publish /path/to/skill-dir --version 1.0.0 --changelog "变更说明"
```
要求目录下有 SKILL.md。

### 方式2：从 zip 发布
上传压缩包到网页端。zip 内必须包含 SKILL.md。

## 不允许的文件类型

SkillHub 拒绝以下文件：
- `.bat` / `.exe` / `.msix`（Windows 可执行文件）
- `.zip`（不能嵌套压缩包）
- `.gitignore` / `.gitattributes`
- `.git/` 目录

**解决方法：** 发布前从目录中删除这些文件，或从临时目录发布：
```bash
rm -rf /tmp/publish-temp && mkdir -p /tmp/publish-temp
cp -r source-dir/* /tmp/publish-temp/
rm -rf /tmp/publish-temp/.git /tmp/publish-temp/*.zip /tmp/publish-temp/*.bat
skillhub publish /tmp/publish-temp
```

## 版本冲突

```bash
Error: slug 冲突: 版本 X.Y.Z 已存在，请使用新的版本号发布
```
每次发布新版本必须升版本号。SkillHub 不允许覆盖已有版本。

## 参赛选项

CLI 发布不支持勾选「参加大赛」。如需参赛：
1. 用 CLI 发布为草稿或低版本
2. 在 SkillHub 网页端重新上传 zip，勾选参赛框
3. 或者 CLI 发布后，在网页端找「编辑」入口

## 审核

- 发布后 `status=None` 表示待审核
- 审核通过后才能在搜索结果中显示
- 包含个人联系方式（微信/电话）会被拒绝
