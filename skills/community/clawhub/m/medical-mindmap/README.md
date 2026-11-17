# Medical Mindmap 医学知识图谱

神经病学/脑电图知识图谱系统，适合医学学习和管理。

## 功能特点

- **实体管理**：支持疾病、检查、症状、药物、解剖、波形等医学实体
- **关系管理**：建立实体间的关联（如疾病→检查、症状→病因）
- **脑电图输出模板**：自动输出六要素格式
  - 核心要点
  - 对比
  - 临床意义
  - 鉴别诊断价值
  - 异常提示
  - 本质总结

## 支持的实体类型

| 类型 | 说明 |
|------|------|
| Disease | 疾病 |
| Examination | 检查 |
| Symptom | 症状 |
| Medication | 药物 |
| Anatomy | 解剖结构 |
| Syndrome | 综合征 |
| Waveform | 脑电图波形 |

## 安装

### 方式一：ClawHub（推荐）

```bash
npx clawhub@latest install medical-mindmap
```

### 方式二：手动安装

```bash
# 克隆仓库
git clone https://github.com/your-github/medical-mindmap.git
# 复制到OpenClaw skills目录
cp -r medical-mindmap ~/.openclaw/workspace/skills/
```

## 使用方法

### 命令行

```bash
# 创建实体
python3 scripts/mindmap.py create Waveform --name "α波" --frequency "8-13Hz"

# 添加事实
python3 scripts/mindmap.py fact add --entity "α波" --fact "频率8-13Hz，正常成人安静闭眼时出现在后头部"

# 查询
python3 scripts/mindmap.py get α波

# 生成摘要
python3 scripts/mindmap.py summarize α波
```

### 直接对话

告诉小社：
- "创建一个波形：β波，频率13-30Hz"
- "总结尖波的知识"
- "尖波和棘波有什么区别？"

## 脑电图输出示例

```
## 尖波

### 核心要点
- 频率：2-5 Hz
- 振幅：100-200 μV
- 形态：突发突止，尖锐
- 分布：局部或广泛
- 生理性：否

### 对比
| 波形 | 频率 | 临床意义 |
|------|------|----------|
| 尖波 | 2-5Hz | 癫痫特异性放电 |
| 棘波 | >5Hz | 癫痫发作 |

### 临床意义
高度提示癫痫，常见于部分性发作

### 鉴别诊断价值
需与伪差、发作性睡病鉴别

### 异常提示
尖波出现=异常，提示癫痫灶定位

### 本质总结
尖波是癫痫的特异性放电标志，反映大脑神经元异常同步化放电。
```

## 数据存储

```
memory/medical-mindmap/
├── graph.jsonl       # 实体和关系
└── knowledge/        # 知识库
    ├── disease/
    ├── examination/
    ├── waveform/
    └── ...
```

## 许可证

MIT License

## 作者

斓光
