---
name: hunyuan-image
description: 腾讯混元生图API - 根据文本描述生成AI图像
homepage: https://cloud.tencent.com/document/product/1729/105969
metadata: {"clawdbot":{"emoji":"🎨","requires":{"bins":["python"],"packages":["tencentcloud-sdk-python"],"env":["TENCENT_SECRET_ID","TENCENT_SECRET_KEY"]},"primaryEnv":"TENCENT_SECRET_ID"}}
---

# Hunyuan Image - 腾讯混元生图

基于腾讯混元大模型的AI图像生成服务。

## 功能

- 文本生成图像
- 支持多种分辨率
- 支持多种绘画风格
- 支持参考图引导
- 支持超分增强

## 前置要求

### 1. 安装Python依赖

```bash
pip install tencentcloud-sdk-python
```

### 2. 配置腾讯云密钥

**需要的环境变量**：
- `TENCENT_SECRET_ID` - 腾讯云SecretId
- `TENCENT_SECRET_KEY` - 腾讯云SecretKey

```powershell
# Windows PowerShell - 永久设置
[Environment]::SetEnvironmentVariable("TENCENT_SECRET_ID", "your-secret-id", "User")
[Environment]::SetEnvironmentVariable("TENCENT_SECRET_KEY", "your-secret-key", "User")

# 或临时设置（当前会话）
$env:TENCENT_SECRET_ID = "your-secret-id"
$env:TENCENT_SECRET_KEY = "your-secret-key"
```

**获取密钥步骤**：
1. 访问 https://console.cloud.tencent.com/cam/capi
2. 点击「新建密钥」
3. 复制 SecretId 和 SecretKey
4. **⚠️ 注意**：SecretKey 只显示一次，请妥善保存

### 3. 验证配置

```powershell
# 检查环境变量是否已设置
if ($env:TENCENT_SECRET_ID -and $env:TENCENT_SECRET_KEY) {
    Write-Host "✅ 环境变量已配置"
} else {
    Write-Host "❌ 请设置 TENCENT_SECRET_ID 和 TENCENT_SECRET_KEY"
}

# 测试生成
python scripts/generate.py "一只小猫"
```

## 使用方法

### 基础用法

```bash
# 生成图片
python {baseDir}/scripts/generate.py "雨中竹林小路"

# 指定风格
python {baseDir}/scripts/generate.py "少女, 樱花, 动漫风格" --style 201

# 指定分辨率
python {baseDir}/scripts/generate.py "未来城市" --resolution 1024:768

# 生成多张
python {baseDir}/scripts/generate.py "山水画" --num 4
```

### 参数说明

| 参数 | 说明 | 示例 |
|------|------|------|
| prompt | 文本描述（必填） | "雨中竹林小路" |
| --style | 绘画风格编号 | 201（动漫） |
| --resolution | 分辨率 | 1024:1024, 768:1024 |
| --num | 生成数量（1-4） | 2 |
| --negative | 反向提示词 | "黑色,模糊" |
| --clarity | 超分选项 | x2, x4 |
| --seed | 随机种子 | 12345 |
| --logo | 添加水印（API级别，默认不添加） | 可选 |
| --output | 输出目录 | ./images |

### 风格列表（常用）

| 编号 | 风格 |
|------|------|
| 101 | 水墨画 |
| 102 | 概念艺术 |
| 103 | 油画 |
| 104 | 水彩画 |
| 201 | 动漫 |
| 202 | 日本动画 |
| 301 | 3D卡通 |
| 401 | 肖像画 |
| 501 | 赛博朋克 |
| 601 | 蒸汽波 |

完整列表：https://cloud.tencent.com/document/product/1729/105846

## 输出

生成的图片保存在 `{output}/{date}/{job_id}/` 目录下：
- `image_0.png` - 生成的图片
- `info.json` - 任务信息（包含扩写后的描述）

## 注意事项

1. **异步接口**：API是异步的，需要等待任务完成
2. **并发限制**：默认1个并发
3. **地域限制**：仅支持 `ap-guangzhou`
4. **Prompt扩写**：默认开启，可提升生成效果
5. **水印**：默认不添加水印。使用 `--logo` 参数可添加"图片由AI生成"水印

## 踩坑记录

### 1. 状态码陷阱 ⚠️

**坑**：API返回 `JobStatusCode: 5` 可能是成功！需要检查 `ResultDetails`：

```python
if status == '4' or (status == '5' and result.get('ResultDetails') == ['Success']):
    print('✅ 实际生成成功！')
    # 处理图片...
```

### 2. Prompt内容限制 🚫

**坑**：某些历史人物名字可能触发内容审核

**实测结果**：
| Prompt | 结果 |
|--------|------|
| "李白" | ❌ 失败 |
| "唐朝诗人李白" | ❌ 失败 |
| "古代诗人，白衣少年" | ✅ 成功 |
| "一只可爱的猫咪" | ✅ 成功 |

**建议**：避免直接使用敏感历史人物全名，用描述性词汇替代

### 3. 网络超时问题 🌐

**坑**：API偶尔连接超时（`ConnectTimeoutError`）

**解决**：
- 增加重试机制
- 设置合理的超时时间（60秒以上）
- 使用稳定的网络环境

### 4. 风格编号无效 ❌

**坑**：文档中的风格编号 `201` 实际调用时报错 `StyleId参数有误`

**解决**：不传 `--style` 参数，让API自动选择默认风格

### 5. 图片下载超时问题 ⏱️

**坑**：下载大图片时可能超时

**解决**：增加超时时间设置
```python
# 设置合理的超时时间（30秒）
urllib.request.urlopen(req, timeout=30)
```

### 6. Prompt扩写效果 ✨

**惊喜**：开启扩写（默认）后，简单描述会被AI优化为详细描述

**示例**：
- **输入**："一只可爱的猫咪"
- **扩写后**："一只可爱的猫咪，拥有圆润的身体和柔软的毛发，它的眼睛大而圆，流露出友好的笑容..."

**建议**：保持原始描述简洁，让AI自动扩写提升效果

### 8. 并发限制 ⏳

**坑**：默认只有1个并发，同时提交多个任务会排队

**解决**：
- 顺序执行，等待前一个完成
- 或购买更多并发额度

### 最佳实践 💡

1. **Prompt编写**：简洁描述 + 让AI扩写 > 冗长描述
2. **错误处理**：检查 `ResultDetails` 而不仅是状态码
3. **内容规避**：用"古代诗人"代替"李白"，用"美少女"代替具体人名
4. **网络重试**：生产环境务必添加重试机制
5. **分辨率**：竖版推荐 `768:1024`，横版推荐 `1024:768`

## 示例

```bash
# 生成动漫风格头像
python scripts/generate.py "可爱女孩, 短发, 微笑, 樱花背景" --style 201 --resolution 768:768

# 生成赛博朋克壁纸
python scripts/generate.py "未来城市, 霓虹灯, 雨夜" --style 501 --resolution 1920:1080 --clarity x2

# 生成水墨画
python scripts/generate.py "山水, 瀑布, 松树, 云雾" --style 101 --resolution 1024:768
```

## 相关链接

- [API文档](https://cloud.tencent.com/document/product/1729/105969)
- [腾讯云控制台](https://console.cloud.tencent.com/cam/capi)
- [风格列表](https://cloud.tencent.com/document/product/1729/105846)

## 许可证

MIT License

---

[English Version](./README.md)
