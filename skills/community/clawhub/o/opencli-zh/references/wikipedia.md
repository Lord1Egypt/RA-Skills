# Wikipedia

## 常用模式

### 搜索
```bash
opencli wikipedia search "马斯克"
opencli wikipedia search "Elon Musk" --limit 10
```

### 摘要
```bash
opencli wikipedia summary "Elon Musk"
```

### 热门词条
```bash
opencli wikipedia trending --limit 10
```

### 随机词条
```bash
opencli wikipedia random
```

## 最小说明

- Wikipedia 多数命令属于公开读操作，不依赖浏览器登录态。
- 若中文查询结果偏离目标，可补试英文词条名。
