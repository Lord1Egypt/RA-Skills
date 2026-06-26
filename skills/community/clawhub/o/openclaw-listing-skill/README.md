# 🛒 OpenClaw 技能包：跨境电商多平台 Listing 生成器

> 输入产品图片或参数，自动生成亚马逊 / 速卖通标题、卖点、SEO关键词

---

## 📦 技能包内容

```
openclaw-listing-skill/
├── README.md                    ← 本文件
├── SKILL.md                     ← 技能完整定义
├── AGENTS_SNIPPET.md            ← 追加到 AGENTS.md 的内容
├── examples/
│   └── sample_outputs.md        ← 示例输入/输出（验收用）
└── scripts/
    └── install.sh               ← 一键部署脚本
```

---

## 🚀 部署方法

### 方法一：一键脚本（推荐）

```bash
cd openclaw-listing-skill
bash scripts/install.sh
```

### 方法二：手动部署

**第一步**：将 Agent 配置追加到 OpenClaw workspace

```bash
cat AGENTS_SNIPPET.md >> ~/.openclaw/workspace/AGENTS.md
```

**第二步**：验证追加成功

```bash
tail -50 ~/.openclaw/workspace/AGENTS.md
```

看到 `Agent: listing-generator` 字样即表示成功。

**第三步**：重启 OpenClaw 让配置生效

```bash
# 如果是 Telegram bot 模式
pkill -f openclaw
openclaw telegram  # 或你原来的启动命令
```

---

## 💬 使用方式（Telegram）

### 基础用法

```
/listing 帮我写一个无线蓝牙耳机的亚马逊listing，目标美国站，30小时续航，降噪
```

### 指定平台

```
/listing amazon [产品描述]
/listing aliexpress [产品描述]
```

### 只要关键词

```
/listing keywords 折叠宠物饮水机 美国站
```

### 图片触发

```
[发送产品图片]
/listing 亚马逊美国站，帮我写listing
```

### 优化已有标题

```
/listing rewrite "Wireless Headphones Bluetooth Over Ear"
目标市场：美国，补充：降噪30小时续航
```

---

## ⚙️ 输出内容说明

| 输出项 | 平台 | 规格 |
|--------|------|------|
| Title 标题 | 亚马逊 | ≤200字符，含核心关键词 |
| Bullet Points | 亚马逊 | 5条，每条≤255字符 |
| Description | 亚马逊 | 3-5句，支持HTML |
| Backend Keywords | 亚马逊 | 15-20个隐藏词 |
| Title 标题 | 速卖通 | ≤128字符 |
| Search Keywords | 速卖通 | 15个，分层分类 |
| Product Tags | 通用 | 10个标签 |

---

## 🧪 验收测试

部署后发送以下消息验证是否正常工作：

```
/listing
产品：主动降噪蓝牙耳机
功能：ANC降噪、30小时续航、蓝牙5.3
目标市场：亚马逊美国站
价格：$35-$50
```

对照 `examples/sample_outputs.md` 检查输出质量。

---

## 🔧 常见问题

**Q: Agent 没有被触发？**
A: 检查 `~/.openclaw/workspace/AGENTS.md` 是否包含 `listing-generator` 内容，确认已重启 OpenClaw。

**Q: 输出语言不对？**
A: 默认输出英文。如需中文，在请求末尾加上"用中文输出"。

**Q: 图片识别失败？**
A: 确认你的 OpenClaw 使用的模型支持多模态（Vision）。Kimi K2.5 支持图片输入，Moonshot API 需确认 `moonshot-v1-8k-vision` 或对应 vision 模型已启用。

---

## 📈 后续扩展方向

- [ ] 接入 Jungle Scout API，自动获取竞品关键词数据
- [ ] 支持批量生成（CSV 导入多个产品）
- [ ] 生成 A+ 页面文案模块
- [ ] 多语言版本（德/法/西/日/阿拉伯语）
- [ ] 违禁词自动检测（亚马逊合规检查）
