math-solver/
├── SKILL.md                          # 主要 Skill 文档（触发条件、用法、配置）
├── README.md                         # 项目概览和使用说明
├── skill.config.json                 # Skill 配置和元数据
│
├── scripts/                          # Python 脚本
│   ├── process_math_problem.py       # OCR 提取 → LaTeX 转换
│   └── generate_solution.py          # 生成解题指导和渲染配置
│
└── references/                       # 参考文档和示例
    ├── QUICKSTART.md                 # 快速开始指南
    └── EXAMPLES.md                   # 测试用例和示例场景

## 文件说明

### SKILL.md (核心文件)
- **作用**: OpenClaw 加载时读取的主文档
- **内容**: 
  - Skill 功能概述
  - 四种核心工作流
  - LaTeX 提取规则
  - 主题配置
  - 解题模式说明
  - 支持的数学领域
  - 输入/输出示例
  - API 集成说明

### README.md
- 项目总体描述
- 快速功能总结
- 性能指标
- 使用场景
- 故障排除
- 路线图

### skill.config.json
- 依赖声明 (PaddleOCR, math-images, Claude API)
- 默认配置项
- 支持的输入/输出格式
- 性能指标
- 元数据和标签

### scripts/process_math_problem.py
**功能**: 数学问题处理管道

核心类:
- `MathFormulaConverter` - 多格式 → LaTeX 转换
  - 分数、幂、根号、希腊字母
  - 求和、积分、极限
  - 验证 LaTeX 语法
  
- `MathProblemAnalyzer` - 分析问题类型
  - 识别数学领域 (代数、几何、微积分等)
  - 评估难度级别
  
- `MathProblemProcessor` - 完整处理流程
  - 提取公式
  - 分析问题
  - 输出结构化数据

使用: `python process_math_problem.py "问题文本" [problem_id]`

### scripts/generate_solution.py
**功能**: 解题引导和渲染配置

核心类:
- `SocraticGuide` - 苏格拉底式问题提示库
  - 理解问题 (5 个问题)
  - 概念识别 (4 个问题)
  - 方法选择 (4 个问题)
  - 执行步骤 (4 个问题)
  - 答案验证 (4 个问题)

- `DetailedExplainer` - 详细解题步骤生成
  - 问题重述
  - 关键概念
  - 分步解答
  - 答案验证

- `LaTeXRenderer` - LaTeX 渲染配置
  - 4 种主题 (light, dark, sepia, chalk)
  - 3 种字体大小 (small, medium, large)
  - DPI 选项 (150, 300, 600)
  - 生成渲染命令传给 math-images

- `SolutionGenerator` - 主类
  - 3 种解题模式 (socratic, detailed, quick)
  - 整合 OCR、分析、指导、渲染

使用: `python generate_solution.py "问题" 领域 [模式] [主题]`

### references/QUICKSTART.md
- 3 种安装方法
- 4 个详细使用示例
- 故障排除指南
- 高级用法

### references/EXAMPLES.md
- 4 个测试用例 (分数、二次方程、极限、批量处理)
- 3 个用户场景 (学生学习、作业检查、公式参考)
- 性能基准
- 集成示例
- 错误恢复策略
- 配置示例 (老师、学生、快速参考)
- 已知问题

## 工作流整合

```
用户输入 (图片/LaTeX)
    ↓
PaddleOCR skill (如果是图片)
    ↓
process_math_problem.py (提取 + LaTeX 转换)
    ↓
MathProblemAnalyzer (识别领域和难度)
    ↓
generate_solution.py (选择解题模式)
    ↓
SocraticGuide / DetailedExplainer (生成内容)
    ↓
LaTeXRenderer (配置渲染参数)
    ↓
math-images skill (生成 PNG)
    ↓
用户获得: 公式 PNG + 解题指导
```

## 关键特性映射

| 功能 | 实现位置 |
|------|---------|
| 图片 OCR | SKILL.md + PaddleOCR skill |
| LaTeX 转换 | process_math_problem.py |
| 公式渲染 | generate_solution.py + math-images skill |
| 苏格拉底式指导 | generate_solution.py (SocraticGuide) |
| 详细解答 | generate_solution.py (DetailedExplainer) |
| 主题支持 | skill.config.json + LaTeXRenderer |
| 领域识别 | MathProblemAnalyzer |
| 难度评估 | MathProblemAnalyzer |
| 批量处理 | 由 OpenClaw 框架支持 |

## 扩展点

### 添加新的数学符号
编辑 `process_math_problem.py` 中的 `PATTERNS` 字典

### 添加新主题
编辑 `generate_solution.py` 中的 `THEME_CONFIGS`

### 添加新问题类型的引导
编辑 `generate_solution.py` 中的 `SOCRATIC_PATTERNS`

### 支持新的数学领域
编辑 `MathProblemAnalyzer.DOMAIN_KEYWORDS`

## 部署到 ClawHub

```bash
# 打包 Skill
python -m scripts.package_skill ./math-solver

# 发布到 ClawHub
npx clawhub publish ./math-solver.skill
```

