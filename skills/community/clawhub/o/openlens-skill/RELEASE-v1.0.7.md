# OpenLens-Skill v1.0.7 发布说明

## 🎯 版本亮点

**OpenLens-Skill 1.0.7** 是一个完全重写的本地优先 AI 媒体生成引擎，支持：
- ✅ 文本→视频 (T2V)
- ✅ 文本→图像 (T2I)  
- ✅ 图像→视频 (I2V)
- ✅ 视频→视频 (V2V)
- ✅ 文本→文本 (T2T) 提示词增强

## 🚀 核心特性

### 1. 双模式架构
- **Mode A (技能模式)**: 作为 OpenClaw 技能导入，调用 `run_openlens_task()`
- **Mode B (GUI 模式)**: 独立运行，启动 `localhost:8501` Streamlit 界面

### 2. 智能本地存储
```python
outputs/
├── T2I/20260304_011122_flux.1-schnell.png
├── T2V/20260304_011233_video_wan2.6-t2v.mp4
├── I2V/20260304_011344_video_wan2.6-i2v.mp4
└── V2V/20260304_011455_video_wan2.6-i2v.mp4
```

### 3. 完整 API 兼容性
- OpenAI 兼容格式
- OnlyPix API 已测试通过
- 支持自定义 API 端点

## 📦 安装方式

### GitHub 直接安装
```bash
git clone https://github.com/openclawrr/openlens-skill.git
cd openlens-skill
pip install -r requirements.txt
```

### ClawHub 安装（即将支持）
```bash
clawhub install openlens-skill
```

## 🛠️ 使用方法

### 方式1: CLI 命令
```bash
cd openlens-skill
python3 skill_main.py \
  --url https://api.onlypixai.com/v1 \
  --api-key YOUR_KEY \
  --model video/wan2.6-t2v \
  --prompt "Sunset over the ocean" \
  --task T2V \
  --resolution 16:9 \
  --duration 10
```

### 方式2: Python 导入
```python
from skill_main import run_openlens_task

result = run_openlens_task(
    url="https://api.onlypixai.com/v1",
    api_key="YOUR_KEY",
    model_id="video/wan2.6-t2v",
    prompt="A cat playing on grass",
    task_type="T2V",
    video_specs={
        "resolution": "16:9",
        "duration": 5,
        "fps": 24,
    },
)

if result["success"]:
    print(f"✅ 视频已保存到: {result['local_path']}")
```

### 方式3: 本地 GUI
```bash
cd openlens-skill
streamlit run skill_main.py
# 打开 http://localhost:8501
```

## 🎨 主要改进

### 🔧 技术修复
1. **API Payload 格式**: 从 `{"prompt": ...}` 改为 `{"input": {"prompt": ...}}`
2. **分辨率格式**: 支持 API 标准 `720p` 和 `1280*720` 格式
3. **错误处理**: 详细的 HTTP 错误日志和状态轮询
4. **依赖更新**: streamlit>=1.32.0, requests>=2.31.0, pillow>=10.0.0

### 🔒 安全增强
1. **配置保护**: `config.json` 加入 `.gitignore`
2. **密钥清理**: 从 Git 历史中彻底删除敏感配置
3. **模板配置**: 提供 `config.example.json` 作为安全模板

### 📦 发布优化
1. **工具定义**: `tool_definition.json` 支持 OpenClaw Agent 注册
2. **完整文档**: `SKILL.md` 指导 OpenClaw 如何调用
3. **子项目**: `openlens-web/` 支持 Streamlit Cloud 一键部署

## 📁 文件结构
```
openlens-skill/
├── skill_main.py          # 核心执行引擎 + GUI
├── tool_definition.json   # OpenClaw 工具定义
├── SKILL.md               # OpenClaw 学习文档
├── manifest.json          # ClawHub 元数据
├── CHANGELOG.md           # 版本历史
├── requirements.txt       # Python 依赖
├── config.example.json    # 配置模板
└── openlens-web/          # Streamlit Cloud 版本
    ├── app.py
    └── requirements.txt
```

## 🧪 测试状态
- ✅ API 连接测试: 通过
- ✅ 视频生成测试: 通过 (已生成 3.4MB 测试视频)
- ✅ 文件保存测试: 通过 (自动保存到本地目录)
- ✅ GUI 模式测试: 通过 (localhost:8501)
- ✅ CLI 模式测试: 通过

## 🆕 迁移指南

### 从旧版本升级
1. 备份 `config.json`
2. 更新代码: `git pull origin main`
3. 恢复配置: `cp config.example.json config.json` (填入密钥)
4. 更新依赖: `pip install -r requirements.txt`

### 首次安装
1. 克隆仓库
2. `cp config.example.json config.json`
3. 编辑 `config.json` 填入 API 密钥
4. `pip install -r requirements.txt`

## 🎬 示例
```python
# 生成猫咪玩耍视频
result = run_openlens_task(
    url="https://api.onlypixai.com/v1",
    api_key="sk-px-xxxxxxxx",
    model_id="video/wan2.6-t2v",
    prompt="Two cats playing on grass, sunny day, realistic",
    task_type="T2V",
    video_specs={"resolution": "16:9", "duration": 5, "fps": 24},
)
```

## 📞 支持
- GitHub Issues: https://github.com/openclawrr/openlens-skill/issues
- OpenClaw Discord: https://discord.com/invite/clawd

---

**发布日期**: 2026-03-04  
**维护者**: openclawrr  
**许可证**: MIT