# Hope Server Max API 常用查询示例

## 1. 查询待上传视频

### 统计待上传数量

```bash
hope_pending_count
```

输出：
```json
{"code":200,"msg":"操作成功","data":500}
```

### 查询待上传视频列表

```bash
hope_pending_list 20
```

### 查询特定频道的待上传视频

```bash
hope_download_list "cleanFlag=2&channelName=CopyCat-bili&pageSize=50"
```

---

## 2. 查询上传状态

### 查询失败的上传任务

```bash
hope_failed_uploads
```

### 查询执行中的上传任务

```bash
hope_running_uploads
```

### 查询某频道的上传记录

```bash
hope_upload_list "channelName=CopyCat-bili&pageSize=20"
```

### 查询今日上传记录

```bash
hope_today_upload
```

---

## 3. 查询频道信息

### 查询所有频道

```bash
hope_channel_list
```

### 查询特定类型的频道

```bash
hope_api "/system/channel/list" "channelType=bili&pageSize=50"
```

### 搜索频道名称

```bash
hope_channel_search "Copy"
```

### 刷新频道 Cookie

```bash
hope_channel_refresh 267
```

---

## 4. 查询引擎状态

### 查询所有引擎

```bash
hope_engine_all
```

---

## 5. 查询账户到期情况

### 查询即将到期的账户

```bash
hope_account_list "pageSize=50"
```

---

## 6. 统计分析

### 上传趋势

```bash
hope_upload_trend "beginTime=2026-04-01&endTime=2026-04-16"
```

### 下载趋势

```bash
hope_download_trend "beginTime=2026-04-01"
```

### 频道统计

```bash
hope_channel_stats
```

---

## 7. 失败诊断

### 查询失败排行

```bash
hope_upload_fail_list "pageSize=20"
```

### 查询失败日志

```bash
hope_upload_fail_log "hope02" "/path/to/video.mp4"
```

---

## 8. 批量操作

### 批量标记已清理

```bash
hope_download_clean "pk1,pk2,pk3"
```