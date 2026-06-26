# ThinkZone API 配置

## ⚠️ 需要设置环境变量

### Windows PowerShell（临时）
```powershell
$env:THINKZONE_API_KEY="amags_bb545cd144c21702ad19c12f8e5e881b465955da2b83f4b038ea11a385a00996"
```

### Windows（永久）
1. 右键"此电脑" → 属性 → 高级系统设置
2. 点击"环境变量"
3. 在"用户变量"或"系统变量"中新建：
   - 变量名：`THINKZONE_API_KEY`
   - 变量值：`amags_bb545cd144c21702ad19c12f8e5e881b465955da2b83f4b038ea11a385a00996`
4. 重启终端生效

### 验证配置
```powershell
echo $env:THINKZONE_API_KEY
```

---

## 🧪 测试命令

```powershell
cd C:\Users\Administrator\.openclaw\workspace\skills\thinkzone-image

# 使用 MiniMax 模型
python scripts/gen_image.py --prompt "一只可爱的金毛犬正在吃玉米" --model "image-01" --width 1024 --height 1024

# 使用 Seedream 模型
python scripts/gen_image.py --prompt "一只可爱的金毛犬正在吃玉米" --model "doubao-seedream-5-0-260128" --size "2K"
```

---

## 📝 可用模型

| 模型 | 命令 |
|------|------|
| **MiniMax Image 01** | `--model "image-01"` |
| **Seedream 5.0 Lite** | `--model "doubao-seedream-5-0-260128"` |
| **Gemini 3.1 Flash** | `--model "gemini-3.1-flash-image-preview"` |

---

配置时间：2026-03-19
