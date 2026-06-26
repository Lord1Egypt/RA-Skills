# 📦 健康管理技能 v1.0 依赖说明

## 一、一键安装

### 🇨🇳 中国大陆（推荐用镜像）

```bash
# 1. 设置镜像环境变量
export OPENCLAW_MIRROR=https://mirror-cn.clawhub.com

# 2. 安装 Skills（用镜像）
openclaw skills install autoglm-browser-agent
openclaw skills install autoglm-image-recognition
openclaw skills install feishu-doc
openclaw skills install feishu-im-read

# 3. 安装 Python 依赖（用清华镜像）
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### 🌏 海外

```bash
# 安装 Skills
openclaw skills install autoglm-browser-agent
openclaw skills install autoglm-image-recognition
openclaw skills install feishu-doc
openclaw skills install feishu-im-read

# 安装 Python 依赖
pip install -r requirements.txt
```

---

## 二、镜像地址

| 类型 | 中国大陆 | 海外 |
|------|----------|------|
| ClawHub | mirror-cn.clawhub.com | clawhub.com |
| PyPI | pypi.tuna.tsinghua.edu.cn | pypi.org |

---

## 三、依赖的 Skills

| Skill | 用途 |
|-------|------|
| autoglm-browser-agent | 搜B站视频 |
| autoglm-image-recognition | 图片OCR |
| feishu-doc | 飞书文档 |
| feishu-im-read | 消息读取 |

---

## 四、Python 依赖

详见 `requirements.txt`

```bash
# 中国大陆
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# 海外
pip install -r requirements.txt
```

---

## 五、飞书应用配置

1. 创建应用：https://open.feishu.cn/
2. 开通权限：im:message:send_as_user, docs:write, docs:read
3. 安装到工作区

---

*2026-04-04*
