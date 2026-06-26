# 安装指南

## 前置条件
- macOS（M系列芯片推荐）或 Linux
- Python 3.12+（需支持 OpenSSL 3.0+）
- torch（MPS/CPU均可）

## 安装步骤

### 1. 安装依赖
```bash
pip3 install sqlite-vec pysqlite3 sentence-transformers
```

### 2. 下载中文embedding模型
如果网络能访问HuggingFace：
```bash
python3 -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('shibing624/text2vec-base-chinese')"
```

如果HuggingFace被墙（中国大陆），设置镜像：
```bash
export HF_ENDPOINT=https://hf-mirror.com
python3 -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('shibing624/text2vec-base-chinese')"
```

或手动下载：
```bash
mkdir -p ~/.cache/huggingface/hub/models--shibing624--text2vec-base-chinese/snapshots/local
cd ~/.cache/huggingface/hub/models--shibing624--text2vec-base-chinese/snapshots/local
# 用curl从镜像下载config.json, pytorch_model.bin, tokenizer.json, tokenizer_config.json, vocab.txt
```

### 3. 初始化数据库
```bash
python3 scripts/memdb.py stats  # 首次运行自动建库
```

### 4. 导入现有记忆（可选）
如果有 Markdown 格式的记忆文件：
```bash
python3 scripts/memdb.py import --dir ./entities
```

### 5. 验证
```bash
python3 scripts/memdb.py search "测试搜索" --limit 3
```

## 注意事项
- Python 3.9 内置 sqlite3 不支持 load_extension，需安装 pysqlite3
- 推荐用 Homebrew 的 Python 3.12（macOS）：`/opt/homebrew/bin/python3.12`
- 模型约400MB，首次加载需下载
- M系列Mac会自动用MPS加速embedding计算
