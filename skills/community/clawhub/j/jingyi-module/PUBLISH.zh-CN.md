# 上架 ClawHub 步骤

## 1. 准备

- 确保目录里至少有：
  - `SKILL.md`
  - `manifest.yaml`
  - `README.md`
- 本技能已经包含：
  - 检索索引 `data/command_index.jsonl`
  - 搜索脚本 `scripts/search_jingyi.py`
  - 文档抓取脚本 `scripts/fetch_jingyi_doc.py`

## 2. 本地测试

```powershell
python .\scripts\build_command_index.py
python .\scripts\fetch_jingyi_doc.py --name "文本_取随机汉字"
```

## 3. 创建 GitHub 仓库

建议仓库名：

```text
jingyi-module-skill
```

初始化并推送：

```powershell
git init
git add .
git commit -m "init jingyi-module skill"
git branch -M main
git remote add origin 你的仓库地址
git push -u origin main
```

## 4. 安装 ClawHub CLI

```powershell
npm i -g clawhub
```

## 5. 登录

```powershell
clawhub login
```

## 6. 先做 dry-run

```powershell
clawhub publish . --slug jingyi-module --name "Jingyi Module" --version 0.1.0 --tags latest --dry-run
```

## 7. 正式发布

```powershell
clawhub publish . --slug jingyi-module --name "Jingyi Module" --version 0.1.0 --tags latest
```

## 8. 后续更新

版本号递增后重新发布：

```powershell
clawhub publish . --slug jingyi-module --name "Jingyi Module" --version 0.1.1 --tags latest --changelog "improve search and docs fetch"
```

## 9. 用户安装

```powershell
clawhub install jingyi-module
```

或：

```powershell
openclaw skills install jingyi-module
```
