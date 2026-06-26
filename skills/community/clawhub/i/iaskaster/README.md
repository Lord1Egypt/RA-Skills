# iaskaster

命理八字分析工具 - 调用外部 iaskaster API 生成专业 PDF 命理报告

## 项目结构

```
├── SKILL.md                    # 技能配置（必需）
├── package.json                # Node 包配置
├── index.js                    # 主入口文件（构建后生成）
├── src/
│   └── main.ts                 # 源代码
├── scripts/                    # 源码模式下的脚本目录
├── node_modules/               # 依赖（不包含在发布包中）
├── install.sh                  # 安装脚本
├── build.sh                    # 构建脚本
├── package.sh                  # 打包脚本
└── README.md                   # 使用说明
```

## 快速开始

### 安装依赖

```bash
npm install
```

### 构建单文件

```bash
npm run build
# 或
bash build.sh
```

构建后生成 `index.js`，所有功能合并到单个文件，无需 `scripts/` 目录。

### 使用

```bash
# 工具调用（Agent 模式）
node index.js --tool iaskaster_auto '{"action":"form"}'
node index.js --tool iaskaster_list '{}'
node index.js --tool iaskaster_download '{"action":"show","reportId":"123"}'
node index.js --tool iaskaster_balance '{}'
node index.js --tool iaskaster_recharge '{}'
node index.js --tool iaskaster_read '{"filename":"report.pdf"}'

# CLI 命令
node index.js list              # 查看报告列表
node index.js balance           # 查询余额
node index.js recharge          # 获取充值链接
node index.js recharge --open   # 打开充值页面
node index.js auto --action form

# 交互模式
node index.js --interactive
```

## 打包发布

### 源码模式（需 npm install）

```bash
bash package.sh source
```

### 单文件模式（无需 node_modules）

```bash
bash package.sh bundle
```

## 安装到 OpenClaw

```bash
bash install.sh
```
