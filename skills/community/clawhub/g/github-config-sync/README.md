# GitHub配置同步

在Mac和Windows之间同步Hermes配置。

## 两种模式

### 模式A：上传（Mac → GitHub）

```bash
cd ~/hermes-sync
git pull
cp ~/.hermes/config.yaml .
cp -r ~/.hermes/memories .
cp -r ~/.hermes/skills .
git add .
git commit -m "更新配置"
git push
```

### 模式B：下载（GitHub → Windows）

```bash
cd ~/hermes-sync
git pull
cp config.yaml ~/.hermes/config.yaml
cp -r memories/* ~/.hermes/memories/
cp -r skills/* ~/.hermes/skills/
hermes restart
```

## 第一次设置

1. 安装GitHub CLI: `brew install gh` (Mac) 或 `winget install GitHub.cli` (Windows)
2. 登录: `gh auth login`
3. 克隆: `git clone https://github.com/zhangwenhao66/hermes-config.git ~/hermes-sync`

## 更多信息

见 SKILL.md