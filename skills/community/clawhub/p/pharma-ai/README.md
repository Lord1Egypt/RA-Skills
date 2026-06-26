# PharmaAI Skill

智能药物发现AI助手 - OpenClaw Agent Skill

## 安装

```bash
# 安装Node.js依赖
npm install

# 安装Python依赖
pip install -r python-core/requirements.txt

# 编译TypeScript
npm run build
```

## 使用

```typescript
import { predictMolecule } from 'pharma-ai';

const result = await predictMolecule('CC(C)Cc1ccc(cc1)C(C)C(=O)O');
console.log(result.toxicity.hERG.risk); // 'Low'
```

## 文件结构

```
pharma-ai/
├── SKILL.md                 # Skill定义
├── package.json             # Node.js配置
├── tsconfig.json            # TypeScript配置
├── src/                     # Node.js源代码
│   ├── index.ts            # 主入口
│   ├── commands/           # 命令实现
│   ├── python-bridge/      # Python桥接层
│   └── types/              # 类型定义
└── python-core/            # Python核心
    ├── predict.py          # 预测脚本
    ├── requirements.txt    # Python依赖
    └── models/             # 预训练模型
        ├── herg_model.pkl
        ├── hepatotoxicity_model.pkl
        └── ames_model.pkl
```

## 架构

```
User Request
    ↓
OpenClaw Agent
    ↓
pharma-ai Skill (Node.js)
    ↓ [子进程调用]
Python Core (RDKit + scikit-learn)
    ↓
Return Result
```

## 模型性能

- hERG: ROC-AUC 0.852
- 肝毒性: ROC-AUC 1.000
- Ames: ROC-AUC 1.000

## License

MIT
