# Kiri Engine — 3D 扫描重建 API 技能

> 调用 KIRI Engine API 生成 3D 模型（照片级扫描 / 无特征物体扫描）或高斯泼溅（3DGS）资产

---

## 首次配置（必须）

### 1. 获取 API Key
1. 注册 KIRI Engine 开发者账号：https://www.kiriengine.com/
2. 在 API Settings 页面创建 API Key（格式：`kiri-<random-string>`）
3. 注册地址：https://www.kiriengine.com/api-settings

### 2. 存储 API Key
```powershell
# 将 API Key 写入配置文件（仅本机可见）
$configPath = "$env:USERPROFILE\.kiri-engine-config.json"
@{ apiKey = "kiri-你的密钥" } | ConvertTo-Json | Set-Content $configPath -Encoding UTF8
```

### 3. 检查余额（可选，建议首次使用）
```powershell
powershell -ExecutionPolicy Bypass -File scripts/kiri-engine.ps1 balance
```

---

## 扫描类型与参数

生成前**必须向用户确认以下所有选项**，缺一不可：

### A. 算法选择

| 算法 | calculateType | 适用场景 | 输出格式 |
|------|:---:|------|------|
| **Photo Scan**（照片级扫描） | 1 | 常规物体、有纹理表面 | OBJ / FBX / GLB / USDZ / STL |
| **Featureless Scan**（无特征扫描） | 2 | 光滑/无纹理/反光表面（如陶瓷、金属） | OBJ / FBX / GLB / USDZ / STL |
| **3DGS Scan**（高斯泼溅） | 3 | 真实感场景复刻、NeRF 替代方案 | PLY + 3DGS 格式 |

### B. 输入方式

| 输入方式 | 约束 |
|---------|------|
| **视频上传** | 分辨率 ≤ 1920×1080，时长 ≤ 3 分钟 |
| **图片集上传** | 20~300 张（最少 20 张保证质量） |

### C. 各算法专属参数

**Photo Scan**：
| 参数 | 值域 | 默认 | 说明 |
|------|------|:---:|------|
| modelQuality | 1/2/3 | 1 | 模型精度（1=标准, 2=中, 3=高） |
| textureQuality | 1/2/3 | 1 | 贴图质量（同上） |
| fileFormat | OBJ/FBX/GLB/USDZ/STL | OBJ | 输出格式 |
| isMask | 0/1 | 1 | 是否自动抠背景 |
| textureSmoothing | 0/1 | 1 | 贴图平滑 |

**Featureless Scan**：
| 参数 | 值域 | 默认 | 说明 |
|------|------|:---:|------|
| fileFormat | OBJ/FBX/GLB/USDZ/STL | OBJ | 输出格式 |

**3DGS Scan**：
| 参数 | 值域 | 默认 | 说明 |
|------|------|:---:|------|
| isMesh | 0/1 | 0 | 是否生成网格 |
| isMask | 0/1 | 0 | 是否自动抠背景 |

---

## 标准工作流

```
┌─────────────────────────────────────────────────┐
│ 1. 检查 API Key 是否配置                          │
│ 2. 查询余额（确保足够）                            │
│ 3. 询问用户：算法 / 输入方式 / 参数               │
│ 4. 确认文件路径（视频或图片集）                    │
│ 5. 验证文件合规（分辨率、时长、数量）              │
│ 6. 上传文件 → 获取 serialize                     │
│ 7. 轮询任务状态（每 30~60 秒）                    │
│ 8. 任务完成 → 下载 zip（60 分钟有效）             │
│ 9. 解压到用户指定目录                             │
│ 10. 报告完成 + 资产路径                           │
└─────────────────────────────────────────────────┘
```

---

## 任务时长估算

| 算法 | 输入规模 | 预估时长 |
|------|---------|---------|
| Photo Scan | 视频 / <50 张图 | 10~30 分钟 |
| Photo Scan | >100 张图 / 高质量 | 30~90 分钟 |
| Featureless Scan | 视频 / 图片集 | 15~40 分钟 |
| 3DGS Scan | 视频 | 20~60 分钟 |
| 3DGS Scan | >100 张图 | 40~120 分钟 |

⚠️ **长时间任务规则**：超过 5 分钟必须主动汇报进度。

---

## 资产获取注意事项

1. **下载链接有效期 60 分钟** — 任务完成后必须立即下载
2. **服务器保留 3 天** — 超时自动删除，无法恢复
3. **下载后必须本地备份** — 建议存入 `projects/<项目名>/资产/3d/`

---

## 错误处理

| HTTP 码 | 含义 | 处理 |
|:---:|------|------|
| 200 | 成功 | — |
| 400 | 参数错误 | 检查文件合规性（分辨率/数量/格式） |
| 401 | 未授权 | API Key 无效或过期，重新配置 |
| 403 | 余额不足 | 提醒用户充值 |
| 500 | 服务器错误 | 重试，若持续则反馈用户 |

---

## 脚本调用方式

```powershell
# 检查余额
.\scripts\kiri-engine.ps1 balance

# 上传视频（Photo Scan）
.\scripts\kiri-engine.ps1 photo-video -video "C:\path\to\video.mp4" -modelQuality 1 -textureQuality 1 -fileFormat OBJ -isMask 1 -textureSmoothing 1

# 上传图片集（Photo Scan）
.\scripts\kiri-engine.ps1 photo-image -images "C:\path\to\images\*.jpg" -modelQuality 2 -fileFormat GLB -isMask 1 -textureSmoothing 1

# 上传视频（Featureless Scan）
.\scripts\kiri-engine.ps1 featureless-video -video "C:\path\to\video.mp4" -fileFormat OBJ

# 上传图片集（3DGS Scan）
.\scripts\kiri-engine.ps1 3dgs-image -images "C:\path\to\images\*.jpg" -isMesh 0 -isMask 0

# 查询任务状态
.\scripts\kiri-engine.ps1 status -serialize "796a6f52457844b4918db3eadd64becc"

# 下载模型（zip）
.\scripts\kiri-engine.ps1 download -serialize "796a6f52457844b4918db3eadd64becc" -output "C:\output\dir"
```

---

## 用户交互模板

生成前向用户确认：

```
🎬 KIRI Engine 3D 扫描任务

请确认以下参数：

1️⃣ 算法类型：Photo Scan / Featureless Scan / 3DGS Scan？
2️⃣ 输入方式：视频上传 / 图片集上传？
3️⃣ 文件路径：视频文件路径 或 图片集所在文件夹？
4️⃣ 输出格式：OBJ / FBX / GLB / USDZ / STL？（3DGS 除外）
5️⃣ 模型精度：标准(1) / 中(2) / 高(3)？（仅 Photo Scan）
6️⃣ 贴图质量：标准(1) / 中(2) / 高(3)？（仅 Photo Scan）
7️⃣ 自动抠背景：是(1) / 否(0)？
8️⃣ 贴图平滑：是(1) / 否(0)？（仅 Photo Scan）
9️⃣ 输出网格：是(1) / 否(0)？（仅 3DGS）
🔟 保存位置：模型下载到哪个目录？

⏱️ 预计生成时间：XX~XX 分钟
```

---

## API 参考

- Base URL: `https://api.kiriengine.app/api/`
- 官方文档: https://gentlebandit.feishu.cn/wiki/PsHawWV0gi2jePkmRoycwMwXnIc
- API Key 管理: https://www.kiriengine.com/api-settings
