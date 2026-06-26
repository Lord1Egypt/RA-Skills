# 🔧 thinkzone-image 环境变量配置方案

## ⚠️ 问题原因

**症状：** 在 `marketing-xiaohongshu-operator` 中调用图片生成显示 API Key 无效

**原因：** 
- Windows 用户环境变量 ≠ Gateway 服务环境变量
- Gateway 作为服务运行，无法读取用户环境变量
- 需要显式设置环境变量给技能脚本

---

## ✅ 解决方案

### 方案 1：使用包装脚本（推荐）⭐

**已创建包装脚本：** `gen_image_wrapper.bat`

**使用方法：**
```bash
gen_image_wrapper.bat --prompt "一只金毛吃玉米" --model "doubao-seedream-5-0-260128"
```

**脚本位置：**
```
C:\Users\Administrator\.openclaw\workspace\skills\thinkzone-image\gen_image_wrapper.bat
```

**优点：**
- ✅ 自动设置环境变量
- ✅ 无需修改 Gateway 配置
- ✅ 所有 agent 都可以使用

---

### 方案 2：在技能脚本中硬编码（备选）

修改 `gen_image.py`，在 `get_config()` 函数中直接返回 API Key：

```python
def get_config():
    """Get configuration from environment variables or defaults."""
    api_key = os.environ.get("THINKZONE_API_KEY")
    base_url = os.environ.get("THINKZONE_BASE_URL", "https://open.thinkzoneai.com")
    
    # Fallback to hardcoded values if env vars not set
    if not api_key:
        api_key = "amags_b6324919c0056a78dc326ef06011ecc7d2af896b6b659c216371e55d66895dac"
    
    if not api_key:
        print("Error: THINKZONE_API_KEY not set", file=sys.stderr)
        sys.exit(1)
    
    return api_key, base_url
```

---

### 方案 3：设置系统级环境变量（永久）

1. 以**管理员身份**打开 PowerShell
2. 运行：
```powershell
[System.Environment]::SetEnvironmentVariable("THINKZONE_API_KEY", "amags_b6324919c0056a78dc326ef06011ecc7d2af896b6b659c216371e55d66895dac", "Machine")
```
3. 重启 Gateway 服务：
```bash
openclaw gateway restart
```

---

## 🧪 测试方法

### 测试包装脚本

```bash
cd C:\Users\Administrator\.openclaw\workspace\skills\thinkzone-image
gen_image_wrapper.bat --prompt "一只可爱的猫咪" --model "doubao-seedream-5-0-260128" --size "2K"
```

### 测试直接调用（需要手动设置环境变量）

```powershell
$env:THINKZONE_API_KEY="amags_b6324919c0056a78dc326ef06011ecc7d2af896b6b659c216371e55d66895dac"
python scripts/gen_image.py --prompt "一只可爱的猫咪" --model "doubao-seedream-5-0-260128"
```

---

## 📝 已更新的文件

| 文件 | 说明 |
|------|------|
| `gen_image_wrapper.bat` | ✓ 新建 - 包装脚本 |
| `AGENTS.md` | ✓ 已更新 - 添加使用说明 |
| `gen_image.py` | 可选修改 - 添加硬编码 fallback |

---

## 🎯 推荐方案

**使用包装脚本（方案 1）**

**理由：**
- ✅ 不需要修改 Gateway 配置
- ✅ 不需要管理员权限
- ✅ 所有 agent 都能自动使用
- ✅ 易于维护和更新

---

**配置时间：** 2026-03-19  
**配置者：** 田渝米 🍚
