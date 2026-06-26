# 压缩格式对比

## 测试结果

| 格式 | 命令 | 大小 | 压缩率 | 适用场景 |
|------|------|------|--------|---------|
| **tar.gz** | `--compress tar.gz` | 86MB | 61% | ✅ **推荐** - Linux/Mac 默认 |
| **zip** | `--compress zip` | 86MB | 61% | Windows 用户/跨平台 |
| **目录** | `--compress none` | 223MB | 0% | rsync 增量传输 |

## 使用示例

### tar.gz 格式（推荐）

```bash
# 打包
openclaw-migration-pro pack --output ~/openclaw-pack.tar.gz

# 归位
openclaw-migration-pro unpack --input ~/openclaw-pack.tar.gz

# 传输
openclaw-migration-pro transfer --input ~/openclaw-pack.tar.gz --target user@host:~/
```

**优点**:
- ✅ 压缩率高（节省 61% 空间）
- ✅ 单个文件，方便传输
- ✅ Linux/Mac 原生支持
- ✅ 适合网盘分享、邮件发送

**缺点**:
- ⚠️ Windows 需要安装 7-Zip 或 WSL

---

### zip 格式

```bash
# 打包
openclaw-migration-pro pack --compress zip --output ~/openclaw-pack.zip

# 归位
openclaw-migration-pro unpack --input ~/openclaw-pack.zip
```

**优点**:
- ✅ 压缩率高（节省 61% 空间）
- ✅ 跨平台支持最好
- ✅ Windows/Mac/Linux 都原生支持
- ✅ 适合网盘分享、邮件发送

**缺点**:
- ⚠️ 需要安装 zip 命令（通常已预装）

---

### 目录格式（不压缩）

```bash
# 打包
openclaw-migration-pro pack --compress none --output ~/openclaw-pack/

# 归位
openclaw-migration-pro unpack --input ~/openclaw-pack/

# rsync 增量传输
rsync -av ~/openclaw-pack/ user@host:~/openclaw-pack/
```

**优点**:
- ✅ 无需解压，直接访问
- ✅ 支持 rsync 增量同步
- ✅ 方便查看和修改内容

**缺点**:
- ❌ 体积大（223MB）
- ❌ 大量小文件，传输慢
- ❌ 不适合网盘分享

---

## 场景推荐

### 场景 1: 换电脑迁移

```bash
# 源电脑：打包为 tar.gz
openclaw-migration-pro pack --output ~/openclaw-pack.tar.gz

# 复制到 U 盘/网盘
cp ~/openclaw-pack.tar.gz /mnt/usb-drive/

# 目标电脑：归位
openclaw-migration-pro unpack --input /mnt/usb-drive/openclaw-pack.tar.gz
```

**推荐格式**: tar.gz 或 zip

---

### 场景 2: 定期备份

```bash
# 每周备份（tar.gz）
0 3 * * 0 openclaw-migration-pro pack --versioned --output ~/weekly-backup/

# 备份文件：
# ~/weekly-backup/openclaw-pack-2026-03-27-173000.tar.gz
# ~/weekly-backup/openclaw-pack-2026-04-03-173000.tar.gz
```

**推荐格式**: tar.gz（节省空间）

---

### 场景 3: 多设备同步

```bash
# 第一次：完整打包
openclaw-migration-pro pack --output ~/base-pack.tar.gz

# 传输到另一台设备
openclaw-migration-pro transfer --input ~/base-pack.tar.gz --target user@device2:~/

# 后续：使用 rsync 增量同步（目录格式）
openclaw-migration-pro pack --compress none --output ~/sync-pack/
rsync -av ~/sync-pack/ user@device2:~/sync-pack/
```

**推荐格式**: 
- 首次：tar.gz
- 增量：目录格式

---

### 场景 4: 网盘分享

```bash
# 打包为单个文件
openclaw-migration-pro pack --output ~/openclaw-pack.tar.gz

# 上传到网盘
# - 百度网盘
# - Google Drive
# - Dropbox
# - 阿里云盘

# 在另一台设备下载并归位
openclaw-migration-pro unpack --input ~/Downloads/openclaw-pack.tar.gz
```

**推荐格式**: tar.gz 或 zip（单个文件）

---

## 性能对比

### 打包速度

| 格式 | 时间 | 说明 |
|------|------|------|
| tar.gz | ~10 秒 | 包含压缩时间 |
| zip | ~12 秒 | 包含压缩时间 |
| 目录 | ~8 秒 | 无压缩 |

### 归位速度

| 格式 | 时间 | 说明 |
|------|------|------|
| tar.gz | ~12 秒 | 包含解压时间 |
| zip | ~14 秒 | 包含解压时间 |
| 目录 | ~10 秒 | 无解压 |

### 传输速度（100Mbps 网络）

| 格式 | 时间 | 说明 |
|------|------|------|
| tar.gz (86MB) | ~7 秒 | ✅ 快 |
| zip (86MB) | ~7 秒 | ✅ 快 |
| 目录 (223MB) | ~18 秒 | ❌ 慢 |

---

## 总结

**默认推荐**: tar.gz
- 压缩率高
- Linux/Mac 原生支持
- 单个文件方便传输

**Windows 用户**: zip
- 跨平台兼容性好
- 压缩率相同

**高级用户**: 目录格式
- 适合 rsync 增量
- 方便自定义修改

---

**更新时间**: 2026-03-27  
**版本**: v1.1.0
