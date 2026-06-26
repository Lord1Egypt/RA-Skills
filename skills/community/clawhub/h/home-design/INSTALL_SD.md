# Stable Diffusion 安装指南

## ⚠️ 系统检测

检测到当前系统：
- **GPU**: 未检测到 NVIDIA 显卡
- **内存**: 7.1GB
- **磁盘**: 71GB 可用

## 🚨 重要提示

**Stable Diffusion 需要 NVIDIA 显卡（8GB+ VRAM 推荐）**

没有独立显卡的情况下：
- ❌ 运行速度极慢（单张图 5-10 分钟）
- ❌ 可能内存不足崩溃
- ❌ 体验很差

## ✅ 推荐方案：使用在线工具

对于没有 NVIDIA 显卡的用户，**强烈推荐使用在线工具**：

### 1. LiblibAI (哩布哩布) ⭐⭐⭐⭐⭐

**网址**: https://www.liblib.ai/

**优点**:
- ✅ 完全免费，每日有免费积分
- ✅ 中文界面，操作简单
- ✅ 模型丰富，质量高
- ✅ 无需安装，打开网页即用
- ✅ 生成速度快（1-2 分钟/张）

**使用步骤**:
1. 访问 https://www.liblib.ai/
2. 注册/登录账号（支持微信、QQ 登录）
3. 点击「AI 绘画」或「在线生成」
4. 复制提示词粘贴到 Prompt 框
5. 设置参数（分辨率 1024×768）
6. 点击生成，等待 1-2 分钟
7. 下载保存效果图

**免费额度**:
- 新用户注册送积分
- 每日签到领积分
- 生成一张图约消耗 1-2 积分

---

### 2. 吐司 TusiArt ⭐⭐⭐⭐

**网址**: https://tusiart.com/

**优点**:
- ✅ 免费额度充足
- ✅ 界面简洁
- ✅ 支持 ControlNet

**使用步骤**:
1. 访问 https://tusiart.com/
2. 注册/登录
3. 进入「在线绘制」
4. 粘贴提示词
5. 生成并下载

---

### 3. SeaArt ⭐⭐⭐⭐

**网址**: https://www.seaart.ai/

**优点**:
- ✅ 免费使用
- ✅ 功能丰富
- ✅ 支持中文

---

### 4. 通义万相（阿里）⭐⭐⭐⭐

**网址**: https://wanxiang.aliyun.com/

**优点**:
- ✅ 阿里出品，质量可靠
- ✅ 中文界面
- ✅ 有免费额度

---

## 🔧 如果坚持安装本地 SD

如果确实需要本地安装（有 NVIDIA 显卡后），参考以下步骤：

### 前置要求

- **GPU**: NVIDIA 显卡（GTX 1060 6GB 或更高）
- **VRAM**: 最低 4GB，推荐 8GB+
- **内存**: 最低 8GB，推荐 16GB+
- **磁盘**: 至少 50GB 可用空间
- **系统**: Windows 10/11 或 Linux

### 方法 1：WebUI 整合包（Windows 推荐）

**秋叶整合包**（最简单）:
1. 访问：https://github.com/AUTOMATIC1111/stable-diffusion-webui
2. 或搜索「秋叶 SD 整合包」
3. 下载解压
4. 运行 `启动器.exe`
5. 点击「一键启动」

### 方法 2：手动安装（Linux）

```bash
# 1. 安装依赖
sudo apt update
sudo apt install -y git python3 python3-pip python3-venv

# 2. 克隆 WebUI
cd ~
git clone https://github.com/AUTOMATIC1111/stable-diffusion-webui.git
cd stable-diffusion-webui

# 3. 运行（首次会自动下载模型）
./webui.sh

# 4. 访问 http://localhost:7860
```

### 方法 3：CPU 版本（不推荐，极慢）

```bash
cd ~
git clone https://github.com/AUTOMATIC1111/stable-diffusion-webui.git
cd stable-diffusion-webui

# 使用 CPU 模式
./webui.sh --use-cpu all --no-half

# 访问 http://localhost:7860
```

**警告**: CPU 模式生成一张图需要 5-10 分钟，仅用于测试！

---

## 📊 方案对比

| 方案 | 成本 | 速度 | 质量 | 推荐度 |
|------|------|------|------|--------|
| LiblibAI | 免费 | 快 | 高 | ⭐⭐⭐⭐⭐ |
| 吐司 TusiArt | 免费 | 快 | 高 | ⭐⭐⭐⭐ |
| 本地 SD（有显卡） | 免费 | 很快 | 高 | ⭐⭐⭐⭐ |
| 本地 SD（无显卡） | 免费 | 极慢 | 高 | ⭐ |

---

## 🎯 最佳实践

**对于当前系统，推荐方案**：

1. **立即使用**: LiblibAI 在线工具
   - 打开 https://www.liblib.ai/
   - 注册账号
   - 使用我们生成的提示词
   - 1-2 分钟出图

2. **未来升级**: 如果经常使用，考虑：
   - 购买 NVIDIA 显卡（RTX 3060 12GB 约 2000 元）
   - 或租用云 GPU（约 1-2 元/小时）

---

## 📝 使用我们的提示词

无论选择哪个在线工具，使用步骤相同：

1. **生成提示词**:
```bash
cd ~/.openclaw/skills/home-design
python scripts/generate_room_prompts.py \
  --style "现代简约" \
  --output /tmp/prompts.json
```

2. **查看提示词**:
```bash
cat /tmp/prompts.json | jq '.客厅.positive_prompt'
```

3. **复制到在线工具**:
   - 打开 LiblibAI
   - 粘贴提示词
   - 点击生成

4. **下载保存**:
   - 下载生成的图片
   - 保存到项目文件夹

---

## 💡 提示

- 8 个房间 × 1-2 积分 = 约 10-15 积分
- LiblibAI 每日签到可获得足够积分
- 生成时可调整「采样步数」20-30 步
- 分辨率建议 1024×768 或 1280×960

---

**需要我帮你生成提示词并指导如何使用 LiblibAI 吗？**
