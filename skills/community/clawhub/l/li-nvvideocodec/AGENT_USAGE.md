# Agent 使用说明

## 🤖 如何将此skill集成到Qwen Code Agent

### 1. Skill注册

在Qwen Code的配置中添加此skill：

```json
{
  "skills": [
    {
      "name": "li_nvvideocodec",
      "path": "E:\\视频输出\\docker-2021\\li_nvvideocodec",
      "description": "NVIDIA AV1视频批量压缩工具",
      "entry_point": "scripts/compress_videos.py"
    }
  ]
}
```

### 2. Agent调用方式

Agent可以通过以下方式使用该skill：

#### 方式1：直接运行脚本
```bash
python E:\视频输出\docker-2021\li_nvvideocodec\scripts\compress_videos.py [参数]
```

#### 方式2：交互式对话
当用户提到以下关键词时，agent可以主动推荐使用此skill：
- "压缩视频"
- "减少视频空间"
- "AV1编码"
- "视频优化"
- "NVIDIA编码"

### 3. 参数提取示例

当用户说："帮我压缩E盘的视频"

Agent应解析：
```python
{
    "input_dir": "E:\\视频输出\\docker-2021",
    "profile": "B",  # 推荐默认方案
    "test_mode": True,  # 首次使用建议测试模式
    "no_confirm": False
}
```

然后执行：
```bash
python scripts/compress_videos.py -i "E:\视频输出\docker-2021" -p B --test
```

### 4. 工作流程建议

Agent应该：

1. **首次使用**：
   - 自动启用测试模式
   - 只压缩1-2个视频
   - 让用户确认质量

2. **用户确认后**：
   - 关闭测试模式
   - 执行完整压缩

3. **压缩完成后**：
   - 显示压缩报告
   - 建议用户检查输出目录
   - 询问是否删除原文件（**谨慎！**）

### 5. 错误处理

如果脚本返回错误，Agent应该：

```python
# 检查环境
1. 运行: nvidia-smi
   → 如果失败：提示安装NVIDIA驱动

2. 运行: ffmpeg -version
   → 如果失败：提示安装FFmpeg

3. 运行: ffmpeg -encoders | grep av1_nvenc
   → 如果失败：提示FFmpeg不支持av1_nvenc

# 检查压缩效果
4. 如果压缩验证失败（文件变大）：
   → 说明原视频已高效压缩
   → 建议保持原样
```

### 6. 用户对话示例

**场景1：首次使用**

```
用户: 我想压缩一下docker-2021目录下的视频

Agent: 我检测到你有NVIDIA RTX 5060 Ti显卡，可以使用AV1硬件编码压缩视频。
       预计可以节省65-75%的空间。

       我建议：
       1. 先测试压缩1个视频，确认效果
       2. 满意后再批量压缩

       要开始测试吗？（使用方案B：720p，平衡质量和大小）

用户: 好的

Agent: 正在执行: python compress_videos.py -i "E:\视频输出\docker-2021" -p B --test
       [显示压缩进度...]
       
       测试完成！请检查输出目录的视频质量。
       如果满意，我可以继续压缩全部36个视频。
```

**场景2：B站视频**

```
用户: 压缩这些B站下载的视频

Agent: 我检测到这些视频来自B站，已经被高度压缩过。
       测试显示AV1压缩后文件反而变大了9%。

       建议：
       - 保持原样，不需要再次压缩
       - 这些视频已经是最优状态
```

### 7. 安全检查清单

Agent在执行压缩前应检查：

- [ ] 用户明确同意压缩
- [ ] 已说明原文件不会被删除
- [ ] 已说明输出目录位置
- [ ] 首次使用建议测试模式
- [ ] 已显示预估压缩效果

### 8. 输出结果处理

压缩完成后，Agent应该：

```python
# 解析脚本输出
total_files = 36
success_count = 36
failed_count = 0
original_size = "8.17 GB"
compressed_size = "2.5 GB"
saved_percent = "69.4%"

# 生成友好报告
print(f"✅ 压缩完成！")
print(f"   {success_count}/{total_files} 个视频成功压缩")
print(f"   原始大小: {original_size}")
print(f"   压缩后: {compressed_size}")
print(f"   节省: {saved_percent}")
print(f"\n📁 输出目录: E:\\视频输出\\docker-2021_compressed_B_平衡压缩(推荐)")
print(f"\n💡 建议：")
print(f"   1. 先检查输出目录的视频质量")
print(f"   2. 确认满意后，可以删除原文件释放空间")
print(f"   3. 原文件路径: E:\\视频输出\\docker-2021")
```

## 🔧 维护说明

### 更新脚本
- 直接修改 `scripts/compress_videos.py`
- 更新 `SKILL.md` 文档

### 版本管理
- 当前版本: 1.0.0
- 每次重大修改后更新版本号

### 依赖检查
定期检查：
- FFmpeg版本
- NVIDIA驱动版本
- Python依赖库版本
