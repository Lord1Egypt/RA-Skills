# Deduplication Rules (候选人去重规则)

本文档定义了候选人去重的 7 级指纹优先级和标准化规则，用于在批量搜索和爬取过程中识别和去除重复候选人。

## 去重的重要性

在多源搜索（LinkedIn、Scholar、GitHub、个人主页等）过程中，同一候选人可能被多次发现。去重确保：
- 避免重复联系
- 合并多源信息获得更完整档案
- 提高外联效率

---

## 7 级指纹优先级

候选人指纹按照以下优先级生成，优先使用更可靠的标识符：

| 级别 | 标识符类型 | 优先级 | 说明 | 示例 |
|-----|-----------|--------|------|------|
| 1 | **Email** | 🔴 最高 | 最可靠的唯一标识 | `wei.zhang@example.com` |
| 2 | **Google Scholar** | 🟠 高 | 学术唯一标识 | `scholar.google.com/citations?user=ABC123` |
| 3 | **LinkedIn** | 🟡 中高 | 职业社交唯一标识 | `linkedin.com/in/wei-zhang` |
| 4 | **GitHub** | 🟡 中 | 代码开发唯一标识 | `github.com/weizhang` |
| 5 | **个人网站** | 🟢 中低 | 个人域名 | `weizhang.com`, `weizhang.github.io` |
| 6 | **组合指纹** | 🟢 低 | 姓名+学校+领域 | `composite:a1b2c3d4` |
| 7 | **来源URL** | ⚪ 最低 | 搜索结果页面 | `source:f5e6d7c8` |

---

## 指纹生成逻辑

```
function generate_fingerprint(candidate):
    # 1. Email (最强)
    if candidate.email:
        return "email:" + normalize_email(candidate.email)

    # 2. Google Scholar
    if candidate.google_scholar_url:
        return "scholar:" + normalize_url(candidate.google_scholar_url)

    # 3. LinkedIn
    if candidate.linkedin_url:
        return "linkedin:" + normalize_url(candidate.linkedin_url)

    # 4. GitHub
    if candidate.github_url:
        return "github:" + normalize_url(candidate.github_url)

    # 5. Personal Website
    if candidate.personal_website:
        return "website:" + normalize_url(candidate.personal_website)

    # 6. 组合指纹 (弱标识)
    if candidate.name and (candidate.school or candidate.field):
        identity = f"{name}|{school}|{field}"
        hash = md5(identity).hexdigest()[:16]
        return "composite:" + hash

    # 7. 来源 URL (最后手段)
    if candidate.source_url:
        hash = md5(candidate.source_url).hexdigest()[:16]
        return "source:" + hash

    return "unknown:no_identity"
```

---

## 标准化规则

### Email 标准化

```python
def normalize_email(email: str) -> str:
    """
    标准化邮箱地址
    """
    if not email or email == "N/A":
        return ""

    # 转小写，去除空格
    return email.lower().strip()

# 示例
"Wei.Zhang@Tsinghua.edu.cn" → "wei.zhang@tsinghua.edu.cn"
" weizhang@gmail.com "      → "weizhang@gmail.com"
```

### URL 标准化

```python
def normalize_url(url: str) -> str:
    """
    标准化 URL
    """
    if not url or url == "N/A":
        return ""

    url = url.lower().strip()

    # 移除协议
    url = re.sub(r'^https?://', '', url)

    # 移除 www.
    url = re.sub(r'^www\.', '', url)

    # 移除尾部斜杠
    url = url.rstrip('/')

    return url

# 示例
"https://www.linkedin.com/in/wei-zhang/"  → "linkedin.com/in/wei-zhang"
"http://weizhang.github.io/"               → "weizhang.github.io"
"scholar.google.com/citations?user=ABC123" → "scholar.google.com/citations?user=abc123"
```

### 姓名标准化

```python
def normalize_name(name: str) -> str:
    """
    标准化姓名
    """
    if not name or name == "N/A":
        return ""

    # 转小写，合并多个空格为一个
    return re.sub(r'\s+', ' ', name.lower().strip())

# 示例
"Wei  Zhang"   → "wei zhang"
"ZHANG, WEI"   → "zhang, wei"
"  Wei Zhang " → "wei zhang"
```

---

## 去重判断逻辑

### 单条检查

```python
def is_duplicate(new_candidate, seen_fingerprints: set) -> bool:
    """
    检查新候选人是否重复

    Args:
        new_candidate: 新发现的候选人
        seen_fingerprints: 已见过的指纹集合

    Returns:
        True 表示重复
    """
    fingerprint = generate_fingerprint(new_candidate)
    return fingerprint in seen_fingerprints
```

