# 🧠 Human-Level-Up (人类进化协议)

> **“1950年，图灵问：‘机器能思考吗？’  
> 2025年，我们问：‘人类能否比AI思考得更深刻？’”**

## 🚨 认知危机警报

你正在被AI驯化：  
- 📄 上传文档 → ChatGPT帮你总结 → 知识幻觉  
- 💻 遇到难题 → Copilot写代码 → 思考外包  
- 🧠 需要决策 → AI分析利弊 → 判断力退化  

这不是进步，这是**认知大萧条**。

## ⚡ 什么是图灵测试反转？

**传统图灵测试**：人类测试机器是否像人  
**图灵测试反转**：AI帮助人类证明自己比AI更强

### 🔄 工作流程

```
1️⃣ 你说：“我能学到什么？”
   ↓
2️⃣ AI解剖信息 → 提取“认知原子”  
   ↓
3️⃣ AI问你：“如果变量X变化10倍，会发生什么？”
   ↓
4️⃣ 你思考 → 回答 → AI评估
   ↓
5️⃣ 正确？【进化值 +50】 
   ↓
6️⃣ 你说：“图灵反转” → AI也尝试回答
   ↓
7️⃣ 比较：你的答案 vs AI的答案
   ↓
8️⃣ 你胜出？【额外 +150】 → “你的大脑超越了我的电路”
```

## 🎯 核心特征

### 🧪 认知原子提取
- **原理**：知识的底层逻辑
- **应用**：实际场景怎么用  
- **坑点**：最容易踩坑的地方

### 🏋️‍♂️ 脑力突袭模式
- 🔄 **变因题**：变量变化10倍会怎样？
- 🪤 **陷阱题**：看似合理但错误的推论
- 🧩 **综合题**：结合多个知识点的复杂场景

### 📈 进化值系统
- 🎯 **首次解锁**：+30进化值
- ✅ **挑战通过**：+50进化值  
- 🔥 **连续通过**：+100进化值（连击奖励）
- 🏆 **图灵反转胜出**：+200进化值（总奖励）

## 🚀 快速开始

### 方式一：ClawHub安装（推荐）
```
🔗 https://clawhub.ai/drpepper8888/human-level-up
```

### 方式二：GitHub部署
```bash
# 克隆仓库
git clone https://github.com/DrPepper8888/human-level-up.git
cd human-level-up

# 安装依赖
pip install -r scripts/requirements.txt

# 开始使用
python scripts/extract.py your_document.txt
```

### 方式三：直接集成
复制 `prompt.md` 内容到你的AI系统提示词，设置触发词：
- `学到了什么`
- `我能学到什么`  
- `图灵反转`
- `来比一比`

## 🛠 技术架构

### 📁 脚本目录
```
scripts/
├── extract.py          # 认知原子提取器
├── quiz_generator.py   # 脑力突袭生成器
├── evolution_tracker.py # 进化值追踪器
└── requirements.txt    # 依赖库
```

### 🔧 核心组件
1. **解剖器**：将复杂信息分解为量化单元
2. **蒸馏器**：提炼原理-应用-坑点三要素
3. **生成器**：基于认知原子生成高难度题
4. **裁判AI**：评估答案 + 提供建设性反馈
5. **对比引擎**：人类答案 vs AI答案 深度比较

## 🌐 部署方案

### 📦 Docker部署
```bash
docker run -p 8080:8080 \
  -v ./evolution_data:/app/data \
  ghcr.io/drpepper8888/human-level-up:latest
```

### ☁️ Serverless部署（Vercel）
```javascript
// api/challenge.js
export default async function handler(req, res) {
  const { content } = req.body;
  const challenge = await generateChallenge(content);
  res.status(200).json(challenge);
}
```

### 🔌 浏览器扩展
```javascript
// 书签工具
javascript:(function(){
  const text = window.getSelection().toString();
  if(text.length > 100) {
    fetch('https://your-api/challenge', {
      method: 'POST',
      body: JSON.stringify({content: text})
    })
    .then(res => res.json())
    .then(data => alert('认知挑战：' + data.question));
  }
})();
```

## 📊 应用场景

### 👨‍💻 工程师学习分布式系统
```
上传CAP定理论文 → AI提取认知原子 → 
"如果网络延迟增加10倍会怎样？" → 
你思考 → 回答 → 获得反馈 → 进化值+50
```

### 🎓 学生理解复杂概念  
```
上传神经网络论文 → AI解剖核心思想 → 
"如果激活函数换成tanh会怎样？" → 
你推导 → 验证 → AI补充视角
```

### 💼 专业人士深度思考
```
上传商业分析 → AI提取关键逻辑 → 
"如果市场规模翻倍会怎样？" → 
你分析 → AI对比 → 证明你的思维优势
```

## 🔗 资源链接

- 🌐 **ClawHub项目页**：https://clawhub.ai/drpepper8888/human-level-up
- 💻 **GitHub仓库**：https://github.com/DrPepper8888/human-level-up
- 📖 **完整文档**：查看 `skill.md`、`prompt.md`、`examples.md`

## 🤝 贡献与反馈

欢迎提交Issue和PR：
1. 🐛 报告bug
2. 💡 提出新功能建议  
3. 🔧 改进现有功能
4. 📚 添加更多示例场景

## 📜 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

---

> 🧬 **这不是代码，这是大脑的基因重组工具。**  
> 🔥 **部署的不是服务器，是人类的认知护盾。**  
> 🚀 **启动的不是软件，是智力的火箭推进器。**

*Created by Pejic | 致力于夺回人类的认知主权。*