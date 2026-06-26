# 发表状态与 CCF 评级模块

## 功能描述

自动查询论文的发表状态，识别是否已发表在会议/期刊，并获取 CCF（中国计算机学会）评级。

## 模块信息

- **模块文件**: `scripts/core/publication_status.py`
- **CCF 评级数据库**: 内置于模块中（第七版，2026 年 3 月更新）
- **数据库规模**: 422 个 venue（会议 275 个，期刊 147 个）

## 评级标准

| 等级 | 说明 | 权威度分数 |
|------|------|-----------|
| CCF-A | 顶级会议/期刊 | 1.0 |
| CCF-B | 优秀会议/期刊 | 0.8 |
| CCF-C | 良好会议/期刊 | 0.6 |
| 已发表未评级 | 有 venue 但未匹配 CCF | 0.5 |
| preprint | 预印本（如 arXiv） | 0.3 |

## 使用方式

发表状态查询**默认启用**，无需额外参数。

### 禁用权威度评分
```bash
python scripts/review.py --query "LLM reasoning" --no-authority
```

### 调整权威度权重
```bash
python scripts/review.py --query "LLM reasoning" --authority-weight 0.5
```

### 使用在线 API 查询（更准确但较慢）
```bash
python scripts/review.py --query "LLM reasoning" --use-api
```

## CCF 数据库统计

### 会议数据库

| 评级 | 数量 | 代表性会议 |
|------|------|-----------|
| A 类 | 65 | NeurIPS, ICML, ICLR, CVPR, ICCV, ECCV, ACL, EMNLP, NAACL, CCS, S&P, USENIX Security, NDSS, SIGMOD, VLDB, ICDE, KDD, WWW, SIGIR, ICSE, FSE, ISSTA, PLDI, POPL, OSDI, SOSP, SIGCOMM, INFOCOM |
| B 类 | 96 | ICANN, ICONIP, WACV, BMVC, ICIP, CIKM, RecSys, ECIR, ASIACRYPT, ESORICS, DSN, RAID, CHES |
| C 类 | 113 | IJCNN, ICPR, DASFAA, APWeb, ICC, GLOBECOM, LCN, ACNS, AsiaCCS, ICICS, TrustCom |

### 期刊数据库

| 评级 | 数量 | 代表性期刊 |
|------|------|-----------|
| A 类 | 28 | IEEE TPAMI, IJCV, JMLR, Artificial Intelligence, TACL, IEEE TIP, IEEE TIFS, TDSC, TOPLAS, TOSEM, TSE, TODS, TOIS, TKDE |
| B 类 | 53 | IEEE TMM, IEEE TNNLS, Pattern Recognition, Neural Networks, Machine Learning, KAIS, Computers & Security |
| C 类 | 62 | ESWA, Neurocomputing, Pattern Recognition Letters, NPL, Expert Systems with Applications |

## 匹配逻辑

- ✅ 期刊优先于会议匹配
- ✅ 长名称优先（更具体的名称优先）
- ✅ 词边界匹配（避免短键名误匹配）
- ✅ 保留 "transactions" 和 "journal" 关键词用于区分期刊/会议

## 测试命令

### 运行完整测试
```bash
python scripts/test_publication_status.py
```

### 测试特定期刊/会议
```bash
python scripts/test_publication_status.py --title "论文标题" --venue "IEEE Transactions on Multimedia"
```

### 显示数据库统计
```bash
python scripts/test_publication_status.py --show-db
```

### 交互式测试
```bash
python scripts/test_publication_status.py --interactive
```

## 扩展 CCF 评级数据库

如需添加新的会议/期刊评级，编辑 `scripts/core/publication_status.py` 中的字典：

```python
CCF_A_CONFERENCES = {
    "neurips": "A",
    "icml": "A",
    # 添加新的会议...
}
```

## 注意事项

1. **CCF 评级数据库**为本地内置，可能不完整。欢迎贡献更多会议/期刊评级。

2. **在线 API 查询**（`--use-api`）依赖 Semantic Scholar API，可能需要网络连接和 API key。

3. **边缘情况**: INTERSPEECH 等不在 CCF 列表中的会议正确识别为"未评级"。