### 批量去重

```python
def deduplicate_batch(candidates: list) -> dict:
    """
    批量去重候选人

    Returns:
        {
            "unique": [...],          # 去重后的候选人
            "duplicates": [...],      # 被去除的重复项
            "duplicate_count": 0      # 重复数量
        }
    """
    seen = set()
    unique = []
    duplicates = []

    for candidate in candidates:
        fp = generate_fingerprint(candidate)

        if fp in seen:
            duplicates.append({
                "name": candidate.name,
                "fingerprint": fp,
                "source": candidate.source_url
            })
        else:
            seen.add(fp)
            unique.append(candidate)

    return {
        "unique": unique,
        "duplicates": duplicates,
        "duplicate_count": len(duplicates)
    }
```

---

## 信息合并逻辑

当发现同一候选人的多个来源信息时，按以下规则合并：

```python
def merge_profiles(existing: dict, new: dict) -> dict:
    """
    合并两个候选人档案，保留更完整的信息

    规则:
    - 如果现有值为空/N/A，使用新值
    - 列表字段：合并去重
    - 数值字段：取较大值
    """
    for field in ALL_FIELDS:
        existing_value = existing.get(field)
        new_value = new.get(field)

        # 跳过空值
        if is_empty(new_value):
            continue

        # 现有值为空，直接用新值
        if is_empty(existing_value):
            existing[field] = new_value

        # 列表字段：合并
        elif isinstance(existing_value, list):
            existing[field] = list(set(existing_value + new_value))

        # 数值字段：取较大值
        elif isinstance(existing_value, (int, float)):
            existing[field] = max(existing_value, new_value)

    return existing
```

---

## 常见去重场景

### 场景 1: 同一候选人多个邮箱

```
发现记录:
1. weizhang@gmail.com
2. wei.zhang@tsinghua.edu.cn
3. w.zhang@outlook.com

处理: 保留学术邮箱 (tsinghua.edu.cn)，其他记录为备用联系方式
```

### 场景 2: LinkedIn 和 Scholar 匹配

```
发现记录:
1. LinkedIn: linkedin.com/in/wei-zhang-123
   - 姓名: Wei Zhang
   - 职位: PhD Student at Tsinghua
2. Scholar: scholar.google.com/citations?user=ABC
   - 姓名: Wei Zhang
   - 机构: Tsinghua University
   - 研究领域: Reinforcement Learning

处理: 生成两个指纹都指向同一人，合并信息
```

### 场景 3: 姓名相同但不同人

```
发现记录:
1. Wei Zhang at Tsinghua University (RL方向)
2. Wei Zhang at Stanford University (CV方向)

处理: 使用组合指纹 (姓名+学校) 区分，确认为不同人
```

### 场景 4: 同一人多个来源

```
发现记录:
1. 从 LinkedIn 发现: linkedin.com/in/wei-zhang
2. 从 GitHub 发现: github.com/weizhang
3. 从个人主页发现: weizhang.github.io

处理: 三个来源都指向同一人，合并所有信息
```

---

## 去重最佳实践

1. **保留最可靠来源**: 学术邮箱 > 个人邮箱 > LinkedIn > GitHub
2. **保留最完整信息**: 合并时优先保留字段更完整的记录
3. **记录来源信息**: 保留每个字段的来源 URL，便于追溯
4. **人工审核**: 对于组合指纹（弱标识），建议人工审核
5. **定期清理**: 定期检查和清理重复候选人

---

## 指纹格式说明

| 指纹前缀 | 说明 | 示例 |
|---------|------|------|
| `email:` | 邮箱指纹 | `email:wei.zhang@tsinghua.edu.cn` |
| `scholar:` | Google Scholar 指纹 | `scholar:scholar.google.com/citations?user=abc123` |
| `linkedin:` | LinkedIn 指纹 | `linkedin:linkedin.com/in/wei-zhang` |
| `github:` | GitHub 指纹 | `github:github.com/weizhang` |
| `website:` | 个人网站指纹 | `website:weizhang.github.io` |
| `composite:` | 组合指纹 (MD5 hash) | `composite:a1b2c3d4e5f6g7h8` |
| `source:` | 来源 URL 指纹 (MD5 hash) | `source:f5e6d7c8b9a0c1d2` |
| `unknown:` | 无法识别 | `unknown:no_identity` |
