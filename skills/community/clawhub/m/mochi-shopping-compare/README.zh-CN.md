# 购物比较助手

[English](README.md)

核算商品总价，比较两次记录的价格变化，保留原始推广链接并导出对比报告。

## 实际功能

核算商品总价，比较两次记录的价格变化，保留原始推广链接并导出对比报告。

## 用法示例

安装后，把下面任意一条发给 AI；涉及文件或网址时，一并提供。

```text
比较我提供的三款洗衣机资料，按价格、容量、尺寸和保修列成表，缺少的信息单独标出。
```

```text
预算3000元，按我提供的商品报价和运费计算到手价，保留来源链接。
```

```text
把这几款商品按我的需求打分，导出比较表和选择理由。
```

## 导出结果

comparison.md / comparison.csv

文件保存在当前助手工作区，返回路径和 SHA256；记录与历史导出保留。

## 运行要求

OpenClaw、已连接的模型、Node.js 24.16+、当前助手工作区的读写权限。查询当前商品页面和价格时使用 OpenClaw 可用的联网浏览工具。

## 安装与开始使用

### MochiLab Skills 助手（推荐）

[首次安装并连接助手](https://mochilab.bz/Skills/Connect.aspx?lang=zh-CN)，然后发送：

```text
安装 mochi-shopping-compare
```

### ClawHub

[打开 Skill 页面](https://clawhub.ai/hznetnewpower/skills/mochi-shopping-compare)，或在当前助手工作区执行：

```text
npx clawhub@latest install @hznetnewpower/mochi-shopping-compare
```

### GitHub

[打开源码目录](https://github.com/hznetnewpower/mochilab-free-skills/tree/main/skills/mochi-shopping-compare)。下载仓库 ZIP，将 `skills/mochi-shopping-compare` 放入当前助手工作区的 `skills/` 目录。

安装后新建对话。

## 详细操作说明

[查看技能操作契约](SKILL.md)。命令、字段名和文件路径保留原样；按当前助手工作区执行，先核对依赖，再检查实际输出。
