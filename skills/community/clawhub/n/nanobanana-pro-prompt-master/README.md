# NanobananaPro 生图大师

> NanobananaPro 官方认证首席生图提示词大师

[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](https://clawhub.ai/skills/nanobanana-pro)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

---

## 🎯 Skill 定位

**NanobananaPro 官方认证首席生图提示词大师** —— 专精于 NanobananaPro 平台的极致生图提示词生成系统

**核心使命：** 生成 100% 适配 NanobananaPro 平台、可直接复制粘贴落地、零废稿、零修改、零翻车的极致专业生图提示词

---

## ⚡ 快速开始

### 安装

```bash
claw skill install nanobanana-pro
```

### 触发词

- `NanobananaPro` / `nano` / `纳米香蕉` / `nbpro`
- `生图` / `生成图片` / `做图` / `AI 绘画`
- `提示词` / `prompt` / `咒语`
- `分镜` / `镜头` / `视频生成`

### 使用示例

**示例 1：电商产品图**
```
帮我生成一个口红产品图，要高端商业质感，发小红书
```

**示例 2：人像写真**
```
生成一个职场女性形象照，现代办公室背景，专业自信
```

**示例 3：视频分镜**
```
生成一个 15 秒抖音短视频，赛博朋克风格，未来都市夜景
```

---

## 🏗️ 核心能力

### 1. 智能需求解析
- 自动提取画面比例、风格、主体等关键元素
- 信息缺失时智能补全提问
- 提供选项降低用户思考成本

### 2. 专业知识库
- **50+ 大师级风格库** - 电影感/艺术风/现代风/二次元/摄影
- **15+ 场景模板** - 人像/场景/产品/特殊类全覆盖
- **7 类负面词库** - 针对性解决人物崩坏/质量问题/风格跳变
- **8 本专业手册** - 构图/光影/色彩/镜头/平台规格

### 3. 提示词生成
- **6 段式标准结构** - 主控前缀 + 核心描述 + 场景 + 风格 + 光影 + 画质
- **权重优化** - 核心关键词自动强化至 1.3-1.5
- **质量验证** - 输出前 7 项检查确保可执行性

### 4. 视频生成支持
- **首尾帧锁定** - 确保 90% 元素一致性
- **单镜优先** - 新手友好方案
- **防闪烁核心** - 精准锁定光源三要素

---

## 📚 知识库结构

```
nanobanana-pro/
├── SKILL.md                          # 核心指令文件
├── references/                       # 知识库（按需加载）
│   ├── style-library.md              # 50+ 大师级风格库
│   ├── prompt-templates.md           # 15+ 场景提示词模板
│   ├── negative-prompts.md           # 7 类负面提示词库
│   ├── composition-guide.md          # 构图法则手册
│   ├── lighting-guide.md             # 光影系统手册
│   ├── color-theory.md               # 色彩理论手册
│   ├── camera-lens-guide.md          # 相机/镜头参数手册
│   └── platform-specs.md             # NanobananaPro 平台规格
├── scripts/                          # 工具脚本
└── assets/examples/                  # 示例输出
```

---

## 🎨 输出格式

### 标准输出结构

```markdown
## 🎨 完整提示词（可直接复制）

```
[完整提示词内容]
```

## 📋 落地执行指南

1. **平台参数设置**
   - 比例：--ar [值]
   - 风格：--style [值]
   - 强度：--s [值]
   - 质量：--q [值]

2. **避坑技巧**
   - [技巧 1]
   - [技巧 2]
   - [技巧 3]

3. **优化方向**
   [可按需调整的参数]
```

---

## 💡 使用场景

### 电商场景
- 产品主图生成
- 电商营销视频
- 品牌视觉设计

### 创意场景
- 概念艺术创作
- 插画设计
- 艺术海报

### 人像场景
- 个人写真
- 商业人像
- 角色设计

### 视频场景
- 抖音/快手短视频
- B 站/YouTube 视频
- 电影感短片

---

## 🔧 扩展能力

### 提示词诊断优化

**常见问题诊断：**
- 人物变形 → 加强负面提示词 + 调整权重
- 风格跳变 → 锁定统一视觉体系
- 光影闪烁 → 固定光源三要素
- 首尾帧不匹配 → 强化锚点元素
- 画质模糊 → 提升质量参数 + 细节描述

### 平台适配推荐

| 平台 | 推荐比例 | 时长 | 风格建议 |
|------|----------|------|----------|
| 抖音 | 9:16 | 15-30s | 强节奏/高饱和 |
| 视频号 | 9:16/1:1 | 15-60s | 商业质感 |
| 小红书 | 3:4/1:1 | 10-30s | 清新/高级感 |
| B 站 | 16:9 | 30s+ | 电影感/二次元 |

---

## 🚀 版本记录

### v1.0.0 (2026-04-03)
- ✅ 初始版本发布
- ✅ 核心架构完成
- ✅ 50+ 风格库
- ✅ 15+ 场景模板
- ✅ 7 类负面词库
- ✅ 平台规格说明

---

## 📝 开发说明

### 技术栈
- OpenClaw Skill 框架
- TypeScript
- Markdown 知识库

### 本地开发
```bash
# 克隆仓库
git clone https://github.com/rfdiosuao/openclaw-skills.git

# 进入目录
cd nanobanana-pro

# 安装依赖
npm install

# 测试
npm test

# 发布
npm run publish
```

---

## 🤝 贡献指南

欢迎提交 Issue 和 Pull Request！

- **BUG 反馈：** https://github.com/rfdiosuao/openclaw-skills/issues
- **功能建议：** https://github.com/rfdiosuao/openclaw-skills/discussions

---

## 📄 许可证

MIT License

---

## 🔗 相关链接

- **ClawHub 页面：** https://clawhub.ai/skills/nanobanana-pro
- **GitHub 仓库：** https://github.com/rfdiosuao/openclaw-skills/tree/main/nanobanana-pro
- **NanobananaPro 官网：** https://nbpro.org
- **OpenClaw 文档：** https://docs.openclaw.ai

---

**NanobananaPro 生图大师 · 让每一张图都专业**
